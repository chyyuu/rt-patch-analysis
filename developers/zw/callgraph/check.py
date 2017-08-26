#!usr/bin/env python
# -*- coding: utf-8 -*-

import gcc
import pickle
import gccutils
import networkx as nx
from re import finditer
from collections import defaultdict, deque


class CheckingPass(gcc.GimplePass):

    def __init__(self, name):
        super(CheckingPass, self).__init__(name)
        self.log = open('log.txt', 'a')
        self.graph = pickle.load(open('graph.pkl', 'rb'))
        self.sleepable = pickle.load(open('sleepable.pkl', 'rb'))
        self.callee2caller = pickle.load(open('callee2caller.pkl', 'rb'))
        self.lock = '_raw_spin_lock_irqsave'
        # self.lock = 'arch_local_irq_disable'
        # self.lock = '__preempt_count_add'
        self.unlock = '_raw_spin_unlock_irqrestore'
        # self.unlock = 'arch_local_irq_enable'
        # self.unlock = '__preempt_count_sub'
        self.global_count = 0

    # This is called per-function during compilation:
    def execute(self, func):
        if not func.decl.name in self.callee2caller[self.lock]:
            return
        self.dfs(func.cfg.entry, set())

    def dfs(self, block, visited):
        visited.add(block)

        count = 0
        for stmt in block.gimple:
            if isinstance(stmt, gcc.GimpleCall):
                name = str(stmt.fn)
                if name == self.lock:
                    count += 1
                    self.global_count += 1
                elif name == self.unlock:
                    count -= 1
                    self.global_count -= 1
                elif self.global_count > 0 and name in self.sleepable:
                    try:
                        self.log.write('{}:{}\n'.format(stmt.loc, nx.all_shortest_path(self.graph, name, '___might_sleep')))
                    except Exception as e:
                        # self.log.write(str(e))
                        pass

        for edge in block.succs:
            if not edge.dest in visited:
                self.dfs(edge.dest, visited)

        self.global_count -= count

        visited.remove(block)

# Wire up our callback:
ps = CheckingPass(name='SleepInAtomic')
ps.register_after('cfg')
