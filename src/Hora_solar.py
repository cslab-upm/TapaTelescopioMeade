import ephem
from datetime import datetime


def solicitarPermiso():
	Permiso_apertura = False

	observatorio = ephem.Observer()
	observatorio.lat, observatorio.lon = '40.406161', '-3.838485'


	 
	i = datetime.utcnow()

	observatorio.date = i



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

	return Permiso_apertura

