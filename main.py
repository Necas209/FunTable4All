import kivy
from kivy.uix.widget import Widget

kivy.require('1.0.9')


from kivy.app import App


class StartPage(Widget):
    def __init__(self):
        super().__init__()


class GameApp(App):
    def build(self):
        return StartPage()


if __name__ == '__main__':
    GameApp().run()
