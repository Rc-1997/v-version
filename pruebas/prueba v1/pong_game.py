'este es ek q funca'
import socket
import string
import sys
'''sys.path.append("C:/Users/ricar/PycharmProjects/v-version/venv/prueba v1/servidor.py")
from servidor import *'''

import datetime
import pickle

import threading
from tkinter import *



class pong_game():
    def __init__(self,ip,jugador):

        self.bandera=0

        self.ip=ip
        self.jugador=jugador
        print(ip,jugador)
        while   TRUE:
            if self.jugador==1:
                self.puerto_enviar=8000
                self.puerto_recive=8001
                break
            elif self.jugador==2:
                self.puerto_enviar=8002
                self.puerto_recive=8003
                break


        self.ventana= Tk()
        self.x=self.ventana.winfo_screenwidth()
        self.y=self.ventana.winfo_screenheight()
        self.ventana.geometry("{0}x{1}+0+0".format(self.x,self.y))
        'self.ventana.overrideredirect(TRUE)'
        self.ventana.config(bg="RED")
        self.canvas= Canvas(self.ventana,bg="Black")

        self.x=1500
        self.y=800

        'pociciones de los objetos'

        self.jugador_posicion = []
        self.jugador_posicion.append((800 * 0.8) * 0.25)
        self.jugador_posicion.append((800 * 0.8) * 0.25)
        self.tope_izquierda = (1500 * 0.8) * 0.1
        self.tope_derecha = (1500 * 0.8) * 0.9
        self.tope_arriba = (800 * 0.8) * 0.1
        'el tope de abajo tiene q considerar el tamaño de la barra '
        self.tamaño_barra = 800 * 0.8 * 0.5
        self.tope_abajo = ((800 * 0.8) * 0.9) - self.tamaño_barra

        x=(1500*0.8)//2
        y=(800*0.8)//2

        t=(1500*0.8)*0.01

        self.pelota_posicion=[]
        self.pelota_posicion.append(x-t)
        self.pelota_posicion.append(y-t)

        'inicio de los objetos'

        self.canvas.place(x=self.x*0.1,y=self.y*0.1,width=self.x*0.8,height=self.y*0.8)

        self.jugador1=  self.canvas.create_line((1500*0.8)*0.075,self.jugador_posicion[0] ,(1500*0.8)*0.075,self.jugador_posicion[0]+self.tamaño_barra
                                                ,fill="blue",width=(1500*0.8)*0.01,tags="j1")

        self.pelota= self.canvas.create_rectangle(self.pelota_posicion[0] ,self.pelota_posicion[1],
                                                  self.pelota_posicion[0]+(2*t),self.pelota_posicion[1]+(2*t),
                                                    fill="white", tags="pelota")



        self.jugador2= self.canvas.create_line((1500*0.8) * 0.925,self.jugador_posicion[0] , (1500*0.8) * 0.925, self.jugador_posicion[0]+self.tamaño_barra
                                               , fill="blue",width=(1500*0.8) * 0.01, tags="j2")


        self.canvas.focus_set()

        'self.establecer_conexion()'
        self.conexionhilo1=threading.Thread(name="hilosconexion1",target=self.establecer_conexion)
        self.conexionhilo1.start()
        '''self.conexionhilo2=threading.Thread(name="hilosconexion2",target=self.conexion_j2)
        self.conexionhilo2.start()'''

        self.canvas.bind("<1>",lambda  event: self.click(event))
        self.canvas.bind("<Key>",lambda event: self.mover(event))
        self.hilo_actualizador=threading.Thread(name="actualizar",target=self.actualizar)
        self.hilo_actualizador.start()


        self.hilo_mainloop=threading.Thread(name="mainloop",target=self.ventana.mainloop())
        self.hilo_mainloop.start()

    def establecer_conexion(self):
        'se establece el recive'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.puerto_recive))
        self.socket.listen(1)
        self.conexion, self.direccion = self.socket.accept()

        'se establece el envia'
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.connect((self.ip, self.puerto_enviar))
        self.bandera+=1


    def click(self,event):
        print(event.x,event.y)

    def mover(self,event):
        if event.char=="w":
            self.enviar_movimiento("arriba")
        if event.char=="s":
            self.enviar_movimiento("abajo")
        if event.char=="i":
            ''
            self.enviar_movimiento_j2("arriba")
        if event.char == "k":
            ''
            self.enviar_movimiento_j2("abajo")

    '''j2
    def conexion_j2(self):
        'se establece el recive'
        self.socket_j2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_j2.bind((self.ip, 8003))
        self.socket_j2.listen(1)
        self.conexion_j2, self.direccion_j2 = self.socket_j2.accept()
        'se establece el envia'
        self.socket_j2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_j2.connect((self.ip, 8002))
        self.bandera+=1
    
    def enviar_movimiento_j2(self,movimiento):
        'movimiento = pickle.dumps(movimiento)'
        self.socket_j2.sendto(movimiento.encode(), (self.ip, self.puerto_enviar))
    
    def actualizar(self):
        'conexion de recive'
        while self.bandera<2:
            ''

        while True:
            self.valores = self.conexion_j2.recv(1024)
            self.valores=pickle.loads(self.valores)
            print(self.valores)
            self.canvas.move(self.jugador1 ,0,self.valores[0]-self.jugador_posicion[0])
            self.canvas.move(self.jugador2, 0, self.valores[1] - self.jugador_posicion[1])
            self.jugador_posicion[0]=self.valores[0]
            self.jugador_posicion[1]=self.valores[1]
            self.canvas.move(self.pelota,self.valores[2]- self.pelota_posicion[0] ,self.valores[3] - self.pelota_posicion[1])
            self.pelota_posicion[0]=self.valores[2]
            self.pelota_posicion[1]=self.valores[3]


            'self.conexion.send("si".encode())'

        self.conexion.close()'''

    def enviar_movimiento(self,movimiento):
        'movimiento = pickle.dumps(movimiento)'
        self.socket.sendto(movimiento.encode(), (self.ip, self.puerto_enviar))

        'respuesta = self.socket.recv(1024).decode()'
        'print(respuesta)'




    def actualizar(self):
        'conexion de recive'
        while self.bandera<1:
            ''

        while True:
            self.valores = self.conexion.recv(1024)
            self.valores=pickle.loads(self.valores)
            print(self.valores)
            self.canvas.move(self.jugador1 ,0,self.valores[0]-self.jugador_posicion[0])
            self.canvas.move(self.jugador2, 0, self.valores[1] - self.jugador_posicion[1])
            self.jugador_posicion[0]=self.valores[0]
            self.jugador_posicion[1]=self.valores[1]
            self.canvas.move(self.pelota,self.valores[2]- self.pelota_posicion[0] ,self.valores[3] - self.pelota_posicion[1])
            self.pelota_posicion[0]=self.valores[2]
            self.pelota_posicion[1]=self.valores[3]


            'self.conexion.send("si".encode())'

        self.conexion.close()

'pong_game(socket.gethostbyname(socket.gethostname()), 1)'


a=threading.Thread(name="j1",target=pong_game,args={socket.gethostbyname(socket.gethostname()),1})
b=threading.Thread(name="j2",target=pong_game,args={socket.gethostbyname(socket.gethostname()),2})
a.start()
b.start()
