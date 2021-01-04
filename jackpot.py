#!/usr/bin/env python
#
#  1 - 4 player game
#  each game consists of 3 rounds
#  high round bonus awarded on one player game when round score is 350 or higher
#  option to play again
#
#  Dice sides
#  White - 2 Orange, 2 Bells, 1 Cherry, 1 Money
#  Yellow - 3 Cherry, 1 Bell, 1 Orange, 1 Money
#
#  Tile quantity
#  Cherry, 35
#  Orange, 28
#  Bell, 28
#  Money, 21
#

import random
import os
import sys
from itertools import groupby

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
        board.append([["1 2 3 4 5 6"],["_"], ["_","_"], ["_","_","_"], ["_","_","_","_"],["_","_","_","_","_","_"]])
    return board

def initialize_round(num_players):
    cherry_tiles = 35
    orange_tiles = 28
    bell_tiles = 28
    money_tiles = 21
    h_jkpt = {}
    d_jkpt = {}
    cont_round = {}
    for i in range(0,num_players):
        h_jkpt.update({i:False})
        d_jkpt.update({i:False})
        cont_round.update({i:True})
    return h_jkpt, d_jkpt, cont_round, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def empty_cells(player):
    player = player - 1
    empty_cells = 0
    row = 0
    while row < len(board[player]):
        col = 0
        while col < len(board[player][row]):
            if row == 5 and col == 5:
                pass
            elif board[player][row][col] == "_":
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
    print "Round",
    for i in range(len(game)):
        print " Player %s" % str(i+1),
    print "\r"
    for rnd in range(3):
        print " "*3, str(rnd+1),
        for plr in range(len(game)):
            print " "*(8 - len(str(game[plr][rnd]))), str(game[plr][rnd]),
            total[plr] += game[plr][rnd]
        print "\r"
        print " "*5,
        for plr in range(len(game)):
            print " "*(8 - len(str(player_bonus[plr][rnd]))), str(player_bonus[plr][rnd]),
            total[plr] += player_bonus[plr][rnd]
        print "\r"
    print "Total",
    for plr in range(len(game)):
        print " "*(8 - len(str(total[plr]))), str(total[plr]),
    print "\r"
    print
    for i in range(cherry_tiles):
        print u"\u001b[31m" + "C" + u"\u001b[0m",
    print "\r"
    for i in range(orange_tiles):
        print u"\u001b[38;5;208m" + "O" + u"\u001b[0m",
    print "\r"
    for i in range(bell_tiles):
        print u"\u001b[34m" + "B" + u"\u001b[0m",
    print "\r"
    for i in range(money_tiles):
        print u"\u001b[32m" + "M" + u"\u001b[0m",
    print "\r"
    print
    print "Round %s > Player %s"  % (str(round), str(player))
    print
    row = 0
    while row < len(board[player-1]):
        col = 0
        while col < len(board[player-1][row]):
            if board[player-1][row][col] == "C":
                print u"\u001b[31m" + board[player-1][row][col] + u"\u001b[0m",
            elif board[player-1][row][col] == "O":
                print u"\u001b[38;5;208m" + board[player-1][row][col] + u"\u001b[0m",
            elif board[player-1][row][col] == "B":
                print u"\u001b[34m" + board[player-1][row][col] + u"\u001b[0m",
            elif board[player-1][row][col] == "M":
                print u"\u001b[32m" + board[player-1][row][col] + u"\u001b[0m",
            else:
                print board[player-1][row][col],
            col += 1
        print "\r"
        row += 1
    print
    score_results = board_score(player)
    score = score_results[0]
    jackpot_H = score_results[1]
    jackpot_D = score_results[2]
    game[player-1][round-1] = score
    print "Score: " + str(score)
    print
    if jackpot_H and not h[player-1]:
        sound_bell()
        print "Jackpot!!!"
        print
        raw_input("Press any key to continue.")
        print
        h[player-1] = True
    elif jackpot_D and not d[player-1]:
        sound_bell()
        print "Jackpot!!!"
        print
        raw_input("Press any key to continue.")
        print
        d[player-1] = True

    return h, d

def score_board(round, board, game, player_bonus):
    os.system('clear')
    total = []
    for i in range(num_players):
        total.append(0)
    print "Round",
    for i in range(len(game)):
        print " Player %s" % str(i+1),
    print "\r"
    for rnd in range(3):
        print " "*3, str(rnd+1),
        for plr in range(len(game)):
            print " "*(8 - len(str(game[plr][rnd]))), str(game[plr][rnd]),
            total[plr] += game[plr][rnd]
        print "\r"
        print " "*5,
        for plr in range(len(game)):
            print " "*(8 - len(str(player_bonus[plr][rnd]))), str(player_bonus[plr][rnd]),
            total[plr] += player_bonus[plr][rnd]
        print "\r"
    print "Total",
    for plr in range(len(game)):
        print " "*(8 - len(str(total[plr]))), str(total[plr]),
    print "\r"
    print
    for i in range(cherry_tiles):
        print u"\u001b[31m" + "C" + u"\u001b[0m",
    print "\r"
    for i in range(orange_tiles):
        print u"\u001b[38;5;208m" + "O" + u"\u001b[0m",
    print "\r"
    for i in range(bell_tiles):
        print u"\u001b[34m" + "B" + u"\u001b[0m",
    print "\r"
    for i in range(money_tiles):
        print u"\u001b[32m" + "M" + u"\u001b[0m",
    print "\r"
    print
    print "Round %s > All Players"  % str(round)
    print
    for row in range(6):
        for plr in range(len(game)):
            col = 0
            while col < len(board[plr-1][row]):
                if board[plr][row][col] == "C":
                    print u"\u001b[31m" + board[plr][row][col] + u"\u001b[0m",
                elif board[plr][row][col] == "O":
                    print u"\u001b[38;5;208m" + board[plr][row][col] + u"\u001b[0m",
                elif board[plr][row][col] == "B":
                    print u"\u001b[34m" + board[plr][row][col] + u"\u001b[0m",
                elif board[plr][row][col] == "M":
                    print u"\u001b[32m" + board[plr][row][col] + u"\u001b[0m",
                else:
                    print board[plr][row][col],
                col += 1
            print " "*3,
            if 1 <= row <= 4:
                print " "*(11-(2*row)),
        print "\r"
    print
    for plr in range(len(game)):
        print "Player %s" % str(plr+1),
        print " "*6,
    print "\r"
    if round < 3:
        print
        raw_input("Press <Enter> to begin round %s. " % str(round+1))

def col_choices(player):
    player = player - 1
    valid_col = []
    row = 0
    while row < len(board[player]):
        col = 0
        while col < len(board[player][row]):
            if board[player][row][col] == "_":
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
    print "Your tile selection: %s" % choices
    print
    input_err = True
    while input_err:
        use_pit = raw_input("Use (U), Remove (R), or Swap (S) pit tile ['%s'] or Not (N)? " % board[player-1][5][5])
        print
        if use_pit.upper() == "U":
            input_err = False
            if board[player-1][5][5] == "C":
                cherry_tiles += 1
            elif board[player-1][5][5] == "O":
                orange_tiles += 1
            elif board[player-1][5][5] == "B":
                bell_tiles += 1
            elif board[player-1][5][5] == "M":
                money_tiles += 1
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, board[player-1][5][5], valid_cols, empty_cells(player), True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            board[player-1][5][5] = "_"
            valid_cols = col_choices(player)
            (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            if empty_cells(player) > 0:
                print "Your roll: " + str(roll)
                print
                if doubles and empty_cells(player) > 0:
                    sound_bell()
                    print "Doubles!"
                    print
        elif use_pit.upper() == "R":
            input_err = False
            if board[player-1][5][5] == "C":
                cherry_tiles += 1
            elif board[player-1][5][5] == "O":
                orange_tiles += 1
            elif board[player-1][5][5] == "B":
                bell_tiles += 1
            elif board[player-1][5][5] == "M":
                money_tiles += 1
            board[player-1][5][5] = "_"
            valid_cols = col_choices(player)
            (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
            print "Your roll: " + str(roll)
            print
            if doubles:
                sound_bell()
                print "Doubles!"
                print
        elif use_pit.upper() == "S":
            input_err = False
            if board[player-1][5][5] == "C":
                cherry_tiles += 1
            elif board[player-1][5][5] == "O":
                orange_tiles += 1
            elif board[player-1][5][5] == "B":
                bell_tiles += 1
            elif board[player-1][5][5] == "M":
                money_tiles += 1
            swap = True
            if len(choices) == 1:
                board[player-1][5][5] = choices[0]
            if choices[0] == "C":
                cherry_tiles -= 1
            elif choices[0] == "O":
                orange_tiles -= 1
            elif choices[0] == "B":
                bell_tiles -= 1
            elif choices[0] == "M":
                money_tiles -= 1
            else:
                sel_input_err = True
                while sel_input_err:
                    selection = raw_input("Select a tile from %s: " % str(choices))
                    print
                    if selection.upper() in choices:
                        board[player-1][5][5] = selection.upper()
                        sel_input_err = False
                    else:
                        sound_bell()
                if selection.upper() == "C":
                    cherry_tiles -= 1
                elif selection.upper() == "O":
                    orange_tiles -= 1
                elif selection.upper() == "B":
                    bell_tiles -= 1
                elif selection.upper() == "M":
                    money_tiles -= 1
        elif use_pit.upper() == "N":
            input_err = False
        else:
            sound_bell()
    return valid_cols, h_jkpt, d_jkpt, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def select_tiles(player, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    if len(choices) == 1 and swap == False:
        if check_supply(choices[0]):
            print "Your tile selection is ['%s']." % choices[0]
            print
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, choices[0], valid_cols, empty_cells(player), False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        else:
            undo = False
            sound_bell()
            raw_input("All of the ['%s'] tiles are currently in play. Press <Enter> to continue." % str(choices[0]))
            print
    elif len(choices) > 1 and swap == False:
        for choice in choices:
            if not check_supply(choice):
                choices.remove(choice)
        if len(choices) == 1:
            print "Your tile selection is ['%s']." % choices[0]
            print
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, choices[0], valid_cols, empty_cells(player), False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        else:
            sel_input_err = True
            while sel_input_err:
                selection = raw_input("Select a tile from %s: " % str(choices))
                print
                if selection.upper() in choices:
                    sel_input_err = False
                    if check_supply(selection.upper()):
                        undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, selection.upper(), valid_cols, empty_cells(player), True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                        if doubles and empty_cells(player) > 0:
                            (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                            valid_cols = col_choices(player)
                            print "Your roll: " + str(roll)
                            print
                            sound_bell()
                            print "Doubles!"
                            print
                            dsel_input_err = True
                            while dsel_input_err:
                                selection = raw_input("Select a tile from %s: " % str(choices))
                                print
                                if selection.upper() in choices:
                                    dsel_input_err = False
                                    undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, selection.upper(), valid_cols, empty_cells(player), True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                                else:
                                    sound_bell()
                    else:
                        sound_bell()
                        raw_input("All of the ['%s'] tiles are currently in play. Press <Enter> to continue." % selection.upper())
                        print
                else:
                    sound_bell()
    elif len(choices) > 1 and swap:
        for choice in choices:
            if not check_supply(choice):
                choices.remove(choice)
        if len(choices) == 1:
            print "Your tile selection is ['%s']." % choices[0]
            print
            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, choices[0], valid_cols, empty_cells(player), False, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        else:
            if doubles and empty_cells(player) > 0:
                (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                valid_cols = col_choices(player)
                print "Your roll: " + str(roll)
                print
                sound_bell()
                print "Doubles!"
                print
                dsel_input_err = True
                while dsel_input_err:
                    selection = raw_input("Select a tile from %s: " % str(choices))
                    print
                    if selection.upper() in choices:
                        dsel_input_err = False
                        if check_supply(selection.upper()):
                            undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = place_tile(player, round, h_jkpt, d_jkpt, selection.upper(), valid_cols, empty_cells(player), True, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                        else:
                            sound_bell()
                            raw_input("All of the ['%s'] tiles are currently in play. Press <Enter> to continue." % selection.upper())
                            print
                    else:
                        sound_bell()
    else:
        undo = False
    return valid_cols, undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles

def place_tile(player, round, h_jkpt, d_jkpt, tile, valid_cols, empty_cells, undoable, cherry_tiles, orange_tiles, bell_tiles, money_tiles):
    player = player - 1
    if len(valid_cols) == 1:
        if undoable:
            do_undo = raw_input("Your column selection is %s. Press <Enter> to continue or Z to undo. " % str(valid_cols[0]))
            if do_undo.upper() == "Z":
                undo = True
                print
            else:
                undo = False
        else:
            undo = False
            raw_input("Your column selection is %s. Press <Enter> to continue. " % str(valid_cols[0]))
        if board[player][5][valid_cols[0] - 1] == "_":
            board[player][5][valid_cols[0] - 1] = tile
        elif board[player][4][valid_cols[0] - 1] == "_":
            board[player][4][valid_cols[0] - 1] = tile
        elif board[player][3][valid_cols[0] - 1] == "_":
            board[player][3][valid_cols[0] - 1] = tile
        elif board[player][2][valid_cols[0] - 1] == "_":
            board[player][2][valid_cols[0] - 1] = tile
        elif board[player][1][valid_cols[0] - 1] == "_":
            board[player][1][valid_cols[0] - 1] = tile
        if tile == "C":
            cherry_tiles -= 1
        elif tile == "O":
            orange_tiles -= 1
        elif tile == "B":
            bell_tiles -= 1
        elif tile == "M":
            money_tiles -= 1
    else:
        pla_input_err = True
        while pla_input_err:
            if undoable:
                placement = raw_input("Select a column from %s or enter Z to undo: " % valid_cols)
            else:
                placement = raw_input("Select a column from %s: " % valid_cols)
            if placement.upper() == "Z":
                pla_input_err = False
                undo = True
                print
            else:
                undo = False
                print
                col_strings = []
                for i in valid_cols:
                    col_strings.append(str(i))
                if placement not in col_strings:
                    sound_bell()
                else:
                    placement = int(placement) - 1
                    if board[player][5][placement] == "_":
                        board[player][5][placement] = tile
                        pla_input_err = False
                        undo_place = 5
                    elif board[player][4][placement] == "_":
                        board[player][4][placement] = tile
                        pla_input_err = False
                        undo_place = 4
                    elif board[player][3][placement] == "_":
                        board[player][3][placement] = tile
                        pla_input_err = False
                        undo_place = 3
                    elif board[player][2][placement] == "_":
                        board[player][2][placement] = tile
                        pla_input_err = False
                        undo_place = 2
                    elif board[player][1][placement] == "_":
                        board[player][1][placement] = tile
                        pla_input_err = False
                        undo_place = 1
                    if tile == "C":
                        cherry_tiles -= 1
                    elif tile == "O":
                        orange_tiles -= 1
                    elif tile == "B":
                        bell_tiles -= 1
                    elif tile == "M":
                        money_tiles -= 1
                    print_board(h_jkpt, d_jkpt, round, player + 1, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    sure = raw_input("Player %s, you have selected column %s. Press <Enter> to continue or Z to undo. " % (str(player + 1), str(placement + 1)))
                    if sure.upper() == "Z":
                        board[player][undo_place][placement] = "_"
                        if tile == "C":
                            cherry_tiles += 1
                        elif tile == "O":
                            orange_tiles += 1
                        elif tile == "B":
                            bell_tiles += 1
                        elif tile == "M":
                            money_tiles += 1
                        pla_input_err = True
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
        num_players = raw_input("Enter number of players (1 - 4): ")
        print
        if str(num_players) not in ["1", "2", "3", "4"]:
            sound_bell()
            pass
        else:
            num_players = int(num_players)
            players_input_err = False
    game, player_bonus, goes_first = initialize_game(num_players)
    if num_players > 1:
        raw_input("Player %s goes first! Press any <Enter> to continue. " % str(goes_first+1))

    #round loop
    for round in range(1,4):
        board = initialize_board(num_players)
        (h_jkpt, d_jkpt, cont_round, cherry_tiles, orange_tiles, bell_tiles, money_tiles) = initialize_round(num_players)
        player = goes_first+1
        continue_round = False
        for item in cont_round:
            if cont_round[item]:
                continue_round = True
                
        #player loop
        while continue_round:
            if empty_cells(player) > 0:
                (h_jkpt, d_jkpt) = print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                raw_input("Player %s, press <Enter> to roll dice: " % str(player))
                print

                #roll dice
                (roll, choices, doubles, empty) = roll_dice()
                valid_cols = col_choices(player)
                print "Your roll: " + str(roll)
                print
                if doubles:
                    sound_bell()
                    print "Doubles!"
                    print

                #use or remove pit tile
                swap = False
                if board[player-1][5][5] != "_" and empty:
                    sound_bell()
                    print "You have the option to play or remove the pit tile!"
                    print
                    (valid_cols, h_jkpt, d_jkpt, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles) = pit_tile(player, round, choices, valid_cols, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles)

                #select tiles
                if empty_cells(player) > 0:
                    undo = True
                    while undo:
                        valid_cols, undo, cherry_tiles, orange_tiles, bell_tiles, money_tiles = select_tiles(player, round, choices, valid_cols, doubles, h_jkpt, d_jkpt, roll, swap, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)

                #Prompt end of turn message for multiple player games only
                if num_players > 1:
                    print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
                    raw_input("End of turn, player %s. Press <Enter> to continue. " % player)
                    print
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
        print "End of round %s." % str(round)
        print
        #high round bonus
        round_scores = {}
        for plr in range(1,len(game)+1):
            round_scores.update({plr:game[plr-1][round-1]})
        round_values = round_scores.values()
        high_score = max(round_values)
        if num_players == 1 and high_score < 350:
            raw_input("Press any key to continue. ")
            print
        else:
            high_player = []
            for k in round_scores.iterkeys():
                if round_scores[k] == high_score:
                    high_player.append(k)
            bonus_score = [30, 60, 120]
            for x in high_player:
                player_bonus[x-1][round-1] = bonus_score[round-1]
            if len(high_player) == 1:
                print "The round %s high round bonus of %s goes to player %s." % (str(round), str(bonus_score[round-1]), str(int(high_player[0])))
            else:
                print "The round %s high round bonus of %s goes to players %s." % (str(round), str(bonus_score[round-1]), str(high_player))
            print
            raw_input("Press any key to update the score and continue.")
        print_board(h_jkpt, d_jkpt, round, player, cherry_tiles, orange_tiles, bell_tiles, money_tiles)
        score_board(round, board, game, player_bonus)

    #end of game
    sound_bell()
    print "Game Over."
    print
    score_board(round, board, game, player_bonus)
    print
    again_input_err = True
    while again_input_err:
        again_yn = raw_input("Would you like to play again? (Y/N) ")
        if again_yn.upper() == "Y":
            again_input_err = False
            print
        elif again_yn.upper() == "N":
            again_input_err = False
            play_again = False
            print
            print "Thank you for playing!"
            print
        else:
            sound_bell()
            print

