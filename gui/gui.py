# -*- coding: utf-8 -*-

from tkinter import BitmapImage, Button, Canvas, Entry, Frame, Label, Menu, PhotoImage, Scrollbar, Text, Tk, Toplevel, Wm

from PIL import Image
from tkinter.ttk import Notebook
import json

## pesquisar interface
APP_TITLE = "Teste Regras Firewall"
APP_XPOS = 200
APP_YPOS = 200
APP_WIDTH = 300
APP_HEIGHT = 200

IMAGE_PATH = "images/"




class CustomDialog(object):
    def __init__(self, master, _title):
        self.top = Toplevel(master)

        self.bodyFrame = Frame(self.top)
        self.bodyFrame.grid(row=0, column=0, sticky='nswe')

        self.body(self.bodyFrame)

        buttonFrame = Frame(self.top, relief='ridge', bd=3, bg='lightgrey')
        buttonFrame.grid(row=1,column=0, sticky='nswe')

        okButton = Button(buttonFrame, width=8, text='OK', relief='groove', bd=4, command=self.okAction)
        okButton.grid(row=0, column=0, sticky='E')

        cancelButton = Button(buttonFrame, width=8, text='Cancelar', relief='groove', bd=4, command=self.okAction)
        cancelButton.grid(row=0, column=1, sticky='W')
        self.countRule = 1
    
    def body(self,master):
        self.rootFrame = master
    
    def apply(self):
        self.top.destroy()

    def okAction(self):
        self.apply()
        self.top.destroy()

    def cancelAction(self):
        self.top.destroy()

class RouterDialog(CustomDialog):
    def __init__(self, master,title,prefDefaults,links):
        self.prefDefaults = prefDefaults
        self.result = None
        self.links = links

        CustomDialog.__init__(self,master,title)
    
    
    def body(self, master):
        self.rootFrame = master
        n = Notebook(self.rootFrame)
        self.netPropertiesFrame = Frame(n)
        self.firewallFrame = Frame(n)
        self.testFrame = Frame(n)
        n.add(self.netPropertiesFrame, text="Propriedades Rede")
        n.add(self.firewallFrame, text="Firewall")
        n.add(self.testFrame, text="Testes")
        n.pack()

        """ Aba 1: Propriedades """
        Label(self.netPropertiesFrame, text='Nome Roteador:').grid(row=0,sticky='E')
        self.hostname = Entry(self.netPropertiesFrame, width=25)
        self.hostname.grid(row=0,column=1)
        if 'hostname' in self.prefDefaults:
            self.hostname.insert(0,self.prefDefaults['hostname'])
        
        Label(self.netPropertiesFrame, text='DNS:').grid(row=1,sticky='E')
        self.dns = Entry(self.netPropertiesFrame, width=25)
        self.dns.grid(row=1,column=1)
        if 'dns' in self.prefDefaults:
            self.dns.insert(0,self.prefDefaults['dns'])
        # print(self.prefDefaults)

        self.confLinks = {}
        i = 2
        for link in self.links:
            self.confLinks[link] = {}
            Label(self.netPropertiesFrame, text="IP iface {}:".format(link)).grid(row=i,sticky='E')
            self.confLinks[link]['ip'] = Entry(self.netPropertiesFrame,width=25) 
            self.confLinks[link]['ip'].grid(row=i,column=1)
            if 'links' in self.prefDefaults and link in self.prefDefaults['links']:
                self.confLinks[link]['ip'].insert(0,self.prefDefaults['links'][link]['ip'])
            i+=1

            Label(self.netPropertiesFrame, text="Máscara iface {}:".format(link)).grid(row=i,sticky='E')
            self.confLinks[link]['mask'] = Entry(self.netPropertiesFrame,width=25) 
            self.confLinks[link]['mask'].grid(row=i,column=1)
            if 'links' in self.prefDefaults and link in self.prefDefaults['links']:
                self.confLinks[link]['mask'].insert(0,self.prefDefaults['links'][link]['mask'])
            i+=1

            Label(self.netPropertiesFrame, text="Gateway iface {}:".format(link)).grid(row=i,sticky='E')
            self.confLinks[link]['gw'] = Entry(self.netPropertiesFrame,width=25) 
            self.confLinks[link]['gw'].grid(row=i,column=1)
            if 'links' in self.prefDefaults and link in self.prefDefaults['links']:
                self.confLinks[link]['gw'].insert(0,self.prefDefaults['links'][link]['gw'])
            i+=1
            
            # Espaço em branco
            Label(self.netPropertiesFrame, text="  ").grid(row=i,sticky='E')
            i+=1
        
        """ Aba 2: Firewall """

        Label(self.firewallFrame, text="Regras (1 regra por linha):").grid(row=0,sticky="NE")
        self.rules = Text(self.firewallFrame, height=5, width=28)
        self.rules.grid(row=1,column=0)
        if 'rules' in self.prefDefaults:
            self.rules.insert(1.0, self.prefDefaults['rules'])
            


    #     addNewRuleButton = Button(self.firewallFrame, text='Adicionar nova regra', command=self.addNewRuleField)
    #     addNewRuleButton.grid()
    #     self.ruleEntries = []


    # def addNewRuleField(self):
    #     Label(self.firewallFrame, text='Regra ' + str(self.countRule)).grid(row=self.countRule,sticky='W')
    #     self.ruleEntries.append(Entry(self.firewallFrame, width=25))
    #     self.ruleEntries[-1].grid(row=self.countRule,column=1)
    #     self.countRule += 1

    #     print("Add nova regra")


    def apply(self):
        self.result = {'hostname': self.hostname.get()}
        self.result['dns'] = self.dns.get()
        self.result['links'] = {}
        for link in self.confLinks:
            self.result['links'][link] = {}
            self.result['links'][link]['ip'] = self.confLinks[link]['ip'].get()
            self.result['links'][link]['mask'] = self.confLinks[link]['mask'].get()
            self.result['links'][link]['gw'] = self.confLinks[link]['gw'].get()
        self.result['rules'] = self.rules.get(1.0,"end-1c")


class HostDialog(CustomDialog):
    def __init__(self, master, title, prefDefaults):
        self.prefDefaults = prefDefaults
        self.result = None

        CustomDialog.__init__(self,master,title)
    
    def body(self,master):
        self.rootFrame = master
        n = Notebook(self.rootFrame)
        self.propertiesFrame = Frame(n)
        self.firewallFrame = Frame(n)
        self.commandsFrame = Frame(n)
        n.add(self.propertiesFrame, text="Propriedades")
        n.add(self.firewallFrame, text="Firewall")
        n.add(self.commandsFrame, text="Comandos")
        n.pack()

        """ Aba 1: Propriedades """
        # Hostname
        Label(self.propertiesFrame, text="Hostname:").grid(row=0,sticky='E')
        self.hostnameEntry = Entry(self.propertiesFrame, width=25)
        self.hostnameEntry.grid(row=0, column=1)
        if 'hostname' in self.prefDefaults:
            self.hostnameEntry.insert(0,self.prefDefaults['hostname'])
        
        # Endereço IP
        Label(self.propertiesFrame, text="Endereço IPV4:").grid(row=1,sticky="E")
        self.ipAddr = Entry(self.propertiesFrame,width=25)
        self.ipAddr.grid(row=1,column=1)
        if 'ip' in self.prefDefaults:
            self.ipAddr.insert(0, self.prefDefaults['mask'])

        # Máscara de rede
        Label(self.propertiesFrame, text="Máscara de rede:").grid(row=2,sticky="E")
        self.mask = Entry(self.propertiesFrame, width=25)
        self.mask.grid(row=2,column=1)
        if 'mask' in self.prefDefaults:
            self.mask.insert(0, self.prefDefaults['ip'])

        # Rota Padrão
        Label(self.propertiesFrame, text="Rota Padrão:").grid(row=3,sticky="E")
        self.defaultGW = Entry(self.propertiesFrame, width=25)
        self.defaultGW.grid(row=3,column=1)
        if 'defaultRoute' in self.prefDefaults:
            self.defaultGW.insert(0, self.prefDefaults['defaultRoute'])

        
        """ Aba 3: Comandos"""
        # Comando inicial
        Label(self.commandsFrame, text="Comando Inicial:").grid(row=0,sticky="NE")
        self.startCommand = Text(self.commandsFrame, height=5, width=28)
        self.startCommand.grid(row=0,column=1)
        if 'startCommand' in self.prefDefaults:
            self.startCommand.insert(1.0, self.prefDefaults['startCommand'])
    
        # Comando final
        Label(self.commandsFrame, text="Comando Final:").grid(row=1,sticky="NE")
        self.finalCommand = Text(self.commandsFrame, height=5, width=28)
        self.finalCommand.grid(row=1,column=1)
        if 'finalCommand' in self.prefDefaults:
            self.finalCommand.insert(1.0, self.prefDefaults['finalCommand'])
    
    def apply(self):
        print("OK")
        # print(self.startCommand.get(1.0,"end-1c"))
        results = {
            'hostname'      : self.hostnameEntry.get(),
            'ip'            : self.ipAddr.get(),
            'mask'          : self.mask.get(),
            'defaultRoute'  : self.defaultGW.get(),
            "startCommand"  : self.startCommand.get(1.0,"end-1c"),
            "finalCommand"  : self.finalCommand.get(1.0,"end-1c")
        }
        self.result = results

    def cancelAction(self):
        print("fdfsdfdfsd")
        result = None
        
class Application(Frame):

    # NOTAS: 
    #   Popup para os hosts, sw, routers
    #   Criar tooltips para os botoes -> linha 99

    def __init__(self,parent=None, cheight=900 , cwidth=1000):
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

        self.ultimo = None

        self.widgetToItem = {}
        self.itemToWidget = {}

        # Ultimo e penultimo item selecionado
        self.ultimaSelecao = None
        self.selecaoAtual = None

        self.createMenubar()

        # Links
        self.link = self.linkWidget = None
        self.linkx = self.linky = self.linkItem = None
        self.links = {}


        # Toolbar -> barra lateral dos equipamentos
        self.ativo = None
        self.imagens = imagens()
        self.tools = ('Select','Switch','Host', 'Router','NetLink', "Start", "Stop")
        self.buttons = {}
        self.toolbar = self.createToolbar()


        # Coloca o canvas e o toolbox na janela
        self.toolbar.grid( column=0, row=0, sticky='nsew')
        self.cframe.grid( column=1, row=0 )
        self.columnconfigure( 1, weight=1 )
        self.rowconfigure( 0, weight=1 )
        self.pack( expand=True, fill='both' )

        self.nodeBindings = self.createNodeBindings()

        # Bindings do teclado
        self.bind( '<KeyPress-Delete>', self.excluiSelecao )
        self.bind( '<Control-q>', lambda event: self.quit() )
        self.focus()

        # Informações dos nodes
        self.hostOpts = {}
        self.switchOpts = {}
        self.routerOpts = {}

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
                
    def ativaBotao(self,botao):
        # Se algum botão já foi selecionado, coloca o mesmo na posição "levantado"
        if self.ativo:
            self.buttons[self.ativo].configure(relief='raised')
        
        # "Afunda" ou "clica o botão selecionado"
        self.buttons[botao].configure(relief='sunken')
        self.ativo = botao
        if botao == 'Start':
            self.startScenario()
        if botao == "Stop":
            self.stopScenario()
        
        

    def startScenario(self):
        topology = {
            'scene':{
                'hosts':[],
                'switchs':[],
                'links':[]
            },
            'test' :[]
        }
        for widget in self.widgetToItem:
            name = widget['text']
            tags = self.canvas.gettags(self.widgetToItem[widget])
            if 'Router' in tags:
                opts = self.routerOpts[name]
                host = {}
                host['type'] = "router"
                host['label'] = name
                host['dns'] = opts['dns']
                host['iface'] = []
                rules = opts['rules'].split('\n')
                host['rules'] = rules
                for link in opts['links']:
                    # print (opts['links'][link])
                    interface = {}
                    interface['ip'] = opts['links'][link].get('ip','')
                    interface['mask'] = opts['links'][link].get('mask','')
                    interface['gw'] = opts['links'][link].get('gw','')
                    host['iface'].append(interface)
                topology['scene']['hosts'].append(host)

            elif 'Host' in tags:
                opts = self.hostOpts[name]
                host = {}
                host['type'] = 'host'
                host['label'] = name
                host['dns'] = opts.get('dns','')
                host['iface'] = []
                host['startCommand'] = opts.get('startCommand','')
                host['finalCommand'] = opts.get('finalCommand','')
                host['iface'].append({
                    'ip': opts.get('ip',''),
                    'mask': opts.get('mask',''),
                    'gw': opts.get('gw','')
                })
                topology['scene']['hosts'].append(host)

            elif 'Switch'in tags:
                topology['scene']['switchs'].append({
                    'label': name
                })


        for link in self.links:
            source_link = self.links[link]['src']['text']
            dest_link = self.links[link]['dest']['text']
            link = {
                'label': "{}_{}".format(source_link,dest_link),
                'to': source_link,
                'from': dest_link 
            }
            topology['scene']['links'].append(link)
        print(json.dumps(topology))
        arq = open("cenario","w")
        arq.write(json.dumps(topology))

    def stopScenario(self):
        print("Parando cenário")
        

    def createNodeBindings(self):
        bindings = {
            # '<Double-Button-1>': self.duploclick,
            '<ButtonPress-1>': self.clickNode,
            '<B1-Motion>': self.dragNode,
            '<ButtonRelease-1>': self.releaseNode,
            '<Enter>': self.enterNode,
            '<Leave>': self.leaveNode,
        }

        l = Label()
        for event,binding in bindings.items():
            l.bind(event,binding)
        
        return l

    def duploclick(self,event):
        print(event)

    def startLink(self,event):
        # Caso não clique em um widget retorne 
        if event.widget not in self.widgetToItem:
            return
        
        w = event.widget
        item = self.widgetToItem[w]

        x,y = self.canvas.coords(item)

        self.link = self.canvas.create_line(x,y,x,y,width=4,fill='blue', tag='link')
        self.linkx = x
        self.linky = y
        self.linkWidget = w
        self.linkItem = item

    def dragNetLink(self,event):
        # Permite que o link seja arrastado
        if self.link is None:
            return
        x = self.canvasx(event.x_root)           
        y = self.canvasy(event.y_root)

        self.canvas.coords(self.link,self.linkx,self.linky,x,y)

    def releaseNetLink(self,_event):
        if self.link != None:
            self.canvas.delete(self.link)
        self.linkWidget = None
        self.link = None
        self.linkItem = None

    def finishLink(self,event):
        # Termina o link

        #Retorna caso não exista link
        if self.link == None:
            return

        # Pega o widget onde o link iniciou
        source = self.linkWidget
        c = self.canvas

        # Retorna a posição X,Y clicada pelo user e verifica se existe um item
        # no local clicado
        x,y = self.canvasx(event.x_root),self.canvasy(event.y_root)
        target = self.findItem(x,y)
        dest = self.itemToWidget.get(target,None)

        # Verifica se origem e destino não são vazios, se não são o msm widget
        # ou se já existe um link entre o destino e origem

        if( source is None or dest is None or source == dest or
            dest in source.links or source in dest.links) :
            self.releaseNetLink(event)
            return

        tags_origem = self.canvas.gettags(self.widgetToItem[source])
        tags_destino = self.canvas.gettags(target)

        # Não deixa o link entre 2 hosts
        if("Host" in tags_origem and "Host" in tags_destino):
            self.releaseNetLink(event)
            return
        
        # Cria os bindings pro link
        linkType = 'data'
        self.createDataLinkBindings()
        c.itemconfig(self.link, tags=c.gettags(self.link)+(linkType,))

        x,y = c.coords(target)

        c.coords(self.link, self.linkx,self.linky,x,y)
        self.addLink(source,dest,linkType=linkType)
        self.link = self.linkWidget = None

    
    def addLink(self,source,dest,linkType='data', linkopts=None):
        if linkopts == None:
            linkopts = {}
        source.links[dest]   = self.link
        dest.links[source] = self.link
        self.links[self.link] = {
            'type'     : linkType,
            'src'      : source,
            'dest'     : dest,
            'linkopts' : linkopts
        }
    


    # Cria os bindings para os links
    def createDataLinkBindings(self):
        def select(_event, link=self.link):
            self.selecionarItem(link)

        def highlight(_event, link=self.link):
            self.selecionarItem( link )
            self.canvas.itemconfig( link, fill='green' ) 

        def unhighlight(_event, link=self.link):
            self.canvas.itemconfig( link, fill='blue' ) 

        self.canvas.tag_bind(self.link, '<Enter>', highlight)
        self.canvas.tag_bind(self.link, '<Leave>', unhighlight)
        self.canvas.tag_bind(self.link, '<ButtonPress-1>', select)
        # self.canvas.tag_bind(self.link, '<Button-3>', highlight)


    def clickNode(self,event):
        if self.ativo == 'NetLink':
            self.startLink(event)
        else: 
            self.selecionaNode(event)
    
    def dragNode(self,event):
        if self.ativo == 'NetLink':
            # Cria a ligação dos links
            self.dragNetLink(event)
        else:
            self.arrastarNodeCanvas(event)
    
    def releaseNode(self,event):
        if self.ativo == 'NetLink':
            self.finishLink(event)
    
    def enterNode(self,event):
        if self.ultimo != "enter":
            self.ultimo = 'enter'
    
    def leaveNode(self,event):
        if self.ultimo != "leave":
            self.ultimo = 'leave'
    
    def excluiSelecao(self,_event):
        if self.selecaoAtual != None:
            self.excluiItem(self.selecaoAtual)

    def excluiItem(self,item):

        if item in self.links:
            self.deleteLink(item)

        if item in self.itemToWidget:
            self.deleteNode(item)
            
        
        self.canvas.delete(item)
    
    def deleteNode (self,item):
        widget = self.itemToWidget[item]
        tags = self.canvas.gettags(item)
        
        for link in list(widget.links.values()):
            self.excluiItem(link)
        del self.itemToWidget[item]
        del self.widgetToItem[widget]

    def deleteLinkRouter(self,src,dest):
        routerName = src['text']
        hostName = dest['text']
        if hostName in self.routerOpts[routerName]['links']:
            del self.routerOpts[routerName]['links'][hostName]
        print(self.routerOpts[routerName])

    def deleteLink(self,link):
        par = self.links.get(link,None)
        itemSrc = self.widgetToItem[par['src']]
        itemDest = self.widgetToItem[par['dest']]
        tagsSrc = self.canvas.gettags(itemSrc)
        tagsDest = self.canvas.gettags(itemDest)
        print(par['src'])
        print (tagsSrc,tagsDest)
        if par:
            if 'Router' in tagsSrc:
                self.deleteLinkRouter(par['src'],par['dest'])

            if 'Router' in tagsDest:
                self.deleteLinkRouter(par['dest'],par['src'])

            # if 'Host' in tagsSrc:
            #     print('hostSrc')
            # if 'Host' in tagsDest:
            #     print('hostDest')
            #PRECISO REMOVER NO ROUTEROPTS
            origem = par['src']
            destino = par['dest']
            del origem.links[destino]
            del destino.links[origem]
        
        if link:
            del self.links[link]
    
    def selecionaNode(self,event):
        item = self.widgetToItem.get(event.widget,None)
        self.selecionarItem(item)

    # Possibilita arrastar o nó no canvas
    def arrastarNodeCanvas(self,event):
        c = self.canvas

        x = self.canvasx(event.x_root)
        y = self.canvasy(event.y_root)

        item = self.widgetToItem[event.widget]

        c.coords(item,x,y)

        w = event.widget

        for dest in w.links:
            link = w.links[ dest ]
            item = self.widgetToItem[ dest ]
            x1, y1 = c.coords( item )
            c.coords( link, x, y, x1, y1 )
        # self.updateScrollRegion()

    def findItem( self, x, y ):
        "Find items at a location in our canvas."
        items = self.canvas.find_overlapping( x, y, x, y )
        if len( items ) == 0:
            return None
        else:
            return items[ 0 ]


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
            self.hostOpts[nomeNo] = {'nodeNum':self.Host_num}
            self.hostOpts[nomeNo]['hostname'] = nomeNo
        elif node == "Router":
            self.Router_num += 1
            nomeNo += str(self.Router_num)
            self.routerOpts[nomeNo] = {'nodeNum': self.Router_num}
            self.routerOpts[nomeNo]['hostname'] = nomeNo
            self.routerOpts[nomeNo]['dns'] = ''
            self.routerOpts[nomeNo]['links'] = {}
            self.routerOpts[nomeNo]['rules'] = ''
            print("Add router " + nomeNo)

        icone = self.nodeIcone(node,nomeNo)
        item = self.canvas.create_window(x,y, anchor='c', window=icone, tags=node)
        self.selecionarItem(item)
        self.widgetToItem[ icone ] = item
        self.itemToWidget[ item ] = icone
        icone.links = {}

        if node == "Switch":
            icone.bind('<Double-Button-1>',self.switchDetails)
        elif node == "Router":
            icone.bind('<Double-Button-1>',self.routerDetails)
        elif node == "Host":
            icone.bind('<Double-Button-1>',self.hostDetails)

    # Cria um novo item para ser colocado no Canvas
    def nodeIcone(self,node,name):
        icone = Button(self.canvas, image=self.imagens[node], text=name, compound='top')
        bindtags = [str(self.nodeBindings)]
        bindtags += list(icone.bindtags())

        icone.bindtags(tuple(bindtags))
        return icone

    # Seleciona o item e guarda a ultima seleção
    def selecionarItem(self,item):
        self.ultimaSelecao = self.selecaoAtual
        self.selecaoAtual = item

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
        fileMenu.add_separator()
        fileMenu.add_command( label='Quit')
    
    def hostDetails(self,event):
        # if( self.selecaoAtual == None or
        #     self.selecaoAtual not in self.itemToWidget):
        #     return
        widget = self.itemToWidget.get(self.selecaoAtual,None)
        if widget == None:
            return
        name = widget['text']
        tags = self.canvas.gettags(self.selecaoAtual)
        if 'Host' not in tags:
            return
        prefDefaults = self.hostOpts[name]
        
        hostBox = HostDialog(self, title='Detalhes Host ' + name, prefDefaults=prefDefaults)
        self.master.wait_window(hostBox.top)
        
        if hostBox.result:
            print(hostBox.result)
            newName = hostBox.result['hostname']
            widget['text'] = newName
            self.hostOpts[newName] = hostBox.result
            if newName != name:
                del self.hostOpts[name]

    def routerDetails(self,event):
        # if self.selecaoAtual not in self.itemToWidget:
        #     return
        widget = self.itemToWidget.get(self.selecaoAtual,None)
        if widget == None:
            return
        name = widget['text']
        tags = self.canvas.gettags(self.selecaoAtual)
        if 'Router' not in tags:
            return
        prefDefaults = self.routerOpts[name]
        links = []
        for link in list(widget.links):
            nome = link['text']
            links.append(nome)
        routerBox = RouterDialog(self,title='Detalhes Router ' + name, prefDefaults=prefDefaults,links=links)
        self.master.wait_window(routerBox.top)
        
        if routerBox.result:
            print(routerBox.result)
            newName = routerBox.result['hostname']
            widget['text'] = newName
            self.routerOpts[newName] = routerBox.result
            if newName != name:
                del self.routerOpts[name]
            


        # print(widget,name,tags, prefDefaults)
        
        
    
    def switchDetails(self,event):
        print("Propriedades SW")
        

def imagens():
    return {
        'Switch': PhotoImage(file="{}sw.png".format(IMAGE_PATH)),
        'Host': PhotoImage(file="{}pc.png".format(IMAGE_PATH)),
        'Router': PhotoImage(file="{}router.png".format(IMAGE_PATH)),
        'NetLink': PhotoImage(file="{}netlink.png".format(IMAGE_PATH)),
        'Start': PhotoImage(file="{}play.png".format(IMAGE_PATH)),
        'Stop': PhotoImage(file="{}stop.png".format(IMAGE_PATH)),
        'Select': BitmapImage(
            file='/usr/include/X11/bitmaps/left_ptr' ),
        
    }

def main():

    app = Application()
    app.mainloop()



if __name__ == '__main__':
    main()
