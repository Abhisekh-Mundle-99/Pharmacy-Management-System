import tkinter as tk
import tkinter.messagebox as msg
import DBMS


# Main Application Class
class Application(tk.Tk):
    # app defaults
    min_height = 640
    min_width = 520
    cur_height = 640
    cur_width = 520
    max_height = 1024
    max_width = 1024

    # fonts
    c_tribars = '\u2261'
    c_search = '\uD836'  # '\uD83D' '\uDD0D'
    c_sun = '\u2600'
    c_moon = '\u263E'  # '\uD83C' '\uDF18'
    c_rupay = '₹'

    menu_font = 'Century Gothic'
    menu_fontsize = 30

    # color schemes
    dark = [{"bg": "black", "fg": "white"}, {"bg": "darkgrey", "fg": "white"}]
    light = [{"bg": "ivory", "fg": "black"}, {"bg": "seablue", "fg": "grey"}]

    # ui options | menu names
    app_name = "CAPS PMS v1.0"
    app_icon = "icon.ico"

    # tooltips | descriptions

    # flags for app states:
    #   full_screen: false, default,    app doesnt start with full screen
    #   dark_mode:  true, default,      color scheme is set to dark by default
    #   message_open: false, default    toggled to check if a message box is already active
    #   logged_in: false, default,      toggled to check if user has logged in, when already
    #                                   logged in, only password confirmation is required for
    #                                   other things
    is_fullscreen = False
    is_dark = True
    msg_open = False
    is_logged_in = True

    # control variables
    cursor_x = 0
    cursor_y = 0

    # default initialization function called on class instantiation
    def __init__(self):
        super().__init__()

        self.title(self.app_name)
        self.iconbitmap(self.app_icon)
        self.setup_look_n_feel()

    # initialize application with default UI preferences
    def setup_look_n_feel(self):
        if self.is_fullscreen:
            self.state('zoomed')
        else:
            self.geometry("{0}x{1}+0+0".format(self.min_height, self.min_width))

        # store screen dimensions for later use
        self.max_width = self.winfo_screenwidth()
        self.max_height = self.winfo_screenheight()

        # ready color scheme
        if self.is_dark:
            bg_color = self.dark[0].get('bg')
            fg_color = self.dark[0].get('fg')
        elif self.is_light:
            bg_color = self.light[0].get('bg')
            fg_color = self.light[0].get('fg')
        else:
            bg_color = self.custom[0].get('bg')
            fg_color = self.custom[0].get('fg')

        DBMS.change_pass()
        self.create_login()

        # define all top menus
        # self.main_menu = tk.Menu(self, bg=bg_color, fg=fg_color, borderwidth=0, tearoff=0)
        # self.main_menu.config(font=(self.menu_font, self.menu_fontsize))

        # add menu commands or cascades or submenus in desired order
        # cascades are menu categories like File, Edit, View, etc
        # and insert sub menus or commands in them
        # self.home_menu = tk.Menu(self, bg=bg_color, fg=fg_color, borderwidth=0, tearoff=0)
        # self.login_btn = self.main_menu.add_cascade(label=self.c_tribars, menu=self.home_menu, font=(self.menu_font, 100), command=self.create_login())
        # self.menu_btn = self.main_menu.add_cascade(label=self.c_tribars, menu=self.home_menu, font=(self.menu_font, 100))
        # self.search_btn = self.main_menu.add_command(label=self.c_search, command=self.popup_search)
        # self.theme_btn = self.main_menu.add_command(label=self.c_moon, command=switch_theme)
        # self.bill_btn = self.main_menu.add_command(label=self.c_rupay, command=self.popup_bill)
        #
        # complete configuration and formatting
        # self.config(menu=self.main_menu)

        tk.Label(self, text="YOUR WORKSPACE", bg="cyan4", fg="white", font="Arial 25").pack()

        # run repeatable behaviour for first time
        self.update()

        self.protocol('WM_DELETE_WINDOW', lambda: close_window(self,"Quit " + self.app_name + "?"))

# POPUPS    
# Search Menu
    def popup_search(self):
        DBMS.SearchForm(self)

#login Form
    def create_login(self):
        DBMS.LoginForm(self)


# Billing Form
    def popup_bill(self):
        DBMS.BillingForm(self)

# Update Components On Resize
    def update(self):
        super(Application, self).update()
        if self.is_fullscreen:
            self.grid(self.cur_width * 0.8, self.cur_height * 0.8)
            # self.main_menu.grid()

# Setup Default Theme & Menus
    def setup_theme(self):

        # override default titlebar, geometry
        # self.overrideredirect(True)
        if self.is_fullscreen:
            self.geometry("{0}x{1}+0+0".format(self.max_width, self.max_height))
        else:
            self.geometry("{0}x{1}+0+0".format(self.min_width, self.min_height))

        # ready color scheme
        if self.is_dark:
            bg_color = self.dark[0].get('bg')
            fg_color = self.dark[0].get('fg')
        elif self.is_light:
            bg_color = self.light[0].get('bg')
            fg_color = self.light[0].get('fg')
        else:
            bg_color = self.custom[0].get('bg')
            fg_color = self.custom[0].get('fg')

    # Generate GUI Elements
        # title bar
        title_bar = tk.Frame(self, bg=bg_color, relief='raised', bd=2)
        title_bar.geometry('{0}x{1}', 100, self.winfo_height())

        # top menu
        self.menu = tk.Menu(self, bg=bg_color, fg=fg_color)

        # right side buttons
        minimize_button = tk.Button(title_bar, text='_', command=self.set_minimize)
        maximize_button = tk.Button(title_bar, text='+', command=self.set_fullscreen)
        close_button = tk.Button(title_bar, text='x', command=lambda: self.close_window("Quit " + self.app_name + "?"))

        # canvas
        window = tk.Canvas(self, bg=bg_color)

        # pack the widgets
        title_bar.pack(expand=1, fill='x')
        close_button.pack(side='right')
        maximize_button.pack(side='right')
        minimize_button.pack(side='right')
        window.pack(expand=1, fill='both')

        # bind title bar left-button click-hold and motion to window
        title_bar.bind('<Button-1>', self.hold_window)


# UI COMPONENTS & BEHAVIOUR

# Toggle Theme
def switch_theme(self):
    self.is_dark = not self.is_dark
    if self.is_dark:
        self.theme_btn.config(label=self.c_moon)
    else:
        self.theme_btn.config(label=self.c_sun)


# Close Button
def close_window(self, message, event=None):
    # this confirmation window operation can be generalized for more than purpose
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
    Label(msg_box, text=message)
    if req_pass:
        Label(msg_box, text="Password")
        password = Entry(msg_box, width=20)
        password.bind("<Return>", check)


# Click-n-Hold Titlebar To Move Window
def hold_window(self, event):
    start_x = event.x_root
    start_y = event.y_root

    relative_x = app.winfo_x() - event.x_root
    relative_y = app.winfo_y() - event.y_root

    def move_window(_event):
        self.geometry('+{0}+{1}'.format(_event.x_root + relative_x, _event.y_root + relative_y))

    start_x = _event.x_root
    start_y = _event.y_root

    # bind title bar motion to window
    self.bind('<B1-Motion>', move_window)


# Minimize Button
def set_minimize(self):
    self.state('withdrawn')


# Toggle Full Screen
def set_fullscreen(self):
    if self.is_fullscreen:
        self.state('normal')
        self.is_fullscreen = False
    elif not self.is_fullscreen:
        self.state('zoomed')
        self.is_fullscreen = True

    # updating state variables to re-place UI components
    cur_height = self.winfo_screenheight()
    cur_width = self.winfo_screenwidth()


# Instantiating Application
if __name__ == "__main__":
    app = Application()
    app.mainloop()
