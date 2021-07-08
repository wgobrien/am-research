#!/usr/bin/python3
# fetch_data.py
# William O'Brien 07/08/2021

import pypyodbc
import pandas as pd
import csv
import sys

def fetch():
    argc = len(sys.argv)
    # optional usuage: fetch_data.py <file_path> <file_name>
    
    if argc > 1:
        # optional: can adjust file path on CL
        fpath = sys.argv[1]
        # optional: can edit file out name on CL
        if argc == 3:
            out_name = sys.argv[2]
        if argc > 3:
            print('optional usuage: fetch_data.py <file_path> <file_name>')
            exit(1)
    else:
        fpath = '../data/raw/research_data.accdb'
        out_name = 'interim_data'

    # MS ACCESS DB CONNECTION
    pypyodbc.lowercase = False
    try:
        conn = pypyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            f"Dbq=C:{fpath};")
        print("\nconnected to database...")
    except:
        print('\nfile path not found...trying default path')
        try:
            conn = pypyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            r"Dbq=C:../data/raw/research_data.accdb;")
        except:
            print("\nDefault path not found // Unix systems not supported on MS Access")
            exit(1)

    # OPEN CURSOR AND EXECUTE SQL
    cur = conn.cursor()
    try:
        table = input('\nselect table >>> ')
        cur.execute(f"SELECT * FROM {table}")
    except:
        print("\ntable not found")
        exit(1)

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
