from flask import Flask, render_template
import requests, datetime

def get_weather():
    api_key = "fd4012c776e80f46bb89271e22a17fe1"
    city = "London"
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid={api_key}"
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    current_weather_data = requests.get(current_url).json()
    future_weather_data = requests.get(forecast_url).json()
    temp = current_weather_data["main"]["temp"]
    precip = current_weather_data["weather"][0]["description"]
    weather_info = f"Current Temperature: {temp}°C<br>Predicted Precipitation: {precip}"

    forecast_html = "<h3>Weather Forecast for the Day:</h3><ul>"
    for forecast in future_weather_data["list"][:5]:
        time = datetime.datetime.fromtimestamp(forecast["dt"]).time().isoformat()
        temp = forecast["main"]["temp"]
        desc = forecast["weather"][0]["description"]
        forecast_html += f"<li>{time}: {temp}°C, {desc}</li>"
    forecast_html += "</ul>"

    return weather_info, forecast_html

def create_app():
    app = Flask(__name__)

    @app.route('/weatherly')
    def hello():
        now, future = get_weather()
        return render_template("index.html", info=now, forecast=future)
    return app

