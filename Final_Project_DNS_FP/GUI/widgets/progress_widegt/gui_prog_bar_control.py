from GUI.widgets.progress_widegt.prog_widget import ProgressWidget
from utils.prog_bar_classes import IProgBar

class ProgBarGUIControl(IProgBar):
    def __init__(self, prog_widget: ProgressWidget, total: int = 100, jump: int = 1, title: str = 'title'):
        self.prog_widget: ProgressWidget = prog_widget
        self.set_bar(total=total, jump=jump, title=title)
        

    def set_bar(self, total: int, jump: int = 1, title: str = 'title'):
        '''
        set the progressbar details
        :param args:
        :param kwargs:
        :return:
        '''
        self.prog_widget.set_progress(total=total, jump=jump, title=title)

    def update_bar(self):
        '''
        function that makes one step in the progress counting
        :return:
        '''
        if self.prog_widget is not None:
            self.prog_widget()

    def close(self):
        '''
        function that closes the progressbar
        :return:
        '''
        if self.prog_widget is not None:
            self.prog_widget = None

def ctor_control_prog_by_widget(prog_widget: ProgressWidget):
    def ctor_inner_prog_widget(*args, **kwargs):
        return ProgBarGUIControl(prog_widget, *args, **kwargs)

    return ctor_inner_prog_widget