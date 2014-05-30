import pandas as pd
import numpy as np
import os, glob, shutil
import matplotlib.pyplot as plt
import seaborn

all_results = {}

iteration = 0
df_sum = None
for lab in os.listdir("output-uqam/"):
	csv = "output-uqam/" + lab + "/results/" + lab + "--results-for-excel.csv"
	try:
		df = pd.read_csv(csv, index_col="description")
		df["equipment inc cfm"] = df["hood inc cfm"]
		df["savings cfm"] = df["savings cad"].apply(lambda x : x / 5.0)
		df["lab total cad"] = df["lab total cfm"].apply(lambda x : x / 5.0)
		df = df[["base lab cfm","equipment inc cfm","sash driven cfm", "lab total cfm", "savings cfm", "lab total cad", "savings cad"]]
		all_results[lab] = df
		df.to_csv("uqam results/raw/output/" + lab + "--results.csv")
		fig, ax = plt.subplots()
		ax = df[["base lab cfm","equipment inc cfm","sash driven cfm", "savings cfm"]].plot(stacked=True, legend=True, kind="barh",title=("Laboratory Summary for All Laboratories"),color=['c', 'm', 'r', 'g'])
		lgd = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)
		plt.tight_layout()
		plt.savefig("uqam results/figures/" + lab + "--final_results--barh.png", bbox_extra_artists=(lgd,), bbox_inches='tight', dpi=500)
		plt.savefig("uqam results/figures/" + lab + "--final_results--barh.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')
		if iteration == 0:
			df_sum = df
			iteration = 1
		else: 
			df_sum = df_sum + df
	except:
		print ""

print df_sum

df_sum.to_csv("final_results.csv")

print df_sum

fig, ax = plt.subplots()
ax = df_sum[["base lab cfm","equipment inc cfm","sash driven cfm", "savings cfm"]].plot(stacked=True, legend=True, kind="barh",title=("Laboratory Summary for All Laboratories"),color=['c', 'm', 'r', 'g'])
lgd = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), fancybox=True, shadow=True, ncol=4)
plt.tight_layout()
plt.savefig("final_results--barh.png", bbox_extra_artists=(lgd,), bbox_inches='tight')
plt.savefig("final_results--barh.pdf", bbox_extra_artists=(lgd,), bbox_inches='tight')