#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import time


def prep_data(num_data, dim):
    '''
    generate a list of normalized random vectors
    '''
    vecs = []
    for i in range(num_data):
        v = np.random.rand(dim)
        v = v / np.linalg.norm(v)
        vecs.append(v)
    return vecs

def run(queries, data, alg, topn):
    '''
    run benchmark and return result
    '''
    # index construction
    start = time.time()
    index = alg['alg'].construct_index(data)
    const_time = time.time() - start

    # search
    start = time.time()
    alg['alg'].search(queries, index, topn)
    query_time = time.time() - start

    result = alg['name'] + ', ' + str(len(queries)) + ', ' + str(len(data)) + ', ' + str(topn) + ', ' + str(const_time) + ', ' + str(query_time) + '\n'
    return result


if __name__ == '__main__':
    import itertools

    import annoy_bench
    # import ngt_bench
    # import flann_bench
    # import faiss_bench
    # import nmslib_bench

    # prepare params
    algs = [{'name': 'annoy', 'alg': annoy_bench}, {'name': 'nmslib', 'alg': nmslib_bench}]
    q_nums = [10, 100, 1000, 10000]
    d_nums = [10000, 100000, 1000000]
    dims = [200]
    topn_nums = [10, 20, 30]
    
    data_set = []
    query_set = []
    for m, d in itertools.product(q_nums, dims):
        query = prep_data(m, d)
        query_set.append(query)
    for n, d in itertools.product(d_nums, dims):
        data = prep_data(n, d)
        data_set.append(data)
        
    # run benchmark
    with open('benchmark.csv', 'a') as f:
        header = 'alg, num_query, num_data, topn, const_time, query_time\n'
        f.write(header)
        
        for alg, query, data, topn in itertools.product(algs, query_set, data_set, topn_nums):
            res = run(query, data, alg, topn)
            f.write(res)
