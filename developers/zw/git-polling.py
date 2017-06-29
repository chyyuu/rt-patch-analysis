#! usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import subprocess

# SCRIPT : the script to execute
SCRIPT = 'rt-linux-lkp.sh'
# URL : git repository url
URL = 'https://github.com/chyyuu/linux-rt-devel.git'
# TIME : time to sleep
TIME = 60


def ls_remote(url):
    ret = subprocess.check_output(['git', 'ls-remote', '-q', '-h', url])
    return ret.strip().split('\n')


def build_record():
    record = {}
    for line in ls_remote(URL):
        sha, branch = line.split('\t')
        record[branch[11:-1]] = sha  # [11:-1] is the range of branch name
    return record


def main_loop():
    record = build_record()
    while True:
        for line in ls_remote(URL):
            sha, branch = line.split('\t')
            if record[branch[11:-1]] != sha:
                record[branch[11:-1]] = sha
                subprocess.call(["sh", SCRIPT, URL, sha])
        time.sleep(TIME)

if __name__ == '__main__':
    main_loop()
