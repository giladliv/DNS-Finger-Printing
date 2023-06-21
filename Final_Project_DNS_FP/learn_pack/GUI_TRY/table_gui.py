# # # #!/usr/bin/python3
# # # import tkinter as tk
# # # import tkinter.ttk as ttk
# # #
# # #
# # # class NewprojectApp:
# # #     def __init__(self, master=None):
# # #         # build ui
# # #         toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
# # #         toplevel1.configure(height=200, width=200)
# # #         toplevel1.geometry("800x600")
# # #         frame1 = ttk.Frame(toplevel1)
# # #         frame1.configure(height=400, width=400)
# # #         treeview1 = ttk.Treeview(frame1)
# # #         treeview1.configure(height=19, selectmode="extended", takefocus=False)
# # #         treeview1.grid(column=0, row=0, sticky="nsew")
# # #         scrollbar1 = ttk.Scrollbar(frame1)
# # #         scrollbar1.configure(orient="vertical")
# # #         scrollbar1.grid(column=1, row=0, sticky="nse")
# # #         scrollbar2 = ttk.Scrollbar(frame1)
# # #         scrollbar2.configure(orient="horizontal")
# # #         scrollbar2.grid(column=0, row=1, sticky="sew")
# # #         frame1.pack(expand=True, fill="both", side="top")
# # #
# # #         # Main widget
# # #         self.mainwindow = toplevel1
# # #
# # #     def run(self):
# # #         self.mainwindow.mainloop()
# # #
# # #
# # # if __name__ == "__main__":
# # #     app = NewprojectApp()
# # #     app.run()
# # import tkinter as tk
# #
# # import tksheet
# #
# # top = tk.Tk()
# #
# # sheet = tksheet.Sheet(top)
# #
# # sheet.grid()
# #
# # sheet.set_sheet_data([[f"{ri+cj}" for cj in range(4)] for ri in range(1)])
# #
# # # table enable choices listed below:
# #
# # sheet.enable_bindings(("single_select",
# #
# #                        "row_select",
# #
# #                        "column_width_resize",
# #
# #                        "arrowkeys",
# #
# #                        "right_click_popup_menu",
# #
# #                        "rc_select",
# #
# #                        "rc_insert_row",
# #
# #                        "rc_delete_row",
# #
# #                        "copy",
# #
# #                        "cut",
# #
# #                        "paste",
# #
# #                        "delete",
# #
# #                        "undo",
# #
# #                        "edit_cell"))
# #
# # top.mainloop()
#
# # -*- coding: utf-8 -*-
#
# # Copyright (c) Juliette Monsel 2018
# # For license see LICENSE
#
# from ttkwidgets import Table
# import tkinter as tk
# from tkinter import ttk
#
# root = tk.Tk()
#
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
#
# style = ttk.Style(root)
# style.theme_use('alt')
# sortable = tk.BooleanVar(root, False)
# drag_row = tk.BooleanVar(root, False)
# drag_col = tk.BooleanVar(root, False)
#
# columns = ["A", "B", "C", "D", "E", "F", "G"]
# table = Table(root, columns=columns, sortable=sortable.get(), drag_cols=drag_col.get(),
#               drag_rows=drag_row.get(), height=6)
# for col in columns:
#     table.heading(col, text=col)
#     table.column(col, width=100, stretch=False)
#
# # sort column A content as int instead of strings
# table.column('A', type=int)
#
# for i in range(12):
#     table.insert('', 'end', iid=i,
#                  values=(i, i) + tuple(i + 10 * j for j in range(2, 7)))
#
# # add scrollbars
# sx = tk.Scrollbar(root, orient='horizontal', command=table.xview)
# sy = tk.Scrollbar(root, orient='vertical', command=table.yview)
# table.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
#
# table.grid(sticky='ewns')
# sx.grid(row=1, column=0, sticky='ew')
# sy.grid(row=0, column=1, sticky='ns')
# root.update_idletasks()
#
#
# # toggle table properties
# def toggle_sort():
#     table.config(sortable=sortable.get())
#
#
# def toggle_drag_col():
#     table.config(drag_cols=drag_col.get())
#
#
# def toggle_drag_row():
#     table.config(drag_rows=drag_row.get())
#
#
# frame = tk.Frame(root)
# tk.Checkbutton(frame, text='sortable', variable=sortable, command=toggle_sort).pack(side='left')
# tk.Checkbutton(frame, text='drag columns', variable=drag_col, command=toggle_drag_col).pack(side='left')
# tk.Checkbutton(frame, text='drag rows', variable=drag_row, command=toggle_drag_row).pack(side='left')
# frame.grid()
# root.geometry('400x200')
#
# root.mainloop()

#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class NewprojectApp:
    def __init__(self, master=None):
        # build ui
        toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1.configure(height=600, width=600)
        toplevel1.geometry("800x600")
        frame1 = ttk.Frame(toplevel1)
        frame1.configure(height=500, width=500)
        treeview1 = ttk.Treeview(frame1)
        treeview1.configure(selectmode="extended", width=500)
        treeview1.grid(sticky="nsew")
        frame1.pack(expand=True, side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = NewprojectApp()
    app.run()

