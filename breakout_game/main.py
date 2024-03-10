"""
Main module to start the program
"""
import os
import sys
import time

from pathlib import Path

import pygame

from breakout_game import log
from breakout_game.utils import path_utils
from breakout_game.config import settings
from breakout_game.sprites import SpriteManager
from breakout_game.screens import MainMenu, LevelMenu, EndGameMenu, PauseMenu

game_logger = log.game_logger


class Game:
    """
    The main game class.

    Handles all the updates and drawing of the objects, menus and screens.

    Attributes:
        display_surface (pygame.Surface): Main screen surface on which everything is displayed.
        title (str): The name displayed at the top of the screen. Defaults to "Breakout Game"
        clock (pygame.time.Clock): Timer to run the game at persistent time rate.
        main_menu (MainMenu): Main menu object.
        pause_menu (PauseMenu): Pause menu object.
        level_menu (LevelMenu): Level menu object.
        end_game_menu (EndGameMenu): End game menu object.
        background (pygame.Surface): The background of the game.
        sprite_manager (SpriteManager):
            The sprite manager object handling the behaviour of all sprites in the game.
        game_active (bool): Whether the game is active or not. Defaults to False.
        start_pause_time (int, float): The time when the game was set on pause. Defaults to 0.
        time_in_pause (int, float): The amount of time spent in pause. Defaults to 0.
        level (int):
            The level of the game. Defaults to 0. Must be a number from 0 to 6.
        level_difficulty (int): The difficulty of the game. Defaults to 0. Must be a number from 0 to 2.
        keys_pressed (pygame.key.ScancodeWrapper): The keys pressed during the game.

    version: 1
    """

    def __init__(self):
        # General Setup
        pygame.init()  # pylint: disable=E1101
        self.display_surface: pygame.Surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.title: str = 'Breakout Game'
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Menu
        self.main_menu: MainMenu = MainMenu()
        self.pause_menu: PauseMenu = PauseMenu()
        self.level_menu: LevelMenu = LevelMenu()
        self.end_game_menu: EndGameMenu = EndGameMenu()

        # Music
        menu_music_path: Path = path_utils.get_asset_path('sounds/menu.mp3')
        pygame.mixer.music.load(menu_music_path)
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        # Background
        self.background: pygame.Surface = self.main_menu.background

        # Sprites
        self.sprite_manager: SpriteManager = SpriteManager()

        # Pause
        self.game_active: bool = False
        self.start_pause_time: [int, float] = 0
        self.time_in_pause: [int, float] = 0

        # Game stage
        self.level: int = 0
        self.level_difficulty: int = 0

        self.keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        game_logger.debug('Game Initialised')

    def restart_game(self):
        """
        Reinitialize the game objects and start the game from scratch
        """
        # Menu
        self.main_menu = MainMenu()
        self.end_game_menu = EndGameMenu()

        # Music
        menu_music_path: Path = path_utils.get_asset_path('sounds/menu.mp3')
        pygame.mixer.music.load(menu_music_path)
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        # Background
        self.background = self.main_menu.background

        # Game Stage
        self.game_active = False
        self.start_pause_time = 0
        self.time_in_pause = 0
        self.level = 0
        self.level_difficulty = 0
        self.keys_pressed = None

        self.sprite_manager = SpriteManager()
        game_logger.info('Game restarted')

    def set_level_background(self):
        """
        Set the background of the game. RGB(125, 125, 125) color is subtracted from the image to make it darker for
        a better gaming experience.
        """
        background_path = path_utils.get_asset_path(f'images/background/level-{self.level}.jpg')
        self.background = pygame.image.load(background_path).convert()
        self.background.fill((125, 125, 125), special_flags=pygame.BLEND_RGB_SUB)  # pylint: disable=E1101
        scale_factor = max([
            settings.WINDOW_HEIGHT / self.background.get_height(),
            settings.WINDOW_WIDTH / self.background.get_width()
        ])
        scaled_width = self.background.get_width() * scale_factor
        scaled_height = self.background.get_height() * scale_factor
        self.background = pygame.transform.scale(self.background, (scaled_width, scaled_height))
        game_logger.info('Background %(background_path)s of level %(level)s is set',
                         {"background_path": background_path, "level": self.level})

    def load_level_music(self):
        """
        Load the music into the pygame.mixer and plays it.
        """
        pygame.mixer.music.unload()
        level_music_path = path_utils.get_asset_path(f'sounds/level-{self.level}.mp3')
        pygame.mixer.music.load(level_music_path)
        pygame.mixer.music.play(fade_ms=1000)
        game_logger.debug('Music %s of level %s started', level_music_path, self.level)

    def check_level_finish(self):
        """
        Checks if payer has finished the level based on the amount of blocks in the game.
        """
        if len(self.sprite_manager.block_sprites_group.sprites()) == 0:
            self.sprite_manager.ball_sprites_group.empty()
            self.sprite_manager.power_up_sprites_group.empty()

            self.game_active = False
            self.level_menu.active = True
            self.level += 1
            game_logger.info('The level %s is finished', self.level)

    def check_end_game(self):
        """
        Checks player has finished the game or lost based on health and level number.
        """
        if self.sprite_manager.player.health <= 0 or self.level > 6:
            self.game_active = False
            self.end_game_menu.active = True
            game_logger.debug('The game has ended')

    def check_events(self):
        """
        Handles the events based on key pressed during the game.

        Note:
            Possible events:

            1. The game window is closed -> ends the program.
            2. The [q] key is pressed -> ends the program.
            3. The [escape] key is pressed -> activates menu and starts timer to prevent powerup timers from counting.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                game_logger.info('The game window is closed. Exiting...')
                pygame.quit()  # pylint: disable=E1101
                sys.exit()

        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_ESCAPE] and self.game_active:  # pylint: disable=E1101
            self.pause_menu.active = True
            self.start_pause_time = time.time()
            game_logger.info('Pause activated')
        elif self.keys_pressed[pygame.K_q]:  # pylint: disable=E1101
            game_logger.info('The [q] button is pressed. Exiting...')
            pygame.quit()  # pylint: disable=E1101
            sys.exit()  # pylint: disable=E1101

    def get_last_blit_main_menu(self) -> list[list]:
        """
        Update the main menu object and get objects to render.

        Returns:
            list[list[pygame.Surface, pygame.Rect]]: Objects to use to render the main menu
        """
        self.main_menu.update(self.keys_pressed)
        self.level_difficulty = self.main_menu.selected_option
        self.display_surface.blit(self.main_menu.title_surface, self.main_menu.title_rect)
        objects_to_blit = []
        for surface, rect in self.main_menu.objects_to_blit:
            objects_to_blit.append([surface, rect])
        return objects_to_blit

    def get_last_level_menu(self) -> list[list]:
        """
        Update the level menu object and get objects to render.

        Returns:
            list[list[pygame.Surface, pygame.Rect]]: Objects to use to render the level menu
        """
        self.level_menu.update(self.keys_pressed)
        objects_to_blit = [[self.level_menu.text_surface, self.level_menu.text_rect]]
        return objects_to_blit

    def get_last_end_game_menu(self) -> list[list]:
        """
        Update the end game menu object and get objects to render.

        Note:
            If the player has pressed [ENTER] in the end game menu, returns empty list
            for compatability purposes.

        Returns:
            list[list[pygame.Surface, pygame.Rect]]: Objects to use to render the end game menu
        """
        self.end_game_menu.update(self.keys_pressed, self.sprite_manager.score.score)
        if self.end_game_menu.restart_needed:
            self.restart_game()
            return [[]]
        objects_to_blit = [[self.end_game_menu.text_surface, self.end_game_menu.text_rect]]
        return objects_to_blit

    def get_last_blit_pause_menu(self) -> list[list]:
        """
        Update the pause menu object and get objects to render.

        Returns:
            list[list[pygame.Surface, pygame.Rect]]: Objects to use to render the pause game menu
        """
        self.pause_menu.update(self.keys_pressed)
        objects_to_blit = [[self.pause_menu.text_surface, self.pause_menu.text_rect]]
        return objects_to_blit

    def init_game_stage(self):
        """
        Initialize the stage of level and start the game.
        """
        self.set_level_background()
        self.sprite_manager.init_level(self.level, self.level_difficulty)
        self.load_level_music()
        self.game_active = True
        game_logger.info('Stage of level %s initialized', self.level)

    def run_game(self, delta_time: float):
        """
        Runs the game. Updates all objects.

        Args:
            delta_time (float): time passed since the last update
        """
        self.check_level_finish()
        self.check_end_game()
        self.sprite_manager.update(delta_time, self.keys_pressed, self.time_in_pause)
        self.time_in_pause = 0
        self.start_pause_time = 0

    def draw_graphics(
            self,
            menu_objects_to_blit: list[list[pygame.Surface, pygame.Rect]]
    ):
        """
        Draw graphics.

        Checks if there are any objects returned from menu. If true, renders them, if false,
        updates the game objects.

        Args:
            menu_objects_to_blit (list[list[pygame.Surface, pygame.Rect]]): Objects passed to blit method.
        """
        self.display_surface.blit(source=self.background, dest=(0, 0))
        if len(menu_objects_to_blit) > 0:
            for menu_object_to_blit in menu_objects_to_blit:
                if len(menu_object_to_blit) > 0:
                    self.display_surface.blit(*menu_object_to_blit)
        else:
            self.sprite_manager.draw_all(self.display_surface)

        pygame.display.update()

    def run(self):
        """
        The main event loop.
        """
        while True:
            delta_time = self.clock.tick_busy_loop(settings.FPS) / 1000

            self.check_events()

            # Handle Menus
            menu_objects_to_blit = []
            if self.main_menu.active:
                menu_objects_to_blit = self.get_last_blit_main_menu()
            elif self.level_menu.active:
                menu_objects_to_blit = self.get_last_level_menu()
            elif self.end_game_menu.active:
                menu_objects_to_blit = self.get_last_end_game_menu()
            elif self.pause_menu.active:
                self.time_in_pause = time.time() - self.start_pause_time
                menu_objects_to_blit = self.get_last_blit_pause_menu()
            else:
                if not self.game_active:
                    self.init_game_stage()
                else:
                    if not self.pause_menu.active:
                        self.run_game(delta_time)

            # Graphics
            self.draw_graphics(menu_objects_to_blit)


def start():
    """
    Start the game
    """
    game = Game()
    game.run()


if __name__ == '__main__':
    working_directory = os.getcwd()
    start()
