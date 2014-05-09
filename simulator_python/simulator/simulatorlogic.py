import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from simulatorstats.cfm_values import *
from simulatorlab.fumehood import *


def generate_fumehood_cfms_for_laboratory(laboratory):
  for fumehood in laboratory.fumehoods:
    populate_fumehood_occupancy_data(fumehood)
  for fumehood in laboratory.fumehoods:
      adjust_cfm_by_occupancy(fumehood)
  for fumehood in laboratory.fumehoods:
      df = fumehood.data.copy()
      df['occupancy'] = fumehood.occupancy_data
  result = get_all_fumehood_data_for_lab(laboratory)
  return result

def populate_laboratory_occupancy_data(laboratory):
  index = pd.Series()
  for fumehood in laboratory.fumehoods:
    if(len(fumehood.data.index) > len(index)):
      index = fumehood.data.index
  result = []
  for each in index:
    if each.hour >= laboratory.day_start.hour and each.hour <= laboratory.night_start.hour and np.random.rand(1)[0] < 0.95:
      result.append(True)
    else:
      result.append(False)
  laboratory.occupancy_data = pd.Series(result, index=index)

def generate_min_evac_series(laboratory):
  index = laboratory.occupancy_data.index
  result = []
  for sample in index:
    result.append(get_min_evac_cfm_for_time(sample, laboratory.occupancy_data.loc[sample], laboratory))
  laboratory.min_evac_series = pd.Series(result, index=index)

def generate_fumehoods_unadjusted_sum(laboratory):
  laboratory.fumehoods_unadjusted_sum = get_all_fumehood_data_for_lab(laboratory).copy().sum(axis=1)

def generate_fumehoods_adjusted_sum(laboratory):
  index = laboratory.occupancy_data.index
  result = []
  for sample in index:
    result.append(np.max([laboratory.fumehoods_unadjusted_sum.loc[sample], laboratory.min_evac_series.loc[sample]]))
  laboratory.fumehoods_adjusted_sum = pd.Series(result, index=index)

def generate_savings(hood_adjusted_sum, hood_unadjusted_sum):
  df = pd.DataFrame(hood_adjusted_sum - hood_unadjusted_sum)
  df.columns = ['cfm_savings']
  return df

def adjust_cfm_for_laboratory_parameters(cfm, laboratory):
  if cfm < laboratory.min_unoccupied_cfm:
    return laboratory.min_unoccupied_cfm
  if cfm > laboratory.min_occupied_cfm:
    return laboratory.min_occupied_cfm
  return cfm

def simulate_per_fumehood(fumehood_flowdata, fumehoods, output_directory):
  
  for fumehood, flowdata in fumehood_flowdata.iteritems():
    flowdata = flowdata.apply(lambda x : adjust_cfm_for_fumehood_state(x, fumehood), axis=1)

  # plot_fumehood_to_flowdata(fumehood_flowdata, output_directory)

  results_series = []

  for fumehood, flowdata in fumehood_flowdata.iteritems():
    result = flowdata.drop('open',1)
    result.columns = [fumehood]
    results_series.append(result)

  results = pd.concat(results_series, join='outer', axis = 1)
  return results

def simulate_per_lab(fumehood_flowdata, laboratories, output_directory):
  results_by_lab = fumehood_flowdata.groupby(lambda x : x.laboratory, 1)
  plot_summary_per_lab(results_by_lab, output_directory + 'datastream-before-labadjustment')
  plot_summary_per_lab_mean(results_by_lab, output_directory + 'datastream-before-labadjustment')

  results = {}

  for k, v in results_by_lab:
    # plot_laboratory_flowdata(str(k) + '_hoods', v, output_directory)
    v.to_csv(output_directory + str(k) + '-full.csv')
    v = v.sum(axis=1)
    v = v.apply(lambda x : adjust_cfm_for_laboratory_parameters(x, k))
    # plot_laboratory_flowdata(str(k) + '_sum', v, output_directory)
    v.to_csv(output_directory + str(k) + '-sum.csv')
    results[k] =  v

  plot_diff_per_lab(results_by_lab, results, output_directory + 'datastream-after-labadjustment')

