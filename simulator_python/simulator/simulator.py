from simulatorio.scrapedfile import *
from simulatorio.load_environment import *

data_directory = "E:/git/equipmind/assess_lab/new-dataset"
output_directory = "E:/git/equipmind/assess_lab/output/"

(laboratories, hoodmodels, fumehoods) = load_environment(data_directory)
print laboratories
print hoodmodels
print fumehoods

(open_scraped, flow_scraped) = load_hoods_datastream("datastream.test")

print(open_scraped)