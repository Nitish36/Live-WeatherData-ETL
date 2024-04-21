from flask import Flask, jsonify
import pandas as pd
app = Flask(__name__)


@app.route("/get")
def getData():
    weather_data = pd.read_csv("Weather_Data.csv", index_col=False)
    weather_data.reset_index(inplace=True)
    data_dict = weather_data.to_dict(orient='index')
    return jsonify(data_dict), 200


if __name__ == "__main__":
    app.run(debug=True)