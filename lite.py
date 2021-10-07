import time, sys
import tkinter as tk

import psutil


DAYS = {
    0: "Lundi",
    1: "Mardi",
    2: "Mercredi",
    3: "Jeudi",
    4: "Vendredi",
    5: "Samedi",
    6: "Dimanche"
}

MONTH = {
    1: "Janvier",
    2: "Fevrier",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre"
}


class Statistic(tk.LabelFrame):
    def __init__(self, *args, **kw):
        tk.LabelFrame.__init__(self, bg='#FFF', *args, **kw)
        self.master.option_add('*Label.Font', ('Arial',14,'bold'))
        self.master.configure(bg='#EFE')
        self.master.wm_attributes('-topmost', 1)
        self.master.wm_attributes('-alpha', 0.5)

        self.master.wm_overrideredirect(True)
        if sys.platform == 'darwin':
            self.master.wm_overrideredirect(False)

        self.master.resizable(0, 0)

        self.pack(expand=1, fill='both', padx=20, pady=20)


        cpu_label = tk.Label(self, text=' CPU :', anchor='w')
        cpu_label.grid(row=1, column=1, sticky='ew', padx=5, pady='5 0', ipadx=10, ipady=3)
        self.cpu_percent = tk.Label(self, text='100.0 %', bg='#FFF')
        self.cpu_percent.grid(row=1, column=2, sticky='ew', pady='5 0', ipadx=10, ipady=3)
        self.cpu_color = tk.Label(self, width=5, bg='#777fff')
        self.cpu_color.grid(row=1, column=3, sticky='ew', pady='5 0', ipadx=10, ipady=3)


        ram_label = tk.Label(self, text=' RAM :', anchor='w')
        ram_label.grid(row=2, column=1, sticky='ew', padx=5, pady='5 0', ipadx=10, ipady=3)
        self.ram_percent = tk.Label(self, text='100.0 %', bg='#FFF')
        self.ram_percent.grid(row=2, column=2, sticky='ew', pady='5 0', ipadx=10, ipady=3)
        self.ram_color = tk.Label(self, width=5, bg='#777fff')
        self.ram_color.grid(row=2, column=3, sticky='ew', pady='5 0', ipadx=10, ipady=3)


        batt_label = tk.Label(self, text=' BATTERIE :', anchor='w')
        batt_label.grid(row=3, column=1, sticky='ew', padx=5, pady=5, ipadx=10, ipady=3)
        self.batt_percent = tk.Label(self, text='100.0 %', bg='#FFF')
        self.batt_percent.grid(row=3, column=2, sticky='ew', pady=5, ipadx=10, ipady=3)
        self.batt_color = tk.Label(self, width=5, bg='#777fff')
        self.batt_color.grid(row=3, column=3, sticky='w', pady=5, ipadx=10, ipady=3)


        self.days_ = tk.Label(self, bg='#FFF', text='Vendredi')
        self.days_.grid(row=2, column=4, sticky='ew', padx=5, pady=5, ipadx=10, ipady=3)
        self.datetime_ = tk.Label(self, bg='#FFF', text='31 Septembre 2021')
        self.datetime_.grid(row=3, column=4, sticky='ew', padx=5, pady=5, ipadx=10, ipady=3)
        self.heurs_ = tk.Label(self, bg='#FFF', text='21 h 30 min 00 s')
        self.heurs_.grid(row=1, column=4, sticky='ew', padx=5, pady=5, ipadx=10, ipady=3)


        self.master.bind('<Leave>', self.mouse_leave)
        self.master.bind('<Motion>', self.mouse_enter)
        self.master.bind('<B1-Motion>', self.leftMove)
        self.master.bind('<Button-1>', self.leftDown)
        self.master.bind('<ButtonRelease-1>', self.leftUp)
        self.master.bind('<Control-Button-1>', self.rightDown)

        self.x = tk.IntVar(value=0)
        self.y = tk.IntVar(value=0)
        self.moving = tk.IntVar(value=0)
        self.status = tk.IntVar(value=1)

        # Refresh data after 500ms
        self.changes()


    def changes(self):
        self.after(500, self.changes)

        objet_date = time.localtime()

        self.datetime_.configure(text=time.strftime(f"%d  {MONTH[objet_date.tm_mon]}  %Y"))

        self.heurs_.configure(text=time.strftime("%H h %M min %S s"))

        self.days_.configure(text=DAYS[objet_date.tm_wday])
        
        # Use the color blue when the value is less than 40,
        # green when it is between 40 and 60 then 
        # red when it exceeds 60

        cpu_ = psutil.cpu_percent()
        cpu_c = '#08F' if cpu_ < 40 else '#0F0' if cpu_ >= 40 and cpu_ < 60 else '#F00'
        self.cpu_color.configure(bg=cpu_c)
        self.cpu_percent.configure(text=f'{cpu_} %', fg=cpu_c)

        ram_ = psutil.virtual_memory().percent
        ram_c = '#08F' if ram_ < 40 else '#0F0' if ram_ >= 40 and ram_ < 60 else '#F00'
        self.ram_color.configure(bg=ram_c)
        self.ram_percent.configure(text=f'{ram_} %', fg=ram_c)

        try:
            batt = psutil.sensors_battery().percent
            batt_c = '#F00' if batt < 40 else '#0F0' if batt >= 40 and batt < 60 else '#08F'
            if psutil.sensors_battery().power_plugged != False:
                batt_c = '#777FFF' # si 'En charge'
            self.batt_percent.configure(text=f'{int(batt)} %', fg=batt_c)
            self.batt_color.configure(width=int((batt * 5) / 100), bg=batt_c)
        except AttributeError:
            self.batt_percent.configure(text="100 %", fg="#777FFF")
            self.batt_color.configure(width=5, bg="#777FFF")


    def mouse_enter(self, *_):
        self.master.wm_attributes('-alpha', 0.5)


    def mouse_leave(self, *_):
        self.master.wm_attributes('-alpha', 0.5)


    def leftUp(self, event):
        self.master.wm_attributes('-alpha',1)
        self.moving.set(0)


    def leftDown(self, event):
        self.master.wm_attributes('-alpha',0.1)
        self.x.set(event.x)
        self.y.set(event.y)
        self.moving.set(1)


    def leftMove(self, event):
        if self.moving.get() == 1:
            newX = self.master.winfo_x() + (event.x - self.x.get())
            newY = self.master.winfo_y() + (event.y - self.y.get())
            self.master.geometry(f'+{int(newX)}+{int(newY)}')


    def rightDown(self, event):
        self.status.set(0)
        self.master.destroy()


if __name__ == '__main__':
    Statistic().mainloop()
