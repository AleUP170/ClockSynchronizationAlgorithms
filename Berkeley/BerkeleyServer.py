# Algoritmo de Berkeley
# Script de servidor

import datetime, zmq, pickle
from time import sleep

# Estructura para guardar datos (tiempo) de clientes. Global
timeClients = []

# Recibe tiempo de todos los clientes conectados
def getTime(numClients : int, socket):
	for x in range(numClients):
		timeC = pickle.loads(socket.recv())
		# Recibe tiempo, imprime tiempo recibido
		print(f"Tiempo {x} recibido: {timeC}")
		# Calcula diferencia de tiempo
		timeClients.append(datetime.datetime.now() - timeC)
		socket.send("Calculando...".encode('utf-8'))

# Calcula promedio
def calcAverageTimeDiff():
	# Sumar tiempos, incluye diferencia con tiempo de servidor (diferencia de 0)
	sumTimes = sum(timeClients, datetime.timedelta(0,0))
	# Divide para obtener promedio
	average = sumTimes/len(timeClients)
	print(f"Diferencia de tiempo promedio: {average}")
	return average 

# Manda nuevo reloj
def sendTime (numClients : int, socket, offset : datetime.timedelta):
	# Obtiene nuevo tiempo de reloj
	newTime = datetime.datetime.now() + offset
	print(f"El nuevo tiempo en el sistema es {newTime}")
	# Obtiene petición para nuevo tiempo de los clientes
	for x in range(numClients):
		# Espera a recibir mensaje
		id = socket.recv().decode('utf-8')
		print (f"Enviando a cliente {id}")
		socket.send(pickle.dumps(newTime))

# Función main del script
def main():
	# Inicialización socket del servidor
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:5555") # Se va a usar el puerto 5555

	# Número de clientes se especifica al iniciar
	numClients = int(input("Ingrese el número de clientes a usar: "))

	# El servidor se queda esperando por respuestas
	while True:
		print("Iniciando sincronización")
		# Función para obtener tiempo
		getTime(numClients, socket)
		offset = calcAverageTimeDiff()
		# Mandar nuevo tiempo a todos los clientes
		sendTime(numClients, socket, offset)
		# Algoritmo terminado
		print("Sincronización terminada")
		sleep(10) # Inicia este proceso cada 10 segundos

if __name__ == '__main__':
	main()