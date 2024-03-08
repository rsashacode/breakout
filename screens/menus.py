import pygame
import settings
import time

from path_utils import get_asset_path


class MainMenu:
	def __init__(self):
		# Load and scale the background image
		background_image_path = get_asset_path('images/background/menu.png')
		self.background = pygame.image.load(background_image_path).convert()
		self.background = pygame.transform.scale(self.background, (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
		self.background.set_alpha(20)

		# Setup font and text rendering
		self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
		self.options = ['EASY', 'NORMAL', 'HARD']
		self.selected_option = 1  # Index of the currently selected option

		# Setup objects to blit
		self.title_surface = self.font.render(
			'WELCOME TO BREAKOUT! CHOOSE YOUR DIFFICULTY:',
			True,
			(255, 255, 255))
		self.title_rect = self.title_surface.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 4))
		self.objects_to_blit = []

		self.active = True
		self.update_objects_to_blit()

		# Used to handle smooth selection
		self.last_pressed = time.time()

	def update_objects_to_blit(self):
		for i, option in enumerate(self.options):
			position = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + i * settings.WINDOW_WIDTH // 15)
			if self.selected_option == i:
				color = (255, 0, 0)
			else:
				color = (255, 255, 255)
			surface_to_blit = self.font.render(option, True, color)
			rect_to_blit = surface_to_blit.get_rect(center=position)
			self.objects_to_blit.append([surface_to_blit, rect_to_blit])

	def update(self, keys_pressed: pygame.key.ScancodeWrapper):
		if time.time() - self.last_pressed >= 0.2:
			if keys_pressed[pygame.K_UP]:
				self.selected_option = max(0, self.selected_option - 1)
				self.last_pressed = time.time()
			elif keys_pressed[pygame.K_DOWN]:
				self.selected_option = min(len(self.options) - 1, self.selected_option + 1)
				self.last_pressed = time.time()
			elif keys_pressed[pygame.K_RETURN]:
				if self.selected_option in [0, 1, 2]:
					self.active = False
			self.update_objects_to_blit()


class LevelMenu:
	def __init__(self):
		self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
		self.text = 'CONGRATULATIONS! PRESS [ENTER] TO CONTINUE.'

		self.text_surface = self.font.render(self.text, True, (255, 255, 255))
		self.text_rect = self.text_surface.get_rect(
			center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
		)
		self.active = False

	def update(self, keys_pressed: pygame.key.ScancodeWrapper):
		if keys_pressed[pygame.K_RETURN]:
			self.active = False


class EndGameMenu:
	def __init__(self):
		self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
		self.text = 'END GAME. PRESS [ENTER] TO RESTART'

		self.text_surface = self.font.render(self.text, True, (0, 0, 0))
		self.text_rect = self.text_surface.get_rect(
			center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
		)
		self.active = False
		self.restart_needed = False

	def update(self, keys_pressed: pygame.key.ScancodeWrapper, score: int):
		self.text = f'YOUR FINAL SCORE: {score}. PRESS [ENTER] TO RESTART'
		self.text_surface = self.font.render(self.text, True, (255, 255, 255))
		self.text_rect = self.text_surface.get_rect(
			center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
		)
		if self.active:
			if keys_pressed[pygame.K_RETURN]:
				self.active = False
				self.restart_needed = True


class PauseMenu:
	def __init__(self):
		self.font = pygame.font.Font(settings.GAME_FONT, settings.MENU_FONT_SIZE)
		self.text = 'PAUSE. PRESS [SPACE] TO CONTINUE.'

		self.text_surface = self.font.render(self.text, True, (255, 255, 255))
		self.text_rect = self.text_surface.get_rect(
			center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2)
		)
		self.active = False

	def update(self, keys_pressed: pygame.key.ScancodeWrapper):
		if keys_pressed[pygame.K_SPACE]:
			self.active = False
