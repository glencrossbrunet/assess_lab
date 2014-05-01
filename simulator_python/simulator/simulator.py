from simulatorio.scrapedfile import *
from simulatorio.load_environment import *

data_directory = "E:/git/equipmind/assess_lab/new-dataset"
output_directory = "E:/git/equipmind/assess_lab/output/"

(laboratories, hoodmodels, fumehoods, open_scraped, flow_scraped) = load_environment(data_directory)
print laboratories
print hoodmodels
print fumehoods
print open_scraped
print flow_scraped