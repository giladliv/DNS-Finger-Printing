from alive_progress import alive_bar

# bar = alive_bar(10, title='try', theme='classic')
# # move one forward
# bar.close()
# Using progressbar to Create a Simple Progress Bar
import progressbar
import time

# print('me')
# bar1 = progressbar.ProgressBar(max_value=50)
# print('me2')
# bar2 = progressbar.ProgressBar(max_value=50)
# for i in range(50):
#     time.sleep(0.1)
#     bar1.update(i)
#
#
# for i in range(50):
#     time.sleep(0.1)
#     bar2.update(i)

# print('me')
# bar1 = progressbar.ProgressBar(max_value=50)
# print('me')
# bar2 = progressbar.ProgressBar(max_value=50)
# print('me')
# for i in range(50):
#     time.sleep(0.1)
#     bar1.update(i)
#     bar2.update(i)

from alive_progress import alive_it

# items = list(range(10))
# bar = alive_it(items, force_tty=True)
# for i in bar:
#     time.sleep(0.1)

    # print(i)
    # break

# for i in bar:
#     print(i)
#     break

def activate_bar(n: int = 10):
    with alive_bar(n, title='hello', theme='classic', force_tty=True) as bar:
        for i in range(n):
            bar()
            yield i

# num = 10
# obj = activate_bar(num)
#
#
# for i in range(num):
#     next(obj)
#     time.sleep(0.1)
# obj.close()