#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import networkx as nx

G = nx.DiGraph()
callee2caller = defaultdict(set)
caller2callee = defaultdict(set)

regex = re.compile(r'"(?P<caller>\w+)"\s->\s"(?P<callee>\w+)"')

with open('callgraph.dot', 'r') as f:
    data = f.read()

for match in regex.finditer(data):
    caller = match.group('caller')
    callee = match.group('callee')
    G.add_edge(caller, callee)
    callee2caller[callee].add(caller)
    caller2callee[caller].add(callee)

print(nx.info(G))

size = 0
sleepable = set(callee2caller['___might_sleep'])

while len(sleepable) > size:
    size = len(sleepable)

    difference = set()
    for callee in sleepable:
        difference |= callee2caller[callee]

    sleepable |= difference

for func in callee2caller['_raw_spin_lock_irqsave']:
    routines = set(caller2callee[func] & sleepable)
    routines.discard('_raw_spin_lock_irqsave')
    routines.discard('_raw_spin_unlock_irqrestore')
    for routine in routines:
        print('{} -> {}'.format(func, ' -> '.join(nx.shortest_path(G, routine, '___might_sleep'))))
