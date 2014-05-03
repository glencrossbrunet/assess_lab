import pylab as plt
import pandas as pd
import numpy as np
from pandas.tools.plotting import bootstrap_plot

def plot_fumehood_to_flowdata(fumehood_flowdata, output_dir):
  for fumehood, flowdata in fumehood_flowdata.iteritems():
    fig = flowdata.plot()
    plt.savefig(output_dir + fumehood.hood_id + '-flowdata.pdf')

def plot_laboratory_flowdata(lab, laboratory_cfm, output_dir):
  fig = laboratory_cfm.plot()
  plt.savefig(output_dir + str(lab) + '-flowdata.pdf')

def plot_summary_per_lab(results_by_lab, fig_title):
  fig = plt.figure()
  ax = plt.subplot(111)
  for k, v in results_by_lab:
    ax.plot(v.mean(axis=1), label=(str(k) + '-mean'))
    ax.plot(v.std(axis=1), label=(str(k) + '-std'))
  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * 0.1,
                   box.width, box.height * 0.9])
  ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
            fancybox=True, shadow=True, ncol=2)
  plt.tight_layout()
  plt.savefig(fig_title + "-std-mean.pdf")

  for k, v in results_by_lab:
    v.corr().to_csv(fig_title + str(k) + '-correlation.csv')
    v.corr().mean().describe().to_csv(fig_title + str(k) + '-correlation-description.csv')

  for k, v in results_by_lab:
    fig = plt.figure()
    v.plot(colormap='jet')
    plt.tight_layout()
    plt.savefig(fig_title + str(k) + '-allfumehoods.pdf')


def plot_summary_per_lab_mean(results_by_lab, fig_title):
  for k, v in results_by_lab:
    data = v.sum(axis=1)
    data = pd.Series(data.ix[:])
    print data
    fig = bootstrap_plot(data, size=100, samples=100)
    plt.tight_layout()
    plt.savefig(fig_title + "-" + str(k) + "-bootstrap.pdf")
