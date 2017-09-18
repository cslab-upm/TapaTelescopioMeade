# -*- coding: utf-8 -*-
'''
Created on 31 ago. 2017

@author: AndresDiaz
'''

from flask import Flask, jsonify, request, abort, url_for, redirect
 
from managerMecanismo import managerMecanismo
import time
from threading import Thread, Timer
from managerColas import managerColas

# Url del servidor
url = '/api/tapa/montegancedo/'


app = Flask(__name__)
#app.config["JSON_SORT_KEYS"] = False

#Instacia del gestor del mecanismo
managerMec = managerMecanismo()
#Se revisa la base de datos.
managerMec.tasksReview()

#Se define la cola de mensajer�a
cola = managerColas()
cola.setMecanismo(managerMec.mecanismo)
#Se lanza en un nuevo hilo
thCola = Thread(target=cola.startQueue)
thCola.start()
#Se pasa la cola de mensajer�a a la instancia del mecanismo.
managerMec.mecanismo.setCola(cola)



@app.route('/')
def mainPage():
    return redirect(url, code = 302)

@app.route(url)
def mainPage2():
    return 'Pagina principal de la tapa del telescopio'


@app.route(url+'status', methods = ['GET'])
def get_status():
        return jsonify(managerMec.getStatus()),201

@app.route(url+'tasks', methods = ['GET'])
def get_tasks():
    return jsonify(managerMec.getTasks()), 201

@app.route(url+'createTask', methods = ['POST'])
def create_tasks():
    if not request.json or not 'orden' in request.json:
        abort(400)

    tasks = managerMec.getTasks()
    task = {
                'orden' : request.json['orden'],
        'done' : False
    }
    task['id'] = tasks[-1]['id']+1 if len(tasks)>0 else 1
    
    task['fechaInicio'] = time.strftime("%d/%m/%y")
    task['horaInicio'] = time.strftime("%H:%M:%S")
    managerMec.insertTask(task)
    managerMec.tasksReview()
    return jsonify({'task': task}), 201    

@app.route(url+'task', methods = ['GET'])
def get_task():
    task_id= request.args.get('task_id')
    task_id=int(task_id)
    task = managerMec.getTask(task_id)
    
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


if __name__ == '__main__':
    app.run(host = 'localhost', port=80, debug = True, use_reloader=True)
