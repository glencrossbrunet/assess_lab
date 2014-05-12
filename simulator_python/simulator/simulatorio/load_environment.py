import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *
from simulatorio.estimators import *

verbose = True

def load_laboratories(file):
  if(verbose):
    print("Loading laboratories")
  df = pd.read_csv(file)
  laboratories = [Laboratory(data) for data in [df.ix[i].to_dict() for i in df.index]]
  return laboratories

def load_hoodmodels(file):
  if(verbose):
    print("Loading hood models")
  df = pd.read_csv(file)
  return [HoodModel(data) for data in [df.ix[i].to_dict() for i in df.index]]

def load_fumehoods(file, laboratories, hoodmodels):
  if(verbose):
    print("Loading fumehoods")
  df = pd.read_csv(file)
  return [Fumehood(data, laboratories, hoodmodels) for data in [df.ix[i].to_dict() for i in df.index]]

def resample_data_to_hourly(df):
  df = df.resample('5min',how='mean',fill_method='ffill',
                            closed='left',label='left')
  df = df.resample('1H',how='mean',fill_method='ffill',
                           closed='left',label='left')
  return df

def resample_data_to_half_hourly(df):
  df = df.resample('5min',how='mean',fill_method='ffill',
                            closed='left',label='left')
  df = df.resample('30min',how='mean',fill_method='ffill',
                           closed='left',label='left')
  return df

def load_hoods_datastream(file, fumehoods):
  if(verbose):
    print("Scraping datastream for fumehood open and flow data")

  df = pd.read_csv(file, skiprows = 1, index_col=0, parse_dates=True, date_parser = lambda x : pd.to_datetime(x * 1e9), header=None, squeeze = True,  names=["fumehood", "flow", "open"])
  df.tz_localize('UTC', copy=False).tz_convert('EST', copy=False)

  bac_to_fumehood_series = df.fumehood.apply(lambda x : get_fumehood_for_bac(x, fumehoods))
  df["fumehood"] = bac_to_fumehood_series
  return df

def preprocess_datastream(df, statistics_directory, fumehoods_with_labs):
  if(verbose):
    print "Printing basic statistics"
  df = df[df.fumehood.isin(fumehoods_with_labs)]
  per_fumehood = df.groupby('fumehood')
  per_fumehood.describe().to_csv(statistics_directory + 'rawfumehoods-describe.csv')
  per_fumehood_dict = {}
  
  for fumehood, group in per_fumehood:
    per_fumehood_dict[fumehood] = resample_data_to_hourly(group)

  return per_fumehood_dict

def convert_percent_open_to_flow(df, statistics_directory):
  pass


def load_environment(data_directory, debug_directory):
  if(verbose):
    "Loading environment"

  laboratories = load_laboratories(data_directory + 'laboratories.csv')

  hoodmodels = load_hoodmodels(data_directory + 'hoodmodels.csv')

  fumehoods = load_fumehoods(data_directory + 'fumehoods.csv', laboratories, hoodmodels)
  
  fumehoods_with_labs = []
  for fumehood in fumehoods:
    if fumehood.laboratory is not None:
      fumehoods_with_labs.append(fumehood)

  fumehoods = fumehoods_with_labs

  fumehoods_with_single_model = []
  for fumehood in fumehoods:
    if not isinstance(fumehood.hood_model, list) and not fumehood.hood_model is None:
      fumehoods_with_single_model.append(fumehood)

  fumehoods = fumehoods_with_single_model

  for fumehood in fumehoods:
    if fumehood.bac == -1:
      fumehood.bac = get_random_working_bac(fumehoods, -1)

  if(verbose):
    print "Finished loading environment"
  return (laboratories, hoodmodels, fumehoods)

def load_datastream(data_directory, debug_directory, statistics_directory, fumehoods):
  df = load_hoods_datastream(data_directory + 'datastream.txt', fumehoods)
  add_unadjusted_fumehood_data_to_fumehoods(df, fumehoods)
  
  with_hoodmodel = []
  for fumehood in fumehoods:
    if not isinstance(fumehood.hood_model, list):
      with_hoodmodel.append(fumehood)
  fumehoods = with_hoodmodel

  for fumehood in fumehoods:
    if fumehood.unadjusted_data is None:
      print "Loading random data for missing data for Fumehood " + str(fumehood)
      fumehood.bac = get_random_working_bac(fumehoods, -1)
  link_missing_sample_data_for_random_fumehoods(fumehoods)
  for fumehood in fumehoods:
    if verbose:
      print "Loading data for Fumehood " + str(fumehood)
    fumehood.unadjusted_data = resample_data_to_half_hourly(fumehood.unadjusted_data)
  # grouped = preprocess_datastream(df, statistics_directory, fumehoods)
