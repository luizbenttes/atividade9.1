try:
    # Tkinter for Python 2.xx
    import Tkinter as tk
except ImportError:
    # Tkinter for Python 3.xx
    import tkinter as tk
    from tkinter import Menu
    from tkinter import ttk
    from tkinter.messagebox import showinfo
    import pandas as pd

APP_TITLE = "SIMTON"
APP_XPOS = 100
APP_YPOS = 100
APP_WIDTH = 400
APP_HEIGHT = 200

IMAGE_PATH = "images/"


class Aresta(object):
    def __init__(self, canvas, comprimento, lista, No1, No2):
        self.comprimento = comprimento
        self.No1 = No1
        self.No2 = No2
        self.canvas = canvas
        self.lista = lista
        self.message = tk.StringVar()
        self.message.set(self.comprimento)

        self.posicaoAresta = self.lista[self.No1].posicaoAtual + self.lista[self.No2].posicaoAtual
        self.aresta = self.canvas.create_line(self.posicaoAresta, width=3)

        self.widget = tk.Button(self.canvas, text=self.message.get(), fg='white', bg='black',command =self.configura_Aresta)
        self.widget.pack()
        canvas.tag_bind(self.aresta, '<Double-Button-1>', self.configura_Aresta)
        x = (self.lista[No1].posicaoAtual[0] + self.lista[No2].posicaoAtual[0]) / 2
        y = (self.lista[No1].posicaoAtual[1] + self.lista[No2].posicaoAtual[1]) / 2
        canvas.create_window(x, y, window=self.widget)


    def deleta_Aresta(self):
        self.canvas.delete(self.aresta)
        self.widget.destroy()
        self.win.destroy()

    def configura_Aresta(self):
        self.win = tk.Toplevel()

        self.win.wm_title(str(self.lista[self.No1].nome_No+"->"+self.lista[self.No2].nome_No))
        self.win.geometry("%dx%d%+d%+d" % (350, 100, 100, 200))

        r = tk.Label(self.win, text=" ")
        r.grid(row=1, column=0)

        l = tk.Label(self.win, text="Distância: ")
        l.grid(row=1, column=1)


        self.distancia = tk.Entry(self.win)
        self.distancia.insert(10, self.comprimento)
        self.distancia.grid(row=1, column=2)

        v = tk.Label(self.win, text=" ")
        v.grid(row=2, column=3)

        t = ttk.Button(self.win, text="Salvar", command=self.salva_conf)
        t.grid(row=1, column=3)

        self.k = ttk.Button(self.win, text="Exclui Aresta", command=self.deleta_Aresta)
        self.k.grid(row=3, column=3)

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

        self.nome_No = 'Nó '+str(cont)
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos
        self.tk_image = tk.PhotoImage(file="{}{}".format(IMAGE_PATH, image_name))
        self.image_obj = canvas.create_image(xpos, ypos, image=self.tk_image)

        self.canvas_id = self.canvas.create_text(xpos - 10, ypos - 35)
        self.canvas.itemconfig(self.canvas_id, text = self.nome_No, font='Helvetica 10')

        canvas.tag_bind(self.image_obj, '<Double-Button-1>', self.set_No)
        canvas.tag_bind(self.image_obj, '<Button1-Motion>',self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)


        self.move_flag = False

    def set_No(self,event):
        self.win = tk.Toplevel()
        self.win.wm_title(self.nome_No)
        self.win.geometry("%dx%d%+d%+d" % (270,70, self.xpos, self.ypos))
        l = tk.Label(self.win, text="Nome do Nó: ")
        l.grid(row=1, column=1)

        self.nome_NoAt = tk.Entry(self.win)
        self.nome_NoAt.insert(10, self.nome_No)
        self.nome_NoAt.grid(row=1, column=2)

        space = tk.Label(self.win,text=" ")
        space.grid(row=2)

        k = ttk.Button(self.win, text="Salvar", command=self.atualiza_info)
        k.grid(row=3, column=1)

        d = ttk.Button(self.win, text="Apagar Nó", command=self.deleta_No)
        d.grid(row=3,column= 2)

        self.move_flag = False

    def deleta_No(self):
        self.canvas.delete(self.image_obj)
        self.win.destroy()
        self.canvas.delete(self.canvas_id)

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

            self.canvas.move(self.image_obj,
                             new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)

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

        self.listadeNos = []
        self.posicaoNo = []
        self.listadeArestas = []

        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)
        self.pack()

        #criacao do menu superior
        menubar = Menu(self.master)
        master.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Criar Rede")
        fileMenu.add_command(label="Carregar Rede",command =self.carregar_Topologia)
        fileMenu.add_command(label="Exit",command=self.close)
        menubar.add_cascade(label="File", menu=fileMenu)
        self.cont = 0
        self.canvas = tk.Canvas(self, width=600, height=400, bg='white', highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
 
        self.criar_no = tk.Button(self, text="Nó", width="10", command=self.criar_No)
        self.criar_no.place(relx=.2, rely=0.96, anchor="w")

        self.salvar_topologia = tk.Button(self, text="Salvar topologia", width="15", command=self.salvar_Topologia)
        self.salvar_topologia.place(relx=.6, rely=.96, anchor="e")

        self.criar_aresta = tk.Button(self, text="Aresta", width="10", command=self.criar_Aresta)
        self.criar_aresta.place(relx=.8, rely=.96, anchor="e")

    def carregar_Topologia(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Nova Topologia")
        self.win.geometry("%dx%d%+d%+d" % (350, 80, 100, 200))

        l = tk.Label(self.win,text="Insira o caminho do arquivo que você deseja carregar:")
        l.place(relx=0.5, rely=0.1, anchor="c")

        self.caminho = tk.Entry(self.win)
        self.caminho.place(relx=.5, rely=.4, anchor="c")

        k = ttk.Button(self.win, text="OK", command=lambda: self.criar_Rede)
        k.place(relx=.5, rely=.75, anchor="c")

    def criar_Rede(self):
        self.topologia = open(self.caminho.get())
        self.win.destroy()

    def aviso(self,text):
        self.win = tk.Toplevel()
        self.win.wm_title("Atenção")
        self.win.geometry("%dx%d%+d%+d" % (230, 70, 100, 200))

        l = tk.Label(self.win, text=text)
        l.place(relx=0.5, rely=0.36, anchor="c")

        k = ttk.Button(self.win, text="OK", command= lambda: self.win.destroy())
        k.place(relx=.5, rely=.8, anchor="c")

    def salvar_Topologia(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Salvar Topologia")
        self.win.geometry("%dx%d%+d%+d" % (350, 50, 100, 200))

        l = tk.Label(self.win, text="Nome da Topologia: ")
        l.grid(row=1,column=1)

        self.nomeTopologia = tk.Entry(self.win)
        self.nomeTopologia.grid(row=1, column=2)

        k = ttk.Button(self.win, text="Salvar", command= self.criar_Dataframe)
        k.grid(row=1, column=3)

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

        arquivo['Nome'] = nome
        arquivo['Px'] = posx
        arquivo['Py'] = posy
        arquivo['Adjacencias'] = adj

        arquivo.to_csv(self.nomeTopologia.get()+'.csv',index=False)

        self.win.destroy()
        self.aviso("Topologia Salva com sucesso!")

    def contaNos(self):
        self.cont = self.cont + 1
        t = self.cont
        return t

    def criar_Aresta(self):
        self.win = tk.Toplevel()
        self.win.wm_title("Adiciona Aresta")
        self.win.geometry("%dx%d%+d%+d" % (350, 100, 100, 200))
        l = tk.Label(self.win, text="Valor da Aresta: ")
        l.grid(row=1, column=1)
    
        self.valorComprimento = tk.Entry(self.win)
        self.valorComprimento.grid(row=1, column=2)

        lj = tk.Label(self.win, text="De:")
        lj.grid(row=2, column=0)

        
        self.lista1 = tk.StringVar(self.win)
        self.lista1.set(" ")
        listaNomesVertices = [str(self.listadeNos[i].nome_No) for i in range(len(self.listadeNos))]
        w = tk.OptionMenu(self.win, self.lista1, *listaNomesVertices)
        w.grid(row=2, column=1)

        iy = tk.Label(self.win, text="Para:")
        iy.grid(row=2, column=2)


        self.lista2 = tk.StringVar(self.win)
        self.lista2.set(" ")
        r = tk.OptionMenu(self.win, self.lista2, *listaNomesVertices)
        r.grid(row=2, column=3)

        k = ttk.Button(self.win, text="Adicionar Aresta", command= self.captura)
        k.grid(row=3, column=2)


    def captura(self):
        item1 = 0
        item2 = 0
        for i in range(len(self.listadeNos)):
            if (self.listadeNos[i].nome_No == self.lista1.get()):
                item1 = i
            if (self.listadeNos[i].nome_No == self.lista2.get()):
                item2 = i

        novaAresta = Aresta(self.canvas, self.valorComprimento.get(), self.listadeNos, item1, item2)
        self.listadeNos[item1].arestasAdj.append(novaAresta)
        self.listadeNos[item2].arestasAdj.append(novaAresta)

        self.listadeNos[item1].nosAdj.append(self.listadeNos[item2])
        self.listadeNos[item2].nosAdj.append(self.listadeNos[item2])

        print(self.listadeNos[item1].arestasAdj)
        print(self.listadeNos[item2].arestasAdj)
        self.win.destroy()

    def close(self):
        print("Rede-Shutdown")
        self.master.destroy()

    def criar_No(self):
        cont = self.contaNos()
        import random
        self.image_1 = No(self.canvas, "pc.png", random.randint(20,100), random.randint(20,100), cont)
        self.listadeNos.append(self.image_1)

def main():
    app_win = tk.Tk()
    app_win.title(APP_TITLE)
    app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    # app_win.geometry("{}x{}".format(APP_WIDTH, APP_HEIGHT))
    app = Rede(app_win)
    #.pack(fill='both', expand=True)
    app_win.mainloop()


if __name__ == '__main__':
    main()  
