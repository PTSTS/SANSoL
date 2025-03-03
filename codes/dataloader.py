import logging
import os
import time

import numpy as np
import torch
from scipy import sparse
from torch.utils.data import Dataset


def time_it(fn):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = fn(*args, **kwargs)
        end = time.time()
        logging.info(f'Time: {end - start}')
        return ret

    return wrapper


class TrainDataset(Dataset):

    def _get_adj_mat(self):
        a_mat = sparse.dok_matrix((self.nentity, self.nentity))
        for (h, _, t) in self.triples:
            a_mat[t, h] = 1
            a_mat[h, t] = 1

        a_mat = a_mat.tocsr()
        return a_mat

    def _get_lies_adj_mat(self):
        a_mat = sparse.dok_matrix((self.nentity, self.nentity))
        for (h, _, t) in self.lies_triples:
            a_mat[t, h] = 1
            a_mat[h, t] = 1

        a_mat = a_mat.tocsr()
        return a_mat

    @time_it
    def build_k_hop(self, k_hop, dataset_name):
        if k_hop == 0:
            return None

        save_path = f'cached_matrices/matrix_{dataset_name}_k{k_hop}_nrw0.npz'

        if os.path.exists(save_path):
            logging.info(f'Using cached matrix: {save_path}')
            k_mat = sparse.load_npz(save_path)
            return k_mat

        _a_mat = self._get_adj_mat()
        _k_mat = _a_mat ** (k_hop - 1)
        k_mat = _k_mat * _a_mat + _k_mat

        sparse.save_npz(save_path, k_mat)

        return k_mat

    @time_it
    def build_lies_k_hop(self, k_hop, dataset_name):
        if k_hop == 0:
            return None

        save_path = f'cached_matrices/matrix_{dataset_name}_lies_k{k_hop}_nrw0.npz'

        if os.path.exists(save_path):
            logging.info(f'Using cached matrix: {save_path}')
            k_mat = sparse.load_npz(save_path)
            return k_mat

        _a_mat = self._get_adj_mat()
        _k_mat = _a_mat ** (k_hop - 1)
        k_mat = _k_mat * _a_mat + _k_mat

        sparse.save_npz(save_path, k_mat)

        return k_mat

    @time_it
    def build_k_rw(self, n_rw, k_hop, dataset_name):
        """
        Returns:
            k_mat: sparse |V| * |V| adjacency matrix
        """
        if n_rw == 0 or k_hop == 0:
            return None

        save_path = f'cached_matrices/matrix_{dataset_name}_k{k_hop}_nrw{n_rw}.npz'

        if os.path.exists(save_path):
            logging.info(f'Using cached matrix: {save_path}')
            k_mat = sparse.load_npz(save_path)
            return k_mat

        a_mat = self._get_adj_mat()
        k_mat = sparse.dok_matrix((self.nentity, self.nentity))

        randomly_sampled = 0

        for i in range(0, self.nentity):
            neighbors = a_mat[i]
            if len(neighbors.indices) == 0:
                randomly_sampled += 1
                walker = np.random.randint(self.nentity, size=n_rw)
                k_mat[i, walker] = 1
            else:
                for _ in range(0, n_rw):
                    walker = i
                    for _ in range(0, k_hop):
                        idx = np.random.randint(len(neighbors.indices))
                        walker = neighbors.indices[idx]
                        neighbors = a_mat[walker]
                    k_mat[i, walker] += 1
        logging.info(f'randomly_sampled: {randomly_sampled}')
        k_mat = k_mat.tocsr()

        sparse.save_npz(save_path, k_mat)

        return k_mat

    @time_it
    def build_lies_k_rw(self, n_rw, k_hop, dataset_name):
        if n_rw == 0 or k_hop == 0:
            return None

        save_path = f'cached_matrices/matrix_{dataset_name}_lies_k{k_hop}_nrw{n_rw}.npz'

        if os.path.exists(save_path):
            logging.info(f'Using cached matrix: {save_path}')
            k_mat = sparse.load_npz(save_path)
            return k_mat

        a_mat = self._get_lies_adj_mat()
        k_mat = sparse.dok_matrix((self.nentity, self.nentity))

        randomly_sampled = 0

        for i in range(0, self.nentity):
            neighbors = a_mat[i]
            if len(neighbors.indices) == 0:
                randomly_sampled += 1
                walker = np.random.randint(self.nentity, size=n_rw)
                k_mat[i, walker] = 1
            else:
                for _ in range(0, n_rw):
                    walker = i
                    for _ in range(0, k_hop):
                        idx = np.random.randint(len(neighbors.indices))
                        walker = neighbors.indices[idx]
                        neighbors = a_mat[walker]
                    k_mat[i, walker] += 1
        logging.info(f'randomly_sampled: {randomly_sampled}')
        k_mat = k_mat.tocsr()

        sparse.save_npz(save_path, k_mat)
        return k_mat

    def __init__(self, triples, nentity, nrelation, negative_sample_size, mode, k_hop, n_rw, dsn,
                 method, lies_triples=None):
        self.len = len(triples)
        self.triples = triples
        self.triple_set = set(triples)
        self.nentity = nentity
        self.nrelation = nrelation
        self.negative_sample_size = negative_sample_size
        self.mode = mode
        self.count = self.count_frequency(triples)
        self.true_head, self.true_tail = self.get_true_head_and_tail(self.triples)
        self.dsn = dsn.split('/')[1]  # dataset name
        self.method = method
        self.pseudo_head = None
        self.pseudo_tail = None
        if lies_triples is not None:
            self.lies_triples = lies_triples
            self.lies_triples_set = set(lies_triples)
        if method == 'pseudo':
            self.pseudo_head = {}
            self.pseudo_tail = {}
            for triple in triples:
                h, r, t = triple
                if r not in self.pseudo_head.keys():
                    self.pseudo_head[r] = set()
                if r not in self.pseudo_tail.keys():
                    self.pseudo_tail[r] = set()
                self.pseudo_tail[r].add(t)
                self.pseudo_head[r].add(h)
        elif method == 'pseudo-lies':
            self.pseudo_head = {}
            self.pseudo_tail = {}
            assert lies_triples is not None
            for triple in lies_triples:
                h, r, t = triple
                if r not in self.pseudo_head.keys():
                    self.pseudo_head[r] = set()
                if r not in self.pseudo_tail.keys():
                    self.pseudo_tail[r] = set()
                self.pseudo_tail[r].add(t)
                self.pseudo_head[r].add(h)
            for triple in triples:
                h, r, t = triple
                if r not in self.pseudo_head.keys():
                    self.pseudo_head[r] = set()
                if r not in self.pseudo_tail.keys():
                    self.pseudo_tail[r] = set()
                self.pseudo_tail[r].add(t)
                self.pseudo_head[r].add(h)


        elif method != 'uniform':
            if n_rw == 0:
                self.k_neighbors = self.build_k_hop(k_hop, dataset_name=self.dsn)
                if self.method != 'SANS':
                    self.lies_k_neighbors = self.build_lies_k_hop(k_hop, dataset_name=self.dsn)
                else:
                    self.lies_k_neighbors = None
            else:
                self.k_neighbors = self.build_k_rw(n_rw=n_rw, k_hop=k_hop, dataset_name=self.dsn)
                if self.method != 'SANS':
                    self.lies_k_neighbors = self.build_lies_k_rw(n_rw=n_rw, k_hop=k_hop, dataset_name=self.dsn)
                else:
                    self.lies_k_neighbors = None

        print(self.method)

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        positive_sample = self.triples[idx]

        head, relation, tail = positive_sample

        subsampling_weight = self.count[(head, relation)] + self.count[(tail, -relation - 1)]
        subsampling_weight = torch.sqrt(1 / torch.Tensor([subsampling_weight]))

        negative_sample_list = []
        negative_sample_size = 0
        previous_negative_sample_size = 0

        k_hop_flag = True
        lies_k_hop_flag = True
        while negative_sample_size < self.negative_sample_size:
            if self.method == 'uniform':
                negative_sample = np.random.randint(self.nentity, size=self.negative_sample_size * 2)
            elif self.method == 'pseudo' or self.method == 'pseudo-lies':
                if self.mode == 'head-batch':
                    if not k_hop_flag:
                        negative_sample = np.random.randint(self.nentity, size=self.negative_sample_size * 2)
                    else:
                        negative_sample = np.random.choice(list(self.pseudo_head[relation]), size=self.negative_sample_size * 2)
                if self.mode == 'tail-batch':
                    if not k_hop_flag:
                        negative_sample = np.random.randint(self.nentity, size=self.negative_sample_size * 2)
                    else:
                        negative_sample = np.random.choice(list(self.pseudo_tail[relation]), size=self.negative_sample_size * 2)
            else:
                if self.k_neighbors is not None and k_hop_flag:
                    if self.method == 'SANS':
                        if self.mode == 'head-batch':
                            khop = self.k_neighbors[tail].indices
                        elif self.mode == 'tail-batch':
                            khop = self.k_neighbors[head].indices
                    elif self.method == 'SANSOL':
                        if self.mode == 'head-batch':
                            khop = self.lies_k_neighbors[tail].indices
                        elif self.mode == 'tail-batch':
                            khop = self.lies_k_neighbors[head].indices
                    elif self.method == 'SANSOLF':
                        if lies_k_hop_flag:
                            if self.mode == 'head-batch':
                                khop = self.lies_k_neighbors[tail].indices
                            elif self.mode == 'tail-batch':
                                khop = self.lies_k_neighbors[head].indices
                        else:
                            if self.mode == 'head-batch':
                                khop = self.k_neighbors[tail].indices
                            elif self.mode == 'tail-batch':
                                khop = self.k_neighbors[head].indices
                    else:
                        raise ValueError('Training batch mode %s not supported' % self.mode)
                    negative_sample = khop[np.random.randint(len(khop), size=self.negative_sample_size * 2)].astype(
                        np.int64)
                else:
                    negative_sample = np.random.randint(self.nentity, size=self.negative_sample_size * 2)
            if self.mode == 'head-batch':
                mask = np.in1d(
                    negative_sample,
                    self.true_head[(relation, tail)],
                    assume_unique=True,
                    invert=True
                )
            elif self.mode == 'tail-batch':
                mask = np.in1d(
                    negative_sample,
                    self.true_tail[(head, relation)],
                    assume_unique=True,
                    invert=True
                )
            else:
                raise ValueError('Training batch mode %s not supported' % self.mode)
            negative_sample = negative_sample[mask]
            negative_sample_list.append(negative_sample)
            if negative_sample.size == 0:
                k_hop_flag = False
            negative_sample_size += negative_sample.size
            if negative_sample_size == 0 and self.method == 'SANSOLF':
                lies_k_hop_flag = False

        negative_sample = np.concatenate(negative_sample_list)[:self.negative_sample_size]

        negative_sample = torch.from_numpy(negative_sample)

        positive_sample = torch.LongTensor(positive_sample)
        return positive_sample, negative_sample, subsampling_weight, self.mode

    @staticmethod
    def collate_fn(data):
        positive_sample = torch.stack([_[0] for _ in data], dim=0)
        negative_sample = torch.stack([_[1] for _ in data], dim=0)
        subsample_weight = torch.cat([_[2] for _ in data], dim=0)
        mode = data[0][3]
        return positive_sample, negative_sample, subsample_weight, mode

    @staticmethod
    def count_frequency(triples, start=4):
        '''
        Get frequency of a partial triple like (head, relation) or (relation, tail)
        The frequency will be used for subsampling like word2vec
        '''
        count = {}
        for head, relation, tail in triples:
            if (head, relation) not in count:
                count[(head, relation)] = start
            else:
                count[(head, relation)] += 1

            if (tail, -relation - 1) not in count:
                count[(tail, -relation - 1)] = start
            else:
                count[(tail, -relation - 1)] += 1
        return count

    @staticmethod
    def get_true_head_and_tail(triples):
        '''
        Build a dictionary of true triples that will
        be used to filter these true triples for negative sampling
        '''

        true_head = {}
        true_tail = {}

        for head, relation, tail in triples:
            if (head, relation) not in true_tail:
                true_tail[(head, relation)] = []
            true_tail[(head, relation)].append(tail)
            if (relation, tail) not in true_head:
                true_head[(relation, tail)] = []
            true_head[(relation, tail)].append(head)

        for relation, tail in true_head:
            true_head[(relation, tail)] = np.array(list(set(true_head[(relation, tail)])))
        for head, relation in true_tail:
            true_tail[(head, relation)] = np.array(list(set(true_tail[(head, relation)])))

        return true_head, true_tail


class TestDataset(Dataset):
    def __init__(self, triples, all_true_triples, nentity, nrelation, mode):
        self.len = len(triples)
        self.triple_set = set(all_true_triples)
        self.triples = triples
        self.nentity = nentity
        self.nrelation = nrelation
        self.mode = mode

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        head, relation, tail = self.triples[idx]

        if self.mode == 'head-batch':
            tmp = [(0, rand_head) if (rand_head, relation, tail) not in self.triple_set
                   else (-1, head) for rand_head in range(self.nentity)]
            tmp[head] = (0, head)
        elif self.mode == 'tail-batch':
            tmp = [(0, rand_tail) if (head, relation, rand_tail) not in self.triple_set
                   else (-1, tail) for rand_tail in range(self.nentity)]
            tmp[tail] = (0, tail)
        else:
            raise ValueError('negative batch mode %s not supported' % self.mode)

        tmp = torch.LongTensor(tmp)
        filter_bias = tmp[:, 0].float()
        negative_sample = tmp[:, 1]

        positive_sample = torch.LongTensor((head, relation, tail))

        return positive_sample, negative_sample, filter_bias, self.mode

    @staticmethod
    def collate_fn(data):
        positive_sample = torch.stack([_[0] for _ in data], dim=0)
        negative_sample = torch.stack([_[1] for _ in data], dim=0)
        filter_bias = torch.stack([_[2] for _ in data], dim=0)
        mode = data[0][3]
        return positive_sample, negative_sample, filter_bias, mode


class BidirectionalOneShotIterator(object):
    def __init__(self, dataloader_head, dataloader_tail):
        self.iterator_head = self.one_shot_iterator(dataloader_head)
        self.iterator_tail = self.one_shot_iterator(dataloader_tail)
        self.step = 0

    def __next__(self):
        self.step += 1
        if self.step % 2 == 0:
            data = next(self.iterator_head)
        else:
            data = next(self.iterator_tail)
        return data

    @staticmethod
    def one_shot_iterator(dataloader):
        '''
        Transform a PyTorch Dataloader into python iterator
        '''
        while True:
            for data in dataloader:
                yield data
