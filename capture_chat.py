
def chat(sock, msg):
	"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
	"""
	print "Trying to send"
	sock.send("PRIVMSG #{} :{} \r\n".format(chan, msg))
	print "PRIVMSG #{} :{}".format(chan, msg)
#chat(s,"FeelsGoodMan")

import cfg
import socket
import re
import time
import datetime
import math
import sys 
import checking_alive as ca
global chan

RATE = (20/30) # messages per second

#chan = cfg.CHAN
chan = sys.argv[1]

def connect_socket():
	s = socket.socket()
	s.connect((cfg.HOST, cfg.PORT))
	s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
	s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
	s.send("JOIN #{}\r\n".format(chan).encode("utf-8"))
	return s

s =connect_socket()

CHAT_MSG=re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")


#Creating the file name
now = datetime.datetime.now()
stamp = [str(x) for x in [now.day,now.month,now.hour,now.minute]]
file_name =chan + '_' + "_".join(stamp)
file_name = "data/" + file_name

#Preparing the identifier to parse the message
id2 = "PRIVMSG #"+chan +" :"

time_last_msg = time.time()

with open(file_name+".csv",'w') as f, open(file_name+'_error' +".csv",'w') as fe:
	while True:
		response = s.recv(4096).decode("utf-8")
		if response == "PING :tmi.twitch.tv\r\n":
			s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
		else:
			if response == None:
				pass
			else:
				for line in [ x for x in response.split('\n') if x != '']:
					try:
						username = line[1:line.index('!')]
						message = line[line.index(id2)+len(id2):]
						if username !='idenoca' and username != 'tmi':
							f.write(username+";"+str(int(math.floor(time.time()))) + ";" + message)
						print(chan + " " + username + ": " + message)
						for pattern in cfg.PATT:
							if re.match(pattern, message):
								#print "LUL"
								break
						time_last_msg = time.time()
					except:
						print "Error" + line
						fe.write(str(math.floor(time.time())).encode("utf-8") + ";" + line.encode("utf-8") + '\n')
						pass
		time.sleep(0.05)
		if time.time() - time_last_msg >=120:
			""" returns 0: online, 1: offline, 2: not found, 3: error """
			status = ca.check_user(chan)
			#Count again
			if status == 0:
				time_last_msg = time.time()
			else:
				print("Stream Over")
				break
		#no more messages
