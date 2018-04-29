import pickle
import socket
import _thread

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

temp_score = 0

class ServerRoot(BoxLayout):
	match_number = ObjectProperty()
	category_name = ObjectProperty()

	chung_name = ObjectProperty()
	chung_score = ObjectProperty()
	chung_penalty = ObjectProperty()

	hong_name = ObjectProperty()
	hong_score = ObjectProperty()
	hong_penalty = ObjectProperty()

	time_counter = ObjectProperty()

	"""docstring for ServerRoot"""
	def __init__(self, **kwargs):
		super(ServerRoot, self).__init__(**kwargs)
		self.t = _thread.start_new_thread(self.start_socket_connection, ('127.0.0.1', 5010))

	def start_socket_connection(self, host, port):
		print("Starting up socket connection...")
		self.s = socket.socket()
		self.s.bind((host, port))
		self.s.listen(4)

		while True:
			c, addr = self.s.accept()
			_thread.start_new_thread(self.on_new_client, (c,addr))
		c.close()
			
	def on_new_client(self, c, addr):
		print("New client connected. " + str(addr))
		while True:
			data = c.recv(1024)
			if not data:
				break
			# global temp_score 
			# temp_score += 1
			d = pickle.loads(data)
			print("Received: " + str(d))

			for key in d:
				if key == 'update_match_number':
					self.match_number.text='Match ' + d[key]

				elif key == 'update_category_name':
					self.category_name.text = 'Category ' + d[key]

				elif key == 'update_total_round':
					pass

				elif key == 'update_round_duration':
					pass

				elif key == 'update_rest_duration':
					pass

				elif key == 'update_chung_name':
					self.chung_name.text = d[key]

				elif key == 'update_chung_team':
					pass

				elif key == 'add_chung_score' or key =='minus_chung_score':
					self.chung_score.text = str(d[key])

				elif key == 'add_chung_penalty' or key =='minus_chung_penalty':
					self.chung_penalty.text = str(d[key])

				elif key == 'update_hong_name':
					self.hong_name.text = d[key]

				elif key == 'update_hong_team':
					pass

				elif key == 'add_hong_score' or key == 'minus_hong_score':
					self.hong_score.text = str(d[key])

				elif key == 'add_hong_penalty' or key == 'minus_hong_penalty':
					self.hong_penalty.text = str(d[key])

				elif key == 'update_time_counter':
					self.time_counter.text = str(d[key])

		c.close()



class EssServer(App):

	def build(self):
		self.root = ServerRoot()
		return self.root


if __name__ == '__main__':

	EssServer().run()
