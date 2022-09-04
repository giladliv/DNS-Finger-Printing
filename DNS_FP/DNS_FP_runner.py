import logging

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import time
from random import sample
import json
from tqdm import tqdm
from alive_progress import alive_bar

FREE_PORTS = range(1024,65536)
mutex = Lock()
JSON_FILE = 'dns_data.json'
json_dict_total = {}

def load_from_json(name_json: str):
    global json_dict_total
    if not os.path.exists(name_json):
        with open(name_json, 'w') as f:
            f.write(json.dumps({}))
    with open(name_json, 'r') as f:
        json_dict_total = json.loads(f.read())

def save_to_json(name_json: str):
    with open(name_json, 'w') as f:
        f.write(json.dumps(json_dict_total))

# primary data of dns requests
dns_dict = {}
def send_DNS_request(dns_server: str, name: str, src_port: int, bar, minutes_timeout: float = 1):
    dns_req = IP(dst=dns_server) / UDP(sport=src_port, dport=53) / DNS(rd=1, qd=DNSQR(qname=name, qtype="A"))
    start = time.time()
    minutes_timeout = int(minutes_timeout*60)
    answer = sr1(dns_req, verbose=0, timeout=minutes_timeout)
    end = time.time()
    with mutex:
        dns_dict[name] = {}
        dns_dict[name]['pkt'] = answer
        dns_dict[name]['time'] = end - start
        bar()
        #time.sleep(0.1)


def gen_port_names(add_names):
    ports = sample(FREE_PORTS, len(add_names))
    dict_names_ports = {}
    i = 0
    for name in add_names:
        dict_names_ports[name] = ports[i]
        i += 1
    return dict_names_ports


def run_names_with_dns(dns_main_ip, names):
    th_list = []
    dict_names_ports = gen_port_names(names)
    #curr_time = str(time.time())
    now = datetime.now()  # current date and time
    curr_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    with alive_bar(len(names), theme='classic') as bar: ## for something nice
        for name in dict_names_ports:
            port = dict_names_ports[name]
            th = threading.Thread(target=send_DNS_request, args=(dns_main_ip, name, port, bar))
            th_list += [th]
            th.start()

    #with tqdm(total=len(th_list), desc="Adding Users", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:

        for th in th_list:
            th.join()
        #bar()
            #pbar.update(1)

    dict_addr_final = {}
    time.sleep(1)
    for name in dns_dict:
        # print(f'{name}:')
        # print('*'*20)
        # print('it took:\t', dns_dict[name]['time'])
        dns_addr = 'No answer received...'
        if dns_dict[name]['pkt'] is not None:
            # dns_dict[name].show()

            dns_addr = str(dns_dict[name]['pkt'][DNS].summary()).replace('DNS Ans ', '').replace('"', '')
            dns_addr = dns_addr if len(dns_addr) > 0 else '--'
            #print(dns_addr)
        # else:
        #     print(None)
        # print()

        dict_addr_final[name] = {'time': dns_dict[name]['time'], 'addr': dns_addr}

    load_from_json(JSON_FILE)
    if dns_main_ip not in json_dict_total:
        json_dict_total[dns_main_ip] = {}
    json_dict_total[dns_main_ip].update({curr_time: dict_addr_final})
    save_to_json(JSON_FILE)
    return dict_addr_final, curr_time

list_names = ['wikipedia.org', 'china.org.cn', 'fdgdhghfhfghfjfdhdh.com', 'cnbc.com', 'lexico.com',
              'tr-ex.me', 'tvtropes.org', 'tandfonline.com', 'amazon.in', 'archive.org']



def get_dict_times_of_dns(dns_ip: str, time_str: str):
    global json_dict_total
    try:
        return json_dict_total[dns_ip][time_str], time_str
    except:
        return None, None


DNS_address = "2.119.99.133"

# dict_1, time_1 = run_names_with_dns(DNS_address, list_names)
#
# min_time = 0.5
# t = int(min_time*60)
# with alive_bar(t, title=f'Wait now {min_time} minuetes', theme='classic') as bar:
#     for i in range(t):
#         time.sleep(1)
#         bar()
#
#
# dict_2, time_2 = run_names_with_dns(DNS_address, list_names)

# the reading from the py
load_from_json(JSON_FILE)
dict_1, time_1 = get_dict_times_of_dns(DNS_address, '08/30/2022, 04:27:46')
dict_2, time_2 = get_dict_times_of_dns(DNS_address, '08/30/2022, 04:33:51')

import matplotlib.pyplot as plt
import numpy as np


labels = list_names.copy()
right_col = [dict_1[name]['time'] for name in labels]

left_col = [dict_2[name]['time'] for name in labels]

x = np.arange(len(labels))  # the label locations
width = 0.42  # the width of the bars

fig, ax = plt.subplots(figsize=(15,6)) #20,10
rects1 = ax.bar(x - width/2, right_col, width, label=time_1)
rects2 = ax.bar(x + width/2, left_col, width, label=time_2)

# # text in grouped bar chart
#
# for bar in ax.patches:
#     value = bar.get_height()
#     text = f'{round(value, 5)}'
#     text_x = bar.get_x() + bar.get_width() / 2
#     text_y = bar.get_y() + value
#     ax.text(text_x, text_y, text, ha='center',color='r',size=12)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('time in seconds')
ax.set_title(f'the receiving adresses from the DNS server {DNS_address}')
ax.set_xticks(x, labels, rotation=-15)
ax.legend()

print(rects1)
ax.bar_label(rects1, padding=3, size=8, fmt='%.5f')
ax.bar_label(rects2, padding=3, size=8, fmt='%.5f')
fig.tight_layout()
# app = pic_of_plot(fig, ax)
# app.runner()
# fig.tight_layout()
#
plt.show()





