#coding: utf-8

from Tkinter import *
from Info import *
from mensagens import *

import threading

class JUsuarios:
	
	def __init__(self,root, listUsers):
		self.myRoot = root
		self.frame1 = Frame(root)
		self.frame1.pack(side=TOP)
		
		self.frame = Frame(self.frame1)
		self.frame.pack(side=BOTTOM)
		
		self.lblListaUser = Label(self.frame1,text="Lista de usuarios:")
		self.lblListaUser.pack()

		self.listaBotoes = []
		self.listaUsuarios = []
		self.dicTelas = {}
		
		for user in listUsers.split("#"):
			if(user != ""):
				self.adicionar_botao(user)
				self.listaUsuarios.append(user)
		
		self.thReceber = threading.Thread(target=self.loop_receber,args=())
		self.thReceber.start()
		
		root.geometry("200x300+200+200")
		root.mainloop()
		
	def adicionar_botao(self,user):
		novoBotao = Button(self.frame,text=user.split(":")[0])
		self.listaBotoes.append(novoBotao)
		btn = self.listaBotoes[self.listaBotoes.index(novoBotao)]
		btn["command"] = lambda:self.acao_botao(btn)
		novoBotao.pack()
		
	def criarJanelaM(self,email,mensagem):
		if(not self.dicTelas.has_key(email)):
			novaJanela = Tk()
			novaJM = JMensagens(novaJanela,email,self)
			self.dicTelas[email] = novaJM
			print(self.dicTelas)
			self.dicTelas[email].receber_mensagem(mensagem)
			novaJM.start()
		
	def remover_offlines(self,novaLista):
		j = 0
		for user in self.listaUsuarios:
			if(user != ""):
				user = self.listaUsuarios[j]
				btn  = self.listaBotoes[j]
				print("Verificando off",user,btn["text"])
				if( not find_in_list(novaLista,user) ):
					print("Usuario desconectado",user,btn)
					email = btn["text"]
					if(self.dicTelas.has_key(email)):
						self.dicTelas[email].receber_mensagem("DESCONECTADO")
						self.dicTelas[email].state_btnEnviar(False)
					self.listaUsuarios.remove(user)
					btn.destroy()
					self.listaBotoes.remove(btn)
					j-=1
				j+=1
				
	def retirar_tela(self,email):
		del self.dicTelas[email]
	
	def adicionar_novos_onlines(self,novaLista):
		for user in novaLista:
			if(user != ""):
				print("Verificando on",user)
				if( not find_in_list(self.listaUsuarios,user) ):
					print("Usuario conectado",user)
					email = user.split(":")[0]
					if(self.dicTelas.has_key(email)):
						self.dicTelas[email].receber_mensagem("CONECTADO")
						self.dicTelas[email].state_btnEnviar(True)
					self.listaUsuarios.append(user)
					self.adicionar_botao(user)
	
	def acao_botao(self, button):
		self.criarJanelaM(button["text"],"")
		
	def loop_receber(self):
		while True:
			print("guiRecebendoTudo")
			mensagem, endereco = receber_mensagem(Info.serverPort)
			self.decodificar(mensagem,endereco)
			
	def decodificar(self,mensagem,endereco):
		if(len(mensagem.split()) >= 2):
			comando = mensagem.split()[0]
			
			if(comando == Info.comando_truco):
				self.func_cair()
				self.remover_offlines(mensagem.split()[1].split("#"))
				self.adicionar_novos_onlines(mensagem.split()[1].split("#"))
			if(comando == Info.comando_envia):
				dest = mensagem.split()[1]
				rem = mensagem.split()[2]
				if( dest != Info.meuEmail ):
					return
				if( self.dicTelas.has_key(rem) ):
					self.dicTelas[rem].receber_mensagem(mensagem.split('#m#')[1])
				else:
					self.criarJanelaM(rem,mensagem.split('#m#')[1])
				
				
	def func_cair(self):
		comando = Info.comando_cai + " " + Info.meuEmail
		send_toServer(comando)
		print(comando)
		
	def func_enviar_mensagem(self,mensagem,email):
		for user in self.listaUsuarios:
			emailU = user.split(":")[0]
			if(emailU == email):
				msg = Info.comando_envia + " " + email + " " +Info.meuEmail + " #m#" + mensagem
				send_to(msg,user.split(":")[1])

		
		
