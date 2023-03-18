from tkinter import *
from tkinter import messagebox
from db import Database
from tkinter import ttk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import tkinter as tk
import sqlite3
import datetime as dt
import csv


conn = sqlite3.connect("translate update.db")
cursor = conn.cursor()
db = Database("translate update.db")

def populate_list():
    tran_list.delete(0, END)
    for row in db.fetch():
        tran_list.insert(END, row)

def add_item():
    if pge_text.get() == "" or bhs_text.get() == "" :
        messagebox.showerror(
            "Warning!", "PG English & PG Bahasa is Required"
        )
        return
    db.insert(pge_text.get(), bhs_text.get(), flag_text.get(), sqltime.get(), sqltimeupdate)
    tran_list.delete(0, END)
    tran_list.insert(
        END, (pge_text.get(), bhs_text.get(), flag_text.get(), sqltime.get(), sqltimeupdate)
    )
    clear_text()
    populate_list()

def select_item(event):
    try:
        global selected_item
        index = tran_list.curselection()[0]
        selected_item = tran_list.get(index)

        id_entry.delete(0, END)
        id_entry.insert(END, selected_item[0])
        pge_entry.delete(0, END)
        pge_entry.insert(END, selected_item[1])
        bhs_entry.delete(0, END)
        bhs_entry.insert(END, selected_item[2])
        flag_entry.delete(0, END)
        flag_entry.insert(END, selected_item[3])
        sqltime_entry.delete(0, END)
        sqltime_entry.insert(END, selected_item[4])
        sqltimeupdate_entry.delete(0, END)
        sqltimeupdate_entry.insert(END, selected_item[5])

    except IndexError:
        pass

def remove_item():
    respon = messagebox.askquestion("Be Noticed !", "This data will be permanently deleted")

    if respon == 'yes' :
        db.remove(selected_item[0])
        clear_text()
        populate_list()
    else:
        populate_list()

def update_item():
    if pge_text.get() == "" or bhs_text.get() == "" or flag_text.get() == "" or sqltime.get() == "" or sqltime.get() != sqltime.get() :
        messagebox.showerror(
            "Warning!", "PG English, PG Bahasa, Flag, Created Time is Required"
        )
        return
    db.update(selected_item[0], pge_text.get(), bhs_text.get(), flag_text.get(), sqltime.get(), sqltimeupdate)
    populate_list()

def clear_text():
    id_entry.delete(0, END)
    pge_entry.delete(0, END)
    bhs_entry.delete(0, END)
    flag_entry.delete(0, END)
    sqltime_entry.delete(0, END)
    sqltimeupdate_entry.delete(0, END)

def clear_search():
    src_entry.delete(0, END)
    populate_list()

def search_data():
    typed = src_entry.get()
    cursor.execute("SELECT * FROM datakamus WHERE kata LIKE ?", ("%" + typed + "%",))
    result = cursor.fetchall()

    tran_list.delete(0, "end")
    for item in result:
        tran_list.insert("end", item)

def upload_file():
    try :
        file = filedialog.askopenfilename(filetypes=[("CSV File",".csv")])
        Rcsv = open(file)
        content = csv.reader(Rcsv)
        insert_records = "INSERT INTO datakamus VALUES (NULL, ?, ?, ?, ?, ?)"
        cursor.executemany(insert_records, content)
        conn.commit()
        populate_list()
        messagebox.showinfo(
                   "Sekilas Info", "Data has been added !")
    except Exception :
        messagebox.showerror(
            "Warning!", "Incorrect Data CSV")
        
# Create window object
app = Tk()
app.title("Translate Manager")
app.geometry("580x770")

# Color Background
# app.config(background="#6D7B8D")

# Column Search
src_entry = Entry(app, textvariable=StringVar, width=30)
src_entry.grid(row=2, column=0, sticky=W, pady=10, padx=20)

# Id
id_text = StringVar()
id_label = Label(app, text="Id", font=("bold", 10), pady=5, padx=20)
id_label.grid(row=3, column=0, sticky=W)
id_entry = Entry(app, textvariable=id_text, width=48)
id_entry.grid(row=3, column=0, sticky=W, padx=150)

# PG English
pge_text = StringVar()
pge_label = Label(app, text="PG English", font=("bold", 10), pady=5, padx=20)
pge_label.grid(row=4, column=0, sticky=W)
pge_entry = Entry(app, textvariable=pge_text, width=48)
pge_entry.grid(row=4, column=0, sticky=W, padx=150)

# PG Bahasa
bhs_text = StringVar()
bhs_label = Label(app, text="PG Bahasa", font=("bold", 10), pady=5, padx=20)
bhs_label.grid(row=5, column=0, sticky=W)
bhs_entry = Entry(app, textvariable=bhs_text, width=48)
bhs_entry.grid(row=5, column=0, sticky=W, padx=150)

# Flag
flag_text = StringVar()
flag_label = Label(app, text="Flag", font=("bold", 10), pady=5, padx=20)
flag_label.grid(row=6, column=0, sticky=W)
flag_entry = Entry(app, textvariable=flag_text, width=48)
flag_entry.grid(row=6, column=0, sticky=W, padx=150)

# Sqltime
sqltime = StringVar()
sqltime_label = Label(app, text="Created Time", font=("bold", 10), pady=5, padx=20)
sqltime_label.grid(row=7, column=0, sticky=W)
sqltime_entry = Entry(app, textvariable=sqltime, width=48)
sqltime_entry.grid(row=7, column=0, sticky=W, padx=150)

# Sqltime Update
sqltimeupdate = dt.datetime.now()
sqltimeupdate_label = Label(app, text="Last Updated Time", font=("bold", 10), pady=5, padx=20)
sqltimeupdate_label.grid(row=8, column=0, sticky=W)
sqltimeupdate_entry = Entry(app, textvariable=sqltimeupdate, width=48)
sqltimeupdate_entry.grid(row=8, column=0, sticky=W, padx=150)

# Translate List
tran_list = Listbox(app, height=26, width=85)
tran_list.grid(row=13, column=0, columnspan=3, rowspan=6, pady=10, sticky=W, padx=20)

# Create scroll bar
scrollbar = Scrollbar(app)
scrollbar.grid(row=13, column=0, sticky=W, padx=540, pady=120)

# Scroll to list
tran_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=tran_list.yview)

# Bind select in list
tran_list.bind("<<ListboxSelect>>", select_item)

# Button
add_btn = Button(
    app,
    text="Add Data",
    width=12,
    bg="#12AD2B",
    fg="white",
    font="Calibri 10 bold",
    command=add_item,
)
add_btn.grid(row=11, column=0, pady=10, sticky=W, padx=20)

update_btn = Button(
    app,
    text="Update Data",
    width=12,
    bg="#6698FF",
    fg="black",
    font="Calibri 10 bold",
    command=update_item,
)
update_btn.grid(row=11, column=0, sticky=W, padx=160)

remove_btn = Button(
    app,
    text="Remove Data",
    width=12,
    bg="#FF6347",
    fg="black",
    font="Calibri 10 bold",
    command=remove_item,
)
remove_btn.grid(row=11, column=0, sticky=W, padx=300)

clear_btn = Button(
    app,
    text="Clear Input",
    width=12,
    bg="#0C090A",
    fg="white",
    font="Calibri 10 bold",
    command=clear_text,
)
clear_btn.grid(row=11, column=0, sticky=W, padx=440)

upload = Button(
    app, text="Select File & Add Data Into Database",
    width=32, height= 2,
    bg="Yellow", fg="Black",
    font="Calibri 10 bold",
    command=upload_file)
upload.grid(row=12, column=0, sticky=W, padx=160)

search_btn = Button(app, text="Search Data", width=10, command=search_data)
search_btn.grid(row=2, column=0, sticky=W, padx=230)

clear_src = Button(app, text="Clear Search", width=12, command=clear_search)
clear_src.grid(row=2, column=0, sticky=W, padx=350)

# populate data
populate_list()

# Start program
app.mainloop()
