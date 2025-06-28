#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#

import argparse
import functools as ft
import random
import re
import sys
import typing as ty

def parse_solitaire_command(command_string):
    """
    Parses a Solitaire command string using regular expressions.

    Args:
        command_string (str): The command string entered by the user.

    Returns:
        tuple: A tuple containing (command_type, args) if parsed successfully,
               otherwise (None, None).
               command_type (str):
                The recognized command (e.g., 'new_deal', 'stock_to_waste').
               args (dict):
                A dictionary of arguments, e.g., {'tableau_col': 3} or
                            {'tableau_col1': 1, 'tableau_col2': 5}.
    """

    # Regex patterns for each command type.
    # Using named capture groups for clarity and easy access to arguments.
    # re.IGNORECASE is used to match 'N'/'n', 'H'/'h', 'Q'/'q', 'U'/'u' case-insensitively.

    # New Deal: N
    new_deal = re.compile(r"^(N)$", re.IGNORECASE)

    # Stock to Waste: n
    stock_to_waste = re.compile(r"^(n)$") # 'n' is case-sensitive as per menu

    # Waste to Tableau: wt #T
    waste_to_tableau = re.compile(r"^(wt)\s+(?P<tableau_col>\d+)$", re.IGNORECASE)

    # Tableau to Foundation: tf #T
    tableau_to_foundation = re.compile(r"^(tf)\s+(?P<tableau_col>\d+)$", re.IGNORECASE)

    # Tableau to Tableau: tt #T1 #T2
    tableau_to_tableau = re.compile(r"^(tt)\s+(?P<tableau_col1>\d+)\s+(?P<tableau_col2>\d+)$", re.IGNORECASE)

    # Undo: u
    undo = re.compile(r"^(u)$", re.IGNORECASE)

    # Help: h
    help_pat= re.compile(r"^(h)$", re.IGNORECASE)

    # Quit: q
    quit_pat = re.compile(r"^(q)$", re.IGNORECASE)


    # Attempt to match the command string against each pattern
    if new_deal_match := new_deal.match(command_string.strip()):
        return "new_deal", {}
    elif stock_to_waste_match := stock_to_waste.match(command_string.strip()):
        return "stock_to_waste", {}
    elif waste_to_tableau_match := waste_to_tableau.match(command_string.strip()):
        # Convert captured group to int
        return "waste_to_tableau", {"tableau_col": int(waste_to_tableau_match.group("tableau_col"))}
    elif tableau_to_foundation_match := tableau_to_foundation.match(command_string.strip()):
        # Convert captured group to int
        return "tableau_to_foundation", {"tableau_col": int(tableau_to_foundation_match.group("tableau_col"))}
    elif tableau_to_tableau_match := tableau_to_tableau.match(command_string.strip()):
        # Convert captured groups to int
        return ("tableau_to_tableau",
                {"tableau_col1": int(tableau_to_tableau_match.group("tableau_col1")),
                 "tableau_col2": int(tableau_to_tableau_match.group("tableau_col2"))})
    elif undo_match := undo.match(command_string.strip()):
        return "undo", {}
    elif help_match := help_pat.match(command_string.strip()):
        return "help", {}
    elif quit_match := quit_path.match(command_string.strip()):
        return "quit", {}
    else:
        return None, None

# --- Example Usage ---
if __name__ == "__main__":
    commands = [
        "N",
        "n",
        "h",
        "q",
        "u",
        "wt 3",
        "tf 7",
        "tt 1 5",
        "WT 1",  # Test case-insensitivity
        "TT 2 6", # Test case-insensitivity
        "invalid command",
        "wt   5", # Test extra spaces
        "TF 10", # Test larger numbers
    ]

    print("Parsing Solitaire Commands:")
    print("----------------------------")
    for cmd in commands:
        cmd_type, args = parse_solitaire_command(cmd)
        if cmd_type:
            print(f"Command: '{cmd}' -> Type: {cmd_type}, Args: {args}")
        else:
            print(f"Command: '{cmd}' -> Could not parse.")
    print("----------------------------")


