from .capitals_game import GamePlugin

def classFactory(iface):
    return GamePlugin(iface)


