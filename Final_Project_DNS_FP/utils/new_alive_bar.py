import concurrent.futures
import time

from alive_progress import alive_bar
class alive_bar_new:
    def __init__(self, total: int, *args, **kwargs):
        self.gen = None
        if total is not None:
            self.gen = self.activate_bar(total, *args, **kwargs)

    def activate_bar(self, total: int, *args, **kwargs):
        '''
        make a loop and wield for the alive bar
        :param total:
        :param args:
        :param kwargs:
        :return:
        '''
        i = 0
        with alive_bar(total, *args, **kwargs) as bar:
            while i < total:
                bar()
                i += 1
                yield 0
        self.close()

    def __call__(self, *args, **kwargs):
        try:
            next(self.gen)
        except:
            self.close()

    def close(self):
        if self.gen is not None:
            self.gen.close()
            self.gen = None

    def __del__(self):
        self.close()


class alive_bar_new_async(alive_bar_new):
    def __init__(self, total, *args, **kwargs):

        self.executor = None
        self.gen = None
        super().__init__(total, *args, **kwargs)

    def activate_bar(self, total, *args, **kwargs):
        self.executor = concurrent.futures.ThreadPoolExecutor()
        return self.executor.submit(self.activate_bar, total, *args, **kwargs).result()

    def close(self):
        super().close()
        if self.executor is not None:
            self.executor.shutdown()
            self.executor = None


with alive_bar(10, title='try over', theme='classic', force_tty=True) as bar:
    for i in range(12):
        bar()


def done(i):
    return i % 2 == 0


with alive_bar(1200, title='try second', theme='classic', force_tty=True) as bar:
    for i in range(1200):

        # time.sleep(0.00001)
        # if done(i):
        #     bar(skipped=True)
        #     continue

        # process item
        data = bar()
        if i % 100 == 0:
            print(data)

bar1 = alive_bar_new_async(10, title='hello1', force_tty=True)
for i in range(10):
    bar1()
print()
# bar2 = alive_bar_new(10, title='hello2', force_tty=True)
# print()
#
# for i in range(20):
#     if i % 2 == 0:
#         bar1()
#     else:
#         bar2()
#     time.sleep(0.5)
#
# bar1.close()
# bar2.close()



# import time
#
# from rich.progress import Progress
#
# with Progress() as progress:
#
#     task1 = progress.add_task("[red]Downloading...", total=1000)
#     task2 = progress.add_task("[green]Processing...", total=1000)
#     task3 = progress.add_task("[cyan]Cooking...", total=1000)
#
#     while not progress.finished:
#         progress.update(task1, advance=5)
#         progress.update(task2, advance=3)
#         progress.update(task3, advance=9)
#         time.sleep(0.2)

