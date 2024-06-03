import requests

api_key = '30d4741c779ba94c470ca1f63045390a'

user_input = input("Enter city: ")

weather_data = requests.get(
    f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={api_key}")

if weather_data.status_code == 404:
    print("No City Found")
else:
    try:
        data = weather_data.json()
        weather = data['weather'][0]['main']
        temp_celsius = round(data['main']['temp'], 2)
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed_m_s = data['wind']['speed']
        wind_speed_kmh = round(wind_speed_m_s * 3.6, 2)
        
        # Function to predict rain probability
        def predict_rain_probability(humidity, pressure):
            if humidity > 80 and pressure < 1000:
                return "High"
            elif 60 < humidity <= 80 and pressure < 1010:
                return "Moderate"
            else:
                return "Low"

        rain_probability = predict_rain_probability(humidity, pressure)

        print(f"The weather in {user_input} is: {weather}")
        print(f"The temperature in {user_input} is: {temp_celsius}ºC")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
        print(f"Wind Speed: {wind_speed_kmh} km/h")
        print(f"Rain Probability: {rain_probability}")
    except KeyError:
        print("Error retrieving weather information. Please try again.")
