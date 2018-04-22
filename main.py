# -*- coding: utf-8 -*-
"""
Created on Sat Apr 14 14:26:58 2018

@author: MaxCian
"""
import os
import googlefinanceAPI as gf_api
from inertia_database import inertiaDB

db_dir = "./db_pool/"

print(os.path.dirname(db_dir))
print(os.path.abspath(db_dir))

if not os.path.exists(db_dir):
    print("not exist")
if not os.path.exists(os.path.dirname(db_dir)):
    print("not exist")
if not os.path.exists(os.path.abspath(db_dir)):
    print("not exist")



db = inertiaDB("test.db")

ssymbol = 'VT'
xsymbol = 'NYSEARCA'
p = '10d'
df = gf_api.get_prices(ssymbol, xsymbol, interval=p)
print(df)
db.add(ssymbol, xsymbol, df)
all = db.fetchall(ssymbol, xsymbol)
for t in all:
    print(t)

