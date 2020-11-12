# Imports =============================================================

# Standard Libraries
import sys
import logging
from logging.handlers import RotatingFileHandler

# Third-party Libraries
from PyQt5 import uic, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

# Local Application Libraries
from gui.ui_utils import find_form
from common import actions
from common.status_logger import QTextEditLogger

# =====================================================================

print('passed')

class PricePalMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(PricePalMainWindow, self).__init__()

        # Load the main window GUI file
        uic.loadUi(find_form('pricepal_mainform.ui'),self)

        # Add the custom matplotlib widget to the defined groupbox
        self.plotwindow = MplWidget(self.groupBox_Graph)

        # Add the status logging textbox to the statusbar
        logging.getLogger().setLevel(logging.DEBUG)
        self.logStatusBox = QTextEditLogger(self.statusbar)
        self.logStatusBox.setFormatter(
            logging.Formatter(
                '%(asctime)s | %(levelname)s | %(module)s | %(message)s'
            )
        )
        logging.getLogger().addHandler(self.logStatusBox)

        # Add a rolling log file for storing more verbose logs
        # Will create a new file when near to the specified maximum, keeping up to backupCount number of copies
        self.logFile = RotatingFileHandler('data/logs/pricepal-log.log', maxBytes=100000, backupCount=9)
        self.logFile.setFormatter(
            logging.Formatter(
                '%(asctime)s | %(levelname)s | Module: %(module)s | Function: %(funcName)s | %(message)s'
            )
        )
        logging.getLogger().addHandler(self.logFile)

        logging.info('')
        logging.info('Start to application session.')

        # Show the GUI window
        self.show()

        logging.info('Application main window launched.')

class MplWidget(QtWidgets.QWidget):
    def __init__(self, group_box: QtWidgets.QGroupBox, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        vertical_layout = QtWidgets.QVBoxLayout()
        vertical_layout.alignment
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas,self))

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.figure.tight_layout()
        self.canvas.tight_layout = True
        group_box.setLayout(vertical_layout)


def main():
    autograph_app = QtWidgets.QApplication(sys.argv)
    mainWindow = PricePalMainWindow()
    autograph_app.exec_()


if __name__ == '__main__':
    main()