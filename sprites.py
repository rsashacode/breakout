import pygame
import settings
import random

from pygame.sprite import AbstractGroup


class Player(pygame.sprite.Sprite):
	def __init__(self, groups: AbstractGroup):
		super().__init__(groups)

		# setup
		self.image = pygame.Surface(size=(settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT))
		self.image.fill('white')

		# position
		self.rect = self.image.get_rect(midbottom=(settings.GAME_WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
		self.last_frame_rect = self.rect.copy()

		self.direction = pygame.math.Vector2()
		self.position = pygame.math.Vector2(self.rect.topleft)

	def check_screen_constraint(self):
		if self.rect.right > settings.GAME_WINDOW_WIDTH:
			self.rect.right = settings.GAME_WINDOW_WIDTH
			self.position.x = self.rect.x

		if self.rect.left < 0:
			self.rect.left = 0
			self.position.x = self.rect.x

	def update(self, delta_time, keys_pressed: pygame.key.ScancodeWrapper):
		self.last_frame_rect = self.rect.copy()

		if keys_pressed[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys_pressed[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		self.check_screen_constraint()

		self.position.x += self.direction.x * settings.DEFAULT_PADDLE_SPEED * delta_time
		self.rect.x = round(self.position.x)


class Scoreboard(pygame.sprite.Sprite):
	def __init__(self, groups):
		super().__init__(groups)
		self.image = pygame.image.load('assets/other/scoreboard.jpg').convert_alpha()
		self.image = pygame.transform.scale(self.image, (settings.SCOREBOARD_WIDTH, settings.WINDOW_HEIGHT))
		self.rect = self.image.get_rect(topright=(settings.WINDOW_WIDTH, 0))
		#heart
		self.heart_surf = pygame.image.load('./assets/other/heart.png').convert_alpha()
		self.rect_H = self.heart_surf.get_rect(topright=(600, 0))

	def display_hearts(self):
		for i in range(3):
			x = i * self.heart_surf.get_width()
			self.display_surface.blit(self.heart_surf, (x, 4))

		self.display_hearts()


class Block(pygame.sprite.Sprite):
	def __init__(self, health: int, pos: tuple[int, int], groups):
		super().__init__(groups)

		# damage information
		self.health = health

		# Image
		self.image = pygame.Surface(size=(settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT))
		self.image.fill(color=settings.COLOR_LEGEND[self.health])

		self.rect = self.image.get_rect(topleft=pos)
		self.last_frame_rect = self.rect.copy()

	def get_damage(self, amount: int):
		self.health -= amount

	def update(self):
		self.last_frame_rect = self.rect.copy()
		if self.health > 0:
			self.image.fill(color=settings.COLOR_LEGEND[self.health])
		else:
			self.kill()


class Ball(pygame.sprite.Sprite):
	def __init__(self, groups, player: Player, blocks: [Block]):
		super().__init__(groups)

		# collision objects
		self.player = player
		self.blocks = blocks

		# graphics setup
		self.image = pygame.image.load('./assets/other/Ball.png').convert_alpha()

		# position setup
		self.rect = self.image.get_rect(midbottom=player.rect.midtop)
		self.position = pygame.math.Vector2(x=self.rect.topleft)
		self.direction = pygame.math.Vector2(x=(random.choice((1, -1)), -1))
		self.speed = settings.DEFAULT_BALL_SPEED
		self.last_frame_rect = self.rect.copy()
		self.last_frame_position = self.position.copy()

		self.active = False

	def randomize_direction(self):
		self.direction.x *= random.randrange(
			100 - settings.DIRECTION_RANDOMIZATION,
			100 + settings.DIRECTION_RANDOMIZATION) / 100
		self.direction.y *= random.randrange(
			100 - settings.DIRECTION_RANDOMIZATION,
			100 + settings.DIRECTION_RANDOMIZATION) / 100

	def get_overlapping_sprites(self) -> [pygame.sprite.Sprite]:
		overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
		if self.rect.colliderect(self.player.rect):
			overlap_sprites.append(self.player)
		return overlap_sprites

	def movement(self, delta_time):
		self.position.x += self.direction.x * self.speed * delta_time
		self.position.y += self.direction.y * self.speed * delta_time
		self.rect.x = round(self.position.x)
		self.rect.y = round(self.position.y)

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
		elif self.rect.bottom > settings.GAME_WINDOW_HEIGHT:
			self.active = False

	def sprites_collision(self):
		# Get colliding sprites
		colliding_sprites = self.get_overlapping_sprites()
		if len(colliding_sprites) > 0:
			# Introducing variables
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
				if getattr(sprite, 'health', None):
					sprite.get_damage(1)

			collision_rectangle_width = abs(total_overlap_left - total_overlap_right)
			collision_rectangle_height = abs(total_overlap_top - total_overlap_bottom)

			if collision_rectangle_width > collision_rectangle_height:
				if self.direction.y < 0:
					self.rect.top = total_overlap_bottom
				else:
					self.rect.bottom = total_overlap_top
				self.direction.y *= -1
			elif collision_rectangle_height == self.rect.height and collision_rectangle_width == self.rect.width:
				raise RuntimeError("Tunneling!!!")
			else:
				if self.direction.x < 0:
					self.rect.left = total_overlap_right
				else:
					self.rect.right = total_overlap_left
				self.direction.x *= -1

			if self.player in colliding_sprites:
				# ToDo Direction depending on where ball hits the paddle
				self.randomize_direction()

	def update(self, delta_time):
		if self.active:

			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()

			self.last_frame_rect = self.rect.copy()
			self.last_frame_position = self.position.copy()

			self.movement(delta_time)

			self.frame_collision()
			self.sprites_collision()
		else:
			self.rect.midbottom = self.player.rect.midtop
			self.position = pygame.math.Vector2(self.rect.topleft)
