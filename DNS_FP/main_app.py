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
    def __init__(self, DNS_address, list_names, list_dict_ans, cols_in_plot=3):
        self.root = tk.Tk()
        self.root.wm_title("Embedding in Tk")
        #self.root.state('zoomed')
        self.list_dict_ans = list_dict_ans
        self.DNS_address = DNS_address

        self.list_names = list_names
        self.subgroups_names = self.get_list_subgroups(list_names, cols_in_plot)
        self.ind_plot = 0

        self.fig, (self.ax_time, self.ax_ttl) = plt.subplots(1, 2, figsize=(9, 6))
        self.WIDTH = 0.7

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

    def __update_plot_of_bars(self, ind: int):
        if self.__change_index_plot(ind):
            self.__update_ax(self.ax_time, 'time', self.subgroups_names[self.ind_plot], to_show_signs=False)
            self.__update_ax(self.ax_ttl, 'time', self.subgroups_names[self.ind_plot], to_show_signs=True)
            self.canvas.draw()
            self.label_pages['text'] = '%d / %d' % (ind + 1, len(self.subgroups_names))
            # self.fig.legend(loc=7)
            #self.fig.tight_layout()

    def __click_prev(self):
        self.__update_plot_of_bars(self.ind_plot - 1)

    def __click_next(self):
        self.__update_plot_of_bars(self.ind_plot + 1)

    def sub_str_find(self, t: str, sep :str = ', '):
        try:
            return t.split(sep)[1]
        except:
            return ''

    def __update_ax(self, ax, category, labels, to_show_signs: bool = False):
        cols = []
        try:
            for dict_col in self.list_dict_ans:
                time = dict_col[1]
                dict_col = dict_col[0]
                cols += [[dict_col[name][category] for name in labels]]
        except:
            return

        x = np.arange(len(labels))*len(self.list_dict_ans)  # the label locations
        ax.clear()

        #mul_arr = np.array([a*4 for a in x])
        bars_list = []
        i = 0
        for (dict_col, time_col) in self.list_dict_ans:
            bars_list += [ax.bar(x + i * self.WIDTH, cols[i], width=self.WIDTH, label=self.sub_str_find(time_col))]
            i += 1

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('time in seconds')
        ax.set_title(f'the receiving adresses from the DNS server {self.DNS_address}')
        ax.set_xticks(x + self.WIDTH * (len(self.list_dict_ans) - 1) / 2, labels, rotation=-15)
        if to_show_signs:
            #ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        for rects in bars_list:
            ax.bar_label(rects, padding=3, size=8, fmt='%.4f')


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