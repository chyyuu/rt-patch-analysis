#!usr/bin/python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict


def count(file):
	# incorrect function for demonstration purpose
    num = 0
    for line in open(file, 'r'):
        if line.startswith('+') or line.startswith('-'):
            num += 1
    return num

statistics = defaultdict(list)

with open('history.org', 'r') as f:
    data = f.read()

pattern = re.compile(
    r'\*.*C::(?P<aspect>\w+)::.*\n.*:(?P<file>.*)\]\[', re.MULTILINE)

for match in pattern.finditer(data):
    aspect = match.group('aspect')
    file = match.group('file')
    # print('{} : {}'.format(aspect, file))
    statistics[aspect].append(count(file))

for k, v in statistics.items():
    print('{}: {}'.format(k, v))
