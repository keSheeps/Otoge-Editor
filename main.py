from tkinter import *
from tkinter import ttk

#定数宣言
#色関連
bg_color = "white"
line_color = "black"
notes=[["Tap","red"],["Slide_s","yellow"],["Slide_B","green"],["Swing","blue"],["MPMChange","purple"],]
#画面解像度関連
mainResW=1366
mainResH=768
chartY=100
#初期状態
page=0
isSnapEnabled=True

#メイン処理
selectedNote = 0;
root = Tk()
root.geometry(str(mainResW)+"x"+str(mainResH+chartY))
#上部操作パネル
def file_open():
    print("placeholder-open")
def file_save():
    print("placeholder-save")
def config():
    print("placeholder-config")
def setNoteLabel(index):
    global notes
    selectedNoteLabel["text"] = notes[index][0]
def Tap():
    selectedNoteLabel["text"] = "Tap"
def Slide_s():
    selectedNoteLabel["text"] = "Slide_s"
def Slide_B():
    selectedNoteLabel["text"] = "Slide_B"
def Swing():
    selectedNoteLabel["text"] = "Swing"
def MPMChange():
    selectedNoteLabel["text"] = "MPMChange"
def previousPage():
    global page
    page = max(0,page-1)
    pageLabel["text"] = str(page)
def nextPage():
    global page
    page = page+1
    pageLabel["text"] = str(page)
def toggleSnap():
    global isSnapEnabled
    isSnapEnabled = not isSnapEnabled
    snapButton["text"] = "Snap:On" if isSnapEnabled else "Snap:Off"
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Button(frm, text="Open", command=file_open).grid(column=0, row=0)
ttk.Button(frm, text="Save", command=file_save).grid(column=1, row=0)
ttk.Button(frm, text="Config", command=config).grid(column=2, row=0)
ttk.Label(frm, text="Selected:").grid(column=3, row=0)
selectedNoteLabel = ttk.Label(frm, text="Tap")
selectedNoteLabel.grid(column=4, row=0)
ttk.Button(frm, text="Tap", command=Tap).grid(column=5, row=0)
ttk.Button(frm, text="Slide_s", command=Slide_s).grid(column=6, row=0)
ttk.Button(frm, text="Slide_B", command=Slide_B).grid(column=7, row=0)
ttk.Button(frm, text="Swing", command=Swing).grid(column=8, row=0)
ttk.Button(frm, text="MPMChange", command=MPMChange).grid(column=9, row=0)
ttk.Label(frm, text="Value:").grid(column=8, row=1)
mpmEntry = Entry(frm,width=10)
mpmEntry.insert(END,"30")
mpmEntry.grid(column=9,row=1)
ttk.Label(frm, text="Page:").grid(column=10, row=0)
pageLabel = ttk.Label(frm, text="0")
pageLabel.grid(column=11, row=0)
ttk.Button(frm, text="←", command=previousPage).grid(column=12, row=0)
ttk.Button(frm, text="→", command=nextPage).grid(column=13, row=0)
snapButton = ttk.Button(frm, text="Snap:On" if isSnapEnabled else "Snap:Off", command=toggleSnap)
snapButton.grid(column=14, row=0);
ttk.Label(frm, text="Division in measure:").grid(column=13, row=1)
divInMeasureEntry = Entry(frm,width=10)
divInMeasureEntry.insert(END,"4")
divInMeasureEntry.grid(column=14,row=1)
ttk.Label(frm, text="Division in line:").grid(column=13, row=2)
divInLineEntry = Entry(frm,width=10)
divInLineEntry.insert(END,"4")
divInLineEntry.grid(column=14,row=2)

#譜面領域
lineBeginX=0
lineBeginY=0

canvasResW = mainResW/4
canvasResH = mainResH/2
measureDivH = canvasResH/(int(divInMeasureEntry.get()))
lineDivW = canvasResW/(int(divInLineEntry.get()))

notes = []#ノート
def draw():
    global canvas,canvasResW,canvasResH,measureDivH,lineDivW
    canvas.create_rectangle(0, 0, canvasResW, canvasResH, fill=bg_color)
    for i in range(0,int(divInMeasureEntry.get())):
        canvas.create_line(0,measureDivH*i,canvasResW,measureDivH*i,fill=line_color)
    for i in range(0,int(divInLineEntry.get())):
        canvas.create_line(lineDivW*i,0,lineDivW*i,canvasResH,fill=line_color)
def canvasClicked(event):
    global lineBeginX,lineBeginY
    lineBeginX=event.x
    lineBeginY=event.y
def canvasDragged(event):
    global lineBeginX,lineBeginY,canvas
    draw()
    canvas.create_line(lineBeginX,lineBeginY,event.x,lineBeginY,fill=notes[selectedNote][1])
def canvasReleased(event):
    global lineBeginX,lineBeginY
    notes.append([lineBeginX,event.x,lineBeginY,])
canvas = Canvas(root, width = canvasResW, height = canvasResH)
canvas.bind("<ButtonPress-1>",canvasClicked)
canvas.bind("<Button1-Motion>", canvasDragged)
canvas.bind("<ButtonRelease-1>",canvasReleased)
canvas.place(x=0,y=chartY)
draw()

root.mainloop()