import sys, os
import re

class PyOrg:

    """Parse, edit and save Emacs org files.

    An org file consists of a (recursive) list of nodes. Each node in the file
    starts with one or more stars (*), followed by the title and some tags in
    the same line and the text body in the next few lines.

    Note that we assume nodes in the same scope have unique titles.

    self.nodes : string -> Node
        a dict mapping titles to top-level nodes

    self.node_order : string list
        a list of titles that memorizes the order of the top-level nodes

    self.filep : string
        the path of the file from which this document is loaded from

    self.comments : string list
        the comments at the beginning of the file which may specify todo list,
        etc.

    """

    class Node:

        """A node in the org file.

        self.level : int
            the level of this node (i.e. the number of stars at the beginning)

        self.title : string
            the title (string)

        self.tags : string list
            a list of tags

        self.contents : string list
            the text body as a list of lines. The trailing newline is stripped.

        self.subnodes : string -> Node
            a dict mapping titles to Nodes

        self.subnode_order : string list
            a list of titles that memorizes the order of the subnodes
        """

        tags_pattern = re.compile('.*[^\s](\s+(:\w+)+:\s?)$')

        def __is_title_line(self, line):
            return line[0] == '*'

        def __title_level(self, line):
            i = 0
            while line[i] == '*':
                i += 1
            return i

        def __title_tags(self, line):
            m = self.tags_pattern.match(line)
            if not m:
                return len(line)

            tag_part = m.group(1)
            self.tags = [t for t in tag_part.strip().split(':') if t]

            return len(line) - len(tag_part)

        def __init__(self):
            self.level = 0
            self.title = ""
            self.tags = []
            self.contents = []
            self.subnodes = {}
            self.subnode_order = []

        def load(self, lines):
            first_line = lines[0]
            if not self.__is_title_line(first_line):
                return

            # load the title
            i = self.__title_level(first_line)
            j = self.__title_tags(first_line)
            self.level = i
            self.title = first_line[i:j]
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

        def create(self, title):
            b = PyOrg.Node();
            b.level = self.level + 1
            b.title = title
            self.subnodes[title] = b
            self.subnode_order.append(title)

            return b

        def sort(self):
            self.subnode_order = sorted(self.subnode_order)
            for b in self.subnodes.values():
                b.sort()
            return self

        def __str__(self):
            out = ''

            out += '%s%s' % ('*' * self.level, self.title)
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

    def __init__(self):
        self.nodes = {}  # str -> Node
        self.node_order = []
        self.filep = ''
        self.comments = []

    def load(self, filep):
        """Load a document from file

        :param filep: path of the file

        """
        f = open(filep, 'r')
        self.filep = filep
        lines = map(lambda x: x.strip('\n'), f.readlines())
        while lines[0].startswith('#'):
            self.comments.append(lines.pop(0))
        while lines:
            b = self.Node()
            b.load(lines)
            self.nodes[b.title] = b
            self.node_order.append(b.title)
        f.close()
        return self

    def save(self, filep = ''):
        """Save the document

        :param filep: path where this file should be saved. When not given, the
        file where this document is loaded from will be overwritten.

        """
        if filep == '':
            filep = self.filep
        if filep != '':
            f = open(filep, 'w')
            f.write(self.__str__())
            f.close()

    def create(self, title):
        """Create a fresh top-level node at the end of the file

        :param title: the title of the new node

        """
        b = PyOrg.Node();
        b.level = 1
        b.title = title
        self.nodes[title] = b
        self.node_order.append(title)

        return b

    def move(self, node, parent_old, parent_new):
        """Move a node

        :param node: the Node to be moved

        :param parent_old: the current parent of the node

        :param parent_new: the new parent of the node

        """
        title = node.title
        if title in parent_old.subnodes.keys() and title not in parent_new.subnodes.keys():
            parent_new.subnodes[title] = node
            parent_new.subnode_order.append(title)
            del parent_old.subnodes[title]
            parent_old.subnode_order.remove(title)

    def sort(self, key = None):
        """Sort the nodes in each scope

        :param key: a optional function mapping titles to any comparable
        structures which are used as keys during the sorting. When not given,
        the title itself is used.

        """

        if key:
            self.node_order = sorted(self.node_order, key = key)
        else:
            self.node_order = sorted(self.node_order)
        for b in self.nodes.values():
            b.sort()
        return self

    def __str__(self):
        out = ''
        for comment in self.comments:
            out += comment + '\n'
        for title in self.node_order:
            out += self.nodes[title].__str__()
        return out

if __name__ == '__main__':
    org = PyOrg()
    p = os.path.dirname(sys.argv[0])
    org.load(os.path.join(p, '.pyorg_test.org'))
    sys.stdout.write(org.sort().__str__())
    org.save()
