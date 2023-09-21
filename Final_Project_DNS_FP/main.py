from DB.dns_db import DnsDBFiles
from dns_engine.dns_req_machine import *
import pprint

def main():
    dns_db = DnsDBFiles()
    names = dns_db.get_list_domain_names()
    # runner = DNS_FP_runner('8.8.8.8', names)
    # print("started")
    # run_result = runner.run_names_with_dns(is_recursive=False)
    #
    # for name in run_result:
    #     print(f'{name}:')
    #     pprint.pprint(runner.get_data_from_pkts(run_result[name]))
    return_data = run_session_ip_list(['8.8.8.8'], list_names=names)
    pprint.pprint(return_data)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
