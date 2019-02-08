import os
import sys
import traceback
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QTextBrowser
from PyQt5.QtGui import QValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout
from gui_util.file_handler import FileHandler
TABS_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.dirname(TABS_DIR)
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, 'util'))
sys.path.append(os.path.join(SRC_DIR, 'database'))
from util import util
from database.ft_db import get_firstrade_db
PROJECT_DIR = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
CONFIG = util.loadConfig(os.path.join(DATA_DIR, 'config.json'))
FTDB = get_firstrade_db(db_fpath=os.path.join(DATA_DIR, CONFIG['database']))

STANDARD_H = 600
STANDARD_W = 800

class ImportTab(QWidget):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.left = 10
        self.top = 10
        self.width = STANDARD_W
        self.height = STANDARD_H
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setUI()

    def setUI(self):
        self.setWindowTitle('Import Data')
        self.vbox_layout = QVBoxLayout()

        self.firstrade_CSV_import_btn = QPushButton("Import Firstrade standard account CSV file")
        self.text_browser = QTextBrowser()

        self.vbox_layout.addWidget(self.firstrade_CSV_import_btn)
        self.vbox_layout.addWidget(self.text_browser)

        self.setLayout(self.vbox_layout) # finally

        self.firstrade_CSV_import_btn.clicked.connect(partial(self._import_data, title="Import Firstrade standard account history CSV file"))

    def _import_data(self, title):
        self.text_browser.clear()
        filepath = self._file_selector(title)
        self.text_browser.append("Ready to import data, source from '{}'".format(filepath))
        try:
            success_count = FTDB.importFTStandardCSV(filepath, self.text_browser)
            self.text_browser.append("Successful importing: {}".format(success_count))
            self.text_browser.append("Import done.".format())
        except (TypeError, FileNotFoundError) as err:
            self.text_browser.append("Invalid filepath (given: '{}'), please select again. (error msg: {})".format(filepath, err))
        except Exception as err:
            self.text_browser.append("Import Error: {}".format(err))
            self.text_browser.append("{}".format(traceback.format_exc()))
        
    def _file_selector(self, title):
        fp = FileHandler(title)
        filepath = fp.openFileNameDialog()
        fp.show()
        fp.deleteLater()
        return filepath

if __name__ == "__main__":
    app = QApplication(sys.argv)
    import_tab = ImportTab()
    import_tab.show()
    sys.exit(app.exec_())
