from sqlalchemy.orm import Session
from sqlalchemy import func, null, and_
from sqlalchemy.sql import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ARRAY, aggregate_order_by
from datetime import datetime
import models, schemas


def symbol_filler(sym):
    """raw data has a fixed size of 7 characters,
    this fills in the trailing spaces for matching"""
    new_sym = str(sym)
    new_sym += ' ' * (7 - len(sym))
    return new_sym


def cycle_filler(cycle):
    """raw data has a fixed size of 11 characters,
    this fills in the trailing spaces for matching"""
    new_cycle = str(cycle)
    new_cycle += ' ' * (11 - len(cycle))
    return new_cycle


def get_symbol_transactions(db: Session, symbol: str):
    return db.query(
            models.FutureTransaction.id,
            func.CONCAT_WS('T',
                models.FutureTransaction.date,
                models.FutureTransaction.time)
                .label('datetime'),
            #models.FutureTransaction.date,
            #models.FutureTransaction.time,
            models.FutureTransaction.symbol,
            models.FutureTransaction.contract_cycle,
            models.FutureTransaction.price,
            models.FutureTransaction.volume
            )\
            .filter(models.FutureTransaction.symbol == symbol_filler(symbol))\
            .all()


def get_symbol_datetime_transactions(
        db: Session,
        symbol: str,
        start_date: datetime,
        end_date: datetime):
    s_date = start_date.date()
    s_time = start_date.time()
    e_date = end_date.date()
    e_time = end_date.time()
    return db.query(
            models.FutureTransaction.id,
            func.CONCAT_WS('T',
                models.FutureTransaction.date,
                models.FutureTransaction.time)
                .label('datetime'),
            #models.FutureTransaction.date,
            #models.FutureTransaction.time,
            models.FutureTransaction.symbol,
            models.FutureTransaction.contract_cycle,
            models.FutureTransaction.price,
            models.FutureTransaction.volume
            )\
            .filter(models.FutureTransaction.symbol == symbol_filler(symbol))\
            .filter(models.FutureTransaction.date >= s_date)\
            .filter(models.FutureTransaction.time >= s_time)\
            .filter(models.FutureTransaction.date <= e_date)\
            .filter(models.FutureTransaction.time <= e_time)\
            .all()


def get_test(db: Session):
    return db.query(models.FutureTransaction)\
            .limit(5).all()
'''
SELECT 
    date date,
    date_trunc('hour', time) time,
    (array_agg(price ORDER BY time ASC))[1] o,
    MAX(price) h,
    MIN(price) l,
    (array_agg(price ORDER BY time DESC))[1] c,
    SUM(volume) volume,
    COUNT(*) ticks
FROM "tw_future_transaction"  
WHERE date BETWEEN '2022-01-04' AND '2022-01-05' AND symbol = 'TX     ' AND front_month_price is NULL 
GROUP BY date, date_trunc('hour', time)  
ORDER BY date, time;
'''

def get_symbol_ohlc(
        db: Session,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        resolution: str):
    #s_date = start_date.date()
    #s_time = start_date.time()
    #e_date = end_date.date()
    #e_time = end_date.time()

    if resolution in ['day', 'week', 'month','quarter', 'year', 'decade']:
        time_model = models.FutureTransaction.date
        time_q = func.to_char(func.date_trunc(resolution, time_model), 'YYYY-MM-DD').label('time_trunc')
    elif resolution in ['second', 'minute', 'hour']:
        time_model = models.FutureTransaction.time
        time_q = func.date_trunc(resolution, time_model).label('time_trunc')
    else:
        return None

    q = db.query(
            func.CONCAT_WS('T',
                models.FutureTransaction.date,
                time_q)
                .label('datetime'),
            #models.FutureTransaction.date,
            models.FutureTransaction.symbol,
            #time_q,
            func.array_agg(aggregate_order_by(models.FutureTransaction.price, models.FutureTransaction.time.asc()))[1].label('o'),
            func.max(models.FutureTransaction.price).label('h'),
            func.min(models.FutureTransaction.price).label('l'),
            func.array_agg(aggregate_order_by(models.FutureTransaction.price, models.FutureTransaction.time.desc()))[1].label('c'),
            func.sum(models.FutureTransaction.volume).label('volume'),
            func.count(models.FutureTransaction.id).label('tick')
            )\
            .filter(models.FutureTransaction.symbol == symbol_filler(symbol))\
            .filter(models.FutureTransaction.contract_cycle == cycle_filler(start_date.strftime('%Y%m')))\
            .filter(
                models.FutureTransaction.date
                + models.FutureTransaction.time >= start_date)\
            .filter(
                models.FutureTransaction.date
                + models.FutureTransaction.time <= end_date)\
            .filter(models.FutureTransaction.front_month_price == null())\
            .group_by(
                    'datetime',
                    func.date_trunc(resolution, time_model).label('time_trunc'),
                    models.FutureTransaction.symbol)\
            .all()
    return q


def get_institution_ohlc(
        db: Session,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        resolution: str):
    s_date = start_date.date()
    s_time = start_date.time()
    e_date = end_date.date()
    e_time = end_date.time()

    institution_time = models.InstitutionalTrade.date
    time_q = func.to_char(func.date_trunc(resolution, institution_time), 'YYYY-MM-DD').label('time_trunc')

#    id = Column(Integer, primary_key=True)
#    date = Column(Date)
#    symbol = Column(String)
#    institution = Column(String)
#    long_trading = Column(Integer)
#    long_trading_currency = Column(Integer)
#    short_trading = Column(Integer)
#    short_trading_currency = Column(Integer)
#    net_trading = Column(Integer)
#    net_trading_currency = Column(Integer)
#    long_open_interest = Column(Integer)
#    long_open_interest_currency = Column(Integer)
#    short_open_interest = Column(Integer)
#    short_open_interest_currency = Column(Integer)
#    net_open_interest = Column(Integer)
#    net_open_interest_currency = Column(Integer)
    reference_symbol = {
            'TXF': '臺股期貨',
            'TE': '電子期貨',
            'TF': '金融期貨',
            'MXF': '小型臺指期貨',
            'ZEF': '小型電子期貨',
            'ZFF': '臺灣50期貨',
            'T5F': '股票期貨',
            #'ETF': 'ETF期貨',
            'GTF': '櫃買指數期貨',
            'XIF': '非金電期貨',
            'G2F': '富櫃200期貨',
            'E4F': '臺灣永續期貨',
            'BTF': '臺灣生技期貨',
            'TJF': '東證期貨',
            'SPF': '美國標普500期貨',
            'UNF': '美國那斯達克100期貨',
            'UDF': '美國道瓊期貨',
            'F1F': '英國富時100期貨'
            }
    if resolution == 'day':
        q = db.query(
                models.InstitutionalTrade.symbol,
                time_q,
                models.InstitutionalTrade.institution,
                func.sum(models.InstitutionalTrade.net_trading).label('net_trading'),
                func.sum(models.InstitutionalTrade.net_open_interest).label('net_open_interest')
                )\
                .filter(models.InstitutionalTrade.symbol == reference_symbol[symbol])\
                .filter(models.InstitutionalTrade.date >= s_date)\
                .filter(models.InstitutionalTrade.date <= e_date)\
                .group_by(models.InstitutionalTrade.institution)\
                .group_by(func.date_trunc(resolution, institution_time).label('time_trunc'), models.InstitutionalTrade.symbol)\
                .all()
    else:
        q = db.query(
                models.InstitutionalTrade.symbol,
                time_q,
                func.array_agg(aggregate_order_by(models.InstitutionalTrade.long_trading, models.InstitutionalTrade.long_trading.asc()))[1].label('lo'),
                func.array_agg(aggregate_order_by(models.InstitutionalTrade.long_trading, models.InstitutionalTrade.long_trading.desc()))[1].label('lc'),
                func.max(models.InstitutionalTrade.long_trading).label('lh'),
                func.min(models.InstitutionalTrade.long_trading).label('ll'),
                func.array_agg(aggregate_order_by(models.InstitutionalTrade.short_trading, models.InstitutionalTrade.short_trading.asc()))[1].label('so'),
                func.array_agg(aggregate_order_by(models.InstitutionalTrade.short_trading, models.InstitutionalTrade.short_trading.desc()))[1].label('sc'),
                func.max(models.InstitutionalTrade.short_trading).label('sh'),
                func.min(models.InstitutionalTrade.short_trading).label('sl'),
                func.array_agg(aggregate_order_by(models.InstitutionalTrade.net_trading, models.InstitutionalTrade.net_trading.asc()))[1].label('no'),
                func.array_agg(aggregate_order_by(models.InstitutionalTrade.net_trading, models.InstitutionalTrade.net_trading.desc()))[1].label('nc'),
                func.max(models.InstitutionalTrade.net_trading).label('nh'),
                func.min(models.InstitutionalTrade.net_trading).label('nl'),
                models.InstitutionalTrade.institution,
                func.sum(models.InstitutionalTrade.net_trading).label('net_trading'),
                func.sum(models.InstitutionalTrade.net_open_interest).label('net_open_interest')
                )\
                .filter(models.InstitutionalTrade.symbol == reference_symbol[symbol])\
                .filter(models.InstitutionalTrade.date >= s_date)\
                .filter(models.InstitutionalTrade.date <= e_date)\
                .group_by(models.InstitutionalTrade.institution)\
                .group_by(func.date_trunc(resolution, institution_time).label('time_trunc'), models.InstitutionalTrade.symbol)\
                .all()

    return q


def get_vsinstitution_ohlc(
        db: Session,
        symbol: str,
        start_date: datetime,
        end_date: datetime,
        resolution: str):
    s_date = start_date.date()
    s_time = start_date.time()
    e_date = end_date.date()
    e_time = end_date.time()

    institution_time = models.InstitutionalTrade.date
    time_q = func.to_char(func.date_trunc(resolution, institution_time), 'YYYY-MM-DD').label('time_trunc')

    reference_symbol = {
            'TXF': '臺股期貨',
            'TE': '電子期貨',
            'TF': '金融期貨',
            'MXF': '小型臺指期貨',
            'ZEF': '小型電子期貨',
            'ZFF': '臺灣50期貨',
            'T5F': '股票期貨',
            #'ETF': 'ETF期貨',
            'GTF': '櫃買指數期貨',
            'XIF': '非金電期貨',
            'G2F': '富櫃200期貨',
            'E4F': '臺灣永續期貨',
            'BTF': '臺灣生技期貨',
            'TJF': '東證期貨',
            'SPF': '美國標普500期貨',
            'UNF': '美國那斯達克100期貨',
            'UDF': '美國道瓊期貨',
            'F1F': '英國富時100期貨'
            }
    if resolution == 'day':
        q = db.query(
                models.InstitutionalTrade.symbol,
                time_q,
                models.InstitutionalTrade.institution,
                func.sum(models.InstitutionalTrade.net_trading).label('net_trading'),
                func.sum(models.InstitutionalTrade.net_open_interest).label('net_open_interest')
                )\
                .filter(models.InstitutionalTrade.symbol == reference_symbol[symbol])\
                .filter(models.InstitutionalTrade.date >= s_date)\
                .filter(models.InstitutionalTrade.date <= e_date)\
                .group_by(models.InstitutionalTrade.institution)\
                .group_by(func.date_trunc(resolution, institution_time)\
                    .label('time_trunc'), models.InstitutionalTrade.symbol)\
                .all()
    else:
        q = db.query(
                models.InstitutionalTrade.symbol,
                time_q,
                func.array_agg(aggregate_order_by(
                    models.InstitutionalTrade.long_trading,
                    models.InstitutionalTrade.long_trading.asc()))[1].label('lo'),
                func.array_agg(aggregate_order_by(
                    models.InstitutionalTrade.long_trading,
                    models.InstitutionalTrade.long_trading.desc()))[1].label('lc'),
                func.max(models.InstitutionalTrade.long_trading).label('lh'),
                func.min(models.InstitutionalTrade.long_trading).label('ll'),
                func.array_agg(aggregate_order_by(
                    models.InstitutionalTrade.short_trading,
                    models.InstitutionalTrade.short_trading.asc()))[1].label('so'),
                func.array_agg(aggregate_order_by(
                    models.InstitutionalTrade.short_trading,
                    models.InstitutionalTrade.short_trading.desc()))[1].label('sc'),
                func.max(models.InstitutionalTrade.short_trading).label('sh'),
                func.min(models.InstitutionalTrade.short_trading).label('sl'),
                func.array_agg(aggregate_order_by(
                    models.InstitutionalTrade.net_trading,
                    models.InstitutionalTrade.net_trading.asc()))[1].label('no'),
                func.array_agg(aggregate_order_by(
                    models.InstitutionalTrade.net_trading,
                    models.InstitutionalTrade.net_trading.desc()))[1].label('nc'),
                func.max(models.InstitutionalTrade.net_trading).label('nh'),
                func.min(models.InstitutionalTrade.net_trading).label('nl'),
                models.InstitutionalTrade.institution,
                func.sum(models.InstitutionalTrade.net_trading).label('net_trading'),
                func.sum(models.InstitutionalTrade.net_open_interest).label('net_open_interest')
                )\
                .filter(models.InstitutionalTrade.symbol == reference_symbol[symbol])\
                .filter(models.InstitutionalTrade.date >= s_date)\
                .filter(models.InstitutionalTrade.date <= e_date)\
                .group_by(models.InstitutionalTrade.institution)\
                .group_by(func.date_trunc(resolution, institution_time).label('time_trunc'), models.InstitutionalTrade.symbol)\
                .all()

    return q
