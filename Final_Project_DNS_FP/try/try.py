from DB.dns_db import DnsDBFiles
from DB.firebase.firebase_db import *
from dns_engine.dns_req_machine import DNS_FP_runner

dns_db = DnsDBFiles()
names = dns_db.get_list_domain_names()
runner = DNS_FP_runner('8.8.8.8', names)
print("started")
run_result = runner.run_names_with_dns(is_recursive=False)
print(run_result['wikipedia.org'])
fb_db = firebase_db()
fb_db.write_to_dns_try('try1', run_result['wikipedia.org'])