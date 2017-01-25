#!/usr/bin/env python
from Tkinter import *
import tkFileDialog
import ScrolledText
import pygments
from pygments import lexers
from subprocess import call

class MicroIDE(Frame):
    CODE_AREA = None
    FilePath = None
    CurrentLanguage = None
    Lexer = None

    def FindLanguage(self) :
        if self.FilePath is None :
            self.CurrentLanguage = None
            return
        
        filename = self.FilePath.split("/")[-1]
        print filename
        self.Lexer = pygments.lexers.get_lexer_for_filename(filename)
        if not self.Lexer == None :
            self.CurrentLanguage = self.Lexer.name
        else :
            self.CurrentLanguage = None


        self.highlight()
        

    def updateTitle(self):
        fileName = "unnamed file"
        languageName = "plain text"
        if not self.FilePath is None :
            fileName = self.FilePath
        if not self.CurrentLanguage is None :
            languageName = self.CurrentLanguage
        
        root.wm_title(fileName + " - " + languageName + " - MicroIDE")

    def dummy(self):
        pass

    def newFile(self,event=None) :
        self.CODE_AREA.delete('1.0', END)
        self.FilePath = None
        self.CurrentLanguage = None
        
        self.FindLanguage()
        self.updateTitle()
    
    def saveFile(self,event=None) :
        if self.FilePath is None :
            self.FilePath = tkFileDialog.asksaveasfilename()
        
        with open(self.FilePath, 'w') as myfile :
            myfile.write(self.CODE_AREA.get("1.0",END))
        
        self.FindLanguage()
        self.updateTitle()

    def saveFileAs(self,event=None) :
        self.FilePath = tkFileDialog.asksaveasfilename()
        with open(self.FilePath, 'w') as myfile :
            myfile.write(self.CODE_AREA.get("1.0",END))
        self.FindLanguage()
        self.updateTitle()

    def openFile(self,event=None) :
        
        FilePath = tkFileDialog.askopenfilename()
        with open(FilePath, 'r') as myfile:
            self.newFile()
            self.CODE_AREA.insert("end",myfile.read())
        self.FilePath = FilePath
        self.highlight()
        
        self.FindLanguage()
        self.updateTitle()

    def close(self,event=None) :
        root.destroy()
    
    def setSyntexColours(self) :
        self.CODE_AREA.tag_configure("Token.Comment",
                                    foreground="#00ff00")
        self.CODE_AREA.tag_configure("Token.Comment.Hashbang",
                                    foreground="#00ff00")
        self.CODE_AREA.tag_configure("Token.Comment.Single", 
                                    foreground="#00ff00")
        
        self.CODE_AREA.tag_configure("Token.Literal.String",
                                    foreground="#ff99cc")
        self.CODE_AREA.tag_configure("Token.Literal.Number.Integer",
                                    foreground="#ff99cc")
        self.CODE_AREA.tag_configure("Token.Literal.Number.Float",
                                    foreground="#ff99cc")                            
        
        self.CODE_AREA.tag_configure("Token.Keyword",
                                    foreground="#aaaa00")
        self.CODE_AREA.tag_configure("Token.Keyword.Type",
                                    foreground="#aaaa00")
        

        self.CODE_AREA.tag_configure("Token.Name.Function",
                                    foreground="#ffff00")
        
        self.CODE_AREA.tag_configure("Token.Operator",
                                    foreground="#ff00ff")

    def createWidgets(self) :
        self.CODE_AREA = ScrolledText.ScrolledText(root)
        self.CODE_AREA.pack(fill=BOTH,expand=True)
        self.setSyntexColours()
        
        self.CODE_AREA.configure(bg = "#555555")
        self.highlight()
        self.CODE_AREA.bind("<KeyRelease>", self.highlight)
        self.CODE_AREA.bind("<Tab>", self.tab)

        self.MENU = Menu(root)

        filemenu = Menu(self.MENU, tearoff=0)
        filemenu.add_command(label="New", command=self.newFile)
        filemenu.add_command(label="Open", command=self.openFile)
        filemenu.add_command(label="Save", command=self.saveFile)
        filemenu.add_command(label="Save as...", command=self.saveFileAs)
        filemenu.add_command(label="Close", command=self.close)

        filemenu.add_separator()
        self.MENU.add_cascade(label="File", menu=filemenu)

        debugmenu = Menu(self.MENU, tearoff=0)

        debugmenu.add_command(label="Run", command=self.runFile)
        self.MENU.add_cascade(label="Debug", menu=debugmenu)

        root.bind("<Control-s>",self.saveFile)
        root.bind("<Control-n>",self.newFile)
        root.bind("<Control-o>",self.openFile)
        root.bind("<Control-Shift-s>",self.saveFileAs)
        self.bind("<Configure>", self.on_resize)
        root.config(menu=self.MENU)
        self.updateTitle()
    
    def runFile(self, event=None) :
        if not self.FilePath == None :
            call(["open","-a","Terminal",self.FilePath])

    def on_resize(self, event=None) :
        pass



    def highlight(self,event=None):
        if self.Lexer is None :
            return
        textStart = "1.0"
        textEnd = "end-1c"
        if not event is None :
            cursorIndex = self.CODE_AREA.index(INSERT)
            textStart = cursorIndex.split(".")[0] + ".0"
            textEnd = cursorIndex.split(".")[0] + ".end"

        self.CODE_AREA.mark_set("range_start", textStart)
        data = self.CODE_AREA.get(textStart, textEnd)
        for token, content in pygments.lex(data, self.Lexer):
            print token
            self.CODE_AREA.mark_set("range_end", "range_start + %dc" % len(content))
            self.CODE_AREA.tag_add(str(token), "range_start", "range_end")
            self.CODE_AREA.mark_set("range_start", "range_end")
    
    def tab(self,event=None) :
        self.CODE_AREA.insert(INSERT,"    ")
        return 'break'

    def __init__(self, master=None):
        Frame.__init__(self, master)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.createWidgets()
        self.pack()
        
    

if __name__ == "__main__" :
    root = Tk()
    app = MicroIDE(master=root)
    app.mainloop()
    root.destroy()