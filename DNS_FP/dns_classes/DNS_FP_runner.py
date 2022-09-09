# https://blog.apnic.net/2021/06/22/cache-me-outside-dns-cache-probing/
# https://publicdnsserver.com/

from dns_classes.cache_graph_gui import pic_of_plot

# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from random import sample
from alive_progress import alive_bar
from dns_classes.dns_data_db import *

INTERVAL_WAIT_SEC = 10

class DNS_FP_runner:
    def __init__(self, DNS_address, list_names, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        if not self.is_ipv4(DNS_address):
            raise ValueError(f'the given string: {DNS_address} is not an ipv4 format')
        self.DNS_address = DNS_address
        self.JSON_FILE = json_file_name if json_file_name.endswith('.json') else JSON_FILE_NAME_DEFAULT
        self.json_dict_total = {}
        self.dns_dict = {}

        self.list_names = list_names
        self.reset_rd_illegal_count()
        self.dns_db = dns_data_db(self.JSON_FILE)
        self.FREE_PORTS = range(1024, 65535)

    def save_db(self):
        self.dns_db.save_and_update_db()

    @staticmethod
    def is_ipv4(ip_addr: str):
        list_nums = ip_addr.split(".")
        if len(list_nums) != 4:
            return False
        try:
            for i in list_nums:
                if int(i) < 0 or int(i) > 255:
                    return False
        except:
            return False
        return True

    def reset_rd_illegal_count(self):
        self.rd_counter = 0
        self.pkt_counter = 0

    def is_recursive_DNS(self):
        if self.pkt_counter == 0:
            return False
        return (self.rd_counter / self.pkt_counter) > 0.5

    # primary data of dns requests

    def send_DNS_request(self, dns_server: str, name_domain: str, src_port: int, bar, is_recusive: bool = False, sec_timeout: int = MAX_WAIT):
        rd_flag = 1 if is_recusive else 0
        answer = None
        i = 0
        dns_req = IP()

        while answer is None and i < 4:
            dns_req = IP(dst=dns_server) / UDP(sport=src_port, dport=53) / DNS(rd=rd_flag, qd=DNSQR(qname=name_domain))
            answer = sr1(dns_req, verbose=0, timeout=sec_timeout)
            src_port = random.randint(1024, 65535)
            i += 1

        bar()

        # count rd that has been chanched by the dns server
        if (answer is not None) and (not is_recusive):
            self.rd_counter += answer[DNS].rd
            self.pkt_counter += 1

        self.dns_dict[name_domain] = {'pkt_recv': answer, 'pkt_sent': dns_req}

    def gen_port_names(self, add_names):
        ports = sample(self.FREE_PORTS, len(add_names))
        dict_names_ports = {}
        i = 0
        for name in add_names:
            dict_names_ports[name] = ports[i]
            i += 1
        return dict_names_ports

    def run_names_with_dns(self, is_recusive: bool = False, title: str = '', label_session: str = ''):
        return self.__run_names_with_dns(self.DNS_address, self.list_names, is_recusive, title)

    def __run_names_with_dns(self, dns_main_ip, names, is_recusive: bool = False, title: str = '', label_session: str = ''):
        dict_names_ports = self.gen_port_names(names)

        self.dns_dict = {}
        time_sample = datetime.now()  # current date and time
        with alive_bar(len(names), title=title, theme='classic') as bar:  ## for something nice
            for name in dict_names_ports:
                port = dict_names_ports[name]
                self.send_DNS_request(dns_main_ip, name, port, bar, is_recusive=is_recusive)

        return self.dns_db.add_data_to_db(dns_main_ip, time_sample, self.dns_dict, label_session)

    def get_dict_times_of_dns(self, dns_ip: str, time_str: str):
        try:
            return self.json_dict_total[dns_ip][time_str], time_str
        except:
            return None, None

def wait_bar(interval_wait_sec: int = INTERVAL_WAIT_SEC):
    sec_time = interval_wait_sec if (interval_wait_sec > 0) else INTERVAL_WAIT_SEC
    with alive_bar(sec_time, title=f'Wait now {sec_time} seconds', theme='classic') as bar:
        for i in range(sec_time):
            time.sleep(1)
            bar()


def get_app_by_time(DNS_address, list_names, col_per_page = 1):

    # list_names = ['xinshipu.com']

    dns_fp_run = DNS_FP_runner(DNS_address, list_names)

    list_ans_vals = []
    list_times = [*dns_fp_run.json_dict_total[DNS_address]][-8*3:]
    for time_str in list_times:
        list_ans_vals += [dns_fp_run.get_dict_times_of_dns(DNS_address, time_str)]


    app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=col_per_page)
    app.runner()

