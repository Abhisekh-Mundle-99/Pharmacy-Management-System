import tkinter as tk
import tkinter.messagebox as msg
from datetime import date
import time
import sqlite3
import tempfile
import win32api
import win32print

"""Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                      widget stick to the cell boundary
        """

login_id = ''
login_type = ''
# two login types: admin | employee
# employees cannot delete inventory
admin_db = sqlite3.connect("admin.db")
cur_log = admin_db.cursor()

columns = ('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
pharm_db = sqlite3.connect("medicine.db")
cur_col = pharm_db.cursor()

# bill processing globals
cart = []
names = []
qty = []
bill_id = 0


""" STATIC UTILITY FUNCTIONS """


# Get Current Date: Used to mark Bills, and check Expiry
def current_date():
    now = time.localtime()
    cur_date = date(now[0], now[1], now[2])
    return cur_date


# Print temporary file to disk
def print_file():
    win32api.ShellExecute(0, "print", B, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)


""" LOGIN FORM CLASS : REDIRECTS TO ADMIN OR EMPLOYEE """


class LoginForm(tk.Toplevel):
<<<<<<< HEAD
    username_Entry = None
    password_Entry = None
=======
    username_entry = None
    password_entry = None
>>>>>>> c498a8521394e90cfcca83ba839b090787d392cc
    is_logged_in = False
    def __init__(self, master, bg='white', fg='black'):

        super().__init__()

        self.master = master

        self.title("Login")
        self.geometry("400x150")

        tk.Label(self, text="YOUR WORKSPACE", bg="cyan4", fg="white", font="Arial 25").pack(fill=tk.BOTH, expand=1)
        tk.Label(self, text="Login ID").pack(fill=tk.BOTH, expand=1)
<<<<<<< HEAD
        self.username_Entry = tk.Entry(self, bg=bg, fg=fg)
        self.username_Entry.pack(fill=tk.BOTH, expand=0)
        tk.Label(self, text="Password").pack(fill=tk.BOTH, expand=1)
        self.password_Entry = tk.Entry(self, bg=bg, fg=fg)
        self.password_Entry.pack(fill=tk.BOTH, expand=0)
=======
        self.username_entry = tk.Entry(self, bg=bg, fg=fg)
        self.username_entry.pack(fill=tk.X, expand=0)
        tk.Label(self, text="Password").pack(fill=tk.BOTH, expand=1)
        self.password_entry = tk.Entry(self, bg=bg, fg=fg)
        self.password_entry.pack(fill=tk.X, expand=0)
>>>>>>> c498a8521394e90cfcca83ba839b090787d392cc

        self.submit_button = tk.Button(self, text="Login", command=self.submit, bg="pink").pack(fill=tk.X)
        #self.submit_button = tk.Button(self, text="Demo", command=demo, bg="orange").pack(fill=tk.X)

# Submit Button's function to collect uID, pass, perform checks, and highlight issues
    def submit(self):
<<<<<<< HEAD
        username = self.username_Entry.get()
        password = self.password_Entry.get()

        if not username:
            self.username_Entry.configure(bg="red", fg="white")
        elif not password:
            self.password_Entry.configure(bg="red", fg="white")
        elif username and password:
            if not check(self):
                self.username_Entry.configure(bg="red", fg="white")
                self.password_Entry.configure(bg="red", fg="white")
            else:
                self.username_Entry.configure(bg="green", fg="white")
                self.password_Entry.configure(bg="green", fg="white")
=======
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username:
            self.username_entry.configure(bg="red", fg="white")
        elif not password:
            self.password_entry.configure(bg="red", fg="white")
        elif username and password:
            if not check(self):
                self.username_entry.configure(bg="red", fg="white")
                self.password_entry.configure(bg="red", fg="white")
            else:
                self.username_entry.configure(bg="green", fg="white")
                self.password_entry.configure(bg="green", fg="white")
>>>>>>> c498a8521394e90cfcca83ba839b090787d392cc
                tk.Label(self.master, text="Welcome", bg="cyan4", fg="white", font="Arial 25").pack(fill=tk.BOTH, expand=1)
                #if login_type == "admin":
                    #self.master.admin_panel = AdminPanel(self.master)
                try:
                    self.destroy()
                except:
                    pass


""" DATABASE LOOKUP FUNCTIONS """


# MEDICINE & STOCK SEARCH FORM: EXPIRED STOCKS ARE UNLISTED FOR EMPLOYEES
class SearchForm(tk.Toplevel):
    def __init__(self, master, bg='white', fg='black'):
        super().__init__()

        self.master = master

        self.title("Search Options")
        self.geometry("300x150")

        tk.Label(self, text="Search by - ").pack(fill=tk.BOTH, expand=1)
        self.category_name = tk.Spinbox(self, bg=bg, fg=fg).pack(fill=tk.BOTH, expand=1)
        self.category_value = tk.Entry(self, bg=bg, fg=fg).pack(fill=tk.BOTH, expand=1)
        self.submit_button = tk.Button(self, text="Submit", command=self.submit).pack(fill=tk.X)
        self.search_results = tk.Listbox(self, bg=fg, fg=bg).pack(fill=tk.BOTH, expand=1)

# Submit Button's function to collect input for search & highlight problems
    def submit(self):
        category_id = self.category_name.get()
        category_value = self.category_value.get()

        if not category_id:
            msg.showerror("Missing Information", "Please select search criteria!")
        if not category_value:
            msg.showerror("Missing Information", "Please enter a valid" + category_id
                          + " to search!")
        elif category_id and category_value:
            if self.search():
                tk.Button(self, label="[+]", command=lambda: append_to_cart(self), bg="blue", fg="white")
                tk.Button(self, label="[-]", command=lambda: delete_from_cart(self), bg="red", fg="white")
            else:
                if category_id == "name":
                    reason = "named "
                elif category_id == "symptom":
                    reason = "for "
                else:
                    reason = "with " + category_id + " "
                msg.showinfo("Search Results", "We did not find any medicines " + reason + category_value)


# User Login & Password Confirmation
def check(self):
    global login_id, login_type
    if self.is_logged_in:
        # If already logged in, this function checks password
        # to confirm some regrettable actions like deleting inventory.
        # The comment below stops IDE warning "login_id might not have any value"
        # noinspection PyUnboundLocalVariable
        cur_log.execute("select * from log where username='%s' and password='%s'"
<<<<<<< HEAD
                        % (login_id, self.password_Entry.get()))
=======
                        % (login_id, self.password_entry.get()))
>>>>>>> c498a8521394e90cfcca83ba839b090787d392cc
        admin_db.commit()
        # confirm password for logged-in admin
        if cur_log.fetchone() is not None:
            return True
        else:
            return False
    else:
<<<<<<< HEAD
        login_id = self.username_Entry.get()
        cur_log.execute("select * from log where username='%s' and password='%s'"
                        % (login_id, self.password_Entry.get()))
=======
        login_id = self.username_entry.get()
        cur_log.execute("select * from log where username='%s' and password='%s'"
                        % (login_id, self.password_entry.get()))
>>>>>>> c498a8521394e90cfcca83ba839b090787d392cc
        admin_db.commit()
        if cur_log.fetchone() is not None:
            self.is_logged_in = True
            return True
        else:
            login_type = cur_log.fetchone()[2]
            return False


# Begin Searching with provided category and value
def search(self):
    self.master.confirm_task(self, "Close Search?")
    return True


# Return Expiry Date of given stock
def check_expiry(self, stock_num):
    now = time.localtime()
    cur_date = date(now[0], now[1], now[2])
    return cur_date


# Return True/False whether this stock has expired
def check_expired(self, stock_num):
    return current_date() > check_expiry(self, stock_num)


""" DATABASE MODIFYING FUNCTIONS """


# Delete Inventory: Only visible to Admin
def dispose(self, med_name, stock_num=None):
    if login_type != "admin":
        self.msg.showerror("You are not authorized to delete inventory!")
        return False
    stocks_state = " "
    confirm_disposal = "Confirm disposal?"
    if stock_num:
        if check_expired(stock_num):
            stocks_state += "Stock no. " + str(stock_num) + " of " + med_name + " has expired!"
        else:
            stocks_state += "Stock no. " + str(stock_num) + " of " + med_name + " has NOT expired yet!"
    else:
        expired = count_expired_stocks(self, med_name)
        stock_count = count_stocks(self, med_name)

        stocks_state += expired + " out of " + stock_count + " stocks of " + med_name + " have expired."
        confirm_disposal = " Dispose ALL or Expired stocks?"
    if self.master.confirm_task(self, stocks_state + confirm_disposal):
        return True
    else:
        return False


# BILLING SYSTEM
class BillingForm(tk.Toplevel):
    def __init__(self, master, bg='white', fg='black'):
        super().__init__()

        self.master = master

        self.title("Billing")
        self.geometry("500x600+{0}+{1}".format(int(self.winfo_screenwidth()/2), int(self.winfo_screenheight())))

        t = 0
        names = []
        qty = []
        sl = []
        n = []
        qtys = [''] * 10

        cur_col.execute("select * from med")
        for i in cur_col:
            n.append(i[1])
        pharm_db.commit()

        tk.Label(self, text="BILLING SYSTEM", bg="cyan4", fg="white", font="Arial 25").pack(fill=tk.BOTH, expand=1)

        tk.Label(self, text='Customer Name: ').pack()
        self.name = tk.Entry(self, bg=bg, fg=fg).pack()

        self.protocol('WM_DELETE_WINDOW', self.close_bill)
        tk.Button(self, width=15, text='Add Valued Customer', command=self.add_valued).pack()
        tk.Button(self, width=15, text='Reset Bill', command=self.clear_bill).pack()
        tk.Button(self, width=15, text='Print Bill', command=lambda: self.print_file(bill)).pack()
        tk.Button(self, width=15, text='Save Bill', command=self.make_bill).pack()

        tk.Label(self, text='Enter phone: ').pack()
        self.phone = tk.Entry(self, bg=bg, fg=fg).pack()
        # self.phone.bind('<Return>', self.check_valued)

        tk.Label(self, text="Valued", bg="grey", fg="white").pack()

        tk.Label(self, text='-' * 115).pack()
        tk.Label(self, text='SELECT PRODUCT', width=25, relief='ridge').pack()
        tk.Label(self, text=' RACK  QTY LEFT     COST          ', width=25, relief='ridge').pack()
        tk.Label(self, text='QUANTITY', width=20, relief='ridge').pack()
        qtys = tk.Entry(self).pack()

# Clear all data in the Billing Form
    def clear_bill(self):
        # reset text file to prevent misprint
        # clear content of data-entry widgets
        # reset menu flags
        self.master.confirm_task("Trash this Bill?")

# Prepare a printable Bill text file
    def make_bill(self):
        global bill_id
        if bill_id != 0:
            bill_id += 1
        else:
            cur_col.execute("select bill_id from bills")
            #if cur_col.fetchall():
            #    bill_id =
            #else:
            #    bill_id = 0;
        pass

# Close the Billing Menu
    def close_bill(self):
        if self.bill_accounted() or self.close_window(self, "Reset this Bill?"):
            self.clear_bill()
        # if transaction billed, account it >> clear bill >> close menu
        try:
            self.destroy()
        except:
            pass

# Check if the Bill is being made for a Valued Customer
    def check_valued(self):
        name = self.name.get()
        phone = self.phone.get()

        if not name:
            self.name.configure(bg="red", fg="white")
        elif not phone:
            self.phone.configure(bg="red", fg="white")
        else:
            cur_log.execute("select * from cus where name='%s' and phone='%s' and valued='%s'"
                            % (name, phone, True))
            pharm_db.commit()
            if cur_log.fetchone() is not None:
                self.valued.configure(bg="green", fg="white")
                return true
            else:
                self.valued.configure(bg="red", fg="white")
        return false

# Add the customer getting billed, as new Valued Customer
    def add_valued(self):
        name = self.name.get()
        phone = self.phone.get()

        if not name:
            self.name.configure(bg="red", fg="white")
        elif not phone:
            self.phone.configure(bg="red", fg="white")
        else:
            cur_col.execute("select * from cus where phone='%s'")
            if cur_col.fetchone() is not None:
                for i in cur_col:
                    if i[2]:
                        if i[0] != name:
                            self.phone.configure(bg="red", fg="white")
                            self.msg.showerror("Phone number already registered under another name!")
                            return False
                        else:
                            self.name.configure(bg="green", fg="white")
                            self.phone.configure(bg="green", fg="white")
                            self.msg.showerror("Already a valued customer!")
                            return False
                if self.master.confirm_task(self, "Make " + name + " a valued customer?"):
                    cur_col.execute("update cus set valued=? where phone = (?,?,?)", (name, phone, value))
            else:
                if self.master.confirm_task(self, "Add " + name + " as a new valued customer?"):
                    cur_col.execute("modify into cus values(?,?,?)", (name, phone, value))
            pharm_db.commit()
        return false


""" BACKGROUND TRANSACTION HANDLERS """
# These functions are active from outside the billing class.
# Their function is to modify the cart variable as the user
# selects or deselects items from other menus like search results.
# It has nothing to do with how the bill is made


# Mark items for next Bill
def append_to_cart(self):
    cart.append(self.search_results.cur_selection()[1])


# Remove items from Bill
def delete_from_cart(self):
    cart.remove(self.search_results.cur_selection()[1])


# Preparing Bill for transaction, performing calculations, storing in database etc
def prepare_bill(self):
    qty.append(qtys.get())


#spc function
def change_pass(password):
    cur_log.execute("update log set password=? where username = 'admin'", password)
    admin_db.commit()
