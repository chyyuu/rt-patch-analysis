#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pyorg import PyOrg


class HistoryOrg(PyOrg):
    """Parse, edit and save history.org files."""

    class Node(PyOrg.Node):
        """A node in the history.org file."""

        def __init__(self):
            PyOrg.Node.__init__(self)  # PyOrg.Node is an old-style class
            self.character = None

        def load(self, lines):
            first_line = lines[0]
            if not self.__is_title_line(first_line):
                return

            # load the title
            i = self.__title_level(first_line)
            j = self.__title_tags(first_line)
            self.level = i

            title = first_line.split(' {')  # use patch name as title
            self.title = title[0].strip()
            if len(title) > 1:
                self.character = title[-1][:-1]

            lines.pop(0)

            # load contents if any
            while lines and not self.__is_title_line(lines[0]):
                self.contents.append(lines.pop(0)[self.level:])

            # load sub-nodes if any
            while lines and self.__is_title_line(lines[0]) and self.__title_level(lines[0]) > self.level:
                b = PyOrg.Node()
                b.load(lines)
                self.subnodes[b.title] = b
                self.subnode_order.append(b.title)

            return self

        def __str__(self):
            out = ''

            out += self.title
            if self.character is not None:
                out += ' {%s}' % (self.character)

            if self.tags:
                tag_part = ':%s:' % ':'.join(self.tags)
                content_len = self.level + len(self.title) + len(tag_part)
                space_len = 1 if content_len >= 77 else (77 - content_len)
                out += ' ' * space_len
                out += tag_part
            out += '\n'
            for line in self.contents:
                out += '%s%s\n' % (' ' * self.level, line)
            for title in self.subnode_order:
                out += self.subnodes[title].__str__()
            return out


def main():
    orgs = []
    for file in sys.argv[1:]:
        org = HistoryOrg()
        org.load(file)
        orgs.append(org)

    for key, val in orgs[0].nodes.items():
        files = []
        for org, file in zip(orgs[1:], sys.argv[2:]):
            nodes = org.nodes
            if key in nodes:
                if val.character is None:
                    val.character = nodes[key].character
                    continue
                elif nodes[key].character is None:
                    continue
                elif nodes[key].character == val.character:
                    continue

            files.append(file)

        if len(files) > 0:
            print('{} @ {}'.format(val.title, files))

    orgs[0].save()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('./merge.py <file>...')
    else:
        main()
