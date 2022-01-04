#! /usr/bin/env python3

from os import access, chdir, makedirs, mkdir
from pexpect import pxssh 
import pexpect
import configparser
import getpass
import sys 
import tempfile
import crypt
from hashlib import pbkdf2_hmac
import requests


def vulnerable_test_function1():
    filename = tempfile.mktemp() # Noncompliant
    tmp_file = open('testfile.txt', "w+")

def vulnerable_test_function2(password):
    hash = pbkdf2_hmac('sha256', password, b'D8VxSmTZt2E2YV454mkqAY5e', 100000)    # Noncompliant: salt is hardcoded
    hash = crypt.crypt(password)

def vulnerable_test_function3():
    requests.get('https://www.zaproxy.org', verify=False) # Noncompliant

config = configparser.ConfigParser()
config.read('config.conf')
namespace = config["CONF"]["namespace"]
maint = config["CONF"]["maint"]
instances = eval(config["CONF"]["instances"])

password = getpass.getpass()

s = pxssh.pxssh()
#s.logfile = sys.stdout.buffer
s.login(f"{maint}.{namespace}", getpass.getuser(), password)

makedirs(f"{namespace}/{maint}")
print(f"getting data from {maint}.{namespace}")
s.sendline('cat /etc/security/access.conf')
s.prompt(timeout=1)
access_conf = s.before.decode()
s.sendline('sudo cat /etc/sudoers')
s.prompt(timeout=1)
s.expect(':')
s.sendline(password)
s.prompt(timeout=1)
sudoers = s.before.decode()
with open(f"{namespace}/{maint}/access.conf", 'w') as f:
            f.writelines(access_conf)
with open(f"{namespace}/{maint}/sudoers", 'w') as f:
            f.writelines(access_conf)

for instance in instances:
    makedirs(f"{namespace}/{instance}")
    print(f"getting data from {instance + namespace}")
    try:
        print("    making directory")
        # s.sendline(f"mkdir data/{instance}")
        # s.prompt()
        s.sendline(f"ssh {instance}.{namespace} 'cat /etc/security/access.conf'")
        s.prompt(timeout=1)
        i = s.expect(['(yes/no)', 'assword:', '$'])
        if i == 0:
            s.sendline('yes')
            s.expect('assword:')
            s.sendline(password)
            s.prompt(timeout=1)
        elif i == 1:
            s.sendline(password)
            s.prompt(timeout=1)
        elif i == 2:
            continue
        access_conf = s.before.decode()
        with open(f"{namespace}/{instance}/access.conf", 'w') as f:
            f.writelines(access_conf)
        
        s.sendline(f"ssh -t {instance}.{namespace} 'sudo cat /etc/sudoers'")
        s.prompt(timeout=1)
        s.expect('assword:')
        s.sendline(password)
        s.prompt(timeout=1)
        s.expect(":")
        s.sendline(password)
        s.prompt(timeout=1)
        sudoers = s.before.decode()
        with open(f"{namespace}/{instance}/sudoers", 'w') as f:
            f.writelines(sudoers)
    except Exception as e:
        print(e)

