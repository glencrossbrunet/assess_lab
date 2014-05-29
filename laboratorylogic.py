import pandas as pd
import numpy as np
from baseformulae import *
import sys
import seaborn as sns
import matplotlib.pyplot as plt

OUTPUT_FOLDER = "output-uqam/"

"""
AUXILIARY FUNCTIONS
"""

def resample_data_to_hourly(df):
  df = df.resample('5min',how='mean',fill_method='ffill', closed='left',label='left', limit=1)
  df = df.resample('15min',how='mean',fill_method='ffill', closed='left',label='left', limit=1)
  df = df.resample('1H',how='mean',fill_method='ffill', closed='left',label='left', limit=2)
  df = df.resample('1H',how='mean',fill_method='bfill', closed='left',label='left', limit=2)

  return df


def get_laboratory_for_id(id, laboratories):
  for laboratory in laboratories:
    if laboratory.laboratory_name == id:
      return laboratory
  return None


def get_fumehood_for_bac(bac, fumehoods):
  for fumehood in fumehoods:
    if fumehood.bac == bac:
      return fumehood
  return None


def get_hoodmodel_for_id(id, hoodmodels):
  for hoodmodel in hoodmodels:
    if hoodmodel.model == id:
      return hoodmodel
  return None


def process_hood_datastream(hood_datastream, hoods, debug_dir):
  summary = pd.DataFrame()
  for k, v in hood_datastream:
    k.dataframe["percent_open"] = v["open"]
    k.dataframe["datastream_flow"] = v["flow"]
    k.dataframe = resample_data_to_hourly(k.dataframe)
    if summary.index is None:
      summary.index = k.dataframe.index
    summary[k.bac] = k.dataframe["percent_open"]

  summary.count(axis=0).transpose().to_csv(OUTPUT_FOLDER + "/general-stats/datastream-flow-values-per-fumehood.csv")
  summary.count(axis=0).transpose().describe().to_csv(OUTPUT_FOLDER + "/general-stats/datastream-flow-values-per-fumehood--description.csv")
  summary.count(axis=0).transpose().plot(kind="bar")
  plt.savefig(OUTPUT_FOLDER + "/datastream-flow-values-per-fumehood.pdf")
  summary.count(axis=1).to_csv(OUTPUT_FOLDER + "/general-stats/datastream-flow-values-per-hour.csv")
  summary.count(axis=1).transpose().plot(kind="line")
  plt.savefig(OUTPUT_FOLDER + "/general-stats/datastream-flow-values-per-hour.pdf")
  fumehood_percent_open_means = summary.mean(axis=0)
  fumehood_percent_open_means.sort()
  fumehood_percent_open_means.to_csv(OUTPUT_FOLDER + "/general-stats/datastream-flow-values-per-fumehood-ordered-mean.csv")

  output_f = open(OUTPUT_FOLDER + "/general-stats/datastream-flow-values-per-fumehood-ordered-self-lag-correlation.csv", "w")
  for i, col in summary.iteritems():
    correlation =  col.corr(col.shift(1))
    output_f.write(str(i) + "," + str(correlation) + "\n")

"""
GENERAL ALGORITHMS
"""

def calculate_occupancy_series(index, time_start, time_end, percent_occupied_inside, percent_occupied_outside):
  result = []
  for time in index:
    if time.hour >= pd.to_datetime(time_start).hour and time.hour <= pd.to_datetime(time_end).hour and np.random.rand(1)[0] < percent_occupied_inside:
      result.append(True)
    else:
      if np.random.rand(1)[0] < percent_occupied_outside:
        result.append(True)
      else:
        result.append(False)
  return pd.Series(result, index=index)



"""
LABORATORY LEVEL ALGORITHMS
"""

def aggregate_hood_occupancy_to_lab(fumehoods):
  index = pd.Index([])
  for hood in fumehoods:
    index = index + hood.dataframe.index
  df = pd.DataFrame()
  for hood in fumehoods:
    df[hood] = hood.dataframe["occupancy"]
  return df.sum(axis=1)


def calculate_min_lab_evacuation_series(laboratory, occupancy):
  result = []
  for time in occupancy.index:
    occupied = True if occupancy.loc[time] > 0 else False
    result.append(get_min_laboratory_evac_cfm_at_time(laboratory, time, occupied))
  return pd.Series(result, index=occupancy.index)


def calculate_min_summed_hood_evacuation_series(fumehoods, occupancy, sash_height_multiplier):
  df = pd.DataFrame(index=occupancy.index)
  for hood in fumehoods:
    df[hood] = calculate_hood_evacuation_series(hood, pd.Series([0 for time in occupancy.index], index=occupancy.index), occupancy, sash_height_multiplier)
  return df.sum(axis=1)


"""
HOOD LEVEL ALGORITHMS
"""

def calculate_hood_evacuation_series(hood, percent_open, occupancy, sash_height_multiplier):
  result = []
  for time in percent_open.index:
    cfm = calculate_bounded_hood_cfm(hood, percent_open.loc[time], occupancy.loc[time], sash_height_multiplier)
    result.append(cfm)
  return pd.Series(result, index = percent_open.index)
