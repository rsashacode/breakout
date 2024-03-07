# GRAPHICS

RESOLUTIONS = {
	'800x600': {
		'window-width': 800,
		'window-height': 600,
	},
	'1280x720': {
		'window-width': 1280,
		'window-height': 720,
	},
	'1366x768': {
		'window-width': 1366,
		'window-height': 768,
	},
	'1600x900': {
		'window-width': 1600,
		'window-height': 900,
	},
	'1920x1080': {
		'window-width': 1920,
		'window-height': 1080,
	},
	'2560x1440': {
		'window-width': 2560,
		'window-height': 1440,
	},
}

SELECTED_RESOLUTION = RESOLUTIONS['1366x768']

WINDOW_WIDTH = SELECTED_RESOLUTION['window-width']
WINDOW_HEIGHT = SELECTED_RESOLUTION['window-height']
NUM_PIXELS = WINDOW_WIDTH * WINDOW_HEIGHT

SCOREBOARD_WIDTH = WINDOW_WIDTH // 4

GAME_WINDOW_WIDTH = WINDOW_WIDTH - SCOREBOARD_WIDTH
GAME_WINDOW_HEIGHT = WINDOW_HEIGHT

PADDLE_WIDTH = GAME_WINDOW_WIDTH // 3
PADDLE_HEIGHT = WINDOW_HEIGHT // 40

HEART_WIDTH = WINDOW_WIDTH // 30
HEART_HEIGHT = WINDOW_HEIGHT // 20

FPS = 60

# Speeds of objects
DEFAULT_PADDLE_SPEED = 800
DEFAULT_BALL_SPEED = 300
DEFAULT_POWERUP_SPEED = 600

# Levels
BLOCK_MAP = [
	'            ',
	'111111111111',
	'111111111111',
	'111111111111',
	'111111111111',
	'111111111111',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            '
]

COLOR_LEGEND = {
	1: './assets/images/blocks/1.png',
	2: './assets/images/blocks/2.png',
	3: './assets/images/blocks/3.png',
	4: './assets/images/blocks/4.png',
	5: './assets/images/blocks/5.png',
	6: './assets/images/blocks/6.png',
	7: './assets/images/blocks/7.png'
}

BALL_SPEED_DURATION = 10
BALL_SIZE_DURATION = 15
BALL_STRENGTH_DURATION = 20
PADDLE_SIZE_DURATION = 15

# Powers tuple(name, probability)
POWERS = {
	'add-life': {
		'probability': 0.1,
		'path': './assets/images/powerups/add-life.png',
		'time': -1
	},
	'big-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/big-ball.png',
		'time': BALL_SIZE_DURATION
	},
	'small-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/small-ball.png',
		'time': BALL_SIZE_DURATION
	},
	'fast-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/fast-ball.png',
		'time': BALL_SPEED_DURATION
	},
	'slow-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/slow-ball.png',
		'time': BALL_SPEED_DURATION
	},
	'multiply-balls': {
		'probability': 0.1,
		'path': './assets/images/powerups/multiply-balls.png',
		'time': -1
	},
	'super-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/super-ball.png',
		'time': BALL_STRENGTH_DURATION
	},
	'big-paddle': {
		'probability': 0.1,
		'path': './assets/images/powerups/big-paddle.png',
		'time': PADDLE_SIZE_DURATION
	},
	'small-paddle': {
		'probability': 0.1,
		'path': './assets/images/powerups/small-paddle.png',
		'time': PADDLE_SIZE_DURATION
	},
}

GAP_SIZE = 2
BLOCK_HEIGHT = GAME_WINDOW_HEIGHT // len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = GAME_WINDOW_WIDTH // len(BLOCK_MAP[0]) - GAP_SIZE

MAX_PLAYER_HEALTH = 3
