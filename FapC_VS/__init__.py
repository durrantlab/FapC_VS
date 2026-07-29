__version__ = "0.0.0"

import logging
from pathlib import Path

def make_log_dir(FILE_LOG: Path) -> None:
    if not FILE_LOG.parent.is_dir():
        FILE_LOG.parent.mkdir(parents=True, exist_ok=True)


def enable_logging(
    FILE_LOG: Path, level: str = '20'
) -> None:
    r"""Enable logging.

    Args:
        level: Requested log level: `10` is debug, `20` is info.
        file_path: Also write logs to files here.
    """
    
    logging.basicConfig(
        filename=FILE_LOG,
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
    )
    make_log_dir(FILE_LOG)
