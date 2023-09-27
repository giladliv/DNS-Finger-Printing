from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn, TimeRemainingColumn


class RichProgressBar(Progress):
    def get_task(self, task_id):
        return self._tasks[task_id]

    def task_finished(self, task_id):
        return self._tasks[task_id].finished


def try1():
    import time


    # Create a Progress object
    # progress = Progress()
    progress = RichProgressBar(
        TextColumn("{task.description}..."),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}% "),
        TextColumn("•"),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
    )

    # Start the Progress rendering
    progress.start()







    # Add tasks
    task1 = progress.add_task("[red]Downloading", total=1000)
    task2 = progress.add_task("[green]Processing", total=1000)
    task3 = progress.add_task("[cyan]Cooking", total=1000)
    # progress.remove_task(task2)
    # task2 = progress.add_task("[green]new one..", total=1000)
    print(task1, task2, task3)
    print(progress.task_ids)
    print(progress._tasks[task2].finished)
    #progress.stop()


    # print(type(task1))
    try:
        while not progress.finished:
            if not progress.task_finished(task1):
                progress.update(task1, advance=5)
            if not progress.task_finished(task2):
                progress.update(task2, advance=3)
            if not progress.task_finished(task3):
                progress.update(task3, advance=9)
            time.sleep(0.1)
    finally:
        # Close the Progress rendering
        progress.stop()

try1()

########################################################################################

def try2():
    from rich.progress import Progress
    import time

    progress = Progress()
    progress.start()
    task = progress.add_task("My Task 1...", total=100, start=True)

    # Let's simulate progress from 0 to 100 (you can replace this with your actual task logic)
    while not progress.finished:
        progress.update(task, advance=1)
        time.sleep(0.01)

    # if task.completed == task.total:
    #     print("Task has ended.")
    # else:
    #     print("Task is not yet complete.")

    # # Reset the task's progress to 0
    # progress.update(task, completed=0)
    #
    # Continue with more progress if needed
    progress.reset(task, description='My Task 2...', total=100, start=True)
    for i in range(101):
        progress.update(task, completed=i)
        time.sleep(0.1)


    progress.stop()

# try2()
