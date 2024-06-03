# Weather Checker

Weather Checker is a simple Python application that retrieves and displays weather information for a specified city using the OpenWeatherMap API.

## Features

- Fetches and displays the current weather condition.
- Shows the temperature in Celsius.
- Provides humidity and atmospheric pressure readings.
- Converts and displays wind speed from meters per second to kilometers per hour.
- Predicts the probability of rain based on humidity and pressure values.
- Retrieves and saves weather data for major cities across Pakistan.
- Converts collected weather data into a well-structured Excel file with pandas and openpyxl.
- Identifies and displays the cities with the highest and lowest temperatures, as well as the city with the highest probability of rain.
  

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/weather-checker.git
    cd weather-checker
    ```

2. **Install required packages:**
    Make sure you have `requests` library installed. If not, install it using pip:
    ```bash
    pip install requests
    ```

## Usage

1. **Set your OpenWeatherMap API key:**
    Replace the `api_key` variable in the code with your OpenWeatherMap API key:
    ```python
    api_key = '30d4741c779ba94c470ca1f63045390a'
    ```

2. **Run the script:**
    ```bash
    python weatherdata.py
    ```

3. **Enter a city:**
    When prompted, enter the name of the city you want to check the weather for.

## Example Output

```
Enter city: Islamabad
The weather in Islamabad is: Clear
The temperature in Islamabad is: 34.91ºC
Humidity: 27%
Pressure: 1003 hPa
Wind Speed: 5.4 km/h
Rain Probability: Low
```

## Rain Prediction Logic

The rain probability is determined based on the following conditions:

- **High:** Humidity > 80% and Pressure < 1000 hPa
- **Moderate:** Humidity between 60% and 80% and Pressure < 1010 hPa
- **Low:** Otherwise

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or features you'd like to see.

## Contact

For any questions or feedback, please contact [sohalfaisal9151@gmail.com].

---

Replace `yourusername` and `your-email@example.com` with your actual GitHub username and email address before using it.
