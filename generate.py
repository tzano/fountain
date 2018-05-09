import sys

from fountain.data_generator import DataGenerator

# DataGenerator
data_generator = DataGenerator()
# load template
template_fname = sys.argv[1]
# parse the DSL template
results = data_generator.parse(template_fname)

# export to csv file
data_generator.to_csv('results.csv')
# export to csv file
# data_generator.to_json('results.json')
