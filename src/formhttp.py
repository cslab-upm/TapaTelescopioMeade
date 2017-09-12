import json
import urllib2

request = {
        'orden': 'Cerrar'
}

req = urllib2.Request('http://localhost:80/api/tapa/montegancedo/createTask')
req.add_header('Content-Type', 'application/json')

response = urllib2.urlopen(req, json.dumps(request))
