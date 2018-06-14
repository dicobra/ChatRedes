#coding:utf-8
""" Servidor chat versão alpha """

import threading
import time
from socket import *

serverPort = 9119

""" Nomes arquivos """
file_client_logins = "logins.cli"
file_client_on = "onlines.cli"

"""Comandos"""
cmd_truco = "Truco"
cmd_cai = "Cai"

""" Respostas """
rst_ok = "ok"
rst_erro_pw = "erro_pw"
rst_erro_em = "erro_em"
rst_erro = "erro"
rst_sin_ok = "sin_ok"
rst_sin_h = "sin_h"
rst_sin_erro_em = "sin_erro_em"
rst_sin_erro = "sin_erro"

""" Perguntas """
pgt_con = "con"
pgt_sin = "sin"

""" Registro de trucos"""
reg_truco = []
qtd_truco = []

""" Funcionalidade da pergunta con """
def func_pgt_con(mensagem,address):
	print("con recebido")
	if( len( mensagem.split() ) == 3):# verifica se a mensagem recebida tem o numero de parametros adequado
		email = getEmail(mensagem)
		senha = getSenha(mensagem)
		
		if(verificarEmail(email) == -1):
			responder(rst_erro_em,address)
			return
		
		if( not verificarEmailSenha(email,senha) ):	
			responder(rst_erro_pw,address)
			return
			
		posi = verificarOnline(email)
		if(posi == -1):
			conectarCliente(email,address)
		else:
			atualizarListaOn(email,address,posi)
		
		posi = encontrarTrucado(email) 
		if( posi == -1):
			reg_truco.append(email)
			qtd_truco.append(0)
		else:
			qtd_truco[posi] = 0
		
		responder(onsToString(obterListaOn()), address)
	else:
		responder(rst_erro, address)

""" Funcionalidade da pergunta sin """	
def func_pgt_sin(mensagem,address):
	print("sin recebido")
	
	if( len( mensagem.split() ) == 3):# verifica se a mensagem recebida tem o numero de parametros adequado
		email = getEmail(mensagem)
		senha = getSenha(mensagem)
		
		if(verificarEmail(email) == -1): #se não encontrar o email no arquivo o cliente é cadastrado
			salvarLogin(email,senha)
			responder(rst_sin_ok,address)
		else: # se encontrar o email retorna o erro ao cliente
			responder(rst_sin_erro_em,address)
		
	else:
		responder(rst_sin_erro,address)

""" Funcionalidade do comando cai """	
def func_cmd_cai(mensagem,address):
	global qtd_truco
	if( len(mensagem.split()) == 2):
		email = getEmail(mensagem)
		posicao = encontrarTrucado(email)
		if( posicao != -1):
			qtd_truco[posicao] = 0
		print("cai recebido",email)

""" Funcionalidade do comando truco """
def func_cmd_truco():
	print("cmd truco")
	
	global reg_truco
	global qtd_truco
	
	eliminarDesconectados()
	
	lista = obterListaOn()
	
	if(len(lista) <= 0):
		return
	
	for usuario in lista:
		ip = obterIpOnline(usuario)
		email = obterEmailOnline(usuario)
		responder(cmd_truco + " " + onsToString(lista),[ip, serverPort]) #envia um truco para o cliente
		posicao = encontrarTrucado(email) #guarda a posição 
		if( posicao == -1): # se não encontrar na lista de trucado adiciona o registro com 1 ocorrencia de trucado
			reg_truco.append(email)
			qtd_truco.append(1)
		else:	
			qtd_truco[posicao] += 1 # senão soma a qntdade de vezes que foi trucado e não respondeu
		
		print("Trucado:",ip,email,qtd_truco[posicao])
		
	
	

""" Decodifica as mensagens recebidas """
def decodificarMsg(mensagem,address):
	if(mensagem[:3] == pgt_con):
		return func_pgt_con(mensagem,address)
		
	if (mensagem[:3] == pgt_sin):
		return func_pgt_sin(mensagem,address)
		
	if (mensagem[:3] == cmd_cai):
		return func_cmd_cai(mensagem,address)
		
""" Loop para receber mensagens """
def loopReceber():
	while True:
		serverSocket = socket(AF_INET, SOCK_DGRAM)
		serverSocket.bind(('', serverPort))
		message, clientAddress = serverSocket.recvfrom(2048)
		if(message != ""):
			thExecutora = threading.Thread(target=decodificarMsg, args=(message,clientAddress))
			thExecutora.start()
		
		serverSocket.close()

""" Responder uma mensagem a um endereço """
def responder(mensagem, address):
	try:
		clientSocket = socket(AF_INET, SOCK_DGRAM)
		clientSocket.sendto(mensagem, (address[0],serverPort))
		clientSocket.close()
	except Exception:
		print("ClienteNaoEncontrado")
		
	




""" utils """

""" a partir de um comando retira a segunda posicao de um split()"""
def getEmail(mensagem):
	email = mensagem.split()[1]
	return email

""" a partir de um comando retira a terceira posicao de um split() """	
def getSenha(mensagem):
	senha = mensagem.split()[2]
	return senha
	
""" obtém o ip dp usuario a partir de uma linha 'email:ip'"""	
def obterIpOnline(usuario):
	ip = usuario[usuario.find(':') + 1:-1]
	return ip
	
""" obtem o email a partir de uma linha 'email:ip'"""	
def obterEmailOnline(usuario):
	email = usuario[:usuario.find(':')]
	return email

"""verifica se esse email ja esta cadastrado no arquivo de login"""
def verificarEmail(email):
	clientes = lerArquivoLogins()
	
	i = 0
	for cliente in clientes:
		emailC = cliente[:cliente.find(':')]
		if( emailC == email ):
			return i
		i += 1
	
	return -1

""" Verifica se o email corresponde com a senha guardada no arquivo de logins """
def verificarEmailSenha(email,senha):
	posi = verificarEmail(email)
	if( posi == -1 ):
		return False
	
	cliente = lerArquivoLogins()[posi]
	login = email + ":" + senha + "\n"
	
	if(cliente != login):
		return False
		
	return True
	
"""Verifica se o cliente esta cadastrado na lista de trucados, se sim retorna qual é a posição da coluna da matriz, caso contrario retorna -1"""
def encontrarTrucado(email):
	global reg_truco
	i = 0
	for reg in reg_truco:
		if(email == reg):
			return i
		i += 1
	return -1
	

""" Verifica se o cliente está online, se está retorna a poisção que ele se encontra no arquivo """
def verificarOnline(email):
	clientes = obterListaOn()

	i = 0
	for cliente in clientes:
		emailC = cliente[:cliente.find(':')]
		if( emailC == email ):
			return i
		i += 1
	
	return -1

""" Converte a lista de onlines em apenas uma string com os clientes separados por '#' """
def onsToString(listOn):
	ons = ""
	for on in listOn:
		ons += on
	
	ons = ons.replace('\n','#')
		
	return ons





""" Arquivos """

"""adciona ao fim do arquivo de logins o mail e a senha """
def salvarLogin(email, senha):
	try:
		arqCliente = open(file_client_logins,"a")
	except IOError:
		arqCliente = open(file_client_logins,"w")
	
	client = email
	client += ":"
	client += senha
	client += "\n"
	
	arqCliente.write(client)
	
	arqCliente.close()

""" retorna o conteudo do arquivo de clientes login como um array de strings """
def lerArquivoLogins():
	try:
		arqCliente = open(file_client_logins,"r")
	except:
		return []
	
	lines = arqCliente.readlines()
	
	arqCliente.close()
	
	return lines
	
""" adciona o cliente ao arquivo de clientes online """	
def conectarCliente(email,address):
	try:
		arqOn = open(file_client_on,"a")
	except IOError:
		arqOn = open(file_client_on,"w")
	
	clientOn = email
	clientOn += ":"
	clientOn += address[0]
	clientOn += "\n"
	
	arqOn.write( clientOn )
	
	arqOn.close()
	
	return True;

""" retorna o conteudo do arquivo de clientes online como um array de strings """	
def obterListaOn():
	try:
		arqOn = open(file_client_on,"r")
	except IOError:
		return []
	
	lines = arqOn.readlines()
	
	arqOn.close()
	
	return lines	

""" atualiza o ip e o email na posição do arquivo de clientes online """
def atualizarListaOn(email, address, posi):
	listaOn = obterListaOn()
	listaOn[posi] = email + ":" + address[0] + "\n"
	
	arqOn = open(file_client_on,"w")
		
	arqOn.writelines(listaOn)
	
	arqOn.close()

"""Elimina do arquivo de clientes onlines e da lista de trucados os usuarios que foram trucados mias de 3x"""
def eliminarDesconectados():
	global reg_truco
	global qtd_truco
	
	lista_onlines = obterListaOn()
	
	if(len(lista_onlines) <= 0):
		return

	clientes_online = ""
	new_reg_truco = []
	new_qtd_truco = []
	i = 0 
	for reg in reg_truco:
		if( qtd_truco[i] < 3 ):
			pos = verificarOnline(reg_truco[i])
			clientes_online += lista_onlines[pos]
			new_reg_truco.append(reg_truco[i])
			new_qtd_truco.append(qtd_truco[i])
		else:
			print("Desconectado",reg_truco[i])
		i+=1
		 
	arquivo = open(file_client_on, "w")
	arquivo.write(clientes_online)
	arquivo.close()
	reg_truco = new_reg_truco
	qtd_truco = new_qtd_truco	




def func_thread_trucar():
	while True:
		func_cmd_truco()
		time.sleep(3)

""" Inicio do Servidor """		
def main():
	thReceber = threading.Thread(target=loopReceber, args=())
	thReceber.start()
	
	thTrucar = threading.Thread(target=func_thread_trucar,args=())
	thTrucar.start()
	
if __name__ == '__main__':
	main()

	
