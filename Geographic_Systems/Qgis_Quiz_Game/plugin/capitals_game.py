import os
import sys
import os
import sys
import inspect
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from qgis.core import QgsProcessingAlgorithm, QgsApplication
import processing
from .gameprovider import GameProvider


cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class GamePlugin:
    def __init__(self, iface):
        self.iface = iface

    def initProcessing(self):
      self.provider = GameProvider()
      QgsApplication.processingRegistry().addProvider(self.provider)
        
    def initGui(self):
      self.initProcessing()
      icon = os.path.join(os.path.join(cmd_folder, 'globe-icon.png'))
      self.action = QAction(QIcon(icon), 'Play Capitals game', self.iface.mainWindow())
      self.action.triggered.connect(self.run)
      self.iface.addPluginToMenu('&GeoQuigiz', self.action)
      self.iface.addToolBarIcon(self.action)

    def unload(self):
      QgsApplication.processingRegistry().removeProvider(self.provider)
      self.iface.removeToolBarIcon(self.action)
      self.iface.removePluginMenu('&GeoQuigiz', self.action)  
      del self.action

    def run(self):
      processing.execAlgorithmDialog('Ready to play capitals game!')

