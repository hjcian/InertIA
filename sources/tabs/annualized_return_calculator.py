import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
from PyQt5.QtGui import QValidator, QDoubleValidator
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QTextBrowser
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractScrollArea
TABS_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.dirname(TABS_DIR)
sys.path.append(TABS_DIR)
sys.path.append(SRC_DIR)
sys.path.append(os.path.join(SRC_DIR, 'financial'))
from gui_util.pop_message import PopWarning
from financial import financial_func

PriceValidator = QDoubleValidator()
PriceValidator.setRange(0.000000, 9999.000000, 6)
PriceValidator.setNotation(QDoubleValidator.StandardNotation)

class PriceLineEdit(QLineEdit):
    '''
    inspired by : https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/
    '''
    def __init__(self, *argv, **kwargv):
        super(self.__class__, self).__init__(*argv, **kwargv)
        self.setValidator(PriceValidator)
        self.textChanged.connect(self._check_state)
        self.textChanged.emit(self.text())

    def _check_state(self):        
        validator = self.validator()
        if validator:
            state = validator.validate(self.text(), 0)[0]
            if state == QValidator.Acceptable:
                color = '#c4df9b' # green
            elif state == QValidator.Intermediate:
                color = '#f6989d' # red
            else:
                color = '#fff79a' # yellow
            self.setStyleSheet('QLineEdit { background-color: %s }' % color)

    def isTextValid(self):
        validator = self.validator()
        if validator:
            state = validator.validate(self.text(), 0)[0]
            if state == QValidator.Acceptable:
                return True
            else:
                return False
        return True

class AnnualizedReturnCalculator(QWidget):
    def __init__(self, parent = None):
        super(self.__class__, self).__init__(parent)
        self.uuid = 0
        self.setUI()

    @property
    def _getNextUUID(self):
        self.uuid += 1
        return self.uuid

    def setFocus(self):
        for uuid in self.symbolPriceRow:
            symbol, price, action = self.symbolPriceRow[uuid]
            if action is None:
                symbol.setFocus()
                break

    def setUI(self):
        # initialization
        self.setWindowTitle("Annualized Return Calculator")
        
        line_symbol = QLineEdit()
        line_symbol.setFocus()        
        line_symbol.setPlaceholderText('e.g. VT')
        line_price = PriceLineEdit()
        line_price.setPlaceholderText('e.g. 71.06')
    
        self.symbolPriceRow = { self._getNextUUID: (line_symbol, line_price, None) }        
        self.addRow = QPushButton("&Add Symbol")
        self.calculate = QPushButton("&Calculate")
        self.clear = QPushButton("&Clear form")

        # layouts
        self.table_layout = QVBoxLayout()
        # self.text_result_browser = QTextBrowser()

        self.form_layout = QFormLayout()
        self.form_layout.addRow(QLabel("Symbol"), QLabel("Price"))
        self.form_layout.addRow(line_symbol, line_price) 
        self.action_layout = QFormLayout()
        self.action_layout.addRow(QLabel("Action"))
        blank_btn = QPushButton("")
        blank_btn.setFlat(True)
        self.action_layout.addRow(blank_btn)
        hbox_layout = QHBoxLayout()
        hbox_layout.addLayout(self.form_layout)
        hbox_layout.addLayout(self.action_layout)

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addLayout(self.table_layout)
        # self.vbox_layout.addWidget(self.text_result_browser)
        self.vbox_layout.addLayout(hbox_layout)
        self.vbox_layout.addWidget(self.addRow)
        self.vbox_layout.addWidget(self.calculate)
        self.vbox_layout.addWidget(self.clear)
        self.setLayout(self.vbox_layout) # finally

        # add signal and slot
        self.clear.clicked.connect(self._clearAllLine)
        self.calculate.clicked.connect(self._calcAndGenTable)
        self.addRow.clicked.connect(self._addNewSymbolPriceRow)

    def _clearAllLine(self):
        for uuid in self.symbolPriceRow:
            symbol, price, action = self.symbolPriceRow[uuid]
            symbol.clear()
            price.clear()
            
    def _addNewSymbolPriceRow(self):
        line_symbol = QLineEdit()
        line_price = PriceLineEdit()
        delete_line = QPushButton("&Del")
        self.form_layout.addRow(line_symbol, line_price, )
        self.action_layout.addRow(delete_line)
        _uuid = self._getNextUUID
        self.symbolPriceRow.update({
            _uuid: (line_symbol, line_price, delete_line)
        })
        def _delete_line(uuid):
            def _del():
                symbol, price, action = self.symbolPriceRow.pop(uuid)
                symbol.deleteLater()
                price.deleteLater()
                action.deleteLater()
            return _del
        delete_line.clicked.connect(_delete_line(_uuid))
    
    def _check_symbol_price(self, symbol, price):
        symbol_text = symbol.text()        
        if not symbol_text:
            raise ValueError('Found blank symbol, please fill it.')
        if len(symbol_text) > 128:
            raise ValueError('Is it possible that number of characters of stock ticker symbol would larger than 128?')
        if not price.text():
            raise ValueError('Found blank price, please fill it.')
        if not price.isTextValid():
            raise ValueError('Found invalid number of price ({})'.format(price.text()))

    def _calcAndGenTable(self):
        symbol_to_price = dict()
        try:
            for uuid in self.symbolPriceRow:
                symbol, price, action = self.symbolPriceRow[uuid]
                self._check_symbol_price(symbol, price)
                if symbol_to_price.get(symbol.text()):
                    raise KeyError('Symbol "{}" occurs twice! Please check your input again.'.format(symbol.text()))
                symbol_to_price.update({ symbol.text().strip().lower(): float(price.text())})
        except Exception as err:
            pop = PopWarning(msg=str(err))
            pop.exec_()
            print(err)
        else:
            ar = financial_func.calcMultiAnnualizedReturn(symbol_to_price)
            table = QTableWidget(2, 2)
            
            label = QTableWidgetItem("Annualized Return (%)")
            portfolio = QTableWidgetItem("Portfolio")
            portfolio_return = QTableWidgetItem("{:.2f}".format(ar * 100))
            table.setItem(0, 1, label)
            table.setItem(1, 0, portfolio)
            table.setItem(1, 1, portfolio_return)
            for i in reversed(range(self.table_layout.count())): 
                self.table_layout.itemAt(i).widget().deleteLater()
            table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            table.resizeColumnsToContents()
            table.resizeRowsToContents()
            self.table_layout.addWidget(table)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Macintosh')
    w = AnnualizedReturnCalculator()
    w.show()
    w.setFocus()
    sys.exit(app.exec_())
