import sys

from optparse import OptionParser

class CLI(object):
	def __init__(self):
		self.__config_parse()

	def __config_parse(self):
		self.__parser = OptionParser(usage="usage: %prog [options]")

		self.__parser.add_option("-p", "--port",
						   dest="port",
						   default=8001,
						   type=int,
						   help="Use a specific port number (default is 8001).")

		self.__parser.add_option("-v", "--version",
						   action="store_true",
						   dest="print_version",
						   default=False,
						   help="Displays zrc vesion and exit.")
		self.__parser.add_option("-u", "--upgradedb",
						   action='store_true',
						   dest="upgradedb",
						   default=False,
						   help="Update Table Structure")

	def parse(self):
		return self.__parser.parse_args()

	def print_msg(self, msg, out=None):
		if not out:
			out = sys.stdout
		out.write(f"{msg}\n")
