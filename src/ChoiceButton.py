from reportlab import xrange

try:
    from Tkinter import *
except ImportError:
    from tkinter import Button, NORMAL, DISABLED, LabelFrame, TOP, BOTH, YES
from tkinter.ttk import *


class ChoiceButton(LabelFrame):
    def __init__(self, master, number, heading, textlist=None, **kwrgs):
        LabelFrame.__init__(self, master, text=heading, labelanchor='n', borderwidth=10, **kwrgs)
        super().__init__(master, **kwrgs)
        self.list = []
        self.active = None
        if textlist == None:
            textlist = range(number)
        for i in xrange(number):
            btn = Button(self, text=textlist[i])
            btn.pack(side=TOP, fill=BOTH, expand=YES)
            btn.bind('<1>', self.disable)
            self.list.append(btn)
        self.active = self.list[0]

    def set(self, index, **kwrgs):
        self.list[index].configure(**kwrgs)

    def get(self, index):
        return self.list[index]

    def disable(self, event):
        if self.active is not None:
            self.active['state'] = NORMAL
        self.active = event.widget
        event.widget['state'] = DISABLED
