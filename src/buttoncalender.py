import time as t
import os
from datetime import datetime
from tkinter import *
from tkinter.ttk import *

from PIL import ImageTk, Image
from tkcalendar import Calendar

from .const import cmp
from src.Cython.proWrd1 import Filter


class CalendarButton(Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.datevar = StringVar()
        self.master = master
        Frame.__init__(self, master, **kw)
        CALENDAR_ICO = os.path.normpath("data/calender.png")
        self.tmp = Image.open(CALENDAR_ICO).resize((30, 30), Image.ANTIALIAS)
        self.tmp = ImageTk.PhotoImage(image=self.tmp)
        self.btn = Button(
            self,
            textvariable=self.datevar,
            image=self.tmp,
            compound=RIGHT,
            command=lambda: self.open_calendar(),
            takefocus=False,
        )
        self.btn.pack(side=TOP, expand=YES, fill=BOTH)
        self.bind("<Button-1>", self.coor)
        self.btn.bind("<Button-1>", self.coor)
        now = self.get_time_tuple()
        self.time_tuple_to_object(now)
        self.update()

    def time_tuple_to_object(self, now):
        self.year = now.tm_year
        self.month = now.tm_mon
        self.day = now.tm_mday
        self.hour = now.tm_hour
        self.min = now.tm_min
        self.sec = now.tm_sec

    def update(self):
        date = datetime(
            self.year,
            int(self.month),
            self.day,
            int(self.hour),
            int(self.min),
            int(self.sec),
        )
        st = date.ctime()
        self.datevar.set("")
        self.datevar.set(st)

    def coor(self, event):
        f = event.widget
        try:
            c = int(str(f).split(".")[1])
        except ValueError:
            return 0
        if cmp(c, w) != 0:
            self.rootc1.destroy()
            self.rootc1.unbind_all("<Button-1>")
            try:
                self.btn["state"] = NORMAL
            except TclError:
                print("calenbutt")

    def get_time_tuple(self, stamp=None):
        if stamp is None:
            return t.localtime()
        return t.strptime(stamp)

    def get_time_stamp(self, timetuple=None):
        if timetuple is None:
            return t.asctime()
        return t.asctime(timetuple)

    def insert(self, string):
        tup = self.get_time_tuple(string)
        self.time_tuple_to_object(tup)
        self.update()

    def get(self):
        return self.datevar.get()

    def got_it(self, se, event=None):
        date = se.get_date()
        self.hour = int(Filter(self._h.get()))
        self.min = int(Filter(self._m.get()))
        self.sec = int(Filter(self._s.get()))
        if date is not None:
            self.month = int(date.split(".")[1])
            self.day = int(date.split(".")[0])
            self.year = int(date.split(".")[2])
        self.update()
        self.rootc1.destroy()
        self.btn["state"] = NORMAL
        self.rootc1.unbind_all("<Button-1>")

    def open_calendar(self):
        self.update_idletasks()
        screenw = self.winfo_screenwidth()
        h = self.winfo_reqheight()
        w = self.winfo_width()
        x = self.winfo_rootx()
        if x > screenw / 2:
            if w < 260:
                x = x - (260 - w)
        y = self.winfo_rooty() + h
        if w < 260:
            w = 260
        self.rootc1 = Toplevel()
        if sys.platform == "win32":
            self.rootc1.wm_attributes("-alpha", "gray98")
        self.rootc1.bind_all("<Button-1>", self.coor, "+")
        self.rootc1.title("Ttk Calendar")
        self.rootc1.columnconfigure(0, weight=1)
        self.rootc1.columnconfigure(1, weight=1)
        self.rootc1.columnconfigure(2, weight=1)
        self.rootc1.columnconfigure(3, weight=1)
        self.rootc1.columnconfigure(4, weight=1)
        self.rootc1.columnconfigure(5, weight=1)
        self.rootc1.rowconfigure(0, weight=1)
        self.rootc1.rowconfigure(1, weight=1)
        self.rootc1.rowconfigure(2, weight=1)
        self.rootc1.overrideredirect(1)
        self.rootc1.focus_set()
        self.rootc1.geometry("%sx220+%d+%d" % (w, x, y))
        ttkcal = Calendar(self.rootc1, firstweekday="monday", locale="ro_RO")
        ttkcal.grid(row=0, column=0, columnspan=6, sticky=N + S + E + W)
        ttkcal.bind("<Button-1>", self.coor)
        Label(self.rootc1, text="Hour", width=15, background="grey99").grid(
            row=1, column=0, sticky=N + S + E + W
        )
        self._h = Spinbox(self.rootc1, from_=0, to=23)
        self._h.grid(row=1, column=1, sticky=N + S + E + W)
        Label(self.rootc1, text="Min", width=15, background="grey99").grid(
            row=1, column=2, sticky=N + S + E + W
        )
        self._m = Spinbox(self.rootc1, from_=0, to=59)
        self._m.grid(row=1, column=3, sticky=N + S + E + W)
        Label(self.rootc1, text="Sec", width=15, background="grey99").grid(
            row=1, column=4, sticky=N + S + E + W
        )
        self._s = Spinbox(self.rootc1, from_=0, to=59)
        self._s.grid(row=1, column=5, sticky=N + S + E + W)
        btn = Button(self.rootc1, text="Done", command=lambda: self.got_it(ttkcal))
        btn.grid(row=2, column=0, columnspan=6, sticky=N + S + E + W)
        self.btn["state"] = DISABLED
        self._h.delete(0, END)
        self._m.delete(0, END)
        self._s.delete(0, END)
        now = self.get_time_tuple()
        self._h.insert(0, now.tm_hour)
        self._m.insert(0, now.tm_min)
        self._s.insert(0, now.tm_sec)
        self.rootc1.mainloop()
