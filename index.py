from flask import render_template, Flask
from pymongo import MongoClient
from datetime import datetime, timedelta

app = Flask(__name__)
client = MongoClient("mongodb+srv://kukakarakuzov:Kuanis2006@cluster0.wjekppx.mongodb.net/?retryWrites=true&w=majority")
db = client["weatherDB"]
collection = db["forecasts"]

@app.route('/')
def index():
    return render_template("mainpage.html")

@app.route('/monitoring')
def monitoring():
    # Получаем все прогнозы из базы данных
    all_forecasts = list(collection.find())

    # Получаем сегодняшнюю дату
    today = datetime.now().date()

    # Фильтруем прогнозы, оставляя только сегодняшние
    today_forecasts = [forecast for forecast in all_forecasts if datetime.strptime(forecast["DateTime"], "%Y-%m-%d %H:%M:%S").date() == today]

    # Передаем данные в шаблон и рендерим страницу
    return render_template("IoT_Monitoring.html", today_forecasts=today_forecasts, all_forecasts=all_forecasts)

if __name__ == '__main__':
    app.run(debug=True)