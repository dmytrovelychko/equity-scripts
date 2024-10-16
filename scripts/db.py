import psycopg2
import pandas as pd

def is_record_exists(First, Second):
    conn = psycopg2.connect(database = "equity_calculator", 
                        user = "postgres", 
                        host= 'db_equity_calculator',
                        password = "example",
                        port = 5432)

    cur = conn.cursor()
    query = "SELECT 1 FROM Equity WHERE First = %s AND Second = %s LIMIT 1"

    try:
        cur.execute(query, (First, Second))
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
        return False

    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists



def insert(First, Second, A, B, C, D, E, F, Concat, Equity):
    conn = psycopg2.connect(database = "equity_calculator", 
                        user = "postgres", 
                        host= 'db_equity_calculator',
                        password = "example",
                        port = 5432)

    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Equity (First, Second, A, B, C, D, E, F, Concat, Equity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (First, Second, A, B, C, D, E, F, Concat, str(Equity)))
    except Exception as e:
        conn.rollback()
        print(f"An error occurred: {e}")
        return False
    conn.commit()
    conn.close()

def sql_to_dataframe():
    conn = psycopg2.connect(database = "equity_calculator", 
                        user = "postgres", 
                        host= 'db_equity_calculator',
                        password = "example",
                        port = 5432)

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT First, Second, A, B, C, D, E, F, Concat, Equity FROM Equity")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    tuples_list = cursor.fetchall()
    cursor.close()
    # Now we need to transform the list into a pandas DataFrame:
    df = pd.DataFrame(tuples_list, columns=("First", "Second", "A", "B", "C", "D", "E", "F", "Concat", "Equity"))
    return df