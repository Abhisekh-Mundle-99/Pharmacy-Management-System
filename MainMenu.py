import tkinter as tk

# background colors
bg_banner = "#00222D"
bg_body = "white"


# Fill main menu options
def fill_revenue(self):

    body = tk.Frame(self, bg=bg_banner)
    self.revenue = tk.LabelFrame(body, text="Today's Revenue", bg=bg_banner, fg=bg_body)
    for y in range(3):
        self.revenue.rowconfigure(y, weight=1)
    for x in range(2):
        self.revenue.columnconfigure(x, weight=1)
    tk.Label(self.revenue, text="Today's Sales: ", bg=bg_banner, fg=bg_body).grid(row=0, column=0)
    self.sum_sales = tk.Label(self.revenue, text="Today's Sales", bg=bg_banner, fg="green")
    self.sum_sales.grid(row=0, column=1)

    tk.Label(self.revenue, text="Today's Profits: ", bg=bg_banner, fg=bg_body).grid(row=1, column=0)
    self.sum_profits = tk.Label(self.revenue, text="Today's Profits", bg=bg_banner, fg="green")
    self.sum_profits.grid(row=1, column=1)

    tk.Label(self.revenue, text="Turned Down: ", bg=bg_banner, fg=bg_body).grid(row=2, column=0)
    self.sum_turned = tk.Label(self.revenue, text="Turned Down", bg=bg_banner, fg="green")
    self.sum_turned.grid(row=2, column=1)
    self.revenue.grid(row=0, column=0, ipadx=20, sticky=tk.NSEW)

    fshortage = self.shortage = tk.LabelFrame(body, text="Stock Shortage", bg=bg_banner, fg=bg_body)
    fshortage.grid(row=1, column=0, sticky=tk.NSEW)

    fexpired = self.expired = tk.LabelFrame(body, text="Expired Products", bg=bg_banner, fg=bg_body)
    fexpired.grid(row=0, column=1, sticky=tk.NSEW)

    fnearexpiry = self.nearexpiry = tk.LabelFrame(body, text="Near Expiry", bg=bg_banner, fg=bg_body)
    fnearexpiry.grid(row=1, column=1, sticky=tk.NSEW)

    body.grid(row=2, column=1, ipadx=20, ipady=20)
    body.columnconfigure(0, weight=1)
    body.columnconfigure(1, weight=1)
    body.rowconfigure(0, weight=1)
    body.rowconfigure(1, weight=1)
