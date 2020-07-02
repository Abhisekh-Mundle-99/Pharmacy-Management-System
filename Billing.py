import tkinter as tk
import random
import DBMS
import time


# BILLING SYSTEM
class BillingForm(tk.Toplevel):
    last_name = ''
    last_phone = 0

    def __init__(self, master, bg='white', fg='black'):
        super().__init__()
        self.master = master
        self.master.update_idletasks()
        pos_x = int(self.master.min_posx + self.winfo_screenwidth() / 2 - 250)
        pos_y = int(self.master.min_posy + self.winfo_screenheight() / 2 - 300)
        self.title("Billing")
        self.geometry("500x600+%d+%d" % (pos_x, pos_y))

        t = 0
        DBMS.names = []
        DBMS.qty = []
        DBMS.sl = []
        DBMS.n = []
        DBMS.qtys = [''] * 10
        DBMS.cur_col.execute("select * from med")
        for i in DBMS.cur_col:
            DBMS.n.append(i[1])
        DBMS.pharm_db.commit()

        self.bg = bg
        self.fg = fg

        for x in range(3):
            self.columnconfigure(x, weight=1)
        for y in range(8):
            self.rowconfigure(y, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(8, weight=5)
        tk.Label(self, text="BILLING SYSTEM", bg="cyan4", fg="white", font="Arial 25").pack(fill=tk.BOTH, expand=1)

        tk.Label(self, text='Customer Name: ').pack()
        self.name = tk.Entry(self, bg=bg, fg=fg)
        self.name.pack()

        self.protocol('WM_DELETE_WINDOW', self.close_bill)
        tk.Button(self, width=15, text='Add Valued Customer', command=self.add_valued).pack()
        self.valued = tk.Label(self, text='Valued\uD83D', bg="grey", fg=bg)
        self.valued.pack()

        tk.Button(self, width=15, text='Reset Bill', command=self.clear_bill).pack()
        tk.Button(self, width=15, text='Save Bill', command=self.make_bill).pack()
        tk.Button(self, width=15, text='Print Bill', command=lambda: DBMS.print_file(bill_file)).pack()

        tk.Label(self, text='Enter phone: ').pack()
        self.phone = tk.Entry(self, bg=bg, fg=fg)
        # self.phone.bind('<Return>', self.check_valued)
        self.phone.pack()

        tk.Label(self, text="Valued", bg="grey", fg="white").pack()

        tk.Label(self, text='-' * 115).pack()
        self.bottomArea = tk.Canvas.pack()
        tk.Label(self, text='SELECT PRODUCT', width=25, relief='ridge').pack(padx=0, expand=True)
        tk.Label(self, text=' RACK  QTY LEFT     COST          ', width=25, relief='ridge').pack(padx=0, expand=True)
        tk.Label(self, text='QUANTITY', width=20, relief='ridge').pack(padx=0, expand=True)
        qtys = tk.Entry(self).pack()

    # Clear all data in the Billing Form
    def clear_bill(self):
        global bill_file
        # reset text file to prevent misprint
        # clear content of data-entry widgets
        # reset menu flags
        if self.master.confirm_task("Trash this Bill?"):
            bill_file = ''
            self.name.config(text='')
            self.phone.config(text='')
            self.valued.config(bg="grey", fg=self.bg)

    # Prepare a printable Bill text file
    def make_bill(self):
        global bill_id, bill_file
        if bill_id != 0:
            bill_id += 1
        else:
            DBMS.cur_col.execute("select bill_id from bills")
            # if cur_col.fetchall():
            #    bill_id =
            # else:
            #    bill_id = 0;
            price = [0.0] * 10
            q = 0
            sl = []
            det = ['', '', '', '', '', '', '', '']
            det[2] = str(sl)
            for i in range(len(sl)):
                print(sl[i], ' ', DBMS.qty[i], ' ', DBMS.names[i])
            for k in range(len(sl)):
                DBMS.cur_col.execute("select * from med where sl_no=?", (sl[k],))
                for i in DBMS.cur_col:
                    price[k] = int(DBMS.qty[k]) * float(i[4])
                    print(DBMS.qty[k], price[k])
                    DBMS.cur_col.execute("update med set qty_left=? where sl_no=?", (int(i[3]) - int(DBMS.qty[k]), sl[k]))
                DBMS.pharm_db.commit()
            det[5] = str(random.randint(100, 999))
            bill_file = 'bill_' + str(det[5]) + '.txt'
            total = 0.00
            for i in range(10):
                if price[i] != '':
                    total += price[i]  # totalling
            m = '\n\n\n'
            m += "                                  No :%s\n\n" % det[5]
            m += "            CAPS PHARMACY\n"
            m += "  Asansol Budha More, Paschim Burdwan, WB.\n\n"
            m += "---------------\n"
            if DBMS.bill_accounted:
                m += "Name: %s\n" % self.last_name
                m += "Address: %s\n" % self.last_phone
                det[0] = self.last_name
                det[1] = self.last_name
                DBMS.cur_col.execute('select * from cus')
                for i in DBMS.cur_col:
                    if i[0] == self.last_name:
                        det[7] = i[2]
            else:
                m += "Name: %s\n" % self.name.get()
                m += "Address: %s\n" % self.phone.get()
                det[0] = self.name.get()
                det[1] = self.phone.get()
            m += "---------------\n"
            m += "Product                      Qty.       Price\n"
            m += "---------------\n"  # 47, qty=27, price=8 after 2
            for i in range(len(sl)):
                if DBMS.names[i] != 'nil':
                    s1 = ' '
                    s1 = (DBMS.names[i]) + (s1 * (27 - len(DBMS.names[i]))) + s1 * \
                         (3 - len(DBMS.qty[i])) + DBMS.qty[i] + s1 * \
                         (15 - len(str(price[i]))) + str(price[i]) + '\n'
                    m += s1
            m += "\n---------------\n"
            if DBMS.bill_accounted:
                ntotal = total * 0.8
                m += 'Total' + (' ' * 25) + (' ' * (15 - len(str(total)))) + str(total) + '\n'
                m += "Valued customer Discount" + (' ' * (20 - len(str(total - ntotal)))) + '-' + str(
                    total - ntotal) + '\n'
                m += "---------------\n"
                m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(ntotal)))) + 'Rs ' + str(ntotal) + '\n'
                det[3] = str(ntotal)
            else:
                m += 'Total' + (' ' * 25) + (' ' * (12 - len(str(total)))) + 'Rs ' + str(total) + '\n'
                det[3] = str(total)

            m += "---------------\n\n"
            m += "Dealer 's signature:___________________________\n"
            m += "===============================================\n"
            print(m)
            p = time.localtime()
            det[4] = str(p[2]) + '/' + str(p[1]) + '/' + str(p[0])
            det[6] = m
            bill = open(bill_file, 'w')
            bill.write(m)
            bill.close()
            cb = ('cus_name', 'cus_add', 'items', 'Total_cost', 'bill_dt', 'bill_no', 'bill', 'val_id')
            DBMS.cur_col.execute('insert into bills values(?,?,?,?,?,?,?,?)',
                                 (det[0], det[1], det[2], det[3], det[4], det[5], det[6], det[7]))
            DBMS.pharm_db.commit()

    # Close the Billing Menu
    def close_bill(self):
        if DBMS.bill_accounted or self.master.close_window(self, "Reset this Bill?"):
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
            DBMS.cur_log.execute("select * from cus where name='%s' and phone='%s' and valued='%s'"
                            % (name, phone, True))
            DBMS.pharm_db.commit()
            if DBMS.cur_log.fetchone() is not None:
                self.valued.configure(bg="green", fg="white")
                return True
            else:
                self.valued.configure(bg="red", fg="white")
        return False

    # Add the customer getting billed, as new Valued Customer
    def add_valued(self):
        name = self.name.get()
        phone = self.phone.get()

        if not name:
            self.name.configure(bg="red", fg="white")
        elif not phone:
            self.phone.configure(bg="red", fg="white")
        else:
            DBMS.cur_col.execute("select * from cus where phone='%s'")
            if DBMS.cur_col.fetchone() is not None:
                for i in DBMS.cur_col:
                    if i[2]:
                        if i[0] != name:
                            self.phone.configure(bg="red", fg="white")
                            DBMS.msg.showerror("Phone number already registered under another name!")
                            return False
                        else:
                            self.name.configure(bg="green", fg="white")
                            self.phone.configure(bg="green", fg="white")
                            DBMS.msg.showerror("Already a valued customer!")
                            return False
                if self.master.confirm_task(self, "Make " + name + " a valued customer?"):
                    DBMS.cur_col.execute("update cus set valued=TRUE where phone=?", phone)
            else:
                if self.master.confirm_task(self, "Add " + name + " as a new valued customer?"):
                    DBMS.cur_col.execute("modify into cus values(?,?,?)", (name, phone, 'TRUE'))
            DBMS.pharm_db.commit()
        return False
