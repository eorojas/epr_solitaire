#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#
import argparse
import functools as ft
import pathlib as pl
import random
import re
import sys
import typing as ty

import cards as C
import deck as D
import foundation as F
import parse_sol_cmds as psc
#import stock_waste as W


class Tableau():
    ''' Class that keeps track of the seven piles of cards on the Tableau
        The Tableau has seven columns, each column has flipped and unflipped
        cards with flipped cards concieved as on top of the unflipped.
        Each column is represented as dictionary of cards.
    '''
    _cols = 7

    def cols() -> int:
        return Tableau._cols

    def __init__(self,
                 cards_lists: ty.List[[ty.List[C.Card]]],
                 foundation: F.Foundation):
                 #waste: W.StockWaste):
        '''
        Args:
            cards_list is a lists, one for each column with counts
            1, 2, 3, ..., 7
            #TODO(epr): consider passing the deck and doing this all there.
            #   rather than passing list of lists
        The result of the init is that we have two dictionaries
        for each column. The flipped (the cards on top) and the
        unflipped the hidden cards.
        The dictionaries are indexed by column numbers 0 to 6
        '''
        self._F = foundation
        #self._W = waste
        self.unflipped = {x: cards_lists[x] for x in range(Tableau._cols)}
        self.flipped = {x: [self.unflipped[x].pop()]
                        for x in range(Tableau._cols)}

    def flip_card(self, col: int):
        ''' Flips a card under column col on the Tableau
            Iff the len(unflipped) > 0
                pop the unflipped and push to flipped.
        Args:
            col: must be in the range 0 to 6
            TODO(epr): can this be done if flipped isn't empty?
        '''
        if len(self.unflipped[col]) > 0:
            self.flipped[col].append(self.unflipped[col].pop())

    def pile_length(self):
        ''' Returns the length of the longest pile on the Tableau
        '''
        return max([len(self.flipped[x]) + len(self.unflipped[x])
                        for x in range(Tableau._cols)])

    def add_cards(self, clist, column):
        ''' Returns true if clist were successfully
                added to column on the Tableau.
            else false
        Args:
            clist: a solitarie sorted list of cards.
            column: int, in range 0 to 6
        '''
        column_cards = self.flipped[column]
        # check of if the colume is empty and the is a king list.
        if len(column_cards) == 0 and clist[0].value == 13:
            column_cards.extend(clist)
            return True
        # if there are cards and the solitaire attach rule is followed
        # extend this list to the column
        if len(column_cards) > 0 and column_cards[-1].attaches(clist[0]):
            column_cards.extend(clist)
            return True
        return False

    def tableau_to_tableau(self, c1, c2):
        ''' Returns True if any card(s) are successfully moved from
            c1 to c2 on the Tableau, returns False otherwise.
        '''
        c1_cards = self.flipped[c1]

        for index in range(len(c1_cards)):
            if self.add_cards(c1_cards[index:], c2):
                self.flipped[c1] = c1_cards[0:index]
                if index == 0:
                    self.flip_card(c1)
                return True
        return False

    def to_foundation(self, column):
        ''' Moves a card from the Tableau to the appropriate
            Foundation pile
        '''
        column_cards = self.flipped[column]
        if len(column_cards) == 0:
            return False
        # was _foundation
        if self._F.add_card(column_cards[-1]):
            column_cards.pop()
            if len(column_cards) == 0:
                self.flip_card(column)
            return True
        return False

    def waste_to_tableau(self, waste_pile, column):
        ''' Returns True if a card from the Waste pile is succesfully
            moved to a column on the Tableau, returns False otherwise.
        '''
        card = waste_pile._waste[-1]
        if self.add_cards([card], column):
            waste_pile.pop_waste_card()
            return True
        return False

def print_tableau(t: Tableau):
    '''
    Debug method to print tableau contents
    '''
    print(f'PL: {t.pile_length()}')
    for col in range(Tableau.cols()):
        #print(f'F({len(t.flipped)}:{t.flipped}')
        print(f'{col}:F:{C.cards_to_str(t.flipped[col])}', end=' -- ')
        print(f'U: {C.cards_to_str(t.unflipped[col])}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test tableau')
    parser.add_argument('--deck', '-d',
                        type=pl.Path,
                        default=None,
                        help='path of deck lay')
    args = parser.parse_args()
    deck = D.Deck()
    # generate a list of lists [1-card, 2-cards, ..., 7-cards]
    f = F.Foundation()
    t = Tableau([deck.deal_cards(x) for x in range(1, Tableau.cols() + 1)], F)
    print_tableau(t)

