# source from: https://pythonspot.com/pyqt5-file-dialog/
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog

class FileHandler(QWidget):    
    def __init__(self, title='QFileDialog', *argv, **kwargv):
        super(self.__class__, self).__init__(*argv, **kwargv)
        self.title = title

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, self.title, "","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            # print(fileName)
            return fileName
        return ""

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;CSV Files (*.csv)", options=options)
        if files:
            # print(files)
            return files
        return ""
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;CSV Files (*.csv)", options=options)
        if fileName:
            # print(fileName)
            return fileName
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fp = FileHandler(title='test open')
    fp.openFileNameDialog()
    fp.show()
    fp.deleteLater()
    sys.exit(app.exec_())