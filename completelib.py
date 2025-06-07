import os
import readline
import re
import subprocess
"""
Complib
This module provides a very basic command line completion library for Python.
GPLv3
email: maru@lithium-dev.xyz (pgp attached)
signal: maru.222
BTC: 16innLYQtz123HTwNLY3vScPmEVP7tob8u
ETH: 0x48994D78B7090367Aa20FD5470baDceec42cAF62 
XMR: 49dNpgP5QSpPDF1YUVuU3ST2tUWng32m8crGQ4NuM6U44CG1ennTvESWbwK6epkfJ6LuAKYjSDKqKNtbtJnU71gi6GrF4Wh
"""


#trie structure is actually insanely good
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        
class CommandTrie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def find_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._get_all_words(node, prefix)
    
    def _get_all_words(self, node, prefix):
        words = []
        if node.is_end:
            words.append(prefix)
        for char, child in node.children.items():
            words.extend(self._get_all_words(child, prefix + char))
        return words

def get_shell_commands():
    try:
        result = subprocess.run(['bash', '-c', 'compgen -c'], stdout=subprocess.PIPE, text=True)
        commands = result.stdout.splitlines()
        return commands
    except Exception as e:
        print(f"Error fetching shell commands: {e}")
        return []
def compile(command_list):
    global commands
    commands = command_list
    comp = Completer()
    comp.initialize_commands(command_list)
    readline.set_completer_delims('\t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(comp.complete)
    return commands
RE_SPACE = re.compile('.*\\s+$', re.M)

class Completer(object):
    def __init__(self):
        self.command_trie = CommandTrie()
        
    def initialize_commands(self, commands):
        for cmd in commands:
            self.command_trie.insert(cmd)
    def _listdir(self, root):
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _listdir_insensitive(self, root, partial=''):
        res = []
        try:
            items = os.listdir(root)
            partial = partial.lower()
            for name in items:
                if name.lower().startswith(partial):
                    path = os.path.join(root, name)
                    if os.path.isdir(path):
                        name += os.sep
                    res.append(name)
        except OSError:
            return []
        return res

    def _complete_path(self, path=None):
        """Perform completion of filesystem path."""
        if not path:
            return self._listdir('.')
        
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        
        # Use case-insensitive matching
        res = [os.path.join(dirname, p)
               for p in self._listdir_insensitive(tmp, rest)]
        
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + '']

    def complete_extra(self, args):
        if not args:
            # Complete from the current directory if no arguments are provided
            return self._complete_path('.')
        # Treat the last argument as a path and complete it
        return self._complete_path(args[-1])

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        line = buffer.split()
        
        # Show all commands if no input
        if not line:
            matches = commands
            return matches[state] if state < len(matches) else None

        cmd = line[0].strip()
        if len(line) == 1:
            matches = self.command_trie.find_prefix(cmd)
            if not matches:
                matches = self._complete_path(text)
        else:
            partial_path = line[-1]
            matches = self._complete_path(partial_path)
            matches = [buffer[:buffer.rfind(partial_path)] + match for match in matches]

        return matches[state] if state < len(matches) else None
