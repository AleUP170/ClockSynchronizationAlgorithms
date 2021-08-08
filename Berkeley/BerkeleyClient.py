# Algoritmo de Berkeley
# Script de cliente

import datetime, zmq, random, pickle
from time import sleep

def getRandomOffset(currTime : datetime.datetime):
	offset = datetime.timedelta(minutes=random.randint(-10,10), seconds=random.randint(-59, 59))
	newTime = currTime + offset
	return newTime

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
		print(f"ID del proceso: {id}\nEnviando tiempo de sincronización")

		# Obtiene tiempo
		firstTime = datetime.datetime.now()
		# Si modo = 2, se añade una variación aleatoria
		if modo == 2:
			firstTime = getRandomOffset(firstTime)
		
		print(f"Enviando tiempo {firstTime}")
		client.send(pickle.dumps(firstTime))

		# Espera a respuesta
		resp = client.recv().decode('utf-8')
		print(f"{resp}")

		#Espera para enviar mensaje de petición de tiempo nuevo
		sleep(0.01)
		client.send("Petición de tiempo".encode('utf-8'))
		# Espera a respuesta
		reply = pickle.loads(client.recv())

		# Mostar en pantalla recepción de mensaje
		print(f"Se recibió el nuevo tiempo: {reply}")

		sleep(10) # Espera 10 segundos

if __name__ == '__main__':
	main()