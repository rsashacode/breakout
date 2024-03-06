import pygame
import sys
import time
import settings
import random

from sprites import Player, Ball, Scoreboard, Block, Heart, PowerUp, Score, Congratulations


def create_bg():
    bg_original = pygame.image.load('./assets/background/menu.png').convert()
    focus_height = settings.WINDOW_HEIGHT 
    focus_y = bg_original.get_height() - focus_height
    focus_rect = pygame.Rect(0, focus_y, settings.WINDOW_WIDTH, focus_height)
    return bg_original, focus_rect

class Menu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game Menu')
        
        # Load and scale the background image
        self.bg_image = pygame.image.load('./assets/background/background.jpg').convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        
        # Setup font for text rendering
        self.font = pygame.font.Font('./assets/other/BAUHS93.ttf', 40)  # Use pygame's default font
        self.title_text = 'Breakout Game'
        self.options = ['Normal', 'Difficult']
        self.selected_option = 0  # Index of the currently selected option

        # Load and play background music
        pygame.mixer.music.load('./assets/music/menu.mp3')
        pygame.mixer.music.play(-1)  # -1 means loop indefinitely

    def render_text(self, text, position, selected=False):
        color = (255, 0, 0) if selected else (255, 255, 255)  # Red for selected, white otherwise
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.display_surface.blit(text_surface, text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = max(0, self.selected_option - 1)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = min(len(self.options) - 1, self.selected_option + 1)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            pygame.mixer.music.stop()
                            game = Game()
                            game.run()
                        elif self.selected_option == 1:
                            pass  # Placeholder for the difficult mode

            self.display_surface.blit(self.bg_image, (0, 0))
            self.render_text(self.title_text, (settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT / 4), selected=False)
            for index, option in enumerate(self.options):
                position = (settings.WINDOW_WIDTH / 2, settings.WINDOW_HEIGHT / 2 + index * 50)
                self.render_text(option, position, selected=index == self.selected_option)

            pygame.display.update()

class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game')
        self.show_congratulations = False
        self.level = 1
        self.time_last_block_added = time.time()
        self.added_rows_count = 0
        self.blocks = []

        # background
        self.bg, self.bg_rect = create_bg()
        
        # sprites group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()
        self.scoreboard_sprites = pygame.sprite.Group()
        self.heart_sprites = pygame.sprite.Group()
        self.power_up_sprites = pygame.sprite.Group()
        self.score_sprites = pygame.sprite.Group()

        # initialise_game
        self.score = Score(self.all_sprites, self.score_sprites)
        self.hearts: list[Heart] = self.hearts_setup()
        self.player: Player = self.player_setup(self.heart_sprites)
        self.power_ups: list[list[PowerUp]] = self.power_ups_setup(player=self.player)
        self.blocks: list[list[Block]] = self.blocks_setup(self.power_ups)
        self.balls: list[Ball] = self.balls_setup(self.player)
        self.scoreboard: Scoreboard = self.scoreboard_setup()

    def player_setup(self, heart_sprites_group) -> Player:
        player_image = pygame.Surface(size=(settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT))
        player_image.fill('white')
        player_rect = player_image.get_rect(midbottom=(settings.GAME_WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
        return Player(
            groups=[self.all_sprites, self.player_sprites],
            image=player_image,
            rect=player_rect,
            heart_group=heart_sprites_group
        )

    def blocks_setup(self, power_ups: list[list[PowerUp]]) -> list[list[Block]]:
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
                    power_up = power_ups[row_index][col_index]

                    block_row.append(
                        Block(
                            groups=[self.all_sprites, self.block_sprites],
                            image=block_image,
                            rect=block_rect,
                            health=health,
                            power_up=None
                        )
                    )
            blocks.append(block_row)
        return blocks

    def power_ups_setup(self, player: Player) -> list[list[PowerUp]]:
        power_ups = []
        for row_index, row in enumerate(settings.BLOCK_MAP):
            power_ups_row = []
            for col_index, block_present in enumerate(row):
                if block_present != ' ': # and random.random() < 0.3:
                    x = (
                        col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2 +
                        settings.BLOCK_WIDTH // 2
                    )
                    y = (
                        row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE) + settings.GAP_SIZE // 2 +
                        settings.BLOCK_HEIGHT // 2
                    )

                    power_up_image = pygame.image.load(random.choice(settings.POWER_UP_IMAGES))
                    power_up_rect = power_up_image.get_rect(topleft=(x, y))

                    power_up = PowerUp(
                        groups=[],
                        image=power_up_image,
                        rect=power_up_rect,
                        player=player,
                        score=self.score
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
                blocks=self.block_sprites,
                score=self.score
            )
        ]
        return balls

    def hearts_setup(self) -> list[Heart]:
        heart_image = pygame.image.load('./assets/other/heart_s.png').convert_alpha()
        hearts = []
        heart_hor_gap = (settings.SCOREBOARD_WIDTH - 20 * 2) // 3
        for i in range(settings.MAX_PLAYER_HEALTH):
            heart_rect = heart_image.get_rect(
                midtop=(settings.GAME_WINDOW_WIDTH + (i + 1) * heart_hor_gap, settings.GAME_WINDOW_HEIGHT // 7)
            )
            heart = Heart(
                    groups=[self.all_sprites, self.heart_sprites],
                    image=heart_image,
                    rect=heart_rect
                )
            hearts.append(heart)
        return hearts

    def scoreboard_setup(self):
        scoreboard_image = pygame.image.load('./assets/other/scoreboard.png').convert_alpha()
        scoreboard_image = pygame.transform.scale(scoreboard_image, (settings.SCOREBOARD_WIDTH, settings.WINDOW_HEIGHT))
        scoreboard_rectangle = scoreboard_image.get_rect(topright=(settings.WINDOW_WIDTH, 0))

        return Scoreboard(
            groups=[self.all_sprites, self.scoreboard_sprites],
            image=scoreboard_image,
            rect=scoreboard_rectangle,
        )
    
    def update_level(self):
        self.level += 1
        new_block_map = []
        for row in settings.BLOCK_MAP:
            new_row = ''
            for char in row:
                if char != ' ':
                    new_row += str(self.level)
                else:
                    new_row += ' '
            new_block_map.append(new_row)
        settings.BLOCK_MAP = new_block_map
        self.blocks = self.blocks_setup(self.power_ups)



    def add_new_blocks(self):
        if self.added_rows_count >= 5:
            self.end_game()
            return

        for block_row in self.blocks:
            for block in block_row:
                if block:
                    block.update()

        for power_up_row in self.power_ups:
            for power_up in power_up_row:
                if power_up is not None:
                    power_up.rect.y += settings.BLOCK_HEIGHT + settings.GAP_SIZE


        new_blocks_row = []
        new_power_ups_row = []
        for col_index in range(len(settings.BLOCK_MAP[0])):
            x = col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2
            y = settings.GAP_SIZE // 2  
            health = self.level

            block_image = pygame.image.load(settings.COLOR_LEGEND[health])
            block_image = pygame.transform.scale(block_image, (settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT))
            block_rect = block_image.get_rect(topleft=(x, y))
            new_block = Block(
                groups=[self.all_sprites, self.block_sprites],
                image=block_image,
                rect=block_rect,
                health=health,
                power_up=None 
            )
            new_blocks_row.append(new_block)

            if random.random() < 0.3:
                power_up_image = pygame.image.load(random.choice(settings.POWER_UP_IMAGES))
                power_up_rect = power_up_image.get_rect(center=(x + settings.BLOCK_WIDTH // 2, y + settings.BLOCK_HEIGHT // 2))
                
                power_up = PowerUp(
                    groups=[self.all_sprites],
                    image=power_up_image,
                    rect=power_up_rect,
                    player=self.player,
                    score=self.score
                )
                new_power_ups_row.append(power_up)
            else:
                new_power_ups_row.append(None)

        self.blocks.insert(0, new_blocks_row)
        self.power_ups.insert(0, new_power_ups_row)
        self.added_rows_count += 1
    
    def update(self):
        if self.is_hit:
            if self.power_up:
                self.power_up.visible = True
                self.power_up.add(self.all_sprites, self.power_up_sprites)

    def end_game(self):
        print("Game Over!")
        pygame.quit()
        sys.exit()

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
            self.score_sprites.update()

            # draw the frame
            self.display_surface.blit(self.bg, (0, 0), self.bg_rect)
            self.player_sprites.draw(surface=self.display_surface)
            self.ball_sprites.draw(surface=self.display_surface)
            self.block_sprites.draw(surface=self.display_surface)
            self.scoreboard_sprites.draw(surface=self.display_surface)
            self.heart_sprites.draw(surface=self.display_surface)
            for powerup_row in self.power_ups:
                for powerup in powerup_row:
                    if powerup is not None:
                        if powerup.visible == 1:
                            powerup.add(self.power_up_sprites)
            self.power_up_sprites.draw(surface=self.display_surface)
            self.score_sprites.draw(surface=self.display_surface)

            if not self.block_sprites and not self.show_congratulations:
                self.show_congratulations = True
                self.congratulations = Congratulations(
                    groups=[self.all_sprites],
                    image_path="./assets/other/congratulations.png",
                    display_surface=self.display_surface
                    )

            if self.show_congratulations:
                self.congratulations.draw()

            if self.show_congratulations:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        self.show_congratulations = False
                        self.update_level()
                        self.blocks = self.blocks_setup(self.power_ups)

            current_time = time.time()
            if current_time - self.time_last_block_added >= 30:
                for block_row in self.blocks:
                    for block in block_row:
                        if block:
                            self.block_sprites.remove(block)
                            self.all_sprites.remove(block)
                for powerup_row in self.power_ups:
                    for powerup in powerup_row:
                        if powerup:
                            self.power_up_sprites.remove(powerup)
                            self.all_sprites.remove(powerup)

                self.add_new_blocks()

                for block_row, powerup_row in zip(self.blocks, self.power_ups):
                    for block in block_row:
                        if block:
                            self.block_sprites.add(block)
                            self.all_sprites.add(block)
                    for powerup in powerup_row:
                        if powerup:
                            self.power_up_sprites.add(powerup)
                            self.all_sprites.add(powerup)

                self.time_last_block_added = current_time

            # update window
            pygame.display.update()



if __name__ == '__main__':
    menu = Menu()
    menu.run()
