from fastapi import FastAPI,Path
import json
app = FastAPI()

@app.get("/")
def home():
    with open('datasets/WeatherData.json', 'r') as file:
        jsoneddata = json.load(file)
        return jsoneddata
