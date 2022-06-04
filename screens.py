import random

from kivy.core.window import Window
from kivy.input import MotionEvent
from kivy.input.providers.tuio import Tuio2dObjMotionEvent
from kivy.properties import NumericProperty, StringProperty, ListProperty
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
        no_rounds = 5
        numbers = random.sample(range(1, 10), no_rounds)  # Should be 11
        play_sc = PlayScreen(name='play_sc1')
        play_sc.numbers = numbers
        self.manager.add_widget(play_sc)
        self.manager.current = 'play_sc1'


def bind_screens(screen: BaseScreen, sc_name: str) -> None:
    screen.bind(score=screen.manager.get_screen(sc_name).setter('score'))
    if sc_name != 'final_sc':
        screen.bind(round_no=screen.manager.get_screen(sc_name).setter('round_no'))
        screen.bind(numbers=screen.manager.get_screen(sc_name).setter('numbers'))
    for prop in ['score', 'round_no', 'numbers']:
        screen.property(prop).dispatch(screen)


class PlayScreen(BaseScreen):
    event_counter = NumericProperty(0)
    play_img = StringProperty()
    numbers = ListProperty()
    score = NumericProperty(0)
    round_no = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_motion=self.on_motion)

    def on_motion(self, window: Window, etype: str, me: MotionEvent):
        if isinstance(me, Tuio2dObjMotionEvent) and self.event_counter == 0:
            self.event_counter += 1
            check_sc_name = f'check_sc{self.round_no}'
            number: int = self.numbers[self.round_no - 1]
            if number == me.fid:
                self.score = self.score + 1
                check_sc = RightScreen(name=check_sc_name)
            else:
                check_sc = WrongScreen(name=check_sc_name)
            self.manager.add_widget(check_sc)
            bind_screens(self, check_sc_name)
            self.manager.current = check_sc_name

    def on_enter(self, *args):
        self.play_img = f'images/numbers/number{self.numbers[self.round_no - 1]}.png'
        if issubclass(type(self.manager.previous()), CheckScreen):
            self.manager.remove_widget(self.manager.previous())


class CheckScreen(BaseScreen):
    play_img = StringProperty()
    numbers = ListProperty()
    score = NumericProperty(0)
    round_no = NumericProperty(1)

    def on_enter(self, *args):
        self.play_img = f'images/numbers/number{self.numbers[self.round_no - 1]}.png'

    def bt_continue(self):
        if self.round_no == len(self.numbers):
            sc_name = 'final_sc'
            next_sc = FinalScreen(name=sc_name)
            next_sc.no_rounds = len(self.numbers)
        else:
            self.round_no = self.round_no + 1
            sc_name = f'play_sc{self.round_no}'
            next_sc = PlayScreen(name=sc_name)
        self.manager.add_widget(next_sc)
        bind_screens(self, sc_name)
        self.manager.current = sc_name


class RightScreen(CheckScreen):
    pass


class WrongScreen(CheckScreen):
    def bt_redo(self):
        play_sc_name = f'play_sc{self.round_no}'
        play_sc: PlayScreen = self.manager.get_screen(play_sc_name)
        play_sc.event_counter = 0
        self.manager.current = play_sc_name
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
