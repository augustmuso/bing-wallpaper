# Bing Wallpaper App Read Me

## Overview

This Python application allows users to download and set Bing wallpapers as their desktop wallpapers. The app also features a simple database for photo storage, allowing users to reset old photos and fetch new ones on refresh.

## Features

1. **Bing Wallpaper Retrieval**: The app fetches the latest Bing wallpaper and downloads it to the local machine.

2. **Desktop Wallpaper Setting**: Sets the downloaded Bing wallpaper as the desktop wallpaper, providing users with a fresh and dynamic background.

3. **Simple Database**: The app includes a basic database for storing downloaded Bing wallpapers. This allows users to manage and reset their wallpaper history.

4. **Reset Functionality**: Users can reset their wallpaper history, removing all stored images from the database.

5. **Refresh Functionality**: The app can fetch new Bing wallpapers on demand, providing users with the option to update their desktop background manually.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Required Python packages (specified in the `requirements.txt` file)

Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Application:**

   ```bash
   python main.py
   ```
   Or
   ```bash
   python main.pyw
   ```

2. **Main Menu:**

   Upon running the application, you will be presented with a main menu that provides options for downloading, setting, resetting, and refreshing wallpapers.

3. **Download Wallpaper:**

   Choose the option to download the latest Bing wallpaper. The app will save the image to the specified directory.

4. **Set Desktop Wallpaper:**

   Select the option to set the downloaded wallpaper as the desktop background.

5. **Reset Wallpaper History:**

   Use this option to reset the wallpaper history stored in the database.

6. **Refresh Wallpaper:**

   Fetch new Bing wallpapers manually by choosing the refresh option.

## Configuration

- The app allows for configuration of the download directory and other settings in the `config.py` file.

## Notes

- Make sure your machine has internet connectivity to download Bing wallpapers.
- The app may need appropriate permissions to set the desktop wallpaper.

## Contributing

Feel free to contribute to the development of this application. Open issues, submit pull requests, and provide feedback to help improve the functionality.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
