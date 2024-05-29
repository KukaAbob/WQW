import os
from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

app = Flask(__name__)

# Получение строки подключения из переменной окружения
MONGO_CONNECT_URL = os.getenv("MONGO_CONNECT_URL")

# Подключение к MongoDB
client = MongoClient(MONGO_CONNECT_URL)
db = client["weatherDB"]
collection = db["forecasts"]
@app.route('/')
def index():
    return render_template("mainpage.html")

@app.route('/secur')
def IoT_secur():
    return render_template("IoT_Secur.html")

@app.route('/smart_home')
def Smart():
    return render_template("Smart_Home.html")

@app.route('/monitoring')
def monitoring():
    # Получаем все прогнозы из базы данных
    all_forecasts = list(collection.find())
    
    # Получаем сегодняшнюю дату
    today = datetime.now().date()

    # Фильтруем прогнозы, оставляя только сегодняшние
    today_forecasts = []
    for forecast in all_forecasts:
        forecast_date = datetime.strptime(forecast["DateTime"], "%Y-%m-%d").date()
        if forecast_date == today:
            existing_forecast = collection.find_one({"DateTime": forecast["DateTime"]})
            if existing_forecast:
                # Обновляем существующий прогноз
                collection.update_one({"_id": existing_forecast["_id"]}, {"$set": forecast})
            else:
                # Добавляем новый прогноз
                collection.insert_one(forecast)
            today_forecasts.append(forecast)

    # Передаем данные в шаблон и рендерим страницу
    return render_template("IoT_Monitoring.html", today_forecasts=today_forecasts, all_forecasts=all_forecasts)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Используем переменную окружения PORT или порт по умолчанию 5000
    app.run(debug=True, host='0.0.0.0', port=port)