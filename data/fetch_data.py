import pypyodbc
import csv

# MS ACCESS DB CONNECTION
pypyodbc.lowercase = False
conn = pypyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:~/MyDocuments/CLLabby/2021\ Summer\ Research/Laser\ Powder\ Bed\ Fusion\parameter_data.accdb;")

# OPEN CSV AND ITERATE THROUGH RESULTS
with open('am_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)    
    for row in cur.fetchall() :
        writer.writerow(row)

cur.close()
conn.close()