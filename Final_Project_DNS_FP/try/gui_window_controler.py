import tkinter as tk

class TopLevelController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Top-Level Controller")

        self.windows = []

        self.button_new = tk.Button(self.root, text="Create New Window", command=self.create_new_window)
        self.button_new.pack()

        self.button_hide = tk.Button(self.root, text="Hide Windows", command=self.hide_windows)
        self.button_hide.pack()

        self.button_show = tk.Button(self.root, text="Show Windows", command=self.show_windows)
        self.button_show.pack()

    def create_new_window(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("New Window")
        label = tk.Label(new_window, text="This is a new window.")
        label.pack()
        self.windows.append(new_window)

    def hide_windows(self):
        for window in self.windows:
            window.withdraw()

    def show_windows(self):
        for window in self.windows:
            window.deiconify()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TopLevelController()
    app.run()
