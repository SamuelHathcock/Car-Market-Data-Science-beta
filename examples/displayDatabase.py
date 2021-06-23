import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('./CarMarket/test.db')
    cur = conn.cursor()
    a = cur.execute("""select * from cars_sqlite""")
    for rows in a.fetchall():
        print(rows)
    conn.close()