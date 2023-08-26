import sqlite3
import os
from PIL import Image
from datetime import datetime

class BingPictureDatabase:
    def __init__(self, db_file=os.path.abspath('bing_picture_database.db')):
        self.db_file = db_file
        self.create_table()

    def create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bing_pictures (
                id INTEGER PRIMARY KEY,
                picture_path TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                link TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def check_db(self, description):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM bing_pictures WHERE description = ?', (description,))
        existing_id = cursor.fetchone()
        conn.close()

        return existing_id 
    
    def get_path(self, id):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT picture_path FROM bing_pictures WHERE id = ?', (id,))
        existing_id = cursor.fetchone()
        conn.close()

        return existing_id 

    def insert_bing_picture(self, picture_path, description, link, current_date = datetime.now().strftime('%a %d %b %Y')):
        

        # Check if the image path already exists in the database
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM bing_pictures WHERE description = ?', (description,))
        existing_id = cursor.fetchone()
        conn.close()

        if existing_id:
            # If the image path already exists, update the description and link
            existing_id = existing_id[0]
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE bing_pictures
                SET description = ?, link = ?
                WHERE id = ?
            ''', (description, link, existing_id))
            conn.commit()
            conn.close()
        else:
            # If the image path doesn't exist, insert a new entry
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bing_pictures (picture_path, date, description, link)
                VALUES (?, ?, ?, ?)
            ''', (picture_path, current_date, description, link))
            conn.commit()
            conn.close()

    def retrieve_bing_pictures(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT picture_path, date, description, link FROM bing_pictures ORDER BY id DESC')

        # cursor.execute('SELECT picture_path, date, description, link FROM bing_pictures')
        data = cursor.fetchall()
        conn.close()

        pictures_data = []
        for row in data:
            picture_path, date, description, link = row
            image = Image.open(picture_path)
            pictures_data.append((image, date, description, link))

        return pictures_data
    
    def remove(self, filename):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM bing_pictures WHERE picture_path = ?', (filename,))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    # Assuming you have image files called "picture1.jpg", "picture2.jpg", etc., in the same directory as this script.
    picture_paths = [r"C:\Users\mine\Pictures\bing\bing-25-07-2023.png",
                    r"C:\Users\mine\Pictures\bing\IMG_0308.JPG", 
                    r"C:\Users\mine\Pictures\Saved Pictures\WEB Mak-2.png"]  # Replace with actual file paths
    descriptions = ["Description 1", "Description 2", "Description 3"]  # Replace with descriptions for each picture
    links = ["https://chat.openai.com/?model=text-davinci-002-render-sha",
              "https://chat.openai.com/?model=text-davinci-002-render-sha",
                "https://chat.openai.com/?model=text-davinci-002-render-sha"]  # Replace with links for each picture

    # Create an instance of the BingPictureDatabase class
    bing_db = BingPictureDatabase()

    # Insert pictures into the database
    for i in range(len(picture_paths)):
        bing_db.insert_bing_picture(picture_paths[i], descriptions[i], links[i])

    # Retrieve and display pictures from the database
    bing_pictures = bing_db.retrieve_bing_pictures()
    for i, (image, date, description, link) in enumerate(bing_pictures):
        print(f"Picture {i + 1}")
        print(f"Date: {date}")
        print(f"Description: {description}")
        print(f"Link: {link}")
        image.show()
