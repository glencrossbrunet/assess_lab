from simulatorio.scrapedfile import *
from simulatorio.load_environment import *
import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *
from simulatorlogic import *

data_directory = "E:/git/equipmind/assess_lab/new-dataset"
output_directory = "E:/git/equipmind/assess_lab/output/"
debug_directory = "E:/git/equipmind/assess_lab/debug/"
statistics_directory = "E:/git/equipmind/assess_lab/stats/"

(laboratories, hoodmodels, fumehoods, fumehood_flowdata) = load_environment(data_directory, debug_directory, statistics_directory)

lab_cfms = simulate(fumehood_flowdata, laboratories, fumehoods, output_directory)

'''
iterative method
      if(laboratory.laboratory_name == fumehood.laboratory
        for time, sample in flowdata.iterrows():
          fumehood.sash_height = sample['open']
          hood_cfms.append(pd.Series({'cfm' : fumehood.finalcfm(), 'laboratory' : fumehood.laboratory}, 
                                     index=time))
'''