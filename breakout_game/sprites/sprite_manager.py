"""
Sprite manager module
"""

from __future__ import annotations

import random
import math

from typing import TYPE_CHECKING

import pygame

from config import settings
from utils import path_utils
from .powerup_manager import PowerUpManager

if not TYPE_CHECKING:
    from sprites.sprite import Player, Score, Heart, PowerUp, Ball, Block, Scoreboard, PowerUpTimerInfo


class SpriteManager:
    """
        Sprite manager class.
        Handles creation of sprites, updates them and draws on the provided surface.
        Provides interface to access another sprites using the composition pattern.
        To initialize all game objects init_level method must be called.

        Attributes:
            all_sprites_group (pygame.sprite.Group): Group containing all sprites objects.
            block_sprites_group (pygame.sprite.Group): Group containing all block sprites.
            player_sprites_group (pygame.sprite.Group): Group containing all player sprites.
            ball_sprites_group (pygame.sprite.Group): Group containing all ball sprites.
            scoreboard_sprites_group (pygame.sprite.Group): Group containing all scoreboard sprites.
            heart_sprites_group (pygame.sprite.Group): Group containing all heart sprites.
            power_up_sprites_group (pygame.sprite.Group): Group containing all power up sprites.
            score_sprites_group (pygame.sprite.Group): Group containing all score sprites.
            power_up_timer_info_group (pygame.sprite.Group): Group containing all power up timer sprites.
            scoreboard (None, Scoreboard): Scoreboard object.
                Defaults to None.
            score (None, Score): Scoreboard object.
                Defaults to None.
            hearts (list, list[Heart]): List of Heart objects in the game.
                Defaults to an empty list.
            blocks (list, list[Block]): List of all block objects in the game.
                Defaults to an empty list.
            player (None, Player): Player object.
                Defaults to None.
            balls (list, list[Ball]): List of all balls in the game.
                Defaults to an empty list.
            power_ups (list, list[PowerUp]): List of all power ups in the game.
                Defaults to an empty list.
            power_up_infos (list, list[PowerUpTimerInfo]): List of all power up timers in the game.
                Defaults to an empty list
            powerup_manager (PowerUpManager): PowerUpManager object, provides status of powerups.
            level_difficulty (None, int): difficulty of the game.
                Defaults to None.
        """
    def __init__(self):
        # Sprites groups
        (
            self.all_sprites_group,
            self.block_sprites_group,
            self.player_sprites_group,
            self.ball_sprites_group,
            self.scoreboard_sprites_group,
            self.heart_sprites_group,
            self.power_up_sprites_group,
            self.score_sprites_group,
            self.power_up_timer_info_group
        ) = (pygame.sprite.Group() for _ in range(9))

        self.scoreboard: (None, Scoreboard) = None
        self.score: (None, Score) = None
        self.hearts: (list, list[Heart]) = []
        self.blocks: (list, list[Block]) = []
        self.player: (None, Player) = None
        self.balls: (list, list[Ball]) = []
        self.power_ups: (list, list[PowerUp]) = []
        self.power_up_infos: (list, list[PowerUpTimerInfo]) = []

        self.powerup_manager: PowerUpManager = PowerUpManager(self)
        self.level_difficulty: (None, int) = None

    def create_scoreboard(self):
        """
        Initialize the scoreboard object.
        """
        scoreboard_image_path = path_utils.get_asset_path('images/background/scoreboard.png')
        scoreboard_image = pygame.image.load(scoreboard_image_path).convert_alpha()
        scoreboard_image = pygame.transform.scale(
            surface=scoreboard_image,
            size=(settings.SCOREBOARD_WIDTH, settings.WINDOW_HEIGHT)
        )
        scoreboard_rect = scoreboard_image.get_rect(topright=(settings.WINDOW_WIDTH, 0))

        self.scoreboard = Scoreboard(
            self,
            sprite_groups=[self.all_sprites_group, self.scoreboard_sprites_group],
            image=scoreboard_image,
            rect=scoreboard_rect,
        )

    def create_score(self):
        """
        Initialize the score object.
        """
        score_color = pygame.Color('white')
        score_font = pygame.font.Font(settings.GAME_FONT, size=settings.SCORE_FONT_SIZE)
        score_image = score_font.render('Score: 0', True, score_color)
        score_rect = score_image.get_rect(
            center=(settings.WINDOW_WIDTH - settings.SCOREBOARD_WIDTH // 2, settings.WINDOW_HEIGHT // 4))
        self.score = Score(
            self,
            sprite_groups=[self.all_sprites_group, self.score_sprites_group],
            image=score_image,
            rect=score_rect,
            font=score_font,
            color=score_color
        )

    def create_heart(self, midtop: tuple):
        """
        Initialize the heart object.

        Args:
            midtop (tuple): The middle top position of a heart sprite on the screen. Must be a tuple of (x, y)
        """
        heart_image_path = path_utils.get_asset_path('images/hearts/heart_s.png')
        heart_image = pygame.image.load(heart_image_path).convert_alpha()
        heart_image = pygame.transform.scale(
            surface=heart_image,
            size=(settings.HEART_WIDTH, settings.HEART_HEIGHT)
        )
        heart_rect = heart_image.get_rect(midtop=midtop)
        heart = Heart(
            self,
            sprite_groups=[self.all_sprites_group, self.heart_sprites_group],
            image=heart_image,
            rect=heart_rect
        )
        self.hearts.append(heart)

    def create_block(self, health: int, x: int, y: int):
        """
        Initialize a block.

        Args:
            health (int): The health of the block.
            x (int): The x position of the block.
            y (int): The y position of the block.
        """
        block_image = pygame.image.load(settings.COLOR_LEGEND[health])
        block_image = pygame.transform.scale(
            surface=block_image,
            size=(settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT)
        )
        block_rect = block_image.get_rect(topleft=(x, y))
        block = Block(
            self,
            sprite_groups=[self.all_sprites_group, self.block_sprites_group],
            image=block_image,
            rect=block_rect,
            health=health,
        )
        self.blocks.append(block)

    def create_player(self):
        """
        Initialize the player.
        """
        player_image = pygame.Surface(
            size=(settings.PADDLE_WIDTH // (self.level_difficulty + 1), settings.PADDLE_HEIGHT)
        )
        player_image.fill('white')
        player_rect = player_image.get_rect(midbottom=(settings.GAME_WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
        self.player = Player(
            self,
            sprite_groups=[self.all_sprites_group, self.player_sprites_group],
            image=player_image,
            rect=player_rect,
        )

    def create_ball(
            self,
            ball_image: [None, pygame.Surface] = None,
            midbottom: [None, tuple] = None,
            angle_radians: [None, float, int] = math.pi / 2,
            speed: int = settings.DEFAULT_BALL_SPEED,
            **kwargs_to_ball
    ):
        """
        Initialize the ball object. Can be used outside in case powerup multiply-balls is activated.

        Args:
            ball_image (None, pygame.Surface): image of a ball created.
                Defaults to None. If None, default image is loaded.
            midbottom (None, tuple): the midbottom position of the ball. Must be a tuple of (x, y).
                Defaults to None. If None player.rect.midtop is used.
            angle_radians (None, float, int): The angle in radians to set the direction.
                Defaults to math.pi / 2 (90 degrees).
            speed (int): The speed of the ball. Defaults to default speed provided in settings
            **kwargs_to_ball: other kwargs passed to the Ball sprite.
        """
        if not ball_image:
            ball_image_path = path_utils.get_asset_path('images/ball/ball.png')
            ball_image = pygame.image.load(ball_image_path).convert_alpha()
            ball_image = pygame.transform.scale(
                ball_image,
                (settings.WINDOW_WIDTH / 40, settings.WINDOW_WIDTH / 40)
            )
        if midbottom is None:
            midbottom = self.player.rect.midtop
        new_ball = Ball(
            sprite_manager=self,
            sprite_groups=[self.all_sprites_group, self.ball_sprites_group],
            image=ball_image,
            rect=ball_image.get_rect(midbottom=midbottom),
            speed=speed
        )
        new_ball.set_direction_from_angle(angle_radians)

        for kwarg in kwargs_to_ball.items():
            setattr(new_ball, kwarg[0], kwarg[1])

        self.balls.append(new_ball)

    def init_level(self, level_number: int = 0, level_difficulty: int = 0):
        """
        Initialize the level.

        Args:
            level_number (int): Level number to initialize the level. The block sprites and background regarding this
                level must be present in assets. Defaults to 0.
            level_difficulty (int): Level difficulty. Defaults to 0.
        """
        self.level_difficulty = level_difficulty

        self.create_scoreboard()
        if self.score is None:
            self.create_score()

        heart_horizontal_gap = settings.SCOREBOARD_WIDTH // (settings.MAX_PLAYER_HEALTH + 1)
        if len(self.hearts) == 0:
            for i in range(settings.MAX_PLAYER_HEALTH):
                heart_midtop = (
                    settings.GAME_WINDOW_WIDTH + (i + 1) * heart_horizontal_gap,
                    settings.GAME_WINDOW_HEIGHT // 7
                )
                self.create_heart(midtop=heart_midtop)

        for row_index, row in enumerate(settings.BLOCK_MAP):
            for col_index, health in enumerate(row):
                if health != ' ':
                    health = int(health) * level_number + 1
                    x = settings.GAP_SIZE / 2 + col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE)
                    y = settings.GAP_SIZE / 2 + row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE)
                    self.create_block(health, x, y)

        if self.player is None:
            self.create_player()

        self.create_ball(speed=int(settings.DEFAULT_BALL_SPEED + level_difficulty * settings.DEFAULT_BALL_SPEED / 2))

    def create_powerup(self, center: tuple, power: str):
        """
        Create a powerup object.

        Args:
            center (tuple): The center of the object. Must be a tuple of (x, y).
            power (str): The name of the powerup.
        """
        power_up_image = pygame.image.load(settings.POWERS[power]['path'])
        power_up = PowerUp(
            sprite_manager=self,
            sprite_groups=[self.all_sprites_group, self.power_up_sprites_group],
            image=power_up_image,
            rect=power_up_image.get_rect(center=center),
            powerup_manager=self.powerup_manager,
            power=power
        )
        self.power_ups.append(power_up)

    def create_powerup_timer_info(self, power_name: str, powerup_time: (int, float)):
        """
        Create powerup timer info object.

        Args:
            power_name (str): The name of the powerup.
            powerup_time (int, float): The lifespan of the powerup.
        """
        last_y = settings.WINDOW_HEIGHT // 3
        existing_power_names = []
        powerup_info_sprites = self.power_up_timer_info_group.sprites()
        for powerup_info_sprite in powerup_info_sprites:
            existing_power_names.append(powerup_info_sprite.power_name)
            last_y = max(last_y, powerup_info_sprite.rect.y)

        color = pygame.Color('white')
        font = pygame.font.Font(settings.GAME_FONT, size=settings.POWERUP_FONT_SIZE)
        image = font.render(f'Time Left: {powerup_time}', True, color)
        rect = image.get_rect(
            center=(
                settings.GAME_WINDOW_WIDTH + settings.SCOREBOARD_WIDTH // 2,
                last_y + settings.GAME_WINDOW_HEIGHT // 20
            )
        )
        powerup_info = PowerUpTimerInfo(
            sprite_manager=self,
            sprite_groups=[self.all_sprites_group, self.power_up_timer_info_group],
            image=image,
            rect=rect,
            font=font,
            color=color,
            power_name=power_name,
            powerup_time=powerup_time
        )
        self.power_up_infos.append(powerup_info)

    def drop_powerup(self, block: Block):
        """
        Drop the powerup from the provided block.

        Args:
            block (Block): The block to drop powerup from.
        """
        random_number = random.random()
        potential_powers = []
        for power in settings.POWERS.keys():
            if random_number <= settings.POWERS[power]['probability']:
                potential_powers.append(power)
        if len(potential_powers) > 0:
            chosen_power = random.choice(potential_powers)
            self.create_powerup(block.rect.center, chosen_power)

    def update(
            self,
            delta_time: float,
            keys_pressed: pygame.key.ScancodeWrapper,
            time_in_pause: float = 0
    ):
        """
        Update all objects during the game.

        Args:
            delta_time (float): Time passed since the last frame.
            keys_pressed (pygame.key.ScancodeWrapper): Keys pressed.
            time_in_pause (float): Time passed in pause mode.
        """
        self.powerup_manager.update(time_in_pause)
        self.player.update(delta_time, keys_pressed)
        self.block_sprites_group.update()
        self.ball_sprites_group.update(delta_time, keys_pressed)
        self.heart_sprites_group.update()
        self.power_up_sprites_group.update(delta_time)
        self.score_sprites_group.update()
        self.power_up_timer_info_group.update(time_in_pause)

    def draw_all(self, display_surface: pygame.Surface):
        """
        Draw all objects on the display

        Args:
            display_surface (pygame.Surface): The surface to draw objects.
        """
        self.player_sprites_group.draw(surface=display_surface)
        self.ball_sprites_group.draw(surface=display_surface)
        self.block_sprites_group.draw(surface=display_surface)
        self.scoreboard_sprites_group.draw(surface=display_surface)
        self.heart_sprites_group.draw(surface=display_surface)
        self.power_up_sprites_group.draw(surface=display_surface)
        self.score_sprites_group.draw(surface=display_surface)
        self.power_up_timer_info_group.draw(surface=display_surface)
