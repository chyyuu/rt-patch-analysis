#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
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


def first_diff(li1, li2):
    for i, (el1, el2) in enumerate(zip(li1, li2)):
        if el1 != el2:
            return i, el1, el2
    return sys.maxsize, '', ''


def main():
    orgs = []
    for file in sys.argv[1:]:
        org = HistoryOrg()
        org.load(file)
        orgs.append(org)

    for key, val in orgs[0].nodes.items():
        files = []
        pos = sys.maxsize
        item1 = ""
        item2 = ""
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
                elif '::' in val.character and '::' in nodes[key].character:
                    diff_pos, diff_item1, diff_item2 = first_diff(
                        val.character.split('::'), nodes[key].character.split('::'))
                    if diff_pos < pos:
                        pos = diff_pos
                        item1 = diff_item1
                        item2 = diff_item2
                elif '??' in val.character and '??' not in nodes[key].character:
                    val.character = nodes[key].character
                    continue

            files.append(file)

        item_maxsize = 2
        if not(val.character is None):
            items = val.character.split('::')
            if len(items) > 1 and items[1] == 'fixbug':
                item_maxsize = 4

        if pos >= 0 and pos <= item_maxsize:
            print('first diff {} {}...{}'.format(pos, item1, item2), end=' ')
        if len(files) > 0:
            print('{} @ {}\n'.format(val.title, files))

    orgs[0].save()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('./merge.py <file>...')
    else:
        main()
