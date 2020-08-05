from qaenv import mongo_ip
import pymongo
import pandas as pd

class QIFI_Portfolio():
    
    def __init__(self, account_cookies: list, mongo_ip: str = mongo_ip):

        """
        主要是用于满足对于多个QIFIAccount的管理
        """

        self.db =  pymongo.MongoClient(mongo_ip).QAREALTIME
        self.account_cookies = account_cookies

    def reload_account(self):
        pass
