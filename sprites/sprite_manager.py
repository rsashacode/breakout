from __future__ import annotations

import pygame
import settings
import random
import math
import path_utils

from typing import TYPE_CHECKING
from powerup_manager import PowerUpManager

if not TYPE_CHECKING:
	from sprites import Player, Score, Heart, PowerUp, Ball, Block, Scoreboard, PowerUpTimerInfo


class SpriteManager:
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

		self.scoreboard = None
		self.score = None
		self.hearts = []
		self.blocks = []
		self.player = None
		self.balls = []
		self.power_ups = []
		self.power_up_infos = []

		self.powerup_manager = PowerUpManager(self)
		self.heart_horizontal_gap = settings.SCOREBOARD_WIDTH // (settings.MAX_PLAYER_HEALTH + 1)

		self.level_difficulty = None

	def create_scoreboard(self):
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
		score_color = pygame.Color('white')
		score_font = pygame.font.Font(settings.GAME_FONT, size=settings.SCORE_FONT_SIZE)
		score_image = score_font.render(f'Score: 0', True, score_color)
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
			midbottom: [None, bool] = None,
			angle_radians: [None, float] = math.pi / 2,
			speed: [None, int] = settings.DEFAULT_BALL_SPEED,
			**kwargs_to_ball
	):
		if not ball_image:
			ball_image_path = path_utils.get_asset_path('images/ball/ball.png')
			ball_image = pygame.image.load(ball_image_path).convert_alpha()
			ball_image = pygame.transform.scale(
				ball_image,
				(settings.WINDOW_WIDTH / 40, settings.WINDOW_WIDTH / 40)
			)
		if not midbottom:
			midbottom = self.player.rect.midtop
		new_ball = Ball(
			sprite_manager=self,
			sprite_groups=[self.all_sprites_group, self.ball_sprites_group],
			image=ball_image,
			rect=ball_image.get_rect(midbottom=midbottom),
			speed=speed
		)
		new_ball.set_direction_from_angle(angle_radians)

		for key in kwargs_to_ball:
			new_ball.__setattr__(key, kwargs_to_ball[key])

		self.balls.append(new_ball)

	def init_level(self, level_number: int = 0, level_difficulty: int = 0):
		self.level_difficulty = level_difficulty

		self.create_scoreboard()
		if self.score is None:
			self.create_score()

		if len(self.hearts) == 0:
			for i in range(settings.MAX_PLAYER_HEALTH):
				heart_midtop = (
					settings.GAME_WINDOW_WIDTH + (i + 1) * self.heart_horizontal_gap,
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

	def create_powerup_timer_info(self, power_name: str, powerup_time: [int, float]):
		last_y = settings.WINDOW_HEIGHT // 3
		existing_power_names = []
		powerup_info_sprites = self.power_up_timer_info_group.sprites()
		for powerup_info_sprite in powerup_info_sprites:
			existing_power_names.append(powerup_info_sprite.power_name)
			if powerup_info_sprite.rect.y > last_y:
				last_y = powerup_info_sprite.rect.y

		# self.powerup_info_coexists(power_name, existing_power_names)
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
		random_number = random.random()
		potential_powers = []
		for power in settings.POWERS.keys():
			if random_number <= settings.POWERS[power]['probability']:
				potential_powers.append(power)
		if len(potential_powers) > 0:
			chosen_power = random.choice(potential_powers)
			self.create_powerup(block.rect.center, chosen_power)

	def update(self, delta_time: float, keys_pressed: pygame.key.ScancodeWrapper, time_in_pause: float = 0):
		# update the game
		self.powerup_manager.update(time_in_pause)
		self.player.update(delta_time, keys_pressed)
		self.block_sprites_group.update()
		self.ball_sprites_group.update(delta_time, keys_pressed)
		self.heart_sprites_group.update()
		self.power_up_sprites_group.update(delta_time)
		self.score_sprites_group.update()
		self.power_up_timer_info_group.update(time_in_pause)

	def draw_all(self, display_surface):
		self.player_sprites_group.draw(surface=display_surface)
		self.ball_sprites_group.draw(surface=display_surface)
		self.block_sprites_group.draw(surface=display_surface)
		self.scoreboard_sprites_group.draw(surface=display_surface)
		self.heart_sprites_group.draw(surface=display_surface)
		self.power_up_sprites_group.draw(surface=display_surface)
		self.score_sprites_group.draw(surface=display_surface)
		self.power_up_timer_info_group.draw(surface=display_surface)
