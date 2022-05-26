from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp


class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        Window.size = (700, 800)

    def bt_start(self):
        self.manager.current = 'menu_sc'


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def bt_play(self):
        self.manager.current = 'games_sc'


class GamesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GameApp(MDApp):
    def build(self):
        sm = ScreenManager()
        start_sc = StartScreen(name='start_sc')
        menu_sc = MenuScreen(name='menu_sc')
        games_sc = GamesScreen(name='games_sc')
        sm.add_widget(start_sc)
        sm.add_widget(menu_sc)
        sm.add_widget(games_sc)
        return sm


if __name__ == '__main__':
    LabelBase.register(name='Comic Neue',
                       fn_regular='fonts/ComicNeue-Bold.ttf',
                       fn_bold='fonts/ComicNeue-Bold.ttf',
                       fn_italic='fonts/ComicNeue-Italic.ttf',
                       fn_bolditalic='fonts/ComicNeue-BoldItalic.ttf')
    GameApp().run()
