from tkinter import *

root = Tk()
root.attributes('-fullscreen', True)

def onClick(r,c):
    if buttons[r][c]["bg"] == "Blue":
        buttons[r][c].config(bg = "Yellow")
    elif buttons[r][c]["bg"] == "Yellow":
        buttons[r][c].config(bg = "Blue")


Rows = 30
Cols = 60
buttons = [[None]*Cols for i in range(Rows)] # for storing references of buttons

for row in range(0, Rows):
    for col in range(0, Cols):
        buttons[row][col] = Button(root, padx = 10, pady = 3, bg = "Blue", command = lambda r = row, c = col,: onClick(r, c))
        buttons[row][col].grid(row = row, column = col)

root.mainloop()