import tkinter as tk 
from tkinter import messagebox 
import mysql.connector as mycon

connection = mycon.connect(
    host="localhost",
    user="root",
    password="lolu123",
    database="mydatabase"
)
# create a cursor
cur = connection.cursor(buffered=True)
try:
    cur.execute("use mydatabase")
except:
    cur.excute("create database if not exists expenscetrackerdb")
    cur.excute("use mydatabase")


# Create new table 
def new():
    table_name = Table_Name_entry.get()
    
    if table_name:  # Check if a table name is provided
        try:
            cur.execute(f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    day DATE,
                    amount FLOAT(7,2),
                    mode VARCHAR(20),
                    remark VARCHAR(100)
                )
            """)
            connection.commit()  # Save changes
            messagebox.showinfo("Notice","New table has been created successfully....")
            Table_Name_entry.delete(0,tk.END)
            Month_table.focus_set()

            print("Create successfully")
        except mycon.Error as err:
            messagebox.showerror("Error", f"Error: {err}")

# Insert Information 
def insert():
    try:
        # Get the table name from user input
        table_name = Month_table.get()
        
        # Define the SQL query with placeholders for parameters
        query = f"INSERT INTO `{table_name}`(day, amount, mode, remark) VALUES (%s, %s, %s, %s)"
        
        # Get the user inputs for the values
        values = (Day_entry.get(), Amount_entry.get(), Mode_of_tracs_entry.get(), Remark_entry.get())
        
        # Execute the parameterized query
        cur.execute(query, values)
        
        # Commit the transaction
        connection.commit()
        messagebox.showinfo("Notice","Data Inserted Successfully...")
        Month_table.delete(0,tk.END)
        Day_entry.delete(0,tk.END)
        Amount_entry.delete(0,tk.END)
        Mode_of_tracs_entry.delete(0,tk.END)
        Remark_entry.delete(0,tk.END)
        Month_table.focus_set()
        print("Data inserted successfully.")
        
    except Exception as e:
        # Print the error if it occurs
        print("An error occurred:", e)

# Delete table 
def dele():
    cur.execute(f"drop table `{Month_ENT.get()}` ")
    connection.commit()
    messagebox.showinfo("Message","Delete Entry Successfully")
    Month_ENT.delete(0,tk.END)
    Month_ENT.focus_set() 
    print("Delete Succesfully")

# Delete table entry 
def dele_id():
    temp1 = Month_ENT.get()
    temp2 = delete_ENT_id.get()
    try:
       qur=f"delete from `{temp1}` where id = %s"
       cur.execute(qur,(temp2,))
       connection.commit()
       messagebox.showinfo("Notice","Delete Successfully...")
       Month_ENT.delete(0,tk.END)
       delete_ENT_id.delete(0,tk.END)
       delete_ENT_id.focus_set()
    except mycon.Error:
        messagebox.showinfo("Warning","Error")
            
# Show list of table in our database 
def show_table():
    if connection :
        cur.execute("show tables")
        tables = cur.fetchall()
        textarea.delete("1.0", tk.END)  # Clear previous output
        for table in tables:
            textarea.insert(tk.END, table[0] + "\n")

# Show the all entry in the particular table 
def show_table_data():
    if connection :
        show_table_name = Month_Name_Entry.get() 
        cur.execute(f"select * from `{show_table_name}`")
        row = cur.fetchall()
        textarea.delete("1.0",tk.END)
        if not row :
            textarea.insert(tk.END,"No Data \n")
        for x in row:
            row_str = " | ".join(map(str, x))  # Convert row elements to strings and join them
            textarea.insert(tk.END, row_str + "\n")
       
# search something using id 
def search_by_id():
    # Fetch input values from Tkinter Entry widgets
    month_name = Month_Name_Entry.get().strip()
    day_value = Day_entry_search.get().strip()
    
    try:
        query = f"SELECT * FROM `{month_name}` WHERE day = %s"
        cur.execute(query, (day_value,))
        rows = cur.fetchall()
        textarea.delete("1.0", tk.END)
        if not rows:
            textarea.insert(tk.END, "No Entry\n")
        else:
            for row in rows:
                row_str = " | ".join(map(str, row))  # Convert row elements to strings
                textarea.insert(tk.END, row_str + "\n")
    
    except mycon.Error as e:
        # Handle SQL errors
        textarea.delete("1.0", tk.END)
        textarea.insert(tk.END, f"Database Error: {e}\n")

# clear the output window  
def clear_output():
    textarea.delete("1.0",tk.END)

# This function give the total amount 
def total_amount():
    total_table=Month_total_Ent.get()
    cur.execute(f"select SUM(amount) as Total_Amount from `{total_table}`") 
    textarea.delete("1.0",tk.END)
    row = cur.fetchall()
    textarea.insert(tk.END,row  )

# search entry according to their name 
def amount_by_search():
    month_name = Month_Name_Entry.get().strip()
    amount_value = Amount_entry_search.get()
    
    try:
        query = f"SELECT * FROM `{month_name}` WHERE amount = %s"
        cur.execute(query, (amount_value,))
        rows = cur.fetchall()
        textarea.delete("1.0", tk.END)
        if not rows:
            textarea.insert(tk.END, "No Entry\n")
        else:
            for row in rows:
                row_str = " | ".join(map(str, row))  # Convert row elements to strings
                textarea.insert(tk.END, row_str + "\n")
                
    
    except mycon.Error as e:
        # Handle SQL errors
        textarea.delete("1.0", tk.END)
        textarea.insert(tk.END, f"Database Error: {e}\n")

# This function calculate the total cash payment 
def cash_calculate():
    month_cash = Month_total_Ent.get()
    mode_cash = Month_total_Mode_Ent.get()
    textarea.delete("1.0",tk.END)
    q=(f"select SUM(amount) as total_cash from `{month_cash}` where mode =%s")
    cur.execute(q,(mode_cash,))
    row = cur.fetchall()
    textarea.insert(tk.END , row)

# This function calculate the total online payment 
def online_calculate(): 
    month_online= Month_total_Ent.get()
    mode_online=Month_total_Mode_Ent.get()
    textarea.delete("1.0",tk.END)
    qur=f"select SUM(amount) as total_online from `{month_online}` WHERE mode =%s"
    cur.execute(qur,(mode_online,))
    row = cur.fetchall()
    textarea.insert(tk.END , row)


# Initialize window
window = tk.Tk()
window.geometry("1270x725")
window.title("Expense Tracker")

# Set window icon
window.iconbitmap("icon.ico")

# Heading
heading = tk.Label(window, text='Expense Tracker Application', font=('times new roman', 30, 'bold'), bg='gray20', fg='gold', relief='ridge')
heading.pack(fill="both", ipady=8 )

# Working frame (middle section of the application)
Working = tk.Frame(window)
Working.pack( fill=tk.BOTH, expand=True)

# Set column configuration for equal width distribution within Working frame
Working.grid_columnconfigure(0, weight=1, uniform="equal")
Working.grid_columnconfigure(1, weight=1, uniform="equal")
Working.grid_columnconfigure(2, weight=1, uniform="equal")

# Input Frame inside Working
Input = tk.LabelFrame(Working, text='Input', font=('times new roman', 15), bg='grey20', fg='gold', relief='groove', bd=8)
Input.grid(row=0, column=0,padx=2 ,  sticky="nsew")

# Month/Year Label and Entry
Table_Name = tk.Label(Input, text='New Month', font=('times new roman', 15), bg='grey20', fg='white')
Table_Name.grid(row=0, column=0, padx=5, pady=5)
Table_Name_entry = tk.Entry(Input, font=('times new roman', 15), bd=5)
Table_Name_entry.grid(row=0, column=1, pady=5)

create_table = tk.Button(Input , text='Create New' , font=('times new roman' , 15) , bd=8 , bg='DeepSkyBlue2' , fg='black' , command=new ) 
create_table.grid(row= 1 , column=1 , padx=5 , pady=10)

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
button1 = tk.Button(Input, text='Submit', font=('times new roman', 15), fg='black', bg='lawn green', bd=5 , command=insert)
button1.grid(row=7, column=1, pady=10, padx=10)

# Search Frame inside Working
Search = tk.LabelFrame(Working, text='Search', font=('times new roman', 15), bg='grey20', fg='gold', relief='groove', bd=8)
Search.grid(row=0, column=1, padx=2 , sticky="nsew")

# Search Frame Content
Table_Name_search = tk.Label(Search, text='All Month', font=('times new roman', 15), bg='grey20', fg='white')
Table_Name_search.grid(row=0, column=0, padx=5, pady=15)
button3=tk.Button(Search , text='Show' , font=('times new roman', 15) , relief='groove',bd=5, bg='RosyBrown3' , fg='black',command=show_table)
button3.grid(row=0 , column=1 , padx=2 , pady=15 )

Month_Name=tk.Label(Search , text='Month Name' , font=('times new roman' , 15 ) , bg='grey20',fg='white')
Month_Name.grid( row=2 , column=0 , padx=5 , pady=5 )
Month_Name_Entry=tk.Entry(Search ,font=('times new roman',15),bd=5)
Month_Name_Entry.grid(row=2,column=1,pady=5 ,padx=5)

button4=tk.Button(Search , text='search' , font=('times new roman', 15) , relief='groove', bd=8 , bg='seaGreen1' , fg='black',command=show_table_data)
button4.grid(row=3 , column=1 , padx=5 , pady=5 )

Day_search = tk.Label(Search, text='Date', font=('times new roman', 15), fg='white', bg='grey20')
Day_search.grid(row=4, column=0, padx=5, pady=5)
Day_entry_search = tk.Entry(Search, font=('times new roman', 15, 'bold'), bd=5)
Day_entry_search.grid(row=4, column=1, pady=5,padx=5)

button4=tk.Button(Search , text='search' , font=('times new roman', 15) , relief='groove', bd=8 , bg='seaGreen1' , fg='black',command=search_by_id)
button4.grid(row=5 , column=1 , padx=5 , pady=5 )

Amount_search = tk.Label(Search, text='Amount', font=('times new roman', 15), fg='white', bg='grey20')
Amount_search.grid(row=6, column=0, padx=5, pady=5)
Amount_entry_search = tk.Entry(Search, font=('times new roman', 15, 'bold'), bd=5)
Amount_entry_search.grid(row=6, column=1, pady=5,padx=5)

button2 = tk.Button(Search, text='Search', font=('times new roman', 15), fg='black', bg='seaGreen1', bd=5 , command=amount_by_search)
button2.grid(row=7, column=1, pady=10, padx=10)

# Output Frame inside Working
Output = tk.LabelFrame(Working, text='Output', font=('times new roman', 15), bg='grey20', fg='gold', relief='groove', bd=8)
Output.grid(row=0, column=2, pady=2, sticky="nsew")

# Output Area
scrollbar=tk.Scrollbar(Output , orient='vertical')
scrollbar.pack(side='right',fill='y')
textarea = tk.Text(Output,yscrollcommand=scrollbar.set )
textarea.pack(padx=5, pady=10)
scrollbar.config(command=textarea.yview)

# Feature Window 
feature= tk.LabelFrame(window , text='More Feature', font=('times new roman',15,'bold'), fg='gold' , bd=8 , relief='groove', bg='gray20' )
feature.pack(fill="both", expand=True)

window.rowconfigure(0, weight=1)  # Allow the feature frame to stretch vertically
window.columnconfigure(0, weight=1)  # Allow the feature frame to stretch horizontally

Month=tk.Label(feature , text='Month' , font=('times new roman', 15 , 'bold') , fg='white', bg='grey20')
Month.grid(row=0 , column=0 , padx=5 , pady=5 )
Month_ENT=tk.Entry(feature , font=('times new roman', 15 ,'bold'), bd=5)
Month_ENT.grid(row=0 , column=1, pady=5, padx=5)
delete=tk.Label(feature , text='Id' , font=('times new roman', 15 , 'bold') , fg='white', bg='grey20')
delete.grid(row=1 , column=0 , padx=5 , pady=5 )
delete_ENT_id=tk.Entry(feature , font=('times new roman', 15 ,'bold'), bd=5)
delete_ENT_id.grid(row=1 , column=1, pady=5, padx=5)

button3=tk.Button(feature , text='Delete Month' , font=('times new roman', 15) , relief='groove', bd=8 , bg='RosyBrown4' , fg='black' , command=dele)
button3.grid(row=2 , column=0 , padx=35 , pady=5 )
button4=tk.Button(feature , text='Delete Entry' , font=('times new roman', 15) , relief='groove', bd=8 , bg='RosyBrown4' , fg='black' , command=dele_id)
button4.grid(row=2 , column=1 , padx=5 , pady=5 )

Month_total = tk.Label(feature , text='Month', font=('Times new roman',15,'bold') , bg='grey20',fg='white')
Month_total.grid(row=0 , column=2 ,padx=15,pady=5)
Month_total_Ent = tk.Entry(feature , font=('Times new roman',15),bd=5)
Month_total_Ent.grid(row=0 , column=3 ,padx=5,pady=5)

Month_total_Mode = tk.Label(feature , text='Mode', font=('Times new roman',15,'bold') , bg='grey20',fg='white')
Month_total_Mode.grid(row=1 , column=2 ,padx=15,pady=5)
Month_total_Mode_Ent = tk.Entry(feature , font=('Times new roman',15),bd=5)
Month_total_Mode_Ent.grid(row=1 , column=3 ,padx=5,pady=5)

total_cash_button = tk.Button(feature,text='Cash',font=('times new roman',15) , relief='groove', bd=8 , fg='black' , bg='green', command=cash_calculate )
total_cash_button.grid(row=2 , column=2 , padx=15 , pady=5)

total_online_button=tk.Button(feature,text='Online',font=('times new roman',15) , relief='groove', bd=8 , fg='black' , bg='lawn green', command=online_calculate)
total_online_button.grid(row=2 , column=3 , padx=15 , pady=10)

# Button frame 
buttonFrame=tk.Frame(feature , bd=8 , relief='groove')
buttonFrame.grid(row=0 , column=4 , rowspan=3,padx=50)

total_button=tk.Button(buttonFrame,text='Total',font=('times new roman',15) , relief='groove', bd=5 , fg='white' , bg='grey20',width=8 , pady=10 , command=total_amount)
total_button.grid(row=0 , column=0 , padx=5 , pady=5)

email_button = tk.Button(buttonFrame,text='Print',font=('times new roman',15) , relief='groove', bd=5 , fg='white' , bg='grey20',width=8 , pady=10 )
email_button.grid(row=0 , column=1 ,pady=20 , padx=5)

print_button=tk.Button(buttonFrame,text='Email',font=('times new roman',15) , relief='groove', bd=5 , fg='white' , bg='grey20',width=8 , pady=10 )
print_button.grid(row=0 , column=2 , padx=5 , pady=20)

clear_button=tk.Button(buttonFrame,text='Clear',font=('times new roman',15) , relief='groove', bd=5 , fg='white' , bg='grey20',width=8 , pady=10 , command=clear_output )
clear_button.grid(row=0 , column=3 , padx=5 , pady=20)

# Run the window
window.mainloop() 
