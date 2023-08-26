import os
import sys
import sqlite3
import subprocess
import time

import requests
# from main import wallpaper
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from commands.wallpaper_manager import looks_manager


class PictureViewerApp(QMainWindow):
    try_counter = 0

    def __init__(self):
        super().__init__()

        self.init_ui()

        # Load pictures from the database on startup
        self.load_pictures()

    def init_ui(self):
        self.setWindowTitle('Bing Picture Viewer')
        self.setWindowIcon(QIcon('bing_app.png'))
        self.setFixedSize(800, 500)  # Set a fixed size for the main window
        self.setStyleSheet('background-color: black; color: white;')

        # Set window dimensions
        window_width = 560
        window_height = 530
        self.setGeometry(0, 0, window_width, window_height)

        # Get the screen dimensions
        screen = app.primaryScreen()
        screen_geometry = screen.availableGeometry()

        # Calculate the position for the bottom-left corner
        bottom_left_x = screen_geometry.left() + window_width
        bottom_left_y = screen_geometry.bottom() - window_height

        # Move the window to the specified position
        self.move(bottom_left_x, bottom_left_y)

        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()

        # Picture display window
        self.picture_label = QLabel()
        self.picture_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.picture_label, 1)

        # Date and Description window (non-editable)
        self.info_browser = QTextBrowser()
        self.info_browser.setStyleSheet('QTextBrowser { background-color: black; color: white; font-size: 14px; padding: 10px; border: 2px solid #888888; border-radius: 10px; }')
        main_layout.addWidget(self.info_browser)

        # Previous, Next, and Refresh buttons
        buttons_layout = QHBoxLayout()

        self.prev_button = QPushButton('Older', clicked=self.show_previous_picture)
        self.prev_button.setStyleSheet('QPushButton { background-color: #888888; color: white; font-size: 16px; padding: 10px 30px; border: none; border-radius: 15px; }'
                                       'QPushButton:disabled { background-color: #555555; color: #888888; font-size: 16px; padding: 10px 30px; border: none; border-radius: 15px; }')
        buttons_layout.addWidget(self.prev_button)

        self.next_button = QPushButton('Newer', clicked=self.show_next_picture)
        self.next_button.setStyleSheet('QPushButton { background-color: #888888; color: white; font: georgia; font-size: 16px; padding: 10px 30px; border: none; border-radius: 15px; }'
                                       'QPushButton:disabled { background-color: #555555; color: #888888; font-size: 16px; padding: 10px 30px; border: none; border-radius: 15px; }')
        buttons_layout.addWidget(self.next_button)

        self.refresh_button = QPushButton('Refresh', clicked=self.run_update_script)
        self.refresh_button.setStyleSheet('background-color: #888888; color: white; font-size: 16px; padding: 10px 30px; border: none; border-radius: 15px;')
        buttons_layout.addWidget(self.refresh_button)

        main_layout.addLayout(buttons_layout)

        main_widget.setLayout(main_layout)

    def load_pictures(self):
        try:
            conn = sqlite3.connect("bing_picture_database.db")
            cursor = conn.cursor()
            cursor.execute('SELECT picture_path, date, description FROM bing_pictures ORDER BY id DESC')
            # cursor.execute("SELECT picture_path, date, description FROM bing_pictures")
            picture_data = cursor.fetchall()
            conn.close()

            self.pictures = picture_data
            self.current_picture_index = 0
            self.show_current_picture()
            self.update_button_states()
        except sqlite3.Error as e:
            print("Error reading data from the database:", e)

    def show_current_picture(self):
        if not self.pictures:
            self.picture_label.clear()
            self.info_browser.clear()
            return

        picture_path, date, description = self.pictures[self.current_picture_index]

        # Display the picture
        pixmap = QPixmap(picture_path)
        self.picture_label.setPixmap(pixmap.scaledToWidth(800))

        # Display date and description
        info_text = f"{date}\n\n{description}"
        self.info_browser.setPlainText(info_text)

    def show_previous_picture(self):
        if not self.pictures:
            return
        self.current_picture_index = min(len(self.pictures) - 1, self.current_picture_index + 1)

        self.set_wallpaper(self.pictures[self.current_picture_index][0])
        self.show_current_picture()
        self.update_button_states()

    def show_next_picture(self):
        if not self.pictures:
            return
        self.current_picture_index = max(0, self.current_picture_index - 1)

        self.set_wallpaper(self.pictures[self.current_picture_index][0])
        self.show_current_picture()
        self.update_button_states()

    def update_button_states(self):
        self.next_button.setEnabled(self.current_picture_index > 0)
        self.prev_button.setEnabled(self.current_picture_index < len(self.pictures) - 1)

    def check_internet_connection(self):
        try:
            requests.get("http://www.google.com", timeout=5)  # Change the URL to a reliable server
            return True
        except requests.RequestException:
            return False

    def run_update_script(self):
        try:
            
            if self.check_internet_connection():
                subprocess.run(["python", "main.pyw"])
            else: \
                pass
            # Replace "main.py" with the path to your main script
        except Exception as e:
            # print("Error running update script:", e)
            pass
        
        # Reload the pictures after running the update script
        self.set_wallpaper(self.pictures[0][0])
        self.load_pictures()

    def set_wallpaper(self, image_path):
        try:
            wallpaper = looks_manager(log_path = os.path.abspath('bing_wallpaper.log'))
            wallpaper.set_wallpaper(image_path)
        except Exception as e:
            print("Error setting wallpaper:", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Apply the Fusion style for a black and white theme

    picture_viewer = PictureViewerApp()
    picture_viewer.show()

    sys.exit(app.exec_())
