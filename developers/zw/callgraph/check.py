#!usr/bin/env python
# -*- coding: utf-8 -*-

import gcc
import gccutils
import re
import networkx as nx
from collections import defaultdict

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

size = 0
sleepable = set(callee2caller['___might_sleep'])
critical = set(callee2caller['_raw_spin_lock_irqsave'])

while len(sleepable) > size:
    size = len(sleepable)

    difference = set()
    for callee in sleepable:
        difference |= callee2caller[callee]

    sleepable |= difference

log = open('log.txt', 'w')


class CheckingPass(gcc.GimplePass):

    def execute(self, func):
        # This is called per-function during compilation:
        if not func.decl.name in critical:
            return

        for bb in func.cfg.basic_blocks:
            if bb.gimple:
                for stmt in bb.gimple:
                    if isinstance(stmt, gcc.GimpleCall):
                        name = str(stmt).split(' (')[0]
                        if name in sleepable:
                            shortest_path = nx.shortest_path(
                                G, name, '___might_sleep')
                            log.write('{}:{}\n'.format(
                                stmt.loc, ' -> '.join(shortest_path)))

    def check(self, node, loc):
        if isinstance(node, gcc.GimpleCall):
            raise Exception(node)

# Wire up our callback:
ps = CheckingPass(name='sleepatomic')
ps.register_after('cfg')
