import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from simulatorstats.cfm_values import *

def adjust_cfm_for_fumehood_state(series, fumehood):
  new_cfm = fumehood.finalcfm(series.ix['open'], True)
  series.ix['flow'] = new_cfm
  return series

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


def simulate(fumehood_flowdata, laboratories, fumehoods, output_directory):
  simulated_df = simulate_per_fumehood(fumehood_flowdata, fumehoods, output_directory)
  simulate_per_lab(simulated_df, laboratories, output_directory)
