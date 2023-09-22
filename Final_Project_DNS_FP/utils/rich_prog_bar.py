from rich.progress import BarColumn, MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn, TimeRemainingColumn


class RichProgressBar(Progress):
    def get_task(self, task_id):
        return self._tasks[task_id]

    def task_finished(self, task_id):
        return self._tasks[task_id].finished


def make_prog_from_template():
    return RichProgressBar(
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