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
import foundation as F
import tableau as T
import stock_waste as SW
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


def new_deal(cmd_args: ty.List[C.Card]) -> bool:
    global _deck, _tableau, _foundation, _waste
    _deck = D.Deck()
    _foundation = F.Foundation()
    # deal out the cards for the tableau, cars arranged init
    t_cards = [_deck.deal_cards(x) for x in range(1, T.Tableau.cols() + 1)]
    _tableau = T.Tableau(t_cards, _foundation)
    _waste = SW.StockWaste(_deck.deal_cards())
    return True


def stock_to_waste(cmd_args: ty.List[int]) -> None:
    ''' turn over the stock pile and put it on the waste/discard pile
        cmd_args should be empty
        cmd is "m"
    '''
    print(f'S.stw: {cmd_args}')
    _waste.stock_to_waste()
    return None


def waste_to_foundation(cmd_args: ty.List[int]) -> None:
    ''' Move the top card in the waste to its foundation pile
    Args:
        cmd_args: should be empty
    cmd is "w"
    '''
    print(f'S.wtf: {cmd_args}')
    c = _waste.get_waste()
    print(f'wtf: {c}')
    if _foundation.add_card(_waste.get_waste()):
        # TODO(epr): accessses waste twice
        _waste.pop_waste_card()
    return None

def waste_to_tableau(cmd_args: ty.List[int]) -> None:
    ''' Move card from the waste/discard pile col in tableaeu
    Args:
        cmd_args: col to move to
    cmd is "w C"
    '''
    col = cmd_args[0]
    print(f'S.wtt: {col=} -> ')
    if _tableau.waste_to_tableau(_waste, col):
        return None
    return None


def tableau_to_foundation(cmd_args: ty.List[int]) -> None:
    ''' Move card at cmd_args[0] to its foundation pile
    Args:
        cmd_args: [x] contains pile number
    cmd is "t C'
    '''
    col = cmd_args[0]
    print(f'S.TTF: {cmd_args=}')

    if _tableau.to_foundation(col):
        return None
    return None


def tableau_to_tableau(cmd_args: ty.List[int]) -> None:
    ''' Move column from one col to another. The from column can
        be partial.
    cmd is t C C
    '''
    print(f'ttt: {cmd_args}')
    if _tableau.tableau_to_tableau(cmd_args[0], cmd_args[1]):
        return None
    return None


def foundation_to_tableau(cmd_args: ty.List[int]) -> None:
    return None


def undo_last(cmd_args: ty.List[int]) -> None:
    print('Undo Not Available.')
    return None

def replay(cmd_args: ty.List[int]) -> None:
    print('Replay Not Available.')
    return None


def hint(cmd_args: ty.List[int]) -> None:
    print('Hint Not Available.')
    #input('no hint')
    return None


def solve(cmd_args: ty.List[int]) -> None:
    print('Solve Not Available.')
    return None


def sol_quit(cmd_args: ty.List[int]) -> None:
    print('Exited solitaire.')
    sys.exit(0)

def invalid_cmd(cmd_args: ty.List[int]) -> None:
    print('Invalid command, ? or <enter> for help')
    show_cmds([])


_help = None
'''Valid Commands:
N - new deal
n - move card from Stock to Waste
wt #T - move card from Waste to Tableau
tf #T - move card from Tableau to Foundation
tt #T1 #T2 - move card from one Tableau column to another
u - undo
h - help
H - hint
s - solve
? - helop
q - quit'''

def show_cmds(cmd_args: ty.List[int]) -> None:
    ''' Provides the list of commands, for when users press h
    '''
    global _help
    if not _help:
        _help = psc.create_sol_help()
    print(_help)



_cmd_table = {
    psc.SolActs.NEW_DEAL : new_deal,
    psc.SolActs.WASTE_FOUNDATION: waste_to_foundation,
    psc.SolActs.STOCK_TO_WASTE : stock_to_waste,
    psc.SolActs.WASTE_TO_TABLEAU : waste_to_tableau,
    psc.SolActs.TABLEAU_TO_FOUNDATION : tableau_to_foundation,
    psc.SolActs.TABLEAU_TO_TABLEAU : tableau_to_tableau,
    psc.SolActs.UNDO : undo_last,
    psc.SolActs.QUIT : sol_quit,
    psc.SolActs.REPLAY : replay,
    psc.SolActs.HINT : hint,
    psc.SolActs.SOLVE : solve,
    psc.SolActs.HELP : show_cmds,
    psc.SolActs.INVALID : invalid_cmd,
}


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
            _foundation.top_card_str(C.Suits.DIAMOND),
            _foundation.top_card_str(C.Suits.CLUB))
          )
    print('\nTableau\n\t1\t2\t3\t4\t5\t6\t7\n')
    # Print the cards, first printing the unflipped cards,
    # and then the flipped.
    for pile_depth in range(_tableau.pile_length()):
        print_str = ''
        for col in range(T.Tableau.cols()):
            hidden_cards = _tableau.unflipped[col]
            shown_cards = _tableau.flipped[col]
            if len(hidden_cards) > pile_depth:
                if show_hidden:
                    logit(f'{pile_depth=}, {len(hidden_cards)=}')
                    uf = ', '.join([str(c) for c in _tableau.unflipped[col]])
                    logit(f'{col=}:{uf}')
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
    new_deal([])

    print(BREAK_STRING)
    print('SOLITAIRE!\n')
    show_cmds([])
    print_table(args.show_hidden)

    while True:
        while not _foundation.game_won():
            try:
                sol_cmd = psc.parse_sol_cmds()
            except psc.InvalidCmd as e_ic:
                print(e_ic)
                continue
            print(f'LOOP: {sol_cmd}')
            _cmd_table[sol_cmd.cmd](sol_cmd.cargs)
            print_table(args.show_hidden)

        print('Congratulations! You\'ve won!')
        y = input('Another?')
        if y[0] == 'y':
            break
    print('Bye!')

