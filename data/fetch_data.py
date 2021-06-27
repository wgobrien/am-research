import pypyodbc
import csv

# MS ACCESS DB CONNECTION
pypyodbc.lowercase = False

try:
    conn = pypyodbc.connect(
        r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};" +
        r"Dbq=C:raw/parameter_data.accdb;")
    print("\nconnected to database...\n")
except:
    print("Connect to database failed")
    print("Unix systems not supported")
    exit()

# OPEN CURSOR AND EXECUTE SQL
cur = conn.cursor()
cur.execute("SELECT * FROM PorosityPlessis");

print("exporting data to csv...\n")

# OPEN CSV AND ITERATE THROUGH RESULTS
with open('interim/am_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(i[0] for i in cur.description)
    for row in cur.fetchall() :
        writer.writerow(row)

cur.close()
conn.close()

print("done.")
