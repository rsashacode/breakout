import pygame
import settings
import sys

from sprite_manager import SpriteManager


def create_bg():
    bg_original = pygame.image.load('./assets/background/background.jpg').convert()
    scale_factor = settings.WINDOW_HEIGHT / bg_original.get_height()
    scaled_width = bg_original.get_width() * scale_factor
    scaled_height = bg_original.get_height() * scale_factor
    scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
    return scaled_bg

class Menu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game Menu')
        
        # Load and scale the background image
        self.bg_image = pygame.image.load('./assets/background/menu.png').convert()
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
    
    def navigate(self, key):
        if key == pygame.K_UP and self.selected_option > 0:
            self.selected_option -= 1
        elif key == pygame.K_DOWN and self.selected_option < len(self.options) - 1:
            self.selected_option += 1
        elif key == pygame.K_RETURN:
            if self.selected_option == 0:
                pygame.mixer.music.stop()
                # Start the game
                game = Game()
                game.run()
            elif self.selected_option == 1:
                # Difficult mode is not yet implemented
                pass

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.navigate(event.key)

            # Render the background and text
            self.display_surface.blit(self.bg_image, (0, 0))

            # Render the title
            self.render_text(self.title_text, (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 4), False)

            # Render the menu options
            for index, option in enumerate(self.options):
                position = (settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + index * 50)
                self.render_text(option, position, selected=index == self.selected_option)

            pygame.display.update()

        pygame.quit()
        sys.exit()
    


class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game')

        # background
        self.bg = create_bg()

        # sprites
        self.sprite_manager = SpriteManager()
        self.sprite_manager.init_level()

    def run(self):
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
            self.sprite_manager.update(delta_time, keys_pressed)

            self.display_surface.blit(source=self.bg, dest=(0, 0))
            self.sprite_manager.draw_all(self.display_surface)

            pygame.display.update()


if __name__ == '__main__':
    menu = Menu()
    menu.run()
