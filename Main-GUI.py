from tkinter import *
import time
import os
import sys

root = Tk()
root.title('AI Maze')
root.configure(bg="black")

class Create_Maze():

    def __init__(self, master, pos):
        self.button_obj = Button(
            master, command=self.Maze_Status, width=3, height=1, bg='white')
        self.position = pos
        self.adjacent = []
        self.wall = 0
        self.start = 0
        self.goal = 0
        self.wall_changed = False
        self.Algo_Stat = 0
        self.start_dist = 0

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
        # elif Maze_Status == 3:
        #     self.Start_BFS()
        # elif Maze_Status == 4:
        #     self.Start_DFS()

    def Create_Start(self):
        global start
        global GridList
        start = self.position
        self.start = 1
        self.button_obj.configure(bg='green3')
        Nxt_Btn.configure(bg='red',text='Set End')
        for node in GridList.values():
            if node.position != start:
                node.start = 0
                node.button_obj.configure(bg='white')

    def Create_End(self):
        global End
        global start
        global GridList
        if self.start != 1:
            End = self.position
            self.goal = 1
            self.button_obj.configure(bg='red')
            Nxt_Btn.configure(bg='grey', fg='white',text='Add Walls')
            for node in GridList.values():
                if (node.position != End) and (node.position != start):
                    node.goal = 0
                    node.button_obj.configure(bg='white')
                    #print(position)

    def Create_Wall(self):
        if self.start == 0 and self.goal == 0:
            self.wall = (self.wall+1) % 2
            Nxt_Btn.configure(bg='light blue', fg='black',text='Visualize Mode')
            # Nxt_Btn.after(1000, Nxt_Btn.destroy)
            if self.wall == 0:
                self.button_obj.configure(bg='white')
            else:
                self.button_obj.configure(bg='black')
                # if self.btnDstat==False:
                #     StepBtn.destroy()
                #     btnDstat=True
        
    def findAdjacents(self):
        global start
        for node_position in GridList:
            if abs(node_position[0]-self.position[0]) <= 1 and abs(node_position[1]-self.position[1]) <= 1:
                if GridList[node_position].wall == 0 and node_position != (self.position or start):
                    self.adjacent.append(node_position)
        return self.adjacent

    def adjacentStartDists(self, GridList):
        for node in self.adjacent:
            node = GridList[node]
            dist = round(((node.position[0]-self.position[0]) **2+(node.position[1]-self.position[1])**2)**0.5, 3)
            node.start_dist = min(node.start_dist, self.start_dist + dist)

    def __str__(self):
        return f'Vector {self.position}'
    
    def mouse_entered(self):
        if self.wall_changed == False:
            self.Create_Wall()
            self.wall_changed = True

def Mouse_Up(event):
    for button in GridList:
        GridList[button].wall_changed = False

def Mouse_Move(event):
    global Grid_Btns
    global Maze_Status
    if Maze_Status == 2:
        for button in GridList:
            if Grid_Btns.winfo_containing(event.x_root, event.y_root) is GridList[button].button_obj:
                GridList[button].mouse_entered()
                root.update()
                
def GuidPath_Color(path):
    for node in path[1:-1]: 
        GridList[node].button_obj.configure(bg='green')
        
def Reset_Window():
    root.destroy()
    os.system('Main-GUI.py')
    #os.startfile("Main-GUI.py")
    # root.mainloop()
    # os.execl(sys.executable, sys.executable, *sys.argv)

    
def Start_BFS():
    global Algo_Stat
    Algo_Stat=1
    label.configure(text='Using BFS to look for End destination...')
    path = BFS(start, End)
    if path != None:
        label.configure(text='Path Found')
        GuidPath_Color(path)
    else:
        label.configure(text='Path Not found:')
        
def Start_DFS():
    global Algo_Stat
    Algo_Stat = 2
    label.configure(text='Using DFS to look for End destination...')
    path = DFS(start, End)
    if path != None:
        label.configure(text='Path Found')
        GuidPath_Color(path)
    else:
        label.configure(text='Path Not found:')
    
def Fill_Maze_GUI():
    global Maze_Status
    global label
    global start
    global End
    
    Maze_Status += 1
    
    if Maze_Status == 1:
        if start == None:
            GridList[(0, 0)].Create_Start()
        label.configure(text='Choose an End position')
    elif Maze_Status == 2:
        if End == None:
            GridList[(rows-1, columns-1)].Create_End()
        label.configure(text='Construct your walls')
    elif Algo_Stat == 1:
        Start_BFS()
    elif Algo_Stat == 2:
        Start_DFS()
       

def BFS(start, goal):
    global root

    current = start
    path = [start]

    GridList[start].start_dist = 0
    goal_dist = round(((start[0]-goal[0])**2+(start[1]-goal[1])**2)**0.5, 3)
    queue = {GridList[start].start_dist: [(current,  path)]}
    in_queue = [start]

    while queue != []:
        min_dist = min(queue)
        (current, path) = queue[min_dist].pop(0)
        if queue[min_dist] == []:
            del queue[min_dist]
        current = GridList[current]
        current.findAdjacents()
        current.adjacentStartDists(GridList)

        for nxt in current.adjacent:

            if nxt == goal:
                path.append(nxt)
                return path
            else:
                if nxt not in in_queue:

                    in_queue.append(nxt)

                    shortest_dist = GridList[nxt].start_dist

                    if shortest_dist in queue:
                        queue[shortest_dist].append(((nxt), path+[nxt]))
                    else:
                        queue[shortest_dist] = [((nxt), path+[nxt])]

                    GridList[nxt].button_obj.configure(
                        bg='Blue', relief=SUNKEN)
                    root.update()

                    time.sleep(0.01)

def DFS(start, goal):

    current = start
    path = [start]

    GridList[start].start_dist = 0
    goal_dist = round(((start[0]-goal[0])**2+(start[1]-goal[1])**2)**0.5, 3)

    queue = {goal_dist: [(current,  path)]}
    in_queue = [start]

    while queue != []:
        min_dist = min(queue)
        (current, path) = queue[min_dist].pop(0)
        if queue[min_dist] == []:
            del queue[min_dist]
        current = GridList[current]
        current.findAdjacents()
        current.adjacentStartDists(GridList)

        for nxt in current.adjacent:

            if nxt == goal:
                path.append(nxt)
                return path
            
            else:
                
                if nxt not in in_queue:

                    in_queue.append(nxt)
                    goal_dist = round(
                        ((nxt[0]-goal[0])**2+(nxt[1]-goal[1])**2)**0.5, 3)

                    if goal_dist in queue:
                        queue[goal_dist].append(((nxt), path+[nxt]))
                    else:
                        queue[goal_dist] = [((nxt), path+[nxt])]

                    GridList[nxt].button_obj.configure(
                        bg='Blue', relief=SUNKEN)
                    root.update()

                    time.sleep(0.05)
GridList = {}
rows = 30
columns = 30
Maze_Status = 0
start = None
End = None

label = Label(text='WELCOME TO MAZE PATHFINDING VISUALIZER')
label.config(font=('Arial', 26))
label.pack(side=TOP, pady=5)

Btn_Type = Frame(root)
# Btn_Type2 = Frame(root)
# Btn_Type3 = Frame(root)

Nxt_Btn = Button(Btn_Type, text='Set Start', width=20, height=3, bg="green2",font=('Arial', 10), command=Fill_Maze_GUI)
Nxt_Btn.grid(row=1,column=0,padx=5)

btn2=Button(Btn_Type,text='BFS',width=20, height=3, font=('Arial', 10),bg="light blue",command=Start_BFS)
btn2.grid(row=1,column=1,padx=5)

btn3=Button(Btn_Type,text='DFS',width=20, height=3, font=('Arial', 10),bg="light blue", command=Start_DFS)
btn3.grid(row=1,column=2,padx=5)

btn4=Button(Btn_Type,text='Reset',width=20, height=3, font=('Arial', 10),bg="Red", command=Reset_Window)
btn4.grid(row=1,column=3,padx=5)

Btn_Type.pack(pady=5)
# Btn_Type2.pack(pady=5)
# Btn_Type3.pack(pady=5)

Grid_Btns = Frame(root, bg='black', bd=2)
for row in range(rows):
    for column in range(columns):

        GridList[(row, column)] = Create_Maze(
            master=Grid_Btns, pos=(row, column))
        GridList[(row, column)].button_obj.grid(row=row, column=column)

Grid_Btns.bind_all("<ButtonRelease-1>", Mouse_Up)
Grid_Btns.bind_all("<B1-Motion>", Mouse_Move)
Grid_Btns.pack()

root.mainloop()
