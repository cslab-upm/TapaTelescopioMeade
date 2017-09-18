'''
Created on 31 ago. 2017

@author: AndresDiaz
'''
import pika
import cfg as c
from mecanismo import mecanismo

class managerColas(object):
    '''
    classdocs
    '''

    mecanismo = None
    credentials = pika.PlainCredentials('venus', 'informaticaciclope')
    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    def setMecanismo(self, mecanismo):
        self.mecanismo = mecanismo

    def startQueue(self):
        
        
        self.channel.queue_declare(queue=c.me, durable = True)
        self.channel.exchange_declare(exchange=c.me)
        for x in c.lista:
                self.channel.queue_declare(queue=x, durable=True)

        for x,y in zip(c.lista,c.severity):
                self.channel.exchange_declare(exchange=x
                                    )
                self.channel.queue_bind(exchange=x,
                                   queue=c.me,
                                   routing_key=y)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            self.processMessage(body)

        self.channel.basic_consume(callback, queue=c.me, no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def processMessage(self, mensaje):
        if (mensaje == 'CierreEmergencia'):
            print 'Cerrando...'
            self.mecanismo.closeCover()
        elif (mensaje == 'Reanudar'):
            print 'reanudando...'
            self.mecanismo.openCover()
        elif (mensaje == 'Posicion'):
            print 'Posible choque, cerrando...'
            self.mecanismo.closeCover()
            
    def sendMessage(self, mensaje, severity):
        self.channel.basic_publish(exchange=c.me,
                      routing_key=severity,
                      body=mensaje)      
        
