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
        each stack is a single suit that has to be in the A to K order.
    '''
    def __init__(self):                                                         
        self._stacks = {C.Suits.SPADE:[],
                        C.Suits.HEART:[],
                        C.Suits.DIAMOND:[],
                        C.Suits.CLUB:[]
                       }
                                                                                
    def stack(self, s: C.Suits) -> ty.List[C.Card]:
        return self._stacks[s]

    def add_card(self, card: C.Card) -> bool:                                                    
        '''
        Args:
            card: is a C.Card
        Returns:
            True iff a card added to the Foundation,
        Rutes:
            if stack is empty card must be an Ace to attach,
            otherwise the "top" of stack must be one less than
            the new card and the opposite color
        '''                                       
        print(f'f.ad: {card}')
        stack = self._stacks[card.suit] # get suit stack
        if not stack:
            # if the foundation stack is empty we can only add an Ace
            if card.value == C.Card.ace():
                stack.append(card)
                return True
        # stack not empty, so the rule is that the bottom if the stack is
        # one less then new card
        print(f'f.ac{C.cards_to_str(stack)}')
        if (card.value - stack[-1].value) == 1:
            stack.append(card)
        return False
                                                                                
    def top_card_str(self, suit: C.Suits) -> str:
        ''' get the string for current top card by suit from its stack
        Returns:
            the top card title of a foundation pile. If the pile               
            is empty, return the symbol for the suit.
        '''
        #print(f'f.tcs: {suit}')
        stack = self._stacks[suit]                                    
        if not stack:
            return C.Card.symbol(suit)
        return str(self._stacks[suit][-1])
                                                                                
    def game_won(self) -> bool:                                                          
        ''' solitaire rule for game won, i.e. all four stacks are full.
        Returns:
            True iff the game is won, i.e., when all stacks being full!
        '''
        print(f'check game won')
        if any(not s for s in self._stacks.values()):
            return False
        # return true iff all stacks have a king as the top card.
        b_all = all(s[-1].value == C.Card.king() for s in self._stacks.values())
        return b_all

def print_foundation(f: Foundation) -> None:
    for s in C.Suits:
        stack = f.stack(s)
        print(f'F:{C.Card.symbol(s)}: {C.cards_to_str(stack)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test foundation operations')
    parser.add_argument('--seed', '-s',
                        type=int,
                        help='set seed')
    parser.add_argument('--interval', '-i',
                        type=int,
                        default=7,
                        help='check interval default: %(default)s')
    args = parser.parse_args()
    if args.seed != None:
        random.seed(args.seed)
    deck = D.Deck()
    f = Foundation()
    i = args.interval
    print(f'Start Not Won?: {f.game_won()}')
    for s in C.Suits:
        print(f'{f.top_card_str(s)}: ', end='')
        for c in range(*C.card_range()):
            i = i - 1
            f.add_card(C.Card(c, s))
            if i <= 0:
                print_foundation(f)
                print(f'Mid {i=} Won?: {f.game_won()}')
                i = args.interval
        print_foundation(f)
        print(f'End suits {s} Won?: {f.game_won()}')
    print_foundation(f)
    print(f'Game Won?: {f.game_won()}')

