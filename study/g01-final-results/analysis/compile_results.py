import logging
from pathlib import Path

DIR_SCRIPT: Path = Path(__file__).parent.resolve()
DIR_STUDY: Path = Path(DIR_SCRIPT / ".." / "..").resolve()
FILE_LOG: Path = (
    DIR_SCRIPT / ".." / "logs" / f"{Path(__file__).name.split('.')[0]}.log"
).resolve()


def main():
    pass


if __name__ == "__main__":
    # inputs

    main()
