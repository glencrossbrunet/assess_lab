from simulatorio.scrapedfile import *
from simulatorio.load_environment import *
import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *

def simulate(fumehood_flowdata, laboratories, fumehoods):
  cfm = 0
  for bac, flowdata in fumehood_flowdata:
    fumehood = get_fumehood_for_bac(bac, fumehoods)
    for time, sample in flowdata.iterrows():
      fumehood.sash_height = sample['open']
      cfm += fumehood.finalcfm()
  print cfm

data_directory = "E:/git/equipmind/assess_lab/new-dataset"
output_directory = "E:/git/equipmind/assess_lab/output/"

(laboratories, hoodmodels, fumehoods, fumehood_flowdata) = load_environment(data_directory)

simulate(fumehood_flowdata, laboratories, fumehoods)