from simulatorio.scrapedfile import *
from simulatorio.load_environment import *

def simulate(fumehood_flowdata):
  cfm = 0
  for fumehood, flowdata in fumehood_flodata:
    for sample in flowdata:
      fumehood.sash_height = sample['open']
      cfm += fumehood.finalcfm()


data_directory = "E:/git/equipmind/assess_lab/new-dataset"
output_directory = "E:/git/equipmind/assess_lab/output/"

(laboratories, hoodmodels, fumehoods, open_scraped, flow_scraped) = load_environment(data_directory)
print laboratories
print hoodmodels
print fumehoods
print fumehood_flowdata

