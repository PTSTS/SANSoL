# Best Configuration for RotatE
#
bash run.sh train RotatE FB15k-237 0 0 1024 256 1000 9.0 1.0 0.00005 100000 16 2 4000 -de
bash run.sh train RotatE FB15k-237 0 0 1024 256 1000 9.0 1.0 0.00005 100000 16 2 4000 -de -adv
bash run.sh train RotatE wn18 0 0 512 1024 500 12.0 0.5 0.0001 80000 8 2 3000 -de
bash run.sh train RotatE wn18 0 0 512 1024 500 12.0 0.5 0.0001 80000 8 2 4500 -de -adv
bash run.sh train RotatE wn18rr 0 0 512 1024 500 6.0 0.5 0.00005 80000 8 2 1000 -de
bash run.sh train RotatE wn18rr 0 0 512 1024 500 6.0 0.5 0.00005 80000 8 2 1000 -de -adv
#
# Best Configuration for TransE
#
bash run.sh train TransE FB15k-237 0 0 1024 256 1000 9.0 1.0 0.00005 100000 16 5 4000
bash run.sh train TransE FB15k-237 0 0 1024 256 1000 9.0 1.0 0.00005 100000 16 4 4000 -adv
bash run.sh train TransE wn18 0 0 512 1024 500 12.0 0.5 0.0001 80000 8 2 1000
bash run.sh train TransE wn18 0 0 512 1024 500 12.0 0.5 0.0001 80000 8 3 4000 -adv
bash run.sh train TransE wn18rr 0 0 512 1024 500 6.0 0.5 0.00005 80000 2 1000 8
bash run.sh train TransE wn18rr 0 0 512 1024 500 6.0 0.5 0.00005 80000 5 2000 8 -adv
#
# Best Configuration for DistMult
#
bash run.sh train DistMult FB15k-237 0 0 1024 256 2000 200.0 1.0 0.001 100000 16 4 3000 -r 0.00001
bash run.sh train DistMult FB15k-237 0 0 1024 256 2000 200.0 1.0 0.001 100000 16 5 3000 -r 0.00001 -adv
bash run.sh train DistMult wn18 0 0 512 1024 1000 200.0 1.0 0.001 80000 8 2 1000 -r 0.00001
bash run.sh train DistMult wn18 0 0 512 1024 1000 200.0 1.0 0.001 80000 8 2 1000 -r 0.00001 -adv
bash run.sh train DistMult wn18rr 0 0 512 1024 1000 200.0 1.0 0.002 80000 8 2 3000 -r 0.000005
bash run.sh train DistMult wn18rr 0 0 512 1024 1000 200.0 1.0 0.002 80000 8 4 1000 -r 0.000005 -adv
#
