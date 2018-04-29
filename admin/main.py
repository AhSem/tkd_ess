import pickle, socket, time
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
	rest_time_counter: ObjectProperty()
	time_set: ObjectProperty()
	rest_duration: ObjectProperty()
	round_total: ObjectProperty()
	round_number: ObjectProperty()
	server_host: ObjectProperty()
	server_port: ObjectProperty()
	connection_status: ObjectProperty()

	def __init__(self, **kwargs):
		super(AdminRoot, self).__init__(**kwargs)
		self.chung_score.text, self.chung_penalty.text, self.hong_score.text, self.hong_penalty.text, self.timer = ('0','0','0','0', 0)
		self.timer_control = 'stop'
		self.time_counter_thread = Thread(target=self.countdown)
		self.time_counter_thread.start()

	def connect_to_server(self):
		if self.server_host.text != '' and self.server_port != '':
			self.s = socket.socket()
			try:
				self.s.connect((self.server_host.text, int(self.server_port.text)))
				self.connection_status.text = 'Connected.'
				self.connection_status.color = [0,1,0,1]
			except:
				print('Connection fails.')
				self.s.close()

	def send_to_server(self, message):
		print(message)
		try:
			self.s.sendall(pickle.dumps(message))	
		except:
			self.connect_to_server()

	# ##########################################################################
	# Settings
	############################################################################
	def countdown(self):
		while True:
			while self.timer >= 0 and self.timer_control == 'start':
				mins, secs = divmod(self.timer, 60)
				self.time_counter.text = '{:02d}:{:02d}'.format(mins, secs)
				try:
					self.send_to_server({'update_time_counter': self.time_counter.text})
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
								self.send_to_server({'update_rest_time_counter': self.rest_time_counter.text})
							except:
								pass
							time.sleep(1)
							rest_duration -= 1

	def set_time(self, text_input):
		ftr = [60,1]
		try:
			self.timer = sum([a*b for a,b in zip(ftr, map(int,text_input.text.split(':')))])
			self.time_counter.text = text_input.text
			self.send_to_server({'update_time_counter': text_input.text})
		except:
			pass

	def set_round(self, text_input):
		self.round_number.text = text_input.text
		self.send_to_server({'update_round_number': text_input.text})
	# ##########################################################################
	# Controls
	############################################################################
	def update_match_number(self, text_input):
		self.send_to_server({'update_match_number': text_input.text})

	def update_category_name(self, text_input):
		self.send_to_server({'update_category_name': text_input.text})

	def update_total_round(self, text_input):
		self.send_to_server({'update_total_round': text_input.text})

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
		self.send_to_server({'update_chung_name': text_input.text})	

	def update_chung_team(self, text_input):
		self.send_to_server({'update_chung_team': text_input.text})

	def add_chung_score(self, button):
		self.chung_score.text = str(int(self.chung_score.text)+1)
		self.send_to_server({'add_chung_score': self.chung_score.text})	

	def minus_chung_score(self, button):
		self.chung_score.text = str(int(self.chung_score.text)-1)
		self.send_to_server({'minus_chung_score': self.chung_score.text})	

	def add_chung_penalty(self, button):
		self.chung_penalty.text = str(int(self.chung_penalty.text)+1)
		self.send_to_server({'add_chung_penalty': self.chung_penalty.text})	

	def minus_chung_penalty(self, button):
		self.chung_penalty.text = str(int(self.chung_penalty.text)-1)
		self.send_to_server({'minus_chung_penalty': self.chung_penalty.text})

	# ##########################################################################
	# HONG
	############################################################################
	def update_hong_name(self, text_input):
		self.send_to_server({'update_hong_name': text_input.text})	

	def update_hong_team(self, text_input):
		self.send_to_server({'update_hong_team': text_input.text})

	def add_hong_score(self, button):
		self.hong_score.text = str(int(self.hong_score.text)+1)
		self.send_to_server({'add_hong_score': self.hong_score.text})	

	def minus_hong_score(self, button):
		self.hong_score.text = str(int(self.hong_score.text)-1)
		self.send_to_server({'minus_hong_score': self.hong_score.text})	

	def add_hong_penalty(self, button):
		self.hong_penalty.text = str(int(self.hong_penalty.text)+1)
		self.send_to_server({'add_hong_penalty': self.hong_penalty.text})	

	def minus_hong_penalty(self, button):
		self.hong_penalty.text = str(int(self.hong_penalty.text)-1)
		self.send_to_server({'minus_hong_penalty': self.hong_penalty.text})



class EssAdmin(App):
	def build(self):
		self.root = AdminRoot()
		return self.root


if __name__ == '__main__':
	EssAdmin().run()