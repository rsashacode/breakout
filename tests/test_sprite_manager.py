import pytest
import pygame
import math
from breakout import settings

from breakout.sprites.sprite_manager import SpriteManager
from breakout.sprites.sprite import Player, Score, Scoreboard, Ball, Block, Heart


@pytest.fixture
def manager():
    pygame.init()
    sprite_manager = SpriteManager()
    sprite_manager.init_level()
    return sprite_manager


def test_init(manager):
    assert isinstance(manager, SpriteManager)


def test_level(manager):
    number_of_blocks = 0
    for block_row in settings.BLOCK_MAP:
        for symbol in block_row:
            if symbol != ' ':
                number_of_blocks += 1

    assert isinstance(manager.score, Score)
    assert isinstance(manager.scoreboard, Scoreboard)
    assert isinstance(manager.player, Player)
    assert isinstance(manager.balls[0], Ball)
    assert isinstance(manager.hearts[0], Heart)
    assert isinstance(manager.blocks[0], Block)

    assert len(manager.balls) == 1
    assert len(manager.blocks) == number_of_blocks
    assert len(manager.power_ups) == 0
    assert len(manager.power_up_infos) == 0


def test_create_scoreboard(manager):
    manager.create_scoreboard()
    assert manager.scoreboard is not None


def test_create_score(manager):
    manager.create_score()
    assert manager.score is not None


def test_create_heart(manager):
    original_hearts_in_game = len(manager.hearts)
    manager.create_heart((10, 10))
    assert len(manager.hearts) == original_hearts_in_game + 1


def test_create_block(manager):
    original_blocks = len(manager.blocks)
    manager.create_block(3, 10, 10)
    manager.create_block(1, 20, 20)
    manager.create_block(5, 30, 30)
    assert len(manager.blocks) == original_blocks + 3


def test_create_player(manager):
    manager.create_player()
    assert manager.player is not None


def test_create_ball(manager):
    original_balls_in_game = len(manager.balls)
    manager.create_ball(midbottom=(10, 100), angle_radians=math.pi / 2, speed=5)
    assert len(manager.balls) == original_balls_in_game + 1


def test_init_level(manager):
    manager.init_level(level_number=1, level_difficulty=2)
    assert manager.level_difficulty == 2


def test_create_powerup(manager):
    manager.create_powerup((10, 10), "big-ball")
    assert len(manager.power_ups) == 1


def test_create_powerup_timer_info(manager):
    manager.create_powerup_timer_info("power", 5)
    assert len(manager.power_up_infos) == 1

