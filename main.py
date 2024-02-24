import pygame, sys, time
from settings import *
from sprites import Player


def create_bg():
    bg_original = pygame.image.load('assets/background/background.jpg').convert()
    scale_factor = WINDOW_HEIGHT / bg_original.get_height()
    scaled_width = bg_original.get_width() * scale_factor
    scaled_height = bg_original.get_height() * scale_factor
    scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
    return scaled_bg


class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout')

        # background
        self.bg = create_bg()

        # sprites group setup
        self.all_sprites = pygame.sprite.Group()

        # setup
        self.player = Player(self.all_sprites)
    
    def run(self):
        last_time = time.time()
        while True:
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # update the game
            self.all_sprites.update(dt)
            

            # draw the frame
            self.display_surface.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.display_surface)

            # update window
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()
