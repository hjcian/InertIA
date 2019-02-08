import os
import sys
import traceback
from functools import partial
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QTextBrowser
STANDARD_H = 600
STANDARD_W = 800

class AboutTab(QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowGeometry()
        self.setUI()

    def setWindowGeometry(self):
        self.left = 10
        self.top = 10
        self.width = STANDARD_W
        self.height = STANDARD_H
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setUI(self):
        self.setWindowTitle("About")
        self.append("Author: Hong-Jhou (Max) Cian")
        self.append("License: GNU General Public License v3.0")
        self.append("Homepage: {}".format(self._genHref("GitHub Repository", "https://github.com/hjcian/InertIA")))
        self.append("Contact: please use {} to leave suggestions and bug reports.".format(self._genHref('Issues', "https://github.com/hjcian/InertIA/issues")))
        self.setOpenExternalLinks(True)
        
    def _genHref(self, text, url):
        return '<a href="{1}">{0}</a>'.format(text, url)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = AboutTab()
    mw.show()
    sys.exit(app.exec_())