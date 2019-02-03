# InertIA

InertIA，為 Inert Investment Assistant 的縮寫，是一個比指數化投資人更懶惰的投資工具，提供懶惰的指數化投資人分析功能，希望協助指數化投資人能夠不受到外力的影響(主動式投資的各種消息)，保持著投資紀律，去起名叫「慣性 (Inertia)」。

# SPEC
**backend**

1. read Fistrade standard trading history output file (CSV), write to sqlite3
2. calculate total annually yearly returns in %

# Dependencies
1. docopt
2. sqlalchemy
3. 