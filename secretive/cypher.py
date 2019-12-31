#! /usr/bin/env python3

import inspect
from random import choice, randint, sample
from string import digits


class Cypher:

    def get_available_cyphers(self):
        """Select random cyphers"""
        return [i for i in inspect.getmembers(self, predicate=inspect.isroutine) if i[0].startswith('to_')]

    def sample_cyphers(self, count=None):
        available_cyphers = self.get_available_cyphers()
        if count is None:
            end = len(available_cyphers)
            count = randint(1, end)

        return sample(available_cyphers, count)

    def to_int(self, char):
        """Convert character to integer

        :param str char: Character
        :return: Cyphered character
        :rtype: str
        """
        store = {
            'a': [4],
            'b': [13, 3],
            'c': [6],
            'd': [9],
            'e': [3, 6, 9],
            'f': [5],
            'g': [9],
            'i': [1],
            'j': [1],
            'l': [1],
            'o': [0],
            's': [5],
            't': [7],
            'z': [2]
        }
        char = char.lower()
        options = [char.swapcase(), char]
        if char in store.keys():
            options += store[char]

        if char.isdigit():
            options += [digits[-int(char)]]

        return choice(options)

    def to_punctuation(self, char):
        """Convert character to special character

        :param str char: Character
        :return: Cyphered character
        :rtype: str
        """
        store = {
            'h': ['#'],
            'a': ['@'],
            'e': ['£'],
            '0': ['()'],
            'u': ['#'],
            'i': ['!', ':'],
            'j': ['!', ';'],
            '8': ['&', '%'],
            '7': ['?'],
            '.': [','],
            'q': ['&'],
            'x': ['&'],
            'k': ['£'],
        }
        char = char.lower()
        options = [char.swapcase(), char]
        if char in store.keys():
            options += store[char]

        return choice(options)
