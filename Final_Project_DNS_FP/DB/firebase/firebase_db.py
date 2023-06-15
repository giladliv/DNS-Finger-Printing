import os

import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import *
import datetime

root_collection = 'active-hosts'
##### IMPORTANT WRITE ALL OF THIS INTO A CLASS!!!!

class firebase_db:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))    # Get the path to the current script
        file_path = os.path.join(current_dir, 'ServiceAccountKey.json')     # Construct the relative file path

        cred = credentials.Certificate(file_path)
        firebase_admin.initialize_app(cred)
        self.db: Client = firestore.client()

    def write_data_db(self, host_ip, queried_domain  , data : dict):
        self.db.collection(root_collection).document(host_ip).collection(queried_domain).add(data)

    def get_all_dns_by_host_ip(self,host_ip):
        doc_ref = self.db.collection(root_collection).document(host_ip)
        dns_data_snapshot = doc_ref.get()
        dns_data = {}
        if dns_data_snapshot.exists:
            dns_data = dns_data_snapshot.to_dict()
            print(dns_data)

        for key in dns_data:
            for queried_domain in dns_data[key]:
               self.get_queried_domain_by_host( host_ip , queried_domain)

    def get_queried_domain_by_host(self,host_ip,queried_domain):
        doc_ref = self.db.collection(root_collection).document(host_ip).collection(queried_domain)
        dns_data_snapshot = doc_ref.get()  # this is duplicate code , refactor
        # returns documents , and we print them
        for snapshot in dns_data_snapshot:
            dns_data = snapshot.to_dict()
            print(dns_data)

    def get_all_dns(self):
        pass

    def write_to_dns_try(self, doc_name, data):
        return self.db.collection('try').document(doc_name).set(data)


#get_queried_domain_by_host('127.0.0.1','google.com')
#get_all_dns_by_host_ip('127.0.0.1')