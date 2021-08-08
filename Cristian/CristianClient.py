# Algoritmo de Cristian
# Script de cliente

import datetime, zmq, random, pickle

# Función para calcular el nuevo tiempo según algoritmo de Cristian
def getNewTime(serverTime : datetime.datetime, firstTime : datetime.datetime, actTime : datetime.datetime):
	# Fórmula para obtener diferencia de tiempo: (T1 - T0)/2
	offset = actTime - firstTime
	offset = offset/2
	# Suma al tiempo actual del sistema el offset
	newTime = serverTime + offset
	# Regresa offset y tiempo nuevo para impresión
	return offset, newTime

def getRandomOffset(currTime : datetime.datetime):
	offset = datetime.timedelta(minutes=random.randint(-10,10), seconds=random.randint(-59, 59))
	newTime = currTime + offset
	return newTime, offset

# Función main del script
def main():
	# Inicialización del cliente
	context = zmq.Context()
	client = context.socket(zmq.REQ)
	client.connect("tcp://localhost:5555") # Se va a usar el puerto 5555

	# Obtiene ID aleatorio para el proceso
	id = random.randint(0, 1024)

	# Selecciona si se usará el tiempo del sistema sin variación o con una variación aleatoria
	modo = int(input("""Inserte el modo de funcionamiento
	1) Normal
	2) Variación de tiempo aleatoria\n"""))

	# Iniciando cliente
	while True:
		_ = input(f"ID del proceso: {id}\nPrecione cualquier tecla para enviar una petición")

		# Empieza el inicio del mensaje
		firstTime = datetime.datetime.now()
		offset = datetime.timedelta(0)

		# Si modo = 2, se añade una variación aleatoria
		if modo == 2:
			firstTime, offset = getRandomOffset(firstTime)
		
		# Enviar mensaje
		mess = f"Petición de tiempo del cliente {id}"
		client.send(mess.encode('utf-8'))

		# Espera a respuesta
		reply = pickle.loads(client.recv())
		# Mostar en pantalla recepción de mensaje
		print(f"Se recibió la respuesta: {reply}")
		# Calcular nuevo tiempo
		actTime = datetime.datetime.now() + offset
		offsetServ, newTime = getNewTime(reply, firstTime, actTime)
		print(f"""Resultados para proceso {id}:
	Tiempo original: 		{firstTime}
	Tiempo del servidor: 		{reply}
	Desfase de tiempo:		{offsetServ}
	Tiempo actual:			{actTime}
	Tiempo corregido:		{newTime}""")

if __name__ == '__main__':
	main()