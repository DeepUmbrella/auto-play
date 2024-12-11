
import time
import pygetwindow as gw
import pyautogui as pg


class ScreenMatch:
    """
    Class to represent a target on the screen.
    """

    def __init__(self, *args):

        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.scaling = 1
        self.win = None

        if len(args) == 1 and isinstance(args[0], str):
            window_title = args[0]
            """
            find window by game name
            """

            retry_count = 0
            window_size = None
            while retry_count < 5 and window_size is None:
                window_size = self.get_target_window(window_title)
                print(window_size, "GET WINDOW SIZE")
                if window_size is None:
                    retry_count += 1
                    print("未检测到游戏窗口，重试中...")
                    time.sleep(5)
                if window_size is not None:
                    self.x, self.y, self.width, self.height = window_size
                    print("检测到游戏窗口,", window_size)
            if retry_count >= 5 and window_size is None:
                print("未找到游戏窗口，请检查游戏是否已启动。")
        elif len(args) == 4 and all(isinstance(arg, int) for arg in args):

            x, y, width, height = args
            self.x = x
            self.y = y
            self.width = width
            self.height = height
        else:
            raise ValueError("Invalid arguments for ScreenTarget")

    @property
    def size(self):
        return self.x, self.y, self.width, self.height

    @property
    def size_enable(self):
        return self.width != 0 and self.height != 0

    def get_center(self):
        """
        Returns the center of the target.
        """
        return self.x + self.width / 2, self.y + self.height / 2

    def get_top_left(self):
        """
        Returns the top left corner of the target.
        """
        return self.x, self.y

    def get_target_window(self, game_name: str):

        all_windows = gw.getWindowsWithTitle(game_name)
        # allanywindows = gw.getAllWindows()

        for win in all_windows:
            left = win.left
            top = win.top
            width = win.width
            height = win.height

            if width != 0 and height != 0:
                self.win = win
                return left, top, width, height
        return None

    def window_active(self):
        if self.win is not None:
            self.win.activate()
        elif self.size_enable:
            pg.click(self.get_center())

    def window_close(self):
        if self.win is not None:
            self.win.close()

    def window_maximize(self):
        if self.win is not None:
            self.win.maximize()

    def window_minimize(self):
        if self.win is not None:
            self.win.minimize()
