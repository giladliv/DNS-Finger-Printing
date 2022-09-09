import json

import time
from scapy.all import *
from scapy.layers.dns import DNS, DNSRR

MAX_WAIT = 5
JSON_FILE_NAME_DEFAULT = 'data/dns_data.json'
RESULTS = 'results'
SESSIONS = 'sessions'
FORMAT_TIME = "%m/%d/%Y, %H:%M:%S"


# the class that takes the packets ad stores it to the db
# currently now the db based on json

class dns_data_db:
    """
    the class that takes the packets' samples data manage it in the db
    currently now the db based on json
    """
    def __init__(self, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        """
        c'tor - loads the json file
        @param json_file_name: the file name of the db
        """
        self.JSON_FILE = json_file_name if json_file_name.endswith('.json') else JSON_FILE_NAME_DEFAULT
        self.json_dict_total = {}
        self.tests_sessions = {}

        self.__load_from_json(JSON_FILE_NAME_DEFAULT)
        # before deleted - we first save the data to the json
        atexit.register(self.save_and_update_db)

    def __load_from_json(self, name_json: str):
        """
        by given string the function loads the json file to the class' dictionary
        @param name_json: db file name
        """
        if not os.path.exists(name_json):
            with open(name_json, 'w') as f:
                f.write(json.dumps({}))
        with open(name_json, 'r') as f:
            dict_from_json = json.loads(f.read())
            # loads the results of the samples
            self.json_dict_total = dict_from_json[RESULTS] if RESULTS in dict_from_json else {}
            # loads the sessions labelling and partition
            self.tests_sessions = dict_from_json[SESSIONS] if SESSIONS in dict_from_json else {}

    def get_all_results_dict(self):
        """
        @return: dict of all of the results
        """
        return self.json_dict_total.copy()

    def save_and_update_db(self):
        """
        save the data that stored to the json file
        """
        with open(self.JSON_FILE, 'w') as f:
            f.write(json.dumps({RESULTS: self.json_dict_total, SESSIONS: self.tests_sessions}))

    def add_data_to_db(self, dns_ip: str, time_when_taken: datetime, sample_dict_data: dict, label_session: str):
        """
        the function add result of whole sample to the db (json-file)
        @param dns_ip: dns server ip
        @param time_when_taken: time that the sample has been taken
        @param sample_dict_data: the data of entire sample
        @param label_session: name of session to take it in consider
        @return: (dict, str) - dict of the samples data, and time that taken in string
        """
        dict_addr_final = {}
        time_str = time_when_taken.strftime(FORMAT_TIME)

        # parse each sample packets and save it to the dictionary
        for name in sample_dict_data:
            dict_addr_final[name] = self.get_data_from_pkts(sample_dict_data[name])

        # update the dict of results from the new results
        if dns_ip not in self.json_dict_total:
            self.json_dict_total[dns_ip] = {}
        self.json_dict_total[dns_ip].update({time_str: dict_addr_final})

        # update the name labels list
        if label_session not in self.tests_sessions:
            self.tests_sessions[label_session] = []
        self.tests_sessions[label_session] += [[dns_ip, time_str]]

        return dict_addr_final, time_str

    def get_dns_dict_by_ip_time(self, dns_ip: str, time_str: str):
        """ return data by dns server ip address and time in str format """
        try:
            return self.json_dict_total[dns_ip][time_str].copy()
        except:
            return None

    def get_session_data_by_label(self, labes_sess: str):
        """
        recover samples of queries by labes name
        @param labes_sess: label name
        @return: (dict , list) : dict that conatins list of all data dictionaries, by sample, and dict of list of all the names
        """
        if labes_sess not in self.tests_sessions:
            return []

        dict_all_data = {}
        dict_exist_names = {}
        for ip_time_arr in self.tests_sessions[labes_sess]:
            dns_ip = ip_time_arr[0]
            time_str = ip_time_arr[1]
            dict_dns_test = self.get_dns_dict_by_ip_time(dns_ip, time_str)
            if dict_dns_test is not None:
                if dns_ip not in dict_all_data:
                    dict_all_data[dns_ip] = []
                dict_all_data[dns_ip] += [dict_dns_test]
                if dns_ip not in dict_exist_names:
                    dict_exist_names[dns_ip] = {}
                dict_exist_names[dns_ip].update(set(dict_dns_test.keys()))

        return dict_all_data, dict_exist_names

    def get_data_from_pkts(self, pkt_dict: dict):
        """
        the function parsers the query's answer that got from the DNS_FP_runner class
        @param pkt_dict: the dict that contains the sent and received packets
        @return: dictionary of the wanted data
        """
        dns_addr = 'No answer received...'
        dns_ttl = 0
        dns_time = MAX_WAIT
        # if keys doesnt match to the pkt then return generic message
        if ('pkt_recv' not in pkt_dict) or ('pkt_sent' not in pkt_dict):
            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': 0, 'recv_time': 0}

        answer = pkt_dict['pkt_recv']
        dns_req = pkt_dict['pkt_sent']
        # if the packets aren't None nor packet class then return with generic ans
        if ((type(dns_req) is not IP) and (dns_req is not None)) or \
                ((type(answer) is not IP) and (answer is not None)):
            return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': 0, 'recv_time': 0}

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

        return {'time': dns_time, 'addr': dns_addr, 'ttl': dns_ttl, 'sent_time': sent_time, 'recv_time': recv_time}
