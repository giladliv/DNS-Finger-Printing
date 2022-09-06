import tkinter as tk
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
#from DNS_FP_runner import DNS_FP_runner

import numpy as np

class pic_of_plot:
    def __init__(self, DNS_address, list_names, dict_1, time_1, dict_2, time_2):
        self.root = tk.Tk()
        self.root.wm_title("Embedding in Tk")
        #self.root.state('zoomed')
        self.dict_1 = dict_1
        self.time_1 = time_1
        self.dict_2 = dict_2
        self.time_2 = time_2
        self.DNS_address = DNS_address

        self.list_names = list_names
        self.subgroups_names = self.get_list_subgroups(list_names, 4)
        self.ind_plot = 0

        self.fig, self.ax = plt.subplots(figsize=(9, 6))


        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.create_frame_1()

        self.__update_plot_of_bars(0)
        # self.canvas.mpl_connect("key_press_event", self.on_key_press)
        # button = tk.Button(master=self.root, text="Quit", command=self._quit)
        # button.pack(side=tk.BOTTOM)
        # button2 = tk.Button(master=self.root, text="Change", command=self.change_plot)
        # button2.pack(side=tk.BOTTOM)

        # button2['state'] = 'disabled' # must be active, disabled, or normal
        # button.pack_forget()
        # button.pack()
        # button2.pack()
        self.root.protocol("WM_DELETE_WINDOW", self._quit)

    def create_frame_1(self):

        self.frame_button = tk.Frame(master=self.root)
        self.label_pages = tk.Label(master=self.frame_button, text="--")
        self.label_pages.pack(side=tk.BOTTOM)
        # self.chat_name = tk.Label(master=self.frame_2, text='\nChat With: {0} \n'.format(self.curr_name))
        # self.chat_name.pack(side=tk.LEFT)
        self.button_next = tk.Button(master=self.frame_button, text="next", command=self.__click_next)
        self.button_next.pack(side=tk.RIGHT)
        tk.Label(master=self.frame_button, text="  ").pack(side=tk.RIGHT)
        self.button_prev = tk.Button(master=self.frame_button, text="prev", command=self.__click_prev)
        self.button_prev.pack(side=tk.RIGHT)

        self.frame_button.pack(side=tk.BOTTOM)

    def on_key_press(self, event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, self.canvas, self.toolbar)

    def _quit(self):
        self.root.quit()     # stops mainloop
        self.root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    def __change_index_plot(self, ind: int):
        if len(self.subgroups_names) == 0:
            self.button_prev['state'] = 'disabled'
            self.button_next['state'] = 'disabled'
            return False
        if ind < 0 or ind >= len(self.subgroups_names):
            return False

        # activate both
        self.button_prev['state'] = 'normal'
        self.button_next['state'] = 'normal'
        # if 0 cannot be less
        if ind == 0:
            self.button_prev['state'] = 'disabled' # must be active, disabled, or normal
        # if at the last stop the next button
        if ind == len(self.subgroups_names) - 1:
            self.button_next['state'] = 'disabled'
        self.ind_plot = ind
        return True

    def __update_plot_of_bars(self, ind: int, width=0.42):
        if self.__change_index_plot(ind):
            self.__update_ax(self.subgroups_names[self.ind_plot], width)

    def __click_prev(self):
        self.__update_plot_of_bars(self.ind_plot - 1)

    def __click_next(self):
        self.__update_plot_of_bars(self.ind_plot + 1)

    def __update_ax(self, labels, width=0.42):
        right_col = [self.dict_1[name]['time'] for name in labels]
        left_col = [self.dict_2[name]['time'] for name in labels]
        x = np.arange(len(labels))  # the label locations
        self.ax.clear()
        rects1 = self.ax.bar(x - width / 2, right_col, width, label=self.time_1)
        rects2 = self.ax.bar(x + width / 2, left_col, width, label=self.time_2)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        self.ax.set_ylabel('time in seconds')
        self.ax.set_title(f'the receiving adresses from the DNS server {self.DNS_address}')
        self.ax.set_xticks(x, labels, rotation=-15)
        self.ax.legend()

        self.ax.bar_label(rects1, padding=3, size=8, fmt='%.5f')
        self.ax.bar_label(rects2, padding=3, size=8, fmt='%.5f')
        self.canvas.draw()

    @staticmethod
    def get_list_subgroups(list_to_part, num_lin_list: int = 10):
        if num_lin_list <= 0:
            num_lin_list = 10
        len_l = len(list_to_part)
        times_run = int(len_l / num_lin_list)
        if len_l % num_lin_list != 0:
            times_run += 1
        list_subs = []
        for i in range(times_run):
            start = i * num_lin_list
            end = min(start + num_lin_list, len_l)
            list_subs += [list_to_part[start:end]]
        return list_subs

    def runner(self):
        self.root.mainloop()



# If you put self.root.destroy() here, it will cause an error if the window is
# closed with the window manager.