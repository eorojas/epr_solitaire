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

UNDER='[4m'


class Card():
    _range = {1, 14} # i.e, Ace to King, or 1 to 13
    _suit_range = {1, 4} # Spades, hearts, diamonds, clubs
    def card_range():
        return Card._range

    _card_map = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7',
               8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K'}

    class Suits(enum.IntEnum):
        SPADE = enum.auto() 
        HEART = enum.auto() 
        DIAMOND = enum.auto() 
        CLUB = enum.auto() 

    _suit_map = {
        Suits.SPADE : 'spade',
        Suits.HEART : 'heart',
        Suits.DIAMOND : 'diamod',
        Suits.CLUB : 'club',
    }

    #Suits = {'club', 'diamond', 'spade', 'heart'}
    RedSuits = {Suits.DIAMOND, Suits.HEART}
    BlackSuits = {Suits.SPADE, Suits.CLUB}
    Symbols = {Suits.SPADE:'\u2660',
               Suits.HEART:'\u2661',
               Suits.DIAMOND:'\u2662',
               Suits.CLUB:'\u2663'} 

    def __init__(self, value: int, suit: Suits):
        self._name = self._card_map[value]
        self._suit = suit
        self._color = COLOR_RED if suit in Card.RedSuits else COLOR_BLUE
        self.title \
            = f'{self._color}{self._name}{Card.Symbols[self._suit]}{COLOR_NONE}'
        self.value = value

    def below(self, card):
        return self.value == (card.value - 1)

    def opposite_color(self, card):
        #if self._suit == 'club' or self._suit == 'spade':
        # TODO(epr): no reason to check twice
        if self._suit in Card.BlackSuits:
            return card._suit in Card.RedSuits
        return card._suit in Card.BlackSuits

    def attaches(self, card):
        if card.below(self) and card.opposite_color(self):
            return True
        else:
            return False

    def __str__(self):
        return self.title

def cards_to_str(card_list: [Card]) -> str:
    '''
    debug method to create a string from a list of cards
    '''
    return ','.join([str(c) for c in card_list])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test cards')
    parser.add_argument('--random', '-r',
                        type=int,
                        help='random random')
    args = parser.parse_args()

    for s in Card.Suits:
        for c in range(*Card._range):
            acard = Card(c, s)
            #print(f'{c}:{s} -> {acard},', end=' ')
            print(f'{acard},', end=' ')
        print()
    if args.random:
        mincard, maxcard = 1, 14
        maxcard -= 1
        numcards = random.randint(1, args.random)
        for i in range(1, numcards):
            s = random.randint(1, 4)
            acard = Card(i, s)
            print(f'{Card._card_map[i]}:{Card._suit_map[s]} => {acard},',
                  end=' ')
            if (i & 15) == 0:
                print()
        print()
