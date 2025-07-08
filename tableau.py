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
import stock_waste as SW

_cols = 7

class Tableau():
    ''' Class that keeps track of the seven piles of cards on the Tableau
        The Tableau has seven columns, each column has flipped and unflipped
        cards with flipped cards concieved as on top of the unflipped.
        Each column is represented as dictionary of cards.
        Note(epr): columns go from 0 to 6
            adjust at APIs
    '''

    def cols() -> int:
        return _cols

    def __init__(self,
                 cards_lists: ty.List[[ty.List[C.Card]]],
                 foundation: F.Foundation):
        '''
        Args:
            cards_list is a lists, one for each column with counts
            1, 2, 3, ..., 7
            #TODO(epr): consider passing the deck and doing this all there.
            #   rather than passing list of lists
            foundation: is an empty foundation at game start
        The result of the init is that we have two dictionaries
        for each column. The flipped (the cards on top) and the
        unflipped the hidden cards.
        The dictionaries are indexed by column numbers 0 to 6
        '''
        self._F = foundation
        self._unflipped = {x: cards_lists[x] for x in range(_cols)}
        self._flipped = {x: [self._unflipped[x].pop()]
                        for x in range(_cols)}

    @property
    def unflipped(self):
        return self._unflipped

    @property
    def flipped(self):
        return self._flipped

    def flip_card(self, srcc: int):
        ''' Flips a card in srcc on the Tableau
            Iff the len(unflipped) > 0
                pop the unflipped and push to flipped.
        Args:
            srcc: must be in the range 0 to 6
            TODO(epr): can this be done if flipped isn't empty?
        '''
        if self._unflipped[srcc]:
            self._flipped[srcc].append(self._unflipped[srcc].pop())

    def pile_length(self):
        ''' Returns the length of the longest pile on the Tableau
        '''
        return max([len(self._flipped[x]) + len(self._unflipped[x])
                        for x in range(_cols)])

    def add_card(self, card: C.Card, dstc: int) -> bool:
        ''' add a single card to the column in the tableaue
        Args:
            card: a C.Card
            dstc: the tableaue column we are trying to attached card to
        Returns:
            True iff it was attached, else False
        '''
        column_cards = self._flipped[dstc]
        if not column_cards and card.value == C.king_value:
            column_cards.append(card)
            return True
        attach_card = column_cards[-1]
        if card.color == attach_card.color:
            return False # can not attach some color
        # sum will be zero when we can attach: 1 below + 1 is zero
        if card.value - attach_card.value + 1:
            return False # not zero cannot attach
        column_cards.append(card)
        return True

    def add_cards(self,
                  clist: ty.List[C.Card],
                  column: ty.List[C.Card]) -> bool:
        ''' adds cards to the column iff it follows solitaire rules.
            If the column is empty only a King(13) can be added.
            otherwise the card must have the opposite color and
            be one below the card that it attaches to.
        Args:
            clist: a solitaire ordered list of cards.
            column: a solitaire ordered list of cards.
        Returns:
            True if clist was successfully added to column on the tableau
            else False
        '''
        print(f'T.addC: new {C.cards_to_str(clist)}')
        #column_cards = self._flipped[column]
        print(f'T.addC: to {C.cards_to_str(column)}')
        # check of if the colume is empty and the is a king list.
        if not column and clist[0].value == C.king_value:
            column.extend(clist)
            return True
        #if not column_cards:
        #    return False
        attach_to_c = clist[0]
        attach_card = column[-1]
        # colors must not be the same to add on tableau
        if attach_to_c.color == attach_card.color:
            print(f'T.addC: bad color')
            return False
        # sum will be zero when we can attach: 1 below + 1 is zero
        if attach_to_c.value - attach_card.value + 1:
            print(f'T.addC:  {attach_to_c.value=} {attach_card.value=}')
            return False
        # Ok extend the column with the new list
        column.extend(clist)
        print(f'T.addC: newcol {C.cards_to_str(column)}')
        return True

    def tableau_to_tableau(self, srcc: int, dstc: int) -> bool:
        ''' Moves some part of the flipped cards in column srcc
            to the bottom for column dest
        Args:
            srcc: the source column 1 based
            dstc: the dest column 1 based
        Returns:
            True if any card(s) are moved from
            srcc to dstc, Otherwise False
        '''
        print(f'Ttt {srcc=} -> {dstc=}')
        src_cards = self._flipped[srcc]
        dst_cards = self._flipped[dstc]
        print(f'Ttt src:{C.cards_to_str(src_cards)}')
        print(f'Ttt dst:{C.cards_to_str(dst_cards)}')

        # walk down the source pile until we find a plce to append to
        # srcc to dstc
        # TODO(epr): this looks a little inefficient
        for index in range(len(src_cards)):
            print(f'Ttt:{index=}')
            if self.add_cards(src_cards[index:], dst_cards):
                self._flipped[srcc] = src_cards[0:index]
                if index == 0:
                    self.flip_card(srcc)
                return True
        return False

    def to_foundation(self, srcc: int) -> bool:
        ''' Moves a card from the bottom of the column to the appropriate
            Foundation pile
        Args:
            srcc: index of source column
        '''
        print(f'T.tf: {srcc=}')
        column = self._flipped[srcc]
        if not column:
            return False
        if self._F.add_card(column[-1]):
            column.pop()
            if not column:
                self.flip_card(srcc)
            return True
        return False

    def waste_to_tableau(self, waste_pile, dstc):
        ''' Moves the card at the "top" of the waste to col
            TODO(epr): passing the waste_pile here ranter than having
                it be a member is inconsistent, but it avoids a circular
                reference
        Args:
            waste_pile: is the waste pile.
            dstc: target column
        Returns:
            True if a card from the Waste pile is succesfully
            moved to a column on the Tableau, returns False otherwise.
        '''
        card = waste_pile._waste[-1]
        print(f'T.wt: {card} -> {dstc}')
        if self.add_card(card, dstc):
            waste_pile.pop_waste_card()
            print(f'T.wt: {card} -> {dstc}')
            return True
        return False


def print_tableau(t: Tableau):
    '''
    Debug method to print tableau contents
    '''
    print(f'PL: {t.pile_length()}')
    for dstc in range(Tableau.cols()):
        #print(f'F({len(t._flipped)}:{t._flipped}')
        print(f'{dstc + 1}:F:{C.cards_to_str(t._flipped[dstc])}', end=' -- ')
        print(f'U: {C.cards_to_str(t._unflipped[dstc])}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test tableau')
    parser.add_argument('--deck', '-d',
                        type=pl.Path,
                        default=None,
                        help='path of deck lay')
    parser.add_argument('--seed', '-s',
                        type=int,
                        help='set seed')
    args = parser.parse_args()
    if args.seed != None:
        random.seed(args.seed)
    deck = D.Deck()
    # generate a list of lists [1-card, 2-cards, ..., 7-cards]
    f = F.Foundation()
    t = Tableau([deck.deal_cards(x) for x in range(1, Tableau.cols() + 1)], F)
    sw = SW.StockWaste(deck.deal_cards())
    print_tableau(t)
    SW.print_sw(sw)

