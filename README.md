# InertIA

InertIA，為 Inert Investment Assistant 的縮寫，是一個比指數化投資人更懶惰的投資工具，提供懶惰的指數化投資人分析功能，希望協助指數化投資人能夠不受到外力的影響(主動式投資的各種消息)，保持著投資紀律，去起名叫「慣性 (Inertia)」。

# SPEC
**backend**

1. read Fistrade standard trading history output file (CSV), write to sqlite3
2. given a symbol "ticker" and "price", calculate that symbol's annually returns

# Dependencies
1. docopt
2. sqlalchemy
3. scipy-1.2.0 (numpy-1.16.1)

