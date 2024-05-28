USE WeatherDB;
CREATE TABLE weather (
        [Time] NVARCHAR(50),
        City NVARCHAR(50),
        State NVARCHAR(50),
        TemperatureC FLOAT,
        TemperatureF FLOAT,
        TemperatureK FLOAT,
        Day_Date NVARCHAR(50),
        Max_Temp FLOAT,
        Min_Temp FLOAT,
        Air_Quality FLOAT,
        Wind FLOAT,
        Humidity FLOAT,
        Visibility FLOAT,
        Pressure FLOAT,
        Dew_point FLOAT,
        UV_index FLOAT,
        Status NVARCHAR(50),
        Moon_Phase NVARCHAR(50),
        Sunrise NVARCHAR(20),
        Sunset NVARCHAR(20),
        Moonrise NVARCHAR(20),
        Moonset NVARCHAR(20),
        Sunny FLOAT,
        Rainsnow FLOAT,
        Rainday FLOAT,
        AvgRainDay FLOAT,
        AvgSnowDay FLOAT,
        Umbrella NVARCHAR(50),
        Outdoors NVARCHAR(50),
        Driving NVARCHAR(50),
        Clothing NVARCHAR(50),
        Heat_Stroke NVARCHAR(50),
        Wind_Chill NVARCHAR(50),
        Date_Taken DATETIME
    );

SELECT * FROM weather;
DROP TABLE weather;