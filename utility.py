from datetime import date
import time
import win32api
import win32print


""" STATIC UTILITY FUNCTIONS """


# Get Current Date for displaying or checking expiry dates
def current_date():
    now = time.localtime()
    cur_date = date(now[0], now[1], now[2])
    return cur_date


# Print a text file using the default printer
def print_file(file):
    win32api.ShellExecute(0, "print", file, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)


# Function to run a buttons or labels command on pressing the Enter key
def on_return(event):
    event.widget.invoke()


# Function to change the focus to the next label or button
# on pressing Enter key
def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"


# Change focus to another window
def bring_in_front_of(to_lift, to_lower=None):
    #to_lift.lift(aboveThis=to_lower)
    to_lift.focus_force()


# functions to highlight and un-highlight buttons when mouse is on the button
def hoverMin(event, color):
    event.widget.config(bg=color)   #we are changing the background color of the button


def unHoverMin(event, color):
    event.widget.config(bg=color)   #we are changing the color of button back to normal
