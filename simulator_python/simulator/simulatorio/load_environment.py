import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *

verbose = True

def printer_auxiliary(x):
  print x
  print type(x)
  return x

def load_laboratories(file):
  if(verbose):
    print("Loading laboratories")
  df = pd.read_csv(file)
  dictionary = [df.ix[i].to_dict() for i in df.index]
  laboratories = [Laboratory(data) for data in dictionary]
  return laboratories

def load_hoodmodels(file):
  if(verbose):
    print("Loading hood models")
  df = pd.read_csv(file)
  dictionary = [df.ix[i].to_dict() for i in df.index]
  hoodmodels = [HoodModel(data) for data in dictionary]
  return hoodmodels

def load_fumehoods(file, laboratories, hoodmodels):
  if(verbose):
    print("Loading fumehoods")
  df = pd.read_csv(file)
  dictionary = [df.ix[i].to_dict() for i in df.index]
  fumehoods = [Fumehood(data, laboratories, hoodmodels) for data in dictionary]
  return fumehoods

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

  open_dict_scraped = {}
  flow_dict_scraped = {}
  f = open(file)

  df = pd.read_csv(file,
                   skiprows = 1,
                   index_col=0,
                   parse_dates=True,
                   date_parser = lambda x : pd.to_datetime(x * 1e9),
                   squeeze = True)
  df.tz_localize('UTC', copy=False).tz_convert('EST', copy=False)
  df.columns = ['BAC','flow','open']

  grouped = df.groupby('BAC')
  fumehood_flowdata = {}
  for bac, group in grouped:
    group = group.drop('BAC', 1)
    hood = get_fumehood_for_bac(bac, fumehoods)
    if hood.laboratory is None:
      continue
    if(verbose):
      print "Processing data for Fumehood: " + str(hood)
    fumehood_flowdata[hood] = resample_data_to_hourly(group)

  # grouped.aggregate(lambda x : resample_data_to_hourly(x))

  return fumehood_flowdata

def load_environment(path, debug_directory):
  if(verbose):
    "Loading environment"
  os.chdir(path)
  laboratories = load_laboratories('laboratories.csv')
  print map(str, laboratories)
  hoodmodels = load_hoodmodels('hoodmodels.csv')
  print map(str, hoodmodels)
  fumehoods = load_fumehoods('fumehoods.csv', laboratories, hoodmodels)
  print map(str, fumehoods)
  grouped = load_hoods_datastream('datastream.txt', fumehoods)
  if(verbose):
    print "Finished loading environment"
  return (laboratories, hoodmodels, fumehoods, grouped)
