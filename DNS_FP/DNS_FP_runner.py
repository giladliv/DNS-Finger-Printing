import logging
import atexit

from scapy.layers.dns import DNSRR

from main_app import pic_of_plot

# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import time
from random import sample
import json
from alive_progress import alive_bar

MAX_WAIT = 5

class DNS_FP_runner:
    def __init__(self, DNS_address, list_names):
        self.FREE_PORTS = range(49152, 65535) #(1024, 65536)
        self.mutex = Lock()
        self.JSON_FILE = 'dns_data.json'
        self.json_dict_total = {}
        self.dns_dict = {}
        self.DNS_address = DNS_address
        self.list_names = list_names
        self.load_from_json(self.JSON_FILE)

        atexit.register(self.save_to_json, self.JSON_FILE)


    # def __del__(self):
    #     self.save_to_json(self.JSON_FILE)

    def load_from_json(self, name_json: str):
        if not os.path.exists(name_json):
            with open(name_json, 'w') as f:
                f.write(json.dumps({}))
        with open(name_json, 'r') as f:
            self.json_dict_total = json.loads(f.read())

    def save_to_json(self, name_json: str):
        with open(name_json, 'w') as f:
            f.write(json.dumps(self.json_dict_total))

    # primary data of dns requests

    def send_DNS_request(self, dns_server: str, name: str, src_port: int, bar, is_recusive: bool = False, sec_timeout: int = MAX_WAIT):
        rd_flag = 1 if (is_recusive == True) else 0
        answer = None
        i = 0
        dns_req = IP()
        while answer is None and i < 4:
            dns_req = IP(dst=dns_server) / UDP(sport=src_port, dport=53) / DNS(rd=rd_flag, qd=DNSQR(qname=name))#, qtype='A'))
            answer = sr1(dns_req, verbose=0, timeout=sec_timeout)
            src_port = random.randint(49152, 65535)
            # with self.mutex:

        self.dns_dict[name] = {'pkt_recv': answer, 'pkt_sent': dns_req}
        self.dns_dict[name]['pkt'] = answer
        self.dns_dict[name]['time'] = sec_timeout if (answer is None) else answer.time - dns_req.sent_time #end - start
        bar()

    def get_data_from_pkts(self, pkt_dict : dict):
        dns_addr = 'No answer received...'
        dns_ttl = 0
        dns_time = MAX_WAIT
        if 'pkt_recv' not in pkt_dict or 'pkt_sent' not in pkt_dict:
                return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl}

        answer = pkt_dict['pkt_recv']
        dns_req = pkt_dict['pkt_sent']
        if answer is not None:
            # self.dns_dict[name].show()

            dns_addr = str(answer[DNS].summary()).replace('DNS Ans ', '').replace('"', '').replace(' ', '')
            dns_addr = dns_addr if len(dns_addr) > 0 else '--'
            dns_time = answer.time - dns_req.sent_time #end - start
            dns_ttl = 0
            RR_ans = answer[DNS].ancount
            if RR_ans > 0:  # if requests came
                for i in range(RR_ans):
                    dns_ttl += answer[DNSRR][i].ttl
                dns_ttl = round(dns_ttl / RR_ans) # get average

            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl}

    def gen_port_names(self, add_names):
        ports = sample(self.FREE_PORTS, len(add_names))
        dict_names_ports = {}
        i = 0
        for name in add_names:
            dict_names_ports[name] = ports[i]
            i += 1
        return dict_names_ports

    def run_names_with_dns(self, is_recusive: bool = False, title: str = ''):
        return self.__run_names_with_dns(self.DNS_address, self.list_names, is_recusive, title)

    def __run_names_with_dns(self, dns_main_ip, names, is_recusive: bool = False, title: str = ''):
        th_list = []
        dict_names_ports = self.gen_port_names(names)
        # curr_time = str(time.time())
        now = datetime.now()  # current date and time
        curr_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        with alive_bar(len(names), title=title, theme='classic') as bar:  ## for something nice
            for name in dict_names_ports:
                port = dict_names_ports[name]
                self.send_DNS_request(dns_main_ip, name, port, bar, is_recusive=is_recusive)
        dict_addr_final = {}
        time.sleep(1)
        for name in self.dns_dict:
            dict_addr_final[name] = self.get_data_from_pkts(self.dns_dict[name])

        # self.load_from_json(self.JSON_FILE)
        if dns_main_ip not in self.json_dict_total:
            self.json_dict_total[dns_main_ip] = {}
        self.json_dict_total[dns_main_ip].update({curr_time: dict_addr_final})
        # self.save_to_json(self.JSON_FILE)
        return dict_addr_final, curr_time

    def get_dict_times_of_dns(self, dns_ip: str, time_str: str):
        try:
            return self.json_dict_total[dns_ip][time_str], time_str
        except:
            return None, None

#python DNS_FP_runner.py

def main(DNS_address, list_names, repeats: int = 8, col_per_page:int = 2, is_first_rec: bool = True):

    #list_names = ['xinshipu.com']

    dns_fp_run = DNS_FP_runner(DNS_address, list_names)

    list_ans_vals = []
    for i in range(repeats):
        is_rec = (i == 0) and is_first_rec
        str_title = f'round %d out ouf %d' % (i + 1, repeats)
        list_ans_vals += [dns_fp_run.run_names_with_dns(is_recusive=is_rec, title=str_title)]

        if i == repeats - 1:
            continue

        sec_time = 10
        with alive_bar(sec_time, title=f'Wait now {sec_time} seconds', theme='classic') as bar:
            for i in range(sec_time):
                time.sleep(1)
                bar()

    # dict_1, time_1 = dns_fp_run.get_dict_times_of_dns(DNS_address, '09/04/2022, 16:49:10')
    # dict_2, time_2 = dns_fp_run.get_dict_times_of_dns(DNS_address, '09/04/2022, 16:50:13')

    app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=col_per_page)
    app.runner()

def get_app_by_time(DNS_address, list_names, col_per_page = 1):

    # list_names = ['xinshipu.com']

    dns_fp_run = DNS_FP_runner(DNS_address, list_names)

    list_ans_vals = []
    list_times = [*dns_fp_run.json_dict_total[DNS_address]][-10:]
    for time_str in list_times:
        list_ans_vals += [dns_fp_run.get_dict_times_of_dns(DNS_address, time_str)]


    app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=col_per_page)
    app.runner()
    # fig.tight_layout()
    #
    # plt.show()

#python DNS_FP_runner.py

if __name__ == "__main__":
    try:
        # 94.153.241.134 - intresting
        # 88.80.64.8 - good dns for check
        DNS_address = '94.153.241.134'  # '88.80.64.8' # <--- GOODONE #'62.219.128.128'
        list_domain_names = ['wikipedia.org', 'china.org.cn', 'fdgdhghfhfghfjfdhdh.com', 'cnbc.com', 'lexico.com',
                      'tr-ex.me', 'tvtropes.org', 'tandfonline.com', 'amazon.in', 'archive.org', 'amitdvir.com',
                      'nihonsport.com', 'aeon-ryukyu.jp', '4stringsjp.com']

        # with open('list_of_domain_names.txt', 'w') as f:
        #     f.write('\n'.join(list_names))

        #main(DNS_address, list_domain_names, repeats=7, col_per_page=2, is_first_rec=True)

        get_app_by_time(DNS_address, list_domain_names, col_per_page=3)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
