import tkinter as tk

class FrameManager:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Frame Manager")
        self.root.geometry('1024x768')

        self.frame1 = tk.Frame(self.root, width=200, height=100, bg="red")
        self.frame1.grid(row=0, column=0)
        self.grid_size()

        self.frame2 = tk.Frame(self.root, width=200, height=100, bg="green")
        self.frame2.grid(row=0, column=1)
        self.grid_size()

        self.frame3 = tk.Frame(self.root, width=200, height=100, bg="blue")
        self.frame3.grid(row=1, column=0, columnspan=2)
        self.grid_size()

        self.show_frame1_button = tk.Button(self.root, text="Show Frame 1", command=self.show_frame1)
        self.show_frame1_button.grid(row=2, column=0)
        self.grid_size()

        self.hide_frame1_button = tk.Button(self.root, text="Hide Frame 1", command=self.hide_frame1)
        self.hide_frame1_button.grid(row=2, column=1)
        self.grid_size()

        self.show_frame2_button = tk.Button(self.root, text="Show Frame 2", command=self.show_frame2)
        self.show_frame2_button.grid(row=3, column=0)
        self.grid_size()

        self.hide_frame2_button = tk.Button(self.root, text="Hide Frame 2", command=self.hide_frame2)
        self.hide_frame2_button.grid(row=3, column=1)
        self.grid_size()

        self.show_frame3_button = tk.Button(self.root, text="Show Frame 3", command=self.show_frame3)
        self.show_frame3_button.grid(row=4, column=0)
        self.grid_size()

        self.hide_frame3_button = tk.Button(self.root, text="Hide Frame 3", command=self.hide_frame3)
        self.hide_frame3_button.grid(row=4, column=1)
        self.grid_size()

    def show_frame1(self):
        self.frame1.grid()
        self.grid_size()

    def hide_frame1(self):
        self.frame1.grid_forget()
        self.grid_size()

    def show_frame2(self):
        self.frame2.grid()
        self.grid_size()

    def hide_frame2(self):
        self.frame2.grid_forget()
        self.grid_size()

    def show_frame3(self):
        self.frame3.grid()
        self.grid_size()

    def hide_frame3(self):
        self.frame3.grid_forget()
        self.grid_size()

    def grid_size(self):
        print('grid_size', self.root.grid_size())

if __name__ == "__main__":
    root = tk.Tk()
    app = FrameManager(root)
    root.mainloop()
