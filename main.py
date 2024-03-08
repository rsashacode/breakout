import pygame
import settings
import sys
import time
import utils

from sprites.sprite_manager import SpriteManager
from screens import MainMenu, LevelMenu, EndGameMenu, PauseMenu


class Game:
    def __init__(self):
        # General Setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.title = 'Breakout Game'
        self.clock = pygame.time.Clock()

        # Menu
        self.main_menu = MainMenu()
        self.pause_menu = PauseMenu()
        self.level_menu = LevelMenu()
        self.end_game_menu = EndGameMenu()

        # Music
        self.menu_music_path = utils.get_asset_path('sounds/menu.mp3')
        pygame.mixer.music.load(self.menu_music_path)
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(-1)

        # Background
        self.background = self.main_menu.background

        # Sprites
        self.sprite_manager = SpriteManager()

        # Game Stage
        self.game_active = False
        self.start_pause_time = 0
        self.time_in_pause = 0
        self.level = 0
        self.level_difficulty = 0
        self.keys_pressed = None

    def restart_game(self):
        # Menu
        self.main_menu = MainMenu()
        self.end_game_menu = EndGameMenu()

        # Music
        pygame.mixer.music.load(self.menu_music_path)
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

    def set_level_background(self):
        background_path = utils.get_asset_path(f'images/background/level-{self.level}.jpg')
        self.background = pygame.image.load(background_path).convert()
        self.background.fill((125, 125, 125), special_flags=pygame.BLEND_RGB_SUB)
        scale_factor = max([
            settings.WINDOW_HEIGHT / self.background.get_height(),
            settings.WINDOW_WIDTH / self.background.get_width()
        ])
        scaled_width = self.background.get_width() * scale_factor
        scaled_height = self.background.get_height() * scale_factor
        self.background = pygame.transform.scale(self.background, (scaled_width, scaled_height))

    def load_level_music(self):
        pygame.mixer.music.unload()
        level_music_path = utils.get_asset_path(f'sounds/level-{self.level}.mp3')
        pygame.mixer.music.load(level_music_path)
        pygame.mixer.music.play(fade_ms=1000)

    def check_level_finish(self):
        if len(self.sprite_manager.block_sprites_group.sprites()) == 0:
            self.sprite_manager.ball_sprites_group.empty()
            self.sprite_manager.power_up_sprites_group.empty()

            self.game_active = False
            self.level_menu.active = True
            self.level += 1

    def check_end_game(self):
        if self.sprite_manager.player.health <= 0 or self.level > 6:
            self.game_active = False
            self.end_game_menu.active = True

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        self.keys_pressed = pygame.key.get_pressed()
        if self.keys_pressed[pygame.K_ESCAPE] and self.game_active:
            self.pause_menu.active = True
            self.start_pause_time = time.time()
        elif self.keys_pressed[pygame.K_q]:
            pygame.quit()
            sys.exit()

    def get_last_blit_main_menu(self) -> list[list]:
        self.main_menu.update(self.keys_pressed)
        self.level_difficulty = self.main_menu.selected_option
        self.display_surface.blit(self.main_menu.title_surface, self.main_menu.title_rect)
        objects_to_blit = []
        for surface, rect in self.main_menu.objects_to_blit:
            objects_to_blit.append([surface, rect])
        return objects_to_blit

    def get_last_level_menu(self) -> list[list]:
        self.level_menu.update(self.keys_pressed)
        objects_to_blit = [[self.end_game_menu.text_surface, self.end_game_menu.text_rect]]
        return objects_to_blit

    def get_last_end_game_menu(self) -> list[list]:
        self.end_game_menu.update(self.keys_pressed, self.sprite_manager.score.score)
        if self.end_game_menu.restart_needed:
            self.restart_game()
            return [[]]
        objects_to_blit = [[self.end_game_menu.text_surface, self.end_game_menu.text_rect]]
        return objects_to_blit

    def get_last_blit_pause_menu(self) -> list[list]:
        self.pause_menu.update(self.keys_pressed)
        objects_to_blit = [[self.pause_menu.text_surface, self.pause_menu.text_rect]]
        return objects_to_blit

    def init_game_stage(self):
        self.set_level_background()
        self.load_level_music()
        self.sprite_manager.init_level(self.level, self.level_difficulty)
        self.load_level_music()
        self.game_active = True

    def run_game(self, delta_time: float):
        self.check_level_finish()
        self.check_end_game()
        self.sprite_manager.update(delta_time, self.keys_pressed, self.time_in_pause)
        self.time_in_pause = 0
        self.start_pause_time = 0

    def draw_graphics(
            self,
            menu_objects_to_blit: list[list[pygame.Surface, pygame.Rect]]
    ):
        self.display_surface.blit(source=self.background, dest=(0, 0))
        if len(menu_objects_to_blit) > 0:
            for menu_object_to_blit in menu_objects_to_blit:
                if len(menu_object_to_blit) > 0:
                    self.display_surface.blit(*menu_object_to_blit)
        else:
            self.sprite_manager.draw_all(self.display_surface)

        pygame.display.update()

    def run(self):
        while True:
            delta_time = self.clock.tick_busy_loop(settings.FPS) / 1000

            # Event handling
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


if __name__ == '__main__':
    game = Game()
    game.run()
