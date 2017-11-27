#!/usr/bin/env python
# -*- coding: utf-8 -*-

import annoy

def construct_index(data, num_trees=10):
    dim = len(data[0])
    n = len(data)
    index = annoy.AnnoyIndex(dim)
    for i in range(n):
        index.add_item(i, data[i])
    index.build(num_trees)
    return index

def search(queries, index, topn=10):
    for q in queries:
        index.get_nns_by_vector(q, topn)
    
