import copy

import pygame
import settings
import math
import time

from powerup_manager import PowerUpManager
from typing import Any


class GameSprite(pygame.sprite.Sprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups: Any,
			image: pygame.Surface,
			rect: pygame.Rect
	):
		super().__init__(sprite_groups)

		self.sprite_manager = sprite_manager
		self.sprite_groups = sprite_groups
		self.image = image
		self.rect = rect

		self.position = pygame.math.Vector2(self.rect.topleft)
		self.direction = pygame.math.Vector2((0, 0))
		self.speed = 0

		self.original_image = self.image.copy()
		self.original_width = self.rect.width
		self.original_height = self.rect.height

	def update(self, *args, **kwargs):
		raise NotImplemented('Sprite class must implement "update" method')

	def movement(self, delta_time):
		self.position.x += self.direction.x * self.speed * delta_time
		self.position.y += self.direction.y * self.speed * delta_time
		self.rect.x = round(self.position.x)
		self.rect.y = round(self.position.y)

	def update_position_from_rect(self):
		self.position.x = self.rect.x
		self.position.y = self.rect.y

	def change_size(self, new_width: int, new_height: int):
		rect_center = self.rect.center
		self.image = pygame.transform.scale(self.original_image, (new_width, new_height))
		self.rect = self.image.get_rect(center=rect_center)
		self.rect.height = new_height
		self.update_position_from_rect()

	def change_image(self, new_image: pygame.Surface, new_width: int, new_height: int):
		rect_center = self.rect.center
		self.image = pygame.transform.scale(
			new_image, (new_width, new_height)
		)
		self.rect = self.image.get_rect(center=rect_center)
		self.update_position_from_rect()

	def restore_size(self):
		rect_center = self.rect.center
		self.image = pygame.transform.scale(self.image, (self.original_width, self.original_height))
		self.rect = self.image.get_rect(center=rect_center)
		self.update_position_from_rect()

	def restore_image(self):
		rect_center = self.rect.center
		self.image = copy.deepcopy(self.original_image)
		self.rect = self.image.get_rect(center=rect_center)
		self.update_position_from_rect()


class Heart(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

	def update(self):
		pass


class Player(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)
		self.direction = pygame.math.Vector2()
		self.health = settings.MAX_PLAYER_HEALTH
		self.speed = settings.DEFAULT_PADDLE_SPEED

		self.lost_hp_sound = pygame.mixer.Sound('./assets/sounds/lost_hp.mp3')

	def check_screen_constraint(self):
		if self.rect.right > settings.GAME_WINDOW_WIDTH:
			self.rect.right = settings.GAME_WINDOW_WIDTH
			self.position.x = self.rect.x

		if self.rect.left < 0:
			self.rect.left = 0
			self.position.x = self.rect.x

	def loose_health(self):
		if self.health >= 1:
			self.health -= 1
			heart_sprites = self.sprite_manager.heart_sprites_group.sprites()
			heart_sprites[-1].kill()
			self.sprite_manager.score_sprites_group.sprites()[0].subtract_score(200)
			self.lost_hp_sound.stop()
			self.lost_hp_sound.play()

	def add_health(self):
		if self.health < settings.MAX_PLAYER_HEALTH:
			self.health += 1

			heart_midtop = (
				settings.GAME_WINDOW_WIDTH + self.health * self.sprite_manager.heart_horizontal_gap,
				settings.GAME_WINDOW_HEIGHT // 7
			)
			self.sprite_manager.create_heart(midtop=heart_midtop)

	def update(self, delta_time, keys_pressed: pygame.key.ScancodeWrapper):
		if keys_pressed[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys_pressed[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		self.movement(delta_time)
		self.check_screen_constraint()
		self.rect.x = round(self.position.x)


class Score(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
			font: pygame.font.Font,
			color: pygame.Color
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)
		self.score = 0
		self.font = font
		self.color = color

	def add_score(self, points):
		self.score += points

	def subtract_score(self, points):
		self.score -= points

	def update(self):
		old_rect_center = self.rect.center
		self.image = self.font.render(f'Score: {self.score}', True, self.color)
		self.rect = self.image.get_rect(center=old_rect_center)


class PowerUp(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
			powerup_manager: PowerUpManager,
			power: str = ''
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

		self.direction = pygame.math.Vector2((0, 1))
		self.speed = settings.DEFAULT_POWERUP_SPEED
		self.power = power
		self.powerup_manager = powerup_manager

		self.powerup_sound = pygame.mixer.Sound('./assets/sounds/get powerup.mp3')
		self.powerup_sound.set_volume(0.3)

	def activate(self):
		self.powerup_manager.activate_powerup(self.power)
		if settings.POWERS[self.power]['time'] != -1:
			powerup_timers_in_game = self.sprite_manager.power_up_timer_info_group.sprites()
			for powerup_timer in powerup_timers_in_game:

				powerup_timer_power_name = powerup_timer.power_name
				conflicting_power = settings.POWERS[powerup_timer_power_name]['conflicting-power']

				if powerup_timer_power_name == self.power:
					powerup_timer.kill()
				elif conflicting_power is not None:
					if conflicting_power == self.power:
						powerup_timer.kill()
			self.sprite_manager.create_powerup_timer_info(self.power, settings.POWERS[self.power]['time'])
		self.powerup_sound.stop()
		self.powerup_sound.play()

	def update(self, delta_time):
		if self.rect.top > settings.GAME_WINDOW_HEIGHT:
			self.kill()
		if pygame.sprite.collide_rect(self, self.sprite_manager.player_sprites_group.sprites()[0]):
			self.activate()
			self.sprite_manager.score_sprites_group.sprites()[0].add_score(
				100 * (self.sprite_manager.level_difficulty + 1)
			)
			self.kill()
		self.movement(delta_time)


class Block(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
			health: int,
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)
		self.health = health
		self.update_image()

		self.hit_sound = pygame.mixer.Sound('./assets/sounds/hit blocks.mp3')
		self.hit_sound.set_volume(0.25)

		self.break_sound = pygame.mixer.Sound('./assets/sounds/break blocks.mp3')
		self.break_sound.set_volume(0.75)

	# damage information
	def get_damage(self, amount: int):
		self.health -= amount
		if self.health <= 0:
			self.sprite_manager.score_sprites_group.sprites()[0].add_score(
				30 * (self.sprite_manager.level_difficulty + 1)
			)
			self.break_sound.stop()
			self.break_sound.play()
			self.kill()
			self.sprite_manager.drop_powerup(self)
		else:
			self.sprite_manager.score_sprites_group.sprites()[0].add_score(
				10 * (self.sprite_manager.level_difficulty + 1)
			)
			self.hit_sound.stop()
			self.hit_sound.play()

	def update_image(self):
		if self.health in settings.COLOR_LEGEND:
			new_image = pygame.image.load(settings.COLOR_LEGEND[self.health])
			self.change_image(new_image, settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT)

	def update(self):
		self.update_image()


class Ball(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
			speed: int
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

		self.direction = pygame.math.Vector2((0, -1))

		self.speed = speed
		self.original_speed = speed

		self.strength = 1
		self.original_strength = 1

		self.time_delay_counter = 0
		self.hit_paddle_sound = pygame.mixer.Sound('./assets/sounds/hit paddle.mp3')
		self.active = False

	def get_angle_of_direction(self):
		return math.atan2(self.direction[1], self.direction[0])

	def set_direction_from_angle(self, angle):
		self.direction = pygame.math.Vector2((math.cos(angle), math.sin(angle)))

	def change_speed(self, new_speed: int):
		self.speed = new_speed

	def restore_speed(self):
		self.speed = self.original_speed

	def change_strength(self, new_strength: int):
		self.strength = new_strength

	def restore_strength(self):
		self.strength = self.original_strength

	def loose_ball(self):
		self.time_delay_counter = time.time()
		if len(self.sprite_manager.ball_sprites_group.sprites()) == 1:
			self.sprite_manager.player_sprites_group.sprites()[0].loose_health()
			self.active = False
		else:
			self.kill()

	def frame_collision(self):
		# Hit the left side of the game window
		if self.rect.left < 0:
			self.rect.left = 0
			self.position.x = 0
			self.direction.x *= -1

		# Hit the right side of the game window
		elif self.rect.right > settings.GAME_WINDOW_WIDTH:
			self.rect.right = settings.GAME_WINDOW_WIDTH
			self.position.x = self.rect.topleft[0]
			self.direction.x *= -1

		# Hit the top of the game window
		if self.rect.top < 0:
			self.rect.top = 0
			self.position.y = 0
			self.direction.y *= -1

		# Hit the bottom of the game window
		elif self.rect.top > settings.GAME_WINDOW_HEIGHT:
			self.loose_ball()

	def get_overlapping_rect(self, colliding_sprites) -> pygame.rect.Rect:
		total_overlap_left = settings.GAME_WINDOW_WIDTH
		total_overlap_right = 0
		total_overlap_top = settings.GAME_WINDOW_HEIGHT
		total_overlap_bottom = 0

		# Calculate the overall area of overlapping
		for sprite in colliding_sprites:
			overlap = self.rect.clip(sprite.rect)
			if overlap.left < total_overlap_left:
				total_overlap_left = overlap.left
			if overlap.right > total_overlap_right:
				total_overlap_right = overlap.right
			if overlap.top < total_overlap_top:
				total_overlap_top = overlap.top
			if overlap.bottom > total_overlap_bottom:
				total_overlap_bottom = overlap.bottom

		# Keyword arguments do not work here
		overlap_rect = pygame.rect.Rect(
			total_overlap_left,  # left
			total_overlap_top,  # top
			abs(total_overlap_right - total_overlap_left),  # width
			abs(total_overlap_bottom - total_overlap_top)  # height
		)
		return overlap_rect

	def handle_vertical_collision(self, overlapping_rect):
		if self.direction.y < 0:
			self.rect.top = overlapping_rect.bottom
		else:
			self.rect.bottom = overlapping_rect.top
		self.direction.y *= -1

	def handle_horizontal_collision(self, overlapping_rect):
		if self.direction.x < 0:
			self.rect.left = overlapping_rect.right
		else:
			self.rect.right = overlapping_rect.left
		self.direction.x *= -1

	def handle_diagonal_collision(self, overlapping_rect):
		if self.direction.x < 0:
			self.rect.left = overlapping_rect.right
		else:
			self.rect.right = overlapping_rect.left
		self.direction.x *= -1
		if self.direction.y < 0:
			self.rect.top = overlapping_rect.bottom
		else:
			self.rect.bottom = overlapping_rect.top
		self.direction.y *= -1

	def handle_hor_hit_by_player(self, colliding_players):
		player_direction_x = colliding_players[0].direction.x
		paddle_path_per_frame = abs(round(player_direction_x * colliding_players[0].speed / settings.FPS))
		if player_direction_x > 0:
			self.rect.x += paddle_path_per_frame * 3
		else:
			self.rect.x -= paddle_path_per_frame * 3

		self.direction.x = player_direction_x

	def paddle_adjust_angle(self, overlapping_rect):
		hit_point_x = overlapping_rect.centerx
		paddle_middle = self.sprite_manager.player_sprites_group.sprites()[0].rect.centerx
		paddle_width = self.sprite_manager.player_sprites_group.sprites()[0].rect.width

		dist_from_paddle_center = hit_point_x - paddle_middle
		angle_ratio = abs(dist_from_paddle_center) / (paddle_width / 2)
		if angle_ratio != 0:
			resulting_angle = math.pi / 2 - angle_ratio * (math.pi / 2 - math.pi / 6)
			resulting_cotangent = 1 / math.tan(resulting_angle)

			if dist_from_paddle_center > 0:
				self.direction.x = resulting_cotangent * abs(self.direction.y)
			else:
				self.direction.x = -1 * resulting_cotangent * abs(self.direction.y)
		else:
			self.direction.x = 0

	def handle_bounce(self, overlapping_rect: pygame.rect.Rect, colliding_players):
		if len(colliding_players) > 0:
			if overlapping_rect.height > overlapping_rect.width:
				self.handle_hor_hit_by_player(colliding_players)
			elif overlapping_rect.width > overlapping_rect.height:
				self.handle_vertical_collision(overlapping_rect)
				self.paddle_adjust_angle(overlapping_rect)
			else:
				self.handle_diagonal_collision(overlapping_rect)
		else:
			# Vertical
			if overlapping_rect.width > overlapping_rect.height:
				self.handle_vertical_collision(overlapping_rect)
			# Horizontal
			if overlapping_rect.height > overlapping_rect.width:
				self.handle_horizontal_collision(overlapping_rect)
			# Diagonal
			if overlapping_rect.height == overlapping_rect.width:
				self.handle_diagonal_collision(overlapping_rect)

	def handle_collisions(self):
		colliding_blocks = pygame.sprite.spritecollide(self, self.sprite_manager.block_sprites_group, False)
		colliding_players = pygame.sprite.spritecollide(self, self.sprite_manager.player_sprites_group, False)
		colliding_sprites = colliding_blocks + colliding_players
		if len(colliding_sprites) > 0:
			overlap_rect = self.get_overlapping_rect(colliding_sprites=colliding_sprites)
			self.handle_bounce(overlapping_rect=overlap_rect, colliding_players=colliding_players)

			if len(colliding_players) == 0:

				for sprite in colliding_sprites:
					if getattr(sprite, 'health', None):
						for _ in range(self.strength):
							sprite.get_damage(1)
			else:
				self.hit_paddle_sound.stop()
				self.hit_paddle_sound.play()
			self.position.x = self.rect.x
			self.position.y = self.rect.y

	def update(self, delta_time, keys_pressed: pygame.key.ScancodeWrapper):

		if self.active:

			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()

			self.movement(delta_time)
			self.frame_collision()
			self.handle_collisions()

		else:
			if time.time() - self.time_delay_counter > 0.5:
				self.rect.midbottom = self.sprite_manager.player_sprites_group.sprites()[0].rect.midtop
				self.position = pygame.math.Vector2(self.rect.topleft)

				if keys_pressed[pygame.K_SPACE]:
					self.active = True
					self.direction = pygame.math.Vector2((0, -1))
			else:
				pass


class Scoreboard(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

	def update(self):
		pass


class PowerUpIcon(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

	def update(self, time):
		pass


class PowerUpTimerInfo(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame,
			font: pygame.font.Font,
			color: pygame.Color,
			power_name: str,
			powerup_time: [int, float]
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

		self.font = font
		self.color = color
		self.powerup_time = powerup_time
		self.start_time = time.time()
		self.power_name = power_name

	def update(self):
		time_left = self.powerup_time - (time.time() - self.start_time)
		old_rect_center = self.rect.center
		if time_left > 0:
			self.image = self.font.render(
				f'{self.power_name.upper()} Time Left: {time_left:.2f}', True, self.color)
			self.rect = self.image.get_rect(center=old_rect_center)
		else:
			self.kill()
