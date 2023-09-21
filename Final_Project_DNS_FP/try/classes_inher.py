NUM = 5

class A:
    def __init__(self, n: int = NUM):
        self.foo(n)

    def foo(self, n):
        print(self.__class__.__name__, '-->', n, ' '*3, 'A parent')

class B(A):
    def __init__(self, n: int = NUM):
        super().__init__(n)

    def foo(self, n: int = NUM):
        # super().foo(n)
        print(self.__class__.__name__, '-->', n, ' '*3, 'YEAH!!!')


A()
B()