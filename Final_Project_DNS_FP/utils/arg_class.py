class ArgClass:
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__setattr__(key, kwargs[key])

    def __repr__(self):
        '''
        representing string
        :return:
        '''
        # s = str(type(self))
        s = self.__class__.__name__ + '  '
        s += ', '.join([f'{k}: {self.__dict__[k]}' for k in self.__dict__])
        s = f'<<{s}>>'
        return s


arg_cls = ArgClass(a=7, b=9)
print(str(arg_cls))
