import requests, urllib.request, os, random, sys
from datetime import datetime
from db.db import BingPictureDatabase

class bing_wallpaper:
    # class attribute
    link = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US"
    # Get the current working directory
    current_directory = os.getcwd()
    # Specify the folder name
    folder_name = "pics"
    storage_link = os.path.join(current_directory, folder_name)
    site = 'bing'

    # instance attribute
    def __init__(self, bing_db = BingPictureDatabase(db_file=os.path.abspath('bing_picture_database.db'))):
        # self.fname = fname
        self.desription = ''
        self.bing_db = bing_db


    def run(self):
        self.download_daily_image()
        self.delete_more_than_7()
        return self.filename, self.desription

    def download_daily_image(self):
        response = requests.get(self.link).json()
        url = "https://bing.com" + response['images'][0]['url']
        self.desription = response['images'][0]['copyright']
        fileName = datetime.now().strftime("bing-%d-%m-%Y")
        self.filename = os.path.join(self.storage_link, f"{fileName}.png")
        current_date = datetime.strptime(response['images'][0]['startdate'], '%Y%m%d').strftime('%a %d %b %Y')
        # print(current_date)

        if not self.bing_db.check_db(self.desription):

            self.filename, _ = urllib.request.urlretrieve(url, self.filename)

            self.bing_db.insert_bing_picture(self.filename, self.desription, url, current_date)

        else:
            self.filename = self.bing_db.get_path(self.bing_db.check_db(self.desription)[0])[0]

        return self.filename
    
    def delete_more_than_7(self):
        files = os.listdir(self.storage_link)
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.storage_link, x)), reverse=True)
        # print(files)
        for file_name in files[7:]:
            # print(os.path.join(self.storage_link, file_name))
            os.remove(os.path.join(self.storage_link, file_name))
            self.bing_db.remove(os.path.join(self.storage_link, file_name))



if __name__ == "__main__":
    
    bing_wall = bing_wallpaper()
    bing_wall.run()
