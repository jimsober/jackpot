# Jackpot

## Game
* 2-4 player game, single player versus 1 to 3 computer opponents.
* Each game consists of 3 rounds.
* Option to forfeit game at the end of each of the first two rounds.
* Option to play again at the end of the game.
* 4 dice, two white and two yellow (see [Dice sides](#dice-sides)).
* 3 or more of a tile in a row horizontally or diagonally scores (see [Scoring](#horizontal-or-diagonal-consecutive-tiles)).
* 5 of a tile in a row is known as a Jackpot (the name of the game).
* 7 or more of the same tiles score a rack bonus (see [Scoring](#rack-bonus)).
* Tiles can become unavailable if supply is depleted (see [Tile quantities](#tile-quantities)).

### Dice sides
* White - 2 Orange, 2 Bell, 1 Cherry, 1 Money
* Yellow - 3 Cherry, 1 Bell, 1 Orange, 1 Money

### Scoring
#### Horizontal or diagonal consecutive tiles
|Tiles|Cherry|Orange|Bell|Money|
|---|---|---|---|---|
|3|30|40|50|100|
|4|60|80|100|200|
|5|120|160|200|400|

#### Rack bonus
|Tiles|Rack bonus|
|---|---|
|9 or more|100|
|8|70|
|7|50|

### Tile quantities
* Cherry, 35
* Orange, 28
* Bell, 28
* Money, 21

## Robot Player Strategy

Computer opponents make decisions using an **Expected Value (EV)** search algorithm (`find_best_play` and `evaluate_potential_score` in `jackpot.py`). On each turn, the robot simulates all legal actions—including pit management and tile placements—and selects the play that maximizes the expected end-of-round score.

### 1. Action Exploration & Decision Tree
* **Pit Options**: When eligible (rolling 3-of-a-kind or 4-of-a-kind), the robot evaluates:
  * `KEEP`: Leaves the pit tile in place.
  * `REMOVE`: Returns the pit tile to the shared supply, freeing the pit.
  * `USE`: Drops the pit tile into any valid rack column (1–5) if it completes or advances a scoring line.
  * `SWAP`: Trades the pit tile with one of the rolled tiles (consuming one placement).
* **Tile Placement**: For each eligible rolled tile and valid column (1–5, or column 6 to stash in the pit), the robot simulates tile drops with gravity.
* **Doubles Lookahead**: When doubles are rolled, the robot performs a 2-step lookahead evaluating all pairwise placement permutations $(t_1, \text{col}_1)$ and $(t_2, \text{col}_2)$.

### 2. Heuristic Evaluation (`evaluate_potential_score`)
Each simulated board state is evaluated using a composite scoring heuristic:

$$\text{Evaluation} = \text{Score}_{\text{actual}} + \text{Potential}_{\text{lines}} + \text{Potential}_{\text{rack bonus}} + \text{Value}_{\text{pit}}$$

1. **Actual Score**: Points currently secured on the board (completed horizontal/diagonal runs and achieved rack bonuses).
2. **Line Completion Potential**:
   * Analyzes all 7 scoring lines (Rows 3–5 and 4 diagonals) for unblocked runs of length 3, 4, or 5.
   * Calculates the completion probability $P(\ge \text{needed} \mid \text{trials}, p)$ using binomial cumulative distribution based on:
     * Tile roll frequencies (Cherry: 50.6%, Orange: 36.0%, Bell: 36.0%, Money: 23.5%).
     * Number of remaining open rack cells (trials).
     * Physical tile supply remaining in the pool.
   * Marginal point gains are discounted across top candidate lines ($[1.0, 0.60, 0.30]$) to reflect realistic rack capacity.
3. **Rack Bonus Potential**:
   * Evaluates the likelihood of reaching 7, 8, or 9 tiles of a single type.
   * Incremental bonus rewards (50, 70, or 100 points) are weighted by completion probability.
4. **Pit Utility**:
   * An empty pit provides an option value of **25.0 points** as a safety buffer for unwanted future rolls.
   * A stored pit tile is valued proportionally to its tile base value (e.g., storing a Money tile is valued higher than a Cherry).

### 3. Supply Awareness
If the shared bank of a specific tile type is depleted or running low, the probability of drawing the required tiles automatically adjusts to reflect remaining supply availability, preventing the robot from pursuing uncompletable lines.

## Scripts
### jackpot.py
The main game entry point. Supports interactive play, high score tracking, and automated tournament simulation:
* `python3 jackpot.py`: Launch interactive game.
* `python3 jackpot.py -s 100 -p 4`: Simulate 100 headless AI-vs-AI games with 4 players and display statistical report.
* `python3 jackpot.py -l`: View Top-5 high score leaderboards.

### high_scores.py
Manages persistent Top-5 leaderboards for both High Game and High Round scores across 2-, 3-, and 4-player games. Run `python3 high_scores.py` to view formatted leaderboards.

### stackpot.py
Using this script, you can build a rack with tiles of your choosing so you can see the score of any rack.

### scoring.py
Shared module containing rack mechanics, coordinate gravity, line checks, and board scoring used by `jackpot.py`, `racks.py`, and `stackpot.py`.

### rolls.py
Create a csv file with the tile_choices, double_tiles flag, and empty_pit flag for every dice roll combination.

### racks.py
Create a csv file with the score for every unique rack combination.

## Command Line Options
`jackpot.py` supports several CLI arguments:

| Flag | Argument | Description |
|---|---|---|
| `-s`, `--simulate` | `<int>` | Run $N$ simulated robot games head-to-head and display an analytical report |
| `-p`, `--players` | `2`, `3`, `4` | Number of players for simulation (default: `4`) |
| `--seed` | `<int>` | Optional random seed for reproducible tournament results |
| `-l`, `--leaderboard` | none | Display Top-5 leaderboards and exit |
| `-h`, `--help` | none | Show command-line help message and options |

## High Scores
High score data is stored in `high_scores.json`. The game tracks a **Top-5 Leaderboard** for both:
* **High Game Scores**: Total cumulative scores across all 3 rounds (including round bonuses).
* **High Round Scores**: Single highest individual round score.

Each leaderboard category maintains top rankings for 2-player, 3-player, and 4-player game formats with player name, score, and timestamp.
## Configuration

The game reads settings from a `config.json` file located in the same directory as `jackpot.py`. All important files are anchored to this script directory so you can run the game from any working directory without path issues:

- `config.json` (configuration)
- `jackpot_log.json` (log output)
- `high_scores.json` (high score data)

On first launch, if `high_scores.json` doesn’t exist, the app will create it by copying `high_scores.default` if present; otherwise it creates a minimal structure.

### Options

- `logLevel` (string): One of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Controls both console and file handler levels. Default: `CRITICAL`.
- `logFile` (string): File name for the log file. Resolved relative to the script directory. Default: `jackpot_log.json`.
- `logMaxBytes` (integer): Maximum size in bytes for a single log file before rotation. Default: `1048576` (1 MB).
- `logBackupCount` (integer): Number of rotated log files to keep (`jackpot_log.json.1`, `jackpot_log.json.2`, …). Default: `5`.

### Logging

All scripts use a shared rotating JSON logger defined in 

`shared_logger.py`

Use it by importing and requesting a named logger:

```python
from shared_logger import get_logger
LOGGER = get_logger("your_module_name")
