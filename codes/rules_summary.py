
import os
import pickle

rules_path = '../rules'
results_path = '../../results/results_2656.pkl'

rules_dict_sansol = {}
rules_dict_sansolf = {}

rules_count_sansol = {}
rules_count_sansolf = {}

results = pickle.load(open(results_path, 'rb'))

for file in os.listdir(rules_path):
    if 'false' in file and 'Claros' not in file:
        rpns = file.split('_')[1]
        id = file.split('_')[2].split('.')[0]
        # if rpns not in rules_dict_sansol.keys():
        #     rules_dict_sansol[rpns] = {}
        # if id not in rules_dict_sansol[rpns].keys():
        #     rules_dict_sansol[rpns][id] = []
        # if rpns not in rules_dict_sansolf.keys():
        #     rules_dict_sansolf[rpns] = {}
        # if id not in rules_dict_sansolf[rpns].keys():
        #     rules_dict_sansolf[rpns][id] = []

        print(file)
        with open(os.path.join(rules_path, file), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                if line:
                    if 'RP' in line.split(':-')[1] and 'RP' in line.split(':-')[0]:
                        if line not in rules_dict_sansol.keys():
                            rules_dict_sansol[line] = []
                            rules_count_sansol[line] = 0
                        if line not in rules_dict_sansolf.keys():
                            rules_dict_sansolf[line] = []
                            rules_count_sansolf[line] = 0
                        if rpns in results['SANSOL'].keys():
                            if id in results['SANSOL'][rpns]:
                                mrr = results['SANSOL'][rpns][id]['MRR']
                                rules_dict_sansol[line].append(mrr)
                                rules_count_sansol[line] += 1
                        if rpns in results['SANSOLF'].keys():
                            if id in results['SANSOLF'][rpns]:
                                mrr = results['SANSOLF'][rpns][id]['MRR']
                                rules_dict_sansolf[line].append(mrr)
                                rules_count_sansolf[line] += 1

for rule, values in rules_dict_sansol.items():
    if len(values):
        rules_dict_sansol[rule] = sum(values) / len(values)
for rule, values in rules_dict_sansolf.items():
    if len(values):
        rules_dict_sansolf[rule] = sum(values) / len(values)
for rule, count in rules_count_sansol.items():
    if count == 0:
        del rules_dict_sansol[rule]
for rule, count in rules_count_sansolf.items():
    if count == 0:
        del rules_dict_sansolf[rule]

# print(rules_dict_sansol)
#
# print(rules_dict_sansolf)

keys = [k for k in rules_count_sansol.keys()]
for key in keys:
    if rules_count_sansol[key] == 0:
        del rules_count_sansol[key]
keys = [k for k in rules_count_sansolf.keys()]
for key in keys:
    if rules_count_sansolf[key] == 0:
        del rules_count_sansolf[key]

# print(rules_count_sansol)
# print(rules_count_sansolf)

rpns_list = [str(x) for x in [5, 10, 15, 20, 25, 32, 40, 50, 60, 70, 80, 90, 100]]
rpns_ids = [str(x) for x in range(5)]
result_list = [[None for x in range(len(rpns_list))] for y in range(len(rpns_ids))]

for k0, v0 in results['SANSOLFcorr4'].items():
    for k1, v1 in v0.items():
        if k1 in rpns_ids and k0 in rpns_list:
            result_list[rpns_ids.index(k1)][rpns_list.index(k0)] = v1['MRR']
        elif str(k1) in rpns_ids and str(k0) in rpns_list:
            result_list[rpns_ids.index(str(k1))][rpns_list.index(str(k0))] = v1['MRR']
        elif str(k1) in rpns_ids and k0 in rpns_list:
            result_list[rpns_ids.index(str(k1))][rpns_list.index(k0)] = v1['MRR']
        elif k1 in rpns_ids and str(k0) in rpns_list:
            result_list[rpns_ids.index(k1)][rpns_list.index(str(k0))] = v1['MRR']
        else:
            result_list[0][0] = v1['MRR']

# print(results['SANS2'])
# print(result_list)
for row in result_list:
    for item in row:
        print(item, '\t', end='')
    print('')