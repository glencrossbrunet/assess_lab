from simulatorio.scrapedfile import *
from optparse import OptionParser
from simulatorio.load_environment import *
import os, sys, copy
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *
from simulatorlogic import *

parser = OptionParser()
parser.add_option("-d", "--data-directory", dest="data_dir", help="selects the directory from which to read datasets", default="data/")
parser.add_option("-o", "--output-directory", dest="output_dir", help="selects the directory to which to write output", default="output/")
parser.add_option("-b", "--debug-direcotry", dest="debug_dir", help="selects the directory to which to write debugging information", default="debug/")
parser.add_option("-s", "--statistics-directory", dest="statistics_dir", help="selects the directory to which to write statistics", default="stats/")
parser.add_option("-p", "--parameters", dest="parameters", help="specifies parameters to test in the format of a list of lists such as [['Current Operating Settings',4,10,4,10,.3,0],['Reduced ACH At Night and 25 percent reduced use',4,10,3,6,.3,.25]], where the values are [description, day unoccupied ach, day occupied ach, night unoccupied ach, night occupied ach, estimated fumehood occupation rate, usage reduction percentage]")
parser.add_option("-v", "--verbose", dest="verbose", default=True, help="prints status messages to stdout")

data_dir = "E:/git/equipmind/assess_lab/new-dataset/"
output_dir = "E:/git/equipmind/assess_lab/output/"
debug_dir = "E:/git/equipmind/assess_lab/debug/"
statistics_dir = "E:/git/equipmind/assess_lab/stats/"

def setup_data(data_dir, output_dir, debug_dir, statistics_dir):
  (laboratories, hoodmodels, fumehoods) = load_environment(data_dir, debug_dir)
  load_datastream(data_dir, debug_dir, statistics_dir, fumehoods)
  laboratories_with_valid_fumehoods = []
  for laboratory in laboratories:
    for fumehood in laboratory.fumehoods:
      if fumehood in fumehoods:
        if not laboratory in laboratories_with_valid_fumehoods:
          laboratories_with_valid_fumehoods.append(laboratory)
  laboratories = laboratories_with_valid_fumehoods
  debug_f = open(debug_dir + 'environment.txt','w')
  debug_f.write('Laboratories :\n'                + str(' | '.join(map(str, laboratories))) + '\n\n')
  debug_f.write('Hoodmodels :\n'                  + str(' | '.join(map(str, hoodmodels))) + '\n\n')
  debug_f.write('Fumehoods with Laboratories :\n' + str(' | '.join(map(str, fumehoods))) + '\n\n')
  debug_f.close()
  return (laboratories, hoodmodels, fumehoods)

# for laboratory in laboratories:
#     result = generate_fumehood_cfms_for_laboratory(laboratory)
#     result.to_csv(output_dir + str(laboratory) + '-all_fumehoods.csv')

# dat control flow
parameters = [["Current Operating Settings",4,10,4,10,.3,0]
          ,["Reduced ACH At Night",4,10,3,6,.3,0]
          ,["Reduced All ACH",4,8,4,8,.3,0]
          ,["Usage Reduction Test",4,10,4,10,.4,0]
          ,["Usage Reduction Test",4,10,4,10,.4,.25]
          ,["Usage Reduction Test",4,10,4,10,.4,.30]
          ,["Usage Reduction Test",4,10,4,10,.4,.50]
          ,["Usage Reduction WIth ACH Reduction",4,8,3,6,.4,.25]
         ]

def fill_values_in_laboratory_struct(laboratory):
  populate_laboratory_occupancy_data(laboratory)
  generate_min_evac_series(laboratory)
  generate_fumehood_cfms_for_laboratory(laboratory)
  generate_fumehoods_unadjusted_sum(laboratory)
  generate_fumehoods_adjusted_sum(laboratory)
  generate_laboratory_summary(laboratory)

laboratory_results = []
savings_results = []

def evaluate_laboratory(laboratory):
  lab_top_dir = output_dir + laboratory.laboratory_name + "/"
  if not os.path.exists(lab_top_dir):
    os.makedirs(lab_top_dir)
  results_file = open(lab_top_dir + "/laboratory-results.csv",'w')
  results_file.write("SIMULATION RESULTS\n")
  results_file.write("Description,Day Unoccupied ACH,Day Occupied ACH,Night Unoccupied ACH,Night Occupied ACH,Fumehood Occupation Rate,Use Reduction Factor,Minimum Evac,Excess Fumehood Evac,Savings\n")
  for param in parameters:
    results_file.write(evaluate_laboratory_by_parameter(laboratory, param))

def evaluate_laboratory_by_parameter(laboratory, param):
  laboratory.reset_parameters(param[1], param[2], param[3], param[4], param[5], param[6])
  laboratory.reset()
  lab_dir = os.path.dirname(output_dir + str(laboratory) + '/')
  if not os.path.exists(lab_dir):
    os.makedirs(lab_dir)
  print "Processing " + str(laboratory)
  fill_values_in_laboratory_struct(laboratory)
  laboratory.summary.to_csv(str(lab_dir) + '/laboratory-summary.csv')
  basic_plot_for_lab(laboratory, str(lab_dir) + '/lab-line-basic.pdf')
  plot_stats_over_time(laboratory.fumehood_data, str(lab_dir) + '/fumehoods-std-mean.pdf')
  fumehood_data_correlation_plot(laboratory, str(lab_dir) + '/fumehood-data-correlation-plot.pdf')
  savings = generate_savings(laboratory.summary['hood_adjusted_sum'], laboratory.summary['minimum_evac'])
  basic_plot_for_savings(savings, str(lab_dir) + '/basic-savings-plot.pdf')
  cumulative_plot_for_savings(savings, str(lab_dir) + '/basic-cummulative-savings-plot.pdf')
  laboratory_results.append(laboratory.summary)
  savings_results.append(savings)
  return (','.join(map(str,param)) + ',' + str(laboratory.summary.sum()['minimum_evac']) + ',' + str(laboratory.summary.sum()['hood_adjusted_sum']) + '\n')
  results_file.close()
  all_adjusted_sums = pd.concat([x['hood_adjusted_sum'] for x in laboratory_results], join='outer', axis = 1)
  all_savings = pd.concat([x for x in savings_results], join='outer', axis = 1)
  all_savings_cummulative = pd.concat([x.cumsum() for x in savings_results], join='outer', axis = 1)
  plot_stats_over_time(all_adjusted_sums, output_dir + laboratory.laboratory_name + '/adjusted_sums_summary.pdf')
  plot_stats_over_time(all_savings, output_dir + laboratory.laboratory_name + '/savings_summary.pdf')  
  plot_stats_over_time(all_savings_cummulative, output_dir + laboratory.laboratory_name + '/savings_summary.pdf')

def main(argv=None):
  if argv is None:
    argv = sys.argv
  (laboratories, hoodmodels, fumehoods) = setup_data(data_dir, output_dir, debug_dir, statistics_dir)
  for laboratory in laboratories:
    evaluate_laboratory(laboratory)

(options, args) = parser.parse_args()
main()