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
import deck
import parse_sol_cmds as psc

BREAK_STRING \
    = '\n-------------------------------------------------------------------'

UNDER='[4m'

_lfd = None
def set_log_file(lfd):
    global _lfd
    _lfd = lfd
    return None

def logit(*args) -> None:
    print(*args, file=_lfd, flush=True)
    return None

def plogit(*args) -> None:
    print(*args, file=_lfd, flush=True)
    print(*args, file=sys.stdout)
    return None


_deck = None
_tableau = None
_foundation = None
_waste = None
_show_hidden = False


def new_deal(positons: []) -> bool:
    global _deck, _tableau, _foundation, _waste
    _deck = deck.Deck()
    # deal out the cards for the tableau, cars arranged init
    _tableau = Tableau([_deck.deal_cards(x)
                        for x in range(1, Tableau.cols() + 1)])
    _foundation = Foundation()
    _waste = StockWaste(_deck.deal_cards())
    return True


def next_card(positons: []) -> None:
    ''' turn over the stock pile and put it on the waste/discard pile
        positions should be empty
    '''
    if _waste.stock_to_waste():
        print_table(args.show_hidden)
    return None


def waste_to_foundation(positions: []) => None:
    ''' move the top card in the waste to its foundation pile
        positions should be empty
    '''
    if _foundation.add_card(_waste.get_waste()):
        _waste.pop_waste_card()
        print_table(args.show_hidden)
    else:
        print('Card could be moved from the'
                'Waste to the Foundation.')
    return None

def waste_to_tableau(positions: [int]) -> None:

    ''' move card from the waste/discard pile to positions[0]
        cmd: wt
        Args:
              
              positions: 
    '''
    col = positions[0]
    if _tableau.waste_to_tableau(_waste, col):
        print_table(_show_hidden)
        return None
    print(f'{card} could be moved Tableau column.')
    return None


def tableau_to_foundation(positions: [int]) -> None:
    ''' move card at positions[0] to its foundation pile
        postions[0] is the column of interest
        cmd: tf
    '''
    col = position[0]
    if _tableau.to_foundation(col):
        print_table(_show_hidden)
        return None
    #print(f'card could be moved from {col=}')
    return None


def tableau_to_tableau(col1: int, col2: int) -> None:
    if _tableau.tableau_to_tableau(col1, col2):
        print_table(_show_hidden)
        return None
    print(f'card could be moved from that'
                'Tableau column.')
    return None


def foundation_to_tableau(suit: int, col: int):
    return None


def undo_last():
    print('Undo Not Available.')
    return None

def replay():
    print('Replay Not Available.')
    return None


def hint():
    print('Hint Not Available.')
    return None

def sol_quit():
    print('Game exited.')
    sys.exit(0)

def invalid_cmd():
    print('Invalid command, h for help')


_cmds = {
    'N' : new_deal,
    'n' : next_card,
    'wt' : waste_to_tableau,
    'tf' : tableau_to_foundation,
    'tt' : tableau_to_tableau,
    'ft' : foundation_to_tableau,
    'u' : undo_last,
    'u' : undo_last,
    'r' : replay,
}
_cmd_table = {
    SolActs.QUIT : sol_quit,
    SolActs.HELP : show_cmds,
    SolActs.NEW_DEAL : new_deal,
    SolActs.STOCK_TO_WASTE : next_card,
    SolActs.WASTE_TO_TABLEAU : waste_to_tableau,
    SolActs.TABLEAU_TO_FOUNDATION : tableau_to_foundation
    SolActs.TABLEAU_TO_TABLEAU : tableau_to_tableau
    SolActs.UNDO : undo_last,
    SolActs.HINT : hint,
    SolActs.SOLVE : solve,
}

_help = '''Valid Commands:
N - new deal
n - move card from Stock to Waste
wt #T - move card from Waste to Tableau
tf #T - move card from Tableau to Foundation
tt #T1 #T2 - move card from one Tableau column to another
u - undo
h - help
H - hint
s - solve
q - quit'''

def show_cmds():
    ''' Provides the list of commands, for when users press h
    '''
    print(_help)

def print_table(show_hidden: bool=False):
    ''' Prints the current status of the table
    '''
    global _deck, _tableau, _foundation, _waste
    # TODO(epr): use ANSI positioning to write in same place
    #   last step in refactoring
    print(BREAK_STRING)
    print('Waste \t Stock \t\t\t\t Foundation')
    print('{}\t{}\t\t{}\t{}\t{}\t{}'.format(_waste.get_waste(),
            _waste.get_stock(), 
            _foundation.top_card_str(C.Suits.SPADE),
            _foundation.top_card_str(C.Suits.HEART), 
            _foundation.top_card_str(C.Suits.DIAMOD),
            _foundation.top_card_str(C.Suits.CLUB))
          )
    print('\nTableau\n\t1\t2\t3\t4\t5\t6\t7\n')
    # Print the cards, first printing the unflipped cards,
    # and then the flipped.
    for pile_depth in range(_tableau.pile_length()):
        print_str = ''
        for col in range(Tableau.Columns):
            hidden_cards = _tableau.unflipped[col]
            shown_cards = _tableau.flipped[col]
            if len(hidden_cards) > pile_depth:
                if show_hidden:
                    logit(f'{pile_depth=}, {len(hidden_cards)=}')
                    uf = ', '.join([str(c) for c in _tableau.unflipped[col]])
                    logit(f'{col=}:{uf}')
                    #print_str += '\tx'
                    print_str += f'\t{UNDER}{str(_tableau.unflipped[col][pile_depth])}'
                else:
                    print_str += '\tx'
            elif len(shown_cards) + len(hidden_cards) > pile_depth:
                print_str += '\t' + str(shown_cards[pile_depth
                                                    - len(hidden_cards)])
            else:
                print_str += '\t'
        #logit(f'{print_str=}')
        print(print_str)
    print(BREAK_STRING)


if __name__ == '__main__':
    #print(Card.Symbols)
    #sys.exit(1)
    parser = argparse.ArgumentParser(description=\
            'Play solitair')
    parser.add_argument('--show_hidden', '-s',
                        action='store_true',
                        help='show the hidden cards')
    parser.add_argument('--log_file', '-l',
                        type=argparse.FileType('w'),
                        default='S.log',
                        help='define the log file: def: (default)s')
    args = parser.parse_args()
    set_log_file(args.log_file)
    _show_hidden = args.show_hidden
    new_deal()

    print(BREAK_STRING)
    print('Welcome to Danny\'s Solitaire!\n')
    show_cmds()
    print_table(args.show_hidden)

    while not _foundation.gameWon():
        command = input('Enter a command (type "h" for help): ')
        logit(command)
        cmdi, positions = psc.parse_sol_cmds(command)
        """
        if command[0] in 'hH':
            show_cmds()
            continue
        if command[0] in 'qQ':
            break
        command = command.lower().replace(' ', '')
        clen = len(command)
        if clen >= 3:
            def col2num(cc: str) -> int:
                if col < '1' or colc > '7':
                    print('column out of range 1 to 7')
                    return -1
                return int(colc) - 1
            colc1 = col2num(command[2])
            if colc1 == -1:
                continue
            if clen != 4:
                print('invalid cmd')
                continue
            if col < '1' or colc > '7':
                print('colume out of range 1 to 7')
                continue
            col = int(colc) - 1
            logit(f'{col=}')
        if command == 'n' :
            if _waste.stock_to_waste():
                print_table(args.show_hidden)
        elif command == 'wf':
            if _foundation.add_card(_waste.get_waste()):
                _waste.pop_waste_card()
                print_table(args.show_hidden)
            else:
                print('Error! No card could be moved from the'
                        'Waste to the Foundation.')
        elif 'wt' in command and len(command) == 3:
            #col = int(command[-1]) - 1
            if _tableau.waste_to_tableau(_waste, col):
                print_table(args.show_hidden)
            else:
                print('Error! No card could be moved'
                        'from the Waste to the Tableau column.')
        elif 'tf' in command and len(command) == 3:
            #col = int(command[-1]) - 1
            if _tableau.to_foundation(col):
                print_table(args.show_hidden)
            else:
                print('Error! No card could be moved from the'
                        'Tableau column to the Foundation.')
        elif 'tt' in command and len(command) == 4:
            c1, c2 = int(command[-2]) - 1, int(command[-1]) - 1
            if _tableau.tableau_to_tableau(c1, c2):
                print_table(args.show_hidden)
            else:
                print('Error! No card could be moved from that'
                        'Tableau column.')
        else:
            print('Sorry, that is not a valid command.')
        """

    if _foundation.gameWon():
        print('Congratulations! You\'ve won!')
    print('Game exited.')

