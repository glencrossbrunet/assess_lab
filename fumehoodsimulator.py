from simulatorio import *
from laboratorylogic import *
from baseformulae import *
from laboratory import *
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.tools.plotting import bootstrap_plot, autocorrelation_plot, lag_plot
import argparse, threading, sys, copy, os
import pandas as pd
import numpy as np

"""
Main control flow is presented here.
"""
base_path = ""
data_dir = base_path + "input-uqam/"
datastream_name = "datastream_raw_processed.txt"
lab_result_f = None
postfix = ""

USE_EXISTING_VALUES = False

# if false, then a laboratory must have a fumehood datapoint for *every* hour that is included in its analysis
use_incomplete_times = True

parameters = pd.read_csv(data_dir + "parameters.csv", header=0, index_col=0)


def generate_result_for_lab_and_parameter(laboratory, parameter, output_dir, stats_dir, results_dir, simulation_name):
  laboratory.reset_and_calculate_mins(parameter)
  
  print laboratory.laboratory_name

  summary = pd.DataFrame()
  for hood in laboratory.fumehoods:
    key = str(hood)
    summary[key] = hood.dataframe['percent_open']

  summary.count(axis=0).transpose().to_csv(stats_dir + laboratory.laboratory_name + "--open-values-count-per-fumehood.csv")
  per_hour_count = summary.count(axis=1).transpose()
  per_hour_average = summary.mean(axis=1)

#  fig, ax = plt.subplots()
#  ax = per_hour_count.plot(kind="line", title=("Hood Data Frequency Over Time for " + laboratory.laboratory_name))
#  fig.tight_layout()
#  plt.savefig(stats_dir + laboratory.laboratory_name + "--open-values-count-per-hour.pdf")
#
#  fig, ax = plt.subplots()
#  fig = bootstrap_plot(per_hour_count, size=50, samples=100)
#  fig.suptitle("Hood Data Frequency Bootstrap Summary for " + laboratory.laboratory_name)
#  fig.tight_layout()
#  plt.savefig(stats_dir + laboratory.laboratory_name + "--open-values-count-per-hour-bootstrap_plot.pdf")
#  
#  fig, ax = plt.subplots()
#  ax = autocorrelation_plot(per_hour_count)
#  fig.suptitle("Hood Data Frequency Autocorrelation Summary for " + laboratory.laboratory_name)
#  fig.tight_layout()
#  plt.savefig(stats_dir + laboratory.laboratory_name + "--open-values-count-per-hour-autocorrelation_plot.pdf")
#
#  per_hour_count.to_csv(stats_dir + laboratory.laboratory_name + "--open-values-count-per-hour.csv")
#  per_hour_count.describe().to_csv(stats_dir + laboratory.laboratory_name + "--open-values-count-per-hour--describe.csv")

## PROBLEM: LOSE ABILITY TO COMPARE TO FLOW
#  for hood in laboratory.fumehoods:
#    for time in hood.dataframe.index:
#      if per_hour_count.loc[time] < .75 * len(laboratory.fumehoods):
#        hood.dataframe['open'].loc[time] = per_hour_average.loc[time]

  for hood in laboratory.fumehoods:
    print "Processing Hood " + str(hood)
    
    try:
      hood.dataframe["evacuation_cfm"] = calculate_hood_evacuation_series(hood, hood.dataframe["percent_open"], hood.dataframe["occupancy"], laboratory.sash_height_multiplier, laboratory.unoccupied_face_velocity_multiplier
)
    except:
      hood.dataframe["occupancy"] = calculate_occupancy_series(hood.dataframe["percent_open"].index, laboratory.ach_day_start, laboratory.ach_night_start, laboratory.fumehood_occupancy_rate, 0.1)
      hood.dataframe["evacuation_cfm"] = calculate_hood_evacuation_series(hood, hood.dataframe["percent_open"], hood.dataframe["occupancy"], laboratory.sash_height_multiplier, laboratory.unoccupied_face_velocity_multiplier
)
    
    hood.dataframe["datastream_and_calculated_cfm_std"] = hood.dataframe[["datastream_flow","evacuation_cfm"]].std(axis=1)
    hood.dataframe["datastream_and_calculated_cfm_mean"] = hood.dataframe[["datastream_flow","evacuation_cfm"]].mean(axis=1)
    hood.dataframe["fumehood"] = pd.Series([str(hood) for x in hood.dataframe["occupancy"].index], index=hood.dataframe["occupancy"].index)
    hood.dataframe.to_csv(output_dir + str(laboratory) + "--" + str(hood) + "--dataframe.csv")
    hood.dataframe.describe().to_csv(output_dir + str(laboratory) + "--" + str(hood) + "--dataframe-description.csv")
    hood.dataframe[["datastream_flow","evacuation_cfm"]].plot()
    plt.savefig(output_dir + str(laboratory) + "--" + str(hood) + "--cfm_difference.pdf")
  
  plt.close('all')

  concatted = pd.concat([hood.dataframe for hood in laboratory.fumehoods])
  sns.lmplot("percent_open", "datastream_flow", concatted, hue="fumehood")
  plt.savefig(output_dir + str(laboratory) + "--cfm_datastream_flow_lmplot.pdf")
  sns.lmplot("percent_open", "evacuation_cfm", concatted, hue="fumehood")
  plt.savefig(output_dir + str(laboratory) + "--cfm_calculated_cfm_lmplot.pdf")

  
  laboratory.dataframe["per_hour_hood_data_count"] = per_hour_count

  laboratory.dataframe["occupancy"] = calculate_occupancy_series(per_hour_count.index, laboratory.ach_day_start, laboratory.ach_night_start, laboratory.day_occupancy_rate, laboratory.night_occupancy_rate)
  
  laboratory.dataframe["min_lab_cfm"] = calculate_min_lab_evacuation_series(laboratory, laboratory.dataframe["occupancy"])
  
  laboratory.dataframe["min_hood_cfm"] = calculate_min_summed_hood_evacuation_series(laboratory.fumehoods, laboratory.dataframe["occupancy"], laboratory.sash_height_multiplier, laboratory.unoccupied_face_velocity_multiplier)
  
  laboratory.dataframe["min_additional_hood_cfm"] = (laboratory.dataframe["min_hood_cfm"] - laboratory.dataframe["min_lab_cfm"]).apply(lambda x : x if x > 0 else 0)
  
  laboratory.dataframe["min_possible_lab_cfm"] = laboratory.dataframe[["min_lab_cfm","min_hood_cfm"]].max(axis=1).apply(lambda x : x - laboratory.additional_equipment_max)
  
  laboratory.dataframe["calc_hood_cfm"] = np.sum([hood.dataframe["evacuation_cfm"] for hood in laboratory.fumehoods],axis=0)
  
  laboratory.dataframe["stream_hood_cfm"] = np.sum([hood.dataframe["datastream_flow"] for hood in laboratory.fumehoods],axis=0)
  
  laboratory.dataframe["stream_and_calc_hood_cfm_std"] = np.sum([hood.dataframe["datastream_and_calculated_cfm_std"] for hood in laboratory.fumehoods],axis=0)
  
  laboratory.dataframe["stream_and_calc_hood_cfm_mean"] = np.sum([hood.dataframe["datastream_and_calculated_cfm_mean"] for hood in laboratory.fumehoods],axis=0)
  
  laboratory.dataframe["calc_total_lab_cfm"] = laboratory.dataframe[["calc_hood_cfm","min_possible_lab_cfm"]].max(axis=1)
  
  laboratory.dataframe["stream_total_lab_cfm"] = laboratory.dataframe[["stream_hood_cfm","min_possible_lab_cfm"]].max(axis=1)
  
  laboratory.dataframe["calc_excess_cfm"] = (laboratory.dataframe["calc_total_lab_cfm"] - laboratory.dataframe["min_possible_lab_cfm"]).apply(lambda x : x if x > 0 else 0)

  laboratory.dataframe["stream_excess_cfm"] = (laboratory.dataframe["stream_total_lab_cfm"] - laboratory.dataframe["min_possible_lab_cfm"]).apply(lambda x : x if x > 0 else 0)


#  laboratory.dataframe.to_csv(output_dir + str(laboratory) + "--dataframe.csv")
#  laboratory.dataframe.describe().to_csv(stats_dir + str(laboratory) + "--dataframe-description.csv")

  laboratory.dataframe.dropna(axis=0, how="any", inplace=True)
#  laboratory.dataframe.to_csv(output_dir + str(laboratory) + "--dataframe-filtered.csv")
#  laboratory.dataframe.describe().to_csv(stats_dir + str(laboratory) + "--dataframe-filtered-description.csv")
#  
#  laboratory.dataframe[["calc_hood_cfm","stream_hood_cfm"]].plot()
#  plt.savefig(output_dir + str(laboratory) + "-stream-vs-calc.pdf")
#
#  laboratory.dataframe[["min_lab_cfm", "min_additional_hood_cfm", "calc_excess_cfm","calc_total_lab_cfm"]].plot()
#  plt.savefig(stats_dir + str(laboratory) + "-calc-base-hood-sash-cfm.pdf")
#  laboratory.dataframe[["min_lab_cfm", "min_additional_hood_cfm", "stream_excess_cfm","stream_total_lab_cfm"]].plot()
#  plt.savefig(stats_dir + str(laboratory) + "-stream-base-hood-sash-cfm.pdf")
#  plt.close("all")

  result = laboratory.dataframe.mean(axis=0)
  result["description"] = simulation_name
  return result


def main(argv=None):
  if argv is None:
    argv = sys.argv
  general_stats_dir = "output-uqam/general-stats/"
  (laboratories, models, hoods) = load_simulator_objects(data_dir, general_stats_dir)
  hood_datastream = load_hood_datastream(data_dir + datastream_name, hoods, general_stats_dir)
  process_hood_datastream(hood_datastream, hoods, general_stats_dir)
  print laboratories
  for laboratory in laboratories: 
    lab_result = []
    top_out = "output-uqam/"
    output_dir = base_path + top_out + laboratory.laboratory_name + "/output" + postfix + "/"
    stats_dir = base_path + top_out + laboratory.laboratory_name + "/statistics" + postfix + "/"
    results_dir = base_path + top_out + laboratory.laboratory_name + "/results" + postfix + "/"
    for directory in [output_dir, stats_dir, results_dir]:
      if not os.path.exists(directory):
        os.makedirs(directory)
    for index in parameters.index:
      parameter = parameters.loc[index]
      print "Working on laboratory " + str(laboratory)
      print "Parameters : " + str(parameter)
      result = generate_result_for_lab_and_parameter(laboratory, parameter.to_dict(), output_dir, stats_dir, results_dir, parameter.name)
      lab_result.append(result)
    
    current_operation_cfm = lab_result[0]["calc_total_lab_cfm"]
    print current_operation_cfm
    print "Current operating cfm for laboratory :: " + str(current_operation_cfm)
    lab_result = pd.DataFrame(lab_result)
    lab_result.to_csv(results_dir + laboratory.laboratory_name + "--results.csv")

    lab_result_summary = pd.DataFrame()
    lab_result_summary["description"] = lab_result["description"]
    lab_result_summary["base lab cfm"] = lab_result["min_lab_cfm"]
    lab_result_summary["hood inc cfm"] = lab_result["min_additional_hood_cfm"]
    lab_result_summary["sash driven cfm"] = lab_result["calc_excess_cfm"]
    lab_result_summary["lab total cfm"] = lab_result["calc_total_lab_cfm"]
    lab_result_summary.set_index("description")
    lab_result_summary["savings cfm"] = lab_result_summary["lab total cfm"].apply(lambda x : 0 if current_operation_cfm - x < 0 else current_operation_cfm - x)
    fig, ax = plt.subplots()
    ax = lab_result_summary[["base lab cfm","hood inc cfm","sash driven cfm", "savings cfm"]].plot(stacked=True, legend=True, kind="barh",title=("Laboratory Summary for " + laboratory.laboratory_name),rot=45,color=['c', 'm', 'r', 'g'])
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)
    plt.savefig(results_dir + laboratory.laboratory_name + "--barh.png")
    plt.savefig(results_dir + laboratory.laboratory_name + "--barh.pdf")
    lab_result_summary["savings cad"] = lab_result_summary["savings cfm"].apply(lambda x : x * laboratory.cost_cfm)
    lab_result_summary = lab_result_summary.drop("savings cfm", axis=1)
    lab_result_summary.to_csv(results_dir + laboratory.laboratory_name + "--results-for-excel.csv")

main()