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

# COLOR_LEGEND = {
# 	'1': 'blue',
# 	'2': 'green',
# 	'3': 'red',
# 	'4': 'orange',
# 	'5': 'purple',
# 	'6': 'bronze',
# 	'7': 'grey',
# }

COLOR_LEGEND = {
	1: (255, 255, 255),
	2: (212, 212, 212),
	3: (169, 169, 169),
	4: (126, 126, 126),
	5: (83, 83, 83),
	6: (40, 40, 40),
	7: (0, 0, 0)
}

GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = GAME_WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE

FPS = 120
DIRECTION_CHANGE = 20
