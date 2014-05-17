from simulatorio import *
from laboratorylogic import *
from baseformulae import *
from laboratory import *

import argparse, threading, sys, copy
import pandas as pd
import numpy as np

'''
Main control flow is presented here.
'''

data_dir = "E:/git/glencrossbrunet/assess_lab/new-dataset/"
output_dir = "E:/git/glencrossbrunet/assess_lab/output/"
debug_dir = "E:/git/glencrossbrunet/assess_lab/debug/"
statistics_dir = "E:/git/glencrossbrunet/assess_lab/stats/"
datastream_name = "datastream_raw_short.txt"

# if false, then a laboratory must have a fumehood datapoint for *every* hour that is included in its analysis
use_incomplete_times = True


parameters = [["Reduced ACH at Day",4,7,2,4,0]
          ,["Current Operating Settings",4,10,4,10,0]
          ,["Reduced ACH at Night",4,8,3,6,0]
          ,["Reduced ACH Both",4,8,3,6,0]
          ,["Usage Reduction -15%",4,10,4,10,.15]
          ,["Usage Reduction -25%",4,10,4,10,.25]
          ,["Usage Reduction -30%",4,10,4,10,.30]
          ,["Usage Reduction -25%" + " with Reduced ACH",4,8,3,6,.25]
          ,["Usage Reduction with ACH Reduction",4,8,3,6,.25]]


def generate_result_for_lab_and_parameter(laboratory, description, new_ach_unoccupied_day, new_ach_occupied_day, new_ach_unoccupied_night, new_ach_occupied_night, new_fumehood_reduction_factor):
  laboratory.reset_and_calculate_mins(new_ach_unoccupied_day, new_ach_occupied_day, new_ach_unoccupied_night, new_ach_occupied_night, new_fumehood_reduction_factor)

  for hood in laboratory.fumehoods:
    hood.dataframe['occupancy'] = calculate_occupancy_series(hood.dataframe['percent_open'].index, laboratory.day_start, laboratory.night_start, laboratory.fumehood_occupancy_percent, 0.1)
    hood.dataframe['evacuation_cfm'] = calculate_hood_evacuation_series(hood, hood.dataframe['percent_open'], hood.dataframe['occupancy'])

  laboratory.dataframe['occupancy'] = aggregate_hood_occupancy_to_lab(laboratory.fumehoods)
  laboratory.dataframe['min_lab_evacuation_cfm'] = calculate_min_lab_evacuation_series(laboratory, laboratory.dataframe['occupancy'])
  laboratory.dataframe['min_summed_hood_evacuation_cfm'] = calculate_min_summed_hood_evacuation_series(laboratory.fumehoods, laboratory.dataframe['occupancy'])
  laboratory.dataframe['min_additional_hood_evacuation_cfm'] = calculate_min_additional_hood_evacuation_series(laboratory.dataframe['min_lab_evacuation_cfm'], laboratory.dataframe['min_summed_hood_evacuation_cfm'])
  laboratory.dataframe['fumehood_evacuation_cfm'] = np.sum([hood.dataframe['evacuation_cfm'] for hood in laboratory.fumehoods],axis=0)
  laboratory.dataframe['total_lab_evacuation'] = laboratory.dataframe[['min_lab_evacuation_cfm', 'fumehood_evacuation_cfm']].min(axis=1)

  laboratory.dataframe.to_csv(output_dir + laboratory.laboratory_name + "--dataframe.csv")


def main(argv=None):
  if argv is None:
    argv = sys.argv
  (laboratories, models, hoods) = load_simulator_objects(data_dir, debug_dir)
  hood_datastream = load_hood_datastream(data_dir + datastream_name, hoods)
  process_hood_datastream(hood_datastream, hoods)
  thead_set = {}
  for laboratory in laboratories:
    for parameter in parameters:
      generate_result_for_lab_and_parameter(copy.deepcopy(laboratory), parameter[0], parameter[1], parameter[2], parameter[3], parameter[4], parameter[5])
      sys.exit()
      # thread_set[(laboratory, parameter)] = threading.Thread(target=generate_result_for_lab_and_parameter, args = (laboratory, parameter[0], parameter[1], param[2], param[3], param[4], param[5]))

main()