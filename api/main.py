from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

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
        response_model=List[schemas.FutureTransaction])
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


