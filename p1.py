from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import bs4
import requests
from PIL import Image, ImageTk

def add():
	add_window.deiconify()
	main_window.withdraw()

def view():
	view_window.deiconify()
	main_window.withdraw()	
	view_window_book_data.delete(1.0, END)
	info=""
	con=None
	try:
		con=connect('Library_table.db')
		cursor=con.cursor()
		sql = "select * from book"
		cursor.execute(sql)
		data = cursor.fetchall()
		for d in data:
			info = info + "Book ISBN: " + str(d[0]) +"\t\tName: "+ str(d[1]) + "\t\tPrice: " + str(d[2]) + '\n'
		print(info)
		view_window_book_data.insert(INSERT, info)
	except Exception as e:
		showerror('Failure', e)
	finally:
		if con is not None:
			con.close()
			


def update():
	update_window.deiconify()
	main_window.withdraw()

def delete():
	delete_window.deiconify()
	main_window.withdraw()

def save(num):
	if num == 1:
		con=None
		try:
			con=connect('Library_table.db')
			cursor=con.cursor()
			sql = "insert into book values ('%d', '%s', '%d')"
			r = int(add_window_ent_isbn.get())
			n = add_window_ent_name.get()
			m = int(add_window_ent_price.get())
			
			if r < 0:
				showerror('Failure', 'Book ISBN cannot be negative')
			elif (len(n) < 2) or (not n.isalpha()):
				showerror('Failure','Invalid name')
			elif (m < 1) :
				showerror('Failure', 'Invalid price')
			else:
				cursor.execute(sql % (r, n, m))
				con.commit()
				showinfo('Success', 'Record Added')
		except ValueError:
			showerror('Failure', "ISBN and Price cannot be empty")
		except Exception as e:
			showerror("Failure", e)
		finally:
			if con is not None:
				con.close()
	
	elif num == 2:
		con=None
		try:
			con=connect('Library_table.db')
			cursor=con.cursor()
			sql = "update book set name = '%s', price='%d' where bisbn = '%d'"
			isbn = int(update_window_ent_isbn.get())
			name = update_window_ent_name.get()
			price = int(update_window_ent_price.get())
			cursor.execute(sql % (name, price, isbn))
			if isbn < 0:
				showerror('Failure', 'Book ISBN cannot be negative')
			elif (len(name) < 2) or (not name.isalpha()):
				showerror('Failure','Invalid Title')
			elif (price < 1) :
				showerror('Failure', 'Invalid price')
			elif cursor.rowcount > 0:
				showinfo('Success', "Record Updated")
				con.commit()
			else:
				showerror("Warning", "Record does not exist")
		except ValueError:
			showerror('Failure', "ISBN and price cannot be empty")
		except Exception as e:
			showerror("Failure", e)
			con.rollback()
		finally:
			if con is not None:
				con.close()

	elif num == 3:
		con=None
		try:
			con = connect('Library_table.db')
			cursor = con.cursor()
			sql = "delete from book where bisbn = '%d'"
			isbn = int(delete_window_ent_isbn.get())
			cursor.execute(sql % (isbn))
			if isbn < 0:
				showerror('Failure', 'Book ISBN cannot be negative')
			elif cursor.rowcount > 0:
				showinfo('Success', 'Record deleted')
				con.commit()
			else:
				showerror('Check', 'Record does not exist')
		except ValueError:
			showerror('Failure', "Book ISBN cannot be empty")
		except Exception as e:
			showerror('Issue', e)
		finally:
			if con is not None:
				con.close()
	
		
		

def back(num):
	if num == 1:
		main_window.deiconify()
		add_window.withdraw()
	elif num == 2:
		main_window.deiconify()
		view_window.withdraw()
	elif num == 3:
		main_window.deiconify()
		update_window.withdraw()
	elif num == 4:
		main_window.deiconify()
		delete_window.withdraw()
	else:
		print('Invalid')
	


try:
	wa = "https://ipinfo.io/"
	res = requests.get(wa)
	data = res.json()
	city_name = data['city']
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city_name
	a2 = "&appid=" + "f6e4d787873078dad37e5bdce4c3e4cd"
	web_add = a1+a2
	res = requests.get(web_add)
	data = res.json()	
	temperature = data['main']
	temp = str(temperature['temp']) + "\u2103"

except Exception as e:
	print("issue",e)




main_window = Tk()
main_window.title('Library Management System')
main_window.geometry('600x500+400+100')
image = Image.open("bg.jpg")
  
# Reszie the image using resize() method
resize_image = image.resize((650,520))
  
img = ImageTk.PhotoImage(resize_image)

label1 = Label(main_window,image=img)
label1.image = img
label1.place(x=0,y=0)

f = ('Calibri', 20, 'bold')
f1 = ('Times New Roman',25,'bold')
proj_label = Label(main_window, text="LIBRARY MANAGEMENT SYSTEM", font=f1,fg='Brown',bg='yellow')
add_button = Button(main_window, text="Add Book", width=15, font=f,bg='dark blue',fg='white', command=add)
view_button = Button(main_window, text = "View Book", width=15, font=f,bg='dark blue',fg='white', command=view)
update_button = Button(main_window, text = "Update Book", width=15, font=f,bg='dark blue',fg='white', command=update)
delete_button = Button(main_window, text = "Delete Book", width=15, font=f,bg='dark blue',fg='white', command=delete)
loc_label = Label(main_window, text="Location:" + city_name, font=f,fg='dark blue')
temp_label = Label(main_window, text="Temp: " +temp, font=f,fg='dark blue')

proj_label.pack(pady=10)
add_button.pack(pady=10)
view_button.pack(pady=10)
update_button.pack(pady=10)
delete_button.pack(pady=10)
loc_label.place(x=20, y=400)
temp_label.place(x=350,y=400)

add_window = Toplevel(main_window)
add_window.title('Add Book')
add_window.geometry('500x550+500+100')


resize_image = image.resize((650,550))
img = ImageTk.PhotoImage(resize_image)
label2 = Label(add_window,image=img)
label2.image = img
label2.place(x=0,y=0)

add_window_lbl_isbn = Label(add_window, text="Enter Book ISBN:",fg='dark blue', font=f)
add_window_ent_isbn = Entry(add_window, bd=5, font=f,fg='dark blue')
add_window_lbl_name = Label(add_window, text="Enter Title:",fg='dark blue', font=f)
add_window_ent_name = Entry(add_window, bd=5, font=f,fg='dark blue')
add_window_lbl_price = Label(add_window, text="Enter Price:",fg='dark blue', font=f)
add_window_ent_price = Entry(add_window, bd=5, font=f,fg='dark blue')
add_window_btn_save = Button(add_window, text="Save", width=10, font=f,bg='dark blue',fg='white', command=lambda:save(1))
add_window_btn_back = Button(add_window, text="Back", width=10, font=f,bg='dark blue',fg='white', command=lambda:back(1))

add_window_lbl_isbn.pack(pady=10)
add_window_ent_isbn.pack(pady=10)
add_window_lbl_name.pack(pady=10)
add_window_ent_name.pack(pady=10)
add_window_lbl_price.pack(pady=10)
add_window_ent_price.pack(pady=10) 
add_window_btn_save.pack(pady=10)
add_window_btn_back.pack(pady=10)
add_window.withdraw()



view_window = Toplevel(main_window)
view_window.title('View Books.')
view_window.geometry('700x500+400+100')

resize_image = image.resize((700,500))
img = ImageTk.PhotoImage(resize_image)
label2 = Label(view_window,image=img)
label2.image = img
label2.place(x=0,y=0)

view_window_book_data = ScrolledText(view_window, width=70, height=10,font=('Arial', 20, 'bold'))
view_window_btn_back = Button(view_window, text='Back',bg='dark blue',fg='white',font=('Arial', 20, 'bold'), command=lambda:back(2))

view_window_book_data.pack(pady=10)
view_window_btn_back.pack(pady=10)
view_window.withdraw()


update_window = Toplevel(main_window)
update_window.title('Update Book')
update_window.geometry('500x550+500+100')

resize_image = image.resize((600,500))
img = ImageTk.PhotoImage(resize_image)
label2 = Label(update_window,image=img)
label2.image = img
label2.place(x=0,y=0)


update_window_lbl_isbn = Label(update_window, text="Enter Book ISBN:",fg='dark blue', font=f)
update_window_ent_isbn = Entry(update_window, bd=5, font=f,fg='dark blue')
update_window_lbl_name = Label(update_window, text="Enter Title:",fg='dark blue', font=f)
update_window_ent_name = Entry(update_window, bd=5, font=f,fg='dark blue')
update_window_lbl_price = Label(update_window, text="Enter Price:",fg='dark blue', font=f)
update_window_ent_price = Entry(update_window, bd=5, font=f,fg='dark blue')
update_window_btn_save = Button(update_window, text="Save", width=10, font=f,bg='dark blue',fg='white', command=lambda:save(2))
update_window_btn_back = Button(update_window, text="Back", width=10, font=f,bg='dark blue',fg='white', command=lambda:back(3))


update_window_lbl_isbn.pack(pady=10)
update_window_ent_isbn.pack(pady=10)
update_window_lbl_name.pack(pady=10)
update_window_ent_name.pack(pady=10)
update_window_lbl_price.pack(pady=10)
update_window_ent_price.pack(pady=10) 
update_window_btn_save.pack(pady=10)
update_window_btn_back.pack(pady=10)
update_window.withdraw()



delete_window = Toplevel(main_window)
delete_window.title('Delete Book')
delete_window.geometry('500x500+400+100')
resize_image = image.resize((600,500))
img = ImageTk.PhotoImage(resize_image)
label2 = Label(delete_window,image=img)
label2.image = img
label2.place(x=0,y=0)

delete_window_lbl_isbn = Label(delete_window, text="Enter Book ISBN:", font=f,fg='dark blue')
delete_window_ent_isbn = Entry(delete_window, bd=5, font=f,fg='dark blue')

delete_window_btn_save = Button(delete_window, text="Save", width=10, font=f,bg='dark blue',fg='white', command=lambda:save(3))
delete_window_btn_back = Button(delete_window, text="Back", width=10, font=f,bg='dark blue',fg='white', command=lambda:back(4))

delete_window_lbl_isbn.pack(pady=10)
delete_window_ent_isbn.pack(pady=10)
delete_window_btn_save.pack(pady=10)
delete_window_btn_back.pack(pady=10)
delete_window.withdraw()


main_window.mainloop()