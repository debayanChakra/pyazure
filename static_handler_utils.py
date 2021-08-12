import yaml
import os, sys
import logging
from netaddr import *
import subprocess


class StaticHandlers:
    _path = 'secrets.yml'

    def __init__(self):
        pass

    @staticmethod
    def break_ip_range(iprange, cidr):
        ip_addr = []
        ip = IPNetwork(iprange)
        address = (ip.subnet(cidr))

        for i in address:
            ip_addr.append(str(i))

        return ip_addr

    @staticmethod
    def read_secret():
        with open(StaticHandlers._path) as secrets:
            secret_details = yaml.safe_load(secrets)
            return secret_details

    @staticmethod
    def check_dir(dir_path):
        '''
        :checking directory is exist or not
        '''
        is_exist = os.path.isdir(dir_path)
        return is_exist

    @staticmethod
    def create_dir(dir_path):
        try:
            os.mkdir(dir_path)
            logging.info("Directory is created")
            return
        except OSError as ose:
            logging.error(ose)
            sys.exit(1)

