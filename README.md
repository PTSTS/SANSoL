# Structure Aware Negative Sampling in Knowledge Graphs

## Introduction

This repository provides the PyTorch implementation of _Structure Aware Negative Sampling (SANS)_ technique as well as several popular KGE models.

## Execution

For example, the following command trains and validates a TransE model on wn18rr dataset by using RW-SANS with 1000 random walks on 3-Hop:

```bash
CUDA_VISIBLE_DEVICES=0 python -u codes/run.py --cuda \
    --do_train --do_valid \
    --data_path data/wn18rr \
    --model TransE \
    -n 256 -b 1024 -d 1000 \
    -g 24.0 -a 1.0 \
    -lr 0.0001 --max_steps 150000 \
    -save models/TransE_wn18rr_0 --test_batch_size 16 \
    -khop 3 -nrw 1000
```

To check all the available arguments, you can run `python codes/run.py --help`.

## Reproducibility

To reproduce the results in the EMNLP 2020 paper _Structure Aware Negative Sampling in Knowledge Graphs_, you can use the commands provided in `bash_config.sh`.

## Acknowledgment

Our implemention is based on the PyTorch implementation of RotatE model provided [here](https://github.com/DeepGraphLearning/KnowledgeGraphEmbedding).
