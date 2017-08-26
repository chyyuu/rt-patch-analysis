#!usr/bin/env python
# -*- coding: utf-8 -*-

import gcc
import gccutils


class CheckingPass(gcc.GimplePass):

    def __init__(self, name):
        super(CheckingPass, self).__init__(name)
        self.log = open('callgraph.txt', 'a')

    # This is called per-function during compilation:
    def execute(self, func):
        caller = func.decl.name
        callees = set()
        for basic_block in func.cfg.basic_blocks:
            for stmt in basic_block.gimple:
                if isinstance(stmt, gcc.GimpleCall):
                    callees.add(str(stmt.fn))
        for callee in callees:
            self.log.write('{} -> {}\n'.format(caller, callee))

# Wire up our callback:
ps = CheckingPass(name='BuildCallGraph')
ps.register_after('cfg')
