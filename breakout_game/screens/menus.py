"""
Module describing all menus present in the game.
"""
import time
import pygame

from utils.path_utils import get_asset_path
from config import settings


class MainMenu:
    """
    Main Menu to be drawn on the screen.

    Note:
        It may be better to create a parent "Screen" class.

    Attributes:
        background (pygame.Surface): Background image of the menu.
        font (pygame.font.Font): Font of the menu.
        options (list): Menu options. Defaults to ['EASY', 'NORMAL', 'HARD']
        selected_option (int): Index of the selected menu option. Defaults to 1.
        title_surface (pygame.Surface): Title of the menu.
        title_rect (pygame.Rect): Rectangle of the title of the menu.
        objects_to_blit (list[pygame.Surface, pygame.Rect]): List of pygame objects to pass later to blit method.
        active (bool): If the menu is active. Defaults to True.
        last_pressed (float): When was the last time the options changed. Used for smooth selection.
    """
    def __init__(self):
        # Load and scale the background image
        background_image_path = get_asset_path('images/background/menu.png')
        self.background = pygame.image.load(background_image_path).convert()
        self.background = pygame.transform.scale(self.background, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.background.set_alpha(20)

        # Setup font and text rendering
        self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
        self.options = ['EASY', 'NORMAL', 'HARD']
        self.selected_option = 1  # Index of the currently selected option

        # Setup objects to blit
        self.title_surface = self.font.render(
            'WELCOME TO BREAKOUT! CHOOSE YOUR DIFFICULTY:',
            True,
            (255, 255, 255))
        self.title_rect = self.title_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 4))
        self.objects_to_blit = []

        self.active = True
        self.update_objects_to_blit()

        # Used to handle smooth selection
        self.last_pressed = time.time()

    def update_objects_to_blit(self):
        """
        Update the objects to pass later to blit method.
        """
        for i, option in enumerate(self.options):
            position = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + i * settings.WINDOW_WIDTH // 15)
            if self.selected_option == i:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            surface_to_blit = self.font.render(option, True, color)
            rect_to_blit = surface_to_blit.get_rect(center=position)
            self.objects_to_blit.append([surface_to_blit, rect_to_blit])

    def update(self, keys_pressed: pygame.key.ScancodeWrapper):
        """
        Update the menu objects and selection based on pressed keys.

        Args:
            keys_pressed (pygame.key.ScancodeWrapper): Keys pressed.
        """
        if time.time() - self.last_pressed >= 0.2:
            if keys_pressed[pygame.K_UP]:  # pylint: disable=E1101
                self.selected_option = max(0, self.selected_option - 1)
                self.last_pressed = time.time()
            elif keys_pressed[pygame.K_DOWN]:  # pylint: disable=E1101
                self.selected_option = min(len(self.options) - 1, self.selected_option + 1)
                self.last_pressed = time.time()
            elif keys_pressed[pygame.K_RETURN]:  # pylint: disable=E1101
                if self.selected_option in [0, 1, 2]:
                    self.active = False
            self.update_objects_to_blit()


class LevelMenu:
    """
    Level Menu to be drawn on the screen. Showing that the level is finished.

    Note:
        It may be better to create a parent "Screen" class.

    Attributes:
        font (pygame.font.Font): Font of the menu.
        text (str): Text to render.
        text_surface (pygame.Surface): Text in form of pygame.Surface.
        text_rect (pygame.Rect): Rectangle of the surface.
        active (bool): If the menu is active. Defaults to True.
    """
    def __init__(self):
        self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
        self.text = 'CONGRATULATIONS! PRESS [ENTER] TO CONTINUE.'

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(
            center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        )
        self.active = False

    def update(self, keys_pressed: pygame.key.ScancodeWrapper):
        """
        Update the state of the menu.

        Args:
            keys_pressed (pygame.key.ScancodeWrapper): Keys pressed.
        """
        if keys_pressed[pygame.K_RETURN]:  # pylint: disable=E1101
            self.active = False


class EndGameMenu:
    """
    End Game Menu to be drawn on the screen. Showing that the player has lost or completed all levels.

    Note:
        It may be better to create a parent "Screen" class.

    Attributes:
        font (pygame.font.Font): Font of the menu.
        text (str): Text to render.
        text_surface (pygame.Surface): Text in form of pygame.Surface.
        text_rect (pygame.Rect): Rectangle of the surface.
        active (bool): If the menu is active. Defaults to True.
        restart_needed (bool): If the player decided to restart the game.
    """
    def __init__(self):
        self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
        self.text = 'END GAME. PRESS [ENTER] TO RESTART'

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(
            center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        )
        self.active = False
        self.restart_needed = False

    def update(self, keys_pressed: pygame.key.ScancodeWrapper, score: int):
        """
        Update the state of the Menu. Checks if the player has pressed the restart game button.

        Args:
            keys_pressed (pygame.key.ScancodeWrapper): Keys pressed.
            score (int): Current game score.
        """
        self.text = f'YOUR FINAL SCORE: {score}. PRESS [ENTER] TO RESTART'
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(
            center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        )
        if self.active:
            if keys_pressed[pygame.K_RETURN]:
                self.active = False
                self.restart_needed = True


class PauseMenu:
    """
    Pause Menu to be drawn on the screen. Is showed during the pause

    Note:
        It may be better to create a parent "Screen" class.

    Attributes:
        font (pygame.font.Font): Font of the menu.
        text (str): Text to render.
        text_surface (pygame.Surface): Text in form of pygame.Surface.
        text_rect (pygame.Rect): Rectangle of the surface.
        active (bool): If the menu is active. Defaults to True.
    """
    def __init__(self):
        self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
        self.text = 'PAUSE. PRESS [SPACE] TO CONTINUE.'

        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(
            center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
        )
        self.active = False

    def update(self, keys_pressed: pygame.key.ScancodeWrapper):
        """
        Update the pause menu.

        Args:
            keys_pressed (pygame.key.ScancodeWrapper): Keys pressed.
        """
        if keys_pressed[pygame.K_SPACE]:  # pylint: disable=E1101
            self.active = False
