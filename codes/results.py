import pickle


def read_results(method, k_hop, rw=100, rpns_rate=0, rpns_id=0, path='../results/results_2656.pkl'):
    key = ('RW' if rw > 0 else '') + method + (str(rw) if rw > 0 else '')
    results = pickle.load(open(path, 'rb'))
    print(results[key][rpns_rate][rpns_id]['MRR'])


read_results('SANS', 3, 0, 0, 0 )