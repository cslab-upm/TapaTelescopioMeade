'''
Created on 13 sept. 2017

@author: AndresDiaz
'''
import pika
import cfg as c


def main():
    # my code here
    credentials = pika.PlainCredentials('venus', 'informaticaciclope')
    parameters = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    startQueue(channel)

def startQueue(channel):
        
        
        channel.queue_declare(queue='cupula', durable = True)
        channel.exchange_declare(exchange='cupula')
        for x in c.lista2:
                channel.queue_declare(queue=x, durable=True)

        for x,y in zip(c.lista2,c.severity):
                channel.exchange_declare(exchange=x)
                channel.queue_bind(exchange=x,
                                   queue='cupula',
                                   routing_key=y)

        def callback(ch, method, properties, body):
            print(" [x] Received %r" % body)
            processMessage(body)

        channel.basic_consume(callback, queue='tapa', no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()

def processMessage(mensaje):
        if (mensaje == 'CierreEmergencia'):
            print 'Cerrando...'
            
        elif (mensaje == 'Reanudar'):
            print 'reanudando...'
            
        elif (mensaje == 'Posicion'):
            print 'Posible choque, cerrando...'
            
        elif (mensaje == 'Fallo al abrir la tapa'):
            print mensaje    
        print mensaje   
def sendMessage( channel,mensaje, severity):
        channel.basic_publish(exchange='cupula',
                      routing_key=severity,
                      body=mensaje)
    
    
    
if __name__ == '__main__':
    main()    