import pygame
import sys
import time
import settings
import random

from sprites import Player, Ball, Scoreboard, Block, Heart, PowerUp


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
        self.player_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.scoreboard_sprites = pygame.sprite.Group()
        self.heart_sprites = pygame.sprite.Group()
        self.power_up_sprites = pygame.sprite.Group()

        # initialise_game
        self.power_ups: list[list[PowerUp]] = self.power_ups_setup()
        self.blocks: list[list[Block]] = self.blocks_setup()
        self.hearts: list[Heart] = self.hearts_setup()
        self.player: Player = self.player_setup()
        self.balls: list[Ball] = self.balls_setup(self.player)
        self.scoreboard: Scoreboard = self.scoreboard_setup()

    def player_setup(self) -> Player:
        player_image = pygame.Surface(size=(settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT))
        player_image.fill('white')
        player_rect = player_image.get_rect(midbottom=(settings.GAME_WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
        return Player(
            groups=[self.all_sprites, self.player_sprites],
            image=player_image,
            rect=player_rect,
            heart_group=self.heart_sprites
        )

    def blocks_setup(self) -> list[list[Block]]:
        # cycle through all rows and columns of BLOCK_MAP
        blocks = []
        for row_index, row in enumerate(settings.BLOCK_MAP):
            block_row = []
            for col_index, health in enumerate(row):
                if health != ' ':
                    health = int(health)
                    # find the x and y position for each individual block
                    x = col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2
                    y = row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE) + settings.GAP_SIZE // 2

                    # Load the image for the block based on the health value
                    block_image = pygame.image.load(settings.COLOR_LEGEND[health])

                    # Scale the image to fit the BLOCK_WIDTH and BLOCK_HEIGHT
                    block_image = pygame.transform.scale(block_image, (settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT))

                    block_rect = block_image.get_rect(topleft=(x, y))

                    # Check if power up exists
                    power_up = self.power_ups[row_index][col_index]

                    block_row.append(
                        Block(
                            groups=[self.all_sprites, self.block_sprites],
                            image=block_image,
                            rect=block_rect,
                            health=health,
                            power_up=power_up
                        )
                    )
            blocks.append(block_row)
        return blocks

    def power_ups_setup(self) -> list[list[PowerUp]]:
        power_ups = []
        for row_index, row in enumerate(settings.BLOCK_MAP):
            power_ups_row = []
            for col_index, block_present in enumerate(row):
                if block_present != ' ': # and random.random() < 0.3:
                    x = col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2
                    y = row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE) + settings.GAP_SIZE // 2

                    power_up_image = pygame.image.load(random.choice(settings.POWER_UP_IMAGES))
                    power_up_rect = power_up_image.get_rect(topleft=(x, y))

                    power_up = PowerUp(
                        groups=[self.all_sprites, self.power_up_sprites],
                        image=power_up_image,
                        rect=power_up_rect
                    )
                    power_ups_row.append(power_up)
                else:
                    power_ups_row.append(None)
            power_ups.append(power_ups_row)
        return power_ups

    def balls_setup(self, player):
        ball_image = pygame.image.load('./assets/other/Ball.png').convert_alpha()
        balls = [
            Ball(
                groups=[self.all_sprites, self.ball_sprites],
                image=ball_image,
                rect=ball_image.get_rect(midbottom=player.rect.midtop),
                player=player,
                blocks=self.block_sprites
            )
        ]
        return balls

    def hearts_setup(self) -> list[Heart]:
        heart_image = pygame.image.load('./assets/other/heart_s.png').convert_alpha()
        hearts = []
        heart_hor_gap = (settings.SCOREBOARD_WIDTH - 20 * 2) // 3
        for i in range(settings.MAX_PLAYER_HEALTH):
            heart_rect = heart_image.get_rect(
                midtop=(settings.GAME_WINDOW_WIDTH + (i + 1) * heart_hor_gap, settings.GAME_WINDOW_HEIGHT // 10)
            )
            heart = Heart(
                    groups=[self.all_sprites, self.heart_sprites],
                    image=heart_image,
                    rect=heart_rect
                )
            hearts.append(heart)
        return hearts

    def scoreboard_setup(self):
        scoreboard_image = pygame.image.load('./assets/other/scoreboard.jpg').convert_alpha()
        scoreboard_image = pygame.transform.scale(scoreboard_image, (settings.SCOREBOARD_WIDTH, settings.WINDOW_HEIGHT))
        scoreboard_rectangle = scoreboard_image.get_rect(topright=(settings.WINDOW_WIDTH, 0))

        return Scoreboard(
            groups=[self.all_sprites, self.scoreboard_sprites],
            image=scoreboard_image,
            rect=scoreboard_rectangle,
        )

    def run(self):
        last_time = time.time()

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

            # update the game
            self.player.update(delta_time, keys_pressed)
            self.block_sprites.update()
            self.ball_sprites.update(delta_time, keys_pressed)
            self.heart_sprites.update()
            self.power_up_sprites.update()
            # self.scoreboard_sprites.update()

            # draw the frame
            self.display_surface.blit(source=self.bg, dest=(0, 0))
            self.player_sprites.draw(surface=self.display_surface)
            self.ball_sprites.draw(surface=self.display_surface)
            self.block_sprites.draw(surface=self.display_surface)
            self.scoreboard_sprites.draw(surface=self.display_surface)
            self.heart_sprites.draw(surface=self.display_surface)
            self.power_up_sprites.draw(surface=self.display_surface)

            # update window
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
