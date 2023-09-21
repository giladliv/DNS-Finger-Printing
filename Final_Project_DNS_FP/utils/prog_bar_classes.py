from time import sleep

from utils.dubeg_outputs import debug_print, to_show_output_debug
from utils.new_alive_bar import alive_bar_new

to_show_output_debug(False)

class IProgBar:
    def set_bar(self, *args, **kwargs):
        '''
        set the progressbar details
        :param args:
        :param kwargs:
        :return:
        '''
        pass

    def update_bar(self):
        '''
        function that makes one step in the progress counting
        :return:
        '''
        pass

    def close(self):
        '''
        function that closes the progressbar
        :return:
        '''
        pass

    def __enter__(self):
        '''
        make the enter function for entering if the form of: " with *** as ***: "
        :param args:
        :param kwargs:
        :return:
        '''
        # self.set_bar(*args, **kwargs)
        debug_print(f'{str(self.__class__.__name__)} __enter__')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''
        for exiting the mode of the: " with *** as ***: "
        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return:
        '''
        debug_print(f'{str(self.__class__.__name__)} __exit__')
        self.close()

    def __call__(self, *args, **kwargs):
        '''
        make the class use the operator "()"
        this makes the class also a function, it is making the update in the progress
        :return:
        '''
        self.update_bar()

    # def __del__(self):
    #     debug_print('del func')
    #     self.close()

class AliveProgBar(IProgBar):
    def __init__(self, total: int, title: str = ''):
        debug_print(str(self.__class__.__name__))
        self.bar = None
        self.set_bar(total, title)

    def set_bar(self, total: int, title: str = ''):
        self.close()
        self.bar = alive_bar_new(total, title=title, theme='classic', force_tty=True)

    def update_bar(self):
        if self.bar is not None:
            self.bar()

    def close(self):
        if self.bar is not None:
            self.bar.close()  # Manually exit the context manager
        debug_print('bar del')
        self.bar = None

# alive_prog = AliveProgBar()

# with AliveProgBar(10, title='try') as tbar:
#     for i in range(10):
#         tbar()
#         sleep(0.1)




