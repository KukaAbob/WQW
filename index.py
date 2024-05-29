import os
from flask import render_template, Flask
from pymongo import MongoClient
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

app = Flask(__name__)

# Получение переменных окружения
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_cluster = os.getenv("MONGO_CLUSTER")
mongo_dbname = os.getenv("MONGO_DBNAME")

# Проверка значений переменных окружения
print("MONGO_USERNAME:", mongo_username)
print("MONGO_PASSWORD:", mongo_password)
print("MONGO_CLUSTER:", mongo_cluster)
print("MONGO_DBNAME:", mongo_dbname)

# Формирование строки подключения
mongo_uri = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster}/{mongo_dbname}?retryWrites=true&w=majority"

client = MongoClient(mongo_uri)
db = client[mongo_dbname]
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