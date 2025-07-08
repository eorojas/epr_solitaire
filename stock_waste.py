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
        TODO(epr): consider as a subclass of Foundation
    '''
    def __init__(self, cards: ty.List[C.Card]):
        ''' 
        Args:
            cards: a list of the remaining cards in the deck at the
                start of the deal.
        The stock are the cards that are turned for a new play.
        The waster are the card availabe after turning
        '''
        self._stock = cards
        self._waste = []

    def stock_to_waste(self):
        ''' 
        Move card from stock to waste if possible.
        Returns:
            True iff a card is sucessfully moved from
                the Stock pile to the Waste pile
        Note(epr): the list is being used as a stack.
        '''
        print(f'SW: stw')
        if not self._stock and not self._waste:
            return False
        if not self._stock:
            self._waste.reverse()
            self._stock = self._waste.copy()
            self._waste.clear()
        self._waste.append(self._stock.pop())
        return True

    def pop_waste_card(self) -> C.Card | None:
        ''' Removes a card from the Waste pile.
        '''
        if self._waste:
            return self._waste.pop()
        return None

    def get_waste(self) -> C.Card:
        ''' Retrieves the top card of the Waste pile, leaving it in place.
            Note _waste is treated like a stack
        '''
        print(f'SW.gw: {C.cards_to_str(self._waste)}')
        if self._waste:
            return self._waste[-1]
        return None

    def get_stock(self):
        ''' Returns a string of the number of cards in the stock.
        '''
        print(f'SW.gs: {C.cards_to_str(self._stock)}')
        if len(self._stock) > 0:
            return str(len(self._stock)) + ' card(s)'
        return None

    def __str__(self) -> str:
        stock_str =  f'S: {C.cards_to_str(self._stock)}'
        waste_str =  f'W: {C.cards_to_str(self._waste)}'
        return f'{stock_str}::{waste_str}'

def print_sw(sw):
    print(f'\n{sw}')


if __name__ == '__main__':
    parser = \
        argparse.ArgumentParser(description='Test stock/waste operations')
    args = parser.parse_args()
    d = D.Deck()
    card_cnt = 17
    sw = StockWaste(d.deal_cards(card_cnt))
    print(f'{sw.get_stock()}')
    print(f'{sw.get_waste()}')
    for i in range(card_cnt):
        sw.stock_to_waste()
        print(f'{sw}')

