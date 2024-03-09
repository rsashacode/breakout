import time
import math
import settings


class PowerUpTimer:
	def __init__(self):
		self.start_time = None
		self.current_time = None

		self.duration = None
		self.active = False

	def start(self, duration: int):
		current_time = time.time()

		self.start_time, self.current_time = current_time, current_time
		self.duration = duration
		self.active = True

	def update(self, time_in_pause: float = 0):
		if self.active:
			self.start_time += time_in_pause
			self.current_time = time.time()

			if self.current_time - self.start_time > self.duration:
				self.active = False
				self.duration, self.start_time, self.current_time = (None, None, None)


class PowerUpManager:
	def __init__(self, sprite_manager):
		self.sprite_manager = sprite_manager

		self.trigger_methods = {
			'add-life': self.activate_add_life,
			'big-ball': self.activate_big_ball,
			'small-ball': self.activate_small_ball,
			'fast-ball': self.activate_fast_ball,
			'slow-ball': self.activate_slow_ball,
			'multiply-balls': self.activate_multiple_balls,
			'super-ball': self.activate_super_ball,
			'big-paddle': self.activate_big_paddle,
			'small-paddle': self.activate_small_paddle
		}

		self.active_powerups = []

		self.ball_size_timer = PowerUpTimer()
		self.ball_speed_timer = PowerUpTimer()
		self.ball_strength_timer = PowerUpTimer()
		self.paddle_size_timer = PowerUpTimer()

	def activate_powerup(self, power: str):
		try:
			self.trigger_methods[power]()
			if power not in ['add-life', 'multiply-balls']:
				self.active_powerups.append(power)
		except KeyError as e:
			print('Unknown power! Skip activating', str(e))

	def deactivate_powerup(self, power: str):
		try:
			self.trigger_methods[power]()
		except KeyError as e:
			print('Unknown power! Skip deactivating', str(e))

	def activate_add_life(self):
		print('activating add-life')
		self.sprite_manager.player_sprites_group.sprites()[0].add_health()

	def activate_big_ball(self, start_timer=True):
		print('Activating big-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():

			new_width = round(ball.original_width * 1.5)
			new_height = round(ball.original_width * 1.5)
			ball.change_size(new_width, new_height)

		if start_timer:
			self.ball_size_timer.start(settings.BALL_SIZE_DURATION)

	def activate_small_ball(self, start_timer=True):
		print('activating small-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():

			new_width = round(ball.original_width * 0.5)
			new_height = round(ball.original_height * 0.5)
			ball.change_size(new_width, new_height)

		if start_timer:
			self.ball_size_timer.start(settings.BALL_SIZE_DURATION)

	def activate_fast_ball(self, start_timer=True):
		print('activating fast-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.change_speed(int(ball.original_speed * 2))

		if start_timer:
			self.ball_speed_timer.start(settings.BALL_SPEED_DURATION)

	def activate_slow_ball(self, start_timer=True):
		print('activating slow-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.change_speed(int(ball.original_speed * 0.5))

		if start_timer:
			self.ball_speed_timer.start(settings.BALL_SPEED_DURATION)

	def activate_multiple_balls(self):
		print('activating multiple balls')
		balls_in_game = self.sprite_manager.ball_sprites_group.sprites()

		if len(balls_in_game) <= 20:
			for ball in balls_in_game:

				left_angle = math.radians(-135)
				right_angle = math.radians(-45)

				ball_kwargs = {
					'speed': ball.speed,
					'original_speed': ball.original_speed,
					'original_width': ball.original_width,
					'original_height': ball.original_height,
					'strength': ball.strength,
					'original_strength': ball.original_strength,
					'active': True,
					'big_ball': False,
					'small_ball': False,
					'fast_ball': False,
					'slow_ball': False,
					'super_ball': False,
				}
				for angle in [left_angle, right_angle]:
					self.sprite_manager.create_ball(
						ball_image=ball.image,
						midbottom=ball.original_rect.midbottom,
						angle_radians=angle,
						**ball_kwargs
					)
				if 'big-ball' in self.active_powerups:
					self.activate_big_ball(start_timer=False)
				if 'small-ball' in self.active_powerups:
					self.activate_small_ball(start_timer=False)

	def activate_super_ball(self, start_timer=True):
		print('Activating super-ball')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.change_strength(int(ball.original_strength * 2))

			if start_timer:
				self.ball_strength_timer.start(settings.BALL_STRENGTH_DURATION)

	def activate_big_paddle(self, start_timer=True):
		print('Activating big-paddle')
		for player in self.sprite_manager.player_sprites_group.sprites():

			original_width = player.original_width
			original_height = player.original_height
			new_paddle_width = int(original_width * 2)

			player.change_size(new_paddle_width, original_height)

		if start_timer:
			self.paddle_size_timer.start(settings.PADDLE_SIZE_DURATION)

	def activate_small_paddle(self, start_timer=True):
		print('Activating small paddle')
		for player in self.sprite_manager.player_sprites_group.sprites():
			original_width = player.original_width
			original_height = player.original_height
			new_paddle_width = int(original_width * 0.5)
			player.change_size(new_paddle_width, original_height)

		if start_timer:
			self.paddle_size_timer.start(settings.PADDLE_SIZE_DURATION)

	def deactivate_paddle_size(self):
		print('Deactivating paddle size powerup')
		for player in self.sprite_manager.player_sprites_group.sprites():
			player.restore_size()
		for power in ['big-paddle', 'small-paddle']:
			if power in self.active_powerups:
				self.active_powerups.remove(power)

	def deactivate_ball_size(self):
		print('Deactivating ball size powerup')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.restore_size()
		for power in ['big-ball', 'small-ball']:
			if power in self.active_powerups:
				self.active_powerups.remove(power)

	def deactivate_ball_speed(self):
		print('Deactivating ball speed powerup')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.restore_speed()
		for power in ['fast-ball', 'slow-ball']:
			if power in self.active_powerups:
				self.active_powerups.remove(power)

	def deactivate_ball_strength(self):
		print('Deactivating ball strength powerup')
		for ball in self.sprite_manager.ball_sprites_group.sprites():
			ball.restore_strength()
		if 'super-ball' in self.active_powerups:
			self.active_powerups.remove('super-ball')

	def update(self, time_in_pause: float = 0):
		if self.paddle_size_timer.active:
			self.paddle_size_timer.update(time_in_pause)
			if not self.paddle_size_timer.active:
				self.deactivate_paddle_size()

		if self.ball_size_timer.active:
			self.ball_size_timer.update(time_in_pause)
			if not self.ball_size_timer.active:
				self.deactivate_ball_size()

		if self.ball_speed_timer.active:
			self.ball_speed_timer.update(time_in_pause)
			if not self.ball_speed_timer.active:
				self.deactivate_ball_speed()

		if self.ball_strength_timer.active:
			self.ball_strength_timer.update(time_in_pause)
			if not self.ball_strength_timer.active:
				self.deactivate_ball_strength()
