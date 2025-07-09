#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#

''' Module for parsing solitaire commands, and keeping the history
    of the game.
'''

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
    EMPTY = 0
    NEW_DEAL = enum.auto()
    STOCK_TO_WASTE = enum.auto()
    WASTE_FOUNDATION = enum.auto()
    WASTE_TO_TABLEAU = enum.auto()
    TABLEAU_TO_FOUNDATION = enum.auto()
    TABLEAU_TO_TABLEAU = enum.auto()
    FOUNDATION_TO_TABLEAU = enum.auto()
    UNDO = enum.auto()
    HELP = enum.auto()
    REPLAY = enum.auto()
    HINT = enum.auto()
    SOLVE = enum.auto()
    QUIT = enum.auto()
    INVALID = enum.auto()

class CmdInfo(object):
    def __init__(self, cmd: str, cargs: ty.List, definition: str):
        self._cmd = cmd
        self._cargs = cargs
        self._definition = definition

    @property
    def cmd(self) -> str:
        return self._cmd

    @property
    def cargs(self) -> str:
        if not self._cargs:
            return ''
        return f' {" ".join(self._cargs)}'

    @property
    def definition(self) -> str:
        return self._definition


_cmd_content_map = {
    SolActs.NEW_DEAL: 'n',
    SolActs.STOCK_TO_WASTE: 'm',
    SolActs.WASTE_FOUNDATION: 'w',
    SolActs.WASTE_TO_TABLEAU: 'w',
    SolActs.TABLEAU_TO_FOUNDATION: 't',
    SolActs.TABLEAU_TO_TABLEAU: 't',
    SolActs.FOUNDATION_TO_TABLEAU : 'f',
    SolActs.UNDO: 'u',
    SolActs.REPLAY: 'r',
    SolActs.HINT: 'h',
    SolActs.SOLVE: 's',
    SolActs.QUIT: 'q',
    SolActs.HELP: '?',
    SolActs.INVALID: '',
}

class SolCmd(object):
    ''' A representation of a solitaire command
        Used to implement a command, to store in history for undo
        and used for saving a game or replay or debug
    '''
    def __init__(self, cmd: SolActs, cargs: ty.List[int]):
        self._cmd = cmd
        self._cargs = cargs

    @property
    def cmd(self) -> SolActs:
        return self._cmd

    @property
    def cargs(self) -> ty.List[int]:
        return self._cargs

    @property
    def cmd_str(self) -> str:
        return _cmd_content_map[self._cmd]

    def __str__(self):
        return f'{self._cmd}:{self._cargs}'


# each entry has a SolActs index and tuple with (num pos, help)
_cmd_info_map = {
    SolActs.EMPTY: CmdInfo('', [], ''),
    SolActs.NEW_DEAL: CmdInfo('N', [], 'New Deal'),
    SolActs.STOCK_TO_WASTE: CmdInfo('m', [],  'Move Card Stock to Waste'),
    SolActs.WASTE_FOUNDATION: CmdInfo('w', [], 'Waste to Foundation'),
    SolActs.WASTE_TO_TABLEAU: CmdInfo('w', ['C'],
                               'Move from Waste to Tableau[C]'),
    SolActs.TABLEAU_TO_FOUNDATION: CmdInfo('t', ['C'],
                                    'Move Tableau[C] to Foundation'),
    SolActs.TABLEAU_TO_TABLEAU: CmdInfo('t', ['C1', 'C2'],
                                 'Move Tableau[C1] to Tableau[C2]'),
    SolActs.FOUNDATION_TO_TABLEAU : CmdInfo('f', ['S', 'C'],
                                    'foundation[S] to tableau[C]'),
    SolActs.UNDO: CmdInfo('u', [], 'Undo last move'),
    SolActs.REPLAY: CmdInfo('r', [], 'Replay the same/last game'),
    SolActs.HINT: CmdInfo('h', [], 'Hint'),
    SolActs.SOLVE: CmdInfo('s', [], 'Solve -- what does this mean?'),
    SolActs.QUIT: CmdInfo('q', [], 'Quit -- leave game\n'),
    SolActs.HELP: CmdInfo('?', [], 'Help -- this msg'),
    SolActs.INVALID: CmdInfo('', [], 'Invalid Commnad'),
}

# command characteristic sets
_no_param_set = {'n', 'u', '?', 'r', 'h', 's', 'q', 'w'}
_one_param_set = {'m', 'w', 't'}
_zero_or_one_set = _no_param_set & _one_param_set
_two_param_set = {'t'}
_cmd_set = _no_param_set | _one_param_set | _two_param_set 


def create_sol_help() -> str:
    ''' using the command map (_cmd_info_map) create a help listing
    '''
    parts = []
    for act in SolActs:
        if act in [SolActs.EMPTY, SolActs.INVALID]:
            #print(f'skip {act}')
            continue
        #print(f'get {act}')
        ci = _cmd_info_map[act] # get the CmdInfo
        parts.append(f'{ci.cmd}{ci.cargs} - {ci.definition}\n')
    return ''.join(parts)


_cmd_history: ty.List[SolCmd] = []

def history_append(cmd: CmdInfo) ->  None:
    ''' append to the history to allow the undo command and to 
        save game state.
    Args:
        cmd: is a CmdInfo object
    '''
    global _cmd_history
    _cmd_history.append(cmd)


def history_op() -> ty.Optional[CmdInfo]:
    global _cmd_history
    return  _cmd_history.pop(-1) if _cmd_history else None


def parse_cmd(cin:str) -> SolCmd:
    ''' there a small set of commands, see _cmd_set
    Each command is a starts with a single charater in the _cmd_set.
    w and t command take 0, 1, or 2 paramters which reresent column
    number.  The user enters columns: 1 >= C <= 7, which we map to [0, 6]
    Returns:
        SolCmd with (cmd, posistions), where cmd is in _cmd_set and
            positions can be [], [C], or [C1, C2] where C is a column #
    '''
    _cmd_history.append(cin) # figure what to do here later
    if not cin:
        return None, []
    parts = cin.strip().split()
    if not parts:
        return None, []
    positions = []
    cmd = parts[0].strip()
    if cmd not in _cmd_set:
        None, parts
    if cmd in _no_param_set and not cmd in _zero_or_one_set:
        if parts[1:]: # if there are parts the syntax was incorrect
            print(f'pc-bad-parts: {parts}')
            return None, parts
        return cmd, positions
    for i, param in enumerate(parts[1:], start=1):
        pi = parts[1].strip()
        if not pi.isdigit(): # only single digits allowed
            # If a non-digit parameter is found, it's an invalid command
            print(f'pc-not-dig: {i} -> {pi}')
            return None, parts
        # now we can convert to an integer
        pos = int(parts[i]) - 1 # zero  base index
        #print(f'pc: {i} -> {pos}')
        if pos > 6 or pos < 0: # check column range form 1 to 7
            print(f'pc-bad-pos: {i} -> {parts}')
            # If position is out of range, it's an invalid command
            return None, parts
        positions.append(int(pos))
    #print(f'PC: {cmd}, {positions}')
    return cmd, positions

def get_cmd() -> ty.Tuple[SolActs, ty.List[int]]:
    cin = input('Enter a command (type "?" or <enter> help): ')
    #print(f'GC: {cin=}')
    return parse_cmd(cin)

class InvalidCmd(Exception):
    def __init__(self, msg):
        super().__init__(self, msg)

def parse_sol_cmds(input_cmd: ty.Callable[[],
                   ty.Tuple[str | None, ty.List[int]]] = get_cmd) \
                    -> SolCmd:
    ''' Parses a Solitaire command string using regular expressions
        and match/case.
    Args:
        input_cmd (callable): A function that returns a tuple (command_str, positions_list).
                              Defaults to get_cmd for interactive input.
    Returns:
        SolCmd: contains (cmd_type, arg) if parsed successfully,
           otherwise (SolActs.INVALID, positions).
           command_type (SolActs): The recognized command (e.g., SolActs.NEW_DEAL).
           args (list[int]): A list of integer arguments (positions).
    '''
    cmd, positions = input_cmd()

    #print(f'PSC: {cmd=} {positions=}') # Uncomment for debugging

    action = SolActs.EMPTY
    match cmd:
        case 'N':
            action = SolActs.NEW_DEAL
        case 'm':
            action = SolActs.STOCK_TO_WASTE
        case 'w':
            print(f'W: {positions=}')
            if len(positions) == 0:
                action = SolActs.WASTE_FOUNDATION
            elif len(positions) == 1:
                action = SolActs.WASTE_TO_TABLEAU
            else:
                action = SolActs.INVALID
        case 't':
            if len(positions) == 1:
                action = SolActs.TABLEAU_TO_FOUNDATION
            elif len(positions) == 2:
                action = SolActs.TABLEAU_TO_TABLEAU
            elif len(positions) == 3:
                # I think specifying the two lists makes the move unique
                action = SolActs.TABLEAU_TO_TABLEAU
            else:
                action = SolActs.INVALID
        case 'u':
            action = SolActs.UNDO
        case 'r':
            action = SolActs.REPLAY
        case 's':
            action = SolActs.SOLVE
        case 'h':
            action = SolActs.HINT
        case '?':
            action = SolActs.HELP
        case 'q':
            action = SolActs.QUIT
        case _: # Default case for no match, or if cmd is None from parse_cmd
            raise InvalidCmd(f'Invalid commnd: {cmd}, {positions}')
    r = SolCmd(action, positions)
    history_append(r)
    return r


# --- Example Usage (Test Code) ---
if __name__ == '__main__':
    _cmds_strings = [
        'n',
        'm 4',
        'm 1',
        '?',
        'u',
        'w 3',
        't 7',
        't 1 5',
        'h',
        'invalid command',
        'w   5', # Test extra spaces
        '', # Empty string
        ' ', # Just spaces
        'N 1', # Test invalid parameter for 'N'
        'w 8', # Test out of range position
        'q 1',
        'q 1',
    ]

    # Create an iterator from your list of command strings
    _test_cmd_iterator = iter(_cmds_strings)
    _finished = False

    # Define a callable function that simulates get_cmd by yielding
    # the next test command
    def get_test_commands() -> ty.Tuple[SolActs, ty.List[int]]:
        global _finished
        try:
            # Get the next raw command string from our test list
            cmd_str = next(_test_cmd_iterator)
            # Parse it using your existing parse_cmd function
            parsed_cmd = parse_cmd(cmd_str)
            #print(f'gtcs: {parsed_cmd[0]}, {parsed_cmd[1]} -> ', end='')
            return parsed_cmd
        except InvalidCmd as e_ic:
            print(e_ic)
            return None, []
        except StopIteration:
            # When the iterator is exhausted, indicate end of commands
            #print('GTcmds: End of test commands.')
            # This can be a special value or just let the main loop handle
            # the StopIteration.
            # For this setup, returning (None, []) will let 
            # parse-sol-cmds return INVALID.
            _finished = True
            return None, []

    def get_manual_test_command() -> ty.Tuple[SolActs, ty.List[int]]:
        cin = input('test cmd: ')
        parsed_cmd = parse_cmd(cin)
        #print(f'GTC: {parsed_cmd}')
        return parsed_cmd
        

    print('Parsing Solitaire Commands:')
    print(create_sol_help())
    print('----------------------------')

    while True:
        try:
            sol_cmd = parse_sol_cmds(get_manual_test_command)
        except InvalidCmd as e_ic:
            print(e_ic)
            continue
        print(f'Man:{sol_cmd}')
        if sol_cmd.cmd == SolActs.QUIT:
            break;
    # Loop indefinitely, calling parse-sol-cmds with our simulator
    # until we explicitly break or the simulator signals end of input.
    while not _finished:
        # Call parse_sol_cmds, passing our simulator as the
        # input-cmd callable.
        # This will internally call get_cmd() each time it needs input.
        try:
            sol_cmd = parse_sol_cmds(get_test_commands)
        except InvalidCmd as e_ic:
            print(e_ic)
            continue
        print(f'SIM: {sol_cmd}')

        # Stop the test loop if the QUIT command is processed or if the simulator
        # signals that it's out of commands (by returning None for the command string).
        if sol_cmd.cmd == SolActs.QUIT and not sol_cmd.positions:
            break
        #input('ret:')
    print('----------------------------')

