#coding:utf-8

from socket import *

class Info:
	meuEmail = ''
	serverIp = '192.168.11.12'
	serverPort = 9119
	
	comando_login = "con"
	comando_signin = "sin"
	
	comando_truco = "Truco"
	comando_cai = "Cai"
	comando_envia = "Envia"
	
	""" Respostas """
	erro_pw = "erro_pw"
	erro_em = "erro_em"
	erro = "erro"
	sin_ok = "sin_ok"
	sin_erro_em = "sin_erro_em"
	sin_erro = "sin_erro"
	
def send_toServer(mensagem):		
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	clientSocket.sendto(mensagem, (Info.serverIp, Info.serverPort))
	clientSocket.close()
	
def receber_mensagem(port):
	serverSocket = socket(AF_INET, SOCK_DGRAM)
	serverSocket.bind(('', Info.serverPort))
	message, clientAddress = serverSocket.recvfrom(2048)
	serverSocket.close()
	
	return message, clientAddress
	
def send_to(mensagem,ip):
	clientSocket = socket(AF_INET, SOCK_DGRAM)
	clientSocket.sendto(mensagem, (ip, Info.serverPort))
	clientSocket.close()

def find_in_list(lista,chave):
	for l in lista:
		if(chave == l):
			return True
	return False
