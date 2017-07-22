#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import re


class Checker(object):

    feature_method = {'hardware', 'debuginfo', 'idle', 'hrtimer', 'statistics',
                      'delay', 'sched', 'mm', 'timer', 'lockless', 'capability',
                      'net', 'rtsupport', 'check', 'arch', 'other'}

    fix_method = {'hardware', 'mutex', 'sync', 'order', 'irq', 'softirq',
                  'preempt', 'migration', 'idle', 'memory', 'config',
                  'syntax', 'runtime', 'semantics'}

    bug_consequence = {'hwerr', 'corrupt', 'hang', 'deadlock', 'livelock', 'crash',
                       'leak', 'data_err', 'irq', 'softirq', 'compile', 'idle',
                       'na', '??'}

    performance_method = {'hardware', 'cache', 'msleep', 'irq', 'softirq',
                          'mutex', 'preempt', 'barrier', 'idle', 'hrtimer',
                          'mm', 'percpu_var', 'smallsize'}

    maintain_method = {'refactor', 'donothing'}

    semantic = {'hardware', 'softirq', 'migration', 'preempt',
                'time', 'irq', 'semantics', 'na'}

    concurrency = {'atomicity', 'order', 'deadlock', 'livelock'}

    memory = {'resource_leak', 'uninit_var', 'typo_var',
              'overflow', 'err_var', 'err_access'}

    error_code = {'compiling_err', 'config_err'}

    bug_type = semantic | concurrency | memory | error_code

    def __init__(self):
        super(Checker, self).__init__()

    def check(self, description):
        line = description.split('::')
        if line[0] is not 'C':
            return False

        aspect = line[1]
        detail = line[2:]
        if aspect == 'feature':
            return self.feature(detail)
        elif aspect == 'bug':
            return self.bug(detail)
        elif aspect == 'performance':
            return self.performance(detail)
        elif aspect == 'maintain':
            return self.maintain(detail)
        else:
            print('Unknown aspect "{}"'.format(aspect))
            return False

    def feature(self, detail):
        if len(detail) != 1 and len(detail) != 2:
            print("FEATURE ::= 'feature'::FEATURE_METHOD::DESCRIPT")
            return False

        if not detail[0] in self.feature_method:
            print('Unknown feature method "{}"'.format(detail[0]))
            return False

        return True

    def bug(self, detail):
        if len(detail) != 3 and len(detail) != 4:
            print("BUG ::= 'bug'::BUG_CONSEQUENCE::BUG_TYPE::FIX_METHOD::DESCRIPT")
            return False

        if not detail[0] in self.bug_consequence:
            print('Unknown bug consequence "{}"'.format(detail[0]))
            return False

        if not detail[1] in self.bug_type:
            print('Unknown bug type "{}"'.format(detail[1]))
            return False

        if not detail[2] in self.fix_method:
            print('Unknown fix method "{}"'.format(detail[2]))
            return False

        return True

    def performance(self, detail):
        if len(detail) != 1 and len(detail) != 2:
            print("PERFORMANCE ::= 'performance'::PERF_METHOD::DESCRIPT")
            return False

        if not detail[0] in self.performance_method:
            print('Unknown performance method "{}"'.format(detail[0]))
            return False

        return True

    def maintain(self, detail):
        if len(detail) != 1 and len(detail) != 2:
            print("MAINTAIN ::= 'maintain'::MAINTAIN_METHOD")
            return False

        if not detail[0] in self.maintain_method:
            print('Unknown maintain method "{}"'.format(detail[0]))
            return False

        return True


def main():
    checker = Checker()
    pattern = re.compile(r'\*.*{(.*?)}')
    with open(sys.argv[1], 'r') as f:
        data = f.read()
    for match in pattern.finditer(data):
        description = match.group(1)
        if checker.check(description) is False:
            print(match.group(0), end='\n\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('./check.py <file>')
    else:
        main()
