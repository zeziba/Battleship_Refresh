from Old.Other_Scripts.clock import *


class Client(threading.Thread):
    def __init__(self, interval=1.0):
        self.thread_count = 0
        self.interval = interval

        threading.Thread.__init__(self)

        self.start()

    def new_clock(self):
        self.thread_count += 1
        exec("%s = None" % "".join(("clock", str(time.time())[:10])))
        aclock = tkinter.Tk()
        clock = Clock(aclock, self.interval, self.thread_count)
        thread = threading.Thread(target=clock)
        thread.start()

    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tkinter.Tk()
        self.root.wm_title("Main Window")
        self.root.geometry("190x100")

        self.button = tkinter.Button(text="New Clock", command=self.new_clock)
        self.button.pack()

        self.root.mainloop()


a = Client()
