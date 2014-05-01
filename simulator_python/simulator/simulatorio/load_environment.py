import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *

verbose = True

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

#  '''
#  Insert code to make the following transformation:
#  { fumehood : pandas dataframe of time series }
#  '''
#  if(verbose):
#    print("Linking data to fumehoods by BAC")
#  fumehood_flowdata = {get_fumehood_for_bac(int(flowdata['BAC']), fumehoods): flowdata for index, flowdata in df.iterrows()}
#  
#  groups = df.groupby('BAC').resample('5min',how='mean',fill_method='ffill',
#                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
#                                                                      closed='left',label='left')
#
#  print groups
#
#  for fumehood, flowdata in fumehood_flowdata.iteritems():
#    flowdata = flowdata.resample('5min',how='mean',fill_method='ffill',
#                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
#                                                                      closed='left',label='left')
#
#  print fumehood_flowdata
#
#  df = df.resample('5min',how='mean',fill_method='ffill',
#                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
#                                                                      closed='left',label='left') 

  grouped = df.groupby('BAC')
  fumehood_flowdata = {}
  for bac, group in grouped:
    group = group.drop('BAC', 1)
    group = group.resample('5min',how='mean',fill_method='ffill',
                            closed='left',label='left')
    fumehood_flowdata[get_fumehood_for_bac(bac, fumehoods)] = group.resample('1H',how='mean',fill_method='ffill',
                           closed='left',label='left')

  return fumehood_flowdata

def load_environment(path):
  if(verbose):
    "Loading environment"
  os.chdir(path)
  laboratories = load_laboratories('laboratories.csv')
  hoodmodels = load_hoodmodels('hoodmodels.csv')
  fumehoods = load_fumehoods('fumehoods.csv', laboratories, hoodmodels)
  grouped = load_hoods_datastream('datastream.txt', fumehoods)
  if(verbose):
    print "Finished loading environment"
  return (laboratories, hoodmodels, fumehoods, grouped)
