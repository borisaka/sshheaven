#!/usr/bin/env python
"""Pick server and start connection with VPNGate (http://www.vpngate.net/en/)"""
__author__ = "Andrea Lazzarotto"
__copyright__ = "Copyright 2014+, Andrea Lazzarotto"
__license__ = "GPLv3"
__version__ = "1.0"
__maintainer__ = "Andrea Lazzarotto"
__email__ = "andrea.lazzarotto@gmail.com"

from argparse import ArgumentParser
from geoip import geolite2
import base64, random, re, subprocess, sys, tempfile, time,  urllib
from cmd import exec_cmd
from cmd import upload_file

def process_args():
    parser = ArgumentParser(prog="vpngate", description='Connects to vpngate.')
    parser.add_argument("-c", "--countries", nargs='+', metavar="US NL", default=[],
            help="Allowed countries (default: all except current)")
    parser.add_argument("-ec", "--exclude-countries", nargs="+", metavar="CN UA", default=[])
    return parser.parse_args()

def whereami():
    ip = urllib.urlopen("https://wtfismyip.com/text").read().strip()
    return geolite2.lookup(ip)

def ls(*allowed_countries):
    def test_country(row):
        if len(allowed_countries) > 0:
            return any([re.search(",%s" % country, row) for country in allowed_countries])
        # elif len(exclude_countries) > 0:
            # print "Exclution list"
            # print exclude_countries
            # return any([re.search(",%s" % country, row) for country not in exclude_countries])
        else:
            return not re.search(",%s" % here, row) 
    def fetch():
        return urllib.urlopen("http://www.vpngate.net/api/iphone").read().split("\n")[2:]
    here = whereami().country
    raw_data = fetch()
    return [row.split(",")[-1] for row in raw_data if len(row) > 5000 and test_country(row)]

def connect(conf):
    _, path = tempfile.mkstemp()
    f = open(path, 'w')
    f.write(base64.b64decode(conf))
    f.close()
    upload_file(path, "/etc/openvpn/myvpn.ovpn")
    exec_cmd("ovpnup")
    
def main():
    exec_cmd("ovpndown")
    allowed_countries = process_args().countries
    # try:
    connect(random.choice(ls(*allowed_countries)))
        # pid.wait()
    # except KeyboardInterrupt:
        # sys.exit(1)

if __name__ == "__main__": 
    main()
