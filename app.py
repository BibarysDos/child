# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["*"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        response = jsonify({})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "Content-Type,Authorization")
        response.headers.add('Access-Control-Allow-Methods', "GET,POST,OPTIONS")
        return response

# Фиксированные данные для ИИН "971202300696"
FIXED_CHILDREN = [
    {
        "child_iin": "170218500993",
        "child_surname": "ШАРИФУЛЛА",
        "child_name": "АЛДИЯР",
        "child_patronymic": "ДАСТАНҰЛЫ",
        "child_birth_date": "2017-02-18T01:00:00",
        "act_date": "2017-02-21T01:00:00",
        "act_number": "10-558-17-0000565",
        "zags_name_kz": "Алматы қ. Наурызбай ауданы әкім аппараты Азаматтық хал актілерін тіркеу бөлімі",
        "zags_name_ru": "Аппарат акима Наурызбайского района г. Алматы  отдел регистрации актов гражданского состояния"
    },
    {
        "child_iin": "191006602454",
        "child_surname": "ШАРИФУЛЛА",
        "child_name": "ДАРИЯ",
        "child_patronymic": "ДАСТАНҚЫЗЫ",
        "child_birth_date": "2019-10-06T01:00:00",
        "act_date": "2019-10-10T01:00:00",
        "act_number": "10-559-19-0003773",
        "zags_name_kz": "Алматы қ. Медеу ауданы әкім аппараты Азаматтық хал актілерін тіркеу бөлімі",
        "zags_name_ru": "Аппарат акима Медеуского района г. Алматы  отдел регистрации актов гражданского состояния"
    }
]

def generate_simple_children():
    """Генерирует простых случайных детей (минимум 1)"""
    # От 1 до 3 детей
    num_children = random.randint(1, 3)
    children = []
    
    names_male = ["АЛДИЯР", "АРМАН", "ДАНИЯР"]
    names_female = ["ДАРИЯ", "АЙГУЛЬ", "БАЛЖАН"]
    surnames = ["ИВАНОВ", "КАСЫМОВ", "АБДУЛЛАЕВ"]
    
    for i in range(num_children):
        is_male = random.choice([True, False])
        birth_year = random.randint(2010, 2020)
        
        child = {
            "child_iin": f"{birth_year-2000:02d}0{random.randint(1,9):01d}{random.randint(10,28):02d}{random.randint(100000,999999)}",
            "child_surname": random.choice(surnames),
            "child_name": random.choice(names_male if is_male else names_female),
            "child_patronymic": "ДАСТАНҰЛЫ" if is_male else "ДАСТАНҚЫЗЫ",
            "child_birth_date": f"{birth_year}-0{random.randint(1,9)}-{random.randint(10,28)}T01:00:00",
            "act_date": f"{birth_year}-0{random.randint(1,9)}-{random.randint(10,28)}T01:00:00",
            "act_number": f"10-{random.randint(558,599)}-{birth_year-2000:02d}-{random.randint(1000000,9999999):07d}",
            "zags_name_kz": "Алматы қ. Наурызбай ауданы әкім аппараты Азаматтық хал актілерін тіркеу бөлімі",
            "zags_name_ru": "Аппарат акима Наурызбайского района г. Алматы  отдел регистрации актов гражданского состояния"
        }
        children.append(child)
    
    return children

@app.route('/api/get-child', methods=['POST'])
def get_child():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Нет данных в запросе"}), 400
        
        phone = data.get('phone')
        iin = data.get('iin')
        
        if not phone or not iin:
            return jsonify({"error": "Требуются поля phone и iin"}), 400
        
        print(f"Запрос для ИИН: {iin}")
        
        # Для специального ИИН возвращаем фиксированные данные
        if iin == "971202300696":
            children_data = FIXED_CHILDREN
            print("Возвращаем фиксированные данные")
        else:
            # Генерируем случайных детей
            children_data = generate_simple_children()
            print(f"Сгенерировано детей: {len(children_data)}")
        
        return jsonify({
            "success": True,
            "data": {
                "result": 2,
                "childs": children_data
            }
        })
        
    except Exception as e:
        print(f"ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Внутренняя ошибка сервера: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK", "service": "child-service"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5003))
    print(f"🚀 Запуск Child Service на порту {port}")
    app.run(debug=False, host='0.0.0.0', port=port)


