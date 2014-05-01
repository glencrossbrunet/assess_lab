import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *

def load_laboratories(file):
  df = pd.read_csv(file)
  dictionary = [df.ix[i].to_dict() for i in df.index]
  laboratories = [Laboratory(data) for data in dictionary]
  return laboratories

def load_hoodmodels(file):
  df = pd.read_csv(file)
  dictionary = [df.ix[i].to_dict() for i in df.index]
  hoodmodels = [HoodModel(data) for data in dictionary]
  return hoodmodels

def load_fumehoods(file, laboratories, hoodmodels):
  df = pd.read_csv(file)
  dictionary = [df.ix[i].to_dict() for i in df.index]
  fumehoods = [Fumehood(data, laboratories, hoodmodels) for data in dictionary]
  return fumehoods

def load_environment(path):
  os.chdir(path)
  laboratories = load_laboratories('laboratories.csv')
  hoodmodels = load_hoodmodels('hoodmodels.csv')
  fumehoods = load_fumehoods('fumehoods.csv', laboratories, hoodmodels)
  return (laboratories, hoodmodels, fumehoods)