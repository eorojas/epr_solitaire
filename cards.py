#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#
import argparse
import enum
import functools as ft
import random
import re
import sys
import typing as ty

import parse_sol_cmds as psc

COLOR_RED='[31;1m'
COLOR_BLUE='[34;1m'

COLOR_RED_BOLD='[31;1m'
COLOR_BLUE_BOLD='[34;1m'
COLOR_NONE='[0m'

class Suits(enum.IntEnum):
    SPADE = enum.auto()
    HEART = enum.auto()
    DIAMOND = enum.auto()
    CLUB = enum.auto()

# define min_suit and max_suit to avoid errors of the other changes.
_min_suit = min(Suits).value
_max_suit = max(Suits).value

def min_suit() -> int:
    return _min_suit

def max_suit() -> int:
    return _max_suit

ace = 1
king = 13

_card_map = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7',
               8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}

_range = {ace, king + 1} # i.e, Ace to King, or 1 to 13
def card_range():
    return _range

class Card():
    _suit_map = {
        Suits.SPADE : 'spade',
        Suits.HEART : 'heart',
        Suits.DIAMOND : 'diamod',
        Suits.CLUB : 'club',
    }

    RedSuits = {Suits.DIAMOND, Suits.HEART}
    BlackSuits = {Suits.SPADE, Suits.CLUB}
    Symbols = {Suits.SPADE:'\u2660',
               Suits.HEART:'\u2661',
               Suits.DIAMOND:'\u2662',
               Suits.CLUB:'\u2663'}

    def symbol(s : Suits) -> str:
        color = COLOR_RED if s in Card.RedSuits else COLOR_BLUE
        return f'{color}{Card.Symbols[s]}{COLOR_NONE}'

    def __init__(self, value: int, suit: Suits):
        assert (value >= ace) and (value <= king), \
                f'Bad card {value=}'
        self._name = _card_map[value]
        self._suit = suit
        self._color = COLOR_RED if suit in Card.RedSuits else COLOR_BLUE
        self._title \
            = f'{self._color}{self._name}{Card.Symbols[self._suit]}{COLOR_NONE}'
        self._value = value

    @property
    def name(self) -> str:
        return self._name

    @property
    def suit(self) -> Suits:
        return self._suit

    @property
    def color(self) -> str:
        return self._color

    @property
    def value(self) -> int:
        return self._value

    @property
    def title(self) -> str:
        return self._title

    #def below(self, card):
    #    return self._value == (card._value - 1)

    #def opposite_color(self, card):
    #    ''' 
    #    Returns:
    #        True colors are opposite, since only two colors this means that
    #        are not equal.
    #    '''
    #    return self._color != card._color
    #    #if self._suit == 'club' or self._suit == 'spade':
    #    # TODO(epr): no reason to check twice
    #    #if self._suit in Card.BlackSuits:
    #    #    return card._suit in Card.RedSuits
    #    #return card._suit in Card.BlackSuits

    #def attaches(self, card):
    #    if card.below(self) and card.opposite_color(self):
    #        return True
    #    else:
    #        return False

    #def attach(self, card: Card, stack : ty.List[Card]) -> bool:
    #    ''' attach a card to the end of a list if follows solitaire rules.
    #    Args:
    #        card: Card
    #        stack: a list of Cards, append to the list if legal
    #    Returns:
    #        True iff attached
    #    '''
    #    if card.below(self) and card.opposite_color(self):
    #        return True
    #    else:
    #        return False

    def __str__(self):
        return self._title

def cards_to_str(card_list: [Card]) -> str:
    '''
    debug method to create a string from a list of cards
    '''
    return ','.join([str(c) for c in card_list])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test cards')
    parser.add_argument('--random', '-r',
                        type=int,
                        help='number between 1 and 13')
    parser.add_argument('--a',
                        action='store_true',
                        help='ace test')
    parser.add_argument('--k',
                        action='store_true',
                        help='king test')
    args = parser.parse_args()

    for s in Suits:
        for c in range(*card_range()):
            acard = Card(c, s)
            #print(f'{c}:{s} -> {acard},', end=' ')
            print(f'{acard},', end=' ')
        print()
    print(f'ace:{ace} to king:{king}')
    print(f'{min_suit()=} to {max_suit()=}')
    try:
        xc = Card(0, Suits.SPADE)
    except AssertionError as e:
        print(f'got low: {e}')
    try:
        xc = Card(14, Suits.CLUB)
    except AssertionError as e:
        print(f'got hi: {e}')

    if args.random:
        if (args.random < ace) or (args.random > king):
            print(f'bad card value: {args.random}')
            args.random = Card.king()
        numcards = random.randint(1, args.random)
        for i in range(1, numcards):
            s = random.randint(1, 4)
            acard = Card(i, s)
            print(f'{_card_map[i]}:{Card._suit_map[s]} => {acard},',
                  end=' ')
            if (i & 15) == 0:
                print()
                break
        print()

