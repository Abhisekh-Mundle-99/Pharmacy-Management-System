import tkinter as tk
import tkinter.messagebox as msg
from ctypes import windll

import DBMS
import Login
import Billing


# Main Application Class
class Application(tk.Tk):

    # this variable stores if the application is fullscreen or not
    is_fullscreen = False

    # application's default screen size
    min_height = 680
    min_width = 700

    # application's current screen size is used to correctly position other menus
    cur_height = 680
    cur_width = 700

    # the current position of the application on the screen
    min_posx = 400
    min_posy = 100

    # application name and logo(icon)
    app_name = "CAPS PMS v1.0"
    app_icon = "icon.ico"

    # class initializer
    def __init__(self):
        super().__init__()

        # give a name and logo
        self.title(self.app_name)
        self.iconbitmap(default=self.app_icon)

        # set starting position on the screen (center of the window)
        self.min_posx = int(self.winfo_screenwidth()/2 - self.min_width/2)
        self.min_posy = int(self.winfo_screenheight()/2 - self.min_height/2 - 20)

        # start the application with the default size and position
        self.geometry("{0}x{1}+{2}+{3}".format(self.min_width, self.min_height, -self.min_width, -self.min_height))

        # start the login window for user login
        self.create_login()
        self.update()

        # when user tries to close the application, this function creates a confirmation window
        self.protocol('WM_DELETE_WINDOW', lambda: close_window(self, "Quit " + self.app_name + "?"))

# CALLING DIFFERENT WINDOWS OF PMS
# Launch the Login Form
    def create_login(self):
        Login.LoginForm(self)

# Launch the Search Menu
    def start_search(self):
        DBMS.SearchForm(self)

# View all transactions
    def view_bills(self):
        Billing.Bills(self)

# Launch the Billing Form
    def start_billing(self):
        Billing.BillingForm(self)

# View the inventory
    def view_inventory(self):
        DBMS.DatabaseView(self, "store")

# View Add Product Form
    def add_inventory(self):
        DBMS.DatabaseView(self, "add")

# Check Expired Products
    def check_expired(self):
        DBMS.DatabaseView(self, "expired")

# Launch the Employee Menu
    def view_users(self):
        DBMS.DatabaseView(self, "users")

# This function is for properly resizing the application
    def update(self):
        super(Application, self).update()
        if self.is_fullscreen:
            self.grid(self.cur_width * 0.8, self.cur_height * 0.8)
            # self.main_menu.grid()

# this function is used to properly minimize and maximize the window
    def overrideredirect(self, boolean=None):
        tk.Tk.overrideredirect(self, boolean)
        if boolean:
            hwnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, DBMS.gwl_exstyle)
            style = style & ~DBMS.ws_ex_toolwindow
            style = style | DBMS.ws_ex_appwindow
            res = windll.user32.SetWindowLongW(hwnd, DBMS.gwl_exstyle, style)
        self.wm_withdraw()
        self.wm_deiconify()


# This function opens a dialog box to confirm before closing any window
def close_window(self, message, event=None):
    if msg.askokcancel("Quit", message):
        if event is None:
            try:
                self.destroy()
            except:
                pass
        else:
            try:
                event.widget.destroy()
            except:
                pass


# Confirm Certain Tasks, W/O Password
def confirm_task(self, event=None, message="Please Confirm", req_pass=False):
    # generalized form for a confirmation message
    msg_box = msg.Message(self)
    tk.Label(msg_box, text=message)
    if req_pass:
        tk.Label(msg_box, text="Password")
        password = tk.Entry(msg_box, width=20)
        password.bind("<Return>", DBMS.check)


# Instantiating Application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
