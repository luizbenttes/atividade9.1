import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter.messagebox import showinfo
import pandas as pd
from PIL import ImageTk
import gc

APP_TITLE = "SIMTON"
APP_XPOS = 300
APP_YPOS = 50
APP_WIDTH = 800
APP_HEIGHT = 600

IMAGE_PATH = "images/"


class Aresta(object):
	def __init__(self, canvas, comprimento, lista, No1, No2, valorLambda):
		self.comprimento = comprimento
		self.No1 = No1
		self.No2 = No2
		self.valorLambda = valorLambda
		self.canvas = canvas
		self.lista = lista
		self.message = tk.StringVar()
		self.message.set(self.comprimento)
		self.on = True

		self.posicaoAresta = self.lista[self.No1].posicaoAtual + self.lista[self.No2].posicaoAtual
		self.aresta = self.canvas.create_line(self.posicaoAresta, width=3)

		self.widget = tk.Button(self.canvas, text=self.message.get(), 
			fg='white', bg='black',command =self.configura_Aresta)
		self.widget.pack()
		#canvas.tag_bind(self.aresta, '<Double-Button-1>', self.configura_Aresta)
		x = (self.lista[No1].posicaoAtual[0] + self.lista[No2].posicaoAtual[0]) / 2
		y = (self.lista[No1].posicaoAtual[1] + self.lista[No2].posicaoAtual[1]) / 2
		canvas.create_window(x, y, window=self.widget)

	def deleta_Aresta_2(self):
		self.on = False
		self.canvas.delete(self.aresta)
		self.widget.destroy()

	def deleta_Aresta(self):
		self.on = False
		self.canvas.delete(self.aresta)
		self.widget.destroy()
		self.win.destroy()

	def configura_Aresta(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Aresta: "+str(self.lista[self.No1].nome_No+"->"+self.lista[self.No2].nome_No))
		self.win.iconbitmap(r'images\favicon.ico')
		self.win.geometry("%dx%d%+d%+d" % (280, 150, 100, 200))

		l = tk.Label(self.win, text="Distância: ")
		l.place(relx=0.25, rely=0.2, anchor="c")

		self.distancia = tk.Entry(self.win)
		self.distancia.insert(10, self.comprimento)
		self.distancia.place(relx=0.7, rely=0.2, anchor="c")

		l2 = tk.Label(self.win, text="Lambda: ")
		l2.place(relx=0.25, rely=0.4, anchor="c")

		self.valorLamb = tk.Entry(self.win)
		self.valorLamb.insert(10,self.valorLambda)
		self.valorLamb.place(relx=0.7, rely=0.4, anchor="c")

		t = tk.Button(self.win, borderwidth=0, highlightthickness=0, command=self.salva_conf)
		self.img_salvar = ImageTk.PhotoImage(file="images/button_salvar.png")
		t.config(image=self.img_salvar)
		self.image = self.img_salvar
		t.place(relx=0.3, rely=0.90, anchor="s")

		self.k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command=self.deleta_Aresta)
		self.img_apagarAresta = ImageTk.PhotoImage(file="images/button_apagar-aresta.png")
		self.k.config(image=self.img_apagarAresta)
		self.image = self.img_apagarAresta
		self.k.place(relx=0.7, rely=0.90, anchor="s")

	def salva_conf(self):
		self.comprimento = self.distancia.get()
		self.message.set(self.comprimento)
		self.widget.configure(text=self.message.get())
		self.win.destroy()

class No(object):
	def __init__(self, canvas, image_name, xpos, ypos, cont):
		self.posicaoAtual = [xpos,ypos]
		self.arestasAdj = []
		self.nosAdj = []
		self.qtdMoves = 0
		self.on = True

		self.nome_No = str(cont) #'Nó '+
		self.canvas = canvas
		self.image_name = image_name
		self.xpos, self.ypos = xpos, ypos
		self.tk_image = tk.PhotoImage(file="{}{}".format(IMAGE_PATH, image_name))
		self.image_obj = canvas.create_image(xpos, ypos, image=self.tk_image)

		self.canvas_id = self.canvas.create_text(xpos - 10, ypos - 35)
		self.canvas.itemconfig(self.canvas_id, text = self.nome_No, font='Helvetica 10')

		canvas.tag_bind(self.image_obj, '<Double-Button-1>', self.set_No)
		canvas.tag_bind(self.image_obj, '<Button1-Motion>',	 self.move)
		canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)

		self.move_flag = False

	def __del__(self):
		print("deletado")

	def set_No(self,event):

		self.win = tk.Toplevel()
		self.win.wm_title("Configurações: "+self.nome_No)
		self.win.iconbitmap(r'images\favicon.ico')
		self.win.geometry("%dx%d%+d%+d" % (290,85, self.xpos, self.ypos))

		l = tk.Label(self.win, text="Nome do Nó: ")
		l.place(relx=0.23, rely=0.2, anchor="n")

		self.nome_NoAt = tk.Entry(self.win)
		self.nome_NoAt.insert(10, self.nome_No)
		self.nome_NoAt.place(relx=0.65, rely=0.2, anchor="n")

		k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command=self.atualiza_info)
		self.img_salvar = ImageTk.PhotoImage(file="images/button_salvar.png")
		k.config(image=self.img_salvar)
		self.image = self.img_salvar
		k.place(relx=0.3, rely=0.96, anchor="s")

		d = tk.Button(self.win, borderwidth=0, highlightthickness=0, command=self.deleta_No)
		self.img_apagarNo = ImageTk.PhotoImage(file="images/button_apagar-no.png")
		d.config(image=self.img_apagarNo)
		self.image = self.img_salvar
		d.place(relx=0.7, rely=0.96, anchor="s")

		self.move_flag = False

	def deleta_No(self):
		self.canvas.delete(self.image_obj)
		self.canvas.delete(self.canvas_id)
		#self.__del__()
		self.on = False
		for i in range(len(self.arestasAdj)):
			self.arestasAdj[i].deleta_Aresta_2()
		self.win.destroy()	

	def atualiza_info(self):
		self.nome_No = self.nome_NoAt.get()
		self.canvas.delete(self.canvas_id)

		new_xpos, new_ypos = self.canvas.coords(self.image_obj)[0], self.canvas.coords(self.image_obj)[1]
		self.canvas_id = self.canvas.create_text(new_xpos - 10, new_ypos - 35, anchor="nw", tag="text")
		self.canvas.itemconfig(self.canvas_id, text=self.nome_No, font='Helvetica 10')

		self.win.destroy()

	def move(self, event):
		if self.move_flag and self.qtdMoves==0:
			new_xpos, new_ypos = event.x, event.y

			self.canvas.move(self.image_obj, new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)

			self.mouse_xpos = new_xpos
			self.mouse_ypos = new_ypos
			self.canvas.delete(self.canvas_id)

		else:
			self.move_flag = True
			self.canvas.tag_raise(self.image_obj)
			self.mouse_xpos = event.x
			self.mouse_ypos = event.y

	def release(self, event):
		self.qtdMoves += 1
		self.canvas.delete(self.canvas_id)
		self.move_flag = False
		print(self.nome_No,": ",self.canvas.coords(self.image_obj))
		self.posicaoAtual = self.canvas.coords(self.image_obj)
		new_xpos, new_ypos = self.canvas.coords(self.image_obj)[0],self.canvas.coords(self.image_obj)[1]

		self.canvas_id = self.canvas.create_text(new_xpos - 10, new_ypos - 35, anchor="nw", tag="text")
		self.canvas.itemconfig(self.canvas_id, text=self.nome_No, font='Helvetica 10')

class Rede(tk.Frame):
	def __init__(self, master):

		self.listadeNos 		= []
		self.posicaoNo 			= []
		self.listadeArestas 	= []
		self.listaNomesVertices = []
		self.grafo 				= [[]]

		self.canvas = tk.Canvas()
		self.master = master
		self.master.protocol("WM_DELETE_WINDOW", self.close)
		tk.Frame.__init__(self, master)
		self.pack()

		#criacao do menu superior
		menubar = Menu(self.master)
		master.config(menu=menubar)
		fileMenu = Menu(menubar)
		fileMenu.add_command(label="Criar Rede",command= self.criar_Rede)
		fileMenu.add_command(label="Carregar Topologia",command =self.carregar_Topologia)
		fileMenu.add_command(label="Exit",command=self.close)
		menubar.add_cascade(label="File", menu=fileMenu)

	def deleta(self):
		self.listadeNos 		= []
		self.posicaoNo 			= []
		self.listadeArestas 	= []
		self.listaNomesVertices = []

	def criar_Canvas(self):
		self.cont = 0
		self.canvas = tk.Canvas(self.master, width=APP_WIDTH, height=APP_HEIGHT, bg='white', highlightthickness=0)
		self.canvas.pack(fill="both", expand=True)

	def criar_Rede(self):
		self.canvas.destroy()
		self.deleta()
		self.criar_Canvas()
		self.canvas.configure(background= 'alice blue')
		
		self.criar_no = tk.Button(self.canvas, borderwidth=0, highlightthickness=0, command=self.criar_No) 
		self.img_criarNo = ImageTk.PhotoImage(file="images/button_adicionar-no.png")
		self.criar_no.config(image=self.img_criarNo)
		self.image = self.img_criarNo
		self.criar_no.place(relx=.04, rely=0.96, anchor="w")

		self.criar_aresta = tk.Button(self.canvas, borderwidth=0, highlightthickness=0, command=self.criar_Aresta)
		self.img_criarAresta = ImageTk.PhotoImage(file = "images/button_adicionar-aresta.png")
		self.criar_aresta.config(image=self.img_criarAresta)
		self.image = self.img_criarAresta
		self.criar_aresta.place(relx=.2, rely=.96, anchor="w")

		self.salvar_topologia = tk.Button(self.canvas, borderwidth=0, highlightthickness=0, command=self.salvar_Topologia)
		self.img_topologia = ImageTk.PhotoImage(file="images/button_salvar-topologia.png")
		self.salvar_topologia.config(image=self.img_topologia)
		self.image = self.img_topologia
		self.salvar_topologia.place(relx=0.96, rely=.96, anchor="e")

	def carregar_Topologia(self): 
		from tkinter import filedialog as fd
		self.caminho = fd.askopenfilename()

		self.canvas.destroy()
		self.deleta()
		self.criar_Canvas()
		self.canvas.configure(background= 'light steel blue')

		self.topologia = open(self.caminho)
		df = pd.read_csv(self.topologia, sep=r',')

		new_list = []
		
		for i in range(len(df)):
			string = df['Adjacencias'][i]
			string = string.replace('[','')
			string = string.replace(']','')
			string = string.replace(', ',',')
			string = string.replace("'","")
			string = string.split(',')
			new_list = new_list + [string]

		self.grafo = [[0 for _ in range(len(df))] for _ in range (len(df))]

		for i in range(len(df)):	
			new = No(self.canvas, "pc.png", df['Px'][i], df['Py'][i], df['Nome'][i])
			self.listadeNos.append(new)
			self.listaNomesVertices.append(self.listadeNos[i].nome_No)

		for i in range (len(df)):
			for j in range(len(new_list[i])-1):
				for k in range (len(self.listaNomesVertices)):
					if (self.listaNomesVertices[k]==new_list[i][j]):
						self.grafo[i][k]=int(new_list[i][j+1])

		self.grafo_adj = {}
		self.dic_adj = {}
		for i in range(len(self.grafo)):
			adjacents = {}
			adj = []
			for j in range(len(self.grafo)):
				if (self.grafo[i][j]!=0 and i<=j):
					novaAresta = Aresta(self.canvas,self.grafo[i][j], self.listadeNos, i, j, 10) #falta por o lambda

					self.listadeArestas.append(novaAresta)
					self.listadeNos[i].arestasAdj.append(novaAresta)
					self.listadeNos[j].arestasAdj.append(novaAresta)
					
					self.listadeNos[i].nosAdj.append(self.listadeNos[j])
					self.listadeNos[j].nosAdj.append(self.listadeNos[i])

				if (self.grafo[i][j] != 0):
					adjacents[j] = (self.grafo[i][j])
					adj.append(j)

			self.dic_adj[i] = adjacents
			self.grafo_adj[i] = adj
		self.carregar_opcoes_topologia()

	def carregar_opcoes_topologia(self):
		self.button_simular = tk.Button(self.canvas, borderwidth=0, highlightthickness=0, command=self.tela_simulacao)
		self.img_simular= ImageTk.PhotoImage(file="images/button_simular.png")
		self.button_simular.config(image=self.img_simular)
		self.image = self.img_simular
		self.button_simular.place(relx=.04, rely=0.96, anchor="w")

		self.button_config = tk.Button(self.canvas, borderwidth=0, highlightthickness=0, command=self.tela_set_Topologia)
		self.img_conf = ImageTk.PhotoImage(file="images/button_configuracoes.png")
		self.button_config.config(image=self.img_conf)
		self.image = self.img_conf
		self.button_config.place(relx=0.96, rely=.96, anchor="e")

	def tela_set_Topologia(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Configuração da Rede")
		self.win.iconbitmap(r'images\favicon.ico')
		self.win.geometry("%dx%d%+d%+d" % (300, 140, 100, 200))

		l = tk.Label(self.win, text="Redefinir Lambda: ")
		l.place(relx=0.3, rely=0.3, anchor="c")

		self.novoL= tk.Entry(self.win, width=15)
		self.novoL.place(relx=0.7, rely=0.3, anchor="c")

		k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command= self.redefinir_Lambda)
		self.img_salvar = ImageTk.PhotoImage(file="images/button_salvar.png")
		k.config(image=self.img_salvar)
		self.image = self.img_salvar
		k.place(relx=0.5, rely=0.8, anchor="c")

	def redefinir_Lambda(self):
		novoLambda = int(self.novoL.get()) 
		for i in range(len(self.listadeArestas)):
			if(self.listadeArestas[i].on):
				self.listadeArestas[i].valorLambda = novoLambda
		self.win.destroy()

	def tela_simulacao(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Simulação")
		self.win.iconbitmap(r'images\favicon.ico')
		self.win.geometry("%dx%d%+d%+d" % (300, 200, 100, 200))

		l = tk.Label(self.win, text="Número de Chamadas: ")
		l.place(relx=0.3, rely=0.3, anchor="c")

		self.numeroChamadas= tk.Entry(self.win, width=15)
		self.numeroChamadas.place(relx=0.7, rely=0.3, anchor="c")

		k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command= self.simulacao)
		self.img_inicia = ImageTk.PhotoImage(file="images/button_iniciar-simulacao.png")
		k.config(image=self.img_inicia)
		self.image = self.img_inicia
		k.place(relx=0.5, rely=0.8, anchor="c")

	def caminhos(self, grafo, origem, destino):
		pilha = [(origem, [origem])]
		while pilha:
			vertice, caminho = pilha.pop()
			for proximo in (set(grafo[vertice]) - set(caminho)):
				if proximo == destino:
					yield caminho + [proximo]
				else:
					pilha.append((proximo, caminho + [proximo]))
	
	def pesos(self, grafo, caminhos):
		pesoCaminho = []
		for i in range(len(caminhos)):
			custo = 0
			for j in range(len(caminhos[i])-1):
				custo = custo + grafo[caminhos[i][j]][caminhos[i][j+1]]
			pesoCaminho.append((caminhos[i] , custo))
		return pesoCaminho
	
	def dijkstra(self, grafo, origem, dest, visited=[], distances={}, predecessors={}):
		if origem == dest:
			path=[]
			pred=dest
			while pred != None:
				path.append(pred)
				pred=predecessors.get(pred,None)
			print('Menor caminho: '+str(path)+" custo = "+str(distances[dest])) 
		else :     
			if not visited: 
				distances[origem] = 0
			for neighbor in grafo[origem] :
				if neighbor not in visited:
					new_distance = distances[origem] + grafo[origem][neighbor]
					if new_distance < distances.get(neighbor,float('inf')):
						distances[neighbor] = new_distance
						predecessors[neighbor] = origem
			visited.append(origem)
			unvisited={}
			for k in grafo:
				if k not in visited:
					unvisited[k] = distances.get(k,float('inf'))
			x = min(unvisited, key=unvisited.get)
			self.dijkstra(grafo, x, dest, visited, distances, predecessors)

	def simulacao(self):
		arquivo = pd.DataFrame()
		arquivo['# da Simulação'] = 0
		arquivo['Origem->Destino'] = 0
		arquivo['Caminho'] = 0
		arquivo['Peso'] = 0

		n 		   = []
		origemDest = []
		caminho    = []
		peso       = []

		nChamadas = int(self.numeroChamadas.get())
		for i in range(nChamadas):
			import random as rd 
			no1 = rd.randint(0,len(self.listadeNos)-1)
			no2 = rd.randint(0,len(self.listadeNos)-1)
			while no1 == no2:
				no2 = rd.randint(0,len(self.listadeNos)-1)

			self.dijkstra(self.dic_adj, no1, no2,visited=[], distances={}, predecessors={})

			caminhos = list(self.caminhos(self.grafo_adj, no1, no2))
			td = self.pesos(self.grafo, caminhos)

			for j in range(len(caminhos)):
				n.append(i)
			n.append("")
			for j in range(len(caminhos)):
				origemDest.append(str(self.listadeNos[no1].nome_No)+"->"+str(self.listadeNos[no2].nome_No))
			origemDest.append("")
			for j in range(len(caminhos)):
				c,p = td[j][0],td[j][1]
				for k in range(len(c)):
					c[k] = self.listadeNos[int(c[k])].nome_No
				c = str(c)
				c = c.replace(",","->")
				c = c.replace("[","")
				c = c.replace("]","")
				c = c.replace("'","")
				caminho.append(c)
				peso.append(p)
			caminho.append("")
			peso.append("")

		arquivo['# da Simulação'] = n
		arquivo['Origem->Destino'] = origemDest
		arquivo['Caminho'] = caminho
		arquivo['Peso'] = peso

		arquivo.to_csv('simulation/simulacao.csv',index=False)

		self.win.destroy()

	def aviso(self,text):
		self.win = tk.Toplevel()
		self.win.wm_title("Atenção")
		self.win.geometry("%dx%d%+d%+d" % (230, 70, 100, 200))

		l = tk.Label(self.win, text=text)
		l.place(relx=0.5, rely=0.3, anchor="c")

		k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command= lambda: self.win.destroy())
		self.img_ok = ImageTk.PhotoImage(file="images/button_ok.png")
		k.config(image=self.img_ok)
		self.image = self.img_ok
		k.place(relx=.5, rely=.76, anchor="c")

	def garbage_collector(self):
		indexToDelete = []
		for i in range(len(self.listadeNos)):
			if self.listadeNos[i].on == False:
				indexToDelete.append(i)

		for i in range(len(indexToDelete)):
			self.listadeNos.remove(self.listadeNos[indexToDelete[i]])

		
		for i in range(len(self.listadeNos)):
			indexToDelete = []		
			for j in range(len(self.listadeNos[i].arestasAdj)):
				if(self.listadeNos[i].arestasAdj[j].on == False):
					indexToDelete.append(j)
			for k in range(len(indexToDelete)):
				self.listadeNos[i].arestasAdj.remove(self.listadeNos[i].arestasAdj[indexToDelete[k]])

		indexToDelete = []

		for i in range(len(self.listadeArestas)):
			if self.listadeArestas[i].on == False:
				indexToDelete.append(i)

		for i in range(len(indexToDelete)):
				self.listadeArestas.remove(self.listadeArestas[indexToDelete[i]])
	def salvar_Topologia(self):
		garbage_collector()

		self.win = tk.Toplevel()
		self.win.wm_title("Salvar Topologia")
		self.win.iconbitmap(r'images\favicon.ico')
		self.win.geometry("%dx%d%+d%+d" % (300, 80, 100, 200))

		l = tk.Label(self.win, text="Nome da Topologia: ")
		l.place(relx=0.2, rely=0.3, anchor="c")

		self.nomeTopologia = tk.Entry(self.win, width=20)
		self.nomeTopologia.place(relx=0.6, rely=0.3, anchor="c")

		k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command= self.criar_Dataframe)
		self.img_salvar = ImageTk.PhotoImage(file="images/button_salvar.png")
		k.config(image=self.img_salvar)
		self.image = self.img_salvar
		k.place(relx=0.5, rely=0.8, anchor="c")

	def criar_Dataframe(self):
		arquivo = pd.DataFrame()
		arquivo['Nome'] = 0
		arquivo['Px'] = 0
		arquivo['Py'] = 0
		arquivo['Adjacencias'] = 0

		nome = []
		posx = []
		posy = []
		adj  = []

		for i in range(len(self.listadeNos)):
			nome.append(str(self.listadeNos[i].nome_No))

		for i in range(len(self.listadeNos)):
			posx.append(self.listadeNos[i].posicaoAtual[0])

		for i in range(len(self.listadeNos)):
			posy.append(self.listadeNos[i].posicaoAtual[1])

		for i in range(len(self.listadeNos)):
			aux = []
			for j in range(len(self.listadeNos[i].arestasAdj)):
				if(self.listadeNos[i].arestasAdj[j].lista[self.listadeNos[i].arestasAdj[j].No1].nome_No == self.listadeNos[i].nome_No):
					aux.append(self.listadeNos[i].arestasAdj[j].lista[self.listadeNos[i].arestasAdj[j].No2].nome_No)
				else:
					aux.append(self.listadeNos[i].arestasAdj[j].lista[self.listadeNos[i].arestasAdj[j].No1].nome_No)
				aux.append(self.listadeNos[i].arestasAdj[j].comprimento)
			adj.append(aux)

		arquivo['Nome'] 		= nome
		arquivo['Px'] 			= posx
		arquivo['Py'] 			= posy
		arquivo['Adjacencias'] 	= adj

		arquivo.to_csv(self.nomeTopologia.get()+'.csv',index=False)

		self.win.destroy()
		self.aviso("Topologia Salva com sucesso!")

	def contaNos(self):
		self.cont = self.cont + 1
		t = self.cont
		return t

	def criar_Aresta(self):
		self.win = tk.Toplevel()
		self.win.wm_title("Nova Aresta")
		self.win.iconbitmap(r'images\favicon.ico')
		self.win.geometry("%dx%d%+d%+d" % (250, 190, 100, 200))


		lj = tk.Label(self.win, text="De:")
		lj.place(relx=0.4, rely=0.1, anchor="e")

		
		self.lista1 = tk.StringVar(self.win)
		self.lista1.set(" ")
		
		self.listaNomesVertices = []

		for i in range (len(self.listadeNos)):
			if self.listadeNos[i].on == True:
				self.listaNomesVertices.append(str(self.listadeNos[i].nome_No))

		try:
			w = tk.OptionMenu(self.win, self.lista1, *self.listaNomesVertices)
		except:
			pass
		w.place(relx=0.6, rely=0.05, anchor="n")

		iy = tk.Label(self.win, text="Para:")
		iy.place(relx=0.4, rely=0.3, anchor="e")


		self.lista2 = tk.StringVar(self.win)
		self.lista2.set(" ")
		try:
			r = tk.OptionMenu(self.win, self.lista2, *self.listaNomesVertices)
		except:
			pass
		r.place(relx=0.6, rely=0.3, anchor="c")

		l = tk.Label(self.win, text="Comprimento: ")
		l.place(relx=0.4, rely=0.5, anchor="e")
	
		self.valorComprimento = tk.Entry(self.win)
		self.valorComprimento.place(relx=0.6, rely=0.5, width = 50, anchor="c")

		l = tk.Label(self.win, text="Lambda (λ): ")
		l.place(relx=0.4, rely=0.65, anchor="e")
	

		self.valorLambda = tk.Entry(self.win)
		self.valorLambda.insert(0,"10")
		self.valorLambda.place(relx=0.6, rely=0.65, width = 50, anchor="c")

		k = tk.Button(self.win, borderwidth=0, highlightthickness=0, command= self.captura)
		self.img_salvar = ImageTk.PhotoImage(file="images/button_salvar.png")
		k.config(image=self.img_salvar)
		self.image = self.img_salvar
		k.place(relx=0.5, rely=0.98, anchor="s")


	def captura(self):
		item1 = 0
		item2 = 0
		for i in range(len(self.listadeNos)):
			if (self.listadeNos[i].nome_No == self.lista1.get()):
				item1 = i
			if (self.listadeNos[i].nome_No == self.lista2.get()):
				item2 = i

		novaAresta = Aresta(self.canvas, self.valorComprimento.get(), self.listadeNos, item1, item2, int(self.valorLambda.get()))
		self.listadeNos[item1].arestasAdj.append(novaAresta)
		self.listadeNos[item2].arestasAdj.append(novaAresta)

		self.listadeNos[item1].nosAdj.append(self.listadeNos[item2])
		self.listadeNos[item2].nosAdj.append(self.listadeNos[item1])

		self.win.destroy()

	def close(self):
		print("Rede-Shutdown")
		self.master.destroy()

	def criar_No(self):
		cont = self.contaNos()
		import random
		self.image_1 = No(self.canvas, "pc.png", random.randint(20,100), random.randint(20,100), cont)
		self.listadeNos.append(self.image_1)
		# print("--------------------------")
		# print(self.listadeNos)

def main():
	app_win = tk.Tk()
	app_win.title(APP_TITLE)
	app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
	app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))
	app_win.resizable(width=False, height=False)
	app_win.iconbitmap(r'images\favicon.ico')
	app = Rede(app_win)
	app_win.mainloop()


if __name__ == '__main__':
	main()  