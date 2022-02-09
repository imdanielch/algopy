from typing import List, Optional
from datetime import date, time, timedelta, datetime
from pydantic import BaseModel


class FutureTransactionBase(BaseModel):
    id: int


class FutureTransaction(FutureTransactionBase):
    date: date
    symbol: str
    contract_cycle: str
    time: time
    price: Optional[float] = None
    volume: int

    class Config:
        orm_mode = True


class FutureTransactionBTW(FutureTransactionBase):
    datetime: datetime
    symbol: str
    contract_cycle: str
    price: Optional[float] = None
    volume: int



class FutureTransactionFull(FutureTransaction):
    front_month_price: Optional[float] = None
    back_month_price: Optional[float] = None
    cop: Optional[str] = ' '


class FutureTransactionOHLC(BaseModel):
    datetime: str
    symbol: str
    o: Optional[float] = None
    h: Optional[float] = None
    l: Optional[float] = None
    c: Optional[float] = None
    volume: int
    tick: int

    class Config:
        orm_mode = True


class InstitutionalTradeBase(BaseModel):
    date: date
    symbol: str
    institution: str
    long_trading: int
    short_trading: int
    net_trading: int
    long_open_interest: int
    short_open_interest: int
    net_open_interest: int


class InstitutionalTrade(InstitutionalTradeBase):
    id: int
    
    class Config:
        orm_mode = True


class InstitutionalTradePrice(InstitutionalTrade):
    long_trading_currency: int
    short_trading_currency: int
    net_trading_currency: int
    long_open_interest_currency: int
    short_open_interest_currency: int
    net_open_interest_currency: int
