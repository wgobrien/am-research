import pypyodbc
import csv

# MS ACCESS DB CONNECTION
pypyodbc.lowercase = False
conn = pypyodbc.connect(
    r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};" +
    r"Dbq=C:parameter_data.accdb;")

print("\nconnected to database...\n")

# OPEN CURSOR AND EXECUTE SQL
cur = conn.cursor()
cur.execute("SELECT * FROM PorosityPlessis");

print("exporting data to csv...\n")

# OPEN CSV AND ITERATE THROUGH RESULTS
with open('am_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(i[0] for i in cur.description)
    for row in cur.fetchall() :
        writer.writerow(row)

cur.close()
conn.close()

print("done.")