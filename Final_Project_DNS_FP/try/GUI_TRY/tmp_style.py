# import time
# import tkinter as tk
# import tkinter.ttk as ttk
#
# tuple_1 = tuple(range(1, 25))
#
# def progress_bar_func(style, progress_bar, sequence):
#     root.after(500, update_progress_bar, style, progress_bar, 1, len(sequence))
#
# def update_progress_bar(style, progress_bar, num, limit):
#     if num <= limit:
#         percentage = round(num/limit * 100)  # Calculate percentage.
#         progress_bar.config(value=num)
#         style.configure('text.Horizontal.TProgressbar', text='{:g} %'.format(percentage))
#         num += 1
#         root.after(500, update_progress_bar, style, progress_bar, num, limit)
#
# root = tk.Tk()
# root.geometry("300x300")
#
# style = ttk.Style(root)
# style.layout('text.Horizontal.TProgressbar',
#              [('Horizontal.Progressbar.trough',
#                {'children': [('Horizontal.Progressbar.pbar',
#                               {'side': 'left', 'sticky': 'ns'})],
#                 'sticky': 'nswe'}),
#               ('Horizontal.Progressbar.label', {'sticky': ''})])
# style.configure('text.Horizontal.TProgressbar', text='0 %')
#
# progress_bar = ttk.Progressbar(root, style='text.Horizontal.TProgressbar', length=200,
#                                maximum=len(tuple_1), value=0)
# progress_bar.pack()
#
# progress_button = tk.Button(root, text="start",
#                             command=lambda: progress_bar_func(style, progress_bar, tuple_1))
# progress_button.pack()
#
# root.mainloop()

import tkinter as tk
from tkinter import ttk
import time

def increment(*args):
    for i in range(100):
        p1["value"] = i+1
        p2["value"] += 2
        print(p2["value"])
        root.update()
        time.sleep(0.1)
        pb_style.configure('text.Horizontal.TProgressbar',
                    text=f"{p1['value']} %")
        pb_style.configure('rr',
                           text=f"{p2['value']} %")
root = tk.Tk()
root.geometry('300x50')

# define the style
pb_style = ttk.Style(root)
print(pb_style.theme_names())
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
print(pb_style)
#pb_style.theme_use()
pb_style.layout('text.Horizontal.TProgressbar',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])
pb_style.layout('rr',
             [('Horizontal.Progressbar.trough',
               {'children': [('Horizontal.Progressbar.pbar',
                              {'side': 'left', 'sticky': 'ns'})],
                'sticky': 'nswe'}),
              ('Horizontal.Progressbar.label', {'sticky': 'nswe'})])

pb_style.configure('text.Horizontal.TProgressbar', text='0 %', anchor='center', foreground='red', background='yellow')
pb_style.configure('rr', text='0 %', anchor='center')
#pb_style.configure("yellow.Vertical.TProgressbar", troughcolor="gray", background="yellow")

p1 = ttk.Progressbar(root, length=200,
                     orient=tk.HORIZONTAL,
                     style='text.Horizontal.TProgressbar',
                     )
p1.grid(row=1,column=1)

p2 = ttk.Progressbar(root, length=200, maximum=200,
                     orient=tk.HORIZONTAL,
                     style='rr', value=0
                     )
p2.grid(row=3,column=1)


btn = ttk.Button(root,text="Start",command=increment)
btn.grid(row=1,column=0)
root.mainloop()
