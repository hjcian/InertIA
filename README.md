# InertIA

InertIA，為 Inert Investment Assistant 的縮寫，是一跟指數化投資人一樣懶惰的投資助理，希冀協助指數型投資人能夠不受到外力的影響(消息、短期波動)，保持著嚴謹的投資慣性(inertia)。

# SPEC
**backend**

1. read Fistrade standard trading history output file (CSV), write to sqlite3
2. given a symbol "ticker" and "price", calculate that symbol's annually returns
    - 2.1 support multiple tickers calculation


# Dependencies
1. docopt
2. sqlalchemy
3. scipy-1.2.0 (numpy-1.16.1)

# Online resource
- [Alpha Vantage](https://www.alphavantage.co/): free APIs for realtime and historical data on stocks and etc. 