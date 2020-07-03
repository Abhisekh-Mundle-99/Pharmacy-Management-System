from utility import *
from Search import *
import tkinter.messagebox as msg
import tkinter as tk
import sqlite3


total_sales = 4450
total_profit = 2324
turned_down = 0


# there are 3 login types: admin | employee | demo mode
# admins have complete access to all features of this application
# employees have limited access and cannot delete inventory, or manage employee data
# in demo_mode, people can learn all features of the application
login_id = ''
login_type = 'demo'
is_logged_in = False
admin_db = sqlite3.connect("admin.db")
cur_log = admin_db.cursor()
# cur_log.execute("ALTER TABLE log ADD type BOOLEAN DEFAULT TRUE NOT NULL ;")
# admin_db.commit()

columns = ('Sl No', 'Name', 'Type', 'Quantity Left', 'Cost', 'Purpose', 'Expiry Date', 'Rack location', 'Manufacture')
pharm_db = sqlite3.connect("medicine.db")
cur_col = pharm_db.cursor()

# bill processing globals
cart = []
names = []
qty = []
bill_id = 0
bill_accounted = True


""" DATABASE MODIFYING FUNCTIONS """


# Delete Inventory: Only visible to Admin
def dispose(self, med_name, stock_id=None):
    if login_type != "admin":
        self.msg.showerror("You are not authorized to delete inventory!")
        return False
    stocks_state = " "
    confirm_disposal = "Confirm disposal?"
    if stock_id is not None:
        if check_expired(stock_id):
            stocks_state += "Stock no. " + str(stock_id) + " of " + med_name + " has expired!"
        else:
            stocks_state += "Stock no. " + str(stock_id) + " of " + med_name + " has NOT expired yet!"
    else:
        expired = count_expired_stocks(self, med_name)
        stock_count = count_stocks(self, med_name)

        stocks_state += str(expired) + " out of " + str(stock_count) + " stocks of " + med_name + " have expired."
        confirm_disposal = " Dispose ALL or Expired stocks?"
    if self.master.confirm_task(self, stocks_state + confirm_disposal):
        return True
    else:
        return False


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
    pass  # qty.append(qtys.get())


# Change admin password
def change_pass():
    cur_log.execute("update log set password='123' where username = 'admin'")
    admin_db.commit()


# Show summary
def update_summary(self):
    try:
        labels = ["Today's Sales", "Profits", "Turned Down Customers"]
        if total_sales == 0:
            self.sum_sales.config(text="Nothing sold yet!", fg="red")
        else:
            self.sum_sales.config(text="Worth " + str(total_sales) + "₹", fg="green")

        if total_sales == 0:
            self.sum_profits.config(text="Nothing sold yet.", fg="red")
        elif total_profit == 0:
            self.sum_profits.config(text="No earnings yet.", fg="black")
        else:
            self.sum_profits.config(text="Worth " + str(total_profit) + "₹", fg="green")

        if total_sales == 0:
            self.sum_turned.config(text="Nothing sold yet.", fg="red")
        if turned_down == 0:
            self.sum_turned.config(text="No one turned down.", fg="green")
        else:
            self.sum_turned.config(text=str(turned_down) + " customers turned down!", bg="red", fg="black")
    finally:
        return


# Show revenue
def show_rev(self):  # opens revenue window---------------TOTAL REVENUE
    labels = ('cus_name', 'cus_add', 'items', 'Total_cost', 'bill_dt', 'bill_no', 'bill', 'val_id')
    flag = 'rev'
    total = 0.0
    today = str(time.localtime()[2]) + '/' + str(time.localtime()[1]) + '/' + str(time.localtime()[0])
    tk.Label(self, text='Today: ' + today).grid(row=0, column=0)
    cur_col.execute('select * from bills')
    for i in cur_col:
        if i[4] == today:
            total += float(i[3])
    print(total)
    tk.Label(self, width=22, text='Total revenue: Rs ' + str(total), bg='black', fg='white').grid(row=1, column=0)
    cx = 0
    vsb = tk.Scrollbar(orient='vertical')
    lb1 = tk.Listbox(self, width=25, yscrollcommand=vsb.set)
    vsb.grid(row=2, column=1, sticky=tk.NS)
    lb1.grid(row=2, column=0)
    vsb.config(command=lb1.yview)
    cur_col.execute("select * from bills")
    for i in cur_col:
        if i[4] == today:
            cx += 1
            lb1.insert(cx, 'Bill No.: ' + str(i[5]) + '    : Rs ' + str(i[3]))
    pharm_db.commit()
    tk.Button(self, text='Main Menu', command=self.close).grid(row=15, column=0)

