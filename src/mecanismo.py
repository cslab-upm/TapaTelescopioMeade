'''
Created on 29 ago. 2017

@author: AndresDiaz
'''
import time
import wiringpi
import RPi.GPIO as GPIO
import sys
import json


class mecanismo(object):
    '''
    classdocs
    '''
    automaticMode = True
    manualMode = False
    FC_cierre = False
    FC_apertura = False
    Abrir_cierre = 167
    Cerrar_cierre = 135
    T1=T2=T3=T4=0
    positions=None
    pulse=0
    cola = None
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    # use 'GPIO naming'
    wiringpi.wiringPiSetupGpio()
         
    # set #18 to be a PWM output
    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pinMode(19, wiringpi.GPIO.PWM_OUTPUT) 
    # set the PWM mode to milliseconds stype
        
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
         
    # divide down clock
    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)


    def __init__(self, positions, query):
        '''
        Constructor
        '''
        self.positions=positions
 
        self.getLastPos(query)
           
        
    
    def callbackOpened(self):
            
        global FC_apertura
        
        if  not GPIO.input(4):
            FC_apertura= True
        else:
            FC_apertura= False
        print FC_apertura
        
##        self.cola.sendMessage('tapaAbierta','info')
    GPIO.add_event_detect(4, GPIO.BOTH, callbackOpened,bouncetime=200)
    
    
    
    
    def callbackClosed(self):
           
        global FC_cierre
        
        if  not GPIO.input(26):
            FC_cierre= True
            wiringpi.pwmWrite(19,self.Cerrar_cierre) 
        else:
            FC_cierre= False
            wiringpi.pwmWrite(19,self.Abrir_cierre)
            
        print FC_cierre
##        self.cola.sendMessage('tapaCerrada','info')
                            
    GPIO.add_event_detect(26, GPIO.BOTH, callbackClosed,bouncetime=200)
    
    
    
    
    def openCover(self):
        
        global T1, T2, pulse
        wiringpi.pwmWrite(19,self.Abrir_cierre)
        #try:
        while pulse<=250 and pulse>125:
            T1=time.time()
                            
            if not FC_apertura and T1-T2 > 0.1:
                T2=time.time()        
                wiringpi.pwmWrite(18, pulse)
                pulse=pulse-1
                print pulse
        
            self.setLastPos()
        
    #    if self.pulse==250 and not self.FC_apertura:
            #self.cola.sendMessage('Fallo al abrir la tapa','critical')    
            
        return True 
    
    def closeCover(self):
        #global T3, FC_cierre, T4
        #try:
        while self.pulse>=125 and self.pulse<249:
            T3=time.time()        
                            
            if not FC_cierre:
                                    
                if self.pulse < 240 and T3-T4 > 0.1:
                    T4=time.time()
                    wiringpi.pwmWrite(18, self.pulse)
                    self.pulse=self.pulse+1
                    print self.pulse
                elif self.pulse >= 240 :
                    T4=time.time()
                    wiringpi.pwmWrite(18, self.pulse)
                    self.pulse=self.pulse+1
                    print self.pulse
                if pulse==250:
                    wiringpi.pwmWrite(19, self.Cerrar_cierre)
                
                self.setLastPos(self.pulse)
                
#        if self.pulse==250 and not self.FC_cierre:
            #self.cola.sendMessage('Fallo al abrir la tapa','critical')
                   
        return True    
    
    
    def setLastPos(self,pulse):
        position = {
                    'id' : '1',
            'pulse' : json.dumps(pulse)
        }
        self.positions.insert(pulse)
    
    def getLastPos(self,query):
        self.pulse=self.positions.search(query.pulse.id == 1)
        
        
    def setAutomaticMode(self):
        self.automaticMode = True
        print('\nModo automatico')
        return True
        
    def setManualMode(self):
        self.manualMode = True
        print('\nModo manual')
        return True

    def setCola(self,cola):
        self.cola=cola

    def getStatus(self):
        if(not self.FC_cierre):
            abierto=True
        else:
            abierto=False
            
        status=[abierto, self.FC_cierre, self.automaticMode, self.manualMode]
        return status
            
                  
                            
                                    
                    
                     
    
                    
    
                
