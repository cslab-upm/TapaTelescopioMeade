# TapaTelescopioMeade

## API REST 

- `GET /api/tapa/montegancedo/status`
- `GET /api/tapa/montegancedo/tasks`
- `GET /api/tapa/montegancedo/tasks/<task-id>`
- `POST /api/tapa/montegancedo/createTask`

### `GET /api/tapa/montegancedo/status`
Obtener información sobre el estado de la tapa
Ejemplo de respuesta:
~~~py
{
'estado':
	{
	'abierto': True ,
	'cerrado': False ,
	'automaticMode': False,
	'modoManual' True 
	}
}
~~~
 
### `GET /api/tapa/montegancedo/tasks`

Obtener información sobre las tareas 

Ejemplo de respuesta:
~~~py
{
"positions": {
    },
	     
"_default": {
    },
    
"tasks": {
    "1": {
	    "orden": "orden",
	    "resultado": false,
	    "done": true,
	    "horaInicio": "00:08:10",
	    "fechaInicio": "08/09/17",
	    "id": 1
	      },
    "2": {
        "orden": "Abrir",
		"resultado": false,
	    "done": true,
		"horaInicio": "00:16:57",
	    "fechaInicio": "08/09/17",
	    "id": 2
		},
	    "3": {
	        "orden": "Cerrar",
		    "horaInicio": "17:46:27",
		    "done": false,
		    "fechaInicio": "10/09/17",
		    "id": 3
		    }
	  }
}

~~~

### `GET /api/tapa/montegancedo/tasks/<task-id>`
Obtener información sobre la tarea **<task-id>**

Ejemplo de respuesta:
~~~py
{
"2": {
        "orden": "Abrir",
		"resultado": false,
	    "done": true,
		"horaInicio": "00:16:57",
	    "fechaInicio": "08/09/17",
	    "id": 2
		}
}
~~~

### `POST /api/tapa/montegancedo/createTask`
Crear una tarea nueva

Petición:
~~~py
{
"orden" : "Abrir"
}
~~~
Respuesta:
~~~py
{
"2": {
        "orden": "Abrir",
		"resultado": false,
	    "done": true,
		"horaInicio": "00:16:57",
	    "fechaInicio": "08/09/17",
	    "id": 2
		}
}

