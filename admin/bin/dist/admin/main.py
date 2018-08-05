import collections, pickle, socket, time, _thread
from kivy.app import App
from kivy.graphics import Color
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from threading import Thread

class AdminRoot(BoxLayout):

	chung_score: ObjectProperty()
	chung_penalty: ObjectProperty()
	hong_score: ObjectProperty()
	hong_penalty: ObjectProperty()
	time_counter: ObjectProperty()
	time_set: ObjectProperty()
	round_number: ObjectProperty()
	server_host: ObjectProperty()
	server_port: ObjectProperty()
	connection_status: ObjectProperty()

	def __init__(self, **kwargs):
		super(AdminRoot, self).__init__(**kwargs)
		self.chung_score.text, self.chung_penalty.text, self.hong_score.text, self.hong_penalty.text, self.timer = ('0','0','0','0', 0)
		self.chung_temp_score, self.hong_temp_score = [], []
		self.timer_control = 'stop'

		self.time_counter_thread = Thread(target=self.countdown)
		self.time_counter_thread.start()

		self.connection_thread = Thread(target=self.start_socket_connection)
		self.connection_thread.start()

		self.score_tracker_thread = Thread(target=self.score_tracker)
		self.score_tracker_thread.start()

		self.chung_resetter_thread = Thread(target=self.chung_temp_score_resetter)
		self.chung_resetter_thread.start()

		self.hong_resetter_thread = Thread(target=self.hong_temp_score_resetter)
		self.hong_resetter_thread.start()

	def start_socket_connection(self):
		with open("server.txt") as f:
			server = f.read().split()

		s = socket.socket()
		s.bind((server[0], int(server[1])))
		s.listen(3) # 3 clients

		while True:
			c, addr = s.accept()
			_thread.start_new_thread(self.on_new_client, (c,addr))
		c.close()

	def on_new_client(self, c, addr):
		print("New client connected. " + str(addr))
		while True:
			data = c.recv(1024)
			if not data:
				break
			d = pickle.loads(data)
			print("Received: " + str(d))

			for key in d:
				if key == 'chung_score':
					self.chung_temp_score.append(d[key])

				elif key == 'hong_score':
					self.hong_temp_score.append(d[key])

		c.close()

	def connect_to_display_server(self):
		if self.server_host.text != '' and self.server_port != '':
			self.s = socket.socket()
			try:
				self.s.connect((self.server_host.text, int(self.server_port.text)))
				self.connection_status.text = 'Connected.'
				self.connection_status.color = [0,1,0,1]
			except:
				print('Connection fails.')
				self.s.close()

	def send_to_display_server(self, message):
		print(message)
		try:
			self.s.sendall(pickle.dumps(message))
		except:
			self.connect_to_display_server()

	def chung_temp_score_resetter(self):
		counter = 0
		while True:
			if len(self.chung_temp_score) > 0:
				time.sleep(1)
				counter += 1
			if counter >= 2:
				print('2 seconds passed. Clear Chung temp scores.')
				del self.chung_temp_score[:]
				counter = 0
	
	def hong_temp_score_resetter(self):
		counter = 0
		while True:
			if len(self.hong_temp_score) > 0:
				time.sleep(1)
				counter += 1
			if counter >= 2:
				print('2 seconds passed. Clear Hong temp scores.')
				del self.hong_temp_score[:]
				counter = 0

	def score_tracker(self):
		while True:
			c_s = [item for item, count in collections.Counter(self.chung_temp_score).items() if count > 2]
			h_s = [item for item, count in collections.Counter(self.hong_temp_score).items() if count > 2]
			if len(c_s) > 0:
				print(c_s)
				print('Chung scores ', c_s[0])
				self.chung_score.text = str(int(self.chung_score.text)+c_s[0])
				self.send_to_display_server({'add_chung_score': self.chung_score.text})
				del self.chung_temp_score[:]
			if len(h_s) > 0:
				print(h_s)
				print('Hong scores ', h_s[0])
				self.hong_score.text = str(int(self.hong_score.text)+h_s[0])
				self.send_to_display_server({'add_hong_score': self.hong_score.text})
				del self.hong_temp_score[:]

	# ##########################################################################
	# Settings
	############################################################################
	def countdown(self):
		while True:
			while self.timer >= 0 and self.timer_control == 'start':
				mins, secs = divmod(self.timer, 60)
				self.time_counter.text = '{:02d}:{:02d}'.format(mins, secs)
				try:
					self.send_to_display_server({'update_time_counter': self.time_counter.text})
				except:
					pass
				time.sleep(1)
				self.timer -= 1
				if self.timer < 0:
					self.timer_control = 'stop'
					if int(self.round_number.text) < int(self.round_total.text):
						self.round_number.text = str(int(self.round_number.text) + 1)
						self.set_time(self.time_set)
						rest_duration = int(self.rest_duration.text)
						while rest_duration >= 0:
							rest_mins, rest_secs = divmod(rest_duration, 60)
							self.rest_time_counter.text = '{:02d}:{:02d}'.format(rest_mins, rest_secs)
							try:
								self.send_to_display_server({'update_rest_time_counter': self.rest_time_counter.text})
							except:
								pass
							time.sleep(1)
							rest_duration -= 1

	def set_time(self, text_input):
		ftr = [60,1]
		try:
			self.timer = sum([a*b for a,b in zip(ftr, map(int,text_input.text.split(':')))])
			self.time_counter.text = text_input.text
			self.send_to_display_server({'update_time_counter': text_input.text})
		except:
			pass

	def set_round(self, text_input):
		self.round_number.text = text_input.text
		self.send_to_display_server({'update_round_number': text_input.text})

	# ##########################################################################
	# Controls
	############################################################################
	def update_match_number(self, text_input):
		self.send_to_display_server({'update_match_number': text_input.text})

	def update_category_name(self, text_input):
		self.send_to_display_server({'update_category_name': text_input.text})

	def update_total_round(self, text_input):
		self.send_to_display_server({'update_total_round': text_input.text})

	# def update_round_duration(self, text_input):
		# self.send_to_server({'update_round_duration': text_input.text})

	# def update_rest_duration(self, text_input):
		# self.send_to_server({'update_rest_duration': text_input.text})

	def start_countdown(self, button):
		self.timer_control = 'start'

	def pause_countdown(self, button):
		self.timer_control = 'pause'

	def reset_countdown(self, button):
		self.timer_control = 'stop'
		self.round_number.text = '1'
		self.set_time(self.time_set)

	# ##########################################################################
	# CHUNG
	############################################################################
	def update_chung_name(self, text_input):
		self.send_to_display_server({'update_chung_name': text_input.text})

	def update_chung_team(self, text_input):
		self.send_to_display_server({'update_chung_team': text_input.text})

	def add_chung_score(self, button):
		self.chung_score.text = str(int(self.chung_score.text)+1)
		self.send_to_display_server({'add_chung_score': self.chung_score.text})

	def minus_chung_score(self, button):
		self.chung_score.text = str(int(self.chung_score.text)-1)
		self.send_to_display_server({'minus_chung_score': self.chung_score.text})

	def add_chung_penalty(self, button):
		self.chung_penalty.text = str(int(self.chung_penalty.text)+1)
		self.send_to_display_server({'add_chung_penalty': self.chung_penalty.text})

	def minus_chung_penalty(self, button):
		self.chung_penalty.text = str(int(self.chung_penalty.text)-1)
		self.send_to_display_server({'minus_chung_penalty': self.chung_penalty.text})

	# ##########################################################################
	# HONG
	############################################################################
	def update_hong_name(self, text_input):
		self.send_to_display_server({'update_hong_name': text_input.text})

	def update_hong_team(self, text_input):
		self.send_to_display_server({'update_hong_team': text_input.text})

	def add_hong_score(self, button):
		self.hong_score.text = str(int(self.hong_score.text)+1)
		self.send_to_display_server({'add_hong_score': self.hong_score.text})

	def minus_hong_score(self, button):
		self.hong_score.text = str(int(self.hong_score.text)-1)
		self.send_to_display_server({'minus_hong_score': self.hong_score.text})

	def add_hong_penalty(self, button):
		self.hong_penalty.text = str(int(self.hong_penalty.text)+1)
		self.send_to_display_server({'add_hong_penalty': self.hong_penalty.text})

	def minus_hong_penalty(self, button):
		self.hong_penalty.text = str(int(self.hong_penalty.text)-1)
		self.send_to_display_server({'minus_hong_penalty': self.hong_penalty.text})



class EssAdmin(App):
	def build(self):
		self.root = AdminRoot()
		return self.root


if __name__ == '__main__':
	EssAdmin().run()
