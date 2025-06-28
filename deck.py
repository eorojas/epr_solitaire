#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#
import argparse
import functools as ft
import random
import re
import sys
import typing as ty

import cards


BREAK_STRING \
    = '\n-------------------------------------------------------------------'

class Deck():
    unshuffled_deck = [cards.Card(card, suit)
                        for card in range(*cards.Card._range)
                            for suit in range(1, 4)
                      ]

    def __init__(self, seed=0):
        # TODO set the seed to duplicate shuffle
        self._deck = self.unshuffled_deck
        random.shuffle(self._deck)

    def Flip_card(self):
        return self.deck.pop()

    def deal_cards(self):
        num_cards = len(self._deck)
        return [self.deck.pop() for x in range(0, num_cards)]

    def __str__(self) -> str:
        cardsstr = ', '.join([str(c) for c in self._deck])
        return f'{str(len(self._deck))}: {cardsstr}'
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test deck')
    parser.add_argument('--seed', '-s',
                        type=int,
                        default=0,
                        help='set seed %(default)s')
    args = parser.parse_args()

    deck = Deck(args.seed)

    print(f'deck({args.seed}: {deck}')

