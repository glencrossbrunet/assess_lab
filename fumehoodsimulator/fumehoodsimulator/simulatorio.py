from laboratorylogic import *
from baseformulae import *
from laboratory import *

import argparse, threading, sys
import pandas as pd
import numpy as np


def resample_data_to_hourly(df):
  df = df.resample('5min',how='mean',fill_method='ffill',
                            closed='left',label='left')
  df = df.resample('1H',how='mean',fill_method='ffill',
                           closed='left',label='left')
  return df


def load_laboratories(file):
  df = pd.read_csv(file)
  laboratories = [Laboratory(data) for data in [df.ix[i].to_dict() for i in df.index]]
  return laboratories


def load_hoodmodels(file):
  df = pd.read_csv(file)
  return [HoodModel(data) for data in [df.ix[i].to_dict() for i in df.index]]


def load_fumehoods(file, laboratories, hoodmodels):
  df = pd.read_csv(file)
  return [Fumehood(data, laboratories, hoodmodels) for data in [df.ix[i].to_dict() for i in df.index]]


def load_simulator_objects(data_directory, debug_directory):

  laboratories = load_laboratories(data_directory + 'laboratories.csv')
  hoodmodels = load_hoodmodels(data_directory + 'hoodmodels.csv')
  fumehoods = load_fumehoods(data_directory + 'fumehoods.csv', laboratories, hoodmodels)
  
  fumehoods_with_labs = []
  for fumehood in fumehoods:
    if fumehood.laboratory is not None:
      fumehoods_with_labs.append(fumehood)

  fumehoods = fumehoods_with_labs

  fumehoods = [hood for hood in fumehoods if hood.bac > 0]
#  for fumehood in fumehoods:
#    if fumehood.bac == -1:
#      fumehood.bac = get_random_working_bac(fumehoods, -1)

  debug_f = open(debug_directory + 'environment.txt','w')
  debug_f.write('Laboratories :\n'                + str(' | '.join(map(str, laboratories))) + '\n\n')
  debug_f.write('Hoodmodels :\n'                  + str(' | '.join(map(str, hoodmodels))) + '\n\n')
  debug_f.write('Fumehoods with Laboratories :\n' + str(' | '.join(map(str, fumehoods))) + '\n\n')
  debug_f.close()

  return (laboratories, hoodmodels, fumehoods)


def load_hood_datastream(file, fumehoods):
  df = pd.read_csv(file, skiprows = 1, index_col=0, parse_dates=True, date_parser = lambda x : pd.to_datetime(x * 1e9), header=None, squeeze = True,  names=["hood", "flow", "open"])
  df.tz_localize('UTC', copy=False).tz_convert('EST', copy=False)

  bac_to_fumehood_series = df["hood"].apply(lambda x : get_fumehood_for_bac(x, fumehoods))
  df["hood"] = bac_to_fumehood_series

  return df.groupby("hood")

def process_hood_datastream(hood_datastream, hoods):
  for k, v in hood_datastream:
    k.dataframe['percent_open'] = v['open']
    k.dataframe['datastream_flow'] = v['flow']
    k.dataframe = resample_data_to_hourly(k.dataframe)
