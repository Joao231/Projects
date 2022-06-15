from PyQt5.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFileDestination)


class GameAlgorithm(QgsProcessingAlgorithm):
    """Saves the attributes of a vector layer to a CSV file."""
    OUTPUT = 'OUTPUT'
    INPUT = 'INPUT'

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT,
                self.tr('Capitals Game'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

       

    def processAlgorithm(self, parameters, context, feedback):
        source = self.parameterAsSource(parameters, self.INPUT, context)
        
        layer = iface.activeLayer()

        

        

        

        return {self.OUTPUT: csv}

    def name(self):
        return 'Capitals Game'

    def displayName(self):
        return self.tr('Capitals Game')

    def group(self):
        return self.tr(self.groupId())

    def groupId(self):
        return ''

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return GameAlgorithm()