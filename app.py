from flask import Flask, request, render_template
import re
import os

app = Flask(__name__)

def find_ean_and_quantity(text):
    # Шаблон для поиска EAN (13-значный штрих-код)
    ean_pattern = r'\b\d{13}\b'
    # Шаблон для поиска целого количества (исключаем числа с точкой)
    quantity_pattern = r'(?<![\d.])\b\d{1,2}\b(?![\d.])'

    # Поиск всех EAN кодов и количеств
    ean_codes = re.findall(ean_pattern, text)
    quantities = re.findall(quantity_pattern, text)

    # Проверяем, что количество найденных элементов совпадает
    if len(ean_codes) != len(quantities):
        return None

    return list(zip(ean_codes, quantities))

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        text = request.form['text']
        results = find_ean_and_quantity(text)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
