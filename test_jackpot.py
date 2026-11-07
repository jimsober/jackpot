import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import jackpot


class TestJackpotRobot(unittest.TestCase):
    def setUp(self):
        self.board = jackpot.initialize_rack(1)[0]
        self.supply = {'C': 35, 'O': 28, 'B': 28, 'M': 21}

    def test_drop_tile(self):
        b = jackpot.copy_board(self.board)
        # Drop into col 1 (should land at row 5, col 0)
        ok, r, c = jackpot.drop_tile(b, 1, 'M')
        self.assertTrue(ok)
        self.assertEqual((r, c), (5, 0))
        self.assertEqual(b[5][0], 'M')

        # Drop into col 1 again (should land at row 4, col 0)
        ok, r, c = jackpot.drop_tile(b, 1, 'M')
        self.assertTrue(ok)
        self.assertEqual((r, c), (4, 0))
        self.assertEqual(b[4][0], 'M')

        # Drop into pit (col 6)
        ok, r, c = jackpot.drop_tile(b, 6, 'C')
        self.assertTrue(ok)
        self.assertEqual((r, c), (5, 5))
        self.assertEqual(b[5][5], 'C')

        # Second drop into pit should fail
        ok, r, c = jackpot.drop_tile(b, 6, 'O')
        self.assertFalse(ok)

    def test_score_board_horizontal_jackpot(self):
        b = jackpot.copy_board(self.board)
        for c in range(5):
            b[5][c] = 'M'
        score, jh, jd = jackpot.score_board(b)
        # 5 M in row 5 = 400
        self.assertEqual(score, 400)
        self.assertTrue(jh)
        self.assertFalse(jd)

    def test_score_board_diagonal_jackpot(self):
        b = jackpot.copy_board(self.board)
        coords = [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)]
        for r, c in coords:
            b[r][c] = 'M'
        score, jh, jd = jackpot.score_board(b)
        self.assertEqual(score, 400)
        self.assertFalse(jh)
        self.assertTrue(jd)

    def test_doubles_play_considers_two_placements(self):
        b = jackpot.copy_board(self.board)
        # Empty board, rolled doubles with choices ['C', 'O', 'B', 'M']
        play, eval_score, final_b, final_s = jackpot.find_best_play(
            b, ['C', 'O', 'B', 'M'], doubles=True, empty=True, supply=self.supply
        )
        pit_act, placements = play
        self.assertEqual(len(placements), 2)
        # Both placements should place Money for highest potential
        self.assertEqual(placements[0][0], 'M')
        self.assertEqual(placements[1][0], 'M')

    def test_pit_tile_stash_unwanted_tile(self):
        b = jackpot.copy_board(self.board)
        # Row 5 has 2 Moneys
        b[5][4] = 'M'
        b[5][3] = 'M'
        # Roll an unwanted Orange (not empty, doubles=False)
        play, eval_score, final_b, final_s = jackpot.find_best_play(
            b, ['O'], doubles=False, empty=False, supply=self.supply
        )
        pit_act, placements = play
        # Should place O in col 6 (pit) to protect the Row 5 Money run
        self.assertEqual(placements, [('O', 6)])
        self.assertEqual(final_b[5][5], 'O')
        self.assertEqual(final_b[5][3], 'M')
        self.assertEqual(final_b[5][4], 'M')

    def test_pit_tile_empty_when_advantageous(self):
        b = jackpot.copy_board(self.board)
        b[5][4] = 'M'
        b[5][3] = 'M'
        b[5][5] = 'O'  # unwanted tile in pit
        # Roll Money with 3-of-a-kind (empty=True)
        play, eval_score, final_b, final_s = jackpot.find_best_play(
            b, ['M'], doubles=False, empty=True, supply=self.supply
        )
        pit_act, placements = play
        # Pit action should be REMOVE (clearing pit)
        self.assertEqual(pit_act, ('REMOVE',))
        self.assertEqual(final_b[5][5], '_')

    def test_pit_tile_use_when_matching(self):
        b = jackpot.copy_board(self.board)
        # Row 5 has M M M _ in cols 4, 3, 2
        b[5][4] = 'M'
        b[5][3] = 'M'
        b[5][2] = 'M'
        # Pit holds 'M'!
        b[5][5] = 'M'
        # Roll 'M' with empty=True
        play, eval_score, final_b, final_s = jackpot.find_best_play(
            b, ['M'], doubles=False, empty=True, supply=self.supply
        )
        pit_act, placements = play
        # Pit tile M should be USED to fill Row 5 col 2 (idx 1), and rolled M completes Jackpot!
        self.assertEqual(pit_act[0], 'USE')
        score, jh, jd = jackpot.score_board(final_b)
        self.assertTrue(jh)
        self.assertGreaterEqual(score, 400)

    def test_supply_conservation(self):
        # Test that total tiles in board + supply + pit remains constant
        initial_supply = {'C': 35, 'O': 28, 'B': 28, 'M': 21}
        initial_total = sum(initial_supply.values())

        b = jackpot.copy_board(self.board)
        s = initial_supply.copy()

        # Simulate 15 turns
        import random
        for _ in range(15):
            choices = random.choice([['C'], ['M'], ['O', 'B'], ['C', 'M'], ['C', 'O', 'B', 'M']])
            doubles = (choices == ['C', 'O', 'B', 'M'] and random.random() < 0.2)
            empty = (len(choices) == 1 or doubles)
            play, _, b, s = jackpot.find_best_play(b, choices, doubles, empty, s)

            board_tiles = 0
            for r in range(1, 6):
                for c in range(len(b[r])):
                    if b[r][c] != '_':
                        board_tiles += 1
            current_total = board_tiles + sum(s.values())
            self.assertEqual(initial_total, current_total)

    def test_auto_play_executes_cleanly(self):
        jackpot.rack = jackpot.initialize_rack(2)
        rack = jackpot.rack
        h_jkpt, d_jkpt, cont_round, preferences, c, o, b, m = jackpot.initialize_round(2)
        valid_cols = jackpot.col_choices(2)

        import builtins
        orig_input = builtins.input
        builtins.input = lambda *args: ""
        try:
            # Turn 1
            valid_cols, rack, preferences, h_jkpt, d_jkpt, c, o, b, m = jackpot.auto_play(
                2, rack, preferences, 1, ['C', 'M'], valid_cols, False, h_jkpt, d_jkpt, ['C', 'C', 'M', 'O'], False, c, o, b, m
            )
            self.assertEqual(jackpot.empty_cells(2), 14)

            # Turn 2: doubles
            valid_cols, rack, preferences, h_jkpt, d_jkpt, c, o, b, m = jackpot.auto_play(
                2, rack, preferences, 1, ['C', 'O', 'B', 'M'], valid_cols, True, h_jkpt, d_jkpt, ['M', 'M', 'M', 'M'], True, c, o, b, m
            )
            self.assertEqual(jackpot.empty_cells(2), 12)
        finally:
            builtins.input = orig_input

    def test_pit_tile_swap_single_choice(self):
        jackpot.rack = jackpot.initialize_rack(2)
        jackpot.rack[0][5][5] = 'O'
        import builtins
        orig_input = builtins.input
        builtins.input = lambda *args: 'S'
        try:
            valid_cols, h_jkpt, d_jkpt, swap, c, o, b, m = jackpot.pit_tile(
                1, 1, ['C'], [1, 2, 3, 4, 5], False, False, ['C', 'C', 'C', 'O'], False, 10, 10, 10, 10
            )
            self.assertTrue(swap)
            self.assertEqual(jackpot.rack[0][5][5], 'C')
            self.assertEqual(c, 9)
            self.assertEqual(o, 11)
        finally:
            builtins.input = orig_input

    def test_pit_tile_swap_multiple_choices(self):
        jackpot.rack = jackpot.initialize_rack(2)
        jackpot.rack[0][5][5] = 'O'
        import builtins
        orig_input = builtins.input
        inputs = ['S', 'M']
        builtins.input = lambda *args: inputs.pop(0)
        try:
            valid_cols, h_jkpt, d_jkpt, swap, c, o, b, m = jackpot.pit_tile(
                1, 1, ['C', 'M'], [1, 2, 3, 4, 5], False, False, ['C', 'C', 'M', 'M'], False, 10, 10, 10, 10
            )
            self.assertTrue(swap)
            self.assertEqual(jackpot.rack[0][5][5], 'M')
            self.assertEqual(m, 9)
            self.assertEqual(o, 11)
        finally:
            builtins.input = orig_input

    def test_high_scores_player_identification(self):
        import tempfile
        import json
        import getpass

        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            tmp_path = f.name
            json.dump({
                'highGame': [{'players': 4, 'score': 1000, 'user': 'Player 4', 'date': '01/01/2019 09:00:00'}],
                'highRound': [{'players': 4, 'score': 400, 'user': 'Player 4', 'date': '01/01/2019 09:00:00'}]
            }, f)

        orig_ensure = jackpot.ensure_high_scores_file
        jackpot.ensure_high_scores_file = lambda: tmp_path
        try:
            # Player 3 setting high round score
            jackpot.high_scores('ROUND', 3, 550, 4, 1)
            with open(tmp_path) as f:
                data = json.load(f)
            self.assertEqual(data['highRound'][0]['user'], 'Player 3')

            # Player 1 setting high game score
            jackpot.high_scores('GAME', 1, 1500, 4, 3)
            with open(tmp_path) as f:
                data = json.load(f)
            self.assertEqual(data['highGame'][0]['user'], getpass.getuser())
        finally:
            jackpot.ensure_high_scores_file = orig_ensure
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_rack_bonus_calculation(self):
        import scoring
        self.assertEqual(scoring.calculate_rack_bonus({'C': 9, 'O': 2, 'B': 1, 'M': 1}), 100)
        self.assertEqual(scoring.calculate_rack_bonus({'C': 8, 'O': 7, 'B': 0, 'M': 0}), 120)
        self.assertEqual(scoring.calculate_rack_bonus({'C': 7, 'O': 7, 'B': 1, 'M': 0}), 100)
        self.assertEqual(scoring.calculate_rack_bonus({'C': 8, 'O': 3, 'B': 2, 'M': 1}), 70)
        self.assertEqual(scoring.calculate_rack_bonus({'C': 7, 'O': 4, 'B': 2, 'M': 1}), 50)
        self.assertEqual(scoring.calculate_rack_bonus({'C': 6, 'O': 5, 'B': 2, 'M': 1}), 0)

    def test_check_supply_parameters(self):
        # Explicit supply parameters
        self.assertTrue(jackpot.check_supply('C', cherry_tiles=5, orange_tiles=0, bell_tiles=0, money_tiles=0))
        self.assertFalse(jackpot.check_supply('C', cherry_tiles=0, orange_tiles=5, bell_tiles=5, money_tiles=5))
        self.assertTrue(jackpot.check_supply('M', cherry_tiles=0, orange_tiles=0, bell_tiles=0, money_tiles=1))
        self.assertFalse(jackpot.check_supply('M', cherry_tiles=0, orange_tiles=0, bell_tiles=0, money_tiles=0))

    def test_select_tiles_depleted_supply_filtering(self):
        import builtins
        orig_input = builtins.input
        inputs = ["1", ""]
        builtins.input = lambda *args: inputs.pop(0) if inputs else ""
        try:
            jackpot.rack = jackpot.initialize_rack(1)
            jackpot.game, jackpot.player_bonus, _ = jackpot.initialize_game(1)
            # C and O both depleted, only B available
            choices = ['C', 'O', 'B']
            valid_cols, undo, c, o, b, m = jackpot.select_tiles(
                1, 1, choices, [1, 2, 3, 4, 5], False, {0: False}, {0: False},
                ['C', 'O', 'B', 'M'], False, 0, 0, 5, 0
            )
            # Only B could be selected and placed
            self.assertEqual(b, 4)
            self.assertEqual(jackpot.rack[0][5][0], 'B')
        finally:
            builtins.input = orig_input

    def test_shared_scoring_consistency(self):
        import racks
        import stackpot
        import scoring

        # Create identical sample rack
        sample = racks.create_board('MMMMMOOOOBBBCCC')
        score1, jh1, jd1 = scoring.score_board(sample[0])
        score2 = racks.board_score(sample)
        score3, jh3, jd3 = stackpot.board_score(1, sample)

        self.assertEqual(score1, score2)
        self.assertEqual(score1, score3)
        self.assertEqual(jh1, jh3)
        self.assertEqual(jd1, jd3)

    def test_high_scores_top_five_ranking_and_truncation(self):
        import tempfile
        import json
        import high_scores

        with tempfile.NamedTemporaryFile('w', delete=False) as f:
            tmp_path = f.name
            json.dump({'highGame': [], 'highRound': []}, f)

        try:
            scores_to_add = [500, 1200, 800, 1500, 950, 700]
            for s in scores_to_add:
                high_scores.record_high_score('GAME', f'User_{s}', s, 4, max_entries=5, scores_path=tmp_path)

            data = high_scores.load_high_scores(tmp_path)
            game_4p = [e for e in data['highGame'] if e['players'] == 4]
            # Must have exactly 5 entries
            self.assertEqual(len(game_4p), 5)
            # Scores must be sorted descending: [1500, 1200, 950, 800, 700]
            scores_in_file = [e['score'] for e in game_4p]
            self.assertEqual(scores_in_file, [1500, 1200, 950, 800, 700])
            self.assertEqual(game_4p[0]['user'], 'User_1500')
            self.assertEqual(game_4p[4]['user'], 'User_700')
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_simulation_tournament_structure(self):
        import io
        from contextlib import redirect_stdout

        stats = jackpot.simulate_tournament(num_games=3, num_players=2, seed=42)
        self.assertEqual(stats['num_games'], 3)
        self.assertEqual(stats['num_players'], 2)
        self.assertGreater(stats['duration_seconds'], 0)
        self.assertEqual(len(stats['all_game_scores']), 6)
        self.assertIn('wins', stats)
        self.assertIn('ties', stats)

        f = io.StringIO()
        with redirect_stdout(f):
            jackpot.print_simulation_report(stats)
        output = f.getvalue()
        self.assertIn("JACKPOT TOURNAMENT SIMULATION REPORT", output)
        self.assertIn("PLAYER PERFORMANCE BY SEAT", output)

    def test_high_scores_formatting(self):
        import high_scores
        output = high_scores.format_leaderboard()
        self.assertIn("JACKPOT LEADERBOARDS", output)
        self.assertIn("HIGH GAME SCORES", output)
        self.assertIn("HIGH ROUND SCORES", output)


if __name__ == '__main__':
    unittest.main()
