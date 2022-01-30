from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, Numeric
from sqlalchemy.orm import relationship
from db import Base

class FutureTransaction(Base):
    __tablename__ = "tw_future_transaction"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    symbol = Column(String)
    contract_cycle = Column(String)
    time = Column(Time)
    price = Column(Numeric(precision=8, scale=2))
    volume = Column(Integer)
    front_month_price = Column(Numeric(precision=8, scale=2))
    back_month_price = Column(Numeric(precision=8, scale=2))
    cop = Column(String)


class InstitutionalTrade(Base): 
    __tablename__ = "institutional_trade"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    symbol = Column(String)
    institution = Column(String)
    long_trading = Column(Integer)
    long_trading_currency = Column(Integer)
    short_trading = Column(Integer)
    short_trading_currency = Column(Integer)
    net_trading = Column(Integer)
    net_trading_currency = Column(Integer)
    long_open_interest = Column(Integer)
    long_open_interest_currency = Column(Integer)
    short_open_interest = Column(Integer)
    short_open_interest_currency = Column(Integer)
    net_open_interest = Column(Integer)
    net_open_interest_currency = Column(Integer)
