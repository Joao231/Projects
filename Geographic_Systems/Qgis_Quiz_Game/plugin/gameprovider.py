import os
import inspect
from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingProvider
from .capitals_game_algoritm import GameAlgorithm


class GameProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def unload(self):
        pass

    def loadAlgorithms(self):
        self.addAlgorithm(GameAlgorithm())

    def id(self):
        return 'Capitals Game'

    def name(self):
        return self.tr('Capitals Game')

    def icon(self):
        cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
        icon = QIcon(os.path.join(os.path.join(cmd_folder, 'globe-icon.png')))
        return icon

    def longName(self):
        return self.name()