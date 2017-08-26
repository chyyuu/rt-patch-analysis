#!usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict
import networkx as nx
import pickle

G = nx.DiGraph()
callee2caller = defaultdict(set)
caller2callee = defaultdict(set)

regex = re.compile(r'(?P<caller>.+)\s->\s(?P<callee>.+)')
# regex = re.compile(r'"(?P<caller>.+)"\s->\s"(?P<callee>.+)"')

with open('callgraph.txt', 'r') as f:
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

G.remove_node('_raw_spin_lock_irqsave')
G.remove_node('_raw_spin_unlock_irqrestore')
# G.remove_node('__warn')
G.remove_node('panic')
G.remove_node('printk')
G.remove_node('printk_deferred')
G.remove_node('vprintk_emit')
G.remove_node('seq_printf')
G.remove_node('do_trace_read_msr')
G.remove_node('debug_show_all_locks')
G.remove_node('debug_smp_processor_id')

pickle.dump(G, open('graph.pkl', 'wb'))
pickle.dump(sleepable, open('sleepable.pkl', 'wb'))
pickle.dump(callee2caller, open('callee2caller.pkl', 'wb'))
pickle.dump(caller2callee, open('caller2callee.pkl', 'wb'))
