from simulatorio.scrapedfile import *
from simulatorio.load_environment import *
import os, sys, copy
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
params = [[4,10,4,10,.3], [4,8,2,6,.4]]

laboratory_results = []
savings_results = []


for laboratory in laboratories:
  if not os.path.exists(output_directory + laboratory.laboratory_name + "/"):
    os.makedirs(output_directory + laboratory.laboratory_name + "/")
  for param in params:
    laboratory.reset_occupancy_values(param[0], param[1], param[2], param[3], param[4])
    laboratory.reset()
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
    generate_laboratory_summary(laboratory)
    laboratory.summary.to_csv(str(lab_directory) + '/laboratory-summary.csv')
    basic_plot_for_lab(laboratory, str(lab_directory) + '/lab-line-basic.pdf')
    plot_stats_over_time(laboratory.fumehood_data, str(lab_directory) + '/fumehoods-std-mean.pdf')
    fumehood_data_correlation_plot(laboratory, str(lab_directory) + '/fumehood-data-correlation-plot.pdf')
    savings = generate_savings(laboratory.summary['hood_adjusted_sum'], laboratory.summary['hood_unadjusted_sum'])
    basic_plot_for_savings(savings, str(lab_directory) + '/basic-savings-plot.pdf')
    cumulative_plot_for_savings(savings, str(lab_directory) + '/basic-cummulative-savings-plot.pdf')
    laboratory_results.append(laboratory.summary)
    savings_results.append(savings)

  all_adjusted_sums = pd.concat([x['hood_adjusted_sum'] for x in laboratory_results], join='outer', axis = 1)
  all_savings = pd.concat([x for x in savings_results], join='outer', axis = 1)
  all_savings_cummulative = pd.concat([x.cumsum() for x in savings_results], join='outer', axis = 1)

  plot_stats_over_time(all_adjusted_sums, output_directory + laboratory.laboratory_name + '/adjusted_sums_summary.pdf')

  plot_stats_over_time(all_savings, output_directory + laboratory.laboratory_name + '/savings_summary.pdf')  

  plot_stats_over_time(all_savings_cummulative, output_directory + laboratory.laboratory_name + '/savings_summary.pdf')