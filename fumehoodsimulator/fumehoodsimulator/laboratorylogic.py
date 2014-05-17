import pandas as pd
import numpy as np
from baseformulae import *


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

'''
GENERAL ALGORITHMS
'''

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


'''
LABORATORY LEVEL ALGORITHMS
'''

def aggregate_hood_occupancy_to_lab(fumehoods):
  index = pd.Index([])
  for hood in fumehoods:
    index = index + hood.dataframe.index
  df = pd.DataFrame()
  for hood in fumehoods:
    df[hood] = hood.dataframe['occupancy']
  return df.sum(axis=1)


def calculate_min_lab_evacuation_series(laboratory, occupancy):
  result = []
  for time in occupancy.index:
    occupied = True if occupancy.loc[time] > 0 else False
    result.append(get_min_laboratory_evac_cfm_at_time(laboratory, time, occupied))
  return pd.Series(result, index=occupancy.index)


def calculate_min_summed_hood_evacuation_series(fumehoods, occupancy):
  df = pd.DataFrame(index=occupancy.index)
  for hood in fumehoods:
    df[hood] = calculate_hood_evacuation_series(hood, pd.Series([0 for time in occupancy.index], index=occupancy.index), occupancy)
  return df.sum(axis=1)


def calculate_min_additional_hood_evacuation_series(min_lab_evacuation,min_summed_hood_evacuation_cfm):
  return (min_summed_hood_evacuation_cfm - min_lab_evacuation).apply(lambda x : x if x > 0 else 0)
  


'''
HOOD LEVEL ALGORITHMS
'''

def calculate_hood_evacuation_series(hood, percent_open, occupancy):
  result = []
  for time in percent_open.index:
    cfm = calculate_bounded_hood_cfm(hood, percent_open.loc[time], occupancy.loc[time])
    result.append(cfm)
  return pd.Series(result, index = percent_open.index)
