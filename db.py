"""
https://www.postgresqltutorial.com/import-csv-file-into-posgresql-table/
https://www.geeksforgeeks.org/python-import-csv-into-postgresql/

https://www.compose.com/articles/store-result-sets-with-materialized-views-in-postgresql/

COP = Calculated Open Prices from Pre-Market Opening Period.

example data:
date,symbol,contract_cycle,time,price,volume,front_month_price, back_month_price,COP
20211208,BRF    ,202202     ,190720,2062,2,-,-, 
20211209,CAF    ,202112/202201,084624,-.14,12,84.6,84.46, 
example 3faren
日期, date
商品名稱, symbol
身份別, institution
多方交易口數, long_trading
多方交易契約金額(千元), long_trading_currency
空方交易口數, short_trading
空方交易契約金額(千元), short_trading_currency
多空交易口數淨額, net_trading
多空交易契約金額淨額(千元), net_trading_currency
多方未平倉口數, long_reserve
多方未平倉契約金額(千元), long_reserve_currency
空方未平倉口數, short_reserve
空方未平倉契約金額(千元), short_reserve_currency
多空未平倉口數淨額, net_reserve
多空未平倉契約金額淨額(千元) net_reserve_currency
三大法人: institutions(id, name)
"""
"""
todo: 
    1. login to postgres
    2. create table if it doesn't exist
    3. go into directory, unzip
    4. generate sql files if don't exist
    5. import sql files into database
"""
import os
import sys
import psycopg2

def connect(db, user, password, host, port):
    try:
        conn = psycopg2.connect(database=db,
                             user=user, password=password,
                             host=host, port=port
                            )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    conn.autocommit = True
    return conn


def create_tables(conn):
    create_futures = '''CREATE TABLE IF NOT EXISTS tw_future_transaction(
                        id serial PRIMARY KEY,
                        date DATE NOT NULL,
                        symbol VARCHAR(50) NOT NULL,
                        contract_cycle VARCHAR(50) NOT NULL,
                        time TIME NOT NULL,
                        price NUMERIC(8,2),
                        volume INTEGER,
                        front_month_price NUMERIC(8,2),
                        back_month_price NUMERIC(8,2),
                        cop VARCHAR(50)
                        );
                    '''
    
    #create_institution ='''CREATE TABLE IF NOT EXISTS institution(
    #                        id serial PRIMARY KEY,
    #                        name VARCHAR(50) NOT NULL
    #                    );'''
    create_institutional_trading = '''CREATE TABLE IF NOT EXISTS institutional_trade(
                                    id serial PRIMARY KEY,
                                    date DATE NOT NULL,
                                    symbol VARCHAR(50) NOT NULL,
                                    institution VARCHAR(50) NOT NULL,
                                    long_trading INTEGER NOT NULL,
                                    long_trading_currency INTEGER NOT NULL,
                                    short_trading INTEGER NOT NULL,
                                    short_trading_currency INTEGER NOT NULL,
                                    net_trading INTEGER NOT NULL,
                                    net_trading_currency INTEGER NOT NULL,
                                    long_open_interest INTEGER NOT NULL,
                                    long_open_interest_currency INTEGER NOT NULL,
                                    short_open_interest INTEGER NOT NULL,
                                    short_open_interest_currency INTEGER NOT NULL,
                                    net_open_interest INTEGER NOT NULL,
                                    net_open_interest_currency INTEGER NOT NULL
                                    );'''
    
    c = conn.cursor()
    c.execute(create_futures)
    #cursor.execute(create_institution)
    c.execute(create_institutional_trading)

def bulk_insert_institutional_trade(conn, path):
    sql = ('''COPY institutional_trade(
                date,
                symbol,
                institution,
                long_trading,
                long_trading_currency,
                short_trading,
                short_trading_currency,
                net_trading,
                net_trading_currency,
                long_open_interest,
                long_open_interest_currency,
                short_open_interest,
                short_open_interest_currency,
                net_open_interest,
                net_open_interest_currency)
            FROM STDIN
            DELIMITER ','
            CSV HEADER;''')
    c = conn.cursor()
    with open(path, encoding = "Big5") as csvfile:
        c.copy_expert(sql, csvfile)

def bulk_insert_future_trade(conn, path):
    sql = ('''COPY tw_future_transaction(
                date,
                symbol,
                contract_cycle,
                time,
                price,
                volume,
                front_month_price,
                back_month_price,
                cop)
            FROM STDIN
            WITH (
            FORMAT CSV,
            DELIMITER ',',
            NULL '-',
            HEADER,
            FORCE_NULL (
                front_month_price,
                back_month_price,
                cop));
            ''')
    c = conn.cursor()
    with open(path, encoding = "Big5") as csvfile:
        c.copy_expert(sql, csvfile)
