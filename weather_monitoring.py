import requests
import json
import time
import pandas as pd
from openpyxl.styles import Font

# OpenWeatherMap API key
api_key = '30d4741c779ba94c470ca1f63045390a'

# List of cities in Pakistan (includes major cities and districts from each province)
cities = [
    'Islamabad', 'Karachi', 'Lahore', 'Rawalpindi', 'Faisalabad', 'Khanewal','Multan',
    'Peshawar', 'Quetta', 'Gujranwala', 'Sialkot', 'Hyderabad', 'Sukkur',
    'Larkana', 'Nawabshah', 'Mirpur Khas', 'Khairpur', 'Jacobabad', 'Shikarpur',
    'Dadu', 'Bahawalpur', 'Sargodha', 'Sheikhupura', 'Jhang', 'Kasur', 'Gujrat',
    'Mardan', 'Kohat', 'Abbottabad', 'Dera Ismail Khan', 'Swabi',
    'Nowshera', 'Charsadda', 'Mansehra', 'Khuzdar', 'Turbat', 'Gwadar', 'Sibi',
    'Zhob', 'Chaman', 'Panjgur', 'Loralai', 'Muzaffarabad',
    'Mirpur', 'Kotli', 'Gilgit', 'Skardu', 'Chilas'
]

# Function to fetch weather data for a city with retries
def get_weather_data(city, retries=3, delay=5):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={api_key}"
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching data for {city}: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Failed to fetch data for {city} after {retries} attempts")
                return None

# Function to predict rain probability
def predict_rain_probability(humidity, pressure):
    if humidity > 80 and pressure < 1000:
        return "High"
    elif 60 < humidity <= 80 and pressure < 1010:
        return "Moderate"
    else:
        return "Low"

# Function to convert JSON data to an Excel file
def json_to_excel(json_data, excel_filename='weather_data.xlsx'):
    # Create a DataFrame from the JSON data
    data = []
    for city, details in json_data.items():
        row = {
            'City': city,
            'Weather': details['weather'][0]['main'],
            'Description': details['weather'][0]['description'],
            'Temperature (C)': details['main']['temp'],
            'Humidity (%)': details['main']['humidity'],
            'Pressure (hPa)': details['main']['pressure'],
            'Wind Speed (km/h)': details['wind']['speed'] * 3.6,  # Convert from m/s to km/h
            'Rain Probability': predict_rain_probability(details['main']['humidity'], details['main']['pressure'])
        }
        data.append(row)

    df = pd.DataFrame(data)

    # Create an Excel writer object and write the DataFrame to Excel
    writer = pd.ExcelWriter(excel_filename, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Weather Data')

    # Access the workbook and the worksheet
    workbook = writer.book
    worksheet = writer.sheets['Weather Data']

    # Define a bold font
    bold_font = Font(bold=True)

    # Apply the bold font to the header cells
    for cell in worksheet["1:1"]:
        cell.font = bold_font

    # Save and close the Excel file
    writer.close()

# Function to get weather data for a single city and print it
def get_and_print_city_weather(city):
    weather_data = get_weather_data(city)

    if weather_data:
        try:
            weather = weather_data['weather'][0]['main']
            temp_celsius = round(weather_data['main']['temp'], 2)
            humidity = weather_data['main']['humidity']
            pressure = weather_data['main']['pressure']
            wind_speed_m_s = weather_data['wind']['speed']
            wind_speed_kmh = round(wind_speed_m_s * 3.6, 2)

            rain_probability = predict_rain_probability(humidity, pressure)

            print(f"The weather in {city} is: {weather}")
            print(f"The temperature in {city} is: {temp_celsius}ºC")
            print(f"Humidity: {humidity}%")
            print(f"Pressure: {pressure} hPa")
            print(f"Wind Speed: {wind_speed_kmh} km/h")
            print(f"Rain Probability: {rain_probability}")
        except KeyError:
            print("Error retrieving weather information. Please try again.")
    else:
        print("No City Found or failed to fetch data after retries.")

# Main function
def main():
    user_input = input("Enter city: ")
    get_and_print_city_weather(user_input)

    user_choice = input("Do you want the list of weather for other cities? (yes/no): ").strip().lower()
    
    if user_choice == 'yes':
        weather_data = {}
        for city in cities:
            print(f"Fetching weather data for {city}...")
            data = get_weather_data(city)
            if data:
                weather_data[city] = data
                time.sleep(1)  # Add a delay to avoid hitting API rate limits
        
        if weather_data:
            with open('weather_data.json', 'w') as file:
                json.dump(weather_data, file, indent=4)
            print("Weather data collected and saved to weather_data.json")
            
            # Convert JSON data to Excel
            json_to_excel(weather_data)
            print("Weather data converted and saved to weather_data.xlsx")
            
            # Find and print the city with the maximum and minimum temperatures
            max_temp = -float('inf')
            min_temp = float('inf')
            max_temp_city = ""
            min_temp_city = ""
            max_rain_prob = ""
            highest_rain_prob = "Low"

            for city, details in weather_data.items():
                temp = details['main']['temp']
                rain_prob = predict_rain_probability(details['main']['humidity'], details['main']['pressure'])

                if temp > max_temp:
                    max_temp = temp
                    max_temp_city = city
                if temp < min_temp:
                    min_temp = temp
                    min_temp_city = city
                if rain_prob == "High" and highest_rain_prob != "High":
                    highest_rain_prob = "High"
                    max_rain_prob = city
                elif rain_prob == "Moderate" and highest_rain_prob == "Low":
                    highest_rain_prob = "Moderate"
                    max_rain_prob = city

            print(f"The city with the maximum temperature is {max_temp_city} with {max_temp}°C.")
            print(f"The city with the minimum temperature is {min_temp_city} with {min_temp}°C.")
            print(f"The city with the highest rain probability is {max_rain_prob} with a {highest_rain_prob} probability.")
        else:
            print("No weather data collected.")
    else:
        print("Thanks for choosing us!")

if __name__ == "__main__":
    main()
