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

- `debug` (boolean): Legacy switch. If `true` and the `LOG_LEVEL` environment variable is not set, forces `DEBUG` logging (overrides `logLevel`). Default: `false`.
- `logLevel` (string): One of `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`. Controls both console and file handler levels. Default: `INFO`.
- `logFile` (string): File name for the log file. Resolved relative to the script directory. Default: `jackpot_log.json`.
- `logMaxBytes` (integer): Maximum size in bytes for a single log file before rotation. Default: `1048576` (1 MB).
- `logBackupCount` (integer): Number of rotated log files to keep (`jackpot_log.json.1`, `jackpot_log.json.2`, …). Default: `5`.

### Logging

The app uses Python’s `logging` framework with a rotating file handler and JSON-formatted file logs:

- File logs: JSON entries written to `logFile`. Each record includes `time` (ISO 8601 with timezone), `level`, `name`, `message`, `module`, `func`, `line`, and optional `exc_info` when exceptions occur.
- Console logs: Human-readable text with timestamp, level, and message.
- Rotation: When the log file size reaches `logMaxBytes`, it is rotated to `logFile.1`; older files are shifted and the oldest is dropped after `logBackupCount` backups.
- Level precedence: `LOG_LEVEL` environment variable overrides `config.json`. If unset, the legacy `debug` flag can force `DEBUG`; otherwise `logLevel` is used.
- Paths: `config.json`, `high_scores.json`, and `logFile` are all resolved relative to the directory containing `jackpot.py`.

Example JSON log entry:

```json
{"time":"2026-10-31T12:34:56-07:00","level":"INFO","name":"jackpot","message":"Starting game with log level INFO","module":"jackpot","func":"<module>","line":123}

