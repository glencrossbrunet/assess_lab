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

# for laboratory in laboratories:
#     result = generate_fumehood_cfms_for_laboratory(laboratory)
#     result.to_csv(output_directory + str(laboratory) + '-all_fumehoods.csv')

# dat control flow
for laboratory in laboratories:
  populate_laboratory_occupancy_data(laboratory)
  generate_min_evac_series(laboratory)
  fumehoods_cfms = generate_fumehood_cfms_for_laboratory(laboratory)
  fumehoods_cfms.to_csv(output_directory + '/fumehoods_adjusted_cfm/' + str(laboratory) + '-all_fumehoods.csv')
  generate_fumehoods_unadjusted_sum(laboratory)
  laboratory_summary = laboratory_summary(laboratory)
  laboratory_summary.to_csv(output_directory + '/fumehoods_adjusted_cfm/' + str(laboratory) + '-summary.csv')

# combined.to_csv('debug.csv')


# lab_cfms = simulate(fumehood_flowdata, laboratories, fumehoods, output_directory)
