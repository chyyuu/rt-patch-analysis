#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from os import listdir, path
from collections import defaultdict
import re

versions = [
    '2.6.22', '2.6.23', '2.6.24', '2.6.25', '2.6.26', '2.6.29',
    '3.0', '3.2', '3.4', '3.6', '3.8', '3.10', '3.12', '3.14', '3.18',
    '4.0', '4.1', '4.4', '4.6', '4.8', '4.9', '4.11'
]

module_regex = re.compile(r'Index.+?/(?P<module>.+)')
backup_regex = re.compile(r'\+\+\+.+?/(?P<module>.+?)[ \t\n]')


def analyse(filename):
    with open(filename, 'r') as f:
        content = f.read()
    modules = set()

    for match in module_regex.finditer(content):
        module = match.group('module')
        modules.add(module)

    # use different regex to avoid missing anything
    for match in backup_regex.finditer(content):
        module = match.group('module')
        modules.add(module)

    return modules


def patch_frequency():
    occurrence = defaultdict(int)
    title = None
    for line in open('history.org', 'r'):
        if line.startswith('*'):
            title = line
        elif line.startswith('  -'):
            pass
        else:
            occurrence[title] += 1

    index = defaultdict(int)
    for k, v in occurrence.items():
        index[v] += 1
    print('Patch Frequency:')
    for k, v in index.items():
        print('{},{}'.format(k, v))


def patch_uniqueness():
    patches = {ver: set([f for f in listdir(ver) if f.endswith('patch')])
               for ver in versions}

    print('Patch Uniqueness:')
    for i in range(len(versions)):
        patch = set(patches[versions[i]])
        for j in range(len(versions)):
            if i != j:
                patch -= patches[versions[j]]
        print('{},{}'.format(versions[i], len(patch)))

    print('New Patch Frequency:')
    for i in range(len(versions)):
        patch = set(patches[versions[i]])
        for j in range(i):
            patch -= patches[versions[j]]
        print('{},{}'.format(versions[i], len(patch)))


def component_distribution():
    files = set()
    for ver in versions:
        for patch in listdir(ver):
            if patch.endswith('patch'):
                files |= analyse(path.join(ver, patch))
    index = defaultdict(int)
    for file in files:
        module = file.split('/')[0]
        index[module] += 1
    print('Component Distribution:')
    for k, v in index.items():
        print('{},{}'.format(k, v))

if __name__ == '__main__':
    patch_frequency()
    patch_uniqueness()
    component_distribution()
