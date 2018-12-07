# -*- coding: utf-8 -*-

import socket
import random
import json
import csv
import hashlib
from Crypto.Cipher import AES
import base64
#coneção ao servidor por tcp
def connect_tcp():
	tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_s.bind( ("0.0.0.0", 0))	

	tcp_s.connect( ("xcoa.av.it.pt", 8080) )
	return tcp_s
   
#obtenção da chave comum
def get_key(server):
	
	p = 1343270965545476954223465975446
	g = 46756894379
	a = (int)(random.random()*10)
    
	
	server.send(("CONNECT " + str(pow(g,a,p)) + "," +str(p) + "," + str(g) +"\n").encode("utf-8"))
	

	data = server.recv(4098)
	data = data.decode("utf-8")
	data = json.loads(data)
	token = data["TOKEN"]
	
	b = data["B"]
	X = pow(b,a,p)
	X = str(X).encode("utf-8")
	MD5 = hashlib.md5()
	MD5.update(X)
	X = MD5.hexdigest()
	X = X[0:16]
	
	return X, token

#codificação dos dados
def encode_data(data, key):
	cipher = AES.new(key)
	

	lastBlockLen = len(data) % cipher.block_size
	if (lastBlockLen != cipher.block_size):
		p = cipher.block_size - len(data)
		data = data + chr(p)*p

	data = cipher.encrypt(data)
	data = base64.b64encode(data)+"\n".encode("utf-8")
	return data


#receber e descodificar os dados
def get_data(server, key):
	cipher = AES.new(key)
	
	data = server.recv(4096)
	data = base64.b64decode(data)
	data = cipher.decrypt(data)
	p = data[len(data)-1]
	data = data[0:len(data)-p]
	return data
	
#escrever no ficheiro csv
def write_to_csv(writer, data):
    writer.writerow(data)

#criar o ficheiro csv
def create_csv(name):
	fout = open(name, 'w')
	writer = csv.DictWriter(fout, fieldnames=['WIND', 'HUMIDITY', 'TEMPERATURE'])
	writer.writeheader()
	return writer


    
    
def write_to_temp(data):
	fout = open("src/temp.csv", 'w')
	writer = csv.DictWriter(fout, fieldnames=['WIND', 'HUMIDITY', 'TEMPERATURE'])
	writer.writeheader()
	writer.writerow(data)
	fout.close()
   
#imprimir mensagem para o utilizador
def write_msg(wind, humi, temp):
	if(humi < 80 and temp > 10 and wind < 30):
		print("Está bom tempo")
	else:
		print("O tempo não está muito bom")
		if(humi >= 80):
			print("Levar Guarda-Chuva")
		if(temp <= 10 or wind >= 30):
			print("Levar Casaco")
		
		
#inicializar o programa
def initialize():
	print("Aplicação de monitorização do clima\n\n")
	
	print("A ligar ao servidor...\n")
	server = connect_tcp()
	print("Ligado.\n")
	print("A obter chave de encriptação...\n")
	X, token = get_key(server)
	print("Chave obtida com sucesso\n")

	print("A pedir os dados ao servidor...\n")
	data = ("READ " + str(token))

	data = encode_data(data, X)
	server.send(data)


	writer = create_csv("data.csv")
	
	#get ok from server
	data = get_data(server, X).decode("utf-8")
	print("Servidor OK\n")
	print("Ctrl + c para terminar o programa\n\n")
	
	return (server, writer, X)
			
		
def main():
	
	X = None
		
	while (X == None):	
		try:
			server, writer, X = initialize()
		except socket.gaierror:
			print("Não foi possivel ligar ao servidor")
			exit(0)
		except:
			print("Ocureu um erro, o programa vai reiniciar\n\n\n")
	
	#get data
	while 1:
		try:
			data = json.loads(get_data(server, X).decode("utf-8"))
			write_to_csv(writer, data)
			write_to_temp(data)
			print("\n\nVento: " + str(data["WIND"]))
			print("Humidade: " + str(data["HUMIDITY"]))
			print("Temperatura: " + str(data["TEMPERATURE"]) + "\n")
			write_msg(data['WIND'], data['HUMIDITY'], data['TEMPERATURE'])
		except KeyboardInterrupt:
			exit()
		except:
			pass
		
main()




