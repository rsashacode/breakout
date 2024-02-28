from typing import Iterable

import pygame
import settings
import random

from pygame.sprite import AbstractGroup


class Player(pygame.sprite.Sprite):
	def __init__(self, groups: AbstractGroup):
		super().__init__(groups)

		# setup
		self.image = pygame.Surface(size=(settings.WINDOW_WIDTH // 10, settings.WINDOW_HEIGHT // 20))
		self.image.fill('white')

		# position
		self.rect = self.image.get_rect(midbottom=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
		self.old_rect = self.rect.copy()
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(x=self.rect.topleft)
		self.speed = 300

	def input(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def screen_constraint(self):
		if self.rect.right > settings.WINDOW_WIDTH - 160:
			self.rect.right = settings.WINDOW_WIDTH - 160
			self.pos.x = self.rect.x
		if self.rect.left < 0:
			self.rect.left = 0
			self.pos.x = self.rect.x

	def update(self, dt: (int, float)):
		self.old_rect = self.rect.copy()
		self.input()
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.x = round(self.pos.x) 
		self.screen_constraint()


class Scoreboard(pygame.sprite.Sprite):
	def __init__(self, groups: Iterable[pygame.sprite.Sprite]):
		super().__init__(groups)
		self.image = pygame.image.load('assets/other/scoreboard.jpg').convert_alpha()
		self.image = pygame.transform.scale(self.image, (160, 720))
		self.rect = self.image.get_rect(topright=(settings.WINDOW_WIDTH, 0))


class Block(pygame.sprite.Sprite):
	def __init__(self, block_type: int, pos: tuple[int, int], groups):
		super().__init__(groups)
		self.image = pygame.Surface(size=(settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT))
		self.rect = self.image.get_rect(topleft=pos)
		self.old_rect = self.rect.copy()

		# damage information
		self.health = int(block_type)

	def get_damage(self, amount: int):
		self.health -= amount

		if self.health > 0:
			# update the image
			pass
		else:
			self.kill()


class Ball(pygame.sprite.Sprite):
	def __init__(self, groups: AbstractGroup, player: Player, blocks: [Block]):
		super().__init__(groups)

		# collision objects
		self.player = player
		self.blocks = blocks

		# graphics setup
		self.image = pygame.image.load('assets/other/Ball.png').convert_alpha()

		# position setup
		self.rect = self.image.get_rect(midbottom=player.rect.midtop)
		self.old_rect = self.rect.copy()
		self.pos = pygame.math.Vector2(x=self.rect.topleft)
		self.direction = pygame.math.Vector2(x=(random.choice((1, -1)), -1))
		self.speed = 400

		# active
		self.active = False

	def window_collision(self, direction: str):
		if direction == 'horizontal':
			if self.rect.left < 0:
				self.rect.left = 0
				self.pos.x = self.rect.x
				self.direction.x *= -1

			if self.rect.right > settings.WINDOW_WIDTH - 160:
				self.rect.right = settings.WINDOW_WIDTH - 160
				self.pos.x = self.rect.x
				self.direction.x *= -1

		if direction == 'vertical':
			if self.rect.top < 0:
				self.rect.top = 0
				self.pos.y = self.rect.y
				self.direction.y *= -1

			if self.rect.bottom > settings.WINDOW_HEIGHT:
				self.active = False

	def collision(self, direction):
		# find overlapping objects
		overlap_sprites = pygame.sprite.spritecollide(sprite=self, group=self.blocks, dokill=False)
		if self.rect.colliderect(self.player.rect):
			overlap_sprites.append(self.player)

		if overlap_sprites:
			if direction == 'horizontal':
				for sprite in overlap_sprites:
					if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
						self.rect.right = sprite.rect.left - 1
						self.pos.x = self.rect.x
						self.direction.x *= -1

					if self.rect.left <= sprite.rect.right and self.old_rect.right >= sprite.old_rect.left:
						self.rect.left = sprite.rect.left + 1
						self.pos.x = self.rect.x
						self.direction.x *= -1

					if getattr(sprite, 'health', None):
						sprite.get_damage(1)

			if direction == 'vertical':
				for sprite in overlap_sprites:
					if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
						self.rect.bottom = sprite.rect.top - 1
						self.pos.y = self.rect.y
						self.direction.y *= -1

					if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
						self.rect.top = sprite.rect.bottom + 1
						self.pos.y = self.rect.y
						self.direction.y *= -1

					if getattr(sprite, 'health', None):
						sprite.get_damage(1)

	def update(self, dt):
		if self.active:

			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()

			# create old rect
			self.old_rect = self.rect.copy()

			# horizontal movement + collision
			self.pos.x += self.direction.x * self.speed * dt
			self.rect.x = round(self.pos.x)
			self.collision('horizontal')
			self.window_collision('horizontal')

			# vertical movement + collision
			self.pos.y += self.direction.y * self.speed * dt
			self.rect.y = round(self.pos.y)
			self.collision('vertical')
			self.window_collision('vertical')
		else:
			self.rect.midbottom = self.player.rect.midtop
			self.pos = pygame.math.Vector2(self.rect.topleft)