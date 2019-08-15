import sqlite3


connection = sqlite3.connect('database.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS hoteis (hotel_id text PRIMARY KEY, nome text,\
     estrelas real, diaria real, cidade text)"

insert_hotel = "INSERT INTO hoteis VALUES ('alpha', 'Alpha Hotel', 4.3, 345.88, 'Sta. Barbara')"

cursor.execute(create_table)
cursor.execute(insert_hotel)

connection.commit()
connection.close()
