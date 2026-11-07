#!/usr/bin/env python3
import csv
import itertools
import os

from shared_logger import get_logger
from scoring import score_board

LOGGER = get_logger("racks")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(SCRIPT_DIR, 'racks_results.csv')


def create_board(result_string):
    board = []
    board.append([['1 2 3 4 5 6'], ['_'], ['_', '_'], ['_', '_', '_'], ['_', '_', '_', '_'], ['_', '_', '_', '_', '_', '_']])
    i = 0
    for row in range(1, 6):
        for col in range(0, 5):
            if col < row:
                board[0][row][col] = result_string[i]
                i += 1
    return board


def board_score(board):
    score, _, _ = score_board(board[0])
    return score


if __name__ == '__main__':
    csvfile = open(OUTPUT_FILE, 'w')
    filewriter = csv.writer(csvfile)
    filewriter.writerow(['score', 'board'])

    results = itertools.product('MBOC', repeat=15)
    uniqs = set()
    counter = 0

    for result in results:
        result_string = ''.join(result)
        if result_string not in uniqs:
            uniqs.add(result_string)
            board = create_board(result_string)
            score = board_score(board)
            if score > 490:
                LOGGER.debug(f"High-scoring board found: score={score}")
                counter += 1
                filewriter.writerow([score, board])

    csvfile.close()
