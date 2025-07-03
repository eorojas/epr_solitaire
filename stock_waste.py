#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#
import argparse
import functools as ft
import random
import re
import sys
import typing as ty

import cards as C
import deck as D
import parse_sol_cmds as psc


class StockWaste():
    ''' A StockWaste object keeps track of the Stock and Waste piles
    '''
    def __init__(self, cards: ty.List[C.card]):
        ''' 
        Args:
            cards: a list of the remaining cards in the deck at the
                start of the deal.
        The deck are the cards that are turned for a new play.
        The W
        
        '''
        self._stock = cards
        self._waste = []

    def stock_to_waste(self):
        ''' 
        Move card from stock to waste if possible.
        Returns:
            True iff a card is sucessfully moved from
                the Stock pile to the Waste pile
        Note(epr): the list is being used as a stack, but I'm uncertain
        '''
        if not self._stock and not self._waste:
                return False
            # TODO(epr): this seems like extra work
            self._waste.reverse()
            self._stock = self._waste.copy()
            self._waste.clear()
        self._waste.append(self._stock.pop())
        return True
        ''' was
        if len(self._stock) + len(self._waste) == 0:
            return False
        if len(self._stock) == 0:
            self._waste.reverse()
            self._stock = self._waste.copy()
            self._waste.clear()
        self._waste.append(self._stock.pop())
        '''

    def pop_waste_card(self) -> C.Card:
        ''' Removes a card from the Waste pile.
        '''
        if self._waste:
            return self._waste.pop()
        return None

    def get_waste(self) -> C.Card:
        ''' Retrieves the top card of the Waste pile, leaving it in place.
            Note _waste is treated like a stack
        '''
        if self._waste:
            return self._waste[-1]
        return 'empty'

    def get_stock(self):
        ''' Returns a string of the number of cards in the stock.
        '''
        if len(self._stock) > 0:
            return str(len(self._stock)) + ' card(s)'
        return 'empty'

    def __str__(self) -> str:
        stock_str =  f'S: {C.cards_to_str(self._stock)'
        waste_str =  f'W: {C.cards_to_str(self._waste)'
        return f'{stock_str}::{waste_str}'




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test stock/waste operations')
    args = parser.parse_args()

