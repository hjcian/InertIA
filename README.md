# InertIA

InertIA，為 Inert Investment Assistant 的縮寫，是一跟指數化投資人一樣懶惰的投資助理，希冀協助指數型投資人能夠不受到外力的影響(消息、短期波動)，保持著嚴謹的投資慣性(inertia)。

# Features

- 匯入
    1. 一鍵匯入 Firstrade 標準帳戶交易紀錄CSV檔
- 財務計算
    1. 手動填入一個或多個股票代號及現在每股淨值，並根據已匯入的資料計算年化投資報酬率


# For developers
**Run by native python**

直接 fork 或 pull 此專案，並且執行以下：
```bash shell
$ virtualenv -p python3 env
(env)$ pip intall -r requirements.txt
(env)$ python sources/main.py
```

**Pack executable binary on Windows**
1. run pyi-makespec with necessary paths
    ```bash
    $ ~/Anaconda3/envs/YourProject/Scripts/pyi-makespec.exe -n inertia -p sources/util/ -p sources/database/ -p sources/financial/ -p sources/tabs/ -p sources/tabs/gui_util/ sources/main.py
    ```
2. now run pyinstaller to build the executable
    ```bash
    $ ~/Anaconda3/envs/YourProject/Scripts/pyinstaller.exe inertia.spec -n inertia --onedir -y
    ```

## SPECs
**backend (prefix B)**

1. read Fistrade standard trading history output file (CSV), write to sqlite3
2. given a symbol "ticker" and "price", calculate that symbol's annually returns
    - 2.1 support multiple tickers calculation

**GUI (prefix G)**
1. add a window for providing a input interface to symbol and price and calcualting annualized return by input information
2. add a window for providing a entry point for selecting file and import it

## Dependencies
1. python3.5 or 3.6
2. docopt
3. sqlalchemy
4. scipy-1.2.0 (numpy-1.16.1)
5. PyQt5-5.11.3

## Online resource
- [Alpha Vantage](https://www.alphavantage.co/): free APIs for realtime and historical data on stocks and etc. 

## Good Q&A
- [dynamically adding and removing widgets in PyQt](https://stackoverflow.com/questions/8651742/dynamically-adding-and-removing-widgets-in-pyqt)

- [setFocus() after show](https://stackoverflow.com/questions/49418905/pyqt-setting-focus-on-qlineedit-widget)

- [How to restrict user input in QLineEdit in pyqt](https://stackoverflow.com/questions/15829782/how-to-restrict-user-input-in-qlineedit-in-pyqt)
    - base: [QValidator](http://pyqt.sourceforge.net/Docs/PyQt4/qvalidator.html)
    ```python
    self.onlyInt = QIntValidator()
    self.LineEdit.setValidator(self.onlyInt)
    ```

- [Validating user input in PyQt4(it work on PyQt5) using QValidator](https://snorfalorpagus.net/blog/2014/08/09/validating-user-input-in-pyqt4-using-qvalidator/)

- Why I just type `pip install pyinstaller`, then got an `ImportError: No module named 'PyInstaller'`? [(*stackoverflow*)](https://stackoverflow.com/questions/44740792/pyinstaller-no-module-named-pyinstaller)

- ImportError when runtime [stackoverflow](https://stackoverflow.com/questions/32093559/exe-file-created-by-pyinstaller-not-find-self-defined-modules-while-running)
    - add path which use sys.path added to 'pathex' in ProgramName.spec