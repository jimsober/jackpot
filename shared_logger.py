import os
import sys
import json
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

def _load_config():
    # Defaults align with README
    default = {
        "debug": False,
        "logLevel": "CRITICAL",
        "logFile": "jackpot_log.json",
        "logMaxBytes": 1048576,
        "logBackupCount": 5,
    }
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    try:
        if not os.path.exists(cfg_path):
            with open(cfg_path, 'w') as f:
                json.dump(default, f, indent=2)
        else:
            with open(cfg_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    for k in default.keys():
                        if k in data:
                            default[k] = data[k]
    except Exception:
        # Use defaults if config is missing or invalid
        pass
    return default

load_config = _load_config

def save_config(cfg):
    cfg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
    try:
        with open(cfg_path, 'w') as f:
            json.dump(cfg, f, indent=2)
    except Exception:
        pass

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "time": datetime.fromtimestamp(record.created).astimezone().isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload)

def get_logger(name: str) -> logging.Logger:
    """Return a configured logger that writes JSON logs to a rotating file and to console.
    Configuration is read from config.json in the script directory and overridden by LOG_LEVEL.
    """
    cfg = _load_config()
    env_level = os.getenv("LOG_LEVEL", "").upper().strip()
    if env_level:
        level_name = env_level
    elif cfg.get("debug"):
        level_name = "DEBUG"
    else:
        level_name = str(cfg.get("logLevel", "CRITICAL")).upper()
    level = getattr(logging, level_name, logging.CRITICAL)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_file = os.path.join(script_dir, str(cfg.get("logFile", "jackpot_log.json")))

    # Avoid duplicate handlers if called multiple times
    if not logger.handlers:
        try:
            max_bytes = int(cfg.get("logMaxBytes", 1048576))
        except (ValueError, TypeError):
            max_bytes = 1048576

        try:
            backup_count = int(cfg.get("logBackupCount", 5))
        except (ValueError, TypeError):
            backup_count = 5

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(JsonFormatter())
        logger.addHandler(file_handler)

        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
        logger.addHandler(console)
    else:
        for handler in logger.handlers:
            handler.setLevel(level)

    return logger
