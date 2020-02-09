import logging


class Logger_settings:
	logger_name = 'aro'
	logger_path = 'C:/Users/aro/InstaPy/logs/light/general.log'


def get_logger():
	# print(logger_name)
	logger = logging.getLogger(Logger_settings.logger_name)
	logger_name = {"username": 'arasssu'}

	logger_formatter = logging.Formatter(
		'%(levelname)s [%(asctime)s] [%(username)s]  %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S')

	file_handler = logging.FileHandler(Logger_settings.logger_path)
	file_handler.setFormatter(logger_formatter)
	# file_handler.setLevel(logging.DEBUG)
	logger.addHandler(file_handler)

	console_handler = logging.StreamHandler()
	console_handler.setFormatter(logger_formatter)
	logger.addHandler(console_handler)
	logger = logging.LoggerAdapter(logger, logger_name)

	logger.setLevel(logging.DEBUG)


	return logger



