"""Shared scoring and board mechanics for Jackpot."""

from itertools import groupby

LINE_SCORES = {
    'C': {3: 30, 4: 60, 5: 120},
    'O': {3: 40, 4: 80, 5: 160},
    'B': {3: 50, 4: 100, 5: 200},
    'M': {3: 100, 4: 200, 5: 400},
}

TILE_BASE_VALUES = {'M': 100, 'B': 50, 'O': 40, 'C': 30}
TILE_PROBABILITIES = {'C': 0.506, 'O': 0.360, 'B': 0.360, 'M': 0.235}
INITIAL_SUPPLY = {'C': 35, 'O': 28, 'B': 28, 'M': 21}
BONUS_SCORE = [30, 60, 120]

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
    """Return a deep copy of the board grid."""
    return [row[:] for row in board]


def empty_cells_count(board):
    """Count empty playable cells on board (excluding the pit at (5, 5))."""
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


def get_valid_cols(board):
    """Return 1-indexed valid columns that currently have at least one empty cell.
    Column 6 corresponds to the pit slot at (5, 5).
    """
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
    """Drop a tile into a column with gravity from bottom (row 5) up.
    Column 6 places into the pit (board[5][5]).
    Returns (success, row, col).
    """
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


def count_board_tiles(board):
    """Count tiles placed on the rack (excluding the pit at (5, 5))."""
    counts = {'C': 0, 'O': 0, 'B': 0, 'M': 0}
    for r in range(1, 6):
        for c in range(len(board[r])):
            if r == 5 and c == 5:
                continue
            tile = board[r][c]
            if tile in counts:
                counts[tile] += 1
    return counts


def calculate_rack_bonus(counts):
    """Calculate rack bonus score based on tile counts:
    - 9 or more of any tile: +100
    - 8 of a tile: +70 (plus +50 if another tile has 7)
    - 7 of a tile: +50 (plus +50 if another tile has 7)
    """
    sorted_counts = sorted(counts.values(), reverse=True)
    top = sorted_counts[0] if sorted_counts else 0
    second = sorted_counts[1] if len(sorted_counts) > 1 else 0

    bonus = 0
    if top >= 9:
        bonus += 100
    elif top == 8:
        bonus += 70
        if second == 7:
            bonus += 50
    elif top == 7:
        bonus += 50
        if second == 7:
            bonus += 50
    return bonus


def score_board(board):
    """Calculate total score for a board along with horizontal/diagonal jackpot flags.
    Returns (score, jackpot_H, jackpot_D).
    """
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
    counts = count_board_tiles(board)
    score += calculate_rack_bonus(counts)

    return score, jackpot_H, jackpot_D
