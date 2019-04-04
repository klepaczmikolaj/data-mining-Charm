import unittest
import charm
import json
import pandas as pd


# class CharmTest(unittest.TestCase()):
    # def setUp(self):

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
data = charm.DataPreparation()
data.import_data(config['file_name'])
data.transform_data()
freq = data.get_frequent_items(config['min_sup'])

print(freq)

algorithm = charm.CharmAlgorithm(config['min_sup'], data.tid_count)

# testing parameters
row1 = pd.Series({'item': {'A'}, 'tid': [1, 3, 4, 5, 6]})
row2 = pd.Series({'item': {'C'}, 'tid': [1, 3, 4, 5]})
items = freq
items_tmp = pd.DataFrame()
new_item = {'C', 'D'}
new_tid = [1, 2, 3, 4, 5]

s = freq.tid.str.len().sort_values().index
freq = freq.reindex(s).reset_index(drop=True)
# freq = freq.reset_index(drop=True)
print(freq)
print(len(freq.index))