# https://blog.apnic.net/2021/06/22/cache-me-outside-dns-cache-probing/
# https://publicdnsserver.com/
import logging
import time
from datetime import datetime
from random import sample
import random
from alive_progress import alive_bar
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR, DNSQR
from scapy.layers.inet import IP, UDP

from utils.utils import *

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

INTERVAL_WAIT_SEC = 10
MAX_WAIT = 5
PKT_SENT = 'pkt_sent'
PKT_RECV = 'pkt_recv'

class DNS_FP_runner:
    """ the class runs the DNS queries and manage the sessions """
    def __init__(self, DNS_address: str, list_names: list, json_file_name: str = ""):
        """
        c'tor the class
        @param DNS_address: the dns server ip
        @param list_names: the list of domain names
        @param json_file_name: the json (the db) file name
        """
        if not DNS_FP_runner.is_ipv4(DNS_address):
            raise ValueError(f'the given string: {DNS_address} is not an ipv4 format')
        self.DNS_address = DNS_address
        # TODO: add type of reading data
        self.json_dict_total = {}
        self.dns_dict = {}

        self.list_names = list_names
        self.reset_rd_illegal_count()
        # TODO: add saving data option
        self.FREE_PORTS = list(range(1024, 65535))

    def save_db(self):
        """ saves the content of the db to its file """
        # save all changes - is it relevant ?

    @staticmethod
    def is_ipv4(ip_addr: str):
        """
        @param ip_addr: string that ought to the the ipv4
        @return: bool - if the string is in ipv4 format
        """
        list_nums = ip_addr.split(".")
        if len(list_nums) != 4:
            return False
        try:
            for i in list_nums:
                if int(i) < 0 or int(i) > 255:
                    return False
            return True
        except:
            return False


    def reset_rd_illegal_count(self):
        """ reset the rd counters """
        self.rd_counter = 0
        self.pkt_counter = 0

    def is_recursive_DNS(self):
        """ check if the dns server if auto-recursive by the counting """
        if self.pkt_counter == 0:
            return False
        return (self.rd_counter / self.pkt_counter) > 0.5

    def send_DNS_request(self, dns_server_ip: str, name_domain: str, src_port: int, bar, is_recursive: bool = False, sec_timeout: int = MAX_WAIT):
        """
        the function sends query of donamin name and get it back to specific dns server ip
        @param dns_server_ip: ip of dns server
        @param name_domain: name of website / domain to check its ip
        @param src_port: the src port that the packet sended with
        @param bar: the progress bar function - when completen adds to the bar
        @param is_recursive: when True the query is recursive, else it's iterative
        @param sec_timeout: time out in sec for each query
        @return: dict of the sent and recived packet
        """
        rd_flag = 1 if is_recursive else 0
        answer = None
        i = 0
        dns_req = IP()
        while answer is None and i < 4:
            dns_req = IP(dst=dns_server_ip) / \
                      UDP(sport=src_port, dport=53) / \
                      DNS(rd=rd_flag, qd=DNSQR(qname=name_domain))
            answer = sr1(dns_req, verbose=0, timeout=sec_timeout)
            src_port = random.randint(1024, 65535)
            i += 1
        # bar()

        # count rd that has been chanched by the dns server
        if (answer is not None) and (not is_recursive):
            self.rd_counter += answer[DNS].rd
            self.pkt_counter += 1

        return name_domain, {PKT_RECV: answer, PKT_SENT: dns_req}

    def gen_port_names(self, add_names):
        """
        creates pairs for each cell in the array with unique port
        @param add_names: the list of domain names
        @return: dict of name-port values
        """
        ports = sample(self.FREE_PORTS, len(add_names))
        dict_names_ports = {}
        for name, port in zip(add_names, ports):
            dict_names_ports[name] = port
        return dict_names_ports

    def run_names_with_dns(self, is_recursive: bool = False, title: str = '', label_session: str = ''):
        """
        run one sample of queries for all the domain names that are in the class and saves it to the db
        @param is_recursive: if the queries must be recursive (else iterative)
        @param title: the title of the progress bar
        @param label_session: name of the total session - for restoring data
        @return: (dict, str) - dict of the samples data, and time that taken in string
        """
        return self.__run_names_with_dns(self.DNS_address, self.list_names, is_recursive, title, label_session=label_session)

    def __run_names_with_dns(self, dns_main_ip, names, is_recursive: bool = False, title: str = '', label_session: str = ''):
        dict_names_ports = self.gen_port_names(names)

        self.dns_dict = {}
        time_sample = datetime.now()  # current date and time
        with alive_bar(len(names), title=title, theme='classic') as bar:  # for showing progress of the packets
            for name in dict_names_ports:
                port = dict_names_ports[name]
                name_domain, dns_packets = self.send_DNS_request(dns_main_ip, name, port, bar, is_recursive=is_recursive)  # run dns query
                self.dns_dict[name_domain] = dns_packets
                bar()

        # store the result to the db and return it
        # TODO: add the save to the db
        #return self.dns_db.add_data_to_db(dns_main_ip, time_sample, self.dns_dict, label_session)
        return self.dns_dict

    @staticmethod
    def get_data_from_pkts(pkt_dict: dict):
        """
        the function parsers the query's answer that got from the DNS_FP_runner class
        @param pkt_dict: the dict that contains the sent and received packets
        @return: dictionary of the wanted data
        """
        dns_addr = 'No answer received...'
        dns_ttl = 0
        dns_time = MAX_WAIT
        # if keys doesn't match to the pkt then return generic message
        if (PKT_RECV not in pkt_dict) or (PKT_SENT not in pkt_dict):
            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl,
                    'sent_time': 0, 'recv_time': 0, PKT_SENT: None, PKT_RECV: None}

        dns_req = pkt_dict[PKT_SENT]
        answer = pkt_dict[PKT_RECV]
        # if the packets aren't None nor packet class then return with generic ans
        if ((type(dns_req) is not IP) and (dns_req is not None)) or \
                ((type(answer) is not IP) and (answer is not None)):
            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': 0, 'recv_time': 0,
                    PKT_SENT: dns_req, PKT_RECV: answer}

        sent_time = dns_req.sent_time
        recv_time = sent_time + MAX_WAIT if (answer is None) else answer.time   # max data if answer couldn't recv
        if answer is not None:
            # parse the answer
            dns_addr = str(answer[DNS].summary()).replace('DNS Ans ', '').replace('"', '').replace(' ', '')
            dns_addr = dns_addr if len(dns_addr) > 0 else '--'
            # get the interval time
            dns_time = answer.time - dns_req.sent_time
            # if there are answers then get its average
            RR_ans = answer[DNS].ancount
            if RR_ans > 0:  # if requests came
                for i in range(RR_ans):
                    dns_ttl += answer[DNSRR][i].ttl
                dns_ttl = round(dns_ttl / RR_ans)  # get average

        return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': sent_time, 'recv_time': recv_time,
                PKT_SENT: dns_req, PKT_RECV: answer}

def run_session(DNS_address: str, list_names: list, session_name: str = '', repeats: int = 8,
                interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True,
                to_show_results: bool = True, json_file_name: str = JSON_FILE_NAME_DEFAULT):
    """
    run session of queries
    """
    session_name = datetime.now().strftime(FORMAT_TIME) if session_name == '' else session_name
    dns_fp_run = DNS_FP_runner(DNS_address, list_names, json_file_name)

    list_ans_vals = []
    for i in range(repeats):
        is_rec = (i == 0) and is_first_rec
        str_title = f'round %d out of %d' % (i + 1, repeats)
        list_ans_vals += \
            [dns_fp_run.run_names_with_dns(is_recursive=is_rec, title=str_title, label_session=session_name)]
        if i == repeats - 1:
            continue
        wait_bar(interval_wait_sec)

    return list_ans_vals, session_name

def run_session_ip_list(DNS_address_list: list, list_names: list, session_name: str = '', repeats: int = 8,
                interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True,
                to_show_results: bool = True, json_file_name: str = JSON_FILE_NAME_DEFAULT):
    """
    run session of queries
    """
    session_name = datetime.now().strftime(FORMAT_TIME) if session_name == '' else session_name

    for dns_addr in DNS_address_list:
        # TODO - enter saving data
        run_session(dns_addr, list_names, session_name=session_name, repeats=repeats,
                    interval_wait_sec=interval_wait_sec, is_first_rec=is_first_rec,
                    to_show_results=to_show_results, json_file_name=json_file_name)

    return list_ans_vals, session_name


def wait_bar(interval_wait_sec: int = INTERVAL_WAIT_SEC):
    """
    creates a waiting progress bar for x seconds
    @param interval_wait_sec: number of seconds to wait
    """
    sec_time = interval_wait_sec if (interval_wait_sec > 0) else INTERVAL_WAIT_SEC
    with alive_bar(sec_time, title=f'Wait now {sec_time} seconds', theme='classic') as bar:
        for i in range(sec_time):
            time.sleep(1)
            bar()

def get_domain_name_list(file_name_domains: str):
    with open(file_name_domains, 'r') as f:
        return [s.replace('\n', '') for s in f.readlines()]