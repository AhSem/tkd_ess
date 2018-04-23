from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class AdminRoot(BoxLayout):
	pass		

class EssAdmin(App):
	def build(self):
		self.root = AdminRoot()
		return self.root


if __name__ == '__main__':
	EssAdmin().run()