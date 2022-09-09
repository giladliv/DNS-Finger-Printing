import argparse
from DNS_FP_runner import *
from DNS_ttl_analyzer import *
from cache_graph_gui import *

FILE_NAME_DOMAIN = 'list_of_domain_names.txt'

def get_domain_name_list(file_name_domains: str):
    with open(file_name_domains, 'r') as f:
        return f.read().replace('\r', '').split('\n')

def run_session(DNS_address: str, list_names: list, session_name: str = '', repeats: int = 8,
                interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True,
                to_show_results: bool = True, json_file_name: str = JSON_FILE_NAME_DEFAULT):

    session_name = datetime.now().strftime(FORMAT_TIME) if session_name == '' else session_name
    dns_fp_run = DNS_FP_runner(DNS_address, list_names, json_file_name)

    list_ans_vals = []
    for i in range(repeats):
        is_rec = (i == 0) and is_first_rec
        str_title = f'round %d out of %d' % (i + 1, repeats)
        list_ans_vals += [dns_fp_run.run_names_with_dns(is_recusive=is_rec, title=str_title, label_session=session_name)]
        if i == repeats - 1:
            continue
        wait_bar(interval_wait_sec)

    dns_fp_run.save_db()
    print()
    ans_rec = 'IS' if dns_fp_run.is_recursive_DNS() else 'is NOT'
    print(f'the DNS server {DNS_address} : {ans_rec} an auto-recoesive dns')
    if to_show_results:
        app = pic_of_plot(DNS_address, list_names, list_ans_vals, cols_in_plot=1)
        app.runner()

def run_dns_cache_gui(ip_dns: str, names_file: str, session_name: str = '', repeats: int = 8,
                      interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True, json_file_name: str = JSON_FILE_NAME_DEFAULT):
    list_names = get_domain_name_list(names_file)
    run_session(ip_dns, list_names, session_name=session_name, repeats=repeats, json_file_name=json_file_name,
                interval_wait_sec=interval_wait_sec, is_first_rec=is_first_rec, to_show_results=True)

def run_analyzer(ip_dns: str, names_file: str, session_name: str = '', repeats: int = 10,
                      interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True, json_file_name: str = JSON_FILE_NAME_DEFAULT):
    list_names = get_domain_name_list(names_file)
    print('WARNING: the check is not suitable and very in accurate for non-auto-recursive dns servers\n\n')
    for i in range(repeats):
        print('session number', i)
        run_session(ip_dns, list_names, session_name=session_name, json_file_name=json_file_name,
                    interval_wait_sec=2, is_first_rec=is_first_rec, repeats=2, to_show_results=False)
        if i == repeats - 1:
            continue

        print()
        print('break between sessions minutes')
        wait_bar(interval_wait_sec)
        print()

    analyzer = DNS_ttl_analyzer(json_file_name)
    print('there are', analyzer.run_all_domains(ip_dns, list_names), 'server behind this one')

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])

def main():

    print('DNS Cache probing tool v1.0.1')
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--analyze', action='store_true', help='if this flag is up than the analyzer program will be activated, '
                                                                        'else the regular progam')
    parser.add_argument('-ip', '--ip_dns', required=True, help='the DNS server ip address')
    parser.add_argument('-nf', '--domain_names_file', default=FILE_NAME_DOMAIN, help='the file name of the domain names')
    parser.add_argument('-jf', '--json_file_name', default=JSON_FILE_NAME_DEFAULT, help='the name of the json file that '
                                                                                      'established as the dns')
    parser.add_argument('-sn', '--session_name', default='', help='the name of current session of running')
    parser.add_argument('-r', '--repeats', type=int, default=8, help='the number of intervals in session: how many repeats on query in one session')
    parser.add_argument('-w', '--wait_sec', type=int, default=10, help='seconds of waiting between intervals in session')
    parser.add_argument('-fnc', '--first_not_recursive', action='store_true', help='if you wish that the first run won\'t '
                                                                                   'be recurssive activate this flag')

    # def run_dns_cache_gui(ip_dns: str, names_file: str, session_name: str = '', repeats: int = 8,
    #                       interval_wait_sec: int = INTERVAL_WAIT_SEC, is_first_rec: bool = True,
    #                       json_file_name: str = JSON_FILE_NAME_DEFAULT):

    args = parser.parse_args()
    is_first_rec = not args.first_not_recursive
    if args.analyze:
        run_analyzer(ip_dns=args.ip_dns, names_file=args.domain_names_file, json_file_name=args.json_file_name,
                          session_name=args.session_name, repeats=args.repeats, interval_wait_sec=args.wait_sec,
                          is_first_rec=is_first_rec)
    else:
        run_dns_cache_gui(ip_dns=args.ip_dns, names_file=args.domain_names_file, json_file_name=args.json_file_name,
                          session_name=args.session_name, repeats=args.repeats, interval_wait_sec=args.wait_sec,
                          is_first_rec=is_first_rec)

# 94.153.241.134 - intresting
# 88.80.64.8 - good dns for check
if __name__ == "__main__":
    install_and_import('alive_progress')
    install_and_import('argparse')
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)