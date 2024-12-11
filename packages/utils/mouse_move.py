import pyautogui as pg


if __name__ == '__main__':

    while True:
        # Get the current mouse position
        x, y = pg.position()

        # Print the mouse position
        print(f"Mouse position: ({x}, {y})")
        # Wait for 1 second
        pg.sleep(3)
