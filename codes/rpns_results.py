key = 'RWSANSOL5'
mode = 'rpns-k'

rpns_rates = [5, 10, 15, 20, 25, 32, 40, 50, 60, 70, 80, 90, 100]
methods = ['SANSOL', 'SANSOLF', 'SANSOLcorr', 'SANSOLFcorr', 'RWSANSOL', 'RWSANSOLF', 'RWSANSOLcorr', 'RWSANSOLFcorr']
with open('../../results/rpns.csv', 'r') as f:
    lines = f.readlines()

def get_result_array(method_str):
    results_array = [[None for i in rpns_rates] for j in range(5)]
    for line in lines:
        if line:
            result = line.split(sep='\t')
            if result[0] == method_str:
                if results_array[int(result[2])][rpns_rates.index(int(result[1]))] is not None:
                    continue
                else:
                    results_array[int(result[2])][rpns_rates.index(int(result[1]))] = float(result[3])
    return results_array




if mode == 'rpns':
    array = get_result_array(key)
    for row in array:
        print('\t'.join([str(x) for x in row]))
    # print(results_array)

elif mode == 'hops-ns':
    for k in range(2, 9):
        for ns in methods:
            array = get_result_array(ns + str(k))
            count = 0
            total = 0
            for row in array:
                for cell in row:
                    if cell is not None:
                        total += cell
                        count += 1

            average = total / count if count != 0 else 0

            print(average, end='\t')
        print('')

elif mode == 'rpns-ave':
    full_array = [[0 for i in rpns_rates] for j in range(5)]
    count_array = [[0 for i in rpns_rates] for j in range(5)]
    for k in range(2, 9):
        for ns in methods:
            array = get_result_array(ns + str(k))
            for i, row in enumerate(array):
                for j, cell in enumerate(row):
                    if cell is not None:
                        full_array[i][j] += cell
                        count_array[i][j] += 1

    for i, row in enumerate(full_array):
        for j, cell in enumerate(row):
            if count_array[i][j] > 0:
                print(cell / count_array[i][j], end='\t')
        print('')

if mode == 'rpns-k':
    for k in range(2, 9):
        rpns_total = [0 for x in rpns_rates]
        rpns_counts = [0 for x in rpns_rates]
        for ns in methods:
            array = get_result_array(ns + str(k))
            for i, row in enumerate(array):
                for j, cell in enumerate(row):
                    if cell is not None:
                        rpns_total[j] += cell
                        rpns_counts[j] += 1
        k_average = [str(rpns_total[i] / rpns_counts[i]) if rpns_counts[i] != 0 else '0' for i in range(len(rpns_total))]
        print('\t'.join(k_average))
