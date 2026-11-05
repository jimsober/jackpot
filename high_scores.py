#!/usr/bin/env python3

import json
import os
import sys

from shared_logger import get_logger
LOGGER = get_logger("high_scores")

def ensure_high_scores_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    scores_path = os.path.join(script_dir, 'high_scores.json')
    default_path = os.path.join(script_dir, 'high_scores.default')

    if os.path.exists(scores_path):
        LOGGER.debug(f"High scores file exists at {scores_path}")
        return scores_path

    try:
        if os.path.exists(default_path):
            LOGGER.info(f"Creating high_scores.json from default at {default_path}")
            with open(default_path, 'r') as src, open(scores_path, 'w') as dst:
                dst.write(src.read())
            LOGGER.info(f"High scores initialized at {scores_path} from default")
        else:
            from datetime import datetime
            now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            default_data = {
                "highGame": [
                    {"players": 2, "score": 0, "user": "N/A", "date": now},
                    {"players": 3, "score": 0, "user": "N/A", "date": now},
                    {"players": 4, "score": 0, "user": "N/A", "date": now}
                ],
                "highRound": [
                    {"players": 2, "score": 0, "user": "N/A", "date": now},
                    {"players": 3, "score": 0, "user": "N/A", "date": now},
                    {"players": 4, "score": 0, "user": "N/A", "date": now}
                ]
            }
            with open(scores_path, 'w') as f:
                json.dump(default_data, f)
            LOGGER.info(f"High scores initialized at {scores_path} with minimal default structure")
    except Exception as e:
        LOGGER.error(f"Failed to initialize high_scores.json at {scores_path}: {e}")

    return scores_path

if __name__ == '__main__':
    os.system('clear')
    scores_path = ensure_high_scores_file()
    with open(scores_path) as json_file:
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

