import inspect
import logging
import multiprocessing
import os
import sys
import time

STD_LEVEL = logging.DEBUG

class Log(object):
	instance = None
	handlers = {logging.DEBUG: None, logging.INFO: None, logging.WARNING: None, logging.ERROR: None}
	dates = {logging.DEBUG: None, logging.INFO: None, logging.WARNING: None,
			 logging.ERROR: None}
	def __init__(self, log_conf):
		self.logger = logging.RootLogger(logging.DEBUG)
		self.format = logging.Formatter(log_conf.log_format)
		self.log_path = log_conf.log_path
		
		self.stdouthandler = logging.StreamHandler(sys.stdout)
		self.stdouthandler.setLevel(STD_LEVEL)
		self.stdouthandler.setFormatter(self.format)

		self.__lock = multiprocessing.Lock()

	@staticmethod
	def create(log_conf):
		Log.instance = Log(log_conf)

	def add_handler(self, level):
		level_name = logging._levelToName[level]
		file_name = time.strftime('%Y-%m-%d', time.localtime(time.time()))
		dir = self.log_path + os.sep + level_name.lower()

		path = dir + os.sep + file_name + '.log'
		if not os.path.exists(dir):
			os.makedirs(dir)
		if file_name != self.dates[level]:
			if self.dates[level] is not None:
				self.logger.removeHandler(self.handlers[level])
			handler = logging.FileHandler(path, encoding='UTF-8', mode='a')
			handler.setLevel(level)
			handler.setFormatter(self.format)
			self.handlers[level] = handler
			self.dates[level] = file_name
			self.logger.addHandler(handler)

	def __log(self, msg, level): 
		if level == logging.DEBUG:
			self.logger.debug(msg)
		elif level == logging.INFO:
			self.logger.info(msg)
		elif level == logging.WARNING:
			self.logging.warning(msg)
		elif level == logging.ERROR:
			self.logging.error(msg)

	@staticmethod
	def log_show_store(msg, level):
		msg = os.path.basename(inspect.stack()[1][1]) + ' - ' + \
        inspect.stack()[1][3] + ' - ' + str(inspect.stack()[1][2]) + ' - ' + msg
		self = Log.instance
		self.__lock.acquire()
		self.logger.addHandler(self.stdouthandler)
		self.add_handler(level)
		self.__log(msg, level)
		self.logger.removeHandler(self.stdouthandler)
		self.__lock.release()




