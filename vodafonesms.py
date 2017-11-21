#!/usr/bin/env python
# # Dependencies : mechanize
# Simple script to send sms via vodafone web2sms service 
#
# Author: Dimitris M
# Published under the GPL v3 
#
# Requires VODAFONE.gr registration!! (https://www.vodafone.gr/portal/client/idm/showRegisterPrePay.action?null)

import re
import mechanize
from getpass import getpass
import sys,signal
from sys import argv, exit
import getopt
import time
from datetime import date
import datetime



#use utf-8
reload(sys)
sys.setdefaultencoding("utf-8")



vodafone = mechanize.Browser(
	 factory=mechanize.DefaultFactory(i_want_broken_xhtml_support=True)
	 )



def login(user,password):
	# Ignore robots.txt.Do not do this without thought and consideration.
	vodafone.set_handle_robots(False)
	vodafone.open("https://www.vodafone.gr/portal/client/idm/loginForm.action?null")
	vodafone.select_form(name="loginform")
	vodafone["username"] = user
	vodafone["password"] = password
	print ("\nLogging in...")
	vodafone.submit()

def sendsms(number,message):
	vodafone.addheaders = [("User-agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)")]
	response1=vodafone.open("http://tools.vodafone.gr/gr/cgi-bin/office.pl?serv=web2sms#http://www.vodafone.gr/portal/client/cms/viewCmsPage.action?pageId=61&menuId=11966")
	response1.seek(0)

		
	try:
		vodafone.select_form(name="thisform")
	except:
		print ("An Error occured. Probably Wrong Username/Password")
		sys.exit(1)

	vodafone["ad_target"] = number
	vodafone["message"] = message.encode('iso-8859-7')
	exceeded = len( vodafone["message"] ) - (640)
	print ("Submiting Request...")
	if exceeded > 0 :
		print ("\nYou exceeded the available characters by %d\n SENDING:" % (exceeded))
		vodafone["txtMessage"] = vodafone["message"][:-exceeded]
		print (vodafone["message"])
                #sys.exit(exceeded)

	#Do not just submit...press the btnSend to submit
	result = vodafone.submit("a_send")
	#print result.read()
	m = "From:"
	if str.find(result.read(), m) != -1:
                text_file = open("/home/mitsos/sms.txt", "a")
                #date.fromtimestamp(time.time())
                #datetime.datetime.utcnow()
                text_file.write("Time:"+str(datetime.datetime.utcnow())+" Number:"+number+" message:"+message+"\n")
                text_file.close()

		print ("Message Sent")
		sys.exit(0)
	else:
                print ("WARNING *** SMS Sending problem *** WARNING")
                print (result.read())
		#sys.exit(2)

def help():
	print ("\nUsage %s <username> <password> <number> <sms>" % (sys.argv[0]))
	print ("or use the interactive interface.")



if __name__ == '__main__' :
	
	def handler(*args):
		print ("\n\nBye Bye!")
		sys.exit(0)


	signal.signal(signal.SIGINT,handler)

	if len(sys.argv) == 1 :
		user = raw_input("Username: ")
		passwd = getpass()
		login(user,passwd)
		
		number = raw_input("Phone Number : ")
		msg = raw_input("SMS Message : ")
		sendsms(number,msg)
	else :
		if len(sys.argv)==2 and (sys.argv[1] in ["-h","--help"]):
			help()
			sys.exit(3)
		elif len(sys.argv) != 9 :
			print ("\nWrong Number of Parameters.")
			help()
			sys.exit(3)
		else :
			count = 0
			try:
				opts, args = getopt.getopt(argv[1:], 'u:p:t:m:')
			except  getopt.GetoptError, msg:
				stderr.write(argv[0] + ': ' + str(msg) + "\n")
				exit(3)

			for c, optarg in opts:
				if c == '-u':
					user = optarg
					count = count + 1
				if c == '-p':
					passwd = optarg
					count = count + 1
				if c == '-t':
					number = optarg
					count = count + 1
				if c == '-m':
					msg = optarg
					#msg = optarg.decode('utf-8')
					count = count + 1
			if count <4:
				print ("Wrong parameters.")
				print ("-u user -p passwd -r number -m msg")
				sys.exit(3)
			else:
				#user = sys.arg[0]
				#passwd = sys.arg[1]
				#number = sys.arg[2]
				#msg = sys.arg[3].encode('utf8')
				#print msg				
				login(user,passwd)
				sendsms(number,msg)

