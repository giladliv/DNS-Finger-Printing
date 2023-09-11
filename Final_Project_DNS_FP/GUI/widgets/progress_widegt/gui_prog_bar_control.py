from utils.prog_bar_classes import IProgBar

class ProgBarGUIControl(IProgBar):
    def __init__(self, ProgressWidget, max_size: int = 100, jump: int = 1, title: str = 'title'):
        pass

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