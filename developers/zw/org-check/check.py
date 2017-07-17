#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import re


class Checker(object):

    def __init__(self):
        super(Checker, self).__init__()

    def check(self, description):
        line = description.split('::')
        if line[0] is not 'C':
            print('Characteristic should start with "C"')
            return False

        aspect = line[1]
        detail = line[1:]
        if aspect == 'feature':
            return self.feature(detail)
        elif aspect == 'fixbug':
            return self.fixbug(detail)
        elif aspect == 'performance':
            return self.performance(detail)
        elif aspect == 'maintain':
            return self.maintain(detail)
        else:
            print('Unknown aspect "{}"'.format(aspect))
            return False

    def feature(self, detail):
        return len(detail) > 0 and len(detail[0]) > 0

    def fixbug(self, detail):
        if len(detail) == 4:
            return True
        print("FIXBUG ::= 'fixbug'::BUG_CONSEQUENCE::BUG_TYPE::FIX_METHOD::DESCRIPT")
        return False

    def performance(self, detail):
        if len(detail) == 2:
            return True
        print("PERFORMANCE ::= 'performance'::PERF_METHOD::DESCRIPT")
        return False

    def maintain(self, detail):
        if len(detail) == 1:
            return True
        print("MAINTAIN ::='maintain'::MAINTAIN_METHOD")
        return False


def main():
    checker = Checker()
    pattern = re.compile(r'\*.*{(.*?)}')
    with open(sys.argv[1], 'r') as f:
        data = f.read()
    for match in pattern.finditer(data):
        description = match.group(1)
        if checker.check(description) is False:
            print(match.group(0))
            print('\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('./check.py <file>')
    else:
        main()
