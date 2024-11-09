import tkinter as tk 

window = tk.Tk()
window.geometry("1270x685")
window.title("Expense Tracker")
# For inserting the icon into the window 
window.iconbitmap("icon.ico")

# Here i create a Heading 
heading = tk.Label(window , text='Expense Tracker Application' , font=('times new roman', 30 , 'bold')  ,bg='gray20', fg='gold' , relief='ridge')
heading.pack(fill= tk.X)

# This the working frame (Middle Frame in the application)
Working=tk.Frame(window)
Working.pack(pady=5) 

# This the Insert data frame which is inside the working frame 
Input=tk.LabelFrame(Working , text='Input' , font=('times new roman',15) , bg='grey20' , fg='gold' , relief='groove',bd=8 )
Input.grid(row=0 , column=0 )

# This part is the label part Month_year 
Table_Name = tk.Label(Input , text='Month_Year' , font=('times new roman',15 ) , bg='grey20' , fg='white')
Table_Name.grid(row=0 , column=0)
# This part is the entry part of month year 
Table_Name_entry= tk.Entry(Input ,font=('times new roman',15),bd=5)
Table_Name_entry.grid(row=0 , column=1 , pady=9)

# This part contain the label of Day
Day = tk.Label(Input , text='Day' , font=('times new roman',15 ) , bg='grey20' , fg='white')
Day.grid(row=1 , column=0)
# This is the entry field of date 
Day= tk.Entry(Input ,font=('times new roman',15),bd=5)
Day.grid(row=1 , column=1, pady=9)

# This is the label part of the amount
Amount=tk.Label(Input,text='Amount',font=('times new roman',15) , fg='white' , bg='grey20')
Amount.grid(row=2 , column=0)
# This is the entry part of the amount 
Amount=tk.Entry(Input, font=('times new roman',15,'bold') , bd=5 )
Amount.grid(row=2 , column=1 , pady=9)

# Mode of transection 
Mode_of_tracs=tk.Label(Input , text='Mode' , font=('times new roman',15),fg='white', bg='grey20')
Mode_of_tracs.grid(row=3,column=0)
Mode_of_tracs=tk.Entry(Input  , font=('times new roman',15,'bold'), bd=5)
Mode_of_tracs.grid(row=3,column=1 ,pady=9)

# Remark Area 
Remark=tk.Label(Input,text='Remark',font=('times new roman' ,15),fg='white' ,bg='grey20')
Remark.grid(row=4,column=0)
Remark=tk.Entry(Input, font=('times new roman',15,'bold'), bd=5)
Remark.grid(row=4,column=1)

# Submit button 
button1=tk.Button(Input , text='Submit' , font=('times new roman ', 15) , fg='black' ,bg='green' , bd=5)
button1.grid(row=5 , column=2, pady=9 , padx=9)

# Search frame 
Search=tk.LabelFrame(Working , text='Search' , font=('times new roman',15) , bg='grey20' , fg='gold' , relief='groove',bd=8 )
Search.grid(row=0 , column=1 )

Table_Name = tk.Label(Search , text='Month_Year' , font=('times new roman',15 ) , bg='grey20' , fg='white')
Table_Name.grid(row=0 , column=0)
# This part is the entry part of month year 
Table_Name_entry= tk.Entry(Search ,font=('times new roman',15),bd=5)
Table_Name_entry.grid(row=0 , column=1 , pady=9)

Day=tk.Label(Search, text='Date' , font=('times new roman' , 15 ) , fg='white' , bg='grey20')
Day.grid(row=1,column=0)
Day=tk.Entry(Search, font=('times new roman' , 15 , 'bold' ) , bd=5)
Day.grid(row=1,column=1 , pady=9)


Amount=tk.Label(Search, text='Amount' , font=('times new roman' , 15 ) , fg='white' , bg='grey20')
Amount.grid(row=2,column=0)
Amount=tk.Entry(Search, font=('times new roman' , 15 , 'bold' ) , bd=5)
Amount.grid(row=2,column=1 , pady=9)

button2=tk.Button(Search , text='Search' , font=('times new roman ', 15) , fg='black' ,bg='light blue' , bd=5)
button2.grid(row=3 , column=2, pady=9 , padx=9)
window.mainloop()