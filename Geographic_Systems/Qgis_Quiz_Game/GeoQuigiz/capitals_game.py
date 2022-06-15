import os
import sys
import inspect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog
from qgis.core import QgsProject, Qgis, QgsMapLayer
from .capitals_game_dialog import CapitalsGameDialog

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

class CapitalsGamePlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
      icon = os.path.join(os.path.join(cmd_folder, 'globe-icon.png'))
      self.action = QAction(QIcon(icon), 'Capitals Game', self.iface.mainWindow())
      self.action.triggered.connect(self.run)
      self.iface.addPluginToMenu('&Capitals Game', self.action)
      self.iface.addToolBarIcon(self.action)
      self.first_start = True

    def unload(self):
      self.iface.removeToolBarIcon(self.action)
      self.iface.removePluginMenu('&Capitals Game', self.action)  
      del self.action

    def select_output_file(self):
      filename, _filter = QFileDialog.getSaveFileName(
        self.dlg, "Select   output file ","", '*.csv')
      self.dlg.lineEdit.setText(filename)
      
    def run(self):
      if self.first_start == True:
        self.first_start = False
        self.dlg = CapitalsGameDialog()
        self.dlg.pushButton.clicked.connect(self.select_output_file)

        
      layers = QgsProject.instance().mapLayers().values()
      vectorlayers = [layer for layer in layers if layer.type() == QgsMapLayer.VectorLayer]
      self.dlg.comboBox.clear()
      self.dlg.lineEdit.clear()
      self.dlg.comboBox.addItems([layer.name() for layer in vectorlayers])
      self.dlg.show()
      # Run the dialog event loop
      result = self.dlg.exec_()
      # See if OK was pressed
      if result:
        filename = self.dlg.lineEdit.text()
        with open(filename, 'w') as output_file:
          selectedLayerName = self.dlg.comboBox.currentText()
          selectedLayer = QgsProject.instance().mapLayersByName(selectedLayerName)[0]
          fieldnames = [field.name() for field in selectedLayer.fields()]
          # write header
          line = ','.join(name for name in fieldnames) + '\n'
          output_file.write(line)
          # wirte feature attributes
          for f in selectedLayer.getFeatures():
            line = ','.join(str(f[name]) for name in fieldnames) + '\n'
            output_file.write(line)
        self.iface.messageBar().pushMessage(
          'Success', 'Output file written at ' + filename, level=Qgis.Success)

