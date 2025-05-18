# common/logging.py
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from pathlib import Path

def setup_logging(service_name: str = "app", log_dir: str = None, level: int = logging.INFO):
    """
    Initialize logging: writes to PROJECT_ROOT/logs/{service_name}_{timestamp}.log
    """
    # Compute project root: one level above common/
    project_root = Path(__file__).resolve().parents[1]
    base_log_dir = Path(log_dir) if log_dir else project_root / "logs"
    service_log_dir = base_log_dir / service_name
    service_log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d")
    log_file = service_log_dir / f"{service_name}_{timestamp}.log"

    handler = RotatingFileHandler(
        filename=str(log_file), maxBytes=10*1024*1024, backupCount=5, encoding="utf-8"
    )
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    # Avoid duplicate handlers
    if not any(isinstance(h, RotatingFileHandler) and h.baseFilename == str(log_file)
               for h in root_logger.handlers):
        root_logger.addHandler(handler)
