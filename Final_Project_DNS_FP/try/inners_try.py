def outer(n: int):
    def func(a: int, b: int):
        return a + b < n
    return func

print(outer(100))

print(outer(100)(2,3))