# https://blog.apnic.net/2021/06/22/cache-me-outside-dns-cache-probing/
# https://publicdnsserver.com/

# logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from random import sample
from alive_progress import alive_bar
from classes.dns_data_db import *

INTERVAL_WAIT_SEC = 10

class DNS_FP_runner:
    """ the class runs the DNS queries and manage the sessions """
    def __init__(self, DNS_address: str, list_names: list, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        """
        c'tor the class
        @param DNS_address: the dns server ip
        @param list_names: the list of domain names
        @param json_file_name: the json (the db) file name
        """
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
        """ saves the content of the db to its file """
        self.dns_db.save_and_update_db()

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
        except:
            return False
        return True

    def reset_rd_illegal_count(self):
        """ reset the rd counters """
        self.rd_counter = 0
        self.pkt_counter = 0

    def is_recursive_DNS(self):
        """ check if the dns server if auto-recursive by the counting """
        if self.pkt_counter == 0:
            return False
        return (self.rd_counter / self.pkt_counter) > 0.5

    def send_DNS_request(self, dns_server: str, name_domain: str, src_port: int, bar, is_recursive: bool = False, sec_timeout: int = MAX_WAIT):
        """
        the function sends query of donamin name and get it back to specific dns server ip
        @param dns_server: ip of dns server
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
            dns_req = IP(dst=dns_server) / UDP(sport=src_port, dport=53) / DNS(rd=rd_flag, qd=DNSQR(qname=name_domain))
            answer = sr1(dns_req, verbose=0, timeout=sec_timeout)
            src_port = random.randint(1024, 65535)
            i += 1
        bar()

        # count rd that has been chanched by the dns server
        if (answer is not None) and (not is_recursive):
            self.rd_counter += answer[DNS].rd
            self.pkt_counter += 1

        self.dns_dict[name_domain] = {'pkt_recv': answer, 'pkt_sent': dns_req}

    def gen_port_names(self, add_names):
        """
        creates pairs for each cell in the array with unique port
        @param add_names: the list of domain names
        @return: dict of name-port values
        """
        ports = sample(self.FREE_PORTS, len(add_names))
        dict_names_ports = {}
        i = 0
        for name in add_names:
            dict_names_ports[name] = ports[i]
            i += 1
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
                self.send_DNS_request(dns_main_ip, name, port, bar, is_recursive=is_recursive)  # run dns query

        # store the result to the db and return it
        return self.dns_db.add_data_to_db(dns_main_ip, time_sample, self.dns_dict, label_session)


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