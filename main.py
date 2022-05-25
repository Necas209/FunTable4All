from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.app import MDApp


class StartPage(Widget):
    def __init__(self):
        super().__init__()


class GameApp(MDApp):
    def build(self):
        return StartPage()


if __name__ == '__main__':
    LabelBase.register(name='Comic Neue',
                       fn_regular='fonts/ComicNeue-Bold.ttf',
                       fn_bold='fonts/ComicNeue-Bold.ttf',
                       fn_italic='fonts/ComicNeue-Italic.ttf',
                       fn_bolditalic='fonts/ComicNeue-BoldItalic.ttf')
    Window.size = (600, 800)
    GameApp().run()
