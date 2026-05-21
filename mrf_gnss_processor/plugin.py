from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from .ui.main_dock import MRFProcessorDock


class MrfGnssProcessorPlugin:
    """QGIS plugin entrypoint."""

    def __init__(self, iface):
        self.iface = iface
        self.action = None
        self.dock = None

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/mrf_gnss_processor/icon.svg"), "MRF GNSS Processor", self.iface.mainWindow())
        self.action.triggered.connect(self.show_dock)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&MRF GNSS Processor", self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu("&MRF GNSS Processor", self.action)
            self.iface.removeToolBarIcon(self.action)
        if self.dock:
            self.iface.removeDockWidget(self.dock)
            self.dock = None

    def show_dock(self):
        if self.dock is None:
            self.dock = MRFProcessorDock(self.iface)
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock)
        self.dock.show()
        self.dock.raise_()
