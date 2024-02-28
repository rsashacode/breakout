WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

BLOCK_MAP = [
	'666666666666',
	'444557755444',
	'333333333333',
	'222222222222',
	'111111111111',
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

GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = (WINDOW_WIDTH - 160) / len(BLOCK_MAP[0]) - GAP_SIZE

COLOR_LEGEND = {
	1: (212, 212, 212),
	2: (169, 169, 169),
	3: (169, 169, 169),
	4: (126, 126, 126),
	5: (83, 83, 83),
	6: (40, 40, 40),
	7: (0, 0, 0)
}

DEFAULT_PADDLE_SPEED = 600
