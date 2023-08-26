import ctypes
from datetime import datetime
import os
import time
from commands.bing_wallpaper import bing_wallpaper
import logging

class looks_manager:

# instance attributes
    def __init__(self, log_path = os.path.abspath('bing_wallpaper.log')):
        self.log_path = log_path
        self.try_counter = 0
        self.bing_connection()
        

    def bing_connection(self):
        try:
            bing_wall = bing_wallpaper()
            self.img, self.description = bing_wall.run()
        except Exception as e :
            logging.basicConfig(filename=self.log_path, level=logging.DEBUG)
            logging.debug(f'{datetime.now()}: An error occurred')
            logging.info(f'try_counter: {self.try_counter}. \\The error: {e}')

    def set_wallpaper(self, img=None):
        try:
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, self.img , 0) \
            if  img==None else \
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, img , 0)

        except Exception as e:
            logging.basicConfig(filename=self.log_path, level=logging.DEBUG)
            logging.debug(f'{datetime.now()}: An error occurred')
            logging.info(f'The error: {e}')

        else:
            logging.basicConfig(filename=self.log_path, level=logging.DEBUG)
            logging.debug(f'{datetime.now()}: Wallpaper downloaded and set Successfully')
            logging.info(f'The Wallpaper: {self.img} ,set result: 1')
    


