# import required modules
from configparser import ConfigParser
import requests
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
import time
from datetime import datetime, timedelta

# extract key from the
# configuration file
config_file = "config.ini"
config = ConfigParser()
config.read(config_file)
api_key = config['Default']['api']
url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'

# Helper: Country code to full name
COUNTRY_NAMES = {
    'IN': 'India', 'US': 'United States', 'GB': 'United Kingdom', 'FR': 'France', 'DE': 'Germany',
    'RU': 'Russia', 'CN': 'China', 'JP': 'Japan', 'CA': 'Canada', 'AU': 'Australia', 'BR': 'Brazil',
    'IT': 'Italy', 'ES': 'Spain', 'TR': 'Turkey', 'MX': 'Mexico', 'KR': 'South Korea', 'ID': 'Indonesia',
    'SA': 'Saudi Arabia', 'SG': 'Singapore', 'AE': 'United Arab Emirates', 'TH': 'Thailand',
    'ZA': 'South Africa', 'AR': 'Argentina', 'NG': 'Nigeria', 'EG': 'Egypt', 'PK': 'Pakistan',
    'BD': 'Bangladesh', 'NL': 'Netherlands', 'SE': 'Sweden', 'CH': 'Switzerland', 'PL': 'Poland',
    'BE': 'Belgium', 'NO': 'Norway', 'FI': 'Finland', 'IE': 'Ireland', 'NZ': 'New Zealand',
    'UA': 'Ukraine', 'AT': 'Austria', 'DK': 'Denmark', 'GR': 'Greece', 'PT': 'Portugal',
    'IL': 'Israel', 'MY': 'Malaysia', 'PH': 'Philippines', 'VN': 'Vietnam', 'CO': 'Colombia',
    'CL': 'Chile', 'CZ': 'Czech Republic', 'HU': 'Hungary', 'RO': 'Romania', 'SK': 'Slovakia',
    'BG': 'Bulgaria', 'HR': 'Croatia', 'SI': 'Slovenia', 'RS': 'Serbia', 'KZ': 'Kazakhstan',
    'IR': 'Iran', 'IQ': 'Iraq', 'QA': 'Qatar', 'KW': 'Kuwait', 'OM': 'Oman', 'LB': 'Lebanon',
    'JO': 'Jordan', 'MA': 'Morocco', 'DZ': 'Algeria', 'TN': 'Tunisia', 'KE': 'Kenya', 'GH': 'Ghana',
    'ET': 'Ethiopia', 'TZ': 'Tanzania', 'UG': 'Uganda', 'SD': 'Sudan', 'SN': 'Senegal', 'CM': 'Cameroon',
    'ZW': 'Zimbabwe', 'ZM': 'Zambia', 'AO': 'Angola', 'CI': 'Ivory Coast', 'ML': 'Mali', 'NE': 'Niger',
    'LY': 'Libya', 'CD': 'Congo', 'MG': 'Madagascar', 'MZ': 'Mozambique', 'BW': 'Botswana',
    'NA': 'Namibia', 'MW': 'Malawi', 'LS': 'Lesotho', 'SZ': 'Eswatini', 'SL': 'Sierra Leone',
    'LR': 'Liberia', 'GM': 'Gambia', 'GW': 'Guinea-Bissau', 'GQ': 'Equatorial Guinea', 'ST': 'Sao Tome and Principe',
    'CV': 'Cape Verde', 'DJ': 'Djibouti', 'ER': 'Eritrea', 'SO': 'Somalia', 'CF': 'Central African Republic',
    'GA': 'Gabon', 'CG': 'Republic of the Congo', 'TD': 'Chad', 'MR': 'Mauritania', 'BJ': 'Benin',
    'TG': 'Togo', 'BF': 'Burkina Faso', 'SS': 'South Sudan', 'RW': 'Rwanda', 'BI': 'Burundi',
    'KM': 'Comoros', 'SC': 'Seychelles', 'MU': 'Mauritius', 'YT': 'Mayotte', 'RE': 'Reunion',
    'SH': 'Saint Helena', 'CV': 'Cape Verde', 'GL': 'Greenland', 'IS': 'Iceland', 'MC': 'Monaco',
    'LI': 'Liechtenstein', 'SM': 'San Marino', 'VA': 'Vatican City', 'LU': 'Luxembourg', 'MT': 'Malta',
    'EE': 'Estonia', 'LV': 'Latvia', 'LT': 'Lithuania', 'MD': 'Moldova', 'GE': 'Georgia', 'AM': 'Armenia',
    'AZ': 'Azerbaijan', 'BY': 'Belarus', 'AL': 'Albania', 'MK': 'North Macedonia', 'BA': 'Bosnia and Herzegovina',
    'ME': 'Montenegro', 'XK': 'Kosovo', 'CY': 'Cyprus', 'PS': 'Palestine', 'AF': 'Afghanistan',
    'TM': 'Turkmenistan', 'UZ': 'Uzbekistan', 'TJ': 'Tajikistan', 'KG': 'Kyrgyzstan', 'MN': 'Mongolia',
    'BT': 'Bhutan', 'NP': 'Nepal', 'LK': 'Sri Lanka', 'MM': 'Myanmar', 'KH': 'Cambodia', 'LA': 'Laos',
    'BN': 'Brunei', 'TL': 'Timor-Leste', 'PG': 'Papua New Guinea', 'FJ': 'Fiji', 'SB': 'Solomon Islands',
    'VU': 'Vanuatu', 'NC': 'New Caledonia', 'PF': 'French Polynesia', 'WS': 'Samoa', 'TO': 'Tonga',
    'TV': 'Tuvalu', 'KI': 'Kiribati', 'NR': 'Nauru', 'FM': 'Micronesia', 'MH': 'Marshall Islands',
    'PW': 'Palau', 'CK': 'Cook Islands', 'NU': 'Niue', 'TK': 'Tokelau', 'WF': 'Wallis and Futuna',
    'AS': 'American Samoa', 'GU': 'Guam', 'MP': 'Northern Mariana Islands', 'VI': 'U.S. Virgin Islands',
    'PR': 'Puerto Rico', 'BM': 'Bermuda', 'KY': 'Cayman Islands', 'VG': 'British Virgin Islands',
    'TC': 'Turks and Caicos Islands', 'AI': 'Anguilla', 'MS': 'Montserrat', 'BL': 'Saint Barthelemy',
    'MF': 'Saint Martin', 'PM': 'Saint Pierre and Miquelon', 'GF': 'French Guiana', 'SR': 'Suriname',
    'AN': 'Netherlands Antilles', 'BQ': 'Caribbean Netherlands', 'CW': 'Curacao', 'SX': 'Sint Maarten',
    'AW': 'Aruba', 'BB': 'Barbados', 'BS': 'Bahamas', 'AG': 'Antigua and Barbuda', 'DM': 'Dominica',
    'GD': 'Grenada', 'KN': 'Saint Kitts and Nevis', 'LC': 'Saint Lucia', 'VC': 'Saint Vincent and the Grenadines',
    'TT': 'Trinidad and Tobago', 'JM': 'Jamaica', 'HT': 'Haiti', 'DO': 'Dominican Republic', 'CU': 'Cuba',
    'MQ': 'Martinique', 'GP': 'Guadeloupe', 'RE': 'Reunion', 'YT': 'Mayotte', 'MQ': 'Martinique',
    'GP': 'Guadeloupe', 'GF': 'French Guiana', 'SR': 'Suriname', 'AN': 'Netherlands Antilles',
    'BQ': 'Caribbean Netherlands', 'CW': 'Curacao', 'SX': 'Sint Maarten', 'AW': 'Aruba', 'BB': 'Barbados',
    'BS': 'Bahamas', 'AG': 'Antigua and Barbuda', 'DM': 'Dominica', 'GD': 'Grenada', 'KN': 'Saint Kitts and Nevis',
    'LC': 'Saint Lucia', 'VC': 'Saint Vincent and the Grenadines', 'TT': 'Trinidad and Tobago', 'JM': 'Jamaica',
    'HT': 'Haiti', 'DO': 'Dominican Republic', 'CU': 'Cuba'
}

# explicit function to get
# weather details
def getweather(city):
    result = requests.get(url.format(city, api_key))
    
    if result:
        json = result.json()
        city = json['name']
        country = json['sys']['country']  # Only country code
        temp_kelvin = json['main']['temp']
        temp_celsius = temp_kelvin-273.15
        weather1 = json['weather'][0]['main']
        # New: Add more details
        temp_min = json['main'].get('temp_min', None)
        temp_max = json['main'].get('temp_max', None)
        humidity = json['main'].get('humidity', None)
        wind_speed = json['wind'].get('speed', None)
        feels_like = json['main'].get('feels_like', None)
        description = json['weather'][0].get('description', None)
        icon_code = json['weather'][0].get('icon', None)
        final = [city, country, temp_kelvin, 
                 temp_celsius, weather1, temp_min, temp_max, humidity, wind_speed, feels_like, description, icon_code]
        return final
    else:
        print("NO Content Found")


# explicit function to
# search city
def search():
    city = city_text.get()
    def do_search():
        show_spinner()
        weather = getweather(city)
        hide_spinner()
        if weather:
            result_frame.pack(pady=(10,0), fill=X)
            city_result_lbl['text'] = weather[0]
            # Convert country code to full name
            country_full = COUNTRY_NAMES.get(weather[1], weather[1])
            country_result_lbl['text'] = country_full
            set_weather_icon(weather[11])
            weather_result_lbl['text'] = weather[4]
            desc_result_lbl['text'] = weather[10].capitalize() if weather[10] else ""
            temp_result_lbl['text'] = '{:.2f} °C'.format(weather[3])
            # Fix: Only show min/max if they are different and not None
            if weather[5] is not None and weather[6] is not None and weather[5] != weather[6]:
                minmax_lbl['text'] = f"Min: {weather[5]-273.15:.1f}°C  Max: {weather[6]-273.15:.1f}°C"
            else:
                minmax_lbl['text'] = ""
            humidity_lbl['text'] = f"💧 {weather[7]}%" if weather[7] else ""
            wind_lbl['text'] = f"🌬 {weather[8]} m/s" if weather[8] else ""
            feels_lbl['text'] = f"🤗 {weather[9]-273.15:.1f}°C" if weather[9] else ""
            # Date & Time (local time for city)
            try:
                # Get timezone from OpenWeatherMap API (if available)
                tz_offset = None
                json = requests.get(url.format(city, api_key)).json()
                if 'timezone' in json:
                    tz_offset = json['timezone']
                if tz_offset is not None:
                    utc_now = datetime.utcnow()
                    local_time = utc_now + timedelta(seconds=tz_offset)
                    local_time_lbl['text'] = f"Local Time: {local_time.strftime('%I:%M %p')}"
                else:
                    local_time_lbl['text'] = "Local Time: N/A"
            except:
                local_time_lbl['text'] = "Local Time: N/A"
            now = datetime.now().strftime('%A, %d %B %Y | %I:%M %p')
            date_time_lbl['text'] = f"As of {now}"
            location_lbl.pack_forget()
            temperature_label.pack_forget()
            weather_l.pack_forget()
            fade_in(result_frame)
        else:
            messagebox.showerror('Error', f"Cannot find {city}")
            result_frame.pack_forget()
    threading.Thread(target=do_search, daemon=True).start()


# Driver Code
# create object
app = Tk()
# add title
app.title("Weather App")
# allow resizing and set minimum size
app.minsize(350, 400)
app.geometry("580x580")
app.resizable(True, True)

# Main frame for padding
main_frame = Frame(app, padx=20, pady=20)
main_frame.pack(expand=True, fill=BOTH)

# City input section
city_label = Label(main_frame, text="Enter City:", font=("Arial", 12))
city_label.pack(pady=(0,5))
city_text = StringVar()
city_entry = Entry(main_frame, textvariable=city_text, font=("Arial", 12), width=22)
city_entry.pack(pady=(0,10))

# List of sample city names for autocomplete (can be extended or loaded from a file)
city_list = [
    "London", "New York", "Paris", "Tokyo", "Delhi", "Sydney", "Moscow", "Beijing", "Berlin", "Dubai",
    "Los Angeles", "Chicago", "Toronto", "Mumbai", "Bangkok", "Singapore", "Hong Kong", "Rome", "Madrid", "Istanbul"
]

# Autocomplete Listbox
suggestion_box = Listbox(main_frame, height=5, font=("Arial", 11), bg="white", fg="black")
suggestion_box.pack_forget()

# Function to update suggestions
def update_suggestions(event=None):
    typed = city_text.get()
    suggestion_box.delete(0, END)
    if typed:
        matches = [city for city in city_list if city.lower().startswith(typed.lower())]
        if matches:
            for city in matches:
                suggestion_box.insert(END, city)
            # Place suggestion box below entry, always correct
            x = city_entry.winfo_rootx() - main_frame.winfo_rootx()
            y = city_entry.winfo_y() + city_entry.winfo_height() + 2
            suggestion_box.place(x=x, y=y, width=city_entry.winfo_width())
            suggestion_box.lift()
            suggestion_box.config(relief=SOLID, bd=2, highlightbackground="#4a90e2", highlightcolor="#4a90e2")
        else:
            suggestion_box.place_forget()
    else:
        suggestion_box.place_forget()

# Function to fill entry with selected suggestion
def fill_city_from_suggestion(event):
    if suggestion_box.curselection():
        selected_city = suggestion_box.get(suggestion_box.curselection())
        city_text.set(selected_city)
        suggestion_box.place_forget()
        city_entry.icursor(END)
        city_entry.focus()

# Keyboard navigation for suggestions
def suggestion_key_nav(event):
    if suggestion_box.size() == 0:
        return
    if event.keysym == 'Down':
        if suggestion_box.curselection():
            idx = suggestion_box.curselection()[0]
            if idx < suggestion_box.size() - 1:
                suggestion_box.selection_clear(idx)
                suggestion_box.selection_set(idx+1)
                suggestion_box.activate(idx+1)
        else:
            suggestion_box.selection_set(0)
            suggestion_box.activate(0)
    elif event.keysym == 'Up':
        if suggestion_box.curselection():
            idx = suggestion_box.curselection()[0]
            if idx > 0:
                suggestion_box.selection_clear(idx)
                suggestion_box.selection_set(idx-1)
                suggestion_box.activate(idx-1)
    elif event.keysym == 'Return':
        fill_city_from_suggestion(None)
        city_entry.icursor(END)
        city_entry.focus()

city_entry.bind('<KeyRelease>', update_suggestions)
city_entry.bind('<Down>', suggestion_key_nav)
city_entry.bind('<Up>', suggestion_key_nav)
city_entry.bind('<Return>', suggestion_key_nav)
suggestion_box.bind('<<ListboxSelect>>', fill_city_from_suggestion)

# Button frame
btn_frame = Frame(main_frame)
btn_frame.pack(pady=(0,15))

Search_btn = Button(btn_frame, text="Search Weather", width=15, command=search, bg="#4a90e2", fg="white", font=("Arial", 10, "bold"))
Search_btn.grid(row=0, column=0, padx=5)

def clear():
    city_text.set("")
    # Hide result frame and reset labels
    result_frame.pack_forget()
    city_result_lbl['text'] = ""
    country_result_lbl['text'] = ""
    icon_canvas.delete("all")
    weather_result_lbl['text'] = ""
    temp_result_lbl['text'] = ""
    desc_result_lbl['text'] = ""
    minmax_lbl['text'] = ""
    humidity_lbl['text'] = ""
    wind_lbl['text'] = ""
    feels_lbl['text'] = ""
    date_time_lbl['text'] = ""
    local_time_lbl['text'] = ""
    # Show old labels for empty state
    location_lbl.pack(fill=X)
    temperature_label.pack(pady=(0,5), fill=X)
    weather_l.pack(pady=(0,10), fill=X)

Clear_btn = Button(btn_frame, text="Clear", width=10, command=clear, bg="#e94e77", fg="white", font=("Arial", 10, "bold"))
Clear_btn.grid(row=0, column=1, padx=5)

# Output section
location_lbl = Label(main_frame, text="Location", font=("Arial", 16, "bold"), pady=10, wraplength=350, anchor="center", justify="center")
location_lbl.pack(fill=X)
temperature_label = Label(main_frame, text="", font=("Arial", 14), wraplength=350, anchor="center", justify="center")
temperature_label.pack(pady=(0,5), fill=X)
weather_l = Label(main_frame, text="", font=("Arial", 14), wraplength=350, anchor="center", justify="center")
weather_l.pack(pady=(0,10), fill=X)

# Optionally, add a weather icon placeholder (can be extended to show icons)
icon_lbl = Label(main_frame)
icon_lbl.pack()

# Weather condition to emoji mapping
weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
    "Smoke": "💨",
    "Dust": "🌪️",
    "Sand": "🌪️",
    "Ash": "🌋",
    "Squall": "💨",
    "Tornado": "🌪️"
}

# Result frame (hidden by default)
result_frame = Frame(main_frame, bg="#f5f7fa", bd=2, relief=RIDGE, highlightbackground="#4a90e2", highlightthickness=2)
result_frame.pack(pady=(10,0), fill=X)
result_frame.pack_forget()

city_result_lbl = Label(result_frame, text="", font=("Arial", 26, "bold"), bg="#f5f7fa", fg="#222")
city_result_lbl.pack(pady=(10,0))
country_result_lbl = Label(result_frame, text="", font=("Arial", 14, "bold"), bg="#f5f7fa", fg="#666")
country_result_lbl.pack()

# Weather icon from OpenWeatherMap
icon_canvas = Canvas(result_frame, width=90, height=90, bg="#f5f7fa", highlightthickness=0)
icon_canvas.pack(pady=(0,0))
icon_img = None

def set_weather_icon(icon_code):
    global icon_img
    icon_canvas.delete("all")
    if (icon_code):
        import urllib.request
        from PIL import Image, ImageTk
        url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        try:
            urllib.request.urlretrieve(url, "weather_icon.png")
            img = Image.open("weather_icon.png").resize((80,80))
            icon_img = ImageTk.PhotoImage(img)
            icon_canvas.create_image(45, 45, image=icon_img)
        except:
            icon_canvas.create_text(45, 45, text="❔", font=("Arial", 40))
    else:
        icon_canvas.create_text(45, 45, text="❔", font=("Arial", 40))

weather_result_lbl = Label(result_frame, text="", font=("Arial", 20, "bold"), bg="#f5f7fa", fg="#4a90e2")
weather_result_lbl.pack(pady=(0,2))

desc_result_lbl = Label(result_frame, text="", font=("Arial", 14, "italic"), bg="#f5f7fa", fg="#555")
desc_result_lbl.pack(pady=(0,5))

separator = Frame(result_frame, height=2, bd=1, relief=SUNKEN, bg="#e0e0e0")
separator.pack(fill=X, padx=10, pady=5)

temp_result_lbl = Label(result_frame, text="", font=("Arial", 32, "bold"), bg="#f5f7fa", fg="#e94e77")
temp_result_lbl.pack(pady=(0,5))

# Extra details frame
extra_frame = Frame(result_frame, bg="#f5f7fa")
extra_frame.pack(pady=(0,10))

# Add labels for names above the values, in different colors
humidity_name = Label(extra_frame, text="Humidity", font=("Arial", 10, "bold"), bg="#f5f7fa", fg="#0077b6")
humidity_name.grid(row=0, column=1, padx=10)
wind_name = Label(extra_frame, text="Wind", font=("Arial", 10, "bold"), bg="#f5f7fa", fg="#009688")
wind_name.grid(row=0, column=2, padx=10)
feels_name = Label(extra_frame, text="Feels Like", font=("Arial", 10, "bold"), bg="#f5f7fa", fg="#e67e22")
feels_name.grid(row=0, column=3, padx=10)

minmax_lbl = Label(extra_frame, text="", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#333")
minmax_lbl.grid(row=1, column=0, padx=10)
humidity_lbl = Label(extra_frame, text="", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#0077b6")
humidity_lbl.grid(row=1, column=1, padx=10)
wind_lbl = Label(extra_frame, text="", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#009688")
wind_lbl.grid(row=1, column=2, padx=10)
feels_lbl = Label(extra_frame, text="", font=("Arial", 13, "bold"), bg="#f5f7fa", fg="#e67e22")
feels_lbl.grid(row=1, column=3, padx=10)

# Sunrise/Sunset, Date & Time

# Add a label for local time
local_time_lbl = Label(result_frame, text="", font=("Arial", 12, "bold"), bg="#f5f7fa", fg="#4a90e2")
local_time_lbl.pack(pady=(0,2))

date_time_lbl = Label(result_frame, text="", font=("Arial", 12), bg="#f5f7fa", fg="#888")
date_time_lbl.pack(pady=(0,5))

# Tooltip for Entry
class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind('<Enter>', self.show_tip)
        widget.bind('<Leave>', self.hide_tip)
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("Arial", 10))
        label.pack(ipadx=5, ipady=2)
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

ToolTip(city_entry, "Type a city name. Suggestions will appear below.")

# Spinner for loading
spinner_lbl = Label(main_frame, text="", font=("Arial", 18), fg="#4a90e2", bg=main_frame["bg"])
spinner_running = False

def show_spinner():
    global spinner_running
    spinner_running = True
    spinner_lbl.place(x=city_entry.winfo_x(), y=city_entry.winfo_y()+city_entry.winfo_height()+40)
    spinner_lbl.lift()
    spinner = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    i = 0
    def spin():
        nonlocal i
        while spinner_running:
            spinner_lbl.config(text=spinner[i % len(spinner)])
            i += 1
            time.sleep(0.1)
    threading.Thread(target=spin, daemon=True).start()

def hide_spinner():
    global spinner_running
    spinner_running = False
    spinner_lbl.config(text="")
    spinner_lbl.place_forget()

# Fade-in animation for result frame
def fade_in(widget, steps=10, delay=10):
    for i in range(steps):
        widget.update()
        widget.tk.call(widget, 'config', '-background', f'#f5f7fa')
        widget.after(delay)

app.mainloop()