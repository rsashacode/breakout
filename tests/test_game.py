import pygame

from breakout.main import Game


def test_restart_game():
    game = Game()
    game.restart_game()
    assert game.game_active is False
    assert game.start_pause_time == 0


def test_set_level_background():
    game = Game()
    game.set_level_background()
    assert isinstance(game.background, pygame.Surface)


def test_load_level_music():
    game = Game()
    game.load_level_music()
    assert pygame.mixer.music.get_busy() is True


def test_get_last_blit_main_menu():
    game = Game()
    result = game.get_last_blit_main_menu()
    assert isinstance(result, list)
