#!/usr/bin/env python3

import os
import sys

from shared_logger import get_logger
from scoring import score_board

LOGGER = get_logger("stackpot")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize_game(num_players):
    game = {}
    for i in range(num_players):
        game.update({i: [0, 0, 0]})
    return game


def initialize_board(num_players):
    board = []
    for i in range(num_players):
        board.append([["1 2 3 4 5 6"], ["_"], ["_", "_"], ["_", "_", "_"], ["_", "_", "_", "_"], ["_", "_", "_", "_", "_", "_"]])
    return board


def board_score(player, board):
    return score_board(board[player - 1])


def print_board(round_num, player, board, game):
    clear_screen()
    row = 0
    while row < len(board[player - 1]):
        col = 0
        while col < len(board[player - 1][row]):
            tile = board[player - 1][row][col]
            if tile == "C":
                print("\u001b[31m" + tile + "\u001b[0m", end=' ')
            elif tile == "O":
                print("\u001b[38;5;208m" + tile + "\u001b[0m", end=' ')
            elif tile == "B":
                print("\u001b[34m" + tile + "\u001b[0m", end=' ')
            elif tile == "M":
                print("\u001b[32m" + tile + "\u001b[0m", end=' ')
            else:
                print(tile, end=' ')
            col += 1
        print("\r")
        row += 1
    print()
    score_results = board_score(player, board)
    score = score_results[0]
    jackpot_H = score_results[1]
    jackpot_D = score_results[2]
    game[player - 1][round_num - 1] = score
    print(f"Score: {score}")
    if jackpot_H:
        print("Horizontal Jackpot!")
    if jackpot_D:
        print("Diagonal Jackpot!")
    print()


def sound_bell():
    sys.stdout.write('\a')
    sys.stdout.flush()


if __name__ == '__main__':
    play_again = True
    while play_again:
        clear_screen()
        game = initialize_game(1)
        board = initialize_board(1)
        tile_count = 1
        while tile_count < 16:
            for row in range(5, 0, -1):
                for col in range(4, -1, -1):
                    if col < row:
                        sel_input_err = True
                        while sel_input_err:
                            selection = input('Select a tile from [C, O, B, M]: ')
                            print()
                            if selection.upper() in ['C', 'O', 'B', 'M']:
                                sel_input_err = False
                                board[0][row][col] = selection.upper()
                            else:
                                sound_bell()
                        print_board(1, 1, board, game)
                        tile_count += 1
        sound_bell()
        print("Game Over.\n")
        print_board(1, 1, board, game)
        again_input_err = True
        while again_input_err:
            again_yn = input("Would you like to play again? (Y/N) ")
            if again_yn.upper() == "Y":
                again_input_err = False
                print()
            elif again_yn.upper() == "N":
                again_input_err = False
                play_again = False
                print("\nThank you for playing!\n")
            else:
                sound_bell()
                print()
