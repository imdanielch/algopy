from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

import crud, models, schemas
from db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
origins = [
    "http://localhost:8000",
    "http://localhost:3000",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/test", response_model=List[schemas.FutureTransaction])
async def get_test(db: Session = Depends(get_db)):
    symbol = crud.get_test(db)
    if symbol is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return symbol


@app.get("/symbol/{sym}", response_model=List[schemas.FutureTransaction])
async def get_symbol_transactions(sym: str, db: Session = Depends(get_db)):
    symbol = crud.get_symbol_transactions(db, symbol=sym)
    if symbol is None:
        raise HTTPException(status_code=404, detail="Symbol not found")
    return symbol

# datetime ISO 8601 works in url. e.g.: 2022-01-29T14:01:42
@app.get("/symbol/{sym}/{start_datetime}/{end_datetime}",
        response_model=List[schemas.FutureTransactionBTW])
async def get_symbol_datetime_transactions(
            sym: str,
            start_datetime: datetime,
            end_datetime: datetime,
            db: Session = Depends(get_db)):
    data = crud.get_symbol_datetime_transactions(
            db,
            symbol = sym,
            start_date = start_datetime,
            end_date = end_datetime)
    return data


@app.get("/symbol/{sym}/{start_datetime}/{end_datetime}/{resolution}",
        response_model=List[schemas.FutureTransactionOHLC])
async def get_symbol_ohlc(
            sym: str,
            start_datetime: datetime,
            end_datetime: datetime,
            resolution: str,
            db: Session = Depends(get_db)):
    accepted_res = [
            'second', 'minute', 'hour', 'day',
            'week', 'month', 'quarter', 'year', 'decade']
    if resolution in accepted_res:
        data = crud.get_symbol_ohlc(
                db,
                symbol = sym,
                start_date = start_datetime,
                end_date = end_datetime,
                resolution = resolution)
    else:
        raise HTTPException(status_code=400, detail="The requested resolution does not exist in " + str(accepted_res))

    return data


@app.get("/institution/{sym}/{start_datetime}/{end_datetime}/{resolution}")
async def get_institution_ohlc(
            sym: str,
            start_datetime: datetime,
            end_datetime: datetime,
            resolution: str,
            db: Session = Depends(get_db)):
    accepted_res = ['day', 'week', 'month', 'quarter', 'year', 'decade']
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
    if resolution not in accepted_res:
        raise HTTPException(status_code=400, detail="The requested resolution does not exist in " + str(accepted_res))
    if sym not in reference_symbol:
        raise HTTPException(status_code=400, detail="The requested symbol does not exist in " + str(reference_symbol))

    data = crud.get_institution_ohlc(
            db,
            symbol = sym,
            start_date = start_datetime,
            end_date = end_datetime,
            resolution = resolution)

    return data

