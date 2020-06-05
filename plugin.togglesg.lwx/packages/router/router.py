class Router(object):
    def __init__(self):
        pass

    def setRoutes(self, routes):
        ''' routes:dict '''
        self.routes = routes

    def route(self, routeKey):
        try:
            print('[Routing to -->', routeKey, ']')
            self.routes[routeKey]()
        except KeyError:
            print('[Router] Invalid routeKey -->', routeKey)
