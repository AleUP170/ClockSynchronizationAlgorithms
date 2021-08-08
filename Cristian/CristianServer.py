# Algoritmo de Cristian
# Script de servidor

import datetime, zmq, pickle

# Función main del script
def main():
	# Inicialización socket del servidor
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:5555") # Se va a usar el puerto 5555

	# El servidor se queda esperando por respuestas
	while True:
		# Recibe mensaje en forma de bits, decodifica a formato UTF-8
		mess = socket.recv().decode('utf-8')
		# Mostar en pantalla recepción de mensaje
		print(f"Se recibió el mensaje: {mess}")
		# Función que obtiene el tiempo actual en el servidor
		time = datetime.datetime.now()
		# Regresa el mensaje, codificado para poder ser leído correctamente
		socket.send(pickle.dumps(time))

if __name__ == '__main__':
	main()