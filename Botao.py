#coding: utf-8

from Tkinter import *
from Info import *
from usuarios_online import *

class Botao:
	
	def __init__(self,frame):
		self.botao = Button(JUsuarios.frame,text=user.split(":")[0],command=lambda:self.acao_botao(self.botao))
		self.botao.pack()
		
	def acao_botao(self, button):
		print("btn clicado",button["text"])

