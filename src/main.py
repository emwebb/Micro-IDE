#!/usr/bin/env python3
from Tkinter import *
import tkFileDialog
import ScrolledText
import pygments
from pygments.lexers import python

class MicroIDE(Frame):
    CODE_AREA = None
    FilePath = None

    def dummy(self):
        pass

    def newFile(self) :
        self.CODE_AREA.delete('1.0', END)
        self.FilePath = None
    
    def saveFile(self) :
        if self.FilePath is None :
            self.FilePath = tkFileDialog.asksaveasfile().write(self.CODE_AREA.get("1.0",END))
        else:
            with open(self.FilePath, 'w') as myfile :
                myfile.write()

    def saveFileAs(self) :
        self.FilePath = tkFileDialog.asksaveasfile().write(self.CODE_AREA.get("1.0",END))
    
    def openFile(self) :
        
        self.FilePath = tkFileDialog.askopenfilename()
        with open(self.FilePath, 'r') as myfile:
            self.newFile()
            self.CODE_AREA.insert("end",myfile.read())
        self.highlight()

    def close(self) :
        root.destroy()

    def createWidgets(self):
        self.CODE_AREA = ScrolledText.ScrolledText(self)
        self.CODE_AREA.insert("end", "def hello():\n    pass\n")
        self.CODE_AREA.pack(side="top", fill="both", expand=True)

        self.CODE_AREA.tag_configure("Token.Comment",
                                    foreground="#00ff00")
        self.CODE_AREA.tag_configure("Token.Literal.String",
                                    foreground="#ff99cc")
        self.CODE_AREA.tag_configure("Token.Keyword",
                                    foreground="#aaaa00")
        self.CODE_AREA.tag_configure("Token.Name.Function",
                                    foreground="#ffff00")
        self.CODE_AREA.configure(bg = "#555555")
        self.highlight()

        self.MENU = Menu(root)

        filemenu = Menu(self.MENU, tearoff=0)
        filemenu.add_command(label="New", command=self.newFile)
        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_command(label="Save as...", command=self.saveFileAs)
        filemenu.add_command(label="Close", command=self.close)

        filemenu.add_separator()
        self.MENU.add_cascade(label="File", menu=filemenu)


        root.config(menu=self.MENU)
        
    
    def highlight(self,event=None):
        textStart = "1.0"
        textEnd = "end-1c"
        if not event is None :
            cursorIndex = self.CODE_AREA.index(INSERT)
            textStart = cursorIndex.split(".")[0] + ".0"
            textEnd = cursorIndex.split(".")[0] + ".end"

        self.CODE_AREA.mark_set("range_start", textStart)
        data = self.CODE_AREA.get(textStart, textEnd)
        for token, content in pygments.lex(data, python.PythonLexer()):
            print token
            self.CODE_AREA.mark_set("range_end", "range_start + %dc" % len(content))
            self.CODE_AREA.tag_add(str(token), "range_start", "range_end")
            self.CODE_AREA.mark_set("range_start", "range_end")

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()
        self.pack()
        root.bind("<KeyRelease>", self.highlight)
    

if __name__ == "__main__" :
    root = Tk()
    app = MicroIDE(master=root)
    app.mainloop()
    root.destroy()