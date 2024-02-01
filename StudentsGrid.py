# Tyler Guldberg
# Caleb Heaps
# Ethan Jacobson
# 5/2/23
# Student Database Group Project

import os
import sqlite3
import tkinter
import tkinter.messagebox


# : Replace 3 student placeholders for a total of ten complete rows


def main():
    # delete previous database for ease of testing
    os.remove('students.db')
    # connect to/create database and create cursor
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    # create student table
    cur.execute('create table Students (student_id text primary key not null, first_name text, last_name text, '
                'student_school text, age text, gender text, height text)')

    # create student table content
    students = [
        ('1', 'Ethan', 'Jacobson', 'SHCC', '17', 'Male', '5ft 9in'),
        ('2', 'Callie', 'Nibbe', 'SHCC', '16', 'Female', '5ft 6in'),
        ('3', 'Vanessa', 'Hobbs', 'SHCC', '21', 'Female', '5ft 11in'),
        ('4', 'Tyler', 'Guldberg', 'SCLA', '18', 'Male', '6ft 0in'),
        ('5', 'Sam', 'Schaefer', 'SCLA', '18', 'Male', '6ft 2in'),
        ('6', 'Milo', 'Gehring', 'SCLA', '18', 'Male', '5ft 7in'),
        ('7', 'Kathy', 'Weigand', 'SCLA', '22', 'Female', '5ft 4in'),
        ('8', 'Alec', 'Bennyhoff', 'UNW', '18', 'Male', '6ft 0in'),
        ('9', 'Noah', 'Bruder', 'UNW', '18', 'Male', '5ft 10in'),
        ('10', 'Haily', 'Beitler', 'UNW', '18', 'Female', '5ft 4in')
    ]
    fields = ['first_name', 'last_name', 'student_school', 'age', 'gender', 'height']
    # add student table content to student table
    cur.executemany('insert into Students values (?, ?, ?, ?, ?, ?, ?)', students)

    # print table contents
    for row in cur.execute('select * from Students'):
        print(row)

    # commit to the database and close it
    conn.commit()
    conn.close()

    class StudentGUI:
        def __init__(self):
            self.main_window = tkinter.Tk()
            self.main_window.title('Student Database Editor')
            self.view_window = tkinter.Tk()
            self.view_window.title('Student Database Viewer')

            # Create frames and row parser
            self.tableFrame = tkinter.Frame(self.view_window)
            self.rowSelectFrame = tkinter.Frame(self.main_window)
            self.fieldSelectFrame = tkinter.Frame(self.main_window)
            self.displayFrame = tkinter.Frame(self.main_window)
            self.rowID = 0

            # Create table
            self.totalRows = len(students)
            self.totalColumns = len(students[0])
            self.num = 1
            for i in fields:
                self.tableTitleLabel = tkinter.Label(self.tableFrame, width=12, text=i)
                self.tableTitleLabel.grid(row=0, column=self.num)
                self.num += 1

            for r in range(self.totalRows):
                for c in range(self.totalColumns):
                    self.tableLabel = tkinter.Label(self.tableFrame, width=12, text=students[r][c])
                    self.tableLabel.grid(row=r + 1, column=c)

            # Create lists of rows and columns and insert items
            self.rowDropdown = tkinter.Listbox(self.rowSelectFrame)
            for i in range(10):
                self.rowDropdown.insert(i, f'{i + 1}')

            self.fieldDropdown = tkinter.Listbox(self.fieldSelectFrame)
            for field in fields:
                self.fieldDropdown.insert(i, field)

            # Create buttons and entry field
            self.changeButton = tkinter.Button(self.fieldSelectFrame, text='Save Changes', command=self.row_update)
            self.quitButton = tkinter.Button(self.fieldSelectFrame, text='Quit', command=self.window_destroy)
            self.changeEntry = tkinter.Entry(self.fieldSelectFrame)
            self.selectButton = tkinter.Button(self.rowSelectFrame, text='Select Row', command=self.row_select_display)

            # Create all labels
            self.rowLabel = tkinter.Label(self.displayFrame, text='')
            self.rowLabel.pack()
            self.rowSelectLabel = tkinter.Label(self.rowSelectFrame, text='')

            # Pack all buttons and entry field
            self.fieldDropdown.grid(row=0, column=1)
            self.changeEntry.grid(row=1, column=1)
            self.quitButton.grid(row=2, column=1, sticky='E')
            self.changeButton.grid(row=2, column=1, sticky='W')

            # Pack row and column list
            self.rowDropdown.pack()
            self.selectButton.pack()

            # Place all frames
            self.tableFrame.grid(row=0, column=0, columnspan=3)
            self.rowSelectFrame.grid(row=0, column=0)
            self.fieldSelectFrame.grid(row=0, column=1)
            self.displayFrame.grid(row=0, column=2)

            tkinter.mainloop()

        def row_update(self):  # Method used for Save Changes button to update selected field with user input
            conn = sqlite3.connect('students.db')
            cur = conn.cursor()

            entry_new = self.changeEntry.get()

            try:
                field_select = self.fieldDropdown.get(self.fieldDropdown.curselection())
            except tkinter.TclError:
                tkinter.messagebox.showerror('TCL Error', message="Please select a field to edit before pressing 'Save Changes' button.")
                return

            row_select = self.rowID  # self.rowDropdown.get(self.rowDropdown.curselection())
            cur.execute(f'UPDATE Students SET {field_select} = "{entry_new}" WHERE student_id = "{row_select}"')
            self.rowLabel.destroy()

            cur.execute(f'SELECT * FROM Students WHERE student_id = "{row_select}"')
            selection = cur.fetchall()
            self.rowLabel = tkinter.Label(self.displayFrame, text=str(selection))
            self.rowLabel.pack()
            cur.execute(f'SELECT * FROM Students')
            students_select = cur.fetchall()
            self.num = 1
            for i in fields:
                self.tableTitleLabel = tkinter.Label(self.tableFrame, width=12, text=i)
                self.tableTitleLabel.grid(row=0, column=self.num)
                self.num += 1

            for r in range(self.totalRows):
                for c in range(self.totalColumns):
                    self.tableLabel = tkinter.Label(self.tableFrame, width=12, text=students_select[r][c])
                    self.tableLabel.grid(row=r + 1, column=c)
            conn.commit()

        def row_select_display(self):  # Method for Select Row button to display row selection
            self.rowSelectLabel.destroy()
            self.rowLabel.destroy()

            conn = sqlite3.connect('students.db')
            cur = conn.cursor()

            try:
                row_select = self.rowDropdown.get(self.rowDropdown.curselection())
            except tkinter.TclError:
                tkinter.messagebox.showerror('TCL Error', message="Please select a row to edit before pressing 'Select Row' button.")
                return

            self.rowID = row_select
            self.rowSelectLabel = tkinter.Label(self.rowSelectFrame, text=f'Row {row_select} is selected')
            self.rowSelectLabel.pack()

            cur.execute(f'SELECT * FROM Students WHERE student_id = "{row_select}"')
            selection = cur.fetchall()
            self.rowLabel = tkinter.Label(self.displayFrame, text=str(selection))
            self.rowLabel.pack()

        def window_destroy(self):
            self.view_window.destroy()
            self.main_window.destroy()

    gui = StudentGUI()


# run main function
if __name__ == '__main__':
    main()
