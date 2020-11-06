import sys
#import random
import strgen
from time import sleep
import signal
from gpiozero import LED, Button
from threading import Thread
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
#from random import  random

# definir  lis pines a usar

LED1 = LED(18)
LED2 = LED(23)
LED3 = LED(24)
#LED4 = LED(24)
BUTTON = Button(4)
BUTTONL = Button(17)
BUTTONS= Button(27)
ACTF = Button(22)
ACTR = Button(3)

#USR= Usuario

PAHT_CRED = '/home/pi/iot/cred.json' # direccion de archivo credenciales de jason.
URL_DB = 'https://iot-maq.firebaseio.com/home' # direccion de base de datos firebase
REF_MAQ = 'MAQ'
REF_HOME = 'home' # referencia principal home
REF_LUCES = 'luces'# referencias luces y sala child home
REF_BOTONES = 'botones' #referenica botones child home
REF_LUZ_SALA = 'luzsala'#referencia luz_sala child luces
REF_LUZ_COCINA= 'luzcocina'
REF_PULSADOR_A = 'pulsadora' #referencia pulsador_a sala child luces
REF_PULSADOR_B = 'pulsadorb' # parac agregar otra luz u otro boton
REF_PULSADOR_S = 'pulsadorS' # parac agregar otra luz u otro boton
REF_PULSADOR_F = 'pulsadorF' # parac agregar otra luz u otro boton
REF_PULSADOR_R = 'pulsadorR' # parac agregar otra luz u otro boton
REF_USUARIO = 'Edfred' 
REF_LATAS = 'Latas_Prem'

class IOT(): #clase python iot

    def __init__(self):
        cred = credentials.Certificate(PAHT_CRED)  #solicita credenciales jasosn
        firebase_admin.initialize_app(cred, {      #inicializa la conexion con base de datos
            'databaseURL': URL_DB                  #se conecta a la url
        })
        self.refMAQ = db.reference(REF_MAQ)
        #self.refHome = db.reference(REF_HOME)
        
        #self.estructuraInicialDB() # solo ejecutar la primera vez
        # creacion de variables para buscar la referencia de cada uno de los 
        self.refUsuario = self.refMAQ.child(REF_USUARIO)
        self.refLatas_Pem = self.refUsuario.child(REF_LATAS)
        
        self.refHome = self.refMAQ.child(REF_HOME)
        self.refLuzSala = self.refHome.child(REF_LUZ_SALA)
        self.refLuzCocina = self.refHome.child(REF_LUZ_COCINA)# hay que crear la variable cocina arriba 
       # self.refBotones = self.refHome.child(REF_BOTONES)
        self.refPulsadorA = self.refHome.child(REF_PULSADOR_A)
        self.refPulsadorB = self.refHome.child(REF_PULSADOR_B) # crear variable arriba
        self.refPulsadorS = self.refHome.child(REF_PULSADOR_S)
        self.refPulsadorF = self.refHome.child(REF_PULSADOR_F)
        self.refPulsadorR = self.refHome.child(REF_PULSADOR_B)
        
    def estructuraInicialDB(self):
        self.refMAQ.set({
            'home': {
                 #Home
                'luzsala':True,
                'luzcocina':True,
           # },
            #'botones':{
                'pulsadora':True,
                'pulsadorb':True,
                'pulsadorS':True,
                'pulsadorF':True,
                'pulsadorR':True
             }
        })
        

            
    def ledControlGPIO(self, estado):# enciende o apaga el led depende el estado
      #while estado:
            
        if estado == "true":
            LED1.on()
            print('LED ON')
        #if estado == "false":
           # LED1.off()
           # print('LED of')
        else:
            LED1.off()
            print('LED OFF')
            
    def led2ControlGPIO(self, estado):# enciende o apaga el led depende el estado
        if estado == "true":
            LED2.on()
            print('LED2 ON')
        else:
            LED2.off()
            print('LED2 OFF')
            
    def led3ControlGPIO(self):# enciende o apaga el led depende el estado
        self.refPulsadorF.set(True)
        servo.value(1)
      # SERVO = AngularServo(17, min_angle= 45, max_angle=-45)
     #  SERVO.angle=15
        print ('activado el boton servo')
        
       
       
    
    #def led4ControlGPIO(self):# enciende o apaga el led depende el estado
      # self.refPulsadorR.set(True)
     #  print ('activado el actuador')

    def lucesStart(self):

        E, i = [], 0  # guardamos los valores en este vector

        estado_anterior = self.refLuzSala.get()   
        self.ledControlGPIO(estado_anterior)

        E.append(estado_anterior)

        while True:  # sealiza una accion cada vez que se realice un cambio
          estado_actual = self.refLuzSala.get() #si el estado actual es diferencte al anterior
          E.append(estado_actual)

          if E[i] != E[-1]:  # si es diferente haga un cambio
              self.ledControlGPIO(estado_actual) # y llama a la funcion led contro gpio y le envioa ese valor a estado

          del E[0]    # pregunta cada 0.4 seg
          i = i + i
          sleep(0.4)
          
    def lucesStart2(self):
        print("hola mundo")
        E2, i2 = [], 0  # guardamos los valores en este vector

        estado_anterior2 = self.refLuzCocina.get()   
        self.led2ControlGPIO(estado_anterior2)

        E2.append(estado_anterior2)

        while True:  # sealiza una accion cada vez que se realice un cambio
          estado_actual2 = self.refLuzCocina.get() #si el estado actual es diferencte al anterior
          E2.append(estado_actual2)

          if E2[i2] != E2[-1]:  # si es diferente haga un cambio
              self.led2ControlGPIO(estado_actual2) # y llama a la funcion led contro gpio y le envioa ese valor a estado

          del E2[0]    # pregunta cada 0.4 seg
          i2 = i2 + i2
          sleep(0.4)

    def pulsador_on(self):    #generador de token
        print('Pulsador On')
        i3 = strgen.StringGenerator("[\w\d]{8}").render()
        self.refPulsadorA.set(i3)
        self.refPulsadorB.set(0)
        
      
    
        
        
    def pulsador_on2(self):  #Genrador de  contador de latas apachadas
        print('Pulsador2ONf')
        contador = self.refPulsadorB.get() 
        user = self.refPulsadorF.get()
        contador = contador +1  
        self.refPulsadorB.set(contador)
       
        print(user)
        self.refMAQ.child(user).child('Latas_Total').set(True)
        
        

       
    def pulsador_on3(self):
        act= self.refLuzSala.get()
        #ser= self.refPulsadorS.get()
        
       # print(ser)
       # if act and ser:
           # self.led3ControlGPIO()

    def pulsador_on4(self):
        print('llamo metodo4')
        act= self.refLuzSala.get()
        der= self.refPulsadorF.get()
        
      
        if act:# ser:
            print ('a')
            if der:
                print('a')
             
        #if act and der:
           #self.led4ControlGPIO()
                
    def pulsador_on5(self):
        print('llamo metodo4')
        act= self.refLuzSala.get()
        ser= self.refPulsadorS.get()
        der= self.refPulsadorF.get()
        lef= self.refPulsadorR.get()
      
        if act:# ser:
            print ('a')
            if der:
                print('a')
        

    def pulsador_off(self):
        print('Pulsador Off')
        self.refPulsadorA.set(False)

    def botonesStart(self):  # llamo a la genrador de string
        print('Start btn !')
        BUTTON.when_pressed = self.pulsador_on
       # BUTTON.when_released = self.pulsador_off
       
    def botonesStart2(self): # llamo a contador de latas
        print('sensor listo')
        BUTTONL.when_pressed = self.pulsador_on2
       
       # BUTTON.when_released = self.pulsador_off
    def botonesStart3(self):
       BUTTONS.when_pressed = self.pulsador_on3   
       ACTF.when_pressed = self.pulsador_on4  
       ACTR.when_pressed = self.pulsador_on5
       
       
 


        


print ('START !')
iot = IOT()


subproceso_led = Thread(target=iot.lucesStart)  # hilo para llamar los datos de la db
subproceso_led.daemon = True
subproceso_led.start()

subproceso_led2 = Thread(target=iot.lucesStart2)  # hilo para llamar los datos de la db
subproceso_led2.daemon = True
subproceso_led2.start()

subproceso_btn = Thread(target=iot.botonesStart)
subproceso_btn.daemon = True
subproceso_btn.start()

subproceso_btn2= Thread(target=iot.botonesStart2)
subproceso_btn2.daemon = True
subproceso_btn2.start()

subproceso_btn3= Thread(target=iot.botonesStart3)
subproceso_btn3.daemon = True
subproceso_btn3.start()

subproceso_btn4= Thread(target=iot.botonesStart3)
subproceso_btn4.daemon = True
subproceso_btn4.start()
signal.pause()
