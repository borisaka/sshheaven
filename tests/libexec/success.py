#!/usr/bin/env/python2.7
import time
promt = "shost:~/x/y >%"

def main():
    time.sleep(3)
    print promt
    print open("./tests/stubs/ifconfig.txt","r").read()
    time.sleep(13)
    print promt
    exit(0)
    
