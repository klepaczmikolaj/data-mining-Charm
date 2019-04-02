import json
import pandas as pd


class DataPreparation:
    transactional = []
    tid_count = 0

    def import_data(self, filename):
        with open(filename, 'r') as file:
            tid = 1
            for line in file:
                line = line.strip().split()
                for element in line:
                    self.transactional.append({'tid': tid, 'item': element})
                tid += 1
        self.tid_count = tid

    def transform_data(self):
        df = pd.DataFrame(self.transactional)
        self.itemsGrouped = df.groupby(['item'])['tid'].apply(list)
        self.itemsGrouped = pd.DataFrame({'item': self.itemsGrouped.index, 'tid': self.itemsGrouped.values})

    def get_frequent_items(self, min_sup):
        return self.itemsGrouped[self.itemsGrouped['tid'].map(len) >= min_sup * self.tid_count]


class CharmAlgorithm:

    def charm_extend(self, items_grouped, min_sup):
        result = pd.DataFrame(columns=['item', 'tid'])
        for index_1, row_1 in items_grouped.iterrows():
            items_tmp = pd.DataFrame()
            item = list()
            item.extend(row_1['item'])
            for index_2, row_2 in items_grouped.iterrows():
                # specify ordering rule
                if index_2 > index_1:
                    item.extend(row_2['item'])
                    tid = list(set(row_1['tid']) & set(row_2['tid']))
                    # print(item)
                    # print(tid)
                    # =======================================
                    # charm property start
                    if len(tid) >= min_sup:
                        if set(row_1['tid']) == set(row_2['tid']):
                            # remove row_2['item'] from items_grouped
                            items_grouped = items_grouped[items_grouped.item != row_2['item']]
                            # replace all row_1['item'] with item
                            items_grouped.loc[items_grouped.item == row_1.item, 'item'] = item
                        elif set(row_1['tid']).issubset(set(row_2['tid'])):
                            # replace all Xi with X
                            items_grouped.loc[items_grouped.item == row_1.item, 'item'] = item
                        elif set(row_2['tid']).issubset(set(row_1['tid'])):
                            # remove row_2['item'] from items_grouped
                            items_grouped = items_grouped[items_grouped.item != row_2['item']]
                            # add {item, tid} to items_tmp (at specified ordering rule)
                            items_grouped = items_grouped.append({'item': item, 'tid': tid}, ignore_index=True)
                        elif set(row_1['tid']) != set(row_2['tid']):
                            # add {item, tid} to items_tmp (at specified ordering rule)
                            items_grouped = items_grouped.append({'item': item, 'tid': tid}, ignore_index=True)

                    # charm property end
                    # =======================================
            if items_tmp.empty:
                self.charm_extend(items_tmp, min_sup)
            # TODO - check if x not subsumed
            items_grouped = items_grouped.append({'item': item, 'tid': tid}, ignore_index=True)
        return result

    def charm_property(self, items_grouped, items_tmp):
        pass


with open('config.json', 'r') as config_file:
    config = json.load(config_file)

data = DataPreparation()
data.import_data(config['file_name'])
data.transform_data()
freq = data.get_frequent_items(config['min_sup'])

print(freq)
print(data.itemsGrouped)

algorithm = CharmAlgorithm()
result_list = algorithm.charm_extend(data.itemsGrouped, config['min_sup'])
