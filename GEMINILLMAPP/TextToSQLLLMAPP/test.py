import psycopg2


## Function to retrieve query from the PostgreSQL database
def read_sql_query(sql):
    try:
        conn = psycopg2.connect(
            dbname="ccares",
            user="postgres",
            password="onlyshouvikknowsthepassword",
            host="10.180.146.63",
            port="27018"
        )
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        return [("Error", str(e))]
    
query = "Select cmpf_acc_no, full_name from member_details limit 5"



data = read_sql_query(query)
for row in data:
    print(row)
