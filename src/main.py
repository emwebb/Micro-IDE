#!/usr/bin/env python
from Tkinter import *
from ScrolledText import ScrolledText

class MicroIDE(Frame):

    def dummy(self):
        pass



    def createWidgets(self):
        self.CODE_AREA = ScrolledText(self)
        self.CODE_AREA.insert("end", "Hello\nworld")
        self.CODE_AREA.pack(side="top", fill="both", expand=True)
        

        self.MENU = Menu(root)

        filemenu = Menu(self.MENU, tearoff=0)
        filemenu.add_command(label="New", command=self.dummy)
        filemenu.add_command(label="Open", command=self.dummy)
        filemenu.add_command(label="Save", command=self.dummy)
        filemenu.add_command(label="Save as...", command=self.dummy)
        filemenu.add_command(label="Close", command=self.dummy)

        filemenu.add_separator()
        self.MENU.add_cascade(label="File", menu=filemenu)


        root.config(menu=self.MENU)
        

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    

if __name__ == "__main__" :
    root = Tk()
    app = MicroIDE(master=root)
    app.mainloop()
    root.destroy()