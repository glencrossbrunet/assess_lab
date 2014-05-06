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
  
  # per_fumehood = pd.DataFrame.from_dict(per_fumehood_dict)

  # per_fumehood.describe().to_csv(statistics_directory + 'resampledfumehoods-describe.csv')

  return per_fumehood_dict

def convert_percent_open_to_flow(df, statistics_directory):
  pass


def load_environment(path, debug_directory, statistics_directory):
  if(verbose):
    "Loading environment"
  os.chdir(path)

  laboratories = load_laboratories('laboratories.csv')
  print map(str, laboratories)

  hoodmodels = load_hoodmodels('hoodmodels.csv')
  print map(str, hoodmodels)

  fumehoods = load_fumehoods('fumehoods.csv', laboratories, hoodmodels)
  
  fumehoods_with_labs = []
  for fumehood in fumehoods:
    if fumehood.laboratory is not None:
      fumehoods_with_labs.append(fumehood)
  print map(str, fumehoods_with_labs)

  df = load_hoods_datastream('datastream.txt', fumehoods)
  grouped = preprocess_datastream(df, statistics_directory, fumehoods_with_labs)


  if(verbose):
    print "Finished loading environment"
  return (laboratories, hoodmodels, fumehoods, grouped)
