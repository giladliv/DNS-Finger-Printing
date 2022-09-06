import logging
import atexit
from main_app import pic_of_plot

# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import time
from random import sample
import json
from alive_progress import alive_bar


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

    def send_DNS_request(self, dns_server: str, name: str, src_port: int, bar, is_recusive: bool = False, sec_timeout: int = 5):
        rd_flag = 1 if (is_recusive == True) else 0
        answer = None
        i = 0
        dns_req = IP()
        while answer is None and i < 4:
            dns_req = IP(dst=dns_server) / UDP(sport=src_port, dport=53) / DNS(rd=rd_flag, qd=DNSQR(qname=name))#, qtype='A'))
            answer = sr1(dns_req, verbose=0, timeout=sec_timeout)
            src_port = random.randint(49152, 65535)
            # with self.mutex:

        self.dns_dict[name] = {}
        self.dns_dict[name]['pkt'] = answer
        self.dns_dict[name]['time'] = sec_timeout if (answer is None) else answer.time - dns_req.sent_time #end - start
        bar()

    def gen_port_names(self, add_names):
        ports = sample(self.FREE_PORTS, len(add_names))
        dict_names_ports = {}
        i = 0
        for name in add_names:
            dict_names_ports[name] = ports[i]
            i += 1
        return dict_names_ports

    def run_names_with_dns(self, is_recusive: bool = False):
        return self.__run_names_with_dns(self.DNS_address, self.list_names, is_recusive)

    def __run_names_with_dns(self, dns_main_ip, names, is_recusive: bool = False):
        th_list = []
        dict_names_ports = self.gen_port_names(names)
        # curr_time = str(time.time())
        now = datetime.now()  # current date and time
        curr_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        with alive_bar(len(names), theme='classic') as bar:  ## for something nice
            for name in dict_names_ports:
                port = dict_names_ports[name]
                self.send_DNS_request(dns_main_ip, name, port, bar, is_recusive=is_recusive)
            #     th = threading.Thread(target=self.send_DNS_request, args=(dns_main_ip, name, port, bar))
            #     th_list += [th]
            #     th.start()
            #
            # for th in th_list:
            #     th.join()

        dict_addr_final = {}
        time.sleep(1)
        for name in self.dns_dict:
            # print(f'{name}:')
            # print('*'*20)
            # print('it took:\t', self.dns_dict[name]['time'])
            dns_addr = 'No answer received...'
            dns_ttl = 'no TTL'
            if self.dns_dict[name]['pkt'] is not None:
                # self.dns_dict[name].show()

                dns_addr = str(self.dns_dict[name]['pkt'][DNS].summary()).replace('DNS Ans ', '').replace('"', '').replace(' ', '')
                dns_addr = dns_addr if len(dns_addr) > 0 else '--'
                dns_ttl = self.dns_dict[name]['pkt'][IP].ttl
                # print(dns_addr)
            # else:
            #     print(None)
            # print()
            dict_addr_final[name] = {'time': self.dns_dict[name]['time'], 'addr': dns_addr, 'ttl': dns_ttl}

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

def main(DNS_address, list_names, repeats: int = 8, is_first_rec: bool = True):

    #list_names = ['xinshipu.com']

    dns_fp_run = DNS_FP_runner(DNS_address, list_names)

    list_ans_vals = []
    for i in range(repeats):
        is_rec = (i == 0) and is_first_rec
        list_ans_vals += [dns_fp_run.run_names_with_dns(is_recusive=is_rec)]

        if i == repeats - 1:
            continue

        sec_time = 10
        with alive_bar(sec_time, title=f'Wait now {sec_time} seconds', theme='classic') as bar:
            for i in range(sec_time):
                time.sleep(1)
                bar()

    # dict_1, time_1 = dns_fp_run.get_dict_times_of_dns(DNS_address, '09/04/2022, 16:49:10')
    # dict_2, time_2 = dns_fp_run.get_dict_times_of_dns(DNS_address, '09/04/2022, 16:50:13')

    app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=3)
    app.runner()
    # fig.tight_layout()
    #
    # plt.show()

#python DNS_FP_runner.py

if __name__ == "__main__":
    try:
        DNS_address = '88.80.64.8'  # '88.80.64.8' # <--- GOODONE #'62.219.128.128'
        list_names = ['wikipedia.org', 'china.org.cn', 'fdgdhghfhfghfjfdhdh.com', 'cnbc.com', 'lexico.com',
                      'tr-ex.me', 'tvtropes.org', 'tandfonline.com', 'amazon.in', 'archive.org', 'www.amitdvir.com',
                      'nihonsport.com', 'aeon-ryukyu.jp', '4stringsjp.com']
        main(DNS_address, list_names, repeats=3, is_first_rec=True)
        # main(False, False)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
