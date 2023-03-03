#!/usr/bin/env python3

import sys

def player_for_word(word):
    return (len(word) % 2) + 1

def other_player(player):
    return 1 if player == 2 else 2

class GhostTrieNode:
    def __init__(self, word, parent):
        self.word = word
        self.parent = parent
        self.continuations = {}
        self.valid_word = False
        self.winner = 0

    def add_word_to_trie(self, word):
        assert(word[:len(self.word)] == self.word)

        if self.valid_word:
            return
        if self.word == word:
            self.continuations.clear()
            self.valid_word = True
            return

        next_char = word[len(self.word)]
        if next_char in self.continuations:
            self.continuations[next_char].add_word_to_trie(word)
        else:
            new_node = GhostTrieNode(word[:len(self.word) + 1], self)
            self.continuations[next_char] = new_node
            new_node.add_word_to_trie(word)

    def establish_winners(self):
        cur_player = player_for_word(self.word)

        if self.valid_word:
            self.winner = cur_player
            return

        is_winner = False
        for node in self.continuations.values():
            node.establish_winners()
            if node.winner == cur_player:
                is_winner = True

        if is_winner:
            self.winner = cur_player
        else:
            self.winner = other_player(cur_player)

def build_ghost_trie(words):
    root_node = GhostTrieNode('', None)
    for word in words:
        root_node.add_word_to_trie(word)
    root_node.establish_winners()
    return root_node

def make_trie_graph(trie):
    graph = ['digraph {']
    graph.append('node [style=filled]')
    player_1_wins = []
    player_2_wins = []

    def escape_word(word):
        if word == '':
            return '" "'
        else:
            return f'"{word}"'

    def visitor(node):
        if node.winner == 1:
            player_1_wins.append(escape_word(node.word))
        else:
            player_2_wins.append(escape_word(node.word))

        for continuation in node.continuations.values():
            graph.append(f'{escape_word(node.word)} -> {escape_word(continuation.word)}')
            visitor(continuation)

    visitor(trie)

    graph.append(', '.join(player_1_wins))
    graph.append('[fillcolor="#aaaaff"]')
    graph.append(', '.join(player_2_wins))
    graph.append('[fillcolor="#ffaaaa"]')
    graph.append('}')

    return '\n'.join(graph)

if __name__ == '__main__':
    words = sys.stdin.read().split()
    words = [word for word in words if len(word) >= 3]
    trie = build_ghost_trie(words)
    print(make_trie_graph(trie))
