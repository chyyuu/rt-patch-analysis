#!usr/bin/env python
# -*- coding: utf-8 -*-

import re

history_regex = re.compile(r'\[\[file:(?P<file>.+)\]\[.+\]\]')
module_regex = re.compile(r'Index.+?/(?P<module>.+)/.+')
backup_regex = re.compile(r'\+\+\+.+?/(?P<module>.+)/.+')

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

def scanfile(history, output):
	with open(output, 'w') as f:
		for line in open(history):
			match = history_regex.search(line)
			if match is None:
				f.write(line)
			else:
				filename = match.group('file')
				modules = analyse(filename)
				f.write(line[:-1] + ' {MOD::' + ','.join(modules) + '}\n')

if __name__ == '__main__':
	scanfile('history.org', 'history-with-modules.org')
