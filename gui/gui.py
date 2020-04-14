from tkinter import Tk, Canvas, Frame, PhotoImage, Menu, Scrollbar, Button, BitmapImage, Label, Wm
from PIL import ImageTk, Image



APP_TITLE = "Teste Regras Firewall"
APP_XPOS = 200
APP_YPOS = 200
APP_WIDTH = 300
APP_HEIGHT = 200

IMAGE_PATH = "images/"


class CreateCanvasObject(object):

    # Coloca a imagem no Canvas
    def __init__(self, canvas, image_name, xpos, ypos):
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos

        self.tk_image = PhotoImage(file="{}{}".format(IMAGE_PATH, image_name))

    
        self.icone = Button(self.canvas, image=self.tk_image,text="Texto", compound='top')
        self.icone.bind('<Button1-Motion>',self.move)
        self.icone.bind('<ButtonRelease-1>',self.release)
        
        # bindtags

        self.item = self.canvas.create_window(200,100,anchor='c', window=self.icone)

        # self.image_obj = canvas.create_image(xpos, ypos, image=self.tk_image)

        # canvas.tag_bind(self.icone, '<Button1-Motion>', self.move)
        # canvas.tag_bind(self.icone, '<ButtonRelease-1>', self.release)

        self.move_flag = False

    # Faz a imagem se mover
    def move(self, event):
        print("Move")
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y

            self.canvas.move(self.item, new_xpos -
                             self.mouse_xpos, new_ypos-self.mouse_ypos)

            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.item)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        print("release")
        self.move_flag = False


class Application(Frame):

    # NOTAS: 
    #   Popup para os hosts, sw, routers
    #   Criar tooltips para os botoes -> linha 99

    def __init__(self,parent=None, cheight=500, cwidth=900):
        # self.master = master
        # self.master.protocol("WM_DELETE_WINDOW", self.close)
        Frame.__init__(self,parent)
        self.appName = APP_TITLE
        
        #Titulo
        self.top = self.winfo_toplevel()
        self.top.title(self.appName)

        # Edita tamanho do canvas
        self.canvasH, self.canvasW = cheight,cwidth
        self.cframe,self.canvas = self.createCanvas()

        self.Switch_num = 0
        self.Router_num = 0
        self.Host_num = 0

        self.prefixos = {
            "Switch": "SW",
            "Router": "R",
            "Host"  : "H"
        }

        self.createMenubar()


        # Toolbar -> barra lateral dos equipamentos
        self.ativo = None
        self.imagens = imagens()
        self.tools = ('Switch','Host', 'Router')
        self.buttons = {}
        self.toolbar = self.createToolbar()


        # Coloca o canvas e o toolbox na janela
        self.toolbar.grid( column=0, row=0, sticky='nsew')
        self.cframe.grid( column=1, row=0 )
        self.columnconfigure( 1, weight=1 )
        self.rowconfigure( 0, weight=1 )
        self.pack( expand=True, fill='both' )

        Wm.wm_protocol( self.top, name='WM_DELETE_WINDOW', func=self.quit )

    def quit( self ):
        # Fecha o programa
        Frame.quit( self )

    def canvasx( self, x_root ):
        "Converte a coordenada x do root para x do canvas"
        c = self.canvas
        return c.canvasx( x_root ) - c.winfo_rootx()

    def canvasy( self, y_root ):
        "Converte a coordenada x do root para y do canvas"
        c = self.canvas
        return c.canvasy( y_root ) - c.winfo_rooty()

    def createToolbar(self):
        toolbar = Frame(self)

        for tool in self.tools:
            cmd_botao = lambda t=tool : self.ativaBotao(t)
            b = Button(toolbar, text=tool,command=cmd_botao)
            if tool in self.tools:
                b.config(height=75, image=self.imagens[tool])
            b.pack()
            self.buttons[tool] = b
        self.ativaBotao(self.tools[0])
        return toolbar
                

    # Ativa o botão selecionado
    def ativaBotao(self,botao):
        # Se algum botão já foi selecionado, coloca o mesmo na posição "levantado"
        if self.ativo:
            self.buttons[self.ativo].configure(relief='raised')
        
        # "Afunda" ou "clica o botão selecionado"
        self.buttons[botao].configure(relief='sunken')
        self.ativo = botao



    def createCanvas(self):
       f = Frame(self)
       canvas = Canvas(f, width=self.canvasH, height=self.canvasH, bg='white')

       xbar = Scrollbar( f, orient='horizontal', command=canvas.xview )
       ybar = Scrollbar( f, orient='vertical', command=canvas.yview )
       canvas.configure( xscrollcommand=xbar.set, yscrollcommand=ybar.set )

       # Resize box
       resize = Label( f, bg='white' )
       # Layout
       canvas.grid( row=0, column=1, sticky='nsew')
       ybar.grid( row=0, column=2, sticky='ns')
       xbar.grid( row=1, column=1, sticky='ew' )
       resize.grid( row=1, column=2, sticky='nsew' )

       # Resize behavior
       f.rowconfigure( 0, weight=1 )
       f.columnconfigure( 1, weight=1 )
       f.grid( row=0, column=0, sticky='nsew' )
       f.bind( '<Configure>', lambda event: self.updateScrollRegion() )  

       # Mouse bindings

       canvas.bind( '<ButtonPress-1>', self.clickCanvas )
       canvas.bind( '<B1-Motion>', self.dragCanvas )
       canvas.bind( '<ButtonRelease-1>', self.releaseCanvas )
       
       return f, canvas

    def updateScrollRegion( self ):
        "Update canvas scroll region to hold everything."
        bbox = self.canvas.bbox( 'all' )
        if bbox is not None:
            self.canvas.configure( scrollregion=( 0, 0, bbox[ 2 ],
                                   bbox[ 3 ] ) )
       

    def canvasHandle( self, eventName, event ):
        "Generic canvas event handler"
        if self.ativo is None:
            return
        toolName = self.ativo
        handler = getattr( self, eventName + toolName, None )
        if handler is not None:
            handler( event )

    def clickCanvas( self, event ):
        "Canvas click handler."
        self.canvasHandle( 'click', event )

    def dragCanvas( self, event ):
        "Canvas drag handler."
        self.canvasHandle( 'drag', event )

    def releaseCanvas( self, event ):
        "Canvas mouse up handler."
        self.canvasHandle( 'release', event )

    def clickRouter(self,event):
        self.novoNode("Router", event)

    def clickSwitch(self,event):
        self.novoNode("Switch", event)

    def clickHost(self,event):
        self.novoNode("Host", event)

    def novoNode(self,node,event):
        # Add um novo nó no canvas
        c = self.canvas
        x = c.canvasx(event.x)
        y = c.canvasy(event.y)

        nomeNo = self.prefixos[node]

        if node == "Switch":
            self.Switch_num += 1
            nomeNo += str(self.Switch_num)
            print("Add Switch " + nomeNo)
        elif node == "Host":
            self.Host_num += 1
            nomeNo += str(self.Host_num)
            print("Add host " + nomeNo)
        elif node == "Router":
            self.Router_num += 1
            nomeNo += str(self.Router_num)
            print("Add router " + nomeNo)
        print(x,y)



    def close(self):
        print("Application-Shutdown")
        self.master.destroy()

    # Cria um menuBar
    def createMenubar(self):    
        "Create our menu bar."
        mbar = Menu( self.top )
        self.top.configure( menu=mbar )


        fileMenu = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="File", menu=fileMenu )
        fileMenu.add_command( label="New")
        fileMenu.add_command( label="Open")
        fileMenu.add_command( label="Save")
        fileMenu.add_command( label="Export Level 2 Script")
        fileMenu.add_separator()
        fileMenu.add_command( label='Quit')


def imagens():
    return {
        'Switch': PhotoImage(file="{}sw.png".format(IMAGE_PATH)),
        'Host': PhotoImage(file="{}pc.png".format(IMAGE_PATH)),
        'Router': PhotoImage(file="{}router.png".format(IMAGE_PATH)),
        'Select': BitmapImage(
            file='/usr/include/X11/bitmaps/left_ptr' ),
        
    }

def main():
    # app_win = Tk()
    # app_win.title(APP_TITLE)
    # app_win.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))

    # app = Application(app_win).pack(fill='both', expand=True)

    # app_win.mainloop()
    app = Application()
    app.mainloop()



if __name__ == '__main__':
    main()
