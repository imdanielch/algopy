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
            'TXF': '????????????',
            'TE': '????????????',
            'TF': '????????????',
            'MXF': '??????????????????',
            'ZEF': '??????????????????',
            'ZFF': '??????50??????',
            'T5F': '????????????',
            #'ETF': 'ETF??????',
            'GTF': '??????????????????',
            'XIF': '???????????????',
            'G2F': '??????200??????',
            'E4F': '??????????????????',
            'BTF': '??????????????????',
            'TJF': '????????????',
            'SPF': '????????????500??????',
            'UNF': '??????????????????100??????',
            'UDF': '??????????????????',
            'F1F': '????????????100??????'
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

