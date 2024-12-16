
from pynput.mouse import Controller, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController

mouse = Controller()
keyboard = KeyboardController()


class Operation ():
    def __init__(self):
        pass

    def active_game_window():

        pass

    def open_store(self):
        pg.hotkey('win', 'r')
        pg.typewrite('https://www.dnfgame.com/')
        pg.press('enter')

    def trigger_package(self):
        pg.keyDown('i')
