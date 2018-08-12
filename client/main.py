import pickle
import socket
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class SettingPopup(Popup):
    connection_status = ObjectProperty()
    def __init__(self, arg):
        super(SettingPopup, self).__init__()

    def on_host_changed(self, textinput):
        self.host = textinput.text
        
    def on_port_changed(self, textinput):
        self.port = textinput.text
    
    def on_connect_btn_pressed(self, button):
        app = App.get_running_app()
        app.root.try_connect()
    
    def on_close_btn_pressed(self, button):
        self.dismiss()

class ClientRoot(BoxLayout):
    action_bar_title = ObjectProperty()
    chung_score = ObjectProperty()
    hong_score = ObjectProperty()

    def __init__(self, **kwargs):
        super(ClientRoot, self).__init__(**kwargs)
        self.popup = SettingPopup(self)

    def open_setting_modal(self):
        self.popup.open()

    def try_connect(self, *args):
        try:
            server = (self.popup.host, int(self.popup.port))
            self.s = socket.socket()
            self.s.connect(server)
            self.action_bar_title.title = self.popup.connection_status.text = 'Connected'
        except:
            self.action_bar_title.title = self.popup.connection_status.text = 'Disconnected'

    def score(self, side, point):
        message = {side: point}
        print('Sending: ', message)
        try:
            self.s.sendall(pickle.dumps(message))
        except:
            self.action_bar_title.title = self.popup.connection_status.text = 'Disconnected'

class EssClient(App):

    def build(self):
        self.root = ClientRoot()
        return self.root

if __name__ == '__main__':
    EssClient().run() 