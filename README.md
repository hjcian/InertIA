# InertIA

InertIA，為 Inert Investment Assistant 的縮寫，是一跟指數化投資人一樣懶惰的投資助理，希冀協助指數型投資人能夠不受到外力的影響(消息、短期波動)，保持著嚴謹的投資慣性(inertia)。

# SPEC
**backend (prefix B)**

1. read Fistrade standard trading history output file (CSV), write to sqlite3
2. given a symbol "ticker" and "price", calculate that symbol's annually returns
    - 2.1 support multiple tickers calculation

**GUI (prefix G)**
1. add a window for providing a input interface to symbol and price and calcualting annualized return by input information
2. add a window for providing a entry point for selecting file and import it

# Dependencies
1. docopt
2. sqlalchemy
3. scipy-1.2.0 (numpy-1.16.1)
4. PyQt5-5.11.3

# Online resource
- [Alpha Vantage](https://www.alphavantage.co/): free APIs for realtime and historical data on stocks and etc. 


# Good Q&A worth to note (will move to other place after finishing development)
- [dynamically adding and removing widgets in PyQt](https://stackoverflow.com/questions/8651742/dynamically-adding-and-removing-widgets-in-pyqt)
- [setFocus() after show](https://stackoverflow.com/questions/49418905/pyqt-setting-focus-on-qlineedit-widget)
- [How to restrict user input in QLineEdit in pyqt](https://stackoverflow.com/questions/15829782/how-to-restrict-user-input-in-qlineedit-in-pyqt)
    - base: [QValidator](http://pyqt.sourceforge.net/Docs/PyQt4/qvalidator.html)
    ```python
    self.onlyInt = QIntValidator()
    self.LineEdit.setValidator(self.onlyInt)
    ```
- [Validating user input in PyQt4(it work on PyQt5) using QValidator](https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/)