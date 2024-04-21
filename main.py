import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import random
from datetime import datetime

retrieved_data = []
def generate_data():
    url = ["https://www.msn.com/en-us/weather/forecast/in-Bengaluru-South,Karnataka?loc=eyJsIjoiQmVuZ2FsdXJ1IFNvdXRoIiwiciI6Ikthcm5hdGFrYSIsInIyIjoiQmFuZ2Fsb3JlIFVyYmFuIiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAyLCJnIjoiZW4tdXMiLCJ4IjoiNzcuNTYwOCIsInkiOiIxMi44ODgyIn0%3D&weadegreetype=C",
           "https://www.msn.com/en-us/weather/forecast/in-Mumbai,Maharashtra?loc=eyJsIjoiTXVtYmFpIiwiciI6Ik1haGFyYXNodHJhIiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAyLCJnIjoiZW4tdXMiLCJ4IjoiNzIuODIxMTk3NTA5NzY1NjIiLCJ5IjoiMTguOTY4OTk5ODYyNjcwOSJ9&ocid=ansmsnweather&weadegreetype=C",
           "https://www.msn.com/en-us/weather/forecast/in-Mandya,Karnataka?loc=eyJsIjoiTWFuZHlhIiwiciI6Ikthcm5hdGFrYSIsImMiOiJJbmRpYSIsImkiOiJJTiIsInQiOjEwMiwiZyI6ImVuLXVzIiwieCI6Ijc2Ljg5NDUwMDczMjQyMTg4IiwieSI6IjEyLjUyNzUwMDE1MjU4Nzg5In0%3D&ocid=ansmsnweather&weadegreetype=C",
           "https://www.msn.com/en-us/weather/forecast/in-Thane,Maharashtra?loc=eyJsIjoiVGhhbmUiLCJyIjoiTWFoYXJhc2h0cmEiLCJjIjoiSW5kaWEiLCJpIjoiSU4iLCJ0IjoxMDIsImciOiJlbi11cyIsIngiOiI3Mi45NzgzIiwieSI6IjE5LjIyNjkifQ%3D%3D&ocid=ansmsnweather&weadegreetype=C",
           "https://www.msn.com/en-us/weather/forecast/in-Chennai,Tamil-Nadu?loc=eyJsIjoiQ2hlbm5haSIsInIiOiJUYW1pbCBOYWR1IiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAyLCJnIjoiZW4tdXMiLCJ4IjoiODAuMjAxOSIsInkiOiIxMy4wNzIxIn0%3D&ocid=ansmsnweather&weadegreetype=C",
           "https://www.msn.com/en-in/weather/forecast/in-Delhi,India?loc=eyJsIjoiRGVsaGkiLCJyIjoiRGVsaGkiLCJjIjoiSW5kaWEiLCJpIjoiSU4iLCJ0IjoxMDIsImciOiJlbi1pbiIsIngiOiI3Ny4yMzE1IiwieSI6IjI4LjY1MiJ9&weadegreetype=C&ocid=msedgntp&cvid=41714ddaec4d4b119f05991828b07e1c",
           "https://www.msn.com/en-in/weather/forecast/in-Shillong,Meghalaya?loc=eyJhIjoiTWVnaGFsYXlhIFRvdXJpc20gRGV2ZWxvcG1lbnQgQ29ycG9yYXRpb24iLCJsIjoiU2hpbGxvbmciLCJyIjoiTWVnaGFsYXlhIiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAxLCJnIjoiZW4taW4iLCJ4IjoiOTEuODgyNSIsInkiOiIyNS41Nzc3In0%3D&weadegreetype=C&ocid=msedgntp&cvid=41714ddaec4d4b119f05991828b07e1c",
           "https://www.msn.com/en-us/weather/forecast/in-Srinagar,Jammu-%26-Kashmir?loc=eyJsIjoiU3JpbmFnYXIiLCJyIjoiSmFtbXUgJiBLYXNobWlyIiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAyLCJnIjoiZW4taW4iLCJ4IjoiNzQuODA0Mjk4NDAwODc4OSIsInkiOiIzNC4wNzE3MDEwNDk4MDQ2OSJ9&weadegreetype=C",
           "https://www.msn.com/en-in/weather/forecast/in-Bareilly,Uttar-Pradesh?loc=eyJsIjoiQmFyZWlsbHkiLCJyIjoiVXR0YXIgUHJhZGVzaCIsImMiOiJJbmRpYSIsImkiOiJJTiIsInQiOjEwMiwiZyI6ImVuLWluIiwieCI6Ijc5LjQwOTYiLCJ5IjoiMjguMzUxOCJ9&weadegreetype=C&ocid=msedgntp&cvid=d7cd4ad070ca4da2a787c2634cdb2fc4",
           "https://www.msn.com/en-in/weather/forecast/in-Manali,Himachal-Pradesh?loc=eyJsIjoiTWFuYWxpIiwiciI6IkhpbWFjaGFsIFByYWRlc2giLCJyMiI6Ikt1bGx1IiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAyLCJnIjoiZW4taW4iLCJ4IjoiNzcuMTkyNSIsInkiOiIzMi4yOTMyIn0%3D&weadegreetype=C&ocid=msedgntp&cvid=d7cd4ad070ca4da2a787c2634cdb2fc4"

         ]
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service = Service(executable_path="C:\\Program Files (x86)\\chromedriver-win64\\chromedriver.exe",options = options)
    driver = webdriver.Chrome(service=service)
    driver2 = webdriver.Chrome(service=service)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    scrapped_data = []
    extracted_data = {}
    for link in url:
        driver.get(link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sectionContainer-DS-EntryPoint1-1'))
        )
        pagesource = driver.page_source
        soup = BeautifulSoup(pagesource, 'lxml')
        times = soup.find('div',attrs={"class":"labelUpdatetime-DS-EntryPoint1-1"}).text.strip()
        place = soup.find('a',attrs={"class":"location_name_label-DS-EntryPoint1-1 location_name_link-DS-EntryPoint1-1"}).text.strip().split(',')[0]
        state = soup.find('a', attrs={"class": "location_name_label-DS-EntryPoint1-1 location_name_link-DS-EntryPoint1-1"}).text.strip().split(',')[1]
        current_temper = soup.find('div',attrs={"class":"overallContainer-DS-EntryPoint1-1"}).text.split()[3].replace('weather','')
        current_temp = re.match(r'(\d+)°', current_temper).group(1)
        day_date = driver.find_element(By.XPATH,'//*[@id="ForecastDays"]/div/ul/li[2]/button/span/div/p').text
        max_temp = float(soup.find('div',attrs={'class':'topTemp-DS-EntryPoint1-1 temp-DS-EntryPoint1-1'}).text.replace('°','').strip())
        min_temp = float(driver.find_element(By.XPATH,'//*[@id="ForecastDays"]/div/ul/li[2]/button/span/div/div/div[2]/div[2]/div').text.replace('°','').strip())
        air_quality = driver.find_element(By.XPATH,'//*[@id="WeatherOverviewCurrentSection"]/div[2]/div/div[3]/div/div[1]/a/div[2]').text
        wind = float(soup.find('div',attrs={'id':'CurrentDetailLineWindValue'}).text.replace(' km/h','').strip())
        humidity = float(soup.find('div',attrs={'id':'CurrentDetailLineHumidityValue'}).text.replace('%','').strip())/100
        visibility = float(soup.find('div',attrs={'id':'CurrentDetailLineVisibilityValue'}).text.replace(' km','').strip())
        pressure = float(soup.find('div',attrs={'id':'CurrentDetailLinePressureValue'}).text.replace(' mb','').strip())
        dew_point = float(soup.find('div',attrs={'id':'CurrentDetailLineDewPointValue'}).text.replace('°','').strip())
        button = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.ID, 'DetailToggle'))
        )
        button.click()
        time.sleep(20)
        # Find the UV index element
        uv_index = driver.find_element(By.CLASS_NAME, 'valueFont-DS-EntryPoint1-1').text.split('·')[0]
        status = driver.find_element(By.CLASS_NAME, 'valueFont-DS-EntryPoint1-1').text.split('·')[1]
        moon_phase_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'valueFont-DS-EntryPoint1-1.labelWidth92-DS-EntryPoint1-1'))
        )
        moon_phase = moon_phase_element.text
        phases = driver.find_elements(By.CLASS_NAME,'newSunGridCellDaylight-DS-EntryPoint1-1')
        li = []
        for phase in phases:
            phaser = phase.find_element(By.CLASS_NAME,'valueFont-DS-EntryPoint1-1').text
            li.append(phaser)
        sunrise = li[2]
        sunset = li[3]
        moonrise = li[1]
        moonset = li[0]

        sunnydays = driver.find_element(By.CLASS_NAME,'wisCarouselCardsItem-DS-EntryPoint1-1').text.replace('\n','').replace('Weather forecastDay','').replace('Night','').split('°.')
        daydata = sunnydays[0]
        nightdata = sunnydays[1]
        monthly = driver.find_element(By.CLASS_NAME,'wisContainer-DS-EntryPoint1-1').text.split('\n')
        sunny = float(monthly[21])
        rainsnow = float(monthly[25].replace("°",""))
        rainday = float(monthly[41].replace("°",""))
        try:
            avgrainday = float(monthly[43].replace(' cm', ''))
        except ValueError:
            avgrainday = 0.25

        try:
            snow = float(monthly[47])
        except ValueError:
            snow = 0
        try:
            avgsnowday = float(monthly[49].replace(' cm',''))
        except ValueError:
            avgsnowday = 0.22
        seemore = driver.find_element(By.CLASS_NAME, "lifeIndexLinkButton-DS-EntryPoint1-1")
        href_value = seemore.get_attribute("href")
        driver2.get(href_value)
        WebDriverWait(driver2, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'lifeBarCoverdLink-DS-EntryPoint1-1'))
        )
        pagesource2 = driver2.page_source
        soup2 = BeautifulSoup(pagesource2, 'lxml')
        but = driver2.find_elements(By.CLASS_NAME,"lifeIndexBarWrapper-DS-EntryPoint1-1")
        but_list = []
        for but_item in but:
            but_value = but_item.get_attribute("aria-label")
            but_list.append(but_value)
        umbrella = but_list[0]
        outdoors = but_list[1]
        driving = but_list[3]
        clothing = but_list[4]
        heat_stroke = but_list[5]
        wind_chill = but_list[6]

        extracted_data = {
            "Time":times,
            "City":place,
            "State":state,
            "TemperatureC":float(current_temp),
            "TemperatureF":(1.8*float(current_temp))+32,
            "TemperatureK":float(current_temp)+273,
            "Day_Date":day_date,
            "Max_Temp":max_temp,
            "Min_Temp":min_temp,
            "Air_Quality":air_quality,
            "Wind":wind,
            "Humidity":humidity,
            "Visibility":visibility,
            "Pressure":pressure,
            "Dew_point":dew_point,
            "UV_index":uv_index,
            "Status":status,
            "Moon_Phase":moon_phase,
            "Sunrise":sunrise,
            "Sunset":sunset,
            "Moonrise":moonrise,
            "Moonset":moonset,
            "Sunny":sunny,
            "Rainsnow":rainsnow,
            "Rainday":rainday,
            "AvgRainDay":avgrainday,
            "AvgSnowDay":avgsnowday,
            "Umbrella":umbrella,
            "Outdoors":outdoors,
            "Driving":driving,
            "Clothing":clothing,
            "Heat_Stroke":heat_stroke,
            "Wind_Chill":wind_chill,
            "Date_Taken": datetime.now()
        }
        scrapped_data.append(extracted_data)
    dataset = pd.DataFrame(scrapped_data)
    file_exists = os.path.isfile("Weather_Data.csv")
    # Set header argument based on whether the file exists or not
    header = not file_exists
    # Append data to CSV
    dataset.to_csv("Weather_Data.csv", index=False, mode='a', header=header)
    retrieved_data = scrapped_data
    return retrieved_data

