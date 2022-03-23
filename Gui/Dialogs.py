#!/usr/bin/env python
from Tkinter import *
import Tkinter
import tkMessageBox
import os

#Code for Dialog class downloaded from effbot.org
#http://effbot.org/tkinterbook/tkinter-dialog-windows.htm
class Dialog(Toplevel):
    def __init__(self, parent, args=None, title=None):
        Toplevel.__init__(self, parent)
        self.transient(parent)

        if args:
            self.args = args

        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()
        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50, parent.winfo_rooty()+50))
        self.initial_focus.focus_set()
        self.wait_window(self)

    def body(self, master):
        pass

    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set()
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.destroy()

#Gets channel state parameters (inherits Dialog base class)
class StateDialog(Dialog):
    pChange = None
    pError = None
    state = None

    def body(self, master):
        #Set up string variables.
        self.pChange = StringVar(self.parent)
        self.pError = StringVar(self.parent)
        self.state = StringVar(self.parent)

        #Copy values in case user cancels.
        self.pChange.set(self.args[0])
        self.pError.set(self.args[1])
        self.state.set(self.args[2])

        #Set up form.
        Label(master, text="Probability of State Change")\
            .grid(row=0, column=0, padx=5, pady=5, sticky=W)
        self.pChangeEntry = Entry(master, textvariable=self.pChange) \
            .grid(row=0, column=1, padx=5, pady=5)

        Label(master, text="Probability of Error")\
            .grid(row=1, column=0, padx=5, pady=5, sticky=W)
        self.pErrorEntry = Entry(master, textvariable=self.pError) \
            .grid(row=1, column=1, padx=5, pady=5)

        Label(master, text="Channel Speed (b/ms)") \
            .grid(row=2, column=0, padx=5, pady=5, sticky=W)
        self.speedEntry = Entry(master, textvariable=self.state) \
            .grid(row=2, column=1, padx=5, pady=5)

    def validate(self):
        try: pChange = float(self.pChange)
        except:
            tkMessageBox.showerror("Invalid Input", "Probabilty of state change must be a number.")
            return False

        try: pError = float(self.pError)
        except:
            tkMessageBox.showerror("Invalid Input", "Probabilty of error must be a number.")
            return False

        try: speed = float(self.speed)
        except:
            tkMessageBox.showerror("Invalid Input", "Channel speed must be a number.")
            return False

        if pChange < 0 or pChange > 1:
            tkMessageBox.showerror("Invalid Input", "Probability of state change must be 0 to 1 inclusive.")
        elif pError < 0 or pError > 1:
            tkMessageBox.showerror("Invalid Input", "Probability of error must be 0 to 1 inclusive.")
        else:
            params = {"pRemain": 1 - pChange, "pError": pError, "speed": speed}
            self.result = params
            return True

    def apply(self):
        pass