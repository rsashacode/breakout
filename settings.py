# GRAPHICS

RESOLUTIONS = {
	'800x600': {
		'window-width': 800,
		'window-height': 600,
		'menu-font-size': 20,
		'score-font-size': 16,
		'powerup-font-size': 8
	},
	'1280x720': {
		'window-width': 1280,
		'window-height': 720,
		'menu-font-size': 30,
		'score-font-size': 26,
		'powerup-font-size': 12
	},
	'1366x768': {
		'window-width': 1366,
		'window-height': 768,
		'menu-font-size': 34,
		'score-font-size': 30,
		'powerup-font-size': 13
	},
	'1600x900': {
		'window-width': 1600,
		'window-height': 900,
		'menu-font-size': 40,
		'score-font-size': 34,
		'powerup-font-size': 16
	},
	'1920x1080': {
		'window-width': 1920,
		'window-height': 1080,
		'menu-font-size': 50,
		'score-font-size': 46,
		'powerup-font-size': 20
	},
	'2560x1440': {
		'window-width': 2560,
		'window-height': 1440,
		'menu-font-size': 60,
		'score-font-size': 50,
		'powerup-font-size': 24
	},
}

SELECTED_RESOLUTION = RESOLUTIONS['1600x900']

WINDOW_WIDTH = SELECTED_RESOLUTION['window-width']
WINDOW_HEIGHT = SELECTED_RESOLUTION['window-height']
NUM_PIXELS = WINDOW_WIDTH * WINDOW_HEIGHT

GAME_FONT = './assets/fonts/joystix monospace.otf'
MENU_FONT_SIZE = SELECTED_RESOLUTION['menu-font-size']
SCORE_FONT_SIZE = SELECTED_RESOLUTION['score-font-size']
POWERUP_FONT_SIZE = SELECTED_RESOLUTION['powerup-font-size']

SCOREBOARD_WIDTH = WINDOW_WIDTH // 4
GAME_WINDOW_WIDTH = WINDOW_WIDTH - SCOREBOARD_WIDTH
GAME_WINDOW_HEIGHT = WINDOW_HEIGHT
PADDLE_WIDTH = GAME_WINDOW_WIDTH // 2.5
PADDLE_HEIGHT = WINDOW_HEIGHT // 40
HEART_WIDTH = WINDOW_WIDTH // 30
HEART_HEIGHT = WINDOW_HEIGHT // 20

FPS = 60


# SPEEDS
DEFAULT_PADDLE_SPEED_BASE = 800
DEFAULT_BALL_SPEED_PER_BASE = 400
DEFAULT_POWERUP_SPEED_PER_BASE = 600
SPEED_COEFFICIENT = (WINDOW_WIDTH / 1366 + WINDOW_HEIGHT / 768) / 2

DEFAULT_PADDLE_SPEED = DEFAULT_PADDLE_SPEED_BASE * SPEED_COEFFICIENT
DEFAULT_BALL_SPEED = DEFAULT_BALL_SPEED_PER_BASE * SPEED_COEFFICIENT
DEFAULT_POWERUP_SPEED = DEFAULT_POWERUP_SPEED_PER_BASE * SPEED_COEFFICIENT


# BLOCKS
BLOCK_MAP = [
	'          ',
	# '1111111111',
	# '1111111111',
	# '1111111111',
	# '1111111111',
	'1111111111',
	'          ',
	'          ',
	'          ',
	'          ',
	'          ',
	'          ',
	'          '
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

GAP_SIZE = 10
BLOCK_HEIGHT = GAME_WINDOW_HEIGHT // len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = GAME_WINDOW_WIDTH // len(BLOCK_MAP[0]) - GAP_SIZE


# POWERUPS
BALL_SPEED_DURATION = 10
BALL_SIZE_DURATION = 15
BALL_STRENGTH_DURATION = 20
PADDLE_SIZE_DURATION = 15

POWERS = {
	'add-life': {
		'probability': 0.1,
		'path': './assets/images/powerups/add-life.png',
		'time': -1,
		'conflicting-power': None
	},
	'big-ball': {
		'probability': 1,
		'path': './assets/images/powerups/big-ball.png',
		'time': BALL_SIZE_DURATION,
		'conflicting-power': 'small-ball'
	},
	'small-ball': {
		'probability': 1,
		'path': './assets/images/powerups/small-ball.png',
		'time': BALL_SIZE_DURATION,
		'conflicting-power': 'big-ball'
	},
	'fast-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/fast-ball.png',
		'time': BALL_SPEED_DURATION,
		'conflicting-power': 'slow-ball'
	},
	'slow-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/slow-ball.png',
		'time': BALL_SPEED_DURATION,
		'conflicting-power': 'fast-ball'
	},
	'multiply-balls': {
		'probability': 0.1,
		'path': './assets/images/powerups/multiply-balls.png',
		'time': -1,
		'conflicting-power': None
	},
	'super-ball': {
		'probability': 0.1,
		'path': './assets/images/powerups/super-ball.png',
		'time': BALL_STRENGTH_DURATION,
		'conflicting-power': None
	},
	'big-paddle': {
		'probability': 0.1,
		'path': './assets/images/powerups/big-paddle.png',
		'time': PADDLE_SIZE_DURATION,
		'conflicting-power': 'small-paddle'
	},
	'small-paddle': {
		'probability': 0.1,
		'path': './assets/images/powerups/small-paddle.png',
		'time': PADDLE_SIZE_DURATION,
		'conflicting-power': 'big-paddle'
	},
}

# HEALTH
MAX_PLAYER_HEALTH = 3
