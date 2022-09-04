import tkinter as tk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np

class pic_of_plot:
    def __init__(self, fig, ax):
        self.root = tk.Tk()
        self.root.wm_title("Embedding in Tk")
        #self.root.state('zoomed')

        self.canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
        self.ax = ax
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.canvas.mpl_connect("key_press_event", self.on_key_press)
        button = tk.Button(master=self.root, text="Quit", command=self._quit)
        button.pack(side=tk.BOTTOM)
        button2 = tk.Button(master=self.root, text="Change", command=self.change_plot)
        button2.pack(side=tk.BOTTOM)
        self.create_frame_1()
        button2['state'] = 'disabled' # must be active, disabled, or normal
        # button.pack_forget()
        # button.pack()
        # button2.pack()
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

    def create_frame_1(self):
        self.frame_button = tk.Frame(master=self.root)
        # self.chat_name = tk.Label(master=self.frame_2, text='\nChat With: {0} \n'.format(self.curr_name))
        # self.chat_name.pack(side=tk.LEFT)
        self.button_next = tk.Button(master=self.frame_button, text="next", command=self.change_plot)
        self.button_next.pack(side=tk.RIGHT)
        tk.Label(master=self.frame_button, text="  ").pack(side=tk.RIGHT)
        self.button_prev = tk.Button(master=self.frame_button, text="prev", command=self.change_plot)
        self.button_prev.pack(side=tk.RIGHT)
        self.frame_button.pack(side=tk.BOTTOM)

    def on_key_press(self, event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def change_plot(self):
        self.ax.clear()
        x = [1, 2, 3, 4]
        self.ax.set_xticks(x)
        self.ax.set_yticks(x)

        # plot bar chart

        plt.bar(x, [2, 3, 4, 12])

        # Define tick labels

        self.ax.set_xticklabels(["A", "B", "C", "D"])
        self.ax.set_yticklabels([1, 2, 3, 4])
        self.canvas.draw()

    def runner(self):
        self.root.mainloop()



# If you put self.root.destroy() here, it will cause an error if the window is
# closed with the window manager.