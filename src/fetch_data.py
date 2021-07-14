#!/usr/bin/python3
# fetch_data.py
# William O'Brien 07/08/2021

import pypyodbc
import pandas as pd
import csv
import sys
import os

def fetch():
    print("--------------------\nFetching Data\n--------------------")
    argc = len(sys.argv)
    # optional usuage: fetch_data.py <file_path> <file_name>
    
    if argc > 1:
        # optional: can adjust file path on CL
        fpath = sys.argv[1]
        out_name = 'interim_data'
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
        print("connected to database...")
    except:
        print('\nfile path not found...trying default path')
        try:
            default_path = '../data/raw/research_data.accdb'
            p = os.path.join(os.path.dirname(__file__), default_path)

            conn = pypyodbc.connect(
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
            f"Dbq={p};")
        except Exception as e:
            print("\ndefault path not found | unix systems not supported on MS Access")
            print("error:", e)
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
    out_path = f'../data/interim/{out_name}.csv'
    f_out = os.path.join(os.path.dirname(__file__), out_path)
    with open(f_out, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(i[0] for i in cur.description)
        for row in cur.fetchall() :
            writer.writerow(row)

    cur.close()
    conn.close()

    print("\ndone.")

if __name__ == '__main__':
    fetch()
