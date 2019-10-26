from __future__ import print_function
from pprint import pprint
from pssh.clients.native import ParallelSSHClient
import random
import getpass
import time

hosts =['brki164-lnx-5.bucknell.edu','brki164-lnx-6.bucknell.edu','brki164-lnx-7.bucknell.edu','brki164-lnx-8.bucknell.edu','brki164-lnx-9.bucknell.edu','brki164-lnx-10.bucknell.edu','brki164-lnx-11.bucknell.edu','brki164-lnx-12.bucknell.edu','brki164-lnx-13.bucknell.edu','brki164-lnx-14.bucknell.edu','brki164-lnx-15.bucknell.edu','brki164-lnx-16.bucknell.edu','brki164-lnx-17.bucknell.edu','brki164-lnx-18.bucknell.edu']



passw = getpass.getpass(prompt="George Password")

client = ParallelSSHClient(hosts, user ='gbm006', password =passw)
#print(client.hosts[0])


#client.run_command('cd Downloads/')
output = client.run_command('cd Code/NLP/Soup/Not_Slim/ && python distributive_scraper.py ' + str(len(hosts)), use_pty='Fasle')

for host in hosts:
	for line in output[host].stdout:
		print(line)

for host in output:
	print(output[host].exit_code)
