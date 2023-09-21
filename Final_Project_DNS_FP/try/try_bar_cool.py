import time
from rich.progress import Progress

# Create a Progress object
progress = Progress()

# Start the Progress rendering
progress.start()

# Add tasks
task1 = progress.add_task("[red]Downloading...", total=1000)
task2 = progress.add_task("[green]Processing...", total=1000)
task3 = progress.add_task("[cyan]Cooking...", total=1000)

print(type(task1))
try:
    while not progress.finished:
        progress.update(task1, advance=5)
        print('hello')
        progress.update(task2, advance=3)
        progress.update(task3, advance=9)
        time.sleep(0.2)
finally:
    # Close the Progress rendering
    progress.stop()
