#!/usr/bin/env python
import csv
import itertools

csvfile =  open('racks_results.csv', 'w')
filewriter = csv.writer(csvfile)
filewriter.writerow(['score', 'board'])

def create_board(result_string):
#
#    print('In create_board with %s' % result_string)
    board = []
    board.append([['1 2 3 4 5 6'],['_'], ['_','_'], ['_','_','_'], ['_','_','_','_'],['_','_','_','_','_','_']])
    i = 0
    for row in range(1,6):
        for col in range(0,5):
            if col < row:
#
#                print('In the business with row %s, col %s, i %s' % (str(row), str(col), str(i)))
                board[0][row][col] = result_string[i]
                i+=1
            else:
                pass
#
#    print('Board: %s' % str(board))
    return board

def board_score(board):
#
#    print('In board_score with %s' % str(board))
    score = 0

    #horizonal consecutive tiles
    L3 = []
    for col in range(3):
        L3.append(board[0][3][col])
    grouped_L3 = [(k, sum(1 for i in g)) for k,g in itertools.groupby(L3)]
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
        L4.append(board[0][4][col])
    grouped_L4 = [(k, sum(1 for i in g)) for k,g in itertools.groupby(L4)]
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
        L5.append(board[0][5][col])
    L5.pop(5)
    grouped_L5 = [(k, sum(1 for i in g)) for k,g in itertools.groupby(L5)]
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
            elif tile == "O":
                score += 160
            elif tile == "B":
                score += 200
            elif tile == "M":
                score += 400

    #diagonal consecutive tiles
    DL3 = []
    DL3.append(board[0][3][0])
    DL3.append(board[0][4][1])
    DL3.append(board[0][5][2])
    grouped_DL3 = [(k, sum(1 for i in g)) for k,g in itertools.groupby(DL3)]
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
    DL3a.append(board[0][5][0])
    DL3a.append(board[0][4][1])
    DL3a.append(board[0][3][2])
    grouped_DL3a = [(k, sum(1 for i in g)) for k,g in itertools.groupby(DL3a)]
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
    DL4.append(board[0][2][0])
    DL4.append(board[0][3][1])
    DL4.append(board[0][4][2])
    DL4.append(board[0][5][3])
    grouped_DL4 = [(k, sum(1 for i in g)) for k,g in itertools.groupby(DL4)]
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
    DL5.append(board[0][1][0])
    DL5.append(board[0][2][1])
    DL5.append(board[0][3][2])
    DL5.append(board[0][4][3])
    DL5.append(board[0][5][4])
    grouped_DL5 = [(k, sum(1 for i in g)) for k,g in itertools.groupby(DL5)]
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
            elif tile == "O":
                score += 160
            elif tile == "B":
                score += 200
            elif tile == "M":
                score += 400

    #rack bonus
    cherry_cnt = 0
    orange_cnt = 0
    bell_cnt = 0
    money_cnt = 0
    row = 0
    while row < len(board[0]):
        col = 0
        while col < len(board[0][row]):
            if row == 5 and col == 5:
                pass
            elif board[0][row][col] == "C":
                cherry_cnt += 1
            elif board[0][row][col] == "O":
                orange_cnt += 1
            elif board[0][row][col] == "B":
                bell_cnt += 1
            elif board[0][row][col] == "M":
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
    return score

#MAIN PROGRAM
results = itertools.product('MBOC', repeat=15)
uniqs = []
counter = 0
##
miss_cnt = 0
for result in results:
    result_string = ''
    for tile in result:
        result_string += tile
##
    miss_cnt+=1
#
#    print('Try count: %s; result_string: %s' % (str(miss_cnt), result_string))
    if result_string in uniqs:
        pass
    else:
        uniqs.append(result_string)
        board = create_board(result_string)
        score = board_score(board)
        if score > 490:
            counter+=1
#
#            print('Hit count: %s; Score: %s; Board: %s' % (str(counter), str(score), str(board)))
            filewriter.writerow([score, board])

csvfile.close()
