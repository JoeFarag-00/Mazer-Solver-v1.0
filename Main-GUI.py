from tkinter import *
import time

class Create_Maze():
   
    def __init__(self, master, position):
        self.button_obj = Button ( 
            master, command=self.Make_Maze, width=3, height=1, bg='white')
        self.position = position #Pos not working btk btk btk
        self.adjacent = []
        self.Cwall_Stat = 0
        self.Cstart_Stat = 0
        self.CEnd_Stat = 0
        self.Construct_Wall = False
        self.start_dist = 2e200

    def Make_Maze(self):
        
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

            for node in GridList.values():
                if (node.position != End) and (node.position != start):
                    node.goal = 0
                    node.button_obj.configure(bg='white')

    def Create_Wall(self):

        if self.Cstart_Stat == 0 and self.CEnd_Stat == 0:
            self.Cwall_Stat = (self.Cwall_Stat+1) % 2
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
    global frame1
    global Maze_Status
    if Maze_Status == 2:
        for button in GridList:
            if frame1.winfo_containing(event.x_root, event.y_root) is GridList[button].button_obj:
                GridList[button].mouse_entered()
                root.update()


rows = 30
columns = 30
GridList = {}
Maze_Status = 0
start = None
End = None

root = Tk()
root.title('Manyoon Maze')

frame1 = Frame(root, bg='black', bd=2)

for row in range(rows):
    for column in range(columns):

        GridList[(row, column)] = Create_Maze(
            master=frame1, position=(row, column))
        GridList[(row, column)].button_obj.grid(row=row, column=column)

frame1.bind_all("<ButtonRelease-1>", mouse_up)
frame1.bind_all("<B1-Motion>", mouse_motion)
frame1.pack()

frame2 = Frame(root)

label = Label(frame2, text='Choose a Start position')
label.pack(side=LEFT)
stepButton = Button(frame2, text='NEXT', width=10, height=3, command=Fill_Maze_GUI)
stepButton.pack(side=RIGHT)

frame2.pack()
root.mainloop()
