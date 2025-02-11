
from time import sleep
import pygetwindow as gw
from discord_winhook.base import BaseHook
import pyautogui as pag
import io
class ScreenshotHook(BaseHook):
    def __init__(self, url : str, window : str | gw.Win32Window):
        super().__init__(url)
        self.__window : gw.Win32Window = gw.getWindowsWithTitle(window)[0] if isinstance(window, str) else window

    def construct_files(self):
        try:
            self.__window.activate()
        except: #noqa
            pass
        sleep(0.4)
        scontent = pag.screenshot(region=(self.__window.left, self.__window.top, self.__window.width, self.__window.height))
        # image to bytes
        img_byte_arr = io.BytesIO()
        scontent.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        return img_byte_arr