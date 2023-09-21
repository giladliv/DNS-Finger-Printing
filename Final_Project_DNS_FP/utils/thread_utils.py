from threading import Thread

class ThreadReturnValue(Thread):
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