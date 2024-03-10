import pytest
import pygame

from breakout_game.sprites.powerup_manager import PowerUpManager
from breakout_game.sprites import SpriteManager


@pytest.fixture
def manager():
    pygame.init()
    sprite_manager = SpriteManager()
    sprite_manager.init_level()
    powerup_manager = PowerUpManager(sprite_manager)
    return powerup_manager


def test_init(manager):
    assert isinstance(manager, PowerUpManager)


def test_wrong_powerup(manager):
    with pytest.raises(KeyError):
        manager.activate_powerup("some random power")


@pytest.mark.parametrize("start_timer", [True, False])
def test_activate_big_ball(manager, start_timer):
    manager.activate_big_ball(start_timer)
    assert manager.ball_size_timer.active is start_timer


@pytest.mark.parametrize("start_timer", [True, False])
def test_activate_small_ball(manager, start_timer):
    manager.activate_small_ball(start_timer)
    assert manager.ball_size_timer.active is start_timer


@pytest.mark.parametrize("start_timer", [True, False])
def test_activate_fast_ball(manager, start_timer):
    manager.activate_fast_ball(start_timer)
    assert manager.ball_speed_timer.active is start_timer


@pytest.mark.parametrize("start_timer", [True, False])
def test_activate_slow_ball(manager, start_timer):
    manager.activate_fast_ball(start_timer)
    assert manager.ball_speed_timer.active is start_timer
