import tkinter as tk
from tkinter import * 
import os

# these are the dimensions for baby screen
HEIGHT = 600
WIDTH = 1040 

TITLE = "DJM FOIL Test"

script_dir = "/home/djm/FOIL_test/scripts"
image_dir = "./img"

def bw_test():
    """
    Main method that will call iperf scripts and test BW
    iperf scripts will send output to file in which results will be retrieved
    """
    results["text"] = "You passed"

def is_connected():
    """
    ping one iface from the other. success -> True
    run 'route_config.sh' if not connected
    This method should be ran every couple seconds or so
    """
    connected["text"] = "Not Connected"
    return True

root = tk.Tk()
root.title(TITLE)

canvas = tk.Canvas(root,height=HEIGHT, width=WIDTH)
canvas.pack()

#CANNOT use jpg for background
#bg_image = tk.PhotoImage(file='./space1.png')
#bg_label = tk.Label(root, image=bg_image)
#bg_label.place(relwidth=1, relheight=1)

header = tk.Label(root, text=TITLE, font=('Ubuntu', 30))
header.place(relx=0.5, rely=0, relwidth=0.75, anchor='n')

# TOP_FRAME CONFIGURATION

#bd =5 gives us a lil border for all of our widgets
top_frame = tk.Frame(root, bg="white", bd=5)
# .5 = 1/2 of screen space
# achor=n ensures frame will be centered
top_frame.place(relx=0.5, rely=0.11, relwidth=0.75, relheight=0.1, anchor='n')

connected = tk.Label(top_frame, text="Connected/Not Connected", 
    font=('Ubuntu', 20), bg="white", anchor='w', justify="left")
connected.place (relx=0.01, relwidth=0.50, relheight = 1)

button = tk.Button(top_frame, text="Run Test", font=('Ubuntu', 12), 
    command=bw_test)
button.place(relx=0.7, relheight=1, relwidth=0.3)

# END OF TOP_FRAME COMPONENTS

lower_frame = tk.Frame(root, bg="white", bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6,anchor='n')

result_head = tk.Label(lower_frame, text="Test Results:", font=('Ubuntu', 12), 
    bg="white",anchor='w',justify='left')
result_head.place(relwidth = 1, relheight=.08)

results = tk.Label(lower_frame, font=('Ubuntu', 15), anchor='nw', 
    justify='left', bd=4) 
results.place(rely=.1, relwidth=1, relheight=.9)

root.mainloop()

