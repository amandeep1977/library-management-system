from sqlite3 import *

con = None
try:
	con = connect("Library_table.db")
	print("Database Created / open ")
except Exception as e:
	print("issue", e)
finally:
	if con is not None:
		con.close()
		print("closed")