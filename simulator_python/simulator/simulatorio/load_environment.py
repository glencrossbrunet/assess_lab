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

  df = pd.read_csv('DataStream.txt',
                            skiprows = 1,
                            index_col=0,
                            parse_dates=True,
                            date_parser = lambda x: np.datetime64(x*1000000),
                            squeeze = True)
  df.tz_localize('UTC', copy=False).tz_convert('EST', copy=False)
  df.columns = ['BAC','flow','open']

  print df
  
  if(verbose):
    print("Resampling Data Points")

  grouped = df.groupby('BAC')
  
  if(verbose):
    print("Resampling datastream for fumehood open and flow.")
  flow_data = flow_data.resample('5min',how='mean',fill_method='ffill',
                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
                                                                      closed='left',label='left') 
  open_data = open_data.resample('5min',how='mean',fill_method='ffill',
                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
                                                                      closed='left',label='left')
 
  if(verbose):
    print("Linking data to fumehoods by BAC")
  fumehood_to_flowdata = {get_fumehood_for_bac(int(flowdata['BAC']), fumehoods): flowdata for index, flowdata in df.iterrows()}
  
  return (open_scraped, flow_scraped)

def load_environment(path):
  os.chdir(path)
  laboratories = load_laboratories('laboratories.csv')
  hoodmodels = load_hoodmodels('hoodmodels.csv')
  fumehoods = load_fumehoods('fumehoods.csv', laboratories, hoodmodels)
  (open_scraped, flow_scraped) = load_hoods_datastream('datastream.txt', fumehoods)
  return (laboratories, hoodmodels, fumehoods, open_scraped, flow_scraped)
