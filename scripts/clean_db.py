import psycopg2
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

import time

logging.info("Waiting for db container up...")
time.sleep(5)

conn = psycopg2.connect(database = "equity_calculator", 
                        user = "postgres", 
                        host= 'db_equity_calculator',
                        password = "example",
                        port = 5432)

cur = conn.cursor()
query = "TRUNCATE TABLE Equity"

try:
    cur.execute(query)
except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")


conn.commit()
conn.close()
