import os
import time

import requests
from commands.wallpaper_manager import looks_manager

wallpaper = looks_manager(log_path = os.path.abspath('bing_wallpaper.log'))
counter = 0

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)  # Change the URL to a reliable server
        return True
    except requests.RequestException:
        return False

def run_update_script(counter = counter):
    if not check_internet_connection() :
        while counter < 6:
            # print("No internet connection. Waiting for 5 minutes before trying again...")
            time.sleep(300)  # Wait for 5 minutes (300 seconds)
            counter += 1
            print(counter)
            run_update_script()  # Run the function again
    else:
        wallpaper.set_wallpaper()
        print("its done.")

run_update_script()