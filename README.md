
# Breakout

A simple and fun breakout game to relive your childhood. Based on pygame framework.
Game requires python 3.11.

It is possible to change the size of the game window by changing the value of **SELECTED_RESOLUTION**
in the settings file
[here](https://github.com/rkvcode/breakout/blob/main/breakout_game/config/settings.py)

## Controls
### Menu
- up-arrow - go up
- down-arrow - go down

### Game
- left-arrow - move paddle to the left
- right-arrow - move paddle to the right
- space - launch the ball
- esc - pause the game

There are two methods of installation:

## Installation
### Method 1 (pip)
    pip install -r -requirements.txt
    python start.py
### Method 2 (setuptools)
    python -m pip install --upgrade setuptools
    python setup.py install
    python -c "import breakout_game; breakout_game.start()"

## Table of Contents

- [Feature](https://github.com/rkvcode/breakout#Feature)
- [Prerequisites](https://github.com/rkvcode/breakout#Prerequisites)
- [Git Commit History](https://github.com/rkvcode/breakout#Git-Commit-History)
- [UML Diagrams](https://github.com/rkvcode/breakout#UML-Diagrams)
- [Unit Tests](https://github.com/rkvcode/breakout#Unit-Tests)


## Feature

The game has three difficulty levels.
Challenge three unique game modes, beyond the traditional paddle, ball, and blocks, 
We've also added special power-ups to enhance your gaming experience even more!

## Prerequisites

#### Required libraries:

- matplotlib==3.8.3
- pygame==2.5.2
- pydantic==2.6.3
- pytest==8.0.2
- pytest-mock==3.12.0
- pylint==3.1.0

## Git Commit History
- [Git Commit History](https://github.com/rkvcode/breakout/commits)

## UML Diagrams
- [UML Diagrams](https://github.com/rkvcode/breakout/tree/master/UML)

## Unit Tests
To run tests: 

python -m pytest ./tests

- [Unit Tests](https://github.com/rkvcode/breakout/tree/main/tests)

