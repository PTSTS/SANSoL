
import subprocess
import pickle
import sys
from os.path import exists
import cProfile


def run_command(lies_path, k_hop, ns, rw=False):
    if not rw:
        command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
            f"""256 -b 1024 -d 1000 -g 24.0 -a 1.0 -lr 0.05 --max_steps 2656 -save models/{lies_path.split('/')[-1]} """ \
            f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns {ns} --lies {lies_path} -save_results 1"""\
            """ --results /var/scratch/yan370/SANSOL/results.txt"""
    else:
        command = f"""python -u codes/run.py --cuda --do_train --do_valid --data_path data/converted --model TransE -n """\
            f"""256 -b 1024 -d 1000 -g 24.0 -a 1.0 -lr 0.05 --max_steps 2656 -save models/{lies_path.split('/')[-1]} """ \
            f"""--test_batch_size 16 -khop {k_hop} --log_steps 100000 -ns {ns} --lies {lies_path} -save_results 1"""\
            """ --results /var/scratch/yan370/SANSOL/results.txt -nrw 100"""

    cmd = subprocess.run(command, shell=True)


def main(skip_to_rpns=None, skip_to_id=None, k_hop=3, corr=False, rw=False):
    ns = sys.argv[1]
    base_path = '/var/scratch/yan370/VLog'
    rpns_rates = [32, 40, 50, 60, 70, 80, 90, 100]

    results_path = '/var/scratch/yan370/SANSOL/results.txt'
    for rate in rpns_rates:
        for i in range(5):
            if skip_to_rpns is not None:
                if int(skip_to_rpns) > rate:
                    continue
            if skip_to_id is not None:
                if int(skip_to_id) > i:
                    continue
            if exists(f'{base_path}/mat_false_{rate}_{i}/train.txt'):
                print(f'{rate} {i} '
                      f'______________________________________________________________________________________')
                # for k in range(2, 8):
                try:
                    run_command(
                        f'{base_path}/mat_false_{rate}_{i}' if not corr else f'{base_path}/mat_false_corr_{rate}_{i}',
                        k_hop, ns, rw=rw
                    )
                    with open(results_path, 'a', encoding='utf-8') as f:
                        f.write(f'Above results are from rules {rate}-{i}, k={3}\n')
                except FileNotFoundError:
                    print(f'Rules {rate} {i} not found')


if __name__ == '__main__':
    if len(sys.argv) > 2:
        start_rpns_rate = sys.argv[2]
        start_rpns_id = sys.argv[3]
        k = int(sys.argv[4])
        corr = False
        rw = False
        if len(sys.argv) > 5:
            corr = bool(sys.argv[5])
        if len(sys.argv) > 6:
            rw = bool(sys.argv[6])

        main(start_rpns_rate, start_rpns_id, k, corr, rw)
    else:
        main()
