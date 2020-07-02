import tkinter as tk
from utility import *
import DBMS


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
            DBMS.msg.showerror("Missing Information", "Please select search criteria!")
        if not category_value:
            DBMS.msg.showerror("Missing Information", "Please enter a valid" + category_id
                          + " to search!")
        elif category_id and category_value:
            if search():
                tk.Button(self, label="[+]", command=lambda: DBMS.append_to_cart(self), bg="blue", fg="white")
                tk.Button(self, label="[-]", command=lambda: DBMS.delete_from_cart(self), bg="red", fg="white")
            else:
                if category_id == "name":
                    reason = "named "
                elif category_id == "symptom":
                    reason = "for "
                else:
                    reason = "with " + category_id + " "
                DBMS.msg.showinfo("Search Results", "We did not find any medicines " + reason + category_value)


# Begin Searching with provided category and value
def search(self):
    self.master.confirm_task(self, "Close Search?")
    return True


# Return total Stocks available for this item
def count_stocks(self, med_name):
    if DBMS.login_type == "admin":
        return 0
    else:
        return 1


# Return Expiry Date of given stock
def check_expiry(self, stock_num):
    now = time.localtime()
    cur_date = date(now[0], now[1], now[2])
    return cur_date


# Return True/False whether this stock has expired
def check_expired(self, stock_num):
    return current_date() > check_expiry(self, stock_num)


# Return total Expired Stocks of an item
def count_expired_stocks(self, med_name):
    return 0
