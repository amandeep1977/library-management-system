from sqlite3 import *

con=None
try:
	con=connect('Library_table.db')
	print('Database created')
	cursor = con.cursor()
	sql = "create table book(bisbn int primary key, name text, price int)"
	cursor.execute(sql)
	print("Table Created")
except exception as e:
	print('Issue', e)
finally:
	if con is not None:
		con.close()
		print('closed')