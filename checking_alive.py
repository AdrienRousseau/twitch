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
 
def check_user(user):
	""" returns 0: online, 1: offline, 2: not found, 3: error """
	global info
	url = 'https://api.twitch.tv/kraken/streams/' + user
	request = urllib.request.Request(url, headers={"Client-ID" : cfg.CLIENTID})
	try:
		info = json.loads(urlopen(request).read().decode('utf-8'))
		if info['stream'] == None:
			status = 1
		else:
			status = 0
	except URLError as e:
		if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
			status = 2
		else:
			status = 3
	return status

def get_game_viewers(user):
	global info
	url = 'https://api.twitch.tv/kraken/streams/' + user
	request = urllib.request.Request(url, headers={"Client-ID" : cfg.CLIENTID})
	try:
		info = json.loads(urlopen(request).read().decode('utf-8'))
		if info['stream'] == None:
			return None, None
		else:
			return info['stream']['game'],info['stream']['viewers']
	except URLError as e:
		if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
			return None, None
		else:
			return None, None


def loopcheck():
	while True:
		status = check_user(user)
		if status == 2:
			print("username not found. invalid username?")
		elif status == 3:
			print(datetime.datetime.now().strftime("%Hh%Mm%Ss")," ","unexpected error. will try again in 5 minutes.")
			time.sleep(300)
		elif status == 1:
			print(user,"currently offline, checking again in",refresh,"seconds")
			time.sleep(refresh) # 30 seconds
		elif status == 0:
			print(user,"online. stop.")
			subprocess.call(["python3","capture_chat.py",user])
			print("Stream is done. Going back to checking..")
			time.sleep(15)
 
def main():
	global refresh
	global user
	global quality
	global directory
	global post_args
	refresh = 30.0
	user = sys.argv[1]
	client = False


	if(refresh<15):
		print("Check interval should not be lower than 15 seconds")
		refresh=15

	print("Checking for",user,"every",refresh,"seconds.")
	loopcheck()

if __name__ == "__main__":
	# execute only if run as a script
	main()