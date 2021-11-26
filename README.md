# Negative Sampling with Rule-Based Reasoning on Knowledge Graphs

## Introduction

This repository provides the PyTorch implementation of the original _Structure Aware Negative Sampling (SANS)_ 
technique presented in _Structure Aware Negative Sampling in Knowledge Graphs_ paper as well as our new proposed 
methods and their variations:

* Pseudo-Type on Lies Negative Sampling (PTLNS)
* Structure Aware Negative Sampling on Lies (SANSoL)
* Sturcture Aware Negative Sampling on Lies and 
Facts (SANSoLF) 
* Structure Aware Negative Sampling on Lies with Random Walk (RW-SANSoL)
* Sturcture Aware Negative Sampling on Lies and 
Facts with Random Walk (RW-SANSoLF) 

This repository is a part of a Master thesis project.

## Execution

As an example, the following command trains and validates a TransE model on wn18rr dataset by using RW-SANSOL with 
1000 random walks on 3-Hop neighborhood:

```bash
CUDA_VISIBLE_DEVICES=0 python -u codes/run.py --cuda \
    --do_train --do_valid \
    --data_path data/wn18rr \
    --model TransE \
    -n 256 -b 1024 -d 1000 \
    -g 24.0 -a 1.0 \
    -lr 0.0001 --max_steps 150000 \
    -save models/TransE_wn18rr_0 --test_batch_size 16 \
    -khop 3 -nrw 1000 \
    --lies data/lies \
    -ns SANSOL \
    --remove_self_loops 1 
```

To check all the available arguments, you can run `python codes/run.py --help`.

## Acknowledgments
