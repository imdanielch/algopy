from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas


def symbol_filler(sym):
    """raw data has a fixed size of 7 characters,
    this fills in the trailing spaces for matching"""
    new_sym = sym
    new_sym += ' ' * (7 - len(sym))
    return new_sym


def cycle_filler(cycle):
    """raw data has a fixed size of 11 characters,
    this fills in the trailing spaces for matching"""
    new_cycle = cycle 
    new_cycle += ' ' * (11 - len(cycle))
    return new_cycle


def get_symbol_transactions(db: Session, symbol: str):
    return db.query(models.FutureTransaction)\
            .filter(models.FutureTransaction.symbol == symbol_filler(symbol)).all()


def get_symbol_datetime_transactions(
        db: Session,
        symbol: str,
        start_date: datetime,
        end_date: datetime):
    s_date = start_date.date()
    s_time = start_date.time()
    e_date = end_date.date()
    e_time = end_date.time()
    return db.query(models.FutureTransaction)\
            .filter(models.FutureTransaction.symbol == symbol_filler(symbol))\
            .filter(models.FutureTransaction.date >= s_date)\
            .filter(models.FutureTransaction.time >= s_time)\
            .filter(models.FutureTransaction.date <= e_date)\
            .filter(models.FutureTransaction.time <= e_time).all()


def get_test(db: Session):
    return db.query(models.FutureTransaction)\
            .limit(5).all()
'''
def get_ohlc(
        db: Session,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        resolution: str):
    s_date = start_date.date()
    s_time = start_date.time()
    e_date = end_date.date()
    e_time = end_date.time()
    return db.query(models.FutureTransaction)\
            .filter(models.FutureTransaction.symbol == symbol_filler(symbol))\
            .filter(models.FutureTransaction.date >= s_date)\
            .filter(models.FutureTransaction.time >= s_time)\
            .filter(models.FutureTransaction.date <= e_date)\
            .filter(models.FutureTransaction.time <= e_time).all()
'''
