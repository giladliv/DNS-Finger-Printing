
# with alive_bar(10, title='try over', theme='classic', force_tty=True) as bar:
#     for i in range(12):
#         bar()


# def done(i):
#     return i % 2 == 0


# with alive_bar(1200, title='try second', theme='classic', force_tty=True) as bar:
#     for i in range(1200):
#
#         # time.sleep(0.00001)
#         # if done(i):
#         #     bar(skipped=True)
#         #     continue
#
#         # process item
#         data = bar()
#         if i % 100 == 0:
#             print(data)

# bar1 = alive_bar_new(10, title='hello1', force_tty=True, dual_line=False)
# print('a')
# # for i in range(10):
# #     bar1()
# # print()
# bar2 = alive_bar_new(10, title='hello2', force_tty=True, dual_line=False)
# print('b')
# # print()
# #
# for i in range(20):
#     if i % 2 == 0:
#         bar1()
#         print('a')
#     else:
#         bar2()
#         print('b')
#     time.sleep(0.5)
# #
# bar1.close()
# bar2.close()
#


# import time
#
# from rich.progress import Progress
#
# with Progress() as progress:
#
#     task1 = progress.add_task("[red]Downloading...", total=1000)
#     task2 = progress.add_task("[green]Processing...", total=1000)
#     task3 = progress.add_task("[cyan]Cooking...", total=1000)
#
#     while not progress.finished:
#         progress.update(task1, advance=5)
#         progress.update(task2, advance=3)
#         progress.update(task3, advance=9)
#         time.sleep(0.2)