import logging

class RouteLoader(object):
    @staticmethod
    def load(package_name):
        import pkgutil
        import sys
        from zcr.core.log import Log
        from zcr.view.decorators import Route
        package = __import__(package_name)
        controllers_module = sys.modules[package_name]
        prefix = controllers_module.__name__ + '.'

        for importer, modname, ispkg in pkgutil.iter_modules(controllers_module.__path__, prefix):
            module = __import__(modname)
        url_routes = Route.get_routes()
        Log.log_show_store(f"路由: {url_routes}", logging.INFO)
        return url_routes
