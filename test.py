import sqlite3

# Set Up the connection
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

# create a table or query you want from database
# then execute the query
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

user = (2, 'Pratik', 'qwerty')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

users = [
    (3, 'Ganesh', 'qwerty'),
    (4, 'Pawar', 'qwerty')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

# if data is updated then commit and close
connection.commit()

connection.close()
