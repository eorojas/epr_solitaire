#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#
import argparse
import enum
import functools as ft
import os
import pathlib
import random
import re
import sys
import typing as ty
import shutil

class SolActs(enum.IntEnum):
    ''' Solitaire actions
    '''
    QUIT = enum.auto()
    HELP = enum.auto()
    NEW_DEAL = enum.auto()
    STOCK_TO_WASTE = enum.auto()
    WASTE_TO_TABLEAU = enum.auto()
    TABLEAU_TO_FOUNDATION = enum.auto()
    TABLEAU_TO_TABLEAU = enum.auto()
    UNDO = enum.auto()
    REPLAY = enum.auto()
    HINT = enum.auto()
    SOLVE = enum.auto()

_cmd_history = []

def parse_cmd(cin:str) -> (str, [int]):
    ''' there a small set of commands, see SolActs
    '''
    _cmd_history.append(cin) # figure what to do here later
    if not cin:
        return None, None
    parts = cin.strip().split()
    #print(f'PC:{cin=}, {parts=}')
    if not parts:
        return None, parts
    positions = []
    cmd = parts[0]
    for i, param in enumerate(parts[1:], start=1):
        if not parts[i].isdigit():
            return None, parts
        pos = int(parts[i])
        if pos > 7 or pos < 1:
            return None, parts
        positions.append(int(parts[i]))
    else:
        positions.append(-1)
    return cmd, positions

def get_cmd() -> (str, int):
    cin = input('Enter a command (type "h" for help): ')
    return parse_cmd(cin)


def parse_sol_cmds(input_cmd: ty.Callable[[None], str]=get_cmd) -> [str, int]:
    ''' gemini then modified
    Parses a Solitaire command string using regular expressions and match/case.
    Args:
        command_string (str): The command string entered by the user.
    Returns:
        tuple: A tuple containing (cmd_type, arg) if parsed successfully,
           otherwise (None, None).
           command_type (str):
           The recognized command (e.g., 'new_deal', 'stock_to_waste').
           args (dict): A dictionary of arguments, e.g., {'tableau_col': 3} or
                        {'tableau_col1': 1, 'tableau_col2': 5}.
    '''
    # Normalize the command string by stripping whitespace and splitting
    # into parts
    # This prepares it for pattern matching
    print(f'PSC:{input_cmd=}', flush=True)
    cmd, positions = input_cmd()
    print(f'PSC:{cmd=}, {positions=}', flush=True)

    # Use match/case for pattern matching
    match cmd:
        case 'N':
            return NEW_DEAL, positions
        case 'n':
            return STOCK_TO_WASTE, positions
        case 'wt':
            if len(positions) != 1:
                # log the error
                return NONE, NONE
            return WASTE_TO_TABLEAU, positions
        case 'tf':
            if len(positions) != 1:
                # log error
                return None, None
            return TABLEAU_TO_FOUNDATION, positions
        case 'tt':
            if len(positions) != 2:
                # log error
                return None, None
            return TABLEAU_TO_TABLEAU, positions
        case 'u':
            return UNDO, positions
        case 'h':
            return HELP, positions
        case 'q':
            return QUIT, positions

        case _: # Default case for no match, 
            return None, None

# --- Example Usage ---
if __name__ == '__main__':
    _cmds = [
        'N',
        'n',
        'h',
        'q',
        'u',
        'wt 3',
        'tf 7',
        'tt 1 5',
        'invalid command',
        'wt   5', # Test extra spaces
        '', # Empty string
        ' ', # Just spaces
    ]
    _finished = False
    def get_test_cmds():
        ''' read the _cmds list and pass to caller one at a time
        '''
        for cmdin in _cmds:
            #print(f'GTC:{cmdin=}')
            cmd, positions = parse_cmd(cmdin)
            #print(f'GTC:{cmd=}, {positions=}')
            yield (cmd, positions)
        _finished = True
        return None, None

    for cmd, positions in get_test_cmds():
        print(f'gtc: {cmd=}, {positions=}')
    sys.exit(0)

    print('Parsing Solitaire Commands (with match/case):')
    print('----------------------------')
    #for things in parse_sol_cmds(get_test_cmds):
    #    print(f'X{things=}')
    #sys.exit(0)
    for cmd, positions in parse_sol_cmds(get_test_cmds()):
        if cmd:
            print(f'{cmd=}: {positions=}')
        else:
            print(f'"{cmd=}" -> Could not parse.')
            if _finished:
                break
    print('----------------------------')


