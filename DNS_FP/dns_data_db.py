import json

import time
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR

MAX_WAIT = 5
JSON_FILE_NAME_DEFAULT = 'dns_data.json'
RESULTS = 'results'
SESSIONS = 'sessions'
FORMAT_TIME = "%m/%d/%Y, %H:%M:%S"


# the class that takes the packets ad stores it to the db
# currently now the db based on json

class dns_data_db:
    def __init__(self, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        self.JSON_FILE = json_file_name if json_file_name.endswith('.json') else JSON_FILE_NAME_DEFAULT
        self.json_dict_total = {}
        self.tests_sessions = {}

        self.__load_from_json(JSON_FILE_NAME_DEFAULT)
        # before deleted - we first save the data to the json
        atexit.register(self.save_and_update_db)

    def __load_from_json(self, name_json: str):
        if not os.path.exists(name_json):
            with open(name_json, 'w') as f:
                f.write(json.dumps({}))
        with open(name_json, 'r') as f:
            dict_from_json = json.loads(f.read())
            self.json_dict_total = dict_from_json[RESULTS] if RESULTS in dict_from_json else {}
            self.tests_sessions = dict_from_json[SESSIONS] if SESSIONS in dict_from_json else {}

    def get_all_results_dict(self):
        return self.json_dict_total.copy()

    def save_and_update_db(self):
        with open(self.JSON_FILE, 'w') as f:
            f.write(json.dumps({RESULTS: self.json_dict_total, SESSIONS: self.tests_sessions}))

    def add_data_to_db(self, dns_ip: str, time_when_taken: datetime, sample_dict_data: dict, label_session: str):
        dict_addr_final = {}
        time_str = time_when_taken.strftime(FORMAT_TIME)

        for name in sample_dict_data:
            dict_addr_final[name] = self.get_data_from_pkts(sample_dict_data[name])

        # self.load_from_json(self.JSON_FILE)
        if dns_ip not in self.json_dict_total:
            self.json_dict_total[dns_ip] = {}
        self.json_dict_total[dns_ip].update({time_str: dict_addr_final})

        if label_session not in self.tests_sessions:
            self.tests_sessions[label_session] = []

        self.tests_sessions[label_session] += [[dns_ip, time_str]]
        return dict_addr_final, time_str

    def get_dns_dict_by_ip_time(self, dns_ip: str, time_str: str):
        try:
            return self.json_dict_total[dns_ip][time_str].copy()
        except:
            return None

    def get_session_data_by_label(self, labes_sess: str):
        if labes_sess not in self.tests_sessions:
            return []

        list_all_data = []
        list_exist_names = {}
        for ip_time_arr in self.tests_sessions[labes_sess]:
            dns_ip = ip_time_arr[0]
            time_str = ip_time_arr[1]
            dict_dns_test = self.get_dns_dict_by_ip_time(dns_ip, time_str)
            if dict_dns_test is not None:
                list_all_data += [dict_dns_test]
                list_exist_names.update(set(dict_dns_test.keys()))

        return list_all_data, list(list_exist_names)

    def get_data_from_pkts(self, pkt_dict: dict):
        dns_addr = 'No answer received...'
        dns_ttl = 0
        dns_time = MAX_WAIT
        # the labels must be on that
        if ('pkt_recv' not in pkt_dict) or ('pkt_sent' not in pkt_dict):
            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': 0, 'recv_time': 0}

        answer = pkt_dict['pkt_recv']
        dns_req = pkt_dict['pkt_sent']

        if ((type(dns_req) is not IP) and (dns_req not in None)) or \
                ((type(answer) is not IP) and (answer not in None)):
            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': 0, 'recv_time': 0}

        sent_time = dns_req.sent_time
        recv_time = sent_time + MAX_WAIT if answer is None else answer.time
        if answer is not None:
            dns_addr = str(answer[DNS].summary()).replace('DNS Ans ', '').replace('"', '').replace(' ', '')
            dns_addr = dns_addr if len(dns_addr) > 0 else '--'
            dns_time = answer.time - dns_req.sent_time  # end - start
            dns_ttl = 0
            RR_ans = answer[DNS].ancount
            if RR_ans > 0:  # if requests came
                for i in range(RR_ans):
                    dns_ttl += answer[DNSRR][i].ttl
                dns_ttl = round(dns_ttl / RR_ans)  # get average

            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': sent_time,
                    'recv_time': recv_time}
