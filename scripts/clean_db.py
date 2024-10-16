import psycopg2

conn = psycopg2.connect(database = "equity_calculator", 
                        user = "postgres", 
                        host= 'db_equity_calculator',
                        password = "example",
                        port = 5432)

cur = conn.cursor()
query = "TRUNCATE TABLE Equity"

try:
    cur.execute(query, (First, Second))
except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")


conn.commit()
conn.close()
