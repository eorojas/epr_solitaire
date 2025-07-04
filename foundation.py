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


class Foundation():                                                                                                                                                                                           
    ''' class represents the four stacks that we are trying to fill to win
    '''
    def __init__(self):                                                         
        self._stacks = {C.Suits.SPADE:[],
                        C.Suits.HEART:[],
                        C.Suits.DIAMOND:[],
                        C.Suits.CLUB:[]
                       }
                                                                                
    def add_card(self, card: C.Card) -> bool:                                                    
        '''
        Args:
            card: is a C.Card
        Returns:
            True iff a card added to the Foundation,
        '''                                       
        stack = self._stacks[card.suit]
        if (not stack and card.value == 1) or stack[-1].below(card):
            stack.append(card)                                                  
            return True
        return False
                                                                                
    def get_top_card(self, suit: C.Card) -> str:
        ''' get the current top card by suit from its stack
        Returns:
            the top card title of a foundation pile. If the pile               
            is empty, return the letter of the suit.
        '''
        stack = self._stacks[suit]                                    
        if not stack:
            return C.symbol(suit)
        return str(self._stacks[suit][-1])
                                                                                
    def game_won(self) -> bool:                                                          
        '''
        Returns: True iff the game is won as indicated all stacks being full!
        '''
        if not any(not s for s in self._stacks.values()):
            return False
        # return true iff all stacks have a king as the top card.
        return any(s[-1] == 13 for s in self._stacks.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test foundation operations')
    args = parser.parse_args()
    f = Foundation()
    for s in C.Suits:
        for c in range(*C.card_range()):
            f.add_card(C.Card(c, s))
    print(f'Game Won?: {f.game_won()}')
