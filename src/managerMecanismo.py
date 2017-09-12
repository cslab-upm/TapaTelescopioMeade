'''
Created on 29 ago. 2017

@author: AndresDiaz
'''
from mecanismo import mecanismo
from tinydb import TinyDB, Query
import json
from threading import Thread, Timer


import ephem
from datetime import datetime
import time

class managerMecanismo(object):
    '''
    classdocs
    '''
    revisando = False
    revisar = True

    #Base de datos
    db = TinyDB('database.json')
    tasks = db.table('tasks')
    positions = db.table('positions')
    query = Query()
    
    permiso=False
    cancelarHilo=False

    mecanismo = None
    def __init__(self):
        '''
        Constructor
        '''
       
        self.mecanismo = mecanismo(self.positions, self.query)
        
        pass
    
    # Devuelve el estado del telescopio en json
    def getStatus(self):
        [abierto, cerrado, automaticMode, manualMode] = self.mecanismo.getStatus()
        return {'estado':{'abierto':abierto, 'cerrado': cerrado, 'automaticMode': automaticMode,
                                      'modoManual': manualMode
                                      }}
    def getTasks(self):
        return self.tasks.all()

    def insertTask(self, task):
        self.tasks.insert(task)

    def getTask(self, iden):
        return self.tasks.search(self.query.id == iden)

    def tasksReview(self):
        self.revisar = True
        if self.revisando == False:
            self.revisando = True
            th = Thread(target = self.petitionsProcess())
            th.start()
            

    def petitionsProcess(self):
        while self.revisar:
            self.revisar = False
            for task in self.tasks.search(self.query.done == False):
                self.taskProcess(task)
        self.revisando = False
        
    def setResult(self, resultado, iden):
        print resultado
        print iden
        self.tasks.update({'resultado': resultado, 'done': True}, self.query.id == iden)

    
        
    # Identifica que debe hacer el telescopio
    def taskProcess(self, peticion):
        print('Procesar una peticion')
        # Anadimos la tarea a la base de datos
        iden = peticion['id']
        # Nos centramos en la orden a realizar
        orden = peticion['orden']
        
        resultado = False
        #Comprobamos las posibles ordenes
        if orden == 'modoAutomatico':
            resultado=self.mecanismo.setAutomaticMode()

        elif orden == 'modoManual':
            resultado=self.mecanismo.setManualMode()

        elif orden == 'Abrir':
            
            
            self.cancelarHilo=False
            thEphem = Thread(target=self.solicitarPermiso())
            thEphem.start()
            
            if self.permiso or mecanismo.manualMode:
                resultado=self.mecanismo.openCover()

        elif orden == 'Cerrar':
            self.cancelarHilo=True
            resultado=self.mecanismo.closeCover()

        
            
                
                   
        # Actualizamos la tarea y finalizamos su procesamiento
        if resultado != True:
            self.setResult(resultado, iden)

        print('Final del procesado')
        return resultado
        
    def solicitarPermiso(self):

        observatorio = ephem.Observer()
        observatorio.lat, observatorio.lon = '40.406161', '-3.838485'
    
    
         
        i = datetime.utcnow()
    
        observatorio.date = i
    
    
        while not self.cancelarHilo:
            #Calcular twilight
            observatorio.horizon = '-18'
            h_AmanecerPrevio = observatorio.previous_rising(ephem.Sun())
            h_AtardecerPrevio = observatorio.previous_setting(ephem.Sun())
            
            if h_AmanecerPrevio > h_AtardecerPrevio:
                Permiso_apertura=False #Dia
            else:
                Permiso_apertura=True #Noche
        
        
            print ('%f'%h_AmanecerPrevio)
            print ('%f'%h_AtardecerPrevio)
            print ('%f'%observatorio.date)
            print Permiso_apertura
            
            time.sleep(10)
    
        return Permiso_apertura
