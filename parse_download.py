import os
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from queries import (
        )
from config import (
        postgres_db,
        postgres_user,
        postgres_password,
        postgres_host,
        postgres_port
        )
from db import (
        connect,
        create_tables,
        bulk_insert_institutional_trade,
        bulk_insert_future_trade
        )

download_path = "./download/"


conn = connect(
        postgres_db,
        postgres_user,
        postgres_password,
        postgres_host,
        postgres_port)

create_tables(conn)
inst_path = os.path.join(
        download_path,
        "institutional_trade20211101.20220126.csv")
bulk_insert_institutional_trade(conn, inst_path)

with TemporaryDirectory() as tmpdir:
    for entry in os.scandir(download_path):
        if entry.path.endswith(".zip"):
            with ZipFile(entry.path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)
            dirpath = os.path.join(tmpdir, entry.name.replace(".zip", ".csv"))
            bulk_insert_future_trade(conn, dirpath)
        elif entry.path.endswith(".csv"):
            #file_content = getFileContent(entry.path)
            print(f"not parsed: {entry.path}")
        else:
            continue

