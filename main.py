﻿#const vars
#color
BG_COLOR = "white"
LINE_COLOR = "black"
NOTE_KINDS=[["Tap","red"],["Slide_s","yellow"],["Slide_B","green"],["Swing","blue"],["MPMChange","purple"]]
#about resolution
MAIN_RES_W=1366
MAIN_RES_H=768
CHART_Y=100
NOTE_EDGE=10
#default values
SELECTED_NOTE = 0;
PAGE=0
IS_SNAP_ENABLED=True
DIV_IN_MEASURE=4
DIV_IN_LINE=4

#↓program
from tkinter import *
from tkinter import ttk
import pickle

root = Tk()
root.geometry(str(MAIN_RES_W)+"x"+str(MAIN_RES_H+CHART_Y))


#control panel
class ControlPanel(Frame):
    def __init__(self,master=None,update=None):
        super().__init__(master)#Frame(master)
        self.selectedNote=SELECTED_NOTE
        self.page=PAGE
        self.isSnapEnabled = IS_SNAP_ENABLED
        self.divInMeasure = StringVar(value=str(DIV_IN_MEASURE))
        self.divInLine = StringVar(value=str(DIV_IN_LINE))
        self.update = update
        #system buttons
        ttk.Button(self, text="Open", command=self.file_open).grid(column=0, row=0)
        ttk.Button(self, text="Save", command=self.file_save).grid(column=1, row=0)
        ttk.Button(self, text="Open(Pickle)", command=file_open_pickle).grid(column=2, row=0)
        ttk.Button(self, text="Save(Pickle)", command=file_save_pickle).grid(column=3, row=0)
        ttk.Button(self, text="Config", command=self.config).grid(column=4, row=0)
        #select a kind of note
        for i in range(0,5):
            ttk.Button(self, text=NOTE_KINDS[i][0], command=self.setNoteLabel(i)).grid(column=i, row=1)
        ttk.Label(self, text="Selected:").grid(column=0, row=2)
        self.selectedNoteLabel = ttk.Label(self, text=NOTE_KINDS[SELECTED_NOTE][0])
        self.selectedNoteLabel.grid(column=1, row=2)
        ttk.Label(self, text="Value:").grid(column=3, row=2)
        self.mpmEntry = Entry(self,width=10)
        self.mpmEntry.insert(END,"30")
        self.mpmEntry.grid(column=4,row=2)
        #page move
        ttk.Button(self, text="←", command=self.previousPage).grid(column=5, row=0)
        ttk.Button(self, text="→", command=self.nextPage).grid(column=6, row=0)
        ttk.Label(self, text="Page:").grid(column=7, row=0)
        self.pageLabel = ttk.Label(self, text="0")
        self.pageLabel.grid(column=8, row=0)
        #note snap
        self.snapButton = ttk.Button(self, text="Snap:On" if self.isSnapEnabled else "Snap:Off", command=self.toggleSnap)
        self.snapButton.grid(column=14, row=0);
        ttk.Label(self, text="Division in measure:").grid(column=13, row=1)
        Entry(self,width=10,textvariable=self.divInMeasure).grid(column=14,row=1)
        ttk.Label(self, text="Division in line:").grid(column=13, row=2)
        Entry(self,width=10,textvariable=self.divInLine).grid(column=14,row=2)

        self.divInMeasure.trace_add('write',update)
        self.divInLine.trace_add('write',update)
    def file_open(self):
        print("placeholder-open")
    def file_save(self):
        print("placeholder-save")
    def config(self):
        print("placeholder-config")
    def setNoteLabel(self,index):
        def inner():
            self.selectedNote = index
            self.selectedNoteLabel["text"] = NOTE_KINDS[index][0]
        return inner
    def previousPage(self):
        self.page = max(0,self.page-1)
        self.pageLabel["text"] = str(self.page)
        self.update(0,0,0)
    def nextPage(self):
        self.page = self.page+1
        self.pageLabel["text"] = str(self.page)
        self.update(0,0,0)
    def toggleSnap(self):
        self.isSnapEnabled = not self.isSnapEnabled
        self.snapButton["text"] = "Snap:On" if self.isSnapEnabled else "Snap:Off"
        self.update(0,0,0)
    def getSelf(self):
        return self

#chart editor
class ChartEditor(Canvas):
    def __init__(self,controlpanel,chart,number,master=None):
        #define variable
        self.canvasResW = MAIN_RES_W/4 #8分割の画面編成にするために
        self.canvasResH = MAIN_RES_H/2 #横4分割と縦2分割でそれぞれ1つのエディタを割り振る
        self.notes = []#note([beginX,EndX,BeginY,noteKind,MPM])
        #make canvas(self)
        super().__init__(master, width = self.canvasResW, height = self.canvasResH)#Canvas(master,width=~,height=~)
        self.bind("<ButtonPress-1>",self.canvasClicked)
        self.bind("<Button1-Motion>", self.canvasDragged)
        self.bind("<ButtonRelease-1>",self.canvasReleased)
        self.update(controlpanel,chart,number=number)
    def update(self,controlpanel,chart,number=0):
        self.selectedNote=controlpanel.selectedNote
        try:
            self.divInMeasure = max(1,int(controlpanel.divInMeasure.get()))
        except ValueError:
            self.divInMeasure = 1
        try:
            self.divInLine = max(1,int(controlpanel.divInLine.get()))
        except ValueError:
            self.divInLine = 1
        self.isSnapEnabled = controlpanel.isSnapEnabled
        self.mpm = controlpanel.mpmEntry.get()
        self.measureDivH = self.canvasResH/self.divInMeasure
        self.lineDivW = self.canvasResW/self.divInLine
        self.page = controlpanel.page
        try:
            self.notes = chart[self.page+number]
        except IndexError:
            chart.append([])
            self.notes = chart[self.page+number]
        self.draw()
    def draw(self):
        self.delete('all')
        self.create_rectangle(0, 0, self.canvasResW, self.canvasResH, fill=BG_COLOR)
        for i in range(0,self.divInMeasure):
            self.create_line(0,self.measureDivH*i,self.canvasResW,self.measureDivH*i,fill=LINE_COLOR)
        for i in range(0,self.divInLine):
            self.create_line(self.lineDivW*i,0,self.lineDivW*i,self.canvasResH,fill=LINE_COLOR)
        for note in self.notes:
            self.create_line(note[0],note[2],note[1],note[2],fill=NOTE_KINDS[note[3]][1])
            self.create_line(note[0],note[2]-NOTE_EDGE,note[0],note[2]+NOTE_EDGE,fill=NOTE_KINDS[note[3]][1],width=3)
            self.create_line(note[1],note[2]-NOTE_EDGE,note[1],note[2]+NOTE_EDGE,fill=NOTE_KINDS[note[3]][1],width=3)
    def canvasClicked(self,event):
        self.lineBeginX=event.x
        self.lineBeginY=event.y
        if(self.isSnapEnabled):
            self.lineBeginX=round(self.lineBeginX/self.lineDivW)*self.lineDivW
            self.lineBeginY=round(self.lineBeginY/self.measureDivH)*self.measureDivH
            if(self.lineBeginY==0):
                self.lineBeginY=self.measureDivH
    def canvasDragged(self,event):
        self.lineEndX=min(self.canvasResW,max(0,event.x))
        if(self.isSnapEnabled):
            self.lineEndX=round(self.lineEndX/self.lineDivW)*self.lineDivW
        self.draw()
        if(self.lineBeginX != self.lineEndX):
            self.create_line(self.lineBeginX,self.lineBeginY,self.lineEndX,self.lineBeginY,fill=NOTE_KINDS[self.selectedNote][1])
    def canvasReleased(self,event):
        self.lineEndX=min(self.canvasResW,max(0,event.x))
        if(self.isSnapEnabled):
            self.lineEndX=round(self.lineEndX/self.lineDivW)*self.lineDivW
        self.notes.append([self.lineBeginX,self.lineEndX,self.lineBeginY,self.selectedNote,self.mpm])
        self.draw()

#↓procedural
chartLower = [[],[],[],[]]
chartUpper = [[],[],[],[]]
def updateAll(arg1,arg2,arg3):
    for i in range(0,4):
        editorsLower[i].update(controlpanel,chartLower,number=i)
        editorsUpper[i].update(controlpanel,chartUpper,number=i)

def file_open_pickle():
    global chartLower,chartUpper
    with open('chart.pickle', mode='br') as fi:
        chart = pickle.load(fi)
        chartLower = chart[0]
        chartUpper = chart[1]
    updateAll(0,0,0)
def file_save_pickle():
    with open('chart.pickle', mode='wb') as fo:
        pickle.dump([chartLower,chartUpper], fo)

controlpanel = ControlPanel(master=root,update=updateAll)
controlpanel.grid()
editorsLower = []
editorsUpper = []
for i in range(0,4):
    editorLower = ChartEditor(controlpanel,chartLower,i,master=root)
    editorUpper = ChartEditor(controlpanel,chartUpper,i,master=root)
    editorsLower.append(editorLower)
    editorsUpper.append(editorUpper)
    editorsLower[i].place(x=(int)(i/2)*MAIN_RES_W/2             ,y=CHART_Y+(1-(i%2))*MAIN_RES_H/2)
    editorsUpper[i].place(x=(int)(i/2)*MAIN_RES_W/2+MAIN_RES_W/4,y=CHART_Y+(1-(i%2))*MAIN_RES_H/2)
root.mainloop()