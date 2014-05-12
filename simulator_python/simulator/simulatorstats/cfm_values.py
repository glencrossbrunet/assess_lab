import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import prettyplotlib as ppl
import seaborn as sns
from prettyplotlib import brewer2mpl
from pandas.tools.plotting import bootstrap_plot
from pandas.tools.plotting import andrews_curves


def bootstrap_for_lab(laboratory, fig_title):
  fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)
  ax1 = bootstrap_plot(laboratory.min_evac_series)
  ax2 = bootstrap_plot(laboratory.fumehoods_unadjusted_sum)
  ax3 = bootstrap_plot(laboratory.fumehoods_adjusted_sum)
 # ax1.sup_title('min_evac_series')
 # ax2.sup_title('fumehoods_unadjusted_sum')
 # ax3.sup_title('fumehoods_adjusted_sum')
  fig.tight_layout()
  plt.savefig(fig_title)
  plt.close('all')

def basic_plot_for_lab(laboratory, fig_title):
  laboratory.summary.plot()
  plt.legend(loc='best')
  plt.suptitle('laboratory summary')
  plt.tight_layout()
  plt.savefig(fig_title)
  plt.close('all')

def basic_plot_for_savings(savings, fig_title):
  savings.plot()
  plt.legend(loc='best')
  plt.suptitle('laboratory summary')
  plt.tight_layout()
  plt.savefig(fig_title)
  plt.close('all')

def cumulative_plot_for_savings(savings, fig_title):
  savings.cumsum().plot()
  plt.legend(loc='best')
  plt.suptitle('laboratory summary')
  plt.tight_layout()
  plt.savefig(fig_title)
  plt.close('all')

def summary_description_plot(df, fig_title):
  fig = plt.figure()
  df.summary.describe().plot(kind='bar')
  plt.legend(loc='best')
  plt.tight_layout()
  plt.savefig(fig_title)
  plt.close('all')

def plot_stats_over_time(df, fig_title):
  df.transpose().describe().transpose().drop(['25%','50%','75%','count','std'], axis=1).plot()
  plt.legend(loc='best')
  plt.tight_layout()
  plt.savefig(fig_title)
  plt.close('all')

def fumehood_data_correlation_plot(laboratory, fig_title):
  sns.corrplot(laboratory.fumehood_data, annot=False, diag_names=False)
  plt.savefig(fig_title)
  plt.close('all')
