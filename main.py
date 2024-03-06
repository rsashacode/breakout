import pygame
import settings
import sys

from sprite_manager import SpriteManager


def create_bg():
    bg_original = pygame.image.load('./assets/background/background.jpg').convert()
    scale_factor = settings.WINDOW_HEIGHT / bg_original.get_height()
    scaled_width = bg_original.get_width() * scale_factor
    scaled_height = bg_original.get_height() * scale_factor
    scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
    return scaled_bg


class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game')

        # background
        self.bg = create_bg()

        # sprites
        self.sprite_manager = SpriteManager()
        self.sprite_manager.init_level()

    def run(self):
        clock = pygame.time.Clock()
        while True:
            delta_time = clock.tick_busy_loop(settings.FPS) / 1000
            fps = clock.get_fps()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys_pressed = pygame.key.get_pressed()
            self.sprite_manager.update(delta_time, keys_pressed)

            self.display_surface.blit(source=self.bg, dest=(0, 0))
            self.sprite_manager.draw_all(self.display_surface)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
