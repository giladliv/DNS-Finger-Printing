from alive_progress import alive_bar
class alive_bar_new:
    def __init__(self, total, *args, **kwargs):
        self.gen = self.__activate_bar(total, *args, **kwargs)

    @staticmethod
    def __activate_bar(total, *args, **kwargs):
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