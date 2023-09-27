import concurrent.futures
import time

from alive_progress import alive_bar

from utils.thread_utils import ThreadReturnValue


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
                yield i < total     # return if still counting


    def __call__(self, *args, **kwargs):
        try:
            still_work = next(self.gen)
            if not still_work:
                self.close()
        except:
            self.close()

    def close(self):
        if self.gen is not None:
            self.gen.close()
            self.gen = None

    def __del__(self):
        self.close()


class backup_alive_bar_new_async(alive_bar_new):
    def __init__(self, total, *args, **kwargs):
        self.thread_bar = None
        self.executor = None
        self.gen = None
        super().__init__(total, *args, **kwargs)

    def activate_bar(self, total, *args, **kwargs):
        self.executor = concurrent.futures.ThreadPoolExecutor()
        return self.executor.submit(super().activate_bar, total, *args, **kwargs).result()

    def close(self):
        super().close()
        if self.executor is not None:
            self.executor.shutdown()
            self.executor = None

class alive_bar_new_async(alive_bar_new):
    def __init__(self, total, *args, **kwargs):
        self.thread_bar = None
        self.gen = None
        super().__init__(total, *args, **kwargs)

    def activate_bar(self, total, *args, **kwargs):
        # creating a thread that runs the active bar and gives the generator as the output
        self.thread_bar = ThreadReturnValue(target=super().activate_bar, args=(total, *args), kwargs=kwargs)
        self.thread_bar.start()
        return self.thread_bar.get_ret_value()

    def close(self):
        super().close()
        if self.thread_bar is not None:
            # self.thread_bar.join()
            self.thread_bar = None

