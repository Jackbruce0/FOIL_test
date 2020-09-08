import tkinter as tk
from tkinter import * 
import subprocess 
import os
import threading
import ctypes
import time

# Dimensions for baby screen
HEIGHT = 600
WIDTH = 1040 

TITLE = "DJM FOIL Test"

# File locations
script_dir = "/home/djm/FOIL_test/scripts/"
image_dir = "./img/"
results_file = "/tmp/foil_test.txt"

# Test result vars
dl_stats = {'transferred_bytes': 0, 'bps': 0, 'duration': 0}
ul_stats = {'transferred_bytes': 0, 'bps': 0, 'duration': 0} 

bw_thread = None

class bw_test_thread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        # target function of the thread class
        bw_test()

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
            ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
                

def bw_test_helper():
    """
    Helper function for making bw_test a thread
    """
    global bw_thread
    bw_thread = bw_test_thread('Test Thread') 
    bw_thread.start()

def bw_test_stop():
    """
    Stops currently running bw_test thread
    """
    bw_thread.raise_exception()
    #bw_thread.join()
    run_test_btn.config(text="Run Test")
    run_test_btn.update_idletasks()
    

def bw_test():
    """
    Main method that will call iperf scripts and test BW
    iperf scripts will send output to file in which results will be retrieved
    """
    run_test_btn.config(text="Testing...")
    run_test_btn.update_idletasks()

    results["text"] = "" 
    results.update_idletasks()

    if not is_connected():
        results["text"] = "TEST FAILED"
        run_test_btn.config(text="Run Test")
        run_test_btn.update_idletasks()
        return
    subprocess.call([script_dir+"run_test.sh"])
    
    """
    VERY sloppy line_count variable explained
    0 -> first line (skip)
    1 -> dl data line
    2 -> ul data line
    """
    line_count = 0
    with open(results_file) as stats:
        for line in stats:
            csv_list = line.split(",")
            if line_count == 0:
                pass
            elif line_count == 1:
                dl_stats['transferred_bytes'] = float(csv_list[7])
                dl_stats['bps'] = float(csv_list[8])
                dl_stats['duration'] = float(csv_list[6].split("-")[1])
                print_results(dl_stats, "DOWNLOAD") 

            elif line_count == 2:
                ul_stats['transferred_bytes'] = float(csv_list[7])
                ul_stats['bps'] = float(csv_list[8])
                ul_stats['duration'] = float(csv_list[6].split("-")[1])
                print_results(ul_stats, "UPLOAD") 
            
            line_count += 1
        
    # PASS/FAIL LOGIC
    threshold = 900000000 #bps
    if dl_stats["bps"] > threshold and ul_stats["bps"] > threshold:
        results["text"] += "TEST PASSED"
    else:
        results["text"] += "TEST FAILED"

        
    run_test_btn.config(text="Run Test")
    run_test_btn.update_idletasks()


def print_results(stats, label):
    """
    Prints stats dictionary to results panel
    """
    results["text"] += label + ":\n"
    """
    for key, value in stats.items():
        results["text"] += key + ": " + str(value) + "\n"
    """
    results["text"] += "    Throughput: "\
    + str("{:.2f}".format(stats["bps"]/1000000)) + " Mbps\n"
    results["text"] += "    Data Transferred: "\
    + str("{:.2f}".format(stats["transferred_bytes"]/1000000000)) + " GB\n"
    """
    results["text"] += "    Test Duration: "\
    + str(stats["duration"]) + " s\n" 
    """


    results["text"] += "\n"
    results.update_idletasks()


def is_connected():
    """
    scripts_dir/is_connected.sh will check for a link between to eth ports via
    ping. Returns non zero exit code when disconnected
    """
    devnull = open(os.devnull, 'w')
    e_code = subprocess.call([script_dir+"is_connected.sh"], stdout=devnull)
    if e_code != 0:
        connected["text"] = "NOT CONNECTED"
        connected["fg"] = "#ff0000"
        return False 
    else:
        connected["text"] = "CONNECTED"
        connected["fg"] = "#00e600"
        return True


def connection_loop():
    """
    uses root.after to constantly check if device is connected
    """
    is_connected()
    root.after(1500, connection_loop)


def shutdown():
    """shutdown system"""
    subprocess.call(["shutdown", "0"])


root = tk.Tk()
root.title(TITLE)

canvas = tk.Canvas(root,height=HEIGHT, width=WIDTH)
canvas.pack()

# final configuration will be full screen only
#root.attributes("-fullscreen", True)

header = tk.Label(root, text=TITLE, font=('Ubuntu', 30))
header.place(relx=0.5, rely=0, relwidth=0.75, anchor='n')

# TOP_FRAME CONFIGURATION

#bd =5 gives us a lil border for all of our widgets
top_frame = tk.Frame(root, bg="white", bd=5)
# .5 = 1/2 of screen space
# achor=n ensures frame will be centered
top_frame.place(relx=0.5, rely=0.11, relwidth=0.75, relheight=0.1, anchor='n')

connected = tk.Label(top_frame,
    font=('Ubuntu', 25), bg="white", anchor='w', justify="left")
connected.place (relx=0.01, relwidth=0.50, relheight = 1)

# run test button
run_test_btn = tk.Button(top_frame, text="Run Test", font=('Ubuntu', 20), 
    command=bw_test_helper)
run_test_btn.place(relx=0.6, relheight=1, relwidth=0.20)

# stop test button - requires multithread only do if I have to
stop_test_btn = tk.Button(top_frame, text="CANCEL", font=('Ubuntu', 20),
    command=bw_test_stop)
stop_test_btn.place(relx=0.80, relheight=1, relwidth=0.20)
# END OF TOP_FRAME COMPONENTS

# RESULTS PANE CONFIGUTRATION

lower_frame = tk.Frame(root, bg="white", bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6,anchor='n')

result_head = tk.Label(lower_frame, text="Test Results:", font=('Ubuntu', 20), 
    bg="white",anchor='w',justify='left')
result_head.place(relwidth = 1, relheight=.08)

results = tk.Label(lower_frame, font=('Ubuntu', 18), anchor='nw', 
    justify='left', bd=4) 
results.place(rely=.1, relwidth=1, relheight=.9)

# END OF RESULTS PANE CONFIGUTRATION

# BOTTOM LEFT BUTTONS CONFIGURATION
bottom_frame = tk.Frame(root, bd=5)
bottom_frame.place(relx=0.5, rely=0.85, relwidth=1, relheight=0.15, anchor='n')

power_img = PhotoImage(file=image_dir+"power_off.png")
shutdown_button = tk.Button(bottom_frame, text="Power Off", image=power_img, 
    command=shutdown)
shutdown_button.place(relx=0.92)
# END OF BOTTOM LEFT BUTTONS CONFIGURATION

root.after(1500, connection_loop)
root.mainloop()

