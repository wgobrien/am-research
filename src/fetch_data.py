import pypyodbc
import h5py as hdf
import pandas as pd
import csv
import sys

argc = len(sys.argv)

if argc != 3:
    print("usage: fetch_data.py <file_path> <data_type>")
    print("<data_type>: h/a (hdf/MS access)")
    exit(1)

fpath = sys.argv[1]

try:
    out_name = input('output file name >> ')
except:
    out_name = 'out_file'

if sys.argv[2] == 'h':
    print('\nfinding file...')
    def hdf_to_csv(f):
        print('\nloading file...')
        try:
            dataset = hdf.File(f, 'r')
        except:
            print('\nfile not found...exit')
            exit()

        print('\nconverting to dataframe...')
        # this is hardcoded to exclude image files, to include all headers,
        # change format to pd.DataFrame(dataset) or specify known headers
        data = pd.DataFrame(dataset['data'])

        print('\nloading csv...')
        data.to_csv(f'../data/interim/{out_name}.csv')
        print('\ndone.')
    hdf_to_csv(fpath)
else:
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
            print("\ndefault path not found")
            print("unix systems not supported on access")
            exit()

    # OPEN CURSOR AND EXECUTE SQL
    cur = conn.cursor()
    cur.execute("SELECT * FROM PorosityPlessis");

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


