"""
Logging configuration
"""
import logging
import logging.config

from logging import LogRecord

from utils.path_utils import base_path


logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True})
_log_file_path = base_path.joinpath('log', 'breakout_game.log')


class _FileHandler(logging.Handler):
    """
    Log to file handler
    """
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record: LogRecord):
        """
        Emit log to file

        Args:
            record (LogRecord): message to log
        """
        message = self.format(record)
        with open(_log_file_path, 'a', encoding='utf-8') as file:
            file.write(message + '\n')


_logger_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'stream_formatter': {
            'format': '{asctime:23} | {levelname:7} | {name:12} | '
                      '{module:15}: {funcName:20} | line:{lineno:4} | {message}',
            'style': '{',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'bold_white',
                'WARNING': 'bold_yellow',
                'ERROR': 'bold_red',
                'CRITICAL': 'bold_red,bg_white'
            },
        },
        'file_formatter': {
            'format': '{asctime} | {levelname} | {name} | {module}:{funcName} line:{lineno} | {message}',
            'style': '{'
        },
    },
    'handlers': {
        'file_handler': {
            '()': _FileHandler,
            'level': 'DEBUG',
            'formatter': 'file_formatter'
        },
        'stream_handler': {
            '()': logging.StreamHandler,
            'level': 'DEBUG',
            'formatter': 'stream_formatter'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}

logging.config.dictConfig(_logger_config)

game_logger = logging.getLogger('')
game_logger.info('Game logger configured')
