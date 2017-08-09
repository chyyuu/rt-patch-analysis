#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import Counter
import sys
import re


class Checker(object):

    versions = ['2.6.22', '2.6.23', '2.6.24', '2.6.25', '2.6.26', '2.6.29', '3.0', '3.2',
               '3.4', '3.6', '3.8', '3.10', '3.12', '3.14', '3.18', '4.0', '4.1', '4.4',
               '4.6', '4.8', '4.9', '4.11']

    lists = [[] for i in range(22)]
    buglist = [[] for i in range(22)]
    featurelist = [[] for i in range(22)]
    performancelist = [[] for i in range(22)]
    bugs = [[0 for i in range(4)]for i in range(22)]
    stc = [{} for i in range(22)]

    feature_method = {'hardware', 'debuginfo', 'idle', 'hrtimer', 'statistics',
                      'delay', 'sched', 'mm', 'timer', 'lockless', 'capability',
                      'net', 'power', 'rtsupport', 'check', 'arch','testcase',  
                      'hotplug', 'other'}

    fix_method = {'hardware', 'mutex', 'sync', 'order', 'irq', 'softirq',
                  'preempt', 'migration', 'idle', 'memory', 'config', 'sched', 
                  'syntax', 'runtime', 'semantics'}

    bug_consequence = {'hwerr', 'corrupt', 'hang', 'deadlock', 'livelock', 'crash',
                       'leak', 'data_err', 'ctrl_err', 'irq', 'softirq', 'compile', 'idle',
                       'rtlatency', 'na', '??'}

    performance_method = {'hardware', 'cache', 'msleep', 'irq', 'softirq',
                          'mutex', 'preempt', 'barrier', 'idle', 'hrtimer',
                          'mm', 'percpu_var', 'smallsize', 'migration','config'}

    maintain_method = {'refactor', 'donothing'}

    semantic = {'hardware', 'softirq', 'migration', 'preempt',
                'time', 'irq', 'sched', 'semantics', 'na'}

    concurrency = {'atomicity', 'order', 'deadlock', 'livelock'}

    memory = {'resource_leak', 'uninit_var', 'typo_var',
              'overflow', 'err_var', 'err_access'}

    error_code = {'compiling_err', 'config_err'}

    bug_type = [semantic, concurrency, memory, error_code]

    def __init__(self):
        super(Checker, self).__init__()

    def check(self,version, description):
	idx = self.versions.index(version)
        line = description.split('::')

        aspect = line[1]
        detail = line[2:]
        self.lists[idx].append(aspect)

        if aspect == 'bug':
            self.bug(idx, detail)

        if aspect == 'feature':
            self.feature(idx, detail)

        if aspect == 'performance':
            self.performance(idx, detail)

    def cnt(self):
        for idx, list in enumerate(self.lists):
	    self.stc[idx] = dict(Counter(list))
        print(self.stc)

        for idx, list in enumerate(self.buglist):
	    self.stc[idx] = dict(Counter(list))
            bug = sorted(self.stc[idx].items(), key=lambda d:d[1], reverse=True)
            other = 0
            
            for (a,b) in bug[:4:-1]:
                other += b
                bug.pop()

            bug.append(('other', other))
            
            print(bug)

        for idx, list in enumerate(self.featurelist):
	    self.stc[idx] = dict(Counter(list))
            feature = sorted(self.stc[idx].items(), key=lambda d:d[1], reverse=True)
            other = 0
            
            for (a,b) in feature[:4:-1]:
                other += b
                feature.pop()

            feature.append(('other', other))
            
            print(feature)

        for idx, list in enumerate(self.performancelist):
	    self.stc[idx] = dict(Counter(list))
            performance = sorted(self.stc[idx].items(), key=lambda d:d[1], reverse=True)
            other = 0
            
            for (a,b) in performance[:4:-1]:
                other += b
                performance.pop()

            performance.append(('other', other))
            
            print(performance)
        

    def bug(self, version, detail):
        self.buglist[version].append(detail[1])    

        for idx, list in enumerate(self.bug_type):
            if detail[1] in list:
                self.bugs[version][idx] += 1
                return

    def feature(self, version, detail):
        self.featurelist[version].append(detail[0])

    def performance(self, version, detail):
        self.performancelist[version].append(detail[0])

def main():
    checker = Checker()
    pattern = re.compile(r'\*.\[\s*(\d+\.\d+\.\d+|\d+\.\d+).*\].*{(.*?)}')
    with open(sys.argv[1], 'r') as f:
        data = f.read()
    for match in pattern.finditer(data):
	version = match.group(1)
        description = match.group(2)
        checker.check(version, description)

    checker.cnt();
    print(checker.bugs)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('./check.py <file>')
    else:
        main()
