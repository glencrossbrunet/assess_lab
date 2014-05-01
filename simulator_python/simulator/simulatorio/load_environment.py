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

  df = pd.read_csv(file)

  print df
  
  if(verbose):
    print("Linking data to fumehoods by BAC")

  fumehood_to_flowdata = {get_fumehood_for_bac(flowdata['BAC'], fumehoods): flowdata for flowdata in df.iterrows()}

  print fumehood_to_flowdata

  bac_to_id = {}
  for i in range(len(hood_info)):
      bac_to_id[hood_info['bac'][i]] = hood_info.index[i]
  
  grouped = data_stream.groupby('BAC')
  
  for name, group in grouped:
      hood_id = bac_to_id[name]
      group['index'] = group.index
      group.drop_duplicates(cols='index', take_last = True, inplace=True)
      open_dict_scraped[hood_id] = group['open']
      flow_dict_scraped[hood_id] = group['flow']
  
  open_scraped = pd.DataFrame(open_dict_scraped)
  flow_scraped = pd.DataFrame(flow_dict_scraped)
  
  if(verbose):
    print("Resampling datastream for fumehood open and flow.")
  flow_data = flow_data.resample('5min',how='mean',fill_method='ffill',
                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
                                                                      closed='left',label='left') 
  open_data = open_data.resample('5min',how='mean',fill_method='ffill',
                                 closed='left',label='left').resample('1H',how='mean',fill_method='ffill',
                                                                      closed='left',label='left')
  
  return (open_scraped, flow_scraped)

def load_environment(path):
  os.chdir(path)
  laboratories = load_laboratories('laboratories.csv')
  hoodmodels = load_hoodmodels('hoodmodels.csv')
  fumehoods = load_fumehoods('fumehoods.csv', laboratories, hoodmodels)
  (open_scraped, flow_scraped) = load_hoods_datastream('datastream.txt', fumehoods)
  return (laboratories, hoodmodels, fumehoods, open_scraped, flow_scraped)
