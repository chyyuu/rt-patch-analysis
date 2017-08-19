#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import networkx as nx

G = nx.DiGraph()
callee2caller = defaultdict(set)

regex = re.compile(r'"(?P<caller>\w+)"\s->\s"(?P<callee>\w+)"')

with open('callgraph.dot', 'r') as f:
    data = f.read()

for match in regex.finditer(data):
    caller = match.group('caller')
    callee = match.group('callee')
    G.add_edge(caller, callee)
    callee2caller[callee].add(caller)

print(nx.info(G))

for func in callee2caller['_raw_spin_lock_irqsave']:
    try:
        path = nx.shortest_path(G, func, '___might_sleep')
        print(' -> '.join(path))
    except Exception as e:
        print('{} cannot reach might_sleep'.format(func))
