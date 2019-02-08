from PyQt5.QtWidgets import QMessageBox

class PopWarning(QMessageBox):
    def __init__(self, msg, detail=None, *argv, **kwargv):
        super(self.__class__, self).__init__(*argv, **kwargv)
        self._setMsgs(msg, detail)

    def _setMsgs(self, msg, detail):
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Warning")
        # self.setInformativeText(msg)
        self.setText(msg)
        if detail:
            self.setDetailedText(detail)
        self.setStandardButtons(QMessageBox.Ok)