import optuna

from run import *
import sys
import random
import subprocess


def obj_sansol(trial: optuna.trial.Trial):
    key = random.randint(0, 999999)

    k_hop = trial.suggest_int('k', 2, 8)
    lr = trial.suggest_float('lr', 0.0001, 0.1)
    nss = trial.suggest_int('nss', 4, 256)
    b = trial.suggest_int('b', 16, 2048)
    rpns_rate = [5, 10, 15, 20, 25, 40][trial.suggest_int('rpns_rate', 0, 5)]
    rpns_id = trial.suggest_categorical('rpns_id', [0, 1, 2, 3, 4])

    base_path = '/var/scratch/yan370/VLog'
    lies_path = f'{base_path}/mat_false_{rpns_rate}_{rpns_id}'
    temp_results_path = f'{key}.pkl'
    command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
        f"""{nss} -b {b} -d 1000 -g 24.0 -a 1.0 -lr {lr} --max_steps 2656 -save models/{lies_path.split('/')[-1]} """ \
        f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns SANSOL --lies {lies_path} -save_results 1 """\
        f"""--results /var/scratch/yan370/SANSOL/results.txt """\
        f"""--temp_results {temp_results_path}"""
    cmd = subprocess.Popen(command, shell=True)
    cmd.communicate()
    results = pickle.load(open(temp_results_path, 'rb'))
    os.remove(temp_results_path)
    return results['MRR']


if __name__ == '__main__':
    study = optuna.create_study()
    n = 1000
    study.optimize(obj_sansol, n_trials=n)
