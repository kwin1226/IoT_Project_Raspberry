from socketIO_client import SocketIO, LoggingNamespace

def pushUsingIn():
	with SocketIO('140.138.77.152', 5050, LoggingNamespace) as socketIO:
		socketIO.emit('PIR', {'eid':'Rasp01','IsUsing':True,'Accident':False})
	return True

def pushUsingOut():
	with SocketIO('140.138.77.152', 5050, LoggingNamespace) as socketIO:
		socketIO.emit('PIR', {'eid':'Rasp01','IsUsing':False,'Accident':False})
	return True

def pushFalldown():
	with SocketIO('140.138.77.152', 5050, LoggingNamespace) as socketIO:
		socketIO.emit('PIR', {'eid':'Rasp01','IsUsing':True,'Accident':True})
	return True
