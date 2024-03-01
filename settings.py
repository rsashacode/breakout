import pygame 
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SCOREBOARD_WIDTH = 160

GAME_WINDOW_WIDTH = WINDOW_WIDTH - SCOREBOARD_WIDTH
GAME_WINDOW_HEIGHT = WINDOW_HEIGHT

PADDLE_WIDTH = GAME_WINDOW_WIDTH // 5
PADDLE_HEIGHT = WINDOW_HEIGHT // 40

DEFAULT_PADDLE_SPEED = 1000
DEFAULT_BALL_SPEED = 300

BLOCK_MAP = [
	'666666666666',
	'444557755444',
	'333333333333',
	'222222222222',
	'111111111111',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ']

COLOR_LEGEND = {
	1: pygame.image.load('./assets/blocks/blue.png'),
	2: pygame.image.load('./assets/blocks/bronce.png'),
	3: pygame.image.load('./assets/blocks/green.png'),
	4: pygame.image.load('./assets/blocks/grey.png'),
	5: pygame.image.load('./assets/blocks/orange.png'),
	6: pygame.image.load('./assets/blocks/purple.png'),
	7: pygame.image.load('./assets/blocks/red.png')
}

POWER_UP_IMAGES = [
    pygame.image.load('./assets/other/heart.png'),
    pygame.image.load('./assets/other/laser.png'),
    pygame.image.load('./assets/other/size.png'),
    pygame.image.load('./assets/other/speed.png'),
]


GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = GAME_WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE

FPS = 60
DIRECTION_CHANGE = 20

MAX_PLAYER_HEALTH = 3
