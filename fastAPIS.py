from fastapi import FastAPI,Path
import json
app = FastAPI()

@app.get("/get")
def home():
    with open('LiveWeatherData.json', 'r') as file:
        jsoneddata = json.load(file)
        return jsoneddata