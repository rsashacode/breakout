import logging
import logging.config

from breakout.utils.path_utils import base_path
from logging import LogRecord

logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})
_log_file_path = base_path.joinpath('log', 'breakout.log')


class _FileHandler(logging.Handler):
	"""
	Log to file handler
	"""
	def __init__(self):
		logging.Handler.__init__(self)

	def emit(self, record: LogRecord) -> None:
		"""
		Emit log to file

		:param record: record of logger instance
		:return:
		"""
		message = self.format(record)
		with open(_log_file_path, 'a') as file:
			file.write(message + '\n')


_logger_config = dict(
	version=1,
	disable_existing_loggers=False,
	formatters=dict(
		stream_formatter={
			'format': '{asctime:23} | {levelname:7} | {name:12} | '
					  '{module:15}: {funcName:20} | line:{lineno:4} | {message}',
			'style': '{',
			'log_colors': dict(
				DEBUG='cyan',
				INFO='bold_white',
				WARNING='bold_yellow',
				ERROR='bold_red',
				CRITICAL='bold_red,bg_white'),
		},
		file_formatter={
			'format': '{asctime} | {levelname} | {name} | {module}:{funcName} line:{lineno} | {message}',
			'style': '{'
		},
	),
	handlers=dict(
		file_handler={
			'()': _FileHandler,
			'level': 'DEBUG',
			'formatter': 'file_formatter'
		},
		stream_handler={
			'()': logging.StreamHandler,
			'level': 'DEBUG',
			'formatter': 'stream_formatter'
		}
	),
	loggers={
		'': {
			'level': 'DEBUG',
			'handlers': ['file_handler', 'stream_handler']
		}
	}
)

logging.config.dictConfig(_logger_config)

game_logger = logging.getLogger('')
game_logger.info('Game logger configured')
