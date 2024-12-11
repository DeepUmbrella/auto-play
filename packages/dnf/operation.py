
import pyautogui as pg


class Operation ():
    def __init__(self):
        pass

    def open_store(self):
        pg.hotkey('win', 'r')
        pg.typewrite('https://www.dnfgame.com/')
        pg.press('enter')

    def trigger_package(self):
        pg.keyDown('i')
