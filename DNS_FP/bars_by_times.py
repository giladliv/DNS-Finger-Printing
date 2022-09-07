# library
# https://www.python-graph-gallery.com/10-barplot-with-number-of-observation
import random

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def get_rand_time_interval(s=1, e=10):
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


list_dict_res = [{'time': 0.08655953407287598, 'addr': '160.153.129.23', 'ttl': 10800, 'sent_time': 1662560521.7196994,
  'recv_time': 1662560521.806259},
 {'time': 0.07806634902954102, 'addr': '160.153.129.23', 'ttl': 10787, 'sent_time': 1662560535.0306427,
  'recv_time': 1662560535.108709},
 {'time': 0.09952712059020996, 'addr': '160.153.129.23', 'ttl': 10774, 'sent_time': 1662560548.221149,
  'recv_time': 1662560548.320676},
 {'time': 0.09983444213867188, 'addr': '160.153.129.23', 'ttl': 10761, 'sent_time': 1662560560.9185426,
  'recv_time': 1662560561.018377},
 {'time': 0.09782862663269043, 'addr': '160.153.129.23', 'ttl': 10748, 'sent_time': 1662560573.6186473,
  'recv_time': 1662560573.716476},
 {'time': 0.10190629959106445, 'addr': '160.153.129.23', 'ttl': 10736, 'sent_time': 1662560586.3116696,
  'recv_time': 1662560586.413576},
 {'time': 0.09980511665344238, 'addr': '160.153.129.23', 'ttl': 10723, 'sent_time': 1662560599.1130528,
  'recv_time': 1662560599.212858},
 {'time': 0.10185551643371582, 'addr': '160.153.129.23', 'ttl': 10710, 'sent_time': 1662560611.9108336,
  'recv_time': 1662560612.012689}]

def get_times_and_intervals(list_dict_res, str_value: str = ''):
    min_time = float('inf')
    for map_res in list_dict_res:
        min_time = min(min_time, map_res['sent_time'])

    start_end_list, intervals, values = [], [], []
    for map_res in list_dict_res:
        start_end_list += [(map_res['sent_time'] - min_time, map_res['recv_time'] - min_time)]
        intervals += [map_res['time']]
        values += [map_res[str_value]]
    return start_end_list, intervals, values

def set_coordinates_for_visable(widths, totals):

    curr_val = 0
    ret_cords = [0]
    ret_both_vals = []
    i = 1
    for w in widths:
        add_gap = 0 if i + 1 >= len(totals) else totals[i+1] - totals[i]
        add_gap /= 6
        ret_cords += [ret_cords[-1] + w + add_gap]
        ret_both_vals += [curr_val, curr_val + w]
        curr_val = curr_val + w + add_gap
        i += 2
    del ret_cords[-1]
    return ret_cords, ret_both_vals


# Create bars
#start_end_list, width = get_rand_time_interval()

start_end_list, width, values = get_times_and_intervals(list_dict_res, str_value='ttl')
width = np.array(width)*10

bars1 = values
r1 = []
total = []
for (s, e) in start_end_list:
    total += [s, e]

r1, total_new = set_coordinates_for_visable(width, total)
r1 = np.array(r1) + np.array(width) / 2

bars_list = []
# Create barplot
for i in range(len(r1)):
    bars_list += [plt.bar([r1[i]], [bars1[i]], width=width, label='Alone' + str(i))]
# Note: the barplot could be created easily. See the barplot section for other examples.

# Create legend
plt.legend()

# Text below each barplot with a rotation at 90°
plt.xticks(total_new, ["%.3f" % t for t in total], size=8)

for rects in bars_list:
    plt.bar_label(rects, padding=3, size=8, fmt='%d')
# Adjust the margins
# plt.subplots_adjust(bottom=0.2, top=0.98)

# Show graphic
plt.show()

# print(get_rand_time_interval())
