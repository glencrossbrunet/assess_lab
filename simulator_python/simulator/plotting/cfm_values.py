import pylab as plt
import pandas as pd
import numpy as np

def plot_fumehood_to_flowdata(fumehood_flowdata, output_dir):
  for fumehood, flowdata in fumehood_flowdata.iteritems():
    flowdata = flowdata.drop('BAC',1)
    fig = flowdata.plot()
    plt.savefig(output_dir + fumehood.hood_id + '-flowdata.pdf')

def plot_laboratory_flowdata(lab, laboratory_cfm, output_dir):
  print "Making a figure"
  fig = laboratory_cfm.plot()
  plt.savefig(output_dir + str(lab) + '-flowdata.pdf')
