import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This should be centered")
        label.grid(row=0, column=0)
        label2 = tk.Label(self, text="This should be centered")
        label2.grid(row=1, column=0)
        label2 = tk.Label(self, text="-----------")
        label2.grid(row=0, column=1)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure('all', minsize=10)
        self.configure(height=700, width=700)
        # self.grid_columnconfigure(2, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1024x768')
    Example(root).grid(sticky="nsew")
    # root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)


    root.mainloop()