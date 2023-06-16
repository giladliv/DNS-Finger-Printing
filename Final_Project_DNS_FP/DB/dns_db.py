from DB.idns_db import *
from utils.utils import *

F_DOMAIN_NAMES = 'data/list_of_domain_names.txt'
F_DNS_SERVER_IP = 'data/list_dns_servers_ip.txt'


class DnsDBFiles(IDNS_DB):

    def __init__(self, f_dns_server_ip: str = F_DNS_SERVER_IP, f_domain_names: str = F_DOMAIN_NAMES):
        # super().__init__()
        self.__update_dns_server_ip(f_dns_server_ip)
        self.__update_domain_names(f_domain_names)

    def __update_dns_server_ip(self, f_dns_server_ip: str):
        self.f_dns_server_ip = f_dns_server_ip
        try:
            self.list_dns_server_ip = get_lines_from_file(self.f_dns_server_ip)
        except:
            self.list_dns_server_ip = None

    def __update_domain_names(self, f_domain_names: str):
        self.f_domain_names = f_domain_names
        try:
            self.list_domain_names = get_lines_from_file(self.f_domain_names)
        except:
            self.list_domain_names = None

    def get_list_dns_server_ip(self):
        return self.list_dns_server_ip

    def get_list_domain_names(self):
        return self.list_domain_names

    @staticmethod
    def get_list_of_testers():
        return ['Gilad', 'David', 'Irit']