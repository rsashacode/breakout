import pygame
import settings
import random
import math
import time

from pygame.sprite import AbstractGroup


class GameSprite(pygame.sprite.Sprite):
	def __init__(self, groups, image: pygame.Surface, rect: pygame.Rect):
		super().__init__(groups)

		self.image = image
		self.rect = rect
		self.position = pygame.math.Vector2(self.rect.topleft)

		self.last_frame_rect = self.rect.copy()
		self.last_frame_position = self.position.copy()

	def update(self, *args, **kwargs):
		raise NotImplemented('Sprite must implement "update" method')


class Heart(GameSprite):
	def __init__(self, groups, image: pygame.Surface, rect: pygame.Rect):
		super().__init__(groups, image, rect)
		self.active = True

	def update(self):
		if not self.active:
			self.kill()


class Player(GameSprite):
	def __init__(self, groups: AbstractGroup, image: pygame.Surface, rect: pygame.Rect, heart_group):
		super().__init__(groups, image, rect)
		self.direction = pygame.math.Vector2()
		self.health = settings.MAX_PLAYER_HEALTH
		self.heart_group = heart_group

	def check_screen_constraint(self):
		if self.rect.right > settings.GAME_WINDOW_WIDTH:
			self.rect.right = settings.GAME_WINDOW_WIDTH
			self.position.x = self.rect.x

		if self.rect.left < 0:
			self.rect.left = 0
			self.position.x = self.rect.x

	def move_paddle(self, delta_time):
		self.position.x += self.direction.x * settings.DEFAULT_PADDLE_SPEED * delta_time

	def loose_health(self, score_obj):
		if self.health >= 1:
			self.health -= 1
			heart_sprites = self.heart_group.sprites()
			heart_sprites[-1].active = False
			score_obj.subtract_score(200)

	def get_health(self):
		if self.health < settings.MAX_PLAYER_HEALTH:
			self.health += 1
			# ToDo Initialise new Heart Object

	def update(self, delta_time, keys_pressed: pygame.key.ScancodeWrapper):
		self.last_frame_rect = self.rect.copy()

		if keys_pressed[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys_pressed[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

		self.check_screen_constraint()
		self.move_paddle(delta_time)
		self.rect.x = round(self.position.x)


class PowerUp(GameSprite):
	def __init__(self, groups, image: pygame.Surface, rect: pygame.Rect, player: Player, score):
		super().__init__(groups, image, rect)
		self.player = player
		self.speed = settings.DEFAULT_POWERUP_SPEED
		self.score = score
		self.visible = 0

	def update(self):
		if self.visible:
			self.rect.y += self.speed
			if pygame.sprite.collide_rect(self, self.player):
				self.visible = 0
				self.score.add_score(100)
				self.kill()
			elif self.rect.top > settings.GAME_WINDOW_HEIGHT:
					self.visible = 0
					self.kill()


class Block(GameSprite):
	def __init__(self, groups, image: pygame.Surface, rect: pygame.Rect, health: int, power_up: [PowerUp, None]):
		super().__init__(groups, image, rect)
		self.health = health
		self.power_up = power_up
		self.update_image()

	# damage information
	def get_damage(self, amount: int, score_obj):
		self.health -= amount
		score_obj.add_score(10)
		if self.health <= 0:
			score_obj.add_score(10)
			self.kill()
			if self.power_up is not None:
				self.power_up.visible = 1
	
	def update_image(self):
		if self.health in settings.COLOR_LEGEND:
			self.image = pygame.image.load(settings.COLOR_LEGEND[self.health])

	def activate_powerup(self):
		self.power_up.visible = 1

	def update(self):
		self.last_frame_rect = self.rect.copy()
		self.update_image()
		if self.health <= 0:
			self.kill()
			if self.power_up is not None:
				self.activate_powerup()


class Ball(GameSprite):
	def __init__(self, groups, image: pygame.Surface, rect: pygame.Rect, player: Player, blocks: [Block], score):
		super().__init__(groups, image, rect)

		# collision objects
		self.player = player
		self.blocks = blocks
		self.score = score
		

		self.direction = pygame.math.Vector2(x=(random.choice((1, -1)), -1))
		self.speed = settings.DEFAULT_BALL_SPEED

		self.time_delay_counter = 0
		self.active = False

	def movement(self, delta_time):
		self.position.x += self.direction.x * self.speed * delta_time
		self.position.y += self.direction.y * self.speed * delta_time
		self.rect.x = round(self.position.x)
		self.rect.y = round(self.position.y)

	def loose_the_ball(self, score_obj):
		self.active = False
		self.time_delay_counter = time.time()
		self.player.loose_health(score_obj)

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
			self.loose_the_ball(self.score)

	def get_overlapping_sprites(self) -> [pygame.sprite.Sprite]:
		overlap_sprites = pygame.sprite.spritecollide(self, self.blocks, False)
		if self.rect.colliderect(self.player.rect):
			overlap_sprites.append(self.player)
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
			self.loose_the_ball(self.score)

		hit_point_x = overlapping_rect.centerx
		paddle_middle = self.player.rect.centerx
		paddle_width = self.player.rect.width

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
			if self.player not in colliding_sprites:

				for sprite in colliding_sprites:
					if getattr(sprite, 'health', None):
						sprite.get_damage(1, self.score)

				self.handle_block_bounce(overlapping_rect=overlap_rect)
			else:
				self.handle_paddle_collision(overlap_rect)

	def update(self, delta_time, keys_pressed: pygame.key.ScancodeWrapper):

		if self.active:

			if self.direction.magnitude() != 0:
				self.direction = self.direction.normalize()

			self.last_frame_rect = self.rect.copy()
			self.last_frame_position = self.position.copy()

			self.movement(delta_time)
			self.frame_collision()
			self.sprite_collisions()
		else:
			if time.time() - self.time_delay_counter > 0.5:
				self.rect.midbottom = self.player.rect.midtop
				self.position = pygame.math.Vector2(self.rect.topleft)

			if keys_pressed[pygame.K_SPACE]:
				self.active = True
				self.direction = pygame.math.Vector2(x=(random.choice((1, -1)), -1))


class Scoreboard(GameSprite):
	def __init__(self, groups, image: pygame.Surface, rect: pygame.Rect):
		super().__init__(groups, image, rect)

	def update(self):
		pass


class Score(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.color = pygame.Color('white')
        self.update_text()
        self.rect = self.image.get_rect(center=(settings.WINDOW_WIDTH - 82, 150))

    def add_score(self, points):
        self.score += points
        self.update_text()

    def subtract_score(self, points):
        self.score -= points
        self.update_text()

    def update_text(self):
        self.image = self.font.render(f'Score: {self.score}', True, self.color)