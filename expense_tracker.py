import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# --- Database Setup ---
db_file = "expenses.db"
db_connection = sqlite3.connect(db_file)
cur = db_connection.cursor()

# NOTE: The old try/except block for 'use mydatabase' has been removed as it's not needed for SQLite.

# --- Database Functions ---

# Create new table
def new():
    table_name = Table_Name_entry.get()
    if table_name:
        try:
            # CHANGED: Updated data types for SQLite compatibility
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    id INTEGER PRIMARY KEY,
                    day TEXT,
                    amount REAL,
                    mode TEXT,
                    remark TEXT
                )
            """)
            db_connection.commit()  # CHANGED: Used consistent connection variable
            messagebox.showinfo("Notice", "New table has been created successfully....")
            Table_Name_entry.delete(0, tk.END)
            Month_table.focus_set()
            print("Create successfully")
        except sqlite3.Error as err:  # CHANGED: Updated error type
            messagebox.showerror("Error", f"Error: {err}")

# Insert Information
def insert():
    try:
        table_name = Month_table.get()
        # CHANGED: Replaced %s with ? for SQLite parameters
        query = f"INSERT INTO `{table_name}`(day, amount, mode, remark) VALUES (?, ?, ?, ?)"
        values = (Day_entry.get(), Amount_entry.get(), Mode_of_tracs_entry.get(), Remark_entry.get())
        cur.execute(query, values)
        db_connection.commit()  # CHANGED: Used consistent connection variable
        messagebox.showinfo("Notice", "Data Inserted Successfully...")
        Month_table.delete(0, tk.END)
        Day_entry.delete(0, tk.END)
        Amount_entry.delete(0, tk.END)
        Mode_of_tracs_entry.delete(0, tk.END)
        Remark_entry.delete(0, tk.END)
        Month_table.focus_set()
        print("Data inserted successfully.")
    except Exception as e:
        print("An error occurred:", e)
        messagebox.showerror("Error", f"An error occurred: {e}")

# Delete table
def dele():
    table_name = Month_ENT.get()
    if table_name and messagebox.askyesno("Confirm", f"Are you sure you want to delete the entire table '{table_name}'?"):
        cur.execute(f"DROP TABLE IF EXISTS `{table_name}`")
        db_connection.commit() # CHANGED: Used consistent connection variable
        messagebox.showinfo("Message", f"Table '{table_name}' deleted successfully.")
        Month_ENT.delete(0, tk.END)
        Month_ENT.focus_set()
        print("Delete Succesfully")

# Delete table entry
def dele_id():
    temp1 = Month_ENT.get()
    temp2 = delete_ENT_id.get()
    try:
        # CHANGED: Replaced %s with ?
        qur = f"DELETE FROM `{temp1}` WHERE id = ?"
        cur.execute(qur, (temp2,))
        db_connection.commit() # CHANGED: Used consistent connection variable
        messagebox.showinfo("Notice", "Delete Successfully...")
        Month_ENT.delete(0, tk.END)
        delete_ENT_id.delete(0, tk.END)
        delete_ENT_id.focus_set()
    except sqlite3.Error as e: # CHANGED: Updated error type
        messagebox.showinfo("Warning", f"Error: {e}")

# Show list of tables in our database
def show_table():
    if db_connection:
        # CHANGED: Replaced 'show tables' with the SQLite equivalent
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        textarea.delete("1.0", tk.END)
        for table in tables:
            textarea.insert(tk.END, table[0] + "\n")

# Show all entries in a particular table
def show_table_data():
    if db_connection:
        show_table_name = Month_Name_Entry.get()
        try:
            cur.execute(f"SELECT * FROM `{show_table_name}`")
            rows = cur.fetchall()
            textarea.delete("1.0", tk.END)
            if not rows:
                textarea.insert(tk.END, "No Data\n")
            for x in rows:
                row_str = " | ".join(map(str, x))
                textarea.insert(tk.END, row_str + "\n")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Could not find table '{show_table_name}'. Error: {e}")

# Search by day/date
def search_by_id():
    month_name = Month_Name_Entry.get().strip()
    day_value = Day_entry_search.get().strip()
    try:
        # CHANGED: Replaced %s with ?
        query = f"SELECT * FROM `{month_name}` WHERE day = ?"
        cur.execute(query, (day_value,))
        rows = cur.fetchall()
        textarea.delete("1.0", tk.END)
        if not rows:
            textarea.insert(tk.END, "No Entry Found\n")
        else:
            for row in rows:
                row_str = " | ".join(map(str, row))
                textarea.insert(tk.END, row_str + "\n")
    except sqlite3.Error as e: # CHANGED: Updated error type
        textarea.delete("1.0", tk.END)
        textarea.insert(tk.END, f"Database Error: {e}\n")

# Clear the output window
def clear_output():
    textarea.delete("1.0", tk.END)

# This function gives the total amount
def total_amount():
    total_table = Month_total_Ent.get()
    try:
        cur.execute(f"SELECT SUM(amount) FROM `{total_table}`")
        total = cur.fetchone()[0]
        textarea.delete("1.0", tk.END)
        if total is None:
            textarea.insert(tk.END, f"Total for '{total_table}': 0.00")
        else:
            textarea.insert(tk.END, f"Total for '{total_table}': {total:.2f}")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error calculating total for '{total_table}'. Error: {e}")


# Search entry according to amount
def amount_by_search():
    month_name = Month_Name_Entry.get().strip()
    amount_value = Amount_entry_search.get()
    try:
        # CHANGED: Replaced %s with ?
        query = f"SELECT * FROM `{month_name}` WHERE amount = ?"
        cur.execute(query, (amount_value,))
        rows = cur.fetchall()
        textarea.delete("1.0", tk.END)
        if not rows:
            textarea.insert(tk.END, "No Entry Found\n")
        else:
            for row in rows:
                row_str = " | ".join(map(str, row))
                textarea.insert(tk.END, row_str + "\n")
    except sqlite3.Error as e: # CHANGED: Updated error type
        textarea.delete("1.0", tk.END)
        textarea.insert(tk.END, f"Database Error: {e}\n")

# This function calculates the total cash payment
def cash_calculate():
    month_cash = Month_total_Ent.get()
    mode_cash = Month_total_Mode_Ent.get()
    textarea.delete("1.0", tk.END)
    try:
        # CHANGED: Replaced %s with ?
        q = f"SELECT SUM(amount) FROM `{month_cash}` WHERE mode = ?"
        cur.execute(q, (mode_cash,))
        total = cur.fetchone()[0]
        if total is None:
            textarea.insert(tk.END, f"Total for mode '{mode_cash}': 0.00")
        else:
            textarea.insert(tk.END, f"Total for mode '{mode_cash}': {total:.2f}")
    except sqlite3.Error as e:
         messagebox.showerror("Error", f"Error calculating total. Error: {e}")


# This function calculates the total online payment
def online_calculate():
    month_online = Month_total_Ent.get()
    mode_online = Month_total_Mode_Ent.get()
    textarea.delete("1.0", tk.END)
    try:
        # CHANGED: Replaced %s with ?
        qur = f"SELECT SUM(amount) FROM `{month_online}` WHERE mode = ?"
        cur.execute(qur, (mode_online,))
        total = cur.fetchone()[0]
        if total is None:
            textarea.insert(tk.END, f"Total for mode '{mode_online}': 0.00")
        else:
            textarea.insert(tk.END, f"Total for mode '{mode_online}': {total:.2f}")
    except sqlite3.Error as e:
         messagebox.showerror("Error", f"Error calculating total. Error: {e}")


# --- GUI Setup ---

# Initialize window
window = tk.Tk()
window.geometry("1270x725")
window.title("Expense Tracker")

# Set window icon (make sure 'icon.ico' is in the same folder)
try:
    window.iconbitmap("icon.ico")
except tk.TclError:
    print("icon.ico not found, skipping.")


# Heading
heading = tk.Label(window, text='Expense Tracker Application', font=('times new roman', 30, 'bold'), bg='gray20', fg='gold', relief='ridge')
heading.pack(fill="both", ipady=8)

# Working frame (middle section of the application)
Working = tk.Frame(window)
Working.pack(fill=tk.BOTH, expand=True)

# Set column configuration for equal width distribution within Working frame
Working.grid_columnconfigure(0, weight=1, uniform="equal")
Working.grid_columnconfigure(1, weight=1, uniform="equal")
Working.grid_columnconfigure(2, weight=1, uniform="equal")

# Input Frame inside Working
Input = tk.LabelFrame(Working, text='Input', font=('times new roman', 15), bg='grey20', fg='gold', relief='groove', bd=8)
Input.grid(row=0, column=0, padx=2, sticky="nsew")

# Month/Year Label and Entry
Table_Name = tk.Label(Input, text='New Month Table', font=('times new roman', 15), bg='grey20', fg='white')
Table_Name.grid(row=0, column=0, padx=5, pady=5)
Table_Name_entry = tk.Entry(Input, font=('times new roman', 15), bd=5)
Table_Name_entry.grid(row=0, column=1, pady=5)

create_table = tk.Button(Input, text='Create New', font=('times new roman', 15), bd=8, bg='DeepSkyBlue2', fg='black', command=new)
create_table.grid(row=1, column=1, padx=5, pady=10)

# Month label and entry
Month = tk.Label(Input, text='Month', font=('times new roman', 15), bg='grey20', fg='white')
Month.grid(row=2, column=0, padx=5, pady=5)
Month_table = tk.Entry(Input, font=('times new roman', 15), bd=5)
Month_table.grid(row=2, column=1, pady=5)

# Day Label and Entry
Day_label = tk.Label(Input, text='Day', font=('times new roman', 15), bg='grey20', fg='white')
Day_label.grid(row=3, column=0, padx=5, pady=5)
Day_entry = tk.Entry(Input, font=('times new roman', 15), bd=5)
Day_entry.grid(row=3, column=1, pady=5)

# Amount Label and Entry
Amount_label = tk.Label(Input, text='Amount', font=('times new roman', 15), fg='white', bg='grey20')
Amount_label.grid(row=4, column=0, padx=5, pady=5)
Amount_entry = tk.Entry(Input, font=('times new roman', 15, 'bold'), bd=5)
Amount_entry.grid(row=4, column=1, pady=5)

# Mode of Transaction Label and Entry
Mode_of_tracs_label = tk.Label(Input, text='Mode', font=('times new roman', 15), fg='white', bg='grey20')
Mode_of_tracs_label.grid(row=5, column=0, padx=5, pady=5)
Mode_of_tracs_entry = tk.Entry(Input, font=('times new roman', 15, 'bold'), bd=5)
Mode_of_tracs_entry.grid(row=5, column=1, pady=5)

# Remark Label and Entry
Remark_label = tk.Label(Input, text='Remark', font=('times new roman', 15), fg='white', bg='grey20')
Remark_label.grid(row=6, column=0, padx=5, pady=5)
Remark_entry = tk.Entry(Input, font=('times new roman', 15, 'bold'), bd=5)
Remark_entry.grid(row=6, column=1, pady=5)

# Submit Button
button1 = tk.Button(Input, text='Submit', font=('times new roman', 15), fg='black', bg='lawn green', bd=5, command=insert)
button1.grid(row=7, column=1, pady=10, padx=10)

# Search Frame inside Working
Search = tk.LabelFrame(Working, text='Search', font=('times new roman', 15), bg='grey20', fg='gold', relief='groove', bd=8)
Search.grid(row=0, column=1, padx=2, sticky="nsew")

# Search Frame Content
Table_Name_search = tk.Label(Search, text='All Month Tables', font=('times new roman', 15), bg='grey20', fg='white')
Table_Name_search.grid(row=0, column=0, padx=5, pady=15)
button3 = tk.Button(Search, text='Show', font=('times new roman', 15), relief='groove', bd=5, bg='RosyBrown3', fg='black', command=show_table)
button3.grid(row=0, column=1, padx=2, pady=15)

Month_Name = tk.Label(Search, text='Month Name', font=('times new roman', 15), bg='grey20', fg='white')
Month_Name.grid(row=2, column=0, padx=5, pady=5)
Month_Name_Entry = tk.Entry(Search, font=('times new roman', 15), bd=5)
Month_Name_Entry.grid(row=2, column=1, pady=5, padx=5)

button4 = tk.Button(Search, text='Search Table Data', font=('times new roman', 15), relief='groove', bd=8, bg='seaGreen1', fg='black', command=show_table_data)
button4.grid(row=3, column=1, padx=5, pady=5)

Day_search = tk.Label(Search, text='Date', font=('times new roman', 15), fg='white', bg='grey20')
Day_search.grid(row=4, column=0, padx=5, pady=5)
Day_entry_search = tk.Entry(Search, font=('times new roman', 15, 'bold'), bd=5)
Day_entry_search.grid(row=4, column=1, pady=5, padx=5)

button4 = tk.Button(Search, text='Search By Date', font=('times new roman', 15), relief='groove', bd=8, bg='seaGreen1', fg='black', command=search_by_id)
button4.grid(row=5, column=1, padx=5, pady=5)

Amount_search = tk.Label(Search, text='Amount', font=('times new roman', 15), fg='white', bg='grey20')
Amount_search.grid(row=6, column=0, padx=5, pady=5)
Amount_entry_search = tk.Entry(Search, font=('times new roman', 15, 'bold'), bd=5)
Amount_entry_search.grid(row=6, column=1, pady=5, padx=5)

button2 = tk.Button(Search, text='Search By Amount', font=('times new roman', 15), fg='black', bg='seaGreen1', bd=5, command=amount_by_search)
button2.grid(row=7, column=1, pady=10, padx=10)

# Output Frame inside Working
Output = tk.LabelFrame(Working, text='Output', font=('times new roman', 15), bg='grey20', fg='gold', relief='groove', bd=8)
Output.grid(row=0, column=2, pady=2, sticky="nsew")

# Output Area
scrollbar = tk.Scrollbar(Output, orient='vertical')
scrollbar.pack(side='right', fill='y')
textarea = tk.Text(Output, yscrollcommand=scrollbar.set)
textarea.pack(padx=5, pady=10, fill=tk.BOTH, expand=True)
scrollbar.config(command=textarea.yview)

# Feature Window
feature = tk.LabelFrame(window, text='More Features', font=('times new roman', 15, 'bold'), fg='gold', bd=8, relief='groove', bg='gray20')
feature.pack(fill="both", expand=True, padx=4, pady=4)

Month = tk.Label(feature, text='Month', font=('times new roman', 15, 'bold'), fg='white', bg='grey20')
Month.grid(row=0, column=0, padx=5, pady=5)
Month_ENT = tk.Entry(feature, font=('times new roman', 15, 'bold'), bd=5)
Month_ENT.grid(row=0, column=1, pady=5, padx=5)
delete = tk.Label(feature, text='Id', font=('times new roman', 15, 'bold'), fg='white', bg='grey20')
delete.grid(row=1, column=0, padx=5, pady=5)
delete_ENT_id = tk.Entry(feature, font=('times new roman', 15, 'bold'), bd=5)
delete_ENT_id.grid(row=1, column=1, pady=5, padx=5)

button3 = tk.Button(feature, text='Delete Month', font=('times new roman', 15), relief='groove', bd=8, bg='RosyBrown4', fg='black', command=dele)
button3.grid(row=2, column=0, padx=35, pady=5)
button4 = tk.Button(feature, text='Delete Entry', font=('times new roman', 15), relief='groove', bd=8, bg='RosyBrown4', fg='black', command=dele_id)
button4.grid(row=2, column=1, padx=5, pady=5)

Month_total = tk.Label(feature, text='Month', font=('Times new roman', 15, 'bold'), bg='grey20', fg='white')
Month_total.grid(row=0, column=2, padx=15, pady=5)
Month_total_Ent = tk.Entry(feature, font=('Times new roman', 15), bd=5)
Month_total_Ent.grid(row=0, column=3, padx=5, pady=5)

Month_total_Mode = tk.Label(feature, text='Mode', font=('Times new roman', 15, 'bold'), bg='grey20', fg='white')
Month_total_Mode.grid(row=1, column=2, padx=15, pady=5)
Month_total_Mode_Ent = tk.Entry(feature, font=('Times new roman', 15), bd=5)
Month_total_Mode_Ent.grid(row=1, column=3, padx=5, pady=5)

total_cash_button = tk.Button(feature, text='Calc By Mode', font=('times new roman', 15), relief='groove', bd=8, fg='black', bg='green', command=cash_calculate)
total_cash_button.grid(row=2, column=2, padx=15, pady=5, columnspan=2)

# Button frame
buttonFrame = tk.Frame(feature, bd=8, relief='groove')
buttonFrame.grid(row=0, column=4, rowspan=3, padx=50)

total_button = tk.Button(buttonFrame, text='Total', font=('times new roman', 15), relief='groove', bd=5, fg='white', bg='grey20', width=8, pady=10, command=total_amount)
total_button.grid(row=0, column=0, padx=5, pady=5)

clear_button = tk.Button(buttonFrame, text='Clear', font=('times new roman', 15), relief='groove', bd=5, fg='white', bg='grey20', width=8, pady=10, command=clear_output)
clear_button.grid(row=0, column=1, padx=5, pady=20)

# Run the window
window.mainloop()

# Close the database connection when the window is closed
db_connection.close()