import os
import sys

import zcr
from .cli import CLI

class Main(object):
    def __init__(self, cli, options, args):
        self.cli = cli
        self.options = options
        self.args = args

    def start(self):
        options = self.options
        # set path
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from zcr.core.webserver import ZCRServer
        server = ZCRServer(
            port=options.port
        )
        server.run()

    def print_version(self):
        msg = f'zcr v{zcr.__version__}'
        self.cli.print_msg(msg)

    def upgradedb(self):
        from alembic.config import main
        main('upgrade head'.split(' '), 'alembic')
