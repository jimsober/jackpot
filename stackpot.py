#!/usr/bin/python
#

import os
import sys
from itertools import groupby

def initialize_game(num_players):
    game = {}
    for i in range(num_players):
        game.update({i:[0, 0, 0]})
    return game

def initialize_board(num_players):
    board = []
    for i in range(num_players):
        board.append([["1 2 3 4 5 6"],["_"], ["_","_"], ["_","_","_"], ["_","_","_","_"],["_","_","_","_","_","_"]])
    return board

def board_score(player):
    score = 0
    jackpot_H = False
    jackpot_D = False

    #horizonal consecutive tiles
    L3 = []
    for col in range(3):
        L3.append(board[player-1][3][col])
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
        L4.append(board[player-1][4][col])
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
        L5.append(board[player-1][5][col])
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
    DL3.append(board[player-1][3][0])
    DL3.append(board[player-1][4][1])
    DL3.append(board[player-1][5][2])
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
    DL3a.append(board[player-1][5][0])
    DL3a.append(board[player-1][4][1])
    DL3a.append(board[player-1][3][2])
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
    DL4.append(board[player-1][2][0])
    DL4.append(board[player-1][3][1])
    DL4.append(board[player-1][4][2])
    DL4.append(board[player-1][5][3])
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
    DL5.append(board[player-1][1][0])
    DL5.append(board[player-1][2][1])
    DL5.append(board[player-1][3][2])
    DL5.append(board[player-1][4][3])
    DL5.append(board[player-1][5][4])
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
    while row < len(board[player-1]):
        col = 0
        while col < len(board[player-1][row]):
            if row == 5 and col == 5:
                pass
            elif board[player-1][row][col] == "C":
                cherry_cnt += 1
            elif board[player-1][row][col] == "O":
                orange_cnt += 1
            elif board[player-1][row][col] == "B":
                bell_cnt += 1
            elif board[player-1][row][col] == "M":
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

def print_board(round, player):
    os.system('clear')
    total = []
    total.append(0)
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

def sound_bell():
    sys.stdout.write('\a')
    sys.stdout.flush()

#MAIN PROGRAM
play_again = True

#game loop
while play_again:
    os.system('clear')
    game = initialize_game(1)
    board = initialize_board(1)
    tile_count = 1
    while tile_count < 16:
        for row in range(5,0,-1):
            for col in range(4,-1,-1):
                if col < row:
                    sel_input_err = True
                    while sel_input_err:
                        selection = raw_input('Select a tile from [C, O, B, M]: ')
                        print
                        if selection.upper() in ['C','O','B','M']:
                            sel_input_err = False
                            board[0][row][col] = selection.upper()
                        else:
                            sound_bell()
                else:
                    pass
                print_board(0, 1)
                tile_count += 1
    #end of game
    sound_bell()
    print "Game Over."
    print
    print_board(0, 1)
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
