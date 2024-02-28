import pygame
import sys
import time
import settings

from sprites import Player, Ball, Scoreboard, Block


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

        # sprites group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()

        # setup
        self.player = Player(self.all_sprites)
        self.stage_setup()
        self.ball = Ball(groups=self.all_sprites, player=self.player, blocks=self.block_sprites)
        self.scoreboard = Scoreboard(self.all_sprites)
    
    def stage_setup(self):
        # cycle through all rows and columns of BLOCK_MAP
        for row_index, row in enumerate(settings.BLOCK_MAP):
            for col_index, health in enumerate(row):
                if health != ' ':
                    # find the x and y position for each individual block
                    x = col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2
                    y = row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE) + settings.GAP_SIZE // 2
                    Block(int(health), (x, y), [self.all_sprites, self.block_sprites])

    def run(self):
        last_time = time.time()

        while True:
            dt = time.time() - last_time
            last_time = time.time()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True

            keys_pressed = pygame.key.get_pressed()

            # update the game
            self.player.update(dt, keys_pressed)
            self.ball.update(dt)
            self.block_sprites.update()

            # draw the frame
            self.display_surface.blit(source=self.bg, dest=(0, 0))
            self.all_sprites.draw(surface=self.display_surface)

            # update window
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
