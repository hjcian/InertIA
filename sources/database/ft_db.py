from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint

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

class FT_Table(Base):
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
        self.Symbol = Symbol.strip()
        self.Quantity = _str2Float(Quantity)
        self.Price = _str2Float(Price)
        self.Action = Action.strip()
        self.Description = Description.strip()
        self.TradeDate = _parseTimeStr(TradeDate)
        self.SettledDate = _parseTimeStr(SettledDate)
        self.Interest = _str2Float(Interest)
        self.Amount = _str2Float(Amount)
        self.Commission = Commission.strip()
        self.Fee = _str2Float(Fee)
        self.CUSIP = CUSIP.strip()
        self.RecordType = RecordType.strip()

    def __repr__(self):
        return "FT_CSV( {} , {} , {} , {} , {} , {} )".format(
            self.Symbol,
            self.Quantity,
            self.Price,
            self.Action,
            self.TradeDate,
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

    def write(self, **kwargs):
        try:
            row = FT_Table(**kwargs)
            self.session.add(row)
            self.session.commit()
        except Exception as err:
            self.session.rollback()
            print('Error when write data: {}'.format(err))
    
    def queryAll(self):
        ret = self.session.query(FT_Table).all()
        return ret