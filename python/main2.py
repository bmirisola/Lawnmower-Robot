import inkey	#for getch() and inkey() functions
import time
import sys, termios, atexit
import roboclaw

TimeOut=.1
DriveState=-1
address = 0x80
speed = 127

def Forward():
	global DriveState
	if(DriveState<>1):
		#print "Forwards"
		roboclaw.BackwardM1 (address, speed)
		roboclaw.ForwardM2 (address, speed)
		DriveState=1
		global TimeOut
		TimeOut=.6
	else:
		TimeOut=.1


def Backward():
	global DriveState
	if(DriveState<>2):
		#print "Backwards"
		roboclaw.ForwardM1 (address, speed)
		roboclaw.BackwardM2 (address, speed)
		DriveState=2
		global TimeOut
		TimeOut=.6
	else:
		TimeOut=.1

def Jog_Left():
	global DriveState
	if(DriveState<>3):
		#print "Jog Left"
		roboclaw.ForwardM2 (address, speed)		
		DriveState=3
		global TimeOut
		TimeOut=.6
	else:
		Timeout=.1

def Jog_Right():
	global DriveState
	if(DriveState<>4):
		#print "Jog Right"
		roboclaw.BackwardM1 (address, speed)
		DriveState=4
		global TimeOut
		TimeOut=.6
	else:
		Timeout=.1

def Jog_Auton():
	global DriveState
	if(DriveState<>5):
		roboclaw.BackwardM1 (address, speed)
		roboclaw.ForwardM2 (address, speed)
		DriveState=5
		global TimeOut
		TimeOut=10
	else:
		TimeOut=.1
	
		
def Stop():
	global DriveState
	if(DriveState<>0):
		roboclaw.ForwardM1(address, 0)
		roboclaw.ForwardM2(address, 0)
		print "Stop"
		DriveState=0

#Linux comport name
roboclaw.Open("/dev/ttyACM0",115200)
atexit.register(inkey.set_normal_term)
inkey.set_curses_term()
LastCmdTime=time.time()
Stop()
while 1:
	if inkey.kbhit():
		c = inkey.getch()
		LastCmdTime=time.time()
		#if (ord(c[0])==27) or (c=="["):
		#	continue
		if (c.lower()=="w") or (c.lower()=="l"):
			Forward()
		elif (c.lower()=="a") or (c.lower()=="p"):
			Jog_Left()
		elif (c.lower()=="d") or (c.lower()=="m"):
			Jog_Right()
		elif (c.lower()=="s") or (c.lower()=="n"):
			Backward()
		elif(c.lower() =="b"):
			Jog_Auton()
		elif (c.lower()== " "):
			Stop()
		elif (c.lower()=="q"):
			Stop()
			print "Quit"
			break
		else:
			print "I got ",c,"(",ord(c),")"
			print "W = Forward"
			print "A = Left"
			print "S = Backward"
			print "D = Right"
			print "Spacebar = Stop"
			print "Q = Quit"
	else:
		if(time.time()-LastCmdTime>TimeOut):
			Stop()
	#time.sleep(.2)
	#sys.stdout.write('.')

print 'done'

