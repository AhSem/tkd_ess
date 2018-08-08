from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.lang import Builder

Builder.load_string('''
<Demo>:
    cols: 1

    BoxLayout:
        Button:
			id: "Bluehead"
            size_hint_x: 0.5
            text: 'Tap(Swipe)Head 2'
			background_color: 0,2,3,1
	
        Button:
			id: "Redhead"
            size_hint_x: 0.5
            text: 'Tap(Swipe)Head'
			background_color: 2,0,0,1

    BoxLayout:
        Button:
			id: "BlueBody"
            size_hint_x: 0.5
            text: 'Tap(Swipe)Body 3'
			background_color: 0,2,3,1

        Button:
			id: "RedBody"
            size_hint_x: 0.5
            text: 'Tap(Swipe)Body'
			background_color: 2,0,0,1

''')


class Demo(GridLayout):
    pass


class DemoApp(App):
    def build(self):
        return Demo()


if __name__ == '__main__':
    DemoApp().run()

	