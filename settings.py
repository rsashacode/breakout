WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

SCOREBOARD_WIDTH = 160

GAME_WINDOW_WIDTH = WINDOW_WIDTH - SCOREBOARD_WIDTH
GAME_WINDOW_HEIGHT = WINDOW_HEIGHT

PADDLE_WIDTH = GAME_WINDOW_WIDTH // 5
PADDLE_HEIGHT = WINDOW_HEIGHT // 40

DEFAULT_PADDLE_SPEED = 1000
DEFAULT_BALL_SPEED = 300
DEFAULT_POWERUP_SPEED = 4

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
 	'            '
    ]

COLOR_LEGEND = {
	1: './assets/blocks/1.png',
	2: './assets/blocks/2.png',
	3: './assets/blocks/3.png',
	4: './assets/blocks/4.png',
	5: './assets/blocks/5.png',
	6: './assets/blocks/6.png',
	7: './assets/blocks/7.png'
}

POWER_UP_IMAGES = [
	'./assets/other/heart.png',
	'./assets/other/laser.png',
	'./assets/other/size.png',
	'./assets/other/speed.png'
]

GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = GAME_WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE

FPS = 60
DIRECTION_CHANGE = 20

MAX_PLAYER_HEALTH = 3
