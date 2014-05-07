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
params = [[4,10,2,6,.3], [2,6,2,4,.4]]

for param in params:
  for laboratory in laboratories:
    laboratory.reset_occupancy_values(param[0], param[1], param[2], param[3], param[4])
    laboratory.reset_laboratory()
    lab_directory = os.path.dirname(output_directory + str(laboratory) + '/')
    if not os.path.exists(lab_directory):
      os.makedirs(lab_directory)
    print "Processing " + str(laboratory)
    populate_laboratory_occupancy_data(laboratory)
    generate_min_evac_series(laboratory)
    fumehoods_cfms = generate_fumehood_cfms_for_laboratory(laboratory)
    fumehoods_cfms.to_csv(str(lab_directory) + '/all_fumehoods.csv')
    generate_fumehoods_unadjusted_sum(laboratory)
    generate_fumehoods_adjusted_sum(laboratory)
    laboratory_summary = laboratory_summary(laboratory)
    laboratory_summary.to_csv(str(lab_directory) + '/laboratory-summary.csv')
    basic_plot_for_lab(laboratory, str(lab_directory) + '/lab-line-basic.pdf')
    # andrews_for_lab(laboratory, str(lab_directory) + 'andrews_for_lab.pdf')
# combined.to_csv('debug.csv')


# lab_cfms = simulate(fumehood_flowdata, laboratories, fumehoods, output_directory)
