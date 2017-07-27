# Source Generated with Decompyle++
# File: provider.pyc (Python 2.7)

import os
import urllib
import base64
import yaml
import json
from datetime import datetime
import time
import config
from common import *

class Provider:
    
    def __init__(self, ssh_context, allow_countries, reject_countries):
        self.cache_path = './tmp'
        self.allow_countries = allow_countries
        self.reject_countries = reject_countries
        self.ssh_context = ssh_context
        self.logger = config.logger
        if not os.path.exists('./tmp'):
            os.makedirs('./tmp')

    
    def connect(self, server):
        f = open('./tmp/config.ovpn', 'w')
        f.write(server.config)
        f.close()
        self.ssh_context.exec_command('rm %s' % config.vpn_config_path)
        self.ssh_context.upload_file('./tmp/config.ovpn', config.vpn_config_path)
        self.ssh_context.exec_command('openvpn --config %s' % config.vpn_config_path)

    connect = ensure_file('./tmp/config.ovpn')(connect)
    
    def disconnect_all(self):
        self.ssh_context.exec_command('killall openvpn')

    
    def find_server(self):
        return self.ordered_servers()[0]

    
    def ordered_servers(self):
        self.logger.debug('ATTEMP TO LOAD SERVERS FROM ./tmp/servers.txt')
        cached_time = datetime.fromtimestamp(self.stat_get('fetched_servers_time', default = time.mktime(datetime.min.timetuple())))
        delta = datetime.now() - cached_time
        self.logger.debug('DELTA: %d' % delta.seconds)
        if delta.seconds > 1200:
            self.logger.debug('CACHE IS EXPIRED OR DOES NOT EXIST')
            self.fetch_servers()
        continue
        hosts = [ h.split(',') for h in open('./tmp/servers.txt', 'r').readlines()[2:-1] ]
        hosts = map((lambda h: VpnHost(h[1], h[6], h[5], h[11], h[-1])), hosts)
        hosts = (filter,)((lambda h: h.ip not in self.history_get()), hosts)
        if len(self.allow_countries) > 0:
            hosts = (filter,)((lambda h: h.country_short in self.allow_countries), hosts)
        elif len(self.reject_countries) > 0:
            hosts = (filter,)((lambda h: h.country_short not in self.reject_countries), hosts)
        return hosts

    
    def fetch_servers(self):
        self.logger.debug('FETCHING SERVERS FROM PROVIDER....')
        data = urllib.urlopen('http://www.vpngate.net/api/iphone').read()
        self.logger.debug('SERVERS FETCHED.... Caching')
        write_file('./tmp/servers.txt', data)
        self.logger.debug('SERVERS STORED TO ./tmp/servers.txt')
        self.stat_put('fetched_servers_time', time.time())
        return data

    fetch_servers = ensure_file('./tmp/servers.txt')(fetch_servers)
    
    def history_get(self):
        return map((lambda h: h.strip()), open('./tmp/hist.txt', 'r').readlines())

    history_get = ensure_file('./tmp/hist.txt')(history_get)
    
    def history_put(self, host):
        history = self.history_get()
        write_file('./tmp/hist.txt', '\n'.join([
            host] + history[0:9]))

    history_put = ensure_file('./tmp/hist.txt')(history_put)
    
    def stat_get(self, stat, default = None):
        stats = json.loads(read_file('./tmp/stats.json'))
        return stats.get(stat, default)

    stat_get = ensure_file('./tmp/stats.json', '{}')(stat_get)
    
    def stat_put(self, stat, value):
        stats = json.loads(read_file('./tmp/stats.json'))
        stats[stat] = value
        write_file('./tmp/stats.json', json.dumps(stats))

    stat_put = ensure_file('./tmp/stats.json', '{}')(stat_put)

if __name__ == '__main__':
    print Provider().ordered_servers()
