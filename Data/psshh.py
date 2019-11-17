from __future__ import print_function
from pprint import pprint
from pssh.clients.native import ParallelSSHClient
import random
import getpass
import time
import os


hosts = []

for i in range(10):
	hostname = 'brki164-lnx-' + str(i) + '.bucknell.edu'
	response = os.system("ping -c 1 " + hostname)

	#and then check the response...
	if response == 0:
		hosts.append(hostname)

print(hosts)
passw = getpass.getpass(prompt="George Password")

client = ParallelSSHClient(hosts, user ='gbm006', password =passw)
#print(client.hosts[0])

folder_name = input("folder name")
#client.run_command('cd Downloads/')
output = client.run_command('cd Patrik/Data/ && python distributive_scraper.py ' + str(len(hosts)) + ' ' +  folder_name, use_pty='Fasle')

for host in hosts:
	for line in output[host].stdout:
		print(line)

for host in output:
	print(output[host].exit_code)
