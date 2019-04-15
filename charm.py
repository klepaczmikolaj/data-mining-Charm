import json
from copy import copy, deepcopy
import pandas as pd
import time
import argparse


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
        self.tid_count = tid - 1

    def transform_data(self):
        df = pd.DataFrame(self.transactional)
        self.itemsGrouped = df.groupby(['item'])['tid'].apply(list)
        self.itemsGrouped = pd.DataFrame({'item': self.itemsGrouped.index, 'tid': self.itemsGrouped.values})
        self.itemsGrouped['item'] = self.itemsGrouped['item'].apply(lambda x: {x})

    def get_frequent_items(self, min_sup):
        return self.itemsGrouped[self.itemsGrouped['tid'].map(len) >= min_sup * self.tid_count]


class CharmAlgorithm:
    def __init__(self, min_sup_config, tid_count):
        self.result = pd.DataFrame(columns=['item', 'tid', 'support'])
        self.min_sup = min_sup_config * tid_count

    @staticmethod
    def replace_values(df, column, find, replace):
        for row in df.itertuples():
            if find <= row[column]:
                row[column].update(replace)

    def charm_property(self, row1, row2, items, new_item, new_tid):
        if len(new_tid) >= self.min_sup:
            if set(row1[2]) == set(row2[2]):
                # remove row2[1] from items
                items = items[items['item'] != row2[1]]
                # replace all row1[1] with new_item
                find = copy(row1[1])
                self.replace_values(items, 1, find, new_item)
                self.replace_values(self.items_tmp, 1, find, new_item)
            elif set(row1[2]).issubset(set(row2[2])):
                # replace all row1[1] with new_item
                find = copy(row1[1])
                self.replace_values(items, 1, find, new_item)
                self.replace_values(self.items_tmp, 1, find, new_item)
            elif set(row2[2]).issubset(set(row1[2])):
                # remove row2[1] from items
                items = items[items['item'] != row2[1]]
                # add {item, tid} to self.items_tmp
                self.items_tmp = self.items_tmp.append({'item': new_item, 'tid': new_tid}, ignore_index=True)
                # sort items by ascending support
                # s = self.items_tmp.tid.str.len().sort_values().index
                # self.items_tmp = self.items_tmp.reindex(s).reset_index(drop=True)
            elif set(row1[2]) != set(row2[2]):
                # add {item, tid} to self.items_tmp
                self.items_tmp = self.items_tmp.append({'item': new_item, 'tid': new_tid}, ignore_index=True)
                # sort items by ascending support
                # s = self.items_tmp.tid.str.len().sort_values().index
                # self.items_tmp = self.items_tmp.reindex(s).reset_index(drop=True)

    def charm_extend(self, items_grouped):
        # sort items by ascending support
        s = items_grouped.tid.str.len().sort_values().index
        items_grouped = items_grouped.reindex(s).reset_index(drop=True)

        for row1 in items_grouped.itertuples():
            self.items_tmp = pd.DataFrame(columns=['item', 'tid'])
            for row2 in items_grouped.itertuples():
                if row2[0] >= row1[0]:
                    item = set()
                    item.update(row1[1])
                    item.update(row2[1])
                    tid = list(set(row1[2]) & set(row2[2]))
                    self.charm_property(row1, row2, items_grouped, item, tid)
            if not self.items_tmp.empty:
                self.charm_extend(self.items_tmp)
            # check if item subsumed
            is_subsumption = False
            for row in self.result.itertuples():
                if row1[1].issubset(row[1]) and set(row[2]) == set(row1[2]):
                    is_subsumption = True
                    break
            # append to result if element not subsumed
            if not is_subsumption:
                self.result = self.result.append({'item': row1[1], 'tid': row1[2], 'support': len(row1[2])}, ignore_index=True)

    def write_result_to_file(self, result_file):
        self.result.to_csv(result_file, sep='\t', columns=['item', 'support'], index=False)

    def write_result_to_smfl_format(self, result_file):
        self.result['item'] = self.result['item'].apply(lambda x: sorted(map(int, x)))
        self.result.to_csv(result_file, sep='\t', columns=['item', 'support'], index=False, header=False)


if __name__ == '__main__':
    start = time.time()

    # parse args
    parser = argparse.ArgumentParser(description='Generate closed frequent itemsets')
    parser.add_argument('-f', '--filename', help="Name of the file with data for itemset generation", required=True)
    parser.add_argument('-s', '--support', help="Minimum support for frequent itemsets", required=True, type=float)
    parser.add_argument('--output', help="Output file name, default: output.txt", required=False, default='output.txt')
    parser.add_argument('--spmf-format', help="Specify output file format as SPMF", required=False, action='store_true')
    args = parser.parse_args()

    # preparation
    data = DataPreparation()
    data.import_data(args.filename)
    data.transform_data()
    freq = data.get_frequent_items(args.support)

    # algorithm
    algorithm = CharmAlgorithm(args.support, data.tid_count)
    algorithm.charm_extend(freq)

    # write to file
    if args.spmf_format:
        algorithm.write_result_to_smfl_format(args.output)
    else:
        algorithm.write_result_to_file(args.output)

    end = time.time()
    print("##############################################################")
    print('File: ' + args.filename)
    print('Python elapsed time: ' + str(round((end - start), 3)) + ' s')
