# Импорт необходимых библиотек
import requests  # Для выполнения HTTP-запросов к API ЦБ РФ
import pandas as pd  # Для работы с данными в табличном формате
import matplotlib.pyplot as plt  # Для построения графиков
from datetime import datetime, timedelta  # Для работы с датами
import xml.etree.ElementTree as ET  # Для парсинга XML-данных

# Список валют, которые мы будем анализировать (обновлен по заданию)
currencies = ['DKK', 'CAD', 'NZD', 'PLN']  # Датская крона, Канадский доллар, Новозеландский доллар, Злотый

# Создаем словарь для хранения данных по валютам
currency_data = {currency: [] for currency in currencies}

# Устанавливаем диапазон дат: последние 30 дней от текущей даты
end_date = datetime.now()  # Текущая дата
start_date = end_date - timedelta(days=30)  # Дата 30 дней назад
current_date = start_date  # Начинаем с начальной даты

# Цикл по всем дням в диапазоне
while current_date <= end_date:
    # Форматируем дату в формат, который понимает API ЦБ (дд/мм/гггг)
    formatted_date = current_date.strftime('%d/%m/%Y')
    
    # Формируем URL для запроса курсов валют на конкретную дату
    url = f"https://www.cbr.ru/scripts/XML_daily.asp?date_req={formatted_date}"
    
    # Отправляем GET-запрос к API ЦБ
    response = requests.get(url)
    response.encoding = 'windows-1251'  # Указываем кодировку ответа
    
    # Проверяем, что запрос успешен (код 200)
    if response.status_code == 200:
        # Парсим XML-ответ
        root = ET.fromstring(response.content)
        
        # Получаем дату из атрибутов XML-документа
        date_record = root.attrib.get('Date')
        
        # Ищем все элементы 'Valute' в XML
        for valute in root.findall('Valute'):
            # Получаем буквенный код валюты
            char_code = valute.find('CharCode').text
            
            # Проверяем, есть ли эта валюта в нашем списке
            if char_code in currencies:
                # Получаем значение курса и номинал
                value = float(valute.find('Value').text.replace(',', '.'))  # Заменяем запятую на точку для float
                nominal = int(valute.find('Nominal').text)  # Номинал (например, 1, 10, 100 и т.д.)
                
                # Нормализуем курс (приводим к стоимости за 1 единицу валюты)
                normalized_value = value / nominal
                
                # Добавляем данные в словарь
                currency_data[char_code].append({
                    'date': date_record,  # Дата записи
                    'value': normalized_value  # Нормализованное значение курса
                })
    
    # Переходим к следующему дню
    current_date += timedelta(days=1)

# Сохраняем данные в Excel-файл
with pd.ExcelWriter('currency_rates.xlsx') as writer:  # Создаем Excel-файл
    for currency in currencies:
        # Создаем DataFrame из собранных данных
        df = pd.DataFrame(currency_data[currency])
        
        if not df.empty:  # Проверяем, что данные есть
            # Преобразуем дату в формат datetime и сортируем по дате
            df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
            df.sort_values('date', inplace=True)
            
            # Сохраняем в отдельный лист Excel с именем валюты
            df.to_excel(writer, sheet_name=currency, index=False)

# Строим графики для каждой валюты
for currency in currencies:
    # Создаем DataFrame из собранных данных
    df = pd.DataFrame(currency_data[currency])
    
    # Проверяем, есть ли данные
    if df.empty:
        print(f"Нет данных для {currency}.")
        continue
    
    # Преобразуем и сортируем даты
    df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y')
    df.sort_values('date', inplace=True)
    
    # Создаем график
    plt.figure(figsize=(12, 6))  # Устанавливаем размер графика
    
    # Рисуем линию с точками
    plt.plot(df['date'], df['value'], 
            marker='o',  # Маркеры в виде кружков
            linestyle='-',  # Сплошная линия
            linewidth=2,  # Толщина линии
            markersize=6,  # Размер маркеров
            color='#2c5aa0')  # Синий цвет
    
    # Заголовок графика
    plt.title(f'Динамика курса {currency} к рублю\n({start_date.strftime("%d.%m.%Y")} - {end_date.strftime("%d.%m.%Y")})', 
             fontsize=14,  # Размер шрифта
             pad=20)  # Отступ
    
    # Подписи осей
    plt.xlabel('Дата', fontsize=12)
    plt.ylabel('Курс, руб', fontsize=12)
    
    # Настройка осей
    plt.xticks(rotation=45, fontsize=10)  # Поворот подписей дат
    plt.yticks(fontsize=10)  # Размер шрифта по оси Y
    plt.grid(True, alpha=0.3)  # Включаем сетку с прозрачностью
    
    # Форматируем отображение дат на оси X
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d.%m'))
    
    # Оптимизируем расположение элементов
    plt.tight_layout()
    
    # Сохраняем график в файл PNG
    plt.savefig(f'{currency}_trend.png', dpi=150)
    
    # Показываем график
    plt.show()

# Выводим сообщение о завершении
print("Обработка завершена. Проверьте файлы:")
print("- currency_rates.xlsx")  # Файл с курсами валют
print("- Графики в формате PNG")  # Сохраненные графики

def calc(a, b, op):
    r = 0
    if op == '+':
        r = a + b
    elif op == '-':
        r = a - b
    elif op == '*':
        r = a * b
    elif op == '/':
        if b != 0:
            r = a / b
        else:
            r = None
    else:
        r = None
    return r

def find_max(arr):
    m = arr[0]
    for x in arr:
        if x > m:
            m = x
    return m
