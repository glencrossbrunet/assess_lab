from simulatorio.scrapedfile import *
from simulatorio.load_environment import *
import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *
from simulatorlogic import *

data_directory = "E:/git/equipmind/assess_lab/new-dataset/"
output_directory = "E:/git/equipmind/assess_lab/output/"
debug_directory = "E:/git/equipmind/assess_lab/debug/"
statistics_directory = "E:/git/equipmind/assess_lab/stats/"

(laboratories, hoodmodels, fumehoods) = load_environment(data_directory, debug_directory)

load_datastream(data_directory, debug_directory, statistics_directory, fumehoods)

for laboratory in laboratories:
    populate_laboratory_occupancy_data(laboratory)

for fumehood in fumehoods:
    populate_fumehood_occupancy_data(fumehood)

fumehoods[0].data.to_csv('debug-a.csv')

for fumehood in fumehoods:
    adjust_cfm_by_occupancy(fumehood)

fumehoods[0].data.to_csv('debug-b.csv')


print pd.concat([fumehood.data for fumehood in fumehoods])

# lab_cfms = simulate(fumehood_flowdata, laboratories, fumehoods, output_directory)
