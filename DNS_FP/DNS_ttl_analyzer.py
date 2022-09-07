from DNS_FP_runner import *

class DNS_ttl_analyzer:
    def __init__(self, json_file_name: str = JSON_FILE_NAME_DEFAULT):
        self.JSON_FILE = json_file_name if json_file_name.endswith('.json') else JSON_FILE_NAME_DEFAULT
        self.load_from_json(self.JSON_FILE)

    def load_from_json(self, name_json: str):
        if not os.path.exists(name_json):
            with open(name_json, 'w') as f:
                f.write(json.dumps({}))
        with open(name_json, 'r') as f:
            self.__json_dict = json.loads(f.read())

    def get_time_and_ttl(self, dns_ip: str, domain_name: str):
        domain_ttl_data = {}
        ttl_max = float('-inf')
        for date in self.__json_dict[dns_ip]:
            d_specific_ttl = self.__json_dict[dns_ip][date][domain_name]
            if 'ttl' not in d_specific_ttl or 'recv_time' not in d_specific_ttl:
                continue
            ttl = d_specific_ttl['ttl']
            recv_time = d_specific_ttl['recv_time']
            domain_ttl_data[recv_time] = ttl
            ttl_max = max(ttl, ttl_max)
        return domain_ttl_data, ttl_max

    def check_ttl_dict(self, d_time_ttl: dict, ttl_max):
        time_list = list(d_time_ttl.keys())
        res = list(zip(time_list, time_list[1:] + time_list[:1]))
        del res[-1]
        for (time_1, time_2) in res:
            ttl_1 = d_time_ttl[time_1]
            ttl_2 = d_time_ttl[time_2]
            time_diff = time_2 - time_1
            if ttl_1 > ttl_2:
                ttl_diff = ttl_1 - ttl_2
                if abs(time_diff - ttl_diff) >= 1:
                    time_diff = round(time_diff)
                    print(f'time 1: {time_1},\tttl1: {ttl_1} \t time 2: {time_2},\tttl2: {ttl_2}')
                    print(f'diffs are not as the same: {time_diff} != {ttl_diff}\n')
            else:
                # time difference must be grater than the left ttl
                # or the next ttl is less than the max
                if time_diff - ttl_1 <= -1 or ttl_max > ttl_2:
                    time_diff = round(time_diff)
                    print(f'****** time 1: {time_1},\tttl1: {ttl_1} \t time 2: {time_2},\tttl2: {ttl_2}')
                    print(f'****** time hasn\'t pass the TTL counting: {time_diff} << {ttl_1}\n')

    #def check_if_difference_valid(self, time_1, ttl_1, time_2, ttl_2):



analyzer = DNS_ttl_analyzer()
d_time_ttl, ttl_max = analyzer.get_time_and_ttl('94.153.241.134', 'amitdvir.com')
print(d_time_ttl)

analyzer.check_ttl_dict(d_time_ttl)
