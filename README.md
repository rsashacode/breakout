
# Breakout

A simple and fun breakout game to relive your childhood. Based on pygame framework.
Game requires python 3.11.

## Table of Contents

- [Configuration](https://github.com/rkvcode/breakout#Configuration)
- [Controls](https://github.com/rkvcode/breakout#Controls)
- [Installation](https://github.com/rkvcode/breakout#Installation)
- [Feature](https://github.com/rkvcode/breakout#Feature)
- [Prerequisites](https://github.com/rkvcode/breakout#Prerequisites)
- [Git Commit History](https://github.com/rkvcode/breakout#Git-Commit-History)
- [UML Diagrams](https://github.com/rkvcode/breakout#UML-Diagrams)
- [Unit Tests](https://github.com/rkvcode/breakout#Unit-Tests)

## Configuration
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

## References

All assets used in the game are open-source, terms of use can be found in the links provided.

### Graphics
- Ball image sourced from [manshagraphics](https://reurl.cc/A4o88e), with usage rights defined by the [License Agreement for Flaticon Content](https://reurl.cc/eL189L).
- Heart image sourced from [opengameart](https://reurl.cc/097OMk), with usage rights defined by the [CC0 1.0 Universal](https://reurl.cc/N4V6mm).
- Background graphics created with an assitance of DALL·E.
 
### Background Music
All background music tracks sourced from Pixabay, with usage rights defined under the [Pixabay Terms of Service](https://reurl.cc/v0V1Yl):
- [Track 1](https://reurl.cc/mr8j9j)
- [Track 2](https://reurl.cc/aLOjvY)
- [Track 3](https://reurl.cc/lgmjd6)
- [Track 4](https://reurl.cc/77Gvo1)
- [Track 5](https://reurl.cc/yYdjgq)
- [Track 6](https://reurl.cc/v0Yj1l)
- [Track 7](https://reurl.cc/YVgr6L)
 
### Menu Music
All Menu music tracks sourced from FesliyanStudios, with usage rights defined under the [FesliyanStudios - FAQ / Policy](https://reurl.cc/RWx1qZ):
- [Track 1](https://reurl.cc/aL2vdl)
 
### Effect Sounds
All effect sounds sourced from Pixabay:
- [Effect Sound 1](https://reurl.cc/N4vm6n)
- [Effect Sound 2](https://reurl.cc/nraj02)
- [Effect Sound 3](https://reurl.cc/zl3jzk)
- [Effect Sound 4](https://reurl.cc/xL5j0b)
- [Effect Sound 5](https://reurl.cc/mrE9yW)
 
### Power up icons
- Power up icons and blocks designed using PowerPoint by ourselves.
 
### Codebase Reference
The final version is a fully original work.

Some early commits may contain parts of code based on the tutorial "Breakout in python tutorial by Clear Code".
- [Breakout in python tutorial by Clear Code](https://reurl.cc/YVy1Va).
 
## Student Credentials
- Full Name: Aleksandr Rykov
- Matriculation Number: 3121337


- Full Name: Chen-Yu Liu
- Matriculation Number: 3121164