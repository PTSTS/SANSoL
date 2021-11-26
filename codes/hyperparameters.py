import optuna

from run import *
import sys
import random
import subprocess


def obj_sansol(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    k_hop = trial.suggest_int('k', 2, 8)
    lr = trial.suggest_float('lr', 0.0001, 0.1)
    gamma = trial.suggest_int('gamma', 0, 50)
    nss = 256
    b = trial.suggest_int('b', 16, 2048)

    # valid_paths = []
    # for filename in os.listdir('/var/scratch/yan370/VLog'):
    #     if 'mat_false' in filename:
    #         valid_paths.append(os.path.join(filename))
    # chosen_path = valid_paths[trial.suggest_categorical('rules', range(len(valid_paths)))]
    rpns_rate = int(sys.argv[2])
    rpns_id = int(sys.argv[3])
    # rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    # rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g {gamma} -a 1.0 -lr {lr} --max_steps 2656 -save models/SANSOL{lies_path.split('/')[-1]} """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANSOL --lies {lies_path} """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_sans(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)
    k_hop = trial.suggest_int('k', 2, 8)
    lr = 10 ** trial.suggest_float('log_lr', -1, -8)
    nss = trial.suggest_int('nss', 4, 256)
    gamma = trial.suggest_int('gamma', 0, 50)
    b = trial.suggest_int('b', 16, 2048)

    base_path = '/var/scratch/yan370/VLog'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g {gamma} -a 1.0 -lr {lr} --max_steps 2656 -save models/SANS """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANS """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_sansolf(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    k_hop = trial.suggest_int('k', 2, 8)
    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = trial.suggest_int('nss', 4, 256)
    b = trial.suggest_int('b', 16, 2048)

    valid_paths = []
    for filename in os.listdir('/var/scratch/yan370/VLog'):
        if 'mat_false' in filename:
            valid_paths.append(os.path.join(filename))
    # chosen_path = valid_paths[trial.suggest_categorical('rules', range(len(valid_paths)))]
    rpns_rate = int(sys.argv[2])
    rpns_id = int(sys.argv[3])
    # print(chosen_path)
    # print(valid_paths)
    # rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    # rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/SANSOLF{lies_path.split('/')[-1]} """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANSOLF --lies {lies_path} """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_rw_sans(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)
    k_hop = trial.suggest_int('k', 2, 8)
    rw = trial.suggest_int('rw', 5, 200)
    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = 256
    b = trial.suggest_int('b', 16, 2048)

    base_path = '/var/scratch/yan370/VLog'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/SANS """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANS """\
        f"""--temp_results {temp_results_path} -nrw {rw}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_rw_sansol(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    k_hop = trial.suggest_int('k', 2, 8)
    rw = trial.suggest_int('rw', 5, 200)
    lr = trial.suggest_float('lr', 0.0001, 0.1)
    gamma = trial.suggest_int('gamma', 0, 50)
    nss = 256
    b = trial.suggest_int('b', 16, 2048)

    rpns_rate = int(sys.argv[2])
    rpns_id = int(sys.argv[3])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g {gamma} -a 1.0 -lr {lr} --max_steps 2656 -save models/SANSOL{lies_path.split('/')[-1]} """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANSOL --lies {lies_path} """\
        f"""--temp_results {temp_results_path} -nrw {rw}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_rw_sansolf(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    k_hop = trial.suggest_int('k', 2, 8)
    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = 256
    rw = trial.suggest_int('rw', 5, 200)

    b = trial.suggest_int('b', 16, 2048)

    valid_paths = []
    for filename in os.listdir('/var/scratch/yan370/VLog'):
        if 'mat_false' in filename:
            valid_paths.append(os.path.join(filename))
    # chosen_path = valid_paths[trial.suggest_categorical('rules', range(len(valid_paths)))]
    rpns_rate = int(sys.argv[2])
    rpns_id = int(sys.argv[3])
    # print(chosen_path)
    # print(valid_paths)
    # rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    # rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/SANSOLF{lies_path.split('/')[-1]} """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANSOLF --lies {lies_path} """\
        f"""--temp_results {temp_results_path} -nrw {rw}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_pseudo(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = trial.suggest_int('nss', 4, 256)
    b = trial.suggest_int('b', 16, 2048)

    valid_paths = []
    for filename in os.listdir('/var/scratch/yan370/VLog'):
        if 'mat_false' in filename:
            valid_paths.append(os.path.join(filename))
    # chosen_path = valid_paths[trial.suggest_categorical('rules', range(len(valid_paths)))]
    rpns_rate = 20
    rpns_id = 7
    # print(chosen_path)
    # print(valid_paths)
    # rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    # rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/pseudo{key}""" \
        f""" --test_batch_size 16 -khop {0} --log_steps 100000 -ns pseudo -save_results 0 """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_pseudo_lies(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = trial.suggest_int('nss', 4, 256)
    b = trial.suggest_int('b', 16, 2048)

    valid_paths = []
    for filename in os.listdir('/var/scratch/yan370/VLog'):
        if 'mat_false' in filename:
            valid_paths.append(os.path.join(filename))
    # chosen_path = valid_paths[trial.suggest_categorical('rules', range(len(valid_paths)))]
    rpns_rate = int(sys.argv[2])
    rpns_id = int(sys.argv[3])
    # print(chosen_path)
    # print(valid_paths)
    # rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    # rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/pseudo-lies{key}""" \
        f""" --test_batch_size 16 -khop {0} --log_steps 100000 -ns pseudo-lies -save_results 0  --lies {lies_path} """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']


def obj_uniform(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = trial.suggest_int('nss', 4, 256)
    b = trial.suggest_int('b', 16, 2048)

    # print(chosen_path)
    # print(valid_paths)
    # rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    # rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/uniform{key} """ \
        f""" --test_batch_size 16 -khop {0} --log_steps 100000 -ns uniform -save_results 0 """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    out, err = cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return -results['MRR']

if __name__ == '__main__':
    study = optuna.create_study()
    n = 1000
    ns = sys.argv[1]
    if ns == 'SANS':
        study.optimize(obj_sans, n_trials=n)
    elif ns == 'SANSOL':
        study.optimize(obj_sansol, n_trials=n)
    elif ns == 'SANSOLF':
        study.optimize(obj_sansolf, n_trials=n)
    if ns == 'RWSANS':
        study.optimize(obj_rw_sans, n_trials=n)
    elif ns == 'RWSANSOL':
        study.optimize(obj_rw_sansol, n_trials=n)
    elif ns == 'RWSANSOLF':
        study.optimize(obj_rw_sansolf, n_trials=n)
    elif ns == 'pseudo':
        study.optimize(obj_pseudo, n_trials=n)
    elif ns == 'pseudo-lies':
        study.optimize(obj_pseudo_lies, n_trials=n)
    elif ns == 'uniform':
        study.optimize(obj_uniform, n_trials=n)
