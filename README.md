# Weather App (Tkinter + OpenWeatherMap)

A beautiful, modern weather application built with Python's Tkinter GUI toolkit. It fetches real-time weather data from the OpenWeatherMap API and displays:
- City and country (full name)
- Weather icon and description
- Temperature (current, min/max, feels like)
- Humidity, wind speed
- Local time of the city
- Date and time of the last update
- Autocomplete for city names
- Responsive, scrollable, and user-friendly interface

---

## Features
- Modern, attractive UI with weather icons and emojis
- Local time display for the selected city
- Full country name display
- Autocomplete city search
- Loading spinner and error handling
- Scrollable output for small windows
- Fade-in animation for results
- Clear button to reset the UI
- Current system time display

---

## Prerequisites
- Python 3.7 or higher
- [OpenWeatherMap API key](https://openweathermap.org/appid)

---

## Installation
1. **Clone or download this repository**
   ```bash
   git clone <your-github-repo-url>
   cd <repo-folder>
   ```

2. **Install required Python packages**
   ```bash
   pip install requests pillow
   ```

3. **Configure your API key**
   - Open `config.ini` and set your OpenWeatherMap API key:
     ```ini
     [Default]
     api=YOUR_API_KEY_HERE
     ```

---

## Usage
1. **Run the app**
   ```bash
   python sample.py
   ```

2. **Type a city name**
   - Use the autocomplete dropdown for suggestions.
   - Click "Search Weather".

3. **View results**
   - See weather details, local time, and more in a modern UI.
   - If the window is small, scroll to see all information.

4. **Clear**
   - Click "Clear" to reset the form and results.

---

## Notes
- The app uses `weather_icon.png` for displaying weather icons. This is downloaded automatically as needed.
- If you want to add more cities to the autocomplete, edit the `city_list` in `sample.py`.
- For best results, use a valid OpenWeatherMap API key.
- The app is fully resizable and supports scrolling for small windows.

---

## Credits
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Pillow (PIL)](https://python-pillow.org/)
- Tkinter (Python standard library)

---

## Contributing
Pull requests and suggestions are welcome!

---

<!-- Maintainer and author details intentionally omitted for privacy in public repositories. -->
