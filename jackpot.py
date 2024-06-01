#!/usr/local/bin/python3

import random
import os
import sys
from itertools import groupby
import json
from datetime import datetime
import getpass

def initialize_game(num_players):
    game = {}
    player_bonus = {}
    goes_first = random.randint(0,num_players-1)
    for i in range(num_players):
        game.update({i:[0, 0, 0]})
        player_bonus.update({i:[0, 0, 0]})
    return game, player_bonus, goes_first

def initialize_board(num_players):
    board = []
    for i in range(num_players):
        board.append([['1 2 3 4 5 6'],['_'], ['_','_'], ['_','_','_'], ['_','_','_','_'],['_','_','_','_','_','_']])
    return board

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

def empty_cells(player):
    player = player - 1
    empty_cells = 0
    row = 0
    while row < len(board[player]):
        col = 0
        while col < len(board[player][row]):
            if row == 5 and col == 5:
                pass
            elif board[player][row][col] == '_':
                empty_cells += 1
            col += 1
        row += 1
    return empty_cells

def board_score(player):
    player = player - 1
    score = 0
    jackpot_H = False
    jackpot_D = False

    #horizonal consecutive tiles
    L3 = []
    for col in range(3):
        L3.append(board[player][3][col])
    grouped_L3 = [(k, sum(1 for i in g)) for k,g in groupby(L3)]
    for (tile,count) in grouped_L3:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
    L4 = []
    for col in range(4):
        L4.append(board[player][4][col])
    grouped_L4 = [(k, sum(1 for i in g)) for k,g in groupby(L4)]
    for (tile, count) in grouped_L4:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
        elif count == 4:
            if tile == "C":
                score += 60
            elif tile == "O":
                score += 80
            elif tile == "B":
                score += 100
            elif tile == "M":
                score += 200
    L5 = []
    for col in range(6):
        L5.append(board[player][5][col])
    L5.pop(5)
    grouped_L5 = [(k, sum(1 for i in g)) for k,g in groupby(L5)]
    for (tile, count) in grouped_L5:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
        elif count == 4:
            if tile == "C":
                score += 60
            elif tile == "O":
                score += 80
            elif tile == "B":
                score += 100
            elif tile == "M":
                score += 200
        elif count == 5:
            if tile == "C":
                score += 120
                jackpot_H = True
            elif tile == "O":
                score += 160
                jackpot_H = True
            elif tile == "B":
                score += 200
                jackpot_H = True
            elif tile == "M":
                score += 400
                jackpot_H = True

    #diagonal consecutive tiles
    DL3 = []
    DL3.append(board[player][3][0])
    DL3.append(board[player][4][1])
    DL3.append(board[player][5][2])
    grouped_DL3 = [(k, sum(1 for i in g)) for k,g in groupby(DL3)]
    for (tile,count) in grouped_DL3:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
    DL3a = []
    DL3a.append(board[player][5][0])
    DL3a.append(board[player][4][1])
    DL3a.append(board[player][3][2])
    grouped_DL3a = [(k, sum(1 for i in g)) for k,g in groupby(DL3a)]
    for (tile,count) in grouped_DL3a:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
    DL4 = []
    DL4.append(board[player][2][0])
    DL4.append(board[player][3][1])
    DL4.append(board[player][4][2])
    DL4.append(board[player][5][3])
    grouped_DL4 = [(k, sum(1 for i in g)) for k,g in groupby(DL4)]
    for (tile, count) in grouped_DL4:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
        elif count == 4:
            if tile == "C":
                score += 60
            elif tile == "O":
                score += 80
            elif tile == "B":
                score += 100
            elif tile == "M":
                score += 200
    DL5 = []
    DL5.append(board[player][1][0])
    DL5.append(board[player][2][1])
    DL5.append(board[player][3][2])
    DL5.append(board[player][4][3])
    DL5.append(board[player][5][4])
    grouped_DL5 = [(k, sum(1 for i in g)) for k,g in groupby(DL5)]
    for (tile, count) in grouped_DL5:
        if count == 3:
            if tile == "C":
                score += 30
            elif tile == "O":
                score += 40
            elif tile == "B":
                score += 50
            elif tile == "M":
                score += 100
        elif count == 4:
            if tile == "C":
                score += 60
            elif tile == "O":
                score += 80
            elif tile == "B":
                score += 100
            elif tile == "M":
                score += 200
        elif count == 5:
            if tile == "C":
                score += 120
                jackpot_D = True
            elif tile == "O":
                score += 160
                jackpot_D = True
            elif tile == "B":
                score += 200
                jackpot_D = True
            elif tile == "M":
                score += 400
                jackpot_D = True

    #rack bonus
    cherry_cnt = 0
    orange_cnt = 0
    bell_cnt = 0
    money_cnt = 0
    row = 0
    while row < len(board[player]):
        col = 0
        while col < len(board[player][row]):
            if row == 5 and col == 5:
                pass
            elif board[player][row][col] == "C":
                cherry_cnt += 1
            elif board[player][row][col] == "O":
                orange_cnt += 1
            elif board[player][row][col] == "B":
                bell_cnt += 1
            elif board[player][row][col] == "M":
                money_cnt += 1
            col += 1
        row += 1
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
    elif orange_cnt ==7:
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

def print_board(h, d, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
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
    while row < len(board[player-1]):
        col = 0
        while col < len(board[player-1][row]):
            if board[player-1][row][col] == "C":
                colorize(board[player-1][row][col])
                print(" ", end = '')
            elif board[player-1][row][col] == "O":
                colorize(board[player-1][row][col])
                print(" ", end = '')
            elif board[player-1][row][col] == "B":
                colorize(board[player-1][row][col])
                print(" ", end = '')
            elif board[player-1][row][col] == "M":
                colorize(board[player-1][row][col])
                print(" ", end = '')
            else:
                print(board[player-1][row][col], end = ' ')
            col += 1
        print("\r")
        row += 1
    print()
    score_results = board_score(player)
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
        input("Press any key to continue.")
        print()
        h[player-1] = True
    elif jackpot_D and not d[player-1]:
        sound_bell()
        print("Jackpot!!!")
        print()
        input("Press any key to continue.")
        print()
        d[player-1] = True

    return h, d

def score_board(round, board, game, player_bonus, forfeit):
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
            while col < len(board[plr-1][row]):
                if board[plr][row][col] == "C":
                    colorize(board[plr][row][col])
                    print(" ", end = '')
                elif board[plr][row][col] == "O":
                    colorize(board[plr][row][col])
                    print(" ", end = '')
                elif board[plr][row][col] == "B":
                    colorize(board[plr][row][col])
                    print(" ", end = '')
                elif board[plr][row][col] == "M":
                    colorize(board[plr][row][col])
                    print(" ", end = '')
                else:
                    print(board[plr][row][col], end = '')
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
        print()
        forfeit = input("Press <Enter> to begin round %s or Q to quit. " % str(round+1))
        if forfeit.upper() == 'Q':
            forfeit = True
    return forfeit

def col_choices(player):
    player = player - 1
    valid_col = []
    row = 0
    while row < len(board[player]):
        col = 0
        while col < len(board[player][row]):
            if board[player][row][col] == '_':
                if (col + 1) not in valid_col:
                    valid_col.append(col + 1)
            col += 1
        row += 1
    return valid_col

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

def pit_tile(player, round, choices, valid_cols, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    print("Your tile selection: ", end = '')
    colorize(choices)
    print("\r")
    print()
    input_err = True
    while input_err:
        use_pit = input("Use (U), Remove (R), or Swap (S) pit tile ['%s'] or Not (N)? " % board[player-1][5][5])
        print()
        if use_pit.upper() == "U":
            input_err = False
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(board[player-1][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            undo_tile = board[player-1][5][5]
            board[player-1][5][5] = '_'
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, undo_tile, valid_cols, empty_cells(player), True, True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            if undo:
                input_err = True
                board[player-1][5][5] = undo_tile
            else:
                valid_cols = col_choices(player)
                (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
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
            input_err = False
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(board[player-1][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            board[player-1][5][5] = '_'
            valid_cols = col_choices(player)
            (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
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
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(board[player-1][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            swap = True
            if len(choices) == 1:
                board[player-1][5][5] = choices[0]
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(choices[0], 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            else:
                sel_input_err = True
                while sel_input_err:
                    print("Select a tile from ")
                    colorize(choices)
                    selection = input(": ")
                    print()
                    if selection.upper() in choices:
                        board[player-1][5][5] = selection.upper()
                        sel_input_err = False
                    else:
                        sound_bell()
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(selection.upper(), 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        elif use_pit.upper() == "N":
            input_err = False
        else:
            sound_bell()
    return valid_cols, h_jkpt, d_jkpt, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def select_tiles(player, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
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
    player = player - 1
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
            else:
                if board[player][5][valid_cols[0] - 1] == '_':
                    pla_input_err = False
                    board[player][5][valid_cols[0] - 1] = tile
                elif board[player][4][valid_cols[0] - 1] == '_':
                    pla_input_err = False
                    board[player][4][valid_cols[0] - 1] = tile
                elif board[player][3][valid_cols[0] - 1] == '_':
                    pla_input_err = False
                    board[player][3][valid_cols[0] - 1] = tile
                elif board[player][2][valid_cols[0] - 1] == '_':
                    pla_input_err = False
                    board[player][2][valid_cols[0] - 1] = tile
                elif board[player][1][valid_cols[0] - 1] == '_':
                    pla_input_err = False
                    board[player][1][valid_cols[0] - 1] = tile
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
            elif placement == "":
                show_tile_sel = True
                sound_bell()
                print_board(h_jkpt, d_jkpt, round, player + 1, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            else:
                col_strings = []
                for i in valid_cols:
                    col_strings.append(str(i))
                if placement not in col_strings:
                    show_tile_sel = True
                    sound_bell()
                else:
                    placement = int(placement) - 1
                    if board[player][5][placement] == '_':
                        board[player][5][placement] = tile
                        pla_input_err = False
                        undo_place = 5
                    elif board[player][4][placement] == '_':
                        board[player][4][placement] = tile
                        pla_input_err = False
                        undo_place = 4
                    elif board[player][3][placement] == '_':
                        board[player][3][placement] = tile
                        pla_input_err = False
                        undo_place = 3
                    elif board[player][2][placement] == '_':
                        board[player][2][placement] = tile
                        pla_input_err = False
                        undo_place = 2
                    elif board[player][1][placement] == '_':
                        board[player][1][placement] = tile
                        pla_input_err = False
                        undo_place = 1
                    if place_pit:
                        board[player][5][5] = '_'
                print_board(h_jkpt, d_jkpt, round, player + 1, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            if undo or pla_input_err:
                pass
            else:
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                sure = input("Player %s, you have selected column %s. Press <Enter> to continue or Z to undo. " % (str(player+1), str(int(placement)+1)))
                if sure.upper() == "Z":
                    pla_input_err = True
                    show_tile_sel = True
                    board[player][undo_place][placement] = '_'
                    if place_pit:
                        board[player][5][5] = tile
                    else:
                        cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    print_board(h_jkpt, d_jkpt, round, player + 1, cherry_tiles, orange_tiles, bell_tiles, money_tiles)

    return undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def check_supply(tile):
    result = False
    if tile == "C" and cherry_tiles > 0:
        result = True
    elif tile == "O" and orange_tiles > 0:
        result = True
    elif tile == "B" and bell_tiles > 0:
        result = True
    elif tile == "M" and money_tiles >0:
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

def auto_play(player, board, preferences, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, empty, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    player = player - 1
    cont = True

    #pit not empty but can be emptied
    if board[player][5][5] != "_" and empty:

        #check to see if pit tile is a preferred tile, try to play it
        if board[player][5][5] in preferences[player]:
            i = 0
            while cont and i < len(preferences[player]):
                if board[player][5][5] == preferences[player][i]:
                    if len(choices) == 1:
                        both_played, pit_played = simulate_play(player, board[player][5][5], choices[0])
                        if both_played or (pit_played and board[player][5][5] != choices[0]):
                            found, cherry_tiles, orange_tiles, bell_tiles, money_tiles = next_best_play(player, i, False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                            if found:
                                cont = False
                                board[player][5][5] = "_"
                                sound_bell()
                                print()
                                input("Player %s plays pit tile. " % str(player+1))
                        else:
                            cont = False
                            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(board[player][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                            board[player][5][5] = "_"
                            sound_bell()
                            print()
                            input("Player %s empties pit tile. " % str(player+1))
                    else:
                        found, cherry_tiles, orange_tiles, bell_tiles, money_tiles = next_best_play(player, i, False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                        if found:
                            cont = False
                            board[player][5][5] = "_"
                            sound_bell()
                            print()
                            input("Player %s plays pit tile. " % str(player+1))
                i += 1

        #check if non-preferred tile is playable in dead space and choice is playable
        if cont and board[player][5][0] != '_' and board[player][4][0] == '_':
            if len(choices) == 1:
                both_played, pit_played = simulate_play(player, board[player][5][5], choices[0])
                if both_played:
                    cont = False
                    board[player][4][0] = board[player][5][5]
                    board[player][5][5] = "_"
                    sound_bell()
                    print()
                    input("Player %s plays pit tile. " % str(player+1))
                else:
                    cont = False
                    cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(board[player][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    board[player][5][5] = "_"
                    sound_bell()
                    print()
                    input("Player %s empties pit tile. " % str(player+1))

        #empty pit tile
        if board[player][5][5] != "_" and empty and cont:
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(board[player][5][5], 'POSITIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            board[player][5][5] = "_"
            sound_bell()
            print()
            input("Player %s empties pit tile. " % str(player+1))

    #strategy for single choice roll
    if len(choices) == 1:
        i = 0
        cont = True

        #check if choice is preferred and if so if it can be played
        while cont and i < len(preferences[player]):
            if preferences[player][i] == choices[0]:
                found, cherry_tiles, orange_tiles, bell_tiles, money_tiles = next_best_play(player, i, True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                if found:
                    cont = False
            i += 1
        i = 0

        #if choice not playable as preferred try to establish a new preferred
        while cont and i < len(preferences[player]):
            if preferences[player][i] == "_":
                cont = False
                preferences[player][i] = choices[0]
                board[player][5][2+i] = choices[0]
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(choices[0], 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            i += 1

        #check if dead space is playable
        if cont and board[player][5][0] != '_' and board[player][4][0] == '_':
            cont = False
            board[player][4][0] = choices[0]
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(choices[0], 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)

        #choice not playable as preferred or in dead space
        if cont:
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = least_bad_play(player, choices, board, cherry_tiles, orange_tiles, bell_tiles, money_tiles)

    #strategy for multiple choice roll
    else:
        play_count = 1
        while play_count <= 1 or (doubles and play_count <= 2):
            rankLoop = True
            for tile in ['M','O','B','C']:
                if rankLoop:
                    cont = True

                    #check if choice is preferred and if so if it can be played
                    if cont and tile in choices:
                        i = 0
                        while cont and i < len(preferences[player]):
                            if tile == preferences[player][i]:
                                found, cherry_tiles, orange_tiles, bell_tiles, money_tiles = next_best_play(player, i, True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                                if found:
                                    cont = False
                                    rankLoop = False
                            i += 1

                    #if choice not playable as preferred try to establish a new preferred
                    if cont and tile in choices and "_" in preferences[player]:
                        i = 0
                        while cont and i < len(preferences[player]):
                            if preferences[player][i] == "_":
                                cont = False
                                rankLoop = False
                                preferences[player][i] = tile
                                board[player][5][2+i] = tile
                                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                            i += 1

            #check if dead space is playable
            if cont and board[player][5][0] != '_' and board[player][4][0] == '_':
                cont = False
                max_tile = least_bad_tile(player)
                board[player][4][0] = max_tile
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(max_tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            play_count += 1

            #choice not playable as preferred or in dead space
            if cont:
                cherry_tiles, orange_tiles, bell_tiles, money_tiles = least_bad_play(player, choices, board, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
    return valid_cols, board, preferences, h_jkpt, d_jkpt, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def least_bad_tile(player):
    M_cnt = 0
    B_cnt = 0
    O_cnt = 0
    C_cnt = 0
    for r in range(len(board[player])):
        for c in range(len(board[player][r])):
            if r == 5 and c == 5:
                pass
            else:
                for tile in board[player][r][c]:
                    if tile == 'M':
                        M_cnt += 1
                    elif tile == 'B':
                        B_cnt += 1
                    elif tile == 'O':
                        O_cnt += 1
                    elif tile == 'C':
                        C_cnt += 1
    max_tile_val = 0
    for tile in choices:
        if tile == 'M':
            if M_cnt > max_tile_val:
                max_tile_val = M_cnt
                max_tile = 'M'
        elif tile == 'B':
            if B_cnt > max_tile_val:
                max_tile_val = B_cnt
                max_tile = 'B'
        elif tile == 'O':
            if O_cnt > max_tile_val:
                max_tile_val = O_cnt
                max_tile = 'O'
        elif tile == 'C':
            if C_cnt > max_tile_val:
                max_tile_val = C_cnt
                max_tile = 'C'
    if max_tile_val == 0:
        for tile in ['M','O','B','C']:
            cont = True
            if cont and tile in choices:
                cont = False
                max_tile = tile
    return max_tile

def next_best_play(player, prefs_index, reduce_supply, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    open_row = {}
    for col in range(5):
        blankNotFound = True
        for row in range(5, col, -1):
            if blankNotFound and board[player][row][col] == "_":
                blankNotFound = False
                open_row.update({col:row})
            elif blankNotFound and row == col+1:
                open_row.update({col:-1})
            else:
                pass
    prefs_tile = board[player][5][prefs_index+2]
    playable = non_dead_play(player, choices)
    found = False

    #strategy for column 3 and lower
    if prefs_index == 0:
        if board[player][5][1] == '_':
            found = True
            board[player][5][1] = prefs_tile
        elif board[player][4][1] == '_':
            found = True
            board[player][4][1] = prefs_tile
        elif board[player][5][0] == '_':
            found = True
            board[player][5][0] = prefs_tile
        elif board[player][4][0] == '_' and not playable:
            found = True
            board[player][4][0] = prefs_tile
        elif board[player][3][0] == '_' and board[player][4][0] != '_':
            found = True
            board[player][3][0] = prefs_tile

    #strategy for columns 4 and 5
    else:
        row = 4
        while not found and row > 2-prefs_index:
            if row == open_row[row-3+prefs_index]:
                if row == 4 and prefs_index == 3-row and playable:
                    pass
                else:
                    board[player][row][row-3+prefs_index] = prefs_tile
                    found = True
            row -= 1
        if not found and board[player][5][0] != '_' and board[player][4][0] == '_' and not playable:
            board[player][4][0] = prefs_tile
            found = True

    if found and reduce_supply:
        cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(prefs_tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
    return found, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def simulate_play(player, tile1, tile2):
    sim_board = []
    for p in range(len(board)):
      sim_board.append([])
      for r in range(6):
        sim_board[p].append([])
        for c in range(len(board[p][r])):
          sim_board[p][r].append(board[p][r][c])
    found = [False,False]
    tile = [tile1,tile2]
    pit_dead = False

    for i in range(2):
        open_row = {}
        for col in range(5):
            blankNotFound = True
            for row in range(5, col, -1):
                if blankNotFound and sim_board[player][row][col] == "_":
                    blankNotFound = False
                    open_row.update({col:row})
                elif blankNotFound and row == col+1:
                    open_row.update({col:-1})
                else:
                    pass

        if tile[i] in preferences[player]:
            cont = True
            j = 0
            while cont and j < len(preferences[player]):
                if tile[i] == preferences[player][j]:

                    #strategy for column 3 and lower
                    if j == 0:
                        if sim_board[player][5][1] == '_':
                            cont = False
                            found[i] = True
                            sim_board[player][5][1] = tile[i]
                        elif sim_board[player][4][1] == '_':
                            cont = False
                            found[i] = True
                            sim_board[player][4][1] = tile[i]
                        elif sim_board[player][5][0] == '_':
                            cont = False
                            found[i] = True
                            sim_board[player][5][0] = tile[i]
                        elif sim_board[player][4][0] == '_':
                            cont = False
                            found[i] = True
                            sim_board[player][4][0] = tile[i]
                        elif sim_board[player][3][0] == '_':
                            cont = False
                            found[i] = True
                            sim_board[player][3][0] = tile[i]

                    #strategy for columns 4 and 5
                    else:
                        row = 4
                        while not found[i] and row > 2-j:
                            if row == open_row[row-3+j]:
                                cont = False
                                found[i] = True
                                sim_board[player][row][row-3+j] = tile[i]
                            row -= 1
                j += 1

        if not found[i] and sim_board[player][5][0] != '_' and sim_board[player][4][0] == '_':
            found[i] = True
            sim_board[player][4][0] = tile[i]
            if i == 0:
                pit_dead = True

    all_found = True
    for i in range(len(found)):
        if not found[i]:
            all_found = False
    if pit_dead:
        pit_found = False
    else:
        pit_found = found[0]

    return all_found, pit_found

def non_dead_play(player, choices):
    open_row = {}
    for col in range(5):
        blankNotFound = True
        for row in range(5, col, -1):
            if blankNotFound and board[player][row][col] == "_":
                blankNotFound = False
                open_row.update({col:row})
            elif blankNotFound and row == col+1:
                open_row.update({col:-1})
            else:
                pass
    found = False

    for choice in choices:
        if choice in preferences[player]:
            i = 0
            while not found and i < len(preferences[player]):
                if choice == preferences[player][i]:

                    #strategy for column 3 and lower
                    if i == 0:
                        if board[player][5][1] == '_':
                            found = True
                        elif board[player][4][1] == '_':
                            found = True
                        elif board[player][5][0] == '_':
                            found = True
                        elif board[player][3][0] == '_':
                            found = True

                    #strategy for columns 4 and 5
                    else:
                        row = 4
                        while not found and row > 2-i:
                            if row == open_row[row-3+i]:
                                found = True
                            row -= 1
                i += 1

    return found

def least_bad_play(player, choices, board, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    open_row = {}
    for col in range(5):
        blankNotFound = True
        for row in range(5, col, -1):
            if blankNotFound and board[player][row][col] == "_":
                blankNotFound = False
                open_row.update({col:row})
            elif blankNotFound and row == col+1:
                open_row.update({col:-1})
            else:
                pass
    if len(choices) == 1:
        tile = choices[0]
    else:
        tile = least_bad_tile(player)
    notFound = True
    i = 0
    while notFound and i < len(open_row):
        if open_row[i] != -1:
            notFound = False
            if board[player][5][5] == "_":
                board[player][5][5] = tile
            else:
                board[player][open_row[i]][i] = tile
            cherry_tiles, orange_tiles, bell_tiles, money_tiles = transact(tile, 'NEGATIVE', cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        i += 1
    return cherry_tiles, orange_tiles, bell_tiles, money_tiles

def high_scores(scope, player, score, num_players, round):
    data = ''
    newData = ''
    now = datetime.now()
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    if player == 0:
        user_name = getpass.getuser()
    else:
        user_name = "Player "+str(player+1)

    with open('high_scores.json') as json_file:
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
                    with open('high_scores.json','w') as outfile:
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
                    with open('high_scores.json','w') as outfile:
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

#MAIN PROGRAM
play_again = True

#game loop
while play_again:
    os.system('clear')
    players_input_err = True
    while players_input_err:
        num_players = input("Enter number of players (2 - 4): ")
        print()
        if str(num_players) not in ["2", "3", "4"]:
            sound_bell()
            pass
        else:
            num_players = int(num_players)
            players_input_err = False
    game, player_bonus, goes_first = initialize_game(num_players)
    player = goes_first+1
    input("Player %s goes first! Press any key to continue. " % str(goes_first+1))
    forfeit = False

    #round loop
    for round in range(1,4):
        if not forfeit:
            board = initialize_board(num_players)
            (h_jkpt, d_jkpt, cont_round, preferences, cherry_tiles, orange_tiles, bell_tiles, money_tiles) = initialize_round(num_players)
            continue_round = False
            for item in cont_round:
                if cont_round[item]:
                    continue_round = True
                
            #player loop
            while continue_round and not forfeit:
                if empty_cells(player) > 0:
                    (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    if player == 1:
                        input("Player %s, press any key to roll dice: " % str(player))
                        print()

                    #roll dice
                    (roll, choices, doubles, empty) = roll_dice()
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
                        else:
                            num_plays = 1

                        #use or remove pit tile
                        swap = False
                        if board[player-1][5][5] != '_' and empty:
                            sound_bell()
                            print("You have the option to play or remove the pit tile!")
                            print()
                            (valid_cols, h_jkpt, d_jkpt, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles) = pit_tile(player, round, choices, valid_cols, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles)

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
                                print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    else:
                        if doubles:
                            sound_bell()
                            print("Doubles!", end = ' ')
                        print("Player "+str(player)+" rolls ", end = '')
                        colorize(roll)
                        print(" resulting in: ", end = '')
                        colorize(choices)
                        input(". ")
                        valid_cols, board, preferences, h_jkpt, d_jkpt, cherry_tiles, orange_tiles, bell_tiles, money_tiles = auto_play(player, board, preferences, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, empty, cherry_tiles, orange_tiles, bell_tiles, money_tiles)

                    print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    if player == 1:
                        input("End of turn, player %s. Press any key to continue. " % str(player))
                    else:
                        input("Player %s has completed their turn. Press any key to continue. " % str(player))
                    print()
                else:
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
                high_scores("ROUND", int(high_player[0])-1, max(round_values), num_players, round-1)
            else:
                print("The round %s high round bonus of %s goes to players %s." % (str(round), str(bonus_score[round-1]), str(high_player)))
            print()
            input("Press any key to update the score and continue. ")
            print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            forfeit = score_board(round, board, game, player_bonus, forfeit)

    #end of game
    sound_bell()
    score_board(round, board, game, player_bonus, forfeit)
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
            high_scores("GAME", int(high_player[0]), max(total), num_players, round-1)
        elif len(high_player) == 2:
            print('The winners are players '+str(high_player[0]+1)+' and '+str(high_player[1]+1)+' with ' + str(max(total)) + ' points!')
        elif len(high_player) == 3:
            print('The winners are players '+str(high_player[0]+1)+', '+str(high_player[1]+1)+', and '+str(high_player[2]+1)+' with ' + str(max(total)) + ' points!')
        elif len(high_player) == 4:
            print('The winners are players '+str(high_player[0]+1)+', '+str(high_player[1]+1)+', '+str(high_player[2]+1)+', and '+str(high_player[3]+1)+' with ' + str(max(total)) + ' points!')
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

