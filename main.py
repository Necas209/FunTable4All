from kivy.app import App
from kivy.uix.widget import Widget


class StartPage(Widget):
    def __init__(self):
        super().__init__()


class GameApp(App):
    def build(self):
        return StartPage()


if __name__ == '__main__':
    GameApp().run()
