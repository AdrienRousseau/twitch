from urllib.request import urlopen
import urllib.request
from urllib.error import URLError
import urllib.parse
from threading import Timer
import os
import time
import json
import sys
import subprocess
import datetime
import cfg
import signal
 

users = ["nl_kripp","itshafu","kolento","thijshs","amazhs","trumpsc","day9tv","hotform"]

process_list = []

def main():
	for u in users:
		process_list.append(subprocess.Popen(["python3","checking_alive.py",u], preexec_fn=os.setsid))
		print ("Checking alive : " + u)

if __name__ == "__main__":
	# execute only if run as a script
	main()
	while True:
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			for p in process_list:
				os.killpg(os.getpgid(p.pid), signal.SIGTERM)
