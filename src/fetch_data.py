#!/usr/bin/python3
# fetch_data.py
# William O'Brien

import pypyodbc
import h5py as hdf
import pandas as pd
import csv
import sys

def fetch():
    argc = len(sys.argv)

    if argc != 2:
        print("usage: fetch_data.py <file_path>")
        exit(1)

    fpath = sys.argv[1]

    out_name = 'interim_data'

    # MS ACCESS DB CONNECTION
    pypyodbc.lowercase = False
    try:
        conn = pypyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            f"Dbq=C:{fpath};")
        print("\nconnected to database...\n")
    except:
        print('\nfile path not found...trying default path')
        try:
            conn = pypyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            r"Dbq=C:../data/raw/parameter_data.accdb;")
        except:
            print("\nDefault path not found // Unix systems not supported on MS Access")
            exit()

    # OPEN CURSOR AND EXECUTE SQL
    cur = conn.cursor()
    try:
        table = input('\nselect table >>> ')
        cur.execute(f"SELECT * FROM {table}")
    except:
        print("table not found")
        exit()

    print("\nexporting data to csv...")

    # OPEN CSV AND ITERATE THROUGH RESULTS
    with open(f'../data/interim/{out_name}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(i[0] for i in cur.description)
        for row in cur.fetchall() :
            writer.writerow(row)

    cur.close()
    conn.close()

    print("\ndone.")

if __name__ == '__main__':
    fetch()
