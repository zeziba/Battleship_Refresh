__author__ = "Charles Engen"

import threading
import time
import tkinter
from random import randint


class Clock(tkinter.Frame):
    def __init__(self, parent, interval=1.0, thread_count=1):
        tkinter.Frame.__init__(self, parent)

        self.parent = parent
        self.pack()

        self.interval = interval
        self.thread_count = thread_count

        self.time_value_var = tkinter.StringVar()
        self.random_var = tkinter.StringVar()

        self.parent.protocol("WM_DELETE_WINDOW", self.callback)
        self.parent.title("Clock: # %s" % self.thread_count)
        self.parent.geometry("300x150")

        self.time_value_var.set(None)
        self.random_var.set(None)

        self.random_label = tkinter.Label(
            self, textvariable=self.random_var, font=("Helvetica", 16)
        )
        self.time_label = tkinter.Label(
            self, textvariable=self.time_value_var, font=("Helvetica", 32)
        )

        self.random_label.pack(side="bottom")
        self.time_label.pack()

    def callback(self):
        self.parent.quit()

    def run(self):
        self.mainloop()
        self._update()

    def _update(self):
        now = time.strftime("%H:%M:%S")
        random_var = randint(0, 100)
        self.time_value_var.set(now)
        self.random_var.set(random_var)
        self.after(int(self.interval * 1000), self._update)

    def __call__(self, *args, **kwargs):
        self._update()


c = Clock(tkinter.Tk())
c.run()
