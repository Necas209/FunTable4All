from kivy import Config
from kivy.core.text import LabelBase
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from screens import StartScreen, MenuScreen, ModesScreen


class GameApp(MDApp):
    no_rounds = NumericProperty(5)
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        Config.set('input', 'fun_table', 'tuio,127.0.0.1:3333')
        self.icon = 'images/app_logo.png'
        sm = ScreenManager()
        start_sc = StartScreen(name='start_sc')
        menu_sc = MenuScreen(name='menu_sc')
        modes_sc = ModesScreen(name='modes_sc')
        sm.add_widget(start_sc)
        sm.add_widget(menu_sc)
        sm.add_widget(modes_sc)
        return sm


if __name__ == '__main__':
    LabelBase.register(name='Comic Neue',
                       fn_regular='fonts/ComicNeue-Bold.ttf',
                       fn_bold='fonts/ComicNeue-Bold.ttf',
                       fn_italic='fonts/ComicNeue-Italic.ttf',
                       fn_bolditalic='fonts/ComicNeue-BoldItalic.ttf')
    GameApp().run()
