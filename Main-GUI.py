from tkinter import *
import time
from turtle import bgcolor

root = Tk()
root.title('Manyoon Maze')

class Create_Maze():
   
    def __init__(self, master, position):
        self.button_obj = Button ( 
            master, command=self.Maze_Status, width=3, height=1, bg='white')
        self.position = position #Pos not working btk btk btk
        self.adjacent = []
        self.Cwall_Stat = 0
        self.Cstart_Stat = 0
        self.CEnd_Stat = 0
        self.Construct_Wall = False
        self.start_dist = 2e200

    def Maze_Status(self):
        
        global Maze_Status
        if Maze_Status == 0:
            self.Create_Start()
        elif Maze_Status == 1:
            self.Create_End()
        elif Maze_Status == 2:
            self.Create_Wall()
        else:
            pass

    def Create_Start(self):
       
        global start
        global GridList
        start = self.position
        self.Cstart_Stat = 1
        self.button_obj.configure(bg='green3')
        StepBtn.configure(bg='red',text='End')
        for node in GridList.values():
            if node.position != start:
                node.start = 0
                node.button_obj.configure(bg='white')

    def Create_End(self):
        
        global End
        global start
        global GridList
        if self.Cstart_Stat != 1:

            End = self.position
            self.CEnd_Stat = 1
            self.button_obj.configure(bg='red')
            StepBtn.configure(bg='grey', fg='white',text='Add Walls')
            for node in GridList.values():
                if (node.position != End) and (node.position != start):
                    node.goal = 0
                    node.button_obj.configure(bg='white')
                    #print(position)

    def Create_Wall(self):

        if self.Cstart_Stat == 0 and self.CEnd_Stat == 0:
            self.Cwall_Stat = (self.Cwall_Stat+1) % 2
            StepBtn.configure(bg='light blue', fg='black',text='visualize')
            if self.Cwall_Stat == 0:
                self.button_obj.configure(bg='white')
            else:
                self.button_obj.configure(bg='black')

    def mouse_entered(self):
        
        if self.Construct_Wall == False:
            self.Create_Wall()
            self.Construct_Wall = True

    def __str__(self):
        return f'Vector {self.position}'


def Fill_Maze_GUI():
    
    global Maze_Status
    global label
    global start
    global End

    Maze_Status += 1

    if Maze_Status == 1:
        if start == None:
            GridList[(0, 0)].createStart()
        label.configure(text='Choose an End position')
    elif Maze_Status == 2:
        if End == None:
            GridList[(rows-1, columns-1)].createGoal()
        label.configure(text='Construct Walls')


def mouse_up(event):
    
    for button in GridList:
        GridList[button].wall_changed = False


def mouse_motion(event):
    global Grid_Btns
    global Maze_Status
    if Maze_Status == 2:
        for button in GridList:
            if Grid_Btns.winfo_containing(event.x_root, event.y_root) is GridList[button].button_obj:
                GridList[button].mouse_entered()
                root.update()

GridList = {}
rows = 30
columns = 30
Maze_Status = 0
start = None
End = None

Btn1 = Frame(root)
label = Label(Btn1, text='WELCOME TO MAZE PATHFINDING VISUALIZER')
label.config(font=('Arial', 26))
label.pack(side=TOP, pady=5)
StepBtn = Button(Btn1, text='Start', width=20, height=3, bg="green2" ,command=Fill_Maze_GUI, font=('Arial', 10))
# StepBtn.place(x=1000,y=20)
StepBtn.pack(pady=8)
Btn1.pack()

# Btn2 = Frame(root)
# label = Label(Btn2, text='Choose an Algorithim')
# label.pack(side=TOP)
# AlgoBtn = Button(Btn2, text='NEXT', width=10, height=3, bg="green2" ,command=Fill_Maze_GUI)
# AlgoBtn.pack(side=BOTTOM, pady=20)
# Btn1.pack()

Grid_Btns = Frame(root, bg='black', bd=10)
for row in range(rows):
    for column in range(columns):

        GridList[(row, column)] = Create_Maze(
            master=Grid_Btns, position=(row, column))
        GridList[(row, column)].button_obj.grid(row=row, column=column)

Grid_Btns.bind_all("<ButtonRelease-1>", mouse_up)
Grid_Btns.bind_all("<B1-Motion>", mouse_motion)
Grid_Btns.pack()

root.mainloop()
