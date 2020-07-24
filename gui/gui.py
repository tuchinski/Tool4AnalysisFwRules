# -*- coding: utf-8 -*-

from tkinter import BitmapImage, Button, Canvas, Entry, Frame, Label, Menu, PhotoImage, Scrollbar, Text, Tk, Toplevel, Wm

from tkinter import filedialog as tkFileDialog
from PIL import Image
from tkinter.ttk import Notebook, Combobox
import json
import os
from threading import Thread
from tkinter.messagebox import showinfo
import uuid

class Th(Thread):
    def __init__(self, num):
        Thread.__init__(self)
        self.num = num

    def run(self):
        print("hello thread")
        print(os.getpid())
        a = os.system("sudo xfce4-terminal -x python ../src/customTopo.py cenario")
        print(a)
        

## pesquisar interface
APP_TITLE = "Teste Regras Firewall"
APP_XPOS = 200
APP_YPOS = 200
APP_WIDTH = 300
APP_HEIGHT = 200

IMAGE_PATH = "images/"



class CustomDialog(object):
    def __init__(self, master, _title,geometry='800x500'):
        self.top = Toplevel(master)
        # Toplevel.__init__(self,master)
        self.top.transient(master)

        if _title:
            self.top.title(_title)
        widthXheight = geometry.split('x')
        bodyW = widthXheight[0]
        bodyH = widthXheight[1]

        self.bodyFrame = Frame(self.top,width=bodyW, height=bodyH)
        self.bodyFrame.grid(row=0, column=0, sticky='nswe')
        
        self.top.parent = master
        self.top.geometry(geometry)

        self.body(self.bodyFrame)

        buttonFrame = Frame(self.top, relief='ridge', bd=3, bg='lightgrey',width=500, height=500)
        buttonFrame.grid(row=1,column=0, sticky='nswe')

        okButton = Button(buttonFrame, width=8, text='OK', relief='groove', bd=4, command=self.okAction)
        okButton.grid(row=0, column=0, sticky='E')

        cancelButton = Button(buttonFrame, width=8, text='Cancelar', relief='groove', bd=4, command=self.cancelAction)
        cancelButton.grid(row=0, column=1, sticky='W')
        self.countRule = 1

        # self.top.geometry("+%d+%d" % (master.winfo_rootx()+50,master.winfo_rooty()+50))
        # self.top.geometry("+50+50")
        self.top.protocol("WM_DELETE_WINDOW", self.cancelAction)

        self.top.wait_window(self.top)
    
    def body(self,master):
        self.rootFrame = master
    
    def apply(self):
        self.top.destroy()

    def okAction(self):
        self.apply()
        self.top.destroy()

    def cancelAction(self):
        print("Cancel action")
        self.top.destroy()
    
    def verifyIP(self,event):
        entryIP = event.widget.get()
        # print(iface_mask_widget)
        if len(entryIP) == 0:
            return

        # Separa a string pelos "."
        octetos = entryIP.split('.')
        
        # Verifica se existem 4 octetos
        if(len(octetos) != 4):
            event.widget.delete(0,'end')
            self.popup("Erro", "Erro! IP não é válido!")
            return
        for octeto in octetos:
            # Verifica se nenhum caracter foi digitado
            if octeto.isnumeric() == False:
                self.popup("Erro", "Erro! Inserir apenas números")
                event.widget.delete(0,'end')
                return
            
            # Verifica o range do IP
            if (int(octeto) < 0) or (int(octeto) > 255):
                self.popup("Erro", "Erro! IP não é válido!")
                event.widget.delete(0,'end')
                return
        return octetos

    def verifyIPwithMask(self,event,iface_mask_widget):
        
        octetos = self.verifyIP(event)
        if octetos == None:
            return
        iface_mask_widget.delete(0,'end')
        first_octet = int(octetos[0])
        if(first_octet < 127):
            # Classe A
            mask = '255.0.0.0'
            iface_mask_widget.insert(0,mask)
            
        elif(first_octet < 191):
            # Classe B
            mask = '255.255.0.0'
            iface_mask_widget.insert(0,mask)
            
        else:
            # Classe C
            mask = '255.255.255.0'
            iface_mask_widget.insert(0,mask)

    def popup(self,titulo,mensagem):
        win = Toplevel(width=500,height=500)
        win.wm_title(titulo)
    
        l = Label(win, text=mensagem)
        l.grid(row=0, column=0)
    
        b = Button(win, text="OK", command=win.destroy)
        b.grid(row=1, column=0)

    def verifyMask(self,event):
        mask = event.widget.get()      
        if len(mask) == 0:
            return     
        octetos = mask.split('.')

        if(len(octetos) != 4):
            event.widget.delete(0,'end')
            self.popup("Erro", 'Erro! Máscara não é válida!')
            return

        isZero = False


        #imnort ipaddress
        #VERIFICAR TESTE 255.255.255.1
        for octeto in octetos:
            if octeto.isnumeric() == False:
                self.popup("Erro", "Erro! Inserir apenas números na máscara")
                event.widget.delete(0,'end')
                return    
            octeto_bin = bin(int(octeto))
            for i in range(2,len(octeto_bin)):
                if octeto_bin[i] == '1' and isZero == True:
                    self.popup("Erro", "ERRO: Máscara Inválida")
                    print()
                    event.widget.delete(0,'end')
                    return

                if octeto_bin[i] == '0':
                    isZero = True


class TestesDialog(CustomDialog):
    def __init__(self, master ,tests):
        self.title = "Testes das Regras de Firewall"
        self.tests =  tests
        self.fieldsTest = {}

        CustomDialog.__init__(self,master,self.title,'1150x700')

    def body(self,master):
        self.rootFrame = master
        self.rootFrame.widgetName = self.title
        routerWidth = 1140
        routerHeight = 630
        n = Notebook(self.rootFrame,width=routerWidth, height=routerHeight)
        self.testFrame = Frame(n)
        n.add(self.testFrame, text="Testes")
        n.pack()
        

        buttonAddRule = Button(self.testFrame, text="Adicionar novo teste", command=self.addNewTest)
        buttonAddRule.grid(row=0, column=0,columnspan=2, padx=1)
        self.testPosition = 0

        # print(firewall_tests)
        for test in self.tests:
            print(test)
            self.addNewTest(test)

    def addNewTest(self,currentTest=None):
        print("Add novo teste")
        
        test = {}
        test['labelTest'] = Label(self.testFrame,text="TESTE {}".format(self.testPosition+1),relief='solid')
        test['labelTest'].grid(row=self.testPosition + 1, column=0,sticky='ww')
        
        test['labelIpSrc'] = Label(self.testFrame,text="Ip Origem:")
        test['labelIpSrc'].grid(row=self.testPosition + 1, column=1, sticky="W")
        
        test['srcIP'] = Entry(self.testFrame,width=14)
        test['srcIP'].grid(row=self.testPosition+1, column=2)
        if currentTest != None:
            # print('oioi',currentTest)
            test['srcIP'].insert(0,currentTest['srcIP'])

        test['labelIpDest'] = Label(self.testFrame,text="Ip Destino:")
        test['labelIpDest'].grid(row=self.testPosition + 1, column=3, sticky="W")

        test['destIP'] = Entry(self.testFrame,width=14)
        test['destIP'].grid(row=self.testPosition+1, column=4)
        if currentTest != None:
            test['destIP'].insert(0,currentTest['destIP'])


        test['labelProtocol'] = Label(self.testFrame,text="Protocolo:")
        test['labelProtocol'].grid(row=self.testPosition + 1, column=5, sticky="W")

        test['comboBoxProtocolo'] = Combobox(self.testFrame, width=5, values=['TCP','UDP', 'ICMP'])
        test['comboBoxProtocolo'].grid(row=self.testPosition+1, column=6)
        if currentTest != None:
            test['comboBoxProtocolo'].set(currentTest['comboBoxProtocolo'])
        else:
            test['comboBoxProtocolo'].current(0)

        test['labelSrcPort'] = Label(self.testFrame,text="Porta Origem:")
        test['labelSrcPort'].grid(row=self.testPosition + 1, column=7, sticky="W")

        test['srcPort'] = Entry(self.testFrame,width=5)
        test['srcPort'].grid(row=self.testPosition+1, column=8)
        if currentTest != None:
            test['srcPort'].insert(0,currentTest['srcPort'])

        test['labelDestPort'] = Label(self.testFrame,text="Porta Destino:")
        test['labelDestPort'].grid(row=self.testPosition + 1, column=9, sticky="W")

        test['destPort'] = Entry(self.testFrame,width=5)
        test['destPort'].grid(row=self.testPosition+1, column=10)
        if currentTest != None:
            test['destPort'].insert(0,currentTest['destPort'])

        test['labelResult'] = Label(self.testFrame,text="Resultado:")
        test['labelResult'].grid(row=self.testPosition + 1, column=11, sticky="W")
        test['comboBoxResult'] = Combobox(self.testFrame, width=8, values=['ACEITAR', 'NEGAR'])
        test['comboBoxResult'].grid(row=self.testPosition+1, column=12)
        if currentTest != None:
            test['comboBoxResult'].set(currentTest['comboBoxResult'])
        else:
            test['comboBoxResult'].current(0)

        test['id'] = uuid.uuid1()

        test['buttonDeleteTest'] = Button(self.testFrame,text="X",command=lambda n=test['id']: self.deleteTest(n))
        test['buttonDeleteTest'].grid(row=self.testPosition + 1, column=13, sticky="E")

        self.fieldsTest[test['id']] = test
        
        self.testPosition += 1

    def deleteTest(self,index):
        # index = index-1
        print(index)
        print(self.fieldsTest[index]['srcPort'])
        self.fieldsTest[index]['labelTest'].destroy()
        self.fieldsTest[index]['labelIpSrc'].destroy()
        self.fieldsTest[index]['srcIP'].destroy()
        self.fieldsTest[index]['labelIpDest'].destroy()
        self.fieldsTest[index]['destIP'].destroy()
        self.fieldsTest[index]['labelProtocol'].destroy()
        self.fieldsTest[index]['comboBoxProtocolo'].destroy()
        self.fieldsTest[index]['labelSrcPort'].destroy()
        self.fieldsTest[index]['srcPort'].destroy()
        self.fieldsTest[index]['labelDestPort'].destroy()
        self.fieldsTest[index]['destPort'].destroy()
        self.fieldsTest[index]['labelResult'].destroy()
        self.fieldsTest[index]['comboBoxResult'].destroy()
        self.fieldsTest[index]['buttonDeleteTest'].destroy()
        # for i in range(index+1,len(self.fieldsTest)):
        #     self.fieldsTest[i]['labelTest']['text'] = "TESTE {}".format(i)
        # self.testPosition -= 1
            
        del self.fieldsTest[index]
        # print(self.fieldsTest)

    def cancelAction(self):
        self.result = self.tests
        return super().cancelAction()

    def apply(self):
        self.result = []
        for test in self.fieldsTest:
            print(test)
            currentTest = {}
            currentTest['srcIP'] = self.fieldsTest[test]['srcIP'].get()
            currentTest['destIP'] = self.fieldsTest[test]['destIP'].get()
            currentTest['comboBoxProtocolo'] = self.fieldsTest[test]['comboBoxProtocolo'].get()
            currentTest['srcPort'] = self.fieldsTest[test]['srcPort'].get()
            currentTest['destPort'] = self.fieldsTest[test]['destPort'].get()
            currentTest['comboBoxResult'] = self.fieldsTest[test]['comboBoxResult'].get()
            self.result.append(currentTest)
        # print(firewall_tests)
        firewall_tests = self.result
        # super().apply()


class RouterDialog(CustomDialog):
    def __init__(self, master,title,prefDefaults,links):
        self.prefDefaults = prefDefaults
        self.result = None
        self.links = links
        self.fieldsTest = {}
        self.buttonsDeleteTests = []

        CustomDialog.__init__(self,master,title,'1150x700')
    
    
    def body(self, master):
        routerWidth = 1140
        routerHeight = 630
        self.rootFrame = master
        self.rootFrame.widgetName = self.prefDefaults['hostname']
        n = Notebook(self.rootFrame,width=routerWidth, height=routerHeight)
        self.netPropertiesFrame = Frame(n)
        self.firewallFrame = Frame(n)
        self.testFrame = Frame(n)
        n.add(self.netPropertiesFrame, text="Propriedades Rede")
        n.add(self.firewallFrame, text="Firewall")
        # n.add(self.testFrame, text="Testes")
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
        
        self.dns.bind("<FocusOut>",self.verifyIP)
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
            
            # cmd_botao = lambda t=tool : self.ativaBotao(t)

            self.confLinks[link]['ip'].bind("<FocusOut>",lambda event, entry_mask=self.confLinks[link]['mask'] : self.verifyIPwithMask(event,entry_mask) )
            self.confLinks[link]['mask'].bind("<FocusOut>",self.verifyMask)
            self.confLinks[link]['gw'].bind("<FocusOut>",self.verifyIP)
            
            # Espaço em branco
            Label(self.netPropertiesFrame, text="  ").grid(row=i,sticky='E')
            i+=1
        
        """ Aba 2: Firewall """

        Label(self.firewallFrame, text="Regras (1 regra por linha):").grid(row=0,sticky="NW")
        self.rules = Text(self.firewallFrame, height=50, width=130)
        self.rules.grid(row=1,column=0)
        if 'rules' in self.prefDefaults:
            self.rules.insert(1.0, self.prefDefaults['rules'])

        """Aba 3: Testes"""
        buttonAddRule = Button(self.testFrame, text="Adicionar novo teste", command=self.addNewRule)
        buttonAddRule.grid(row=0, column=0,columnspan=2, padx=1)
        self.testPosition = 0

        for test in self.prefDefaults['tests']:
            print(test['srcIP'])
            self.addNewRule(test)
        
    def addNewRule(self,currentTest=None):
        print("Add novo teste")
        
        test = {}
        test['labelTest'] = Label(self.testFrame,text="TESTE {}".format(self.testPosition+1),relief='solid')
        test['labelTest'].grid(row=self.testPosition + 1, column=0,sticky='ww')
        
        test['labelIpSrc'] = Label(self.testFrame,text="Ip Origem:")
        test['labelIpSrc'].grid(row=self.testPosition + 1, column=1, sticky="W")
        
        test['srcIP'] = Entry(self.testFrame,width=14)
        test['srcIP'].grid(row=self.testPosition+1, column=2)
        if currentTest != None:
            test['srcIP'].insert(0,currentTest['srcIP'])

        test['labelIpDest'] = Label(self.testFrame,text="Ip Destino:")
        test['labelIpDest'].grid(row=self.testPosition + 1, column=3, sticky="W")

        test['destIP'] = Entry(self.testFrame,width=14)
        test['destIP'].grid(row=self.testPosition+1, column=4)
        if currentTest != None:
            test['destIP'].insert(0,currentTest['destIP'])


        test['labelProtocol'] = Label(self.testFrame,text="Protocolo:")
        test['labelProtocol'].grid(row=self.testPosition + 1, column=5, sticky="W")

        test['comboBoxProtocolo'] = Combobox(self.testFrame, width=5, values=['TCP','UDP', 'ICMP'])
        test['comboBoxProtocolo'].grid(row=self.testPosition+1, column=6)
        if currentTest != None:
            test['comboBoxProtocolo'].set(currentTest['comboBoxProtocolo'])
        else:
            test['comboBoxProtocolo'].current(0)

        test['labelSrcPort'] = Label(self.testFrame,text="Porta Origem:")
        test['labelSrcPort'].grid(row=self.testPosition + 1, column=7, sticky="W")

        test['srcPort'] = Entry(self.testFrame,width=5)
        test['srcPort'].grid(row=self.testPosition+1, column=8)
        if currentTest != None:
            test['srcPort'].insert(0,currentTest['srcPort'])

        test['labelDestPort'] = Label(self.testFrame,text="Porta Destino:")
        test['labelDestPort'].grid(row=self.testPosition + 1, column=9, sticky="W")

        test['destPort'] = Entry(self.testFrame,width=5)
        test['destPort'].grid(row=self.testPosition+1, column=10)
        if currentTest != None:
            test['destPort'].insert(0,currentTest['destPort'])

        test['labelResult'] = Label(self.testFrame,text="Resultado:")
        test['labelResult'].grid(row=self.testPosition + 1, column=11, sticky="W")
        test['comboBoxResult'] = Combobox(self.testFrame, width=8, values=['ACEITAR', 'NEGAR'])
        test['comboBoxResult'].grid(row=self.testPosition+1, column=12)
        if currentTest != None:
            test['comboBoxResult'].set(currentTest['comboBoxResult'])
        else:
            test['comboBoxResult'].current(0)

        test['id'] = uuid.uuid1()

        test['buttonDeleteTest'] = Button(self.testFrame,text="X",command=lambda n=test['id']: self.deleteTest(n))
        test['buttonDeleteTest'].grid(row=self.testPosition + 1, column=13, sticky="E")

        self.fieldsTest[test['id']] = test
        
        self.testPosition += 1

    def deleteTest(self,index):
        # index = index-1
        print(index)
        print(self.fieldsTest[index]['srcPort'])
        self.fieldsTest[index]['labelTest'].destroy()
        self.fieldsTest[index]['labelIpSrc'].destroy()
        self.fieldsTest[index]['srcIP'].destroy()
        self.fieldsTest[index]['labelIpDest'].destroy()
        self.fieldsTest[index]['destIP'].destroy()
        self.fieldsTest[index]['labelProtocol'].destroy()
        self.fieldsTest[index]['comboBoxProtocolo'].destroy()
        self.fieldsTest[index]['labelSrcPort'].destroy()
        self.fieldsTest[index]['srcPort'].destroy()
        self.fieldsTest[index]['labelDestPort'].destroy()
        self.fieldsTest[index]['destPort'].destroy()
        self.fieldsTest[index]['labelResult'].destroy()
        self.fieldsTest[index]['comboBoxResult'].destroy()
        self.fieldsTest[index]['buttonDeleteTest'].destroy()
        # for i in range(index+1,len(self.fieldsTest)):
        #     self.fieldsTest[i]['labelTest']['text'] = "TESTE {}".format(i)
        # self.testPosition -= 1
            
        del self.fieldsTest[index]
        # print(self.fieldsTest)

    def cancelAction(self):
        return super().cancelAction()

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
        self.result['tests'] = []
        for test in self.fieldsTest:
            print(test)
            currentTest = {}
            currentTest['srcIP'] = self.fieldsTest[test]['srcIP'].get()
            currentTest['destIP'] = self.fieldsTest[test]['destIP'].get()
            currentTest['comboBoxProtocolo'] = self.fieldsTest[test]['comboBoxProtocolo'].get()
            currentTest['srcPort'] = self.fieldsTest[test]['srcPort'].get()
            currentTest['destPort'] = self.fieldsTest[test]['destPort'].get()
            currentTest['comboBoxResult'] = self.fieldsTest[test]['comboBoxResult'].get()
            self.result['tests'].append(currentTest)


class HostDialog(CustomDialog):
    def __init__(self, master, title, prefDefaults):
        self.prefDefaults = prefDefaults
        self.result = None

        CustomDialog.__init__(self,master,title,'800x600')
    
    def body(self,master):
        hostWidth = 790
        hostHeight = 525
        self.rootFrame = master
        n = Notebook(self.rootFrame, width = hostWidth, height = hostHeight)
        self.propertiesFrame = Frame(n)
        self.firewallFrame = Frame(n)
        self.commandsFrame = Frame(n)
        n.add(self.propertiesFrame, text="Propriedades")
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
            self.ipAddr.insert(0, self.prefDefaults['ip'])

        # Máscara de rede
        Label(self.propertiesFrame, text="Máscara de rede:").grid(row=2,sticky="E")
        self.mask = Entry(self.propertiesFrame, width=25)
        self.mask.grid(row=2,column=1)
        if 'mask' in self.prefDefaults:
            self.mask.insert(0, self.prefDefaults['mask'])

        # Rota Padrão
        Label(self.propertiesFrame, text="Rota Padrão:").grid(row=3,sticky="E")
        self.defaultGW = Entry(self.propertiesFrame, width=25)
        self.defaultGW.grid(row=3,column=1)
        if 'defaultRoute' in self.prefDefaults:
            self.defaultGW.insert(0, self.prefDefaults['defaultRoute'])

        
        """ Aba 3: Comandos"""
        # Comando inicial
        Label(self.commandsFrame, text="Comando Inicial:").grid(row=0,sticky="NE")
        self.startCommand = Text(self.commandsFrame, height=15, width=80)
        self.startCommand.grid(row=0,column=1)
        if 'startCommand' in self.prefDefaults:
            self.startCommand.insert(1.0, self.prefDefaults['startCommand'])
    
        # Comando final
        Label(self.commandsFrame, text="Comando Final:").grid(row=1,sticky="NE")
        self.finalCommand = Text(self.commandsFrame, height=15, width=80)
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
        return super().cancelAction()
        
class Application(Frame):

    # NOTAS: 
    #   Popup para os hosts, sw, routers
    #   Criar tooltips para os botoes -> linha 99

    def __init__(self,parent=None, cheight=900 , cwidth=1000):
        # self.master = master
        # self.master.protocol("WM_DELETE_WINDOW", self.close)
        Frame.__init__(self,parent,width=1000,height=1000)
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
        # Testes das regras de firewall
        self.firewallTests = []

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
        self.bind( '<Key>', self.keyPressed )
        self.focus()

        # Informações dos nodes
        self.hostOpts = {}
        self.switchOpts = {}
        self.routerOpts = {}

        Wm.wm_protocol( self.top, name='WM_DELETE_WINDOW', func=self.quit )

    def keyPressed(self,event):
        key = event.char.lower()
        if key == 'r':
            self.ativaBotao('Router')
        elif key == 's':
            self.ativaBotao('Switch')
        elif key == 'h':
            self.ativaBotao('Host')
        elif key == 'm':
            self.ativaBotao('Select')
        elif key == 'n':
            self.ativaBotao('NetLink')




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
                b.config(height=75, width=100, image=self.imagens[tool])
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

        glossary_result = {
            'ACEITAR': 'accept',
            'NEGAR': 'deny'
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

        for test in self.firewallTests:
            currentTest = {}
            currentTest['sourceIP'] = test['srcIP']
            currentTest['destIP'] = test['destIP']
            currentTest['protocol'] = test['comboBoxProtocolo'].lower()
            if currentTest['protocol'] == 'icmp':
                currentTest['sPort'] = '*'
                currentTest['dPort'] = '*'
            else:
                currentTest['sPort'] = test['srcPort']
                currentTest['dPort'] = test['destPort']

            currentTest['expected'] = glossary_result[test['comboBoxResult']]
            topology['test'].append(currentTest)

        print(json.dumps(topology))
        arq = open("cenario","w")
        arq.write(json.dumps(topology))
        arq.close()
        thread_run = Th(1)
        thread_run.start()

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
        self.novoNode("Router", event,None,None,None)

    def clickSwitch(self,event):
        self.novoNode("Switch", event)

    def clickHost(self,event):
        self.novoNode("Host", event)

    def novoNode(self,node,event=None,x=None,y=None,nomeNo=None):
        # Add um novo nó no canvas
        c = self.canvas
        if x == None:
            x = c.canvasx(event.x)
        
        if y == None:
            y = c.canvasy(event.y)

        if node == "Switch":
            if nomeNo == None:
                nomeNo = self.prefixos[node]
                self.Switch_num += 1
                nomeNo += str(self.Switch_num)
            print("Add Switch " + nomeNo)

        elif node == "Host":
            if nomeNo == None:
                nomeNo = self.prefixos[node]
                self.Host_num += 1
                nomeNo += str(self.Host_num)
            print("Add host " + nomeNo)
            self.hostOpts[nomeNo] = {'nodeNum':self.Host_num}
            self.hostOpts[nomeNo]['hostname'] = nomeNo

        elif node == "Router":
            if nomeNo == None:
                nomeNo = self.prefixos[node]
                self.Router_num += 1
                nomeNo += str(self.Router_num)
            self.routerOpts[nomeNo] = {'nodeNum': self.Router_num}
            self.routerOpts[nomeNo]['hostname'] = nomeNo
            self.routerOpts[nomeNo]['dns'] = ''
            self.routerOpts[nomeNo]['links'] = {}
            self.routerOpts[nomeNo]['rules'] = ''
            self.routerOpts[nomeNo]['tests'] = []
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

    def cria_testes(self):
        valor = TestesDialog(self,self.firewallTests)
        print('criatests',valor.result)
        self.firewallTests = valor.result

    # Cria um menuBar
    def createMenubar(self):    
        "Create our menu bar."
        mbar = Menu( self.top )
        self.top.configure( menu=mbar )


        fileMenu = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="Arquivos", menu=fileMenu )
        fileMenu.add_command( label="New Topology", command=self.newTopology)
        fileMenu.add_command( label="Load Topology", command=self.loadTopology)
        fileMenu.add_command( label="Save Topology", command=self.saveTopology)
        fileMenu.add_separator()
        fileMenu.add_command( label='Quit',command=self.quit)
        
        fileMenuTestes = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="Testes", menu=fileMenuTestes )
        # fileMenuTestes.add_command(label='Criar testes',command=TestesDialog)
        a = fileMenuTestes.add_command(label='Criar testes',command=self.cria_testes)
        print('firewall_tests',a)

    
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
        # self.master.wait_window(hostBox.top)
        
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
        # self.master.wait_window(routerBox.top)
        
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
    
    def saveTopology(self):
        formats = [
            ('Mininet Topology','*.mn'),
            ('All Files','*'),
        ]

        topology = {}
        hosts = []
        switchs = []
        routers = []
        fileName = tkFileDialog.asksaveasfilename(filetypes=formats ,title="Save the topology as...")

        # Salvando os hosts
        for widget in self.widgetToItem:
            name = widget['text']
            tags = self.canvas.gettags(self.widgetToItem[widget])
            x1,y1 = self.canvas.coords(self.widgetToItem[widget])
            if "Switch" in tags:
                nodeToSave = {
                    'x': str(x1),
                    'y': str(y1),
                    'name': name
                }
                switchs.append(nodeToSave)
            elif "Host" in tags:
                # nodeNum = self.hostOpts[name]['nodeNum']
                nodeToSave = {
                                  'x':str(x1),
                                  'y':str(y1),
                                  'opts':self.hostOpts[name] }
                hosts.append(nodeToSave)

            elif "Router" in tags:
                # nodeNum = self.routerOpts[name]['nodeNum']
                nodeToSave = {
                                  'x':str(x1),
                                  'y':str(y1),
                                  'opts':self.routerOpts[name] }
                routers.append(nodeToSave)

        topology['hosts'] = hosts    
        topology['switchs'] = switchs    
        topology['routers'] = routers
        topology['tests'] = self.firewallTests   

        # Salvando os links 
        links = []
        for link in self.links.values():
            src = link['src']
            dest = link['dest']

            srcName, dstName = src[ 'text' ], dest[ 'text' ]

            linkToSave = {'src':srcName,
                          'dest':dstName,
                        }
            if link['type'] == 'data':
                links.append(linkToSave)

        topology['links'] = links
        
        try:
            f = open(fileName,'w')
            f.write(json.dumps(topology, sort_keys=True, indent=4, separators=(',', ': ')))
        except Exception as error:
            print(error)
        finally:
            f.close()

        # print(json.dumps(topology))
            
    def loadTopology(self):
        c = self.canvas
        formats = [
            ('Mininet Topology','*.mn'),
            ('All Files','*'),
        ]

        f = tkFileDialog.askopenfile(filetypes=formats, mode='r')
        if f == None:
            return
        
        self.newTopology()
        loadedTopo = json.load(f)
        # Carregando os hosts
        hosts = loadedTopo['hosts']

        # Carrega os testes
        self.firewallTests = loadedTopo['tests']

        for host in hosts:
            hostname = host['opts']['hostname']
            x = host['x']
            y = host['y']
            self.novoNode("Host", None,float(x),float(y),hostname)
            self.hostOpts[hostname] = host['opts']
        
        # Carregando os roteadores
        routers = loadedTopo['routers']
        for router in routers:
            hostname = router['opts']['hostname']
            x = router['x']
            y = router['y']
            self.novoNode("Router", None, float(x),float(y), hostname)
            self.routerOpts[hostname] = router['opts']

        # Carregando os Switchs
        switchs = loadedTopo['switchs']
        for switch in switchs:
            hostname = switch['name']
            x = switch['x']
            y = switch['y']
            self.novoNode("Switch", None, float(x), float(y), hostname)

        # Carregando os links
        links = loadedTopo['links']
        for link in links:
            
            srcNode = link['src']
            src = self.findWidgetByName(srcNode)
            sx,sy = self.canvas.coords(self.widgetToItem[src])

            destNode = link['dest']
            dest = self.findWidgetByName(destNode)
            dx,dy = self.canvas.coords(self.widgetToItem[dest])

            self.link = self.canvas.create_line(sx,sy,dx,dy,width=4, fill='blue', tag='link')
            self.addLink(src,dest)
            self.createDataLinkBindings()
            self.link = self.widget = None
        
        f.close()

    def findWidgetByName( self, name ):
        for widget in self.widgetToItem:
            if name ==  widget[ 'text' ]:
                return widget

    def newTopology(self):
        for widget in list(self.widgetToItem.keys()):
            print('heyy')
            self.excluiItem(self.widgetToItem[widget])
        self.Host_num = 0
        self.Router_num = 0
        self.Switch_num = 0
        self.links = {}
        self.hostOpts = {}
        self.routerOpts = {}

        


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

