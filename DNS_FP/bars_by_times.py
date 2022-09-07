# library
# https://www.python-graph-gallery.com/10-barplot-with-number-of-observation
import random

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_rand_time_interval(s = 1, e = 10):
    start_time = 0.1
    end_points_intervals = []
    only_intervals = []
    gap = e - s + 1
    for i in range(s, e + 1):
        interval = round(random.randint(s, e) / gap, 1)
        only_intervals += [interval]
        end_time = round(start_time + interval, 1)
        end_points_intervals += [(start_time, end_time)]
        start_time = round(end_time + random.randint(s, e) / gap, 1)
    return end_points_intervals, only_intervals

# Create bars
barWidth = 0.9
start_end_list, width = get_rand_time_interval()
print(start_end_list , width)
bars1 = width
r1 = []
total = []
for (s, e) in start_end_list:
    r1 += [s]
    total += [s, e]

r1 = np.array(r1) + np.array(width) / 2


# Create barplot
plt.bar(r1, bars1, width=width, color=(0.3, 0.1, 0.4, 0.6), label='Alone')
# Note: the barplot could be created easily. See the barplot section for other examples.

# Create legend
plt.legend()



# Text below each barplot with a rotation at 90°
plt.xticks(total, [str(t) for t in total])

# Adjust the margins
# plt.subplots_adjust(bottom=0.2, top=0.98)

# Show graphic
plt.show()



# print(get_rand_time_interval())
