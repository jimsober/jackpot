#!/usr/bin/env python3

import json
import os
import sys
from datetime import datetime

from shared_logger import get_logger
LOGGER = get_logger("high_scores")

DEFAULT_MAX_ENTRIES = 5


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


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
                json.dump(default_data, f, indent=2)
            LOGGER.info(f"High scores initialized at {scores_path} with minimal default structure")
    except Exception as e:
        LOGGER.error(f"Failed to initialize high_scores.json at {scores_path}: {e}")

    return scores_path


def load_high_scores(scores_path=None):
    """Load high score data from file with fallback if missing or corrupt."""
    if scores_path is None:
        scores_path = ensure_high_scores_file()
    try:
        with open(scores_path, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
            data.setdefault('highGame', [])
            data.setdefault('highRound', [])
            return data
    except Exception as e:
        LOGGER.warning(f"Error loading high scores from {scores_path}: {e}")
        return {"highGame": [], "highRound": []}


def save_high_scores(data, scores_path=None):
    """Save high score data to JSON file."""
    if scores_path is None:
        scores_path = ensure_high_scores_file()
    try:
        with open(scores_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        LOGGER.error(f"Failed to save high scores to {scores_path}: {e}")
        return False


def record_high_score(scope, player_name, score, num_players, max_entries=DEFAULT_MAX_ENTRIES, scores_path=None):
    """Evaluate and record a score into the Top-N leaderboard.
    scope: 'GAME' or 'ROUND'
    Returns: (qualified: bool, rank: int, message: str)
    """
    key = 'highGame' if scope.upper() == 'GAME' else 'highRound'
    data = load_high_scores(scores_path)
    now_str = datetime.now().strftime("%m/%d/%Y %H:%M:%S")

    all_entries = data.get(key, [])
    # Separate entries for this player count from others
    matching = [e for e in all_entries if e.get('players') == num_players]
    others = [e for e in all_entries if e.get('players') != num_players]

    # Remove placeholder N/A entries if real scores exist
    matching = [e for e in matching if e.get('user') != 'N/A' or e.get('score', 0) > 0]

    # Check if this score qualifies for the top N
    is_top_score = False
    rank = 0

    if len(matching) < max_entries or score > min(e['score'] for e in matching):
        is_top_score = True
        new_entry = {
            'players': num_players,
            'score': score,
            'user': player_name,
            'date': now_str
        }
        matching.append(new_entry)
        # Sort descending by score, tie-breaking by date descending
        matching.sort(key=lambda x: (x.get('score', 0)), reverse=True)
        # Keep top max_entries
        matching = matching[:max_entries]

        if new_entry in matching:
            rank = matching.index(new_entry) + 1
        else:
            is_top_score = False

    if is_top_score:
        data[key] = others + matching
        save_high_scores(data, scores_path)

        scope_name = "game" if scope.upper() == "GAME" else "round"
        if rank == 1:
            msg = f"Congratulations, {player_name}! Your {scope_name} score of {score} is a new {num_players}-player high {scope_name} score!!!"
        else:
            msg = f"Congratulations, {player_name}! Your {scope_name} score of {score} is #{rank} on the {num_players}-player leaderboard!"
        return True, rank, msg
    else:
        # Check if tied
        highest = matching[0]['score'] if matching else 0
        if score == highest and highest > 0:
            top_user = matching[0].get('user', 'Unknown')
            top_date = matching[0].get('date', '')
            scope_name = "game" if scope.upper() == "GAME" else "round"
            msg = f"Congratulations, {player_name}! Your {scope_name} score ties the {num_players}-player high {scope_name} score of {score} by {top_user} on {top_date}!"
            return False, 0, msg
        return False, 0, ""


def format_leaderboard(data=None, max_entries=DEFAULT_MAX_ENTRIES):
    """Format high score data into an attractive CLI leaderboard table."""
    if data is None:
        data = load_high_scores()

    lines = []
    lines.append("=" * 68)
    lines.append("                         JACKPOT LEADERBOARDS                       ")
    lines.append("=" * 68)

    sections = [("HIGH GAME SCORES", "highGame"), ("HIGH ROUND SCORES", "highRound")]

    for title, key in sections:
        lines.append(f"\n--- {title} ---")
        lines.append(f"{'Mode':<11} {'Rank':<6} {'Score':>6}  {'Player':<16} {'Date'}")
        lines.append("-" * 68)

        entries = data.get(key, [])
        for p in range(2, 5):
            p_entries = [e for e in entries if e.get('players') == p]
            p_entries.sort(key=lambda x: x.get('score', 0), reverse=True)
            p_entries = p_entries[:max_entries]

            if not p_entries:
                lines.append(f"{p}-player    None recorded")
            else:
                for idx, entry in enumerate(p_entries):
                    mode_label = f"{p}-player" if idx == 0 else ""
                    rank_label = f"#{idx + 1}"
                    score_val = entry.get('score', 0)
                    user_val = entry.get('user', 'N/A')[:15]
                    date_val = entry.get('date', 'N/A')
                    lines.append(f"{mode_label:<11} {rank_label:<6} {score_val:>6}  {user_val:<16} {date_val}")
        lines.append("-" * 68)

    return "\n".join(lines)


def print_leaderboard(data=None):
    print(format_leaderboard(data))


if __name__ == '__main__':
    clear_screen()
    print_leaderboard()
    print()
