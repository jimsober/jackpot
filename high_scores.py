#!/usr/local/bin/python3

import json
import os

os.system('clear')
with open('high_scores.json') as json_file:
    data = json.load(json_file)
    print('High Game Scores')
    print('----------------')
    print('Game     Score Name     Date')
    for p in range(2,5):
        for g in data['highGame']:
            if g['players'] == p:
                print(str(p)+'-player ', end = ' ')
                print(' '*(4-len(str(g['score'])))+str(g['score']), end = ' ')
                print(g['user'], end = ' ')
                print(' '*(8 - len(g['user']))+g['date'])
            else:
                pass

    print()
    print('High Round Scores')
    print('-----------------')
    print('Game     Score Name     Date')
    for p in range(2,5):
        for r in data['highRound']:
            if r['players'] == p:
                print(str(p)+'-player  ', end = ' ')
                print(' '*(3-len(str(r['score'])))+str(r['score']), end = ' ')
                print(r['user'], end = ' ')
                print(' '*(8 - len(r['user']))+r['date'])
            else:
                pass
print()
