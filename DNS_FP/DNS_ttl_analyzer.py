from statistics import mean

from DNS_FP_runner import *
from dns_data_db import dns_data_db

class DNS_ttl_analyzer:
    def __init__(self, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        self.JSON_FILE = json_file_name if json_file_name.endswith('.json') else JSON_FILE_NAME_DEFAULT
        self.dns_data = dns_data_db(self.JSON_FILE)
        self.__json_dict = self.dns_data.get_all_results_dict()

    def get_time_and_ttl(self, dns_ip: str, domain_name: str):
        domain_ttl_data = {}
        ttl_max = float('-inf')
        for date in self.__json_dict[dns_ip]:
            try:
                d_specific_ttl = self.__json_dict[dns_ip][date][domain_name]
                ttl = d_specific_ttl['ttl']
                recv_time = d_specific_ttl['recv_time']
                domain_ttl_data[recv_time] = ttl
                ttl_max = max(ttl, ttl_max)
            except:
                continue
        return domain_ttl_data, ttl_max

    def servers_amount_by_domain_name(self, dns_ip: str, domain_name: str):
        d_time_ttl, ttl_max = self.get_time_and_ttl(dns_ip, domain_name)
        potential_servers_act = []
        for time_curr in d_time_ttl:
            ttl_curr = d_time_ttl[time_curr]
            # if ttl_curr == 0:
            #     continue
            if ttl_curr == 0:
                continue

            i = 0
            while i < len(potential_servers_act):
                (time_sus, ttl_sus) = potential_servers_act[i]
                if self.check_if_difference_valid(time_sus, ttl_sus, time_curr, ttl_curr, ttl_max):
                    potential_servers_act[i] = (time_curr, ttl_curr)
                    break
                i += 1
            if i == len(potential_servers_act):
                potential_servers_act += [(time_curr, ttl_curr)]
        return len(potential_servers_act)



    def check_if_difference_valid(self, time_1, ttl_1, time_2, ttl_2, ttl_max):
        time_diff = time_2 - time_1
        if ttl_1 > ttl_2:
            ttl_diff = ttl_1 - ttl_2
            if abs(time_diff - ttl_diff) > 1:
                return False
        else:
            # time difference must be grater than the left ttl
            # or the next ttl is less than the max
            if time_diff - ttl_1 < -1 or ttl_max > ttl_2:
                return False
        return True

    def run_all_domains(self, dns_ip, list_domain_names):
        sumry_anomaly = [self.servers_amount_by_domain_name(dns_ip, name) for name in list_domain_names]
        return round(mean(sumry_anomaly))
