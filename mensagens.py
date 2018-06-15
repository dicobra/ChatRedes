#coding: utf-8

from Tkinter import *
from Info import *

class JMensagens:
	
	def __init__(self,root,email,pai):
		self.myRoot = root
		self.email = email
		self.meuPai = pai
		
		self.frame = Frame(root)
		self.frame.grid()
		
		self.lblListaUser = Label(self.frame,text="Conversa com: "+self.email)
		self.lblListaUser.grid(row=0,column=0,columnspan=3)
		
		self.textArea = Text(self.frame)
		self.textArea.grid(row=1,column=0,columnspan=2)
		self.textArea["state"] = DISABLED
		
		self.scrollBar = Scrollbar(self.frame)
		self.scrollBar.grid(row=1,column=2,sticky=N+S)
		
		self.scrollBar.config(command=self.textArea.yview)
		self.textArea.config(yscrollcommand=self.scrollBar.set)
		
		self.entrada = Entry(self.frame)
		self.entrada.grid(row=2,column=0,columnspan=2,sticky=W+E)
		
		self.btnEnviar = Button(self.frame,text="Enviar",command=self.acao_btnEnviar)
		self.btnEnviar.grid(row=2,column=1,sticky=E)
		
		self.myRoot.protocol("WM_DELETE_WINDOW", lambda:self.on_closing())
		
	def start(self):
		self.myRoot.mainloop()
		
	def on_closing(self):
		print("Estou indo embora")
		self.meuPai.retirar_tela(self.email)
		self.myRoot.destroy()

	def acao_btnEnviar(self):
		mensagem = self.entrada.get()
		if( mensagem != ""):
			self.textArea["state"] = NORMAL
			self.textArea.insert(END,"Você>> "+mensagem+"\n")
			self.textArea["state"] = DISABLED
			self.entrada.delete(0,END)
			self.meuPai.func_enviar_mensagem(mensagem,self.email)
	
	def receber_mensagem(self,mensagem):
		if(mensagem == ""):
			return
		self.textArea["state"] = NORMAL
		self.textArea.insert(END,self.email+"<< "+mensagem+"\n")
		self.textArea["state"] = DISABLED
		
	def state_btnEnviar(self,enabled):
		if(enabled):
			self.btnEnviar["state"] = NORMAL
		else:
			self.btnEnviar["state"] = DISABLED
