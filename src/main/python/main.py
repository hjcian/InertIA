import os
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QTabWidget
from PyQt5.QtGui import QValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea
from tabs import (annualized_return_calculator, 
                  import_tab,
                  about,
                 )
STANDARD_H = 600
STANDARD_W = 800

class MainWindow(QTabWidget):
    def __init__(self, *argv, **kwargv):
        super().__init__(*argv, **kwargv)
        self.setWindowGeometry()
        self.setUI()

    def setWindowGeometry(self):
        self.left = 10
        self.top = 10
        self.width = STANDARD_W
        self.height = STANDARD_H
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setUI(self):
        self.setWindowTitle("InertIA - Inert Investment Assistant")
        self.import_tab = import_tab.ImportTab()
        self.annualized_return_calculator_tab = annualized_return_calculator.AnnualizedReturnCalculator()
        self.about_tab = about.AboutTab()

        self.addTab(self.import_tab, "Import Data")
        self.addTab(self.annualized_return_calculator_tab, "Calculate Annualized Return")
        self.addTab(self.about_tab, "About")
        self.setCurrentIndex(0)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Macintosh')
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())