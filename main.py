import requests
import pandas as pd
import os
from pytz import timezone
import gspread
from gspread_dataframe import set_with_dataframe

def weather_api_call():
    api_key = os.getenv("WEATHER_API_KEY")  # Retrieve API key from environment variables
    if not api_key:
        raise ValueError("API key not found. Make sure WEATHER_API_KEY is set as an environment variable.")
    
    cities = ["bangalore", "mumbai", "hyderabad", "delhi", "gujarat", "mangalore", "assam", "srinagar", "bareilly", "meghalaya"]
    all_data = []  # To store data for all cities

    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url).json()
        if response.get("cod") == 200:  # Ensure the API call was successful
            all_data.append(response)
        else:
            print(f"Error fetching data for {city}: {response.get('message')}")

    return all_data


def flatten_json(json_obj, parent_key='', sep='_'):
    items = []
    for key, value in json_obj.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        elif isinstance(value, list):
            for i, item in enumerate(value):
                items.extend(flatten_json(item, f"{new_key}[{i}]", sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)


def process_weather_data():
    all_responses = weather_api_call()
    flattened_data = [flatten_json(response) for response in all_responses]  # Flatten each city's data
    new_data = pd.DataFrame(flattened_data)  # Convert to DataFrame

    # Convert Unix timestamp columns to IST
    ist_timezone = timezone('Asia/Kolkata')
    for col in ['dt', 'sys_sunrise', 'sys_sunset']:
        if col in new_data.columns:
            new_data[col] = pd.to_datetime(new_data[col], unit='s').dt.tz_localize('UTC').dt.tz_convert(ist_timezone)

    # CSV Operations
    csv_file = "datasets/WeatherData.csv"
    if os.path.exists(csv_file):
        existing_data = pd.read_csv(csv_file)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        combined_data = new_data
    combined_data.to_csv(csv_file, index=False)

    # JSON Operations
    json_file = "datasets/WeatherData.json"
    if os.path.exists(json_file):
        existing_data = pd.read_json(json_file, orient="records")
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        combined_data = new_data
    combined_data.to_json(json_file, orient="records")

    print("Data successfully processed, converted to IST, and saved.")

    # Google Sheets
    GSHEET_NAME = 'Weatherfeeder'
    TAB_NAME = 'Weather'
    credentials_json = os.getenv("GSHEET_CONNECTION")  # Retrieve credentials from environment variables
    if not credentials_json:
        raise ValueError("Google Sheets credentials not found. Make sure GSHEET_CONNECTION is set as an environment variable.")

    gc = gspread.service_account_from_dict(eval(credentials_json))  # Load credentials
    sh = gc.open(GSHEET_NAME)
    worksheet = sh.worksheet(TAB_NAME)

    # Load data into Google Sheets
    df = pd.read_csv(csv_file)
    set_with_dataframe(worksheet, df)
    print("Data loaded successfully to Google Sheets!")


process_weather_data()
