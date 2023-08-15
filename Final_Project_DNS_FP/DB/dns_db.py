from DB.idns_db import *
from utils.utils import *
from DB.db_utils import *

F_DOMAIN_NAMES = '../data/list_of_domain_names.txt'
F_DNS_SERVER_IP = '../data/list_dns_servers_ip.txt'
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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

# db_files = DnsDBFiles()
# print(db_files.get_list_dns_server_ip())


class DNSJsonDB(IDNS_DB):
    def __init__(self, file_name: str = os.path.join(SCRIPT_DIR, 'test_data.json')):
        self.dns_server_ip = {}
        self.domain_names = {}
        self.tester_names = []
        self.sites = []
        self.file_name = file_name
        self.load_from_json()

    def to_tict(self):
        dict_data = self.__dict__.copy()
        del dict_data['file_name']
        return dict_data

    def save_to_json(self):
        save_json(self.to_tict(), self.file_name)

    def load_from_json(self):
        self.set_from_dict(load_json(self.file_name))

    def set_from_dict(self, src_dict: dict):
        for key in src_dict:
            if key in self.__dict__.keys():
                setattr(self, key, src_dict[key])

    # Getter for dns_server_ip field
    def get_dns_server_ip(self):
        return self.dns_server_ip

    # Getter for domain_names field
    def get_domain_names(self):
        return self.domain_names

    # Getter for tester_names field
    def get_tester_names(self):
        return self.tester_names

    # Getter for sites field
    def get_sites(self):
        return self.sites



    #def set_
def set_my_file():
    db = DNSJsonDB()
    db_files = DnsDBFiles()
    print(db.to_tict(), db.file_name)

    db.dns_server_ip = {'base': db_files.get_list_dns_server_ip(), 'other': ['']}
    db.domain_names = {'group 1': db_files.get_list_domain_names(), 'group 2': ['']}
    db.tester_names = ['Gilad', 'David', 'Irit']
    db.sites = ['home', 'lab']

    db.save_to_json()

# set_my_file()