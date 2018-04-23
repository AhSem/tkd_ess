import socket
import _thread

temp_score = 0

def on_new_client(c, addr):
	print("New client connected. " + str(addr))
	while True:
		data = c.recv(1024)
		if not data:
			break
		global temp_score 
		temp_score += 1
		# print("Client: " + str(temp_score))
		print("Client: " + data.decode('utf-8'))


	c.close()

if __name__ == '__main__':
	
	s = socket.socket()
	s.bind(('127.0.0.1', 5010))

	s.listen(4)

	while True:
		c, addr = s.accept()
		_thread.start_new_thread(on_new_client, (c,addr))

	c.close()