import os.path
from os import path
import time
import random
import sys





#print(len(sys.argv))
if not(len(sys.argv) == 2):
        print("i need how many computers are you using")
        exit()

num_pcs = int(sys.argv[1])
#gonna pull a sneky acet116-lnx-1.bucknell.edu
myhostnum = int(os.uname()[1].split('-')[2].split('.')[0]) % num_pcs #possibly % num machines i will use machines 1 to 9 so im not worried
print(myhostnum)
delay = random.uniform(10,20) #sleep for 10 to 20 seconds to avoid ipban? it knows that something is pinging it in underseonds
print('time delay = ' + str(delay))
#print('urls remaining: ' + str(num_lines)) 
time.sleep(delay)


