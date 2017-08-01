#!/usr/bin/env python2.7
import time
import sys
PROMT = "shost:~/x/y >%"
ALLOWED = ['promt']
def main(mode):
    def promt():
        print PROMT

    def ifconfig():
        promt()
        print open('./tests/stubs/ifconfig.txt').read()
    def netstat():
        promt()
        print open('./tests/stubs/netstat-nr.txt').read()
        promt()

    locals()[mode]()

if __name__ == "__main__":
    main(sys.argv[1])
