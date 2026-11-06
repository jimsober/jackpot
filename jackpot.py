#!/usr/bin/env python3

import random
import os
import sys
import math
from itertools import groupby
import json
import logging
from datetime import datetime
import getpass
from enum import IntEnum
import os as _os

from shared_logger import get_logger, _load_config
from high_scores import ensure_high_scores_file

class LogLevel(IntEnum):
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10

class Logger:
    def __init__(self, level: int = LogLevel.INFO):
        self.level = level

    def set_level(self, level: int):
        self.level = level

    def _should(self, level: int) -> bool:
        return int(level) >= int(self.level)

    def debug(self, msg: str):
        if self._should(LogLevel.DEBUG):
            print(f"DEBUG: {msg}")

    def info(self, msg: str):
        if self._should(LogLevel.INFO):
            print(f"INFO: {msg}")

    def warning(self, msg: str):
        if self._should(LogLevel.WARNING):
            print(f"WARNING: {msg}")

    def error(self, msg: str):
        if self._should(LogLevel.ERROR):
            print(f"ERROR: {msg}")

# Configuration persisted in config.json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')


def load_config():
    return _load_config()


def save_config(cfg):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass


CONFIG = load_config()

LOGGER = get_logger("jackpot")


class _ActiveLevel(str):
    @property
    def name(self):
        return str(self)


active_level = _ActiveLevel(logging.getLevelName(LOGGER.getEffectiveLevel()))


def initialize_game(num_players):
    game = {}
    player_bonus = {}
    player = random.randint(1,num_players)
    for i in range(num_players):
        game.update({i:[0, 0, 0]})
        player_bonus.update({i:[0, 0, 0]})
    return game, player_bonus, player

def initialize_rack(num_players):
    rack = []
    for i in range(num_players):
        rack.append([['1 2 3 4 5 6'],['_'], ['_','_'], ['_','_','_'], ['_','_','_','_'],['_','_','_','_','_','_']])
    return rack

def initialize_round(num_players):
    cherry_tiles = 35
    orange_tiles = 28
    bell_tiles = 28
    money_tiles = 21
    h_jkpt = {}
    d_jkpt = {}
    cont_round = {}
    preferences = {}
    for i in range(0,num_players):
        h_jkpt.update({i:False})
        d_jkpt.update({i:False})
        cont_round.update({i:True})
        preferences.update({i:['_','_','_']})
    return h_jkpt, d_jkpt, cont_round, preferences, cherry_tiles, orange_tiles, bell_tiles, money_tiles

LINE_SCORES = {
    'C': {3: 30, 4: 60, 5: 120},
    'O': {3: 40, 4: 80, 5: 160},
    'B': {3: 50, 4: 100, 5: 200},
    'M': {3: 100, 4: 200, 5: 400},
}

TILE_BASE_VALUES = {'M': 100, 'B': 50, 'O': 40, 'C': 30}
TILE_PROBABILITIES = {'C': 0.506, 'O': 0.360, 'B': 0.360, 'M': 0.235}

LINES = [
    ('Row3', [(3, 0), (3, 1), (3, 2)]),
    ('Row4', [(4, 0), (4, 1), (4, 2), (4, 3)]),
    ('Row5', [(5, 0), (5, 1), (5, 2), (5, 3), (5, 4)]),
    ('DL3',  [(3, 0), (4, 1), (5, 2)]),
    ('DL3a', [(5, 0), (4, 1), (3, 2)]),
    ('DL4',  [(2, 0), (3, 1), (4, 2), (5, 3)]),
    ('DL5',  [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)]),
]


def copy_board(board):
    return [row[:] for row in board]


def empty_cells_count(board):
    cnt = 0
    row = 0
    while row < len(board):
        col = 0
        while col < len(board[row]):
            if row == 5 and col == 5:
                pass
            elif board[row][col] == '_':
                cnt += 1
            col += 1
        row += 1
    return cnt


def empty_cells(player):
    return empty_cells_count(rack[player-1])


def get_valid_cols(board):
    valid_col = []
    row = 0
    while row < len(board):
        col = 0
        while col < len(board[row]):
            if board[row][col] == '_':
                if (col + 1) not in valid_col:
                    valid_col.append(col + 1)
            col += 1
        row += 1
    return valid_col


def drop_tile(board, col_1_indexed, tile):
    if col_1_indexed == 6:
        if board[5][5] == '_':
            board[5][5] = tile
            return True, 5, 5
        return False, -1, -1
    col = col_1_indexed - 1
    if col < 0 or col > 4:
        return False, -1, -1
    for row in range(5, col, -1):
        if board[row][col] == '_':
            board[row][col] = tile
            return True, row, col
    return False, -1, -1


def score_board(board):
    score = 0
    jackpot_H = False
    jackpot_D = False

    # Horizontal consecutive tiles
    L3 = [board[3][c] for c in range(3)]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(L3)]:
        if count == 3 and tile in LINE_SCORES:
            score += LINE_SCORES[tile][3]

    L4 = [board[4][c] for c in range(4)]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(L4)]:
        if count in (3, 4) and tile in LINE_SCORES:
            score += LINE_SCORES[tile][count]

    L5 = [board[5][c] for c in range(5)]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(L5)]:
        if count in (3, 4, 5) and tile in LINE_SCORES:
            score += LINE_SCORES[tile][count]
            if count == 5:
                jackpot_H = True

    # Diagonal consecutive tiles
    DL3 = [board[3][0], board[4][1], board[5][2]]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(DL3)]:
        if count == 3 and tile in LINE_SCORES:
            score += LINE_SCORES[tile][3]

    DL3a = [board[5][0], board[4][1], board[3][2]]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(DL3a)]:
        if count == 3 and tile in LINE_SCORES:
            score += LINE_SCORES[tile][3]

    DL4 = [board[2][0], board[3][1], board[4][2], board[5][3]]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(DL4)]:
        if count in (3, 4) and tile in LINE_SCORES:
            score += LINE_SCORES[tile][count]

    DL5 = [board[1][0], board[2][1], board[3][2], board[4][3], board[5][4]]
    for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(DL5)]:
        if count in (3, 4, 5) and tile in LINE_SCORES:
            score += LINE_SCORES[tile][count]
            if count == 5:
                jackpot_D = True

    # Rack bonus
    counts = {'C': 0, 'O': 0, 'B': 0, 'M': 0}
    for r in range(1, 6):
        for c in range(len(board[r])):
            if r == 5 and c == 5:
                continue
            tile = board[r][c]
            if tile in counts:
                counts[tile] += 1

    cherry_cnt = counts['C']
    orange_cnt = counts['O']
    bell_cnt = counts['B']
    money_cnt = counts['M']

    if cherry_cnt >= 9 or orange_cnt >= 9 or bell_cnt >= 9 or money_cnt >= 9:
        score += 100
    elif cherry_cnt == 8:
        score += 70
        if orange_cnt == 7 or bell_cnt == 7 or money_cnt == 7:
            score += 50
    elif orange_cnt == 8:
        score += 70
        if cherry_cnt == 7 or bell_cnt == 7 or money_cnt == 7:
            score += 50
    elif bell_cnt == 8:
        score += 70
        if cherry_cnt == 7 or orange_cnt == 7 or money_cnt == 7:
            score += 50
    elif money_cnt == 8:
        score += 70
        if cherry_cnt == 7 or orange_cnt == 7 or bell_cnt == 7:
            score += 50
    elif cherry_cnt == 7:
        score += 50
        if orange_cnt == 7 or bell_cnt == 7 or money_cnt == 7:
            score += 50
    elif orange_cnt == 7:
        score += 50
        if cherry_cnt == 7 or bell_cnt == 7 or money_cnt == 7:
            score += 50
    elif bell_cnt == 7:
        score += 50
        if cherry_cnt == 7 or orange_cnt == 7 or money_cnt == 7:
            score += 50
    elif money_cnt == 7:
        score += 50
        if cherry_cnt == 7 or orange_cnt == 7 or bell_cnt == 7:
            score += 50

    return score, jackpot_H, jackpot_D


def rack_score(player):
    return score_board(rack[player-1])

def print_rack(h, d, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    os.system('clear')
    total = []
    for i in range(num_players):
        total.append(0)
        i += 1
    print("Round", end = ' ')
    for i in range(len(game)):
        print(" Player %s" % str(i+1), end = ' ')
    print("\r")
    for rnd in range(3):
        print(" "*3, str(rnd+1), end = ' ')
        for plr in range(len(game)):
            print(" "*(8 - len(str(game[plr][rnd]))), str(game[plr][rnd]), end = ' ')
            total[plr] += game[plr][rnd]
        print("\r")
        print(" "*5, end = ' ')
        for plr in range(len(game)):
            print(" "*(8 - len(str(player_bonus[plr][rnd]))), str(player_bonus[plr][rnd]), end = ' ')
            total[plr] += player_bonus[plr][rnd]
        print("\r")
    print("Total", end = ' ')
    for plr in range(len(game)):
        print(" "*(8 - len(str(total[plr]))), str(total[plr]), end = ' ')
    print("\r")
    print()
    for i in range(cherry_tiles):
        colorize("C")
        print(" ", end = '')
    print("\r")
    for i in range(orange_tiles):
        colorize("O")
        print(" ", end = '')
    print("\r")
    for i in range(bell_tiles):
        colorize("B")
        print(" ", end = '')
    print("\r")
    for i in range(money_tiles):
        colorize("M")
        print(" ", end = '')
    print("\r")
    print()
    print("Round %s > Player %s"  % (str(round), str(player)))
    print()
    row = 0
    while row < len(rack[player-1]):
        col = 0
        while col < len(rack[player-1][row]):
            if rack[player-1][row][col] == "C":
                colorize(rack[player-1][row][col])
                print(" ", end = '')
            elif rack[player-1][row][col] == "O":
                colorize(rack[player-1][row][col])
                print(" ", end = '')
            elif rack[player-1][row][col] == "B":
                colorize(rack[player-1][row][col])
                print(" ", end = '')
            elif rack[player-1][row][col] == "M":
                colorize(rack[player-1][row][col])
                print(" ", end = '')
            else:
                print(rack[player-1][row][col], end = ' ')
            col += 1
        print("\r")
        row += 1
    print()
    score_results = rack_score(player)
    score = score_results[0]
    jackpot_H = score_results[1]
    jackpot_D = score_results[2]
    game[player-1][round-1] = score
    print("Score: " + str(score))
    print()
    if jackpot_H and not h[player-1]:
        sound_bell()
        print("Jackpot!!!")
        print()
        LOGGER.info(f"Player {player} hit horizontal jackpot")
        input("Press any key to continue.")
        print()
        h[player-1] = True
    elif jackpot_D and not d[player-1]:
        sound_bell()
        print("Jackpot!!!")
        print()
        LOGGER.info(f"Player {player} hit diagonal jackpot")
        input("Press any key to continue.")
        print()
        d[player-1] = True

    return h, d

def score_rack(round, rack, game, player_bonus, forfeit):
    os.system('clear')
    total = []
    for i in range(num_players):
        total.append(0)
    print("Round", end = ' ')
    for i in range(len(game)):
        print(" Player %s" % str(i+1), end = ' ')
    print("\r")
    for rnd in range(3):
        print(" "*3, str(rnd+1), end = ' ')
        for plr in range(len(game)):
            print(" "*(8 - len(str(game[plr][rnd]))), str(game[plr][rnd]), end = ' ')
            total[plr] += game[plr][rnd]
        print("\r")
        print(" "*5, end = ' ')
        for plr in range(len(game)):
            print(" "*(8 - len(str(player_bonus[plr][rnd]))), str(player_bonus[plr][rnd]), end = ' ')
            total[plr] += player_bonus[plr][rnd]
        print("\r")
    print("Total", end = ' ')
    for plr in range(len(game)):
        print(" "*(8 - len(str(total[plr]))), str(total[plr]), end = ' ')
    print("\r")
    print()
    for i in range(cherry_tiles):
        colorize("C")
        print(" ", end = '')
    print("\r")
    for i in range(orange_tiles):
        colorize("O")
        print(" ", end = '')
    print("\r")
    for i in range(bell_tiles):
        colorize("B")
        print(" ", end = '')
    print("\r")
    for i in range(money_tiles):
        colorize("M")
        print(" ", end = '')
    print("\r")
    print()
    print("Round %s > All Players"  % str(round))
    print()
    for row in range(6):
        for plr in range(len(game)):
            col = 0
            while col < len(rack[plr-1][row]):
                if rack[plr][row][col] == "C":
                    colorize(rack[plr][row][col])
                    print(" ", end = '')
                elif rack[plr][row][col] == "O":
                    colorize(rack[plr][row][col])
                    print(" ", end = '')
                elif rack[plr][row][col] == "B":
                    colorize(rack[plr][row][col])
                    print(" ", end = '')
                elif rack[plr][row][col] == "M":
                    colorize(rack[plr][row][col])
                    print(" ", end = '')
                else:
                    print(rack[plr][row][col], end = '')
                    print(" ", end = '')
                col += 1
            print(" "*3, end = ' ')
            if 1 <= row <= 4:
                print(" "*(11-(2*row)), end = ' ')
        print("\r")
    print()
    for plr in range(len(game)):
        print("Player %s" % str(plr+1), end = ' ')
        print(" "*6, end = ' ')
    print("\r")
    if round < 3 and not forfeit:
        forfeit = input("Press <Enter> to begin round %s or Q to quit. " % str(round+1))
        if forfeit.upper() == 'Q':
            LOGGER.info("User chose to quit during round score screen")
            forfeit = True
    return forfeit

def col_choices(player):
    return get_valid_cols(rack[player-1])

def roll_dice():
    dice = []
    tile_choices = []
    double_tiles = False
    empty_pit = False
    cherry_cnt = 0
    orange_cnt = 0
    bell_cnt = 0
    money_cnt = 0
    white_dice = [random.randint(1,6), random.randint(1,6)]
    yellow_dice = [random.randint(1,6), random.randint(1,6)]
    for die in white_dice:
        if die == 1 or die == 4:
            dice.append("O")
            orange_cnt += 1
        elif die == 2 or die == 5:
            dice.append("B")
            bell_cnt += 1
        elif die == 3:
            dice.append("C")
            cherry_cnt += 1
        elif die == 6:
            dice.append("M")
            money_cnt += 1
    for die in yellow_dice:
        if die == 1 or die == 3 or die == 5:
            dice.append("C")
            cherry_cnt += 1
        elif die == 2:
            dice.append("O")
            orange_cnt += 1
        elif die == 4:
            dice.append("B")
            bell_cnt += 1
        elif die == 6:
            dice.append("M")
            money_cnt += 1
    if cherry_cnt == 4 or orange_cnt == 4 or bell_cnt == 4 or money_cnt == 4:
        double_tiles = True
        empty_pit = True
        tile_choices = ["C", "O", "B", "M"]
    elif cherry_cnt == 3:
        empty_pit = True
        tile_choices = ["C"]
    elif orange_cnt == 3:
        empty_pit = True
        tile_choices = ["O"]
    elif bell_cnt == 3:
        empty_pit = True
        tile_choices = ["B"]
    elif money_cnt == 3:
        empty_pit = True
        tile_choices = ["M"]
    elif cherry_cnt == 2:
        tile_choices.append("C")
        if orange_cnt == 2:
            tile_choices.append("O")
        elif bell_cnt == 2:
            tile_choices.append("B")
        elif money_cnt == 2:
            tile_choices.append("M")
    elif orange_cnt == 2:
        tile_choices.append("O")
        if bell_cnt == 2:
            tile_choices.append("B")
        elif money_cnt == 2:
            tile_choices.append("M")
    elif bell_cnt == 2:
        tile_choices.append("B")
        if money_cnt == 2:
            tile_choices.append("M")
    elif money_cnt == 2:
        tile_choices = ["M"]
    elif cherry_cnt == 1 and orange_cnt == 1 and bell_cnt == 1 and money_cnt == 1:
        tile_choices = ["C", "O", "B", "M"]
    return dice, tile_choices, double_tiles, empty_pit

def pit_tile(player, round, choices, valid_cols, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles, doubles=None):
    if doubles is None:
        doubles = globals().get('doubles', False)
    print("Your tile selection: ", end = '')
    colorize(choices)
    print("\r")
    print()
    LOGGER.info(f"Player {player} pit options: current={rack[player-1][5][5]}, choices={choices}")
    input_err = True
    while input_err:
        use_pit = input("Use (U), Remove (R), or Swap (S) pit tile ['%s'] or Not (N)? " % rack[player-1][5][5])
        print()
        if use_pit.upper() == "U":
            LOGGER.info(f"Player {player} uses pit tile {rack[player-1][5][5]}")
            input_err = False
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(rack[player-1][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            undo_tile = rack[player-1][5][5]
            rack[player-1][5][5] = '_'
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, undo_tile, valid_cols, empty_cells(player), True, True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            if undo:
                input_err = True
                rack[player-1][5][5] = undo_tile
            else:
                valid_cols = col_choices(player)
                (h_jkpt, d_jkpt) = print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                if empty_cells(player) > 0:
                    print("Your roll: ", end = '')
                    colorize(roll)
                    print("\r")
                    print()
                    if doubles and empty_cells(player) > 0:
                        sound_bell()
                        print("Doubles!")
                        print()
        elif use_pit.upper() == "R":
            LOGGER.info(f"Player {player} removes pit tile {rack[player-1][5][5]}")
            input_err = False
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(rack[player-1][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            rack[player-1][5][5] = '_'
            valid_cols = col_choices(player)
            (h_jkpt, d_jkpt) = print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            print("Your roll: ", end = '')
            colorize(roll)
            print("\r")
            print()
            if doubles:
                sound_bell()
                print("Doubles!")
                print()
        elif use_pit.upper() == "S":
            input_err = False
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(rack[player-1][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            swap = True
            if len(choices) == 1:
                rack[player-1][5][5] = choices[0]
                LOGGER.info(f"Player {player} swaps pit tile with {choices[0]}")
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(choices[0], 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            else:
                sel_input_err = True
                while sel_input_err:
                    print("Select a tile from ")
                    colorize(choices)
                    selection = input(": ")
                    print()
                    if selection.upper() in choices:
                        rack[player-1][5][5] = selection.upper()
                        LOGGER.info(f"Player {player} swaps pit tile with {selection.upper()}")
                        sel_input_err = False
                    else:
                        sound_bell()
                        LOGGER.warning("Invalid pit swap selection")
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(selection.upper(), 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        elif use_pit.upper() == "N":
            LOGGER.info(f"Player {player} keeps pit tile as is")
            input_err = False
        else:
            sound_bell()
            LOGGER.warning(f"Invalid input for pit tile action: {use_pit}")
    return valid_cols, h_jkpt, d_jkpt, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def select_tiles(player, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    undo = False
    if len(choices) == 1 and swap == False:
        if check_supply(choices[0]):
            print("Your tile selection is ['", end = '')
            colorize(choices[0])
            print("'].")
            print()
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, choices[0], valid_cols, empty_cells(player), False, False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        else:
            undo = False
            sound_bell()
            LOGGER.warning(f"Tile {choices[0]} not available in supply")
            print("All of the ['", end = ' ')
            colorize(choices[0])
            input("'] tiles are currently in play. Press any key to continue. ")
            input("All of the ['%s'] tiles are currently in play. Press any key to continue." % str(choices[0]))
            print()
    elif len(choices) > 1 and swap == False:
        for choice in choices:
            if not check_supply(choice):
                choices.remove(choice)
        if len(choices) == 1:
            print("Your tile selection is ['", end = '')
            colorize(choices[0])
            print("'].")
            print()
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, choices[0], valid_cols, empty_cells(player), False, False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        else:
            sel_input_err = True
            while sel_input_err:
                print("Select a tile from ", end = ' ')
                colorize(choices)
                selection = input(": ")
                print()
                if selection.upper() in choices:
                    sel_input_err = False
                    if check_supply(selection.upper()):
                        undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, selection.upper(), valid_cols, empty_cells(player), True, False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    else:
                        sound_bell()
                        LOGGER.warning(f"Tile {selection.upper()} not available in supply")
                        print("All of the ['", end = ' ')
                        colorize(selection.upper())
                        input(" tiles are currently in play. Press any key to continue. ")
                        print()
                else:
                    sound_bell()
    elif len(choices) > 1 and swap:
        for choice in choices:
            if not check_supply(choice):
                choices.remove(choice)
        if len(choices) == 1:
            print("Your tile selection is ['", end = '')
            colorize(choices[0])
            print("'].")
            print()
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, choices[0], valid_cols, empty_cells(player), False, False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
    else:
        undo = False
    valid_cols = col_choices(player)
    return valid_cols, undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def place_tile(player, round, h_jkpt, d_jkpt, tile, valid_cols, empty_cells, undoable, place_pit, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    undo = False
    pla_input_err = True
    show_tile_sel = False
    while pla_input_err:
        if len(valid_cols) == 1:
            if show_tile_sel:
                print("Your tile choice: ['", end = '')
                colorize(tile)
                print("']")
                print()
            if undoable:
                do_undo = input("Your column selection is %s. Press <Enter> to continue or Z to undo. " % str(valid_cols[0]))
            else:
                input("Your column selection is %s. Press any key to continue. " % str(valid_cols[0]))
            print()
            if undoable and do_undo.upper() == "Z":
                pla_input_err = False
                undo = True
                LOGGER.info("Placement undone by user")
            else:
                if rack[player-1][5][valid_cols[0] - 1] == '_':
                    rack[player-1][5][valid_cols[0] - 1] = tile
                    LOGGER.info(f"Player {player} placed {tile} in column {valid_cols[0]}")
                    pla_input_err = False
                elif rack[player-1][4][valid_cols[0] - 1] == '_':
                    rack[player-1][4][valid_cols[0] - 1] = tile
                    LOGGER.info(f"Player {player} placed {tile} in column {valid_cols[0]}")
                    pla_input_err = False
                elif rack[player-1][3][valid_cols[0] - 1] == '_':
                    rack[player-1][3][valid_cols[0] - 1] = tile
                    LOGGER.info(f"Player {player} placed {tile} in column {valid_cols[0]}")
                    pla_input_err = False
                elif rack[player-1][2][valid_cols[0] - 1] == '_':
                    rack[player-1][2][valid_cols[0] - 1] = tile
                    LOGGER.info(f"Player {player} placed {tile} in column {valid_cols[0]}")
                    pla_input_err = False
                elif rack[player-1][1][valid_cols[0] - 1] == '_':
                    rack[player-1][1][valid_cols[0] - 1] = tile
                    LOGGER.info(f"Player {player} placed {tile} in column {valid_cols[0]}")
                    pla_input_err = False
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        else:
            if show_tile_sel:
                print("Your tile choice: ['", end = '')
                colorize(tile)
                print("']")
                print()
            if undoable:
                placement = input("Select a column from %s or enter Z to undo: " % valid_cols)
            else:
                placement = input("Select a column from %s: " % valid_cols)
            print()
            if undoable and placement.upper() == "Z":
                pla_input_err = False
                undo = True
                LOGGER.info("Placement undone by user")
            elif placement == "":
                show_tile_sel = True
                sound_bell()
                LOGGER.warning("Empty column selection input")
                print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            else:
                col_strings = []
                for i in valid_cols:
                    col_strings.append(str(i))
                if placement not in col_strings:
                    show_tile_sel = True
                    sound_bell()
                    LOGGER.warning(f"Invalid column selection: {placement}")
                else:
                    placement = int(placement) - 1
                    if rack[player-1][5][placement] == '_':
                        rack[player-1][5][placement] = tile
                        LOGGER.info(f"Player {player} placed {tile} in column {int(placement)+1}")
                        pla_input_err = False
                        undo_place = 5
                    elif rack[player-1][4][placement] == '_':
                        rack[player-1][4][placement] = tile
                        LOGGER.info(f"Player {player} placed {tile} in column {int(placement)+1}")
                        pla_input_err = False
                        undo_place = 4
                    elif rack[player-1][3][placement] == '_':
                        rack[player-1][3][placement] = tile
                        LOGGER.info(f"Player {player} placed {tile} in column {int(placement)+1}")
                        pla_input_err = False
                        undo_place = 3
                    elif rack[player-1][2][placement] == '_':
                        rack[player-1][2][placement] = tile
                        LOGGER.info(f"Player {player} placed {tile} in column {int(placement)+1}")
                        pla_input_err = False
                        undo_place = 2
                    elif rack[player-1][1][placement] == '_':
                        rack[player-1][1][placement] = tile
                        LOGGER.info(f"Player {player} placed {tile} in column {int(placement)+1}")
                        pla_input_err = False
                        undo_place = 1
                    if place_pit:
                        rack[player-1][5][5] = '_'
                print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            if undo or pla_input_err:
                pass
            else:
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                sure = input("Player %s, you have selected column %s. Press <Enter> to continue or Z to undo. " % (str(player), str(int(placement)+1)))
                if sure.upper() == "Z":
                    pla_input_err = True
                    show_tile_sel = True
                    rack[player-1][undo_place][placement] = '_'
                    if place_pit:
                        rack[player-1][5][5] = tile
                    else:
                        cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    LOGGER.info("Placement undone by user confirmation")

    return undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def check_supply(tile):
    result = False
    if tile == "C" and cherry_tiles > 0:
        result = True
    elif tile == "O" and orange_tiles > 0:
        result = True
    elif tile == "B" and bell_tiles > 0:
        result = True
    elif tile == "M" and money_tiles > 0:
        result = True
    return result

def transact(tile, sign, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    if sign.upper() == 'POSITIVE':
        amt = 1
    elif sign.upper() == 'NEGATIVE':
        amt = -1

    if tile == "C":
        cherry_tiles += amt
    elif tile == "O":
        orange_tiles += amt
    elif tile == "B":
        bell_tiles += amt
    elif tile == "M":
        money_tiles += amt

    return cherry_tiles, orange_tiles, bell_tiles, money_tiles

def completion_probability(tile, needed, trials, supply_available):
    if needed <= 0:
        return 1.0
    if needed > trials or needed > supply_available:
        return 0.0
    p = TILE_PROBABILITIES.get(tile, 0.25)
    prob = 0.0
    for i in range(needed, trials + 1):
        prob += math.comb(trials, i) * (p ** i) * ((1.0 - p) ** (trials - i))
    return prob


def evaluate_potential_score(board, supply):
    actual_score, _, _ = score_board(board)
    empty_cells = empty_cells_count(board)

    # Effective remaining trials roughly equal to empty cells
    trials = min(empty_cells, 14)

    # 1. Line potential
    line_evs = []

    for line_name, cells in LINES:
        L = len(cells)
        current_tiles = [board[r][c] for r, c in cells]
        current_line_score = 0
        for tile, count in [(k, sum(1 for _ in g)) for k, g in groupby(current_tiles)]:
            if tile in LINE_SCORES and count in LINE_SCORES[tile]:
                if count >= 3:
                    current_line_score = max(current_line_score, LINE_SCORES[tile][count])

        best_line_ev = 0.0

        for k in range(3, L + 1):
            for start_idx in range(L - k + 1):
                window = current_tiles[start_idx:start_idx + k]
                non_blanks = [t for t in window if t != '_']
                distinct_tiles = set(non_blanks)

                if len(distinct_tiles) == 1:
                    target_tile = non_blanks[0]
                    placed = len(non_blanks)
                    needed = k - placed

                    if needed > 0 and empty_cells >= needed and supply.get(target_tile, 0) >= needed:
                        target_val = LINE_SCORES[target_tile][k]
                        delta = max(0, target_val - current_line_score)
                        prob = completion_probability(target_tile, needed, trials, supply.get(target_tile, 0))
                        ev = delta * prob
                        if ev > best_line_ev:
                            best_line_ev = ev

        if best_line_ev > 0:
            line_evs.append(best_line_ev)

    # Realistic budget: top lines contribute most, capped realistic budget
    line_evs.sort(reverse=True)
    discount_weights = [1.0, 0.60, 0.30]
    line_potential = sum(ev * w for ev, w in zip(line_evs, discount_weights))

    # 2. Rack bonus potential
    rack_bonus_ev = 0.0
    counts = {'C': 0, 'O': 0, 'B': 0, 'M': 0}
    for r in range(1, 6):
        for c in range(len(board[r])):
            if r == 5 and c == 5:
                continue
            t = board[r][c]
            if t in counts:
                counts[t] += 1

    for t, cnt in counts.items():
        avail = min(empty_cells, supply.get(t, 0))
        max_possible = cnt + avail

        if max_possible >= 9 and cnt < 9:
            needed = 9 - cnt
            base = 100 - (70 if cnt == 8 else (50 if cnt == 7 else 0))
            prob = completion_probability(t, needed, trials, avail)
            rack_bonus_ev += base * prob
        elif max_possible >= 8 and cnt < 8:
            needed = 8 - cnt
            base = 70 - (50 if cnt == 7 else 0)
            prob = completion_probability(t, needed, trials, avail)
            rack_bonus_ev += base * prob
        elif max_possible >= 7 and cnt < 7:
            needed = 7 - cnt
            base = 50
            prob = completion_probability(t, needed, trials, avail)
            rack_bonus_ev += base * prob

    # 3. Pit tile value
    pit_tile = board[5][5]
    if pit_tile != '_':
        pit_val = TILE_BASE_VALUES.get(pit_tile, 20) * 0.20
    else:
        # Option value of an empty pit ready to absorb unwanted tiles
        pit_val = 25.0

    return actual_score + line_potential + rack_bonus_ev + pit_val


def get_possible_pit_actions(board, choices, supply, empty):
    pit_tile = board[5][5]
    if pit_tile == '_' or not empty:
        return [None]

    actions = [('KEEP',)]
    actions.append(('REMOVE',))

    # USE in any valid column 1..5
    for col in range(1, 6):
        c = col - 1
        if board[c + 1][c] == '_':
            actions.append(('USE', col))

    # SWAP with any choice from roll that has supply > 0
    for t in set(choices):
        if supply.get(t, 0) > 0:
            actions.append(('SWAP', t))

    return actions


def find_best_play(board, choices, doubles, empty, supply):
    best_eval = -1e9
    best_play = None
    best_final_board = None
    best_final_supply = None

    pit_actions = get_possible_pit_actions(board, choices, supply, empty)

    for pit_act in pit_actions:
        b1 = copy_board(board)
        s1 = supply.copy()

        if pit_act is not None:
            act_type = pit_act[0]
            if act_type == 'KEEP':
                pass
            elif act_type == 'REMOVE':
                pt = b1[5][5]
                b1[5][5] = '_'
                s1[pt] = s1.get(pt, 0) + 1
            elif act_type == 'USE':
                col = pit_act[1]
                pt = b1[5][5]
                b1[5][5] = '_'
                ok, _, _ = drop_tile(b1, col, pt)
                if not ok:
                    continue
            elif act_type == 'SWAP':
                tile = pit_act[1]
                pt = b1[5][5]
                b1[5][5] = tile
                s1[pt] = s1.get(pt, 0) + 1
                s1[tile] -= 1

        if pit_act is not None and pit_act[0] == 'SWAP':
            num_placements = 1 if doubles else 0
        else:
            num_placements = 2 if doubles else 1

        if num_placements == 0:
            val = evaluate_potential_score(b1, s1)
            if val > best_eval:
                best_eval = val
                best_play = (pit_act, [])
                best_final_board = b1
                best_final_supply = s1

        elif num_placements == 1:
            if empty_cells_count(b1) == 0:
                val = evaluate_potential_score(b1, s1)
                if val > best_eval:
                    best_eval = val
                    best_play = (pit_act, [])
                    best_final_board = b1
                    best_final_supply = s1
            else:
                valid_cols = get_valid_cols(b1)
                valid_choices = [t for t in set(choices) if s1.get(t, 0) > 0]
                if not valid_choices or not valid_cols:
                    val = evaluate_potential_score(b1, s1)
                    if val > best_eval:
                        best_eval = val
                        best_play = (pit_act, [])
                        best_final_board = b1
                        best_final_supply = s1
                else:
                    for t in valid_choices:
                        for col in valid_cols:
                            b2 = copy_board(b1)
                            s2 = s1.copy()
                            ok, _, _ = drop_tile(b2, col, t)
                            if ok:
                                s2[t] -= 1
                                tb = 0.001 * TILE_BASE_VALUES.get(t, 0)
                                val = evaluate_potential_score(b2, s2) + tb
                                if val > best_eval:
                                    best_eval = val
                                    best_play = (pit_act, [(t, col)])
                                    best_final_board = b2
                                    best_final_supply = s2

        elif num_placements == 2:
            if empty_cells_count(b1) == 0:
                val = evaluate_potential_score(b1, s1)
                if val > best_eval:
                    best_eval = val
                    best_play = (pit_act, [])
                    best_final_board = b1
                    best_final_supply = s1
            else:
                valid_cols_1 = get_valid_cols(b1)
                valid_choices_1 = [t for t in set(choices) if s1.get(t, 0) > 0]
                if not valid_choices_1 or not valid_cols_1:
                    val = evaluate_potential_score(b1, s1)
                    if val > best_eval:
                        best_eval = val
                        best_play = (pit_act, [])
                        best_final_board = b1
                        best_final_supply = s1
                else:
                    for t1 in valid_choices_1:
                        for col1 in valid_cols_1:
                            b2 = copy_board(b1)
                            s2 = s1.copy()
                            ok1, _, _ = drop_tile(b2, col1, t1)
                            if not ok1:
                                continue
                            s2[t1] -= 1

                            if empty_cells_count(b2) == 0:
                                val = evaluate_potential_score(b2, s2)
                                if val > best_eval:
                                    best_eval = val
                                    best_play = (pit_act, [(t1, col1)])
                                    best_final_board = b2
                                    best_final_supply = s2
                            else:
                                valid_cols_2 = get_valid_cols(b2)
                                valid_choices_2 = [t for t in set(choices) if s2.get(t, 0) > 0]
                                if not valid_choices_2 or not valid_cols_2:
                                    val = evaluate_potential_score(b2, s2)
                                    if val > best_eval:
                                        best_eval = val
                                        best_play = (pit_act, [(t1, col1)])
                                        best_final_board = b2
                                        best_final_supply = s2
                                else:
                                    for t2 in valid_choices_2:
                                        for col2 in valid_cols_2:
                                            b3 = copy_board(b2)
                                            s3 = s2.copy()
                                            ok2, _, _ = drop_tile(b3, col2, t2)
                                            if ok2:
                                                s3[t2] -= 1
                                                tb = 0.001 * (TILE_BASE_VALUES.get(t1, 0) + TILE_BASE_VALUES.get(t2, 0))
                                                val = evaluate_potential_score(b3, s3) + tb
                                                if val > best_eval:
                                                    best_eval = val
                                                    best_play = (pit_act, [(t1, col1), (t2, col2)])
                                                    best_final_board = b3
                                                    best_final_supply = s3

    return best_play, best_eval, best_final_board, best_final_supply


def auto_play(player, rack, preferences, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, empty, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    current_supply = {
        'C': cherry_tiles,
        'O': orange_tiles,
        'B': bell_tiles,
        'M': money_tiles,
    }
    board = rack[player - 1]

    best_play, best_eval, best_final_board, best_final_supply = find_best_play(
        board, choices, doubles, empty, current_supply
    )

    LOGGER.debug(f"robot player {player} selected play: {best_play} with eval score: {best_eval:.2f}")

    if best_play is not None:
        pit_act, placements = best_play

        if pit_act is not None:
            act_type = pit_act[0]
            if act_type == 'REMOVE':
                pt = rack[player - 1][5][5]
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(
                    pt, 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles
                )
                rack[player - 1][5][5] = '_'
                sound_bell()
                print()
                input(f"Player {player} empties pit tile. ")
            elif act_type == 'USE':
                col = pit_act[1]
                pt = rack[player - 1][5][5]
                rack[player - 1][5][5] = '_'
                drop_tile(rack[player - 1], col, pt)
                sound_bell()
                print()
                input(f"Player {player} plays pit tile. ")
            elif act_type == 'SWAP':
                tile = pit_act[1]
                pt = rack[player - 1][5][5]
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(
                    pt, 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles
                )
                rack[player - 1][5][5] = tile
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(
                    tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles
                )
                sound_bell()
                print()
                input(f"Player {player} swaps pit tile. ")

        for tile, col in placements:
            ok, r, c = drop_tile(rack[player - 1], col, tile)
            if ok:
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(
                    tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles
                )
                LOGGER.debug(f"Player {player} placed {tile} in column {col} at ({r}, {c})")

    valid_cols = col_choices(player)
    return valid_cols, rack, preferences, h_jkpt, d_jkpt, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def high_scores(scope, player, score, num_players, round):
    data = ''
    newData = ''
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    if player == 1:
        user_name = getpass.getuser()
    else:
        user_name = "Player "+str(player)

    scores_path = ensure_high_scores_file()

    with open(scores_path) as json_file:
        data = json.load(json_file)
        newData = data.copy()

    if scope == "GAME":
        tieScore = True
        for g in data['highGame']:
            if g['players'] != num_players:
                pass
            else:
                if g['score'] < score:
                    sound_bell()
                    tieScore = False
                    print()
                    print('Congratulations, %s! Your game score of %s is a new %s-player high game score!!!' % (user_name, str(score), str(g['players'])))
                    for i in range(len(newData['highGame'])):
                        if newData['highGame'][i]['players'] == num_players:
                            del newData['highGame'][i]
                            break
                    newData['highGame'].append({
                        'players': num_players,
                        'score': score,
                        'user': user_name,
                        'date': dt_string
                    })
                    with open(scores_path,'w') as outfile:
                        json.dump(newData, outfile)
                elif g['score'] == score and tieScore:
                    print()
                    print('Congratulations, %s! Your game score ties the %s-player high game score of %s by %s on %s!!!' % (user_name, str(g['players']), str(g['score']), g['user'], g['date']))
                    print('Your score must beat this score to be recognized as the new high game score.')
    elif scope == "ROUND":
        tieScore = True
        for r in data['highRound']:
            if r['players'] != num_players:
                pass
            else:
                if r['score'] < score:
                    sound_bell()
                    tieScore = False
                    print()
                    print('Congratulations, %s! Your round score of %s is a new %s-player high round score!!!' % (user_name, str(score), str(r['players'])))
                    for i in range(len(newData['highRound'])):
                        if newData['highRound'][i]['players'] == num_players:
                            del newData['highRound'][i]
                            break
                    newData['highRound'].append({
                        'players': num_players,
                        'score': score,
                        'user': user_name,
                        'date': dt_string
                    })
                    with open(scores_path,'w') as outfile:
                        json.dump(newData, outfile)
                elif r['score'] == score and tieScore:
                    print()
                    print('Congratulations, %s! Your round score ties the %s-player high round score of %s by %s on %s!!!' % (user_name, str(r['players']), str(r['score']), r['user'], r['date']))
                    print('Your score must beat this score to be recognized as the new high round score.')

def colorize(tiles):
    if isinstance(tiles, str):
        if tiles == "C":
            print(u"\u001b[31m" + str(tiles) + u"\u001b[0m", end = '')
        elif tiles == "O":
            print(u"\u001b[38;5;208m" + str(tiles) + u"\u001b[0m", end = '')
        elif tiles == "B":
            print(u"\u001b[34m" + str(tiles) + u"\u001b[0m", end = '')
        elif tiles == "M":
            print(u"\u001b[32m" + str(tiles) + u"\u001b[0m", end = '')
    else:
        tile_cnt = 0
        print("[", end = '')
        for tile in tiles:
            tile_cnt += 1
            print("'", end = '')
            if tile == "C":
                print(u"\u001b[31m" + tile + u"\u001b[0m", end = '')
            elif tile == "O":
                print(u"\u001b[38;5;208m" + tile + u"\u001b[0m", end = '')
            elif tile == "B":
                print(u"\u001b[34m" + tile + u"\u001b[0m", end = '')
            elif tile == "M":
                print(u"\u001b[32m" + tile + u"\u001b[0m", end = '')
            print("'", end = '')
            if tile_cnt < len(tiles):
                print(", ", end = '')
        print("]", end = '')

def sound_bell():
    sys.stdout.write('\a')
    sys.stdout.flush()

if __name__ == "__main__":
    #MAIN PROGRAM
    play_again = True
    
    #game loop
    while play_again:
        os.system('clear')
        LOGGER.info(f"Starting game with log level {active_level.name}")
        players_input_err = True
        while players_input_err:
            num_players = input("Enter number of players (2 - 4): ")
            print()
            if str(num_players) not in ["2", "3", "4"]:
                sound_bell()
                LOGGER.warning(f"Invalid players input: {num_players}")
            else:
                num_players = int(num_players)
                players_input_err = False
                LOGGER.info(f"Players selected: {num_players}")
        game, player_bonus, player = initialize_game(num_players)
        input("Player %s goes first! Press any key to continue. " % str(player))
        LOGGER.info(f"Player {player} will go first")
        forfeit = False
    
        #round loop
        for round in range(1,4):
            if not forfeit:
                rack = initialize_rack(num_players)
                (h_jkpt, d_jkpt, cont_round, preferences, cherry_tiles, orange_tiles, bell_tiles, money_tiles) = initialize_round(num_players)
                LOGGER.info(f"Round {round} start. Supply C={cherry_tiles}, O={orange_tiles}, B={bell_tiles}, M={money_tiles}. Starting player: {player}")
                #
                LOGGER.debug(f"preferences is {preferences}")
                continue_round = False
                for item in cont_round:
                    if cont_round[item]:
                        continue_round = True
                    
                #player loop
                while continue_round and not forfeit:
                    if empty_cells(player) > 0:
                        (h_jkpt, d_jkpt) = print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                        if player == 1:
                            input("Player %s, press any key to roll dice: " % str(player))
                            print()
    
                        #roll dice
                        (roll, choices, doubles, empty) = roll_dice()
                        LOGGER.info(f"Player {player} rolled {roll}; choices={choices}; doubles={doubles}; pitEmpty={empty}")
                        valid_cols = col_choices(player)
                        if player == 1:
                            print("Your roll: ", end = '')
                            colorize(roll)
                            print("\r")
                            print()
                            if doubles:
                                num_plays = 2
                                sound_bell()
                                print("Doubles!")
                                print()
                                LOGGER.info(f"Player {player} rolled doubles")
                            else:
                                num_plays = 1
    
                            #use or remove pit tile
                            swap = False
                            if rack[player-1][5][5] != '_' and empty:
                                sound_bell()
                                print("You have the option to play or remove the pit tile!")
                                print()
                                (valid_cols, h_jkpt, d_jkpt, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles) = pit_tile(player, round, choices, valid_cols, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles, doubles=doubles)
    
                            #select tiles
                            play_cnt = 1
                            while play_cnt <= num_plays:
                                if empty_cells(player) == 0:
                                    play_cnt += 1
                                elif empty_cells(player) > 0:
                                    undo = True
                                    while undo:
                                        valid_cols, undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = select_tiles(player, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                                    play_cnt += 1
                                    print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                        else:
                            if doubles:
                                sound_bell()
                                print("Doubles!", end = ' ')
                                LOGGER.info(f"Player {player} rolled doubles")
                            print("Player "+str(player)+" rolls ", end = '')
                            colorize(roll)
                            print(" resulting in: ", end = '')
                            colorize(choices)
                            input(". ")
                            valid_cols, rack, preferences, h_jkpt, d_jkpt, cherry_tiles, orange_tiles, bell_tiles, money_tiles = auto_play(player, rack, preferences, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, empty, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
    
                        #
                        LOGGER.debug(f"preferences is {preferences}")
                        print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                        if player == 1:
                            input("End of turn, player %s. Press any key to continue. " % str(player))
                        else:
                            input("Player %s has completed their turn. Press any key to continue. " % str(player))
                        print()
                    else:
                        LOGGER.info(f"Player {player} has no empty cells; ending participation in this round")
                        cont_round[player-1] = False
                    if player == num_players:
                        player = 1
                    else:
                        player += 1
                    continue_round = False
                    for item in cont_round:
                        if cont_round[item]:
                            continue_round = True
    
                #end of round
                sound_bell()
                print("End of round %s." % str(round))
                print()
                #high round bonus
                round_scores = {}
                for plr in range(1,len(game)+1):
                    round_scores.update({plr:game[plr-1][round-1]})
                round_values = round_scores.values()
                high_score = max(round_values)
                high_player = []
                for k in iter(round_scores.keys()):
                    if round_scores[k] == high_score:
                        high_player.append(k)
                bonus_score = [30, 60, 120]
                for x in high_player:
                    player_bonus[x-1][round-1] = bonus_score[round-1]
                if len(high_player) == 1:
                    print("The round %s high round bonus of %s goes to player %s." % (str(round), str(bonus_score[round-1]), str(int(high_player[0]))))
                    LOGGER.info(f"Round {round} high round bonus {bonus_score[round-1]} awarded to player {int(high_player[0])}")
                    high_scores("ROUND", int(high_player[0]), max(round_values), num_players, round-1)
                else:
                    print("The round %s high round bonus of %s goes to players %s." % (str(round), str(bonus_score[round-1]), str(high_player)))
                    LOGGER.info(f"Round {round} high round bonus {bonus_score[round-1]} awarded to players {high_player}")
                print()
                input("Press any key to update the score and continue. ")
                print_rack(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                forfeit = score_rack(round, rack, game, player_bonus, forfeit)
    
        #end of game
        sound_bell()
        score_rack(round, rack, game, player_bonus, forfeit)
        print()
        print("Game Over.")
        print()
        if not forfeit:
            #winner
            total = []
            all = []
            for plr in range(len(game)):
                total.append(0)
                for rnd in range(3):
                    total[plr] += game[plr][rnd] + player_bonus[plr][rnd]
                    all.append(total[plr])
            high_score = max(all)
            high_player = []
            for k in range(len(total)):
                if total[k] == high_score:
                    high_player.append(k)
            if len(high_player) == 1:
                print("The winner is player " + str(high_player[0]+1) + " with " + str(max(total)) + " points!")
                LOGGER.info(f"Game winner: player {high_player[0]+1} with {max(total)} points")
                high_scores("GAME", int(high_player[0])+1, max(total), num_players, round-1)
            elif len(high_player) == 2:
                print('The winners are players '+str(high_player[0]+1)+' and '+str(high_player[1]+1)+' with ' + str(max(total)) + ' points!')
                LOGGER.info(f"Game winners: players {high_player[0]+1} and {high_player[1]+1} with {max(total)} points")
            elif len(high_player) == 3:
                print('The winners are players '+str(high_player[0]+1)+', '+str(high_player[1]+1)+', and '+str(high_player[2]+1)+' with ' + str(max(total)) + ' points!')
                LOGGER.info(f"Game winners: players {high_player[0]+1}, {high_player[1]+1}, and {high_player[2]+1} with {max(total)} points")
            elif len(high_player) == 4:
                print('The winners are players '+str(high_player[0]+1)+', '+str(high_player[1]+1)+', '+str(high_player[2]+1)+', and '+str(high_player[3]+1)+' with ' + str(max(total)) + ' points!')
                LOGGER.info(f"Game winners: players {high_player[0]+1}, {high_player[1]+1}, {high_player[2]+1}, and {high_player[3]+1} with {max(total)} points")
            print()
        again_input_err = True
        while again_input_err:
            again_yn = input("Would you like to play again? (Y/N) ")
            if again_yn.upper() == "Y":
                again_input_err = False
                print()
            elif again_yn.upper() == "N":
                again_input_err = False
                play_again = False
                print()
                print("Thank you for playing!")
                print()
            else:
                sound_bell()
                print()
    
