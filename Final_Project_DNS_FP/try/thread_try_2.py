from threading import Thread

def foo(bar):
    print('hello {0}'.format(bar))
    return "foo"

def foo_y(n: int = 5, title='foo_y'):
    for i in range(n):
        yield i
        print(f'{title}:\t', i, 'out of', n)

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        self._kwargs = None
        self._args = None
        self._target = None
        self._return = None

        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, **kwargs):
        Thread.join(self)
        return self._return


# twrv = ThreadWithReturnValue(target=foo, args=('world!',))
#
# twrv.start()
# print(twrv.join())   # prints foo

twrv1 = ThreadWithReturnValue(target=foo_y, kwargs={'title': 'th 1'})
twrv2 = ThreadWithReturnValue(target=foo_y, kwargs={'title': 'th 2'})

twrv1.start()
twrv2.start()

gen1 = twrv1.join()
gen2 = twrv2.join()

while gen1 is not None or gen2 is not None:
    try:
        next(gen1)
    except:
        gen1 = None

    try:
        next(gen2)
    except:
        gen2 = None

# print(twrv2.join())

