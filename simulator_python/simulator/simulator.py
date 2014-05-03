from simulatorio.scrapedfile import *
from simulatorio.load_environment import *
import os, sys
from simulatorlab.laboratory import *
from simulatorlab.fumehood import *
from plotting.cfm_values import *
from simulatorlogic import *

data_directory = "E:/git/equipmind/assess_lab/new-dataset"
output_directory = "E:/git/equipmind/assess_lab/output/"

def simulate(fumehood_flowdata, laboratories, fumehoods):
  lab_cfms = pd.DataFrame()
  hood_cfms = pd.DataFrame()
  for fumehood, flowdata in fumehood_flowdata.iteritems():
    flowdata = flowdata.apply(lambda x : adjust_cfm_for_fumehood_state(x, fumehood), axis=1)

  # plot_fumehood_to_flowdata(fumehood_flowdata, output_directory)

  results_series = []

  for fumehood, flowdata in fumehood_flowdata.iteritems():
    result = flowdata.drop('open',1)
    result.columns = [fumehood]
    results_series.append(result)

  results = pd.concat(results_series, join='outer', axis = 1)

  results.to_csv('debug.csv')

  results_by_lab = results.groupby(lambda x : x.laboratory, 1)
  for k, v in results_by_lab:
    # plot_laboratory_flowdata(str(k) + '_hoods', v, output_directory)
    v.to_csv(output_directory + str(k) + '-full.csv')
    v = v.sum(axis=1)
    print "Lab : " + k.laboratory_name
    print "Lab Min : " + str(k.min_evac_cfm)
    print "Lab Max : " + str(k.max_evac_cfm)
    v = v.apply(lambda x : adjust_cfm_for_laboratory_parameters(x, k))
    # plot_laboratory_flowdata(str(k) + '_sum', v, output_directory)
    v.to_csv(output_directory + str(k) + '-sum.csv')


(laboratories, hoodmodels, fumehoods, fumehood_flowdata) = load_environment(data_directory)

lab_cfms = simulate(fumehood_flowdata, laboratories, fumehoods)

'''
iterative method
      if(laboratory.laboratory_name == fumehood.laboratory
        for time, sample in flowdata.iterrows():
          fumehood.sash_height = sample['open']
          hood_cfms.append(pd.Series({'cfm' : fumehood.finalcfm(), 'laboratory' : fumehood.laboratory}, 
                                     index=time))
'''