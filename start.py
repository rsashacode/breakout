import os

from pathlib import Path

os.chdir(Path(os.getcwd()).joinpath('breakout_game'))

if __name__ == '__main__':
    from breakout_game import start
    start()
