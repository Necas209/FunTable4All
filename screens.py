from kivy.input import MotionEvent
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen


class BaseScreen(Screen):
    pass


class GoBackScreen(BaseScreen):
    def go_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = self.manager.previous()


class StartScreen(BaseScreen):
    def bt_start(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'menu_sc'


class MenuScreen(GoBackScreen):
    def bt_play(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'modes_sc'


class ModesScreen(GoBackScreen):
    def bt_numbers(self):
        play_sc = PlayScreen(name='play_sc1')
        play_sc.play_img = 'images/numbers/number1.png'
        self.manager.add_widget(play_sc)
        self.manager.current = 'play_sc1'


def bind_screens(screen: BaseScreen, sc_name: str) -> None:
    screen.bind(score=screen.manager.get_screen(sc_name).setter('score'))
    if 'final_sc' not in sc_name:
        screen.bind(round_no=screen.manager.get_screen(sc_name).setter('round_no'))
    screen.bind(no_rounds=screen.manager.get_screen(sc_name).setter('no_rounds'))
    for prop in ['score', 'round_no', 'no_rounds']:
        screen.property(prop).dispatch(screen)


class PlayScreen(BaseScreen):
    play_img = StringProperty()
    score = NumericProperty(0)
    round_no = NumericProperty(1)
    no_rounds = NumericProperty(1)

    def on_motion(self, etype: str, me: MotionEvent):
        print(me.type_id, me.profile)

    def on_enter(self, *args):
        if issubclass(type(self.manager.previous()), CheckScreen):
            self.manager.remove_widget(self.manager.previous())

    def bt_check_play(self, result):
        check_sc_name = f'check_sc{self.round_no}'
        if result:
            self.score = self.score + 1
            check_sc = RightScreen(name=check_sc_name)
        else:
            check_sc = WrongScreen(name=check_sc_name)
        self.manager.add_widget(check_sc)
        self.bind(play_img=self.manager.get_screen(check_sc_name).setter('play_img'))
        self.property('play_img').dispatch(self)
        bind_screens(self, check_sc_name)
        self.manager.current = check_sc_name


class CheckScreen(BaseScreen):
    play_img = StringProperty()
    score = NumericProperty(0)
    round_no = NumericProperty(1)
    no_rounds = NumericProperty(5)

    def bt_continue(self):
        if self.round_no == self.no_rounds:
            final_sc_name = 'final_sc'
            final_sc = FinalScreen(name=final_sc_name)
            self.manager.add_widget(final_sc)
            bind_screens(self, final_sc_name)
            self.manager.current = final_sc_name
        else:
            self.round_no = self.round_no + 1
            play_sc_name = f'play_sc{self.round_no}'
            play_sc = PlayScreen(name=play_sc_name)
            self.manager.add_widget(play_sc)
            bind_screens(self, play_sc_name)
            play_sc.play_img = f'images/numbers/number{self.round_no}.png'
            self.manager.current = play_sc_name


class RightScreen(CheckScreen):
    pass


class WrongScreen(CheckScreen):
    def bt_redo(self):
        self.manager.current = f'play_sc{self.round_no}'
        self.manager.remove_widget(self)


class FinalScreen(BaseScreen):
    score = NumericProperty(0)
    no_rounds = NumericProperty(5)

    def bt_new_game(self):
        sm = self.manager
        sm.clear_widgets()
        start_sc = StartScreen(name='start_sc')
        menu_sc = MenuScreen(name='menu_sc')
        modes_sc = ModesScreen(name='modes_sc')
        sm.add_widget(start_sc)
        sm.add_widget(menu_sc)
        sm.add_widget(modes_sc)
        sm.current = 'modes_sc'
