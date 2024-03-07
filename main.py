import pygame
import settings
import sys

from sprite_manager import SpriteManager
from menu import MainMenu, LevelMenu, EndGameMenu


class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        self.title = 'Breakout Game'

        # Menu
        self.main_menu = MainMenu()
        self.level_menu = LevelMenu()
        self.end_game_menu = EndGameMenu()

        pygame.mixer.music.load('./assets/sounds/menu.mp3')

        # Background
        self.background = self.main_menu.background

        # Sprites
        self.sprite_manager = SpriteManager()

        # Game Stage
        self.game_active = False
        self.level = 0

    def set_level_background(self):
        self.background = pygame.image.load(f'assets/images/background/level-{self.level}.jpg').convert()
        self.background.fill((150, 150, 150), special_flags=pygame.BLEND_RGB_SUB)
        scale_factor = settings.WINDOW_HEIGHT / self.background.get_height()
        scaled_width = self.background.get_width() * scale_factor
        scaled_height = self.background.get_height() * scale_factor
        self.background = pygame.transform.scale(self.background, (scaled_width, scaled_height))

    def load_level_music(self):
        pass

    def check_level_finish(self):
        if len(self.sprite_manager.block_sprites_group.sprites()) == 0:
            self.sprite_manager.ball_sprites_group.empty()
            self.sprite_manager.power_up_sprites_group.empty()

            self.game_active = False
            self.level_menu.active = True
            self.level += 1

    def check_end_game(self):
        if self.sprite_manager.player.health <= 0 or self.level >= 6:
            self.game_active = False
            self.end_game_menu.active = True

    def run(self):
        clock = pygame.time.Clock()
        pygame.mixer.music.play(-1)

        while True:
            delta_time = clock.tick_busy_loop(settings.FPS) / 1000
            fps = clock.get_fps()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys_pressed = pygame.key.get_pressed()
            self.display_surface.blit(source=self.background, dest=(0, 0))

            if self.main_menu.active:
                self.main_menu.update(keys_pressed)
                self.display_surface.blit(self.main_menu.title_surface, self.main_menu.title_rect)
                for surface, rect in self.main_menu.objects_to_blit:
                    self.display_surface.blit(surface, rect)
            elif self.level_menu.active:
                self.level_menu.update(keys_pressed)
                self.display_surface.blit(self.level_menu.text_surface, self.level_menu.text_rect)
            elif self.end_game_menu.active:
                self.end_game_menu.update_text(self.sprite_manager.score.score)
                self.display_surface.blit(self.end_game_menu.text_surface, self.end_game_menu.text_rect)
            else:
                if not self.game_active:
                    self.set_level_background()
                    level_difficulty = self.main_menu.selected_option
                    self.sprite_manager.init_level(self.level, level_difficulty)
                    self.load_level_music()
                    self.game_active = True
                else:
                    self.check_level_finish()
                    self.check_end_game()
                self.sprite_manager.update(delta_time, keys_pressed)
                self.sprite_manager.draw_all(self.display_surface)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
