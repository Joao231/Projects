from .capitals_game import CapitalsGamePlugin

def classFactory(iface):
    return CapitalsGamePlugin(iface)


