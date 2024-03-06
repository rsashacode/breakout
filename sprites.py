import pygame
import settings
import random
import math
import time

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

	def update(self, *args, **kwargs):
		raise NotImplemented('Sprite must implement "update" method')


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

		# powerups
		self.big_paddle = False
		self.small_paddle = False

	def activate_big_paddle(self):
		if not self.big_paddle:
			new_paddle_width = int(settings.PADDLE_WIDTH * 2)
			self.image = pygame.Surface(size=(new_paddle_width, settings.PADDLE_HEIGHT))
			self.image.fill('white')
			self.rect = self.image.get_rect(midbottom=(self.rect.midbottom[0], self.rect.midbottom[1]))
			self.big_paddle = True

	def activate_small_paddle(self):
		if not self.small_paddle:
			new_paddle_width = int(settings.PADDLE_WIDTH * 0.5)
			self.image = pygame.Surface(size=(new_paddle_width, settings.PADDLE_HEIGHT))
			self.image.fill('white')
			self.rect = self.image.get_rect(midbottom=(self.rect.midbottom[0], self.rect.midbottom[1]))
			self.small_paddle = True

	def check_screen_constraint(self):
		if self.rect.right > settings.GAME_WINDOW_WIDTH:
			self.rect.right = settings.GAME_WINDOW_WIDTH
			self.position.x = self.rect.x

		if self.rect.left < 0:
			self.rect.left = 0
			self.position.x = self.rect.x

	def move_paddle(self, delta_time):
		self.position.x += self.direction.x * settings.DEFAULT_PADDLE_SPEED * delta_time

	def loose_health(self):
		if self.health >= 1:
			self.health -= 1
			heart_sprites = self.sprite_manager.heart_sprites_group.sprites()
			heart_sprites[-1].kill()
			self.sprite_manager.score_sprites_group.sprites()[0].subtract_score(200)

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

		self.check_screen_constraint()
		self.move_paddle(delta_time)
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
		self.image = self.font.render(f'Score: {self.score}', True, self.color)


class PowerUp(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
			power: str = ''
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

		self.direction = pygame.math.Vector2((0, 1))
		self.speed = settings.DEFAULT_POWERUP_SPEED
		self.power = power

		self.trigger_methods = {
			'add-life': self.trigger_add_life,
			'big-ball': self.trigger_big_ball,
			'small-ball': self.trigger_small_ball,
			'fast-ball': self.trigger_fast_ball,
			'slow-ball': self.trigger_slow_ball,
			'multiply-balls': self.trigger_multiple_balls,
			'super-ball': self.trigger_super_ball,
			'big-paddle': self.trigger_big_paddle,
			'small-paddle': self.trigger_small_paddle
		}

	def movement(self, delta_time):
		self.position.x += self.direction.x * self.speed * delta_time
		self.position.y += self.direction.y * self.speed * delta_time
		self.rect.x = round(self.position.x)
		self.rect.y = round(self.position.y)

	def trigger_add_life(self):
		print('activating add-life')
		self.sprite_manager.player_sprites_group.sprites()[0].add_health()

	def trigger_big_ball(self):
		print('activating big-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.activate_big_ball()

	def trigger_small_ball(self):
		print('activating small-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.activate_small_ball()

	def trigger_fast_ball(self):
		print('activating fast-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.activate_fast_ball()

	def trigger_slow_ball(self):
		print('activating slow-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.activate_slow_ball()

	def trigger_multiple_balls(self):
		print('activating multiple balls')
		balls_in_game = self.sprite_manager.ball_sprites_group.sprites()
		for ball in balls_in_game:
			original_angle = ball.get_angle_of_direction()
			left_angle = original_angle + math.radians(15)
			right_angle = original_angle - math.radians(15)

			kwargs = {
				'speed': ball.speed,
				'strength': ball.strength,
				'active': True,
				'big_ball': False,
				'small_ball': False,
				'fast_ball': False,
				'slow_ball': False,
				'super_ball': False,
			}

			self.sprite_manager.create_ball(
				ball_image=ball.image,
				midbottom=ball.rect.midbottom,
				angle_radians=left_angle,
				**kwargs
			)
			self.sprite_manager.create_ball(
				ball_image=ball.image,
				midbottom=ball.rect.midbottom,
				angle_radians=right_angle,
				**kwargs
			)

	def trigger_super_ball(self):
		print('Activating super-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.activate_super_ball()

	def trigger_big_paddle(self):
		print('Activating big-paddle')
		self.sprite_manager.player_sprites_group.sprites()[0].activate_big_paddle()

	def trigger_small_paddle(self):
		print('Activating small paddle')
		self.sprite_manager.player_sprites_group.sprites()[0].activate_small_paddle()

	def activate(self):
		try:
			self.trigger_methods[self.power]()
		except KeyError as err:
			print(err, "Unknown power: " + self.power)

	def update(self, delta_time):
		if self.rect.top > settings.GAME_WINDOW_HEIGHT:
			self.kill()
		if pygame.sprite.collide_rect(self, self.sprite_manager.player_sprites_group.sprites()[0]):
			self.activate()
			self.sprite_manager.score_sprites_group.sprites()[0].add_score(100)
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

	# damage information
	def get_damage(self, amount: int):
		self.health -= amount
		self.sprite_manager.score_sprites_group.sprites()[0].add_score(10)

	def update_image(self):
		if self.health in settings.COLOR_LEGEND:
			self.image = pygame.image.load(settings.COLOR_LEGEND[self.health])

	def update(self):
		self.update_image()
		if self.health <= 0:
			self.kill()
			self.sprite_manager.activate_powerup(self)


class Ball(GameSprite):
	def __init__(
			self,
			sprite_manager,
			sprite_groups,
			image: pygame.Surface,
			rect: pygame.Rect,
	):
		super().__init__(sprite_manager=sprite_manager, sprite_groups=sprite_groups, image=image, rect=rect)

		self.direction = pygame.math.Vector2((random.choice((1, -1)), -1))
		self.speed = settings.DEFAULT_BALL_SPEED
		self.strength = 1

		self.time_delay_counter = 0
		self.active = False

		# powerups
		self.big_ball = False
		self.small_ball = False
		self.fast_ball = False
		self.slow_ball = False
		self.super_ball = False

	def activate_big_ball(self):
		if not self.big_ball:
			new_width = int(self.rect.width * 2)
			new_height = int(self.rect.width * 2)
			self.image = pygame.transform.scale(self.image, (new_width, new_height))
			self.rect.width = new_width
			self.rect.height = new_height

			self.big_ball = True

	def activate_small_ball(self):
		if not self.small_ball:
			new_width = int(self.rect.width * 0.5)
			new_height = int(self.rect.width * 0.5)
			self.image = pygame.transform.scale(self.image, (new_width, new_height))
			self.rect.width = new_width
			self.rect.height = new_height

			self.small_ball = True

	def activate_fast_ball(self):
		if not self.fast_ball:
			self.speed = int(self.speed * 2)
			self.fast_ball = True

	def activate_slow_ball(self):
		if not self.slow_ball:
			self.speed = int(self.speed * 0.5)
			self.slow_ball = True

	def activate_super_ball(self):
		if not self.super_ball:
			self.strength = 2
			self.super_ball = True

	def get_angle_of_direction(self):
		return math.atan2(self.direction[1], self.direction[0])

	def set_direction_from_angle(self, angle):
		self.direction = pygame.math.Vector2((math.cos(angle), math.sin(angle)))

	def movement(self, delta_time):
		self.position.x += self.direction.x * self.speed * delta_time
		self.position.y += self.direction.y * self.speed * delta_time
		self.rect.x = round(self.position.x)
		self.rect.y = round(self.position.y)

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

	def get_overlapping_sprites(self) -> [pygame.sprite.Sprite]:
		overlap_block_sprites = pygame.sprite.spritecollide(self, self.sprite_manager.block_sprites_group, False)
		overlap_player_sprites = pygame.sprite.spritecollide(self, self.sprite_manager.player_sprites_group, False)
		overlap_sprites = overlap_block_sprites + overlap_player_sprites
		return overlap_sprites

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

	def handle_block_bounce(self, overlapping_rect: pygame.rect.Rect) -> None:
		# Vertical collision
		if overlapping_rect.width > overlapping_rect.height:
			if self.direction.y < 0:
				self.rect.top = overlapping_rect.bottom
			else:
				self.rect.bottom = overlapping_rect.top
			self.direction.y *= -1
		# Horizontal collision
		elif overlapping_rect.height > overlapping_rect.width:
			if self.direction.x < 0:
				self.rect.left = overlapping_rect.right
			else:
				self.rect.right = overlapping_rect.left
			self.direction.x *= -1
		# Vertical and horizontal collision (perfectly hit an angle)
		else:
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

	def handle_paddle_collision(self, overlapping_rect: pygame.rect.Rect):
		# Vertical collision
		if overlapping_rect.width > overlapping_rect.height:
			if self.direction.y < 0:
				self.rect.top = overlapping_rect.bottom
			else:
				self.rect.bottom = overlapping_rect.top
		# Horizontal collision and Vertical and horizontal collision (perfectly hit an angle)
		else:
			self.loose_ball()

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
		self.direction.y *= -1

	def sprite_collisions(self):
		# Get colliding sprites
		colliding_sprites = self.get_overlapping_sprites()
		if len(colliding_sprites) > 0:
			overlap_rect = self.get_overlapping_rect(colliding_sprites=colliding_sprites)
			if self.sprite_manager.player_sprites_group.sprites()[0] not in colliding_sprites:

				for sprite in colliding_sprites:
					if getattr(sprite, 'health', None):
						for _ in range(self.strength):
							sprite.get_damage(1)

				self.handle_block_bounce(overlapping_rect=overlap_rect)
			else:
				self.handle_paddle_collision(overlap_rect)

	def update(self, delta_time, keys_pressed: pygame.key.ScancodeWrapper):

		if self.active:

			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()

			self.movement(delta_time)
			self.frame_collision()
			self.sprite_collisions()
		else:
			if time.time() - self.time_delay_counter > 0.5:
				self.rect.midbottom = self.sprite_manager.player_sprites_group.sprites()[0].rect.midtop
				self.position = pygame.math.Vector2(self.rect.topleft)

			if keys_pressed[pygame.K_SPACE]:
				self.active = True
				self.direction = pygame.math.Vector2((random.choice((1, -1)), -1))


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
