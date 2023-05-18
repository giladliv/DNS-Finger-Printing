# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from dns_engine.dns_req_machine import *
import pprint

def main():
    names = get_domain_name_list('data/list_of_domain_names.txt')
    runner = DNS_FP_runner('8.8.8.8', names)
    print("started")
    run_result = runner.run_names_with_dns(is_recursive=True)

    for name in run_result:
        print(f'{name}:')
        pprint.pprint(runner.get_data_from_pkts(run_result[name]))



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
