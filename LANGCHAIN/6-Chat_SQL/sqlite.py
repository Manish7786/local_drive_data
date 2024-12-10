import sqlite3

## connect to sqlite
connection = sqlite3.connect("employee.db")

## create a cursor object to insert record, create table
cursor = connection.cursor()

## Create the table
table_info = """
create table EMPLOYEE(NAME VARCHAR(25), DESIGNATION VARCHAR(25),
ROLE varchar(25), STATE varchar(25), MOBILE int, SALARY int)
"""

cursor.execute(table_info)

## Insert some more records
cursor.execute('''INSERT INTO EMPLOYEE VALUES('Manish', 'Project Associate', 'Data Science', 'Haryana', 7015850084, 120000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES('Baiju', 'Project Associate', 'Developer', 'Maharastra', 7263870062, 120000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES('Shivani', 'Project Associate', 'Developer', 'Maharastra', 7836537937, 130000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES('Artika', 'Project Engineer', 'Developer', 'UP', 8687983974, 150000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES('Shubham', 'Project Engineer', 'Developer', 'Chattisgarh', 8637593743, 155000)''')
cursor.execute('''INSERT INTO EMPLOYEE VALUES('Shouvik', 'Knowledge Associate', 'Data Science', 'West Bengal', 8365739579, 200000)''')

## Display all the records
print("The inserted records are")
data = cursor.execute('''Select * from EMPLOYEE''')
for row in data:
    print(row)

## Commit your changes in the database
connection.commit()
connection.close()