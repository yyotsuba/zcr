import os
import sys

import tornado
import tornado.httpserver
import tornado.web
from zcr.config.settings import settings


class ZCRServer(object):
    def __init__(self, port):
        self.application = None
        self.logger = None
        self.port = port

    def init_logging(self):
        import logging
        from zcr.core.log import Log
        Log.create(settings.LOG_CONF)

    def load_routes(self):
        from zcr.core.routes import RouteLoader
        return RouteLoader.load("zcr.controllers")

    def run(self):
        # init logger
        self.init_logging()

        # init url routes
        url_routes = self.load_routes()

        config = settings.TORNADO_CONF

        # setup the controller action routes
        self.application = tornado.web.Application(url_routes,
                                                           **config)
        # instantiate a server instance
        http_server = tornado.httpserver.HTTPServer(self.application)

        # bind sever to port
        http_server.listen(self.port)

        # start the server
        tornado.ioloop.IOLoop.instance().start()

