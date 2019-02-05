import os
import sys
import csv
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint
FILE_DIR = os.path.dirname(os.path.realpath(__file__))
SRC_DIR = os.path.dirname(FILE_DIR)
sys.path.append(SRC_DIR)
from util import logger
LOGGER = logger.get_single_logger()

Base = declarative_base()

def _parseTimeStr(time_str):
    if time_str.count('-') == 2:
        return datetime.strptime(time_str.strip(), '%Y-%m-%d')
    elif time_str.count('/') == 2:
        return datetime.strptime(time_str.strip(), '%Y/%m/%d')
    else:
        raise KeyError('Unsupported date-string format ({})'.format(time_str))

def _str2Float(string):
    return float(string) if string else float('0.0')

class FirstradeRecord(Base):
    __tablename__ = 'ft'
    id = Column(Integer, primary_key=True)
    Symbol = Column(String)
    Quantity = Column(Float)
    Price = Column(Float)
    Action = Column(String)
    Description = Column(String)
    TradeDate = Column(DateTime)
    SettledDate = Column(DateTime)
    Interest = Column(Float)
    Amount = Column(Float)
    Commission = Column(Float)
    Fee = Column(Float)
    CUSIP = Column(String)
    RecordType = Column(String)    
    __table_args__ = (UniqueConstraint(
        'Symbol', 
        'Quantity',
        'Price', 
        'Action',
        'Description', 
        'TradeDate',
        'SettledDate',
        'Interest',
        'Amount',
        'Commission',
        'Fee',
        'CUSIP',
        'RecordType',
        name='_all_uc'),)

    def __init__(self, Symbol, Quantity, Price, Action, Description, TradeDate, SettledDate, Interest, Amount, Commission, Fee, CUSIP, RecordType):
        self.Symbol = Symbol.strip().lower()
        self.Quantity = _str2Float(Quantity)
        self.Price = _str2Float(Price)
        self.Action = Action.strip().lower()
        self.Description = Description.strip().lower()
        self.TradeDate = _parseTimeStr(TradeDate)
        self.SettledDate = _parseTimeStr(SettledDate)
        self.Interest = _str2Float(Interest)
        self.Amount = _str2Float(Amount)
        self.Commission = Commission.strip().lower()
        self.Fee = _str2Float(Fee)
        self.CUSIP = CUSIP.strip().lower()
        self.RecordType = RecordType.strip().lower()

    def __repr__(self):
        return "FT_CSV( {} , {} , {} , {} , {} , {} , {} )".format(
            self.Symbol,
            self.Quantity,
            self.Price,
            self.Action,
            self.TradeDate,
            self.Amount,
            self.RecordType,
        )

def _create(database_fpath=':memory:'):
    db_uri = 'sqlite:///{}'.format(database_fpath)
    engine = create_engine(db_uri, echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

class FirstradeDB(object):
    def __init__(self, db_fpath=':memory:'):
        self.session = _create(db_fpath)

    def _write(self, **kwargs):
        try:
            row = FirstradeRecord(**kwargs)
            self.session.add(row)
            self.session.commit()
            return 1
        except Exception as err:
            self.session.rollback()
            if "UNIQUE constraint failed" in str(err):
                LOGGER.warning('UNIQUE constraint failed, pass record ({})'.format(kwargs))
            else:
                LOGGER.error('Unexpected error: '.format(), exc_info=True)
            return 0

    def readBySymbol(self, symbol):
        try:
            ret = self.session.query(FirstradeRecord).filter(FirstradeRecord.Symbol == symbol).order_by(FirstradeRecord.TradeDate).all()            
            return ret
        except Exception as err:
            self.session.rollback()
            LOGGER.warning('Read data error: {}'.format(err))
            return []

    def importFTStandardCSV(self, fpath):
        with open(fpath, 'r') as fp:
            csv_reader = csv.DictReader(fp)        
            success_count, total = self.writeFTStandardCSV(csv_reader)
            LOGGER.error('Import: write {}/{} to FT database.'.format(success_count, total))

    def writeFTStandardCSV(self, csv_reader):
        total = 0
        success_count = 0
        for row in csv_reader:
            success_count += self._write(**row)
            total += 1
        return success_count, total

    def queryAll(self):
        ret = self.session.query(FirstradeRecord).all()
        return ret
    
class Singleton(object):
    __instance = None

    class __Singleton(FirstradeDB):
        pass

    def __new__(self, *args, **kwargs):
        if Singleton.__instance is None:
             Singleton.__instance = Singleton.__Singleton(*args, **kwargs)
        return Singleton.__instance

def get_firstrade_db(db_fpath):
    db = Singleton(db_fpath)
    return db