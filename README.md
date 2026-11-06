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

## Scripts
### stacker.py
Using this script, you can build a rack with tiles of your choosing so you can see the score of any rack.

### rolls.py
Create a csv file with the tile_choices, double_tiles flag, and empty_pit flag for every dice roll combination.

### racks.py
Create a csv file with the score for every unique rack combination.
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
