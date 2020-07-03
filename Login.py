import tkinter as tk
from ctypes import windll
from utility import *
from MainMenu import *
import DBMS

""" LOGIN FORM CLASS : REDIRECTS TO ADMIN OR EMPLOYEE """

gwl_exstyle = -20
ws_ex_appwindow = 0x00040000
ws_ex_toolwindow = 0x00000080


class LoginForm(tk.Tk):
    username_entry = None
    password_entry = None

    def overrideredirect(self, boolean=None):
        tk.Tk.overrideredirect(self, boolean)
        if boolean:
            hwnd = windll.user32.GetParent(self.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, gwl_exstyle)
            style = style & ~ws_ex_toolwindow
            style = style | ws_ex_appwindow
            res = windll.user32.SetWindowLongW(hwnd, gwl_exstyle, style)
        self.wm_withdraw()
        self.wm_deiconify()

    def __init__(self, master):
        super().__init__()

        bg_header = "#008080"
        bg_banner = "#00222D"
        bg = "#008E8E"
        fg = "black"

        self.master = master
        self.update_idletasks()
        self.overrideredirect(True)
        self.title("Login")
        x = self.master.min_posx + int(self.master.winfo_width() / 2 - 200)
        y = self.master.min_posy + int(self.master.winfo_height() / 2 - 125)
        self.geometry("400x250+%d+%d" % (x, y))
        self.config(bg=bg)

        tk.Frame(self, bg="teal").pack(fill=tk.BOTH, expand=True)
        tk.Label(self, text="CAPS PHARMACY", bg=bg_header, fg="White",
                 font="Arial 25").pack(fill=tk.X, expand=False)
        tk.Label(self, text="  Asansol Budha More, Paschim Burdwan, WB  ",
                 bg=bg_banner, fg="White").pack(fill=tk.X)
        tk.Frame(self, bg=bg).pack(fill=tk.Y, expand=True)

        tk.Label(self, text="Login ID", bg=bg).pack(fill=tk.X)
        self.username_entry = tk.Entry(self, fg=fg, width=40)
        self.username_entry.pack(fill=tk.NONE)
        self.username_entry.focus_force()

        tk.Label(self, text="Password", bg=bg).pack(fill=tk.X)
        self.password_entry = tk.Entry(self, fg=fg, width=40)
        self.password_entry.pack(fill=tk.NONE)
        self.username_entry.bind('<Return>', lambda event: self.password_entry.focus())
        self.password_entry.bind('<Return>', self.submit)
        self.password_entry.bind('<Shift-Return>', lambda event: self.username_entry.focus())

        buttons = tk.Frame(self, bg=bg)

        tk.Frame(buttons, bg=bg).pack(in_=buttons, fill=tk.X, expand=True, side=tk.LEFT)
        self.submit_button = tk.Button(self, text="   Login   ", command=self.submit, bg="orange")
        self.submit_button.pack(in_=buttons, side=tk.LEFT)
        tk.Frame(buttons, bg=bg).pack(in_=buttons, fill=tk.X, expand=True, side=tk.LEFT)
        tk.Frame(buttons, bg=bg).pack(in_=buttons, fill=tk.X, expand=True, side=tk.RIGHT)
        self.demo = tk.Button(self, text="    Demo    ", command=lambda: self.submit(is_demo=True), bg="turquoise")
        self.demo.pack(in_=buttons, side=tk.RIGHT)

        buttons.pack(fill=tk.X, expand=True)
        tk.Frame(self, bg=bg).pack(fill=tk.Y, expand=True)

    # Submit Button's function to collect uID, pass, perform checks, and highlight issues
    def submit(self, event=None, is_demo=False):
        if not is_demo:
            username = self.username_entry.get()
            password = self.password_entry.get()

            if not username:
                self.username_entry.configure(bg="red", fg="white")
                return
            elif not password:
                self.password_entry.configure(bg="red", fg="white")
                return
            elif username and password:
                if not check(self):
                    self.username_entry.configure(bg="red", fg="white")
                    self.password_entry.configure(bg="red", fg="white")
                    return
                else:
                    self.username_entry.configure(bg="green", fg="white")
                    self.password_entry.configure(bg="green", fg="white")

        bring_in_front_of(self.master, self)
        self.update_idletasks()
        self.master.geometry("%dx%d+%d+%d" % (self.master.winfo_width(), self.master.winfo_height(),
                                              self.master.min_posx, self.master.min_posy))

        if DBMS.login_type == "demo":
            fill4demo(self.master)
        elif DBMS.login_type == "admin":
            fill4admin(self.master)
        elif DBMS.login_type == "employee":  # cant use else for security reason
            fill4employee(self.master)
        try:
            self.destroy()
        except:
            self.geometry("+%d+%d" % (-400, 0))


""" UI Setup by login_type """


def fill4demo(self):
    fill4admin(self)
    self.footer.config(text=self.app_name+" DEMO")


def fill4employee(self):
    tk.Label(self, text="CAPS PHARMACY", bg="teal", fg="White",
             font="Arial 25").grid(row=0, sticky=tk.NSEW, columnspan=2)
    tk.Label(self, text="Welcome " + DBMS.login_id, bg="cyan4", fg="white",
             font="Arial 25").grid(row=1, sticky=tk.NSEW, columnspan=2)


def fill4admin(master):

    master.columnconfigure(index=1, weight=5)
    master.rowconfigure(index=0, weight=1)
    master.rowconfigure(index=2, weight=6)

    # fonts
    font_header = "Garamond 35"
    font_banner = "Arial 12"
    font_label = "Arial 10"
    font_footer = "Arial 8"

    # colors
    fg_header = "white"
    fg_banner = "#5f8f9f"
    fg_label = fg_header        # buttons

    # background colors
    bg_header = "#008080"
    bg_banner = "#00222D"
    bg_label = "#008787"        # buttons
    bg_body = "white"         # body right side
    bg_sublabel = bg_banner

    bg_footer = "#005050"       # status bar

    master.config(bg=bg_body)

    tk.Label(master, text="CAPS PHARMACY", bg=bg_header,
             fg=fg_header, font=font_header).grid(row=0, ipady=5, sticky=tk.NSEW, columnspan=2)
    tk.Label(master, text="WELCOME " + DBMS.login_id.upper(),
             bg=bg_banner, fg=fg_banner, font=font_banner).grid(row=1, ipady=4, sticky=tk.NSEW, columnspan=2)

    menu_btns = ["Stock Maintenance", "Add Product", "Delete Product",
                 "Access Database", "Search", "Expired Stocks",
                 "Handle Cash Flows", "Manage Employees", "Check Bills", "Billing"]

    sidebar = tk.Frame(master, bg=bg_banner)
    for y in range(9):
        sidebar.rowconfigure(y, weight=1)

        sdow = tk.Canvas(sidebar, bg=bg_banner, confine=False, highlightbackground=bg_sublabel, offset="0,0")
        if y in [0, 3, 6]:
            sdow.grid(row=y, sticky=tk.NSEW)
        else:
            sdow.grid(row=y, sticky=tk.NSEW)
        sdow.columnconfigure(0, weight=1)
        sdow.rowconfigure(0, weight=1)

        if y in [0, 3, 6]:
            btn = tk.Label(sdow, text=menu_btns[y].upper(), bg=bg_label, fg=fg_label, font=font_label)
            btn.grid(sticky=tk.EW)
        else:
            btn = tk.Label(sdow, text=menu_btns[y].upper(), bg=bg_sublabel, fg=fg_label)
            btn.grid(sticky=tk.NSEW)
            btn.bind("<Enter>", lambda event: hoverMin(event, color=bg_label))
            btn.bind("<Leave>", lambda event: unHoverMin(event, color=bg_sublabel))

    sidebar.grid(row=2, column=0, sticky=tk.NS + tk.W)
    sidebar.rowconfigure(10, weight=10)
    sidebar.columnconfigure(0, weight=1)

    fill_revenue(master)
    #fill_stock_info(master)

    master.footer = tk.Label(master, text=master.app_name, bg=bg_footer, fg=fg_header, font=font_footer)
    master.footer.grid(ipady=2, sticky=tk.EW, columnspan=2)


# User Login & Password Confirmation
def check(self, event=None):
    if DBMS.is_logged_in:
        # If already logged in, this function checks password
        # to confirm some regrettable actions like deleting inventory.
        # The comment below stops IDE warning "login_id might not have any value"
        # noinspection PyUnboundLocalVariable
        DBMS.cur_log.execute("select * from log where username='%s' and password='%s'"
                             % (DBMS.login_id, self.password_entry.get()))
        DBMS.admin_db.commit()
        # confirm password for logged-in admin
        if DBMS.cur_log.fetchone():
            return True
        else:
            return False
    else:
        DBMS.login_id = self.username_entry.get()
        DBMS.cur_log.execute("select type from log where username='%s' and password='%s'"
                             % (DBMS.login_id, self.password_entry.get()))
        DBMS.admin_db.commit()
        is_employee = DBMS.cur_log.fetchone()
        if is_employee:
            if is_employee[0]:
                DBMS.login_type = "employee"
            else:
                DBMS.login_type = "admin"
            DBMS.is_logged_in = True
            return True
        else:
            return False

