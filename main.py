import requests
import pandas as pd
import os
from pytz import timezone
import gspread
from gspread_dataframe import set_with_dataframe

def weather_api_call():
    api_key = "cbd37b8290bf0a1572748518c7e55e85"
    cities = ["bangalore", "mumbai", "hyderabad", "delhi", "gujarat", "mangalore", "assam","srinagar","bareilly"
              ,"meghalaya"]
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
    credentialsPath = os.path.expanduser("credentials\\diamond-analysis-ac6758ca1ace.json")  # Create your own credentials through Google Sheet API
    df = pd.read_csv("datasets/WeatherData.csv")  # Convert the list to a DataFrame

    if os.path.isfile(credentialsPath):
        # Authenticate and open the Google Sheet
        gc = gspread.service_account(filename=credentialsPath)
        sh = gc.open(GSHEET_NAME)
        worksheet = sh.worksheet(TAB_NAME)

        # Find the last row with data
        last_row = len(worksheet.get_all_values()) + 1

        # Append the new data below the existing data
        set_with_dataframe(worksheet, df, row=last_row, include_index=False, include_column_header=False)
        print("Data loaded successfully!!")
    else:
        print(f"Credentials file not found at {credentialsPath}")		


process_weather_data()
