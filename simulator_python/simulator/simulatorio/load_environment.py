import os, sys

def load_laboratories(file):
  pass

def load_hoodmodels(file):
  pass

def load_fumehoods(file):
  pass

def load_environment(path):
  os.chdir(path)
  load_laboratories('laboratories.csv')
  load_fumehoods('fumehoods.csv')
  load_hoodmodels('hoodmodels.csv')