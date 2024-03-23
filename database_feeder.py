from main import generate_data
import mysql.connector
import numpy as np
import gspread
from gspread_dataframe import set_with_dataframe
import os
import pandas as pd

def feed_database():
    GSHEET_NAME = 'WeatherDataFeeder'
    TAB_NAME = 'Weather'
    credentialsPath = os.path.expanduser(
        "credentials\\diamond-analysis-ac6758ca1ace.json")  # Create your own credentials through Google Sheet API
    data = generate_data()
    df = pd.DataFrame(data)  # Convert the list to a DataFrame

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

    print(data)
    item_data_tuples = [tuple(row) for row in np.array(data)]
    print(item_data_tuples)
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="$Freeman_007$",
            auth_plugin = 'mysql_native_password'
        )
    mycursor = mydb.cursor(buffered = True)
    mycursor.execute("CREATE DATABASE IF NOT EXISTS weatherdata")
    mycursor.execute("SHOW DATABASES")
    mycursor.execute("USE weatherdata")
    mycursor.execute("""CREATE TABLE IF NOT EXISTS weather (
            Time VARCHAR(50),
            City VARCHAR(50),
            State VARCHAR(50),
            TemperatureC DOUBLE,
            TemperatureF DOUBLE,
            TemperatureK DOUBLE,
            Day_Date VARCHAR(50),
            Max_Temp DOUBLE,
            Min_Temp DOUBLE,
            Air_Quality DOUBLE,
            Wind DOUBLE,
            Humidity DOUBLE,
            Visibility DOUBLE,
            Pressure DOUBLE,
            Dew_point DOUBLE,
            UV_index DOUBLE,
            Status varchar(50),
            Moon_Phase VARCHAR(50),
            Sunrise VARCHAR(20),
            Sunset VARCHAR(20),
            Moonrise VARCHAR(20),
            Moonset VARCHAR(20),
            Sunny DOUBLE,
            Rainsnow DOUBLE,
            Rainday DOUBLE,
            AvgRainDay DOUBLE,
            AvgSnowDay DOUBLE,
            Umbrella VARCHAR(50),
            Outdoors VARCHAR(50),
            Driving VARCHAR(50),
            Clothing VARCHAR(50),
            Heat_Stroke VARCHAR(50),
            Wind_Chill VARCHAR(50),
            Date_Taken DATETIME
                );
            """
        )
    mycursor.execute("SHOW TABLES")
    table_name = "weather"
    column_names = ', '.join(data[0].keys())

    # Define the placeholders for the values
    placeholders = ', '.join(['%s'] * len(data[0].keys()))

    # Define the INSERT query
    insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

    # Prepare data for insertion
    data_values = [tuple(row.values()) for row in data]

    # Execute the query to insert data
    mycursor.executemany(insert_query, data_values)

    # Commit changes and close the connection
    mydb.commit()
    '''
    ins = """
        INSERT INTO weather (
            Time, City, State, TemperatureC, TemperatureF, TemperatureK,
            Day_Date, Max_Temp, Min_Temp, Air_Quality, Wind, Humidity,
            Visibility, Pressure, Dew_point, UV_index, Status, Moon_Phase,
            Sunrise, Sunset, Moonrise, Moonset, Sunny, Rainsnow, Rainday,
            AvgRainDay, AvgSnowDay, Umbrella, Outdoors, Driving, Clothing,
            Heat_Stroke, Wind_Chill, Date_Taken
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
    """

    # Execute the INSERT statement for each item in item_list
    mycursor.executemany(ins, item_data_tuples)
    mydb.commit()
    '''
    mycursor.execute("SELECT * FROM weather")
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    print("\n")

