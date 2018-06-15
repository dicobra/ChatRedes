#coding: utf-8

from Tkinter import *
from Info import *
from usuarios_online import *

class JLogin:
	
	def __init__(self,root):
		self.myRoot = root
		self.frame  = Frame(root)
		self.frame.grid()
		
		#titulo interno "Login/Signin"
		self.lblTitulo = Label(self.frame,text="Login/Signin")
		self.lblTitulo.grid(row=0,column=0,columnspan=2)
		
		#label email
		self.lblEmail = Label(self.frame,text="email:")
		self.lblEmail.grid(row=1,column=0)
		
		self.entradaEmail = Entry(self.frame)
		self.entradaEmail.grid(row=1,column=1)
		
		self.lblSenha = Label(self.frame,text="senha:")
		self.lblSenha.grid(row=2,column=0)
		
		self.entradaSenha = Entry(self.frame,show = "*")
		self.entradaSenha.grid(row=2,column=1)
		
		self.btnSign = Button(self.frame,text="Signin",command=self.acao_btnSign)
		self.btnSign.grid(row=3,column=1,sticky=W)
		
		self.btnLogn = Button(self.frame,text="Login",command=self.acao_btnLogn)
		self.btnLogn.grid(row=3,column=1,sticky=E)
		
		self.lblResultado = Label(self.frame,text="")
		self.lblResultado.grid(row=4,column=0,columnspan=2)
		
		root.mainloop()
		
	def acao_btnLogn(self):
		print("Botao login pressionado")
		
		comando = Info.comando_login + " " + self.entradaEmail.get() + " " + self.entradaSenha.get()
		
		send_toServer(comando)
		mensagem,endereco = receber_mensagem(Info.serverPort)	
		
		if(mensagem == Info.erro_em):
			self.lblResultado["text"] = "Email não cadastrado"
			return
			
		if(mensagem == Info.erro_pw):
			self.lblResultado["text"] = "Senha incorreta"
			return
		
		if(mensagem == Info.erro):
			self.lblResultado["text"] = "Erro do servidor"
			return
			
		self.lblResultado["text"] = "Login efetuado"
		Info.meuEmail = self.entradaEmail.get()

		print(mensagem,endereco,Info.meuEmail)

		self.myRoot.destroy()
		novaJanela = Tk()
		JUsuarios(novaJanela,mensagem)
		
		
	def acao_btnSign(self):
		print("Botao signin pressionado")
		
		comando = Info.comando_signin + " " + self.entradaEmail.get() + " " + self.entradaSenha.get()
		
		send_toServer(comando)
		mensagem,endereco = receber_mensagem(Info.serverPort)
		
		print(mensagem,endereco)	
		
		if(mensagem == Info.sin_erro_em):
			self.lblResultado["text"] = "Email já cadastrado"
			return
			
		if(mensagem == Info.sin_erro):
			self.lblResultado["text"] = "Erro do servidor"
			return
			
		self.lblResultado["text"] = "Usuário cadastrado"
		
		
janela = Tk()

JLogin(janela)
