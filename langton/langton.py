"""
    langton.py
    Runs Langton's Ant
    Uses Tkinter's grid geometry manager for layout
    v1.3.2.19.15
    Changelog:
        Bug fixes for py2exe compatibility
        Filter harmless warnings
"""

from tkinter import *
from tkinter import messagebox
import numpy as np
import random
import tkDialog #this is a custom file
import time
import warnings
warnings.simplefilter('ignore')

#declare global variables
running = False
drawspeed = 0.0
d = random.randint(0, 3)#0=left, 1=up, 2=right, 3=down
antx = 30
anty = 30
generation = 0
step_called = False

#custom dialog classes
class speedDialog(tkDialog.Dialog):
    """
        A dialog box where the user will input a new speed.
    """
    def body(self, master):
        """
            Creates the body of the dialog
        """
        Label(master, text="Time to wait between loops (seconds): ").grid(row=0, column=0)

        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)

        return self.e1#initial focus

    def apply(self):
        global drawspeed
        drawspeed = float(self.e1.get())
        
#function definitions
def sim():
    """
        Runs Langton's Ant
    """
    global d, antx, anty, generation, running, step_called, drawspeed
    while (running == True or step_called == True):
        #reset deltas
        dx = dy = 0
        #check the fill of the cell the ant's on
        if (c.itemcget(rec[antx][anty], "fill") == "black"):
            if (d == 0):#change direction accordingly
                d = 1
            elif (d == 1):
                d = 2
            elif (d == 2):
                d = 3
            elif (d == 3):
                d = 0
            else:
                print("Error: Invalid direction")
            #update the label
            v1.set("Direction: "+str(d))
        elif (c.itemcget(rec[antx][anty], "fill") == "white"):
            if (d == 0):
                d = 3
            elif (d == 1):
                d = 0
            elif (d == 2):
                d = 1
            elif (d == 3):
                d = 2
            else:
                print("Error: Invalid direction")
            v1.set("Direction: "+str(d))
        #invert the cell the ant's on
        if (c.itemcget(rec[antx][anty], "fill") == "black"):
            c.itemconfig(rec[antx][anty], fill="white")
        elif (c.itemcget(rec[antx][anty], "fill") == "white"):
            c.itemconfig(rec[antx][anty], fill="black")
        #calculate deltas
        if (d == 0):
            dx = -1
        elif (d == 1):
            dy = -1
        elif (d == 2):
            dx = 1
        elif (d == 3):
            dy = 1
        else:
            print("Error: Invalid direction")
        #calculate new coords and wrap if necessary
        antx += dx
        anty += dy
        if (antx >= 60):
            antx = 0
            c.move(ant, -600, 0)
        if (antx <= -1):
            antx = 59
            c.move(ant, 600, 0)
        if (anty >= 60):
            anty = 0
            c.move(ant, 0, -600)
        if (anty <= -1):
            anty = 59
            c.move(ant, 0, 600)
        c.move(ant, dx*10, dy*10)
        #update gen label
        generation += 1
        v2.set("Generation: "+str(generation))
        #check if we need to stop, and call update() to keep the speed under control
        if (step_called == True):
            step_called = False
        if (running == True):
            time.sleep(drawspeed)
            c.update()

def step():
    """
        Continues the simulation for one generation
    """
    global running, step_called
    if (running == True):
        running = False
    step_called = True
    sim()

def run():
    """
        Continues the simulation until the user stops it
    """
    global running
    running = True
    sim()

def stop():
    """
        Stops the simulation
    """
    global running
    running = False
    sim()

def clear():
    """
        Clears the grid to all white
    """
    for i in range(0, 60):
        for j in range(0, 60):
            c.itemconfig(rec[i][j], fill="white")
    c.update()

def about():
    """
        Shows information about the program and simulation
    """
    messagebox.showinfo("About", "Langton's Ant v0.8.2.3.15\n\nLangton's Ant is a simple, 4-state Turing machine that is one of the simpler demonstrations of cellular automata. When the \"ant\" is on a white square, it turns left and inverts the color, and if it is on a black square, it turns right and inverts the color.\nhttp://en.wikipedia.org/wiki/Langton%27s_ant")

def speed():
    """
        Prompts the user to adjust the speed
    """
    d = speedDialog(root, title="Speed")
    root.wait_window(d)
    
#create main window
root = Tk()
root.title("Langton's Ant")

#create a canvas object, where all the graphics will be shown
c = Canvas(root, width=600, height=600)
c.grid(row=1, column=0, columnspan=3)

#add controls
step = Button(root, text="Step", command=step)
step.grid(row=2, column=0, sticky=W+E)#we want the buttons to fill the bottom row

run = Button(root, text="Run", command=run)
run.grid(row=2, column=1, sticky=W+E)

stop = Button(root, text="Stop", command=stop)
stop.grid(row=2, column=2, sticky=W+E)

#add labels and corresponding variables
v1 = StringVar(root)
v2 = StringVar(root)

#add frame for separation
frame = LabelFrame(root)
frame.grid(row=0, column=0, columnspan=3, sticky=W+E)

gen = Label(frame, textvariable=v2)
gen.grid(row=0, column=0, sticky=W)
v2.set("Generation: "+str(generation))

dire = Label(frame, textvariable=v1)
dire.grid(row=0, column=1, sticky=W+E)
v1.set("Direction: "+str(d))

#add menu bar with cascade menu and commands
menubar = Menu(root)
simmenu = Menu(menubar, tearoff=0)
simmenu.add_command(label="Clear Field", command=clear)
simmenu.add_command(label="Speed...", command=speed)
simmenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="Simulation", menu=simmenu)
menubar.add_command(label="About", command=about)
root.config(menu=menubar)

#create the grid
for i in range(0, 600, 10):#horizontals
    c.create_line(0, i, 600, i)
for i in range(0, 600, 10):#verticals
    c.create_line(i, 0, i, 600)

#this is the array that will hold all of the cells for easy access
rec = np.ndarray(shape=(60, 60), dtype=Widget)

#create rectangles to track states
for i in range(0, 60):
    for j in range(0, 60):
        rec[i][j] = c.create_rectangle(i*10, j*10, (i*10)+10, (j*10)+10, fill="white")

#place the ant
ant = c.create_rectangle(300, 300, 310, 310, fill="red")#screen coords to grid coords are 1:10

#render window and wait for events
root.mainloop()
