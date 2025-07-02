#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#

import functools as ft
import random
import re
import sys
import typing as ty

import cards as C


class Deck():
    _unshuffled_deck = [C.Card(card, suit)
                          for card in range(*C.Card.card_range())
                            for suit in C.Card.Suits ]

    def random_shuffle() -> ty.Iterable[C.Card]:
        d = list(Deck._unshuffled_deck)
        random.shuffle(d)
        yield from d

    def __init__(self, genit: ty.Iterable[C.Card]=random_shuffle):
        '''
        Args:
            genit: a function that returns the cards in a predetermined order
        '''
        self._deck = list(genit())

    #def flip_card(self) -> C.Card:
    #    return self._deck.pop()

    def deal_cards(self, num_cards:int=0) -> [C.Card]:
        if num_cards == 0: # deal the remaining cards
            num_cards = len(self._deck)
        return [self._deck.pop() for x in range(0, num_cards)]

    def __str__(self) -> str:
        cardsstr = ', '.join([str(c) for c in self._deck])
        return f'{str(len(self._deck))}: {cardsstr}'
        

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Test deck')
    parser.add_argument('--seed', '-s',
                        type=int,
                        default=0,
                        help='set seed %(default)s')
    args = parser.parse_args()

    deck = Deck()

    print(f'deck({args.seed}: {deck}')
    cols = list(range(1, 8))
    cols.append(0)
    for col in cols:
        column = deck.deal_cards(col)
        print(f'column{col}:', end=' ')
        col_str = C.cards_to_str(column)
        print(col_str)

