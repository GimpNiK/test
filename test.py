import requests
import json
import sys

# Базовый URL вашего API
BASE_URL = "http://127.0.0.1:5000"

def print_response(method, endpoint, response):
    """Красиво печатает ответ API"""
    print(f"\n{'='*60}")
    print(f"{method} {endpoint}")
    print(f"Status: {response.status_code}")
    if response.text:
        try:
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        except:
            print(f"Response: {response.text}")
    print(f"{'='*60}")

def test_hello():
    """Тест эндпоинта /hello"""
    response = requests.get(f"{BASE_URL}/hello")
    print_response("GET", "/hello", response)
    return response.status_code == 200 and response.text == "Hello"

def test_table():
    """Тест эндпоинта /table"""
    response = requests.get(f"{BASE_URL}/table")
    print_response("GET", "/table", response)
    return response.status_code == 200 and "Table" in response.text

def test_get_all_tasks():
    """Тест получения всех задач"""
    response = requests.get(f"{BASE_URL}/api/tasks")
    print_response("GET", "/api/tasks", response)
    return response.status_code == 200

def test_create_task():
    """Тест создания задачи"""
    task_data = {
        "title": "Тестовая задача",
        "description": "Это тестовая задача созданная через API",
        "completed": False
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data,
        headers={"Content-Type": "application/json"}
    )
    print_response("POST", "/api/tasks", response)
    
    if response.status_code == 201:
        data = response.json()
        print(f"✅ Создана задача с ID: {data.get('id')}")
        return data.get('id')
    return None

def test_get_task(task_id):
    """Тест получения задачи по ID"""
    if not task_id:
        return False
    
    response = requests.get(f"{BASE_URL}/api/tasks/{task_id}")
    print_response("GET", f"/api/tasks/{task_id}", response)
    return response.status_code == 200

def test_update_task(task_id):
    """Тест обновления задачи"""
    if not task_id:
        return False
    
    update_data = {
        "title": "Обновленная задача",
        "completed": True
    }
    
    response = requests.put(
        f"{BASE_URL}/api/tasks/{task_id}",
        json=update_data,
        headers={"Content-Type": "application/json"}
    )
    print_response("PUT", f"/api/tasks/{task_id}", response)
    return response.status_code == 200

def test_toggle_task(task_id):
    """Тест переключения статуса задачи"""
    if not task_id:
        return False
    
    response = requests.patch(f"{BASE_URL}/api/tasks/{task_id}/toggle")
    print_response("PATCH", f"/api/tasks/{task_id}/toggle", response)
    return response.status_code == 200

def test_delete_task(task_id):
    """Тест удаления задачи"""
    if not task_id:
        return False
    
    response = requests.delete(f"{BASE_URL}/api/tasks/{task_id}")
    print_response("DELETE", f"/api/tasks/{task_id}", response)
    return response.status_code == 200

def test_create_task_validation():
    """Тест валидации при создании задачи"""
    print("\n🔍 Тестирование валидации...")
    
    # Тест 1: Отсутствует title
    task_data = {
        "description": "Задача без заголовка"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data,
        headers={"Content-Type": "application/json"}
    )
    print_response("POST (без title)", "/api/tasks", response)
    
    if response.status_code == 400:
        print("✅ Валидация работает: title обязателен")
    else:
        print("❌ Валидация не работает")
        return False
    
    # Тест 2: Минимальные данные
    task_data = {
        "title": "Минимальная задача"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tasks",
        json=task_data,
        headers={"Content-Type": "application/json"}
    )
    print_response("POST (минимальные данные)", "/api/tasks", response)
    
    return response.status_code == 201

def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Начинаем тестирование REST API...")
    print(f"Базовая ссылка: {BASE_URL}")
    
    results = []
    created_task_id = None
    
    try:
        # Тест 1: Простой эндпоинт
        print("\n1️⃣ Тестируем /hello...")
        results.append(("GET /hello", test_hello()))
        
        # Тест 2: HTML страница
        print("\n2️⃣ Тестируем /table...")
        results.append(("GET /table", test_table()))
        
        # Тест 3: Получение всех задач
        print("\n3️⃣ Тестируем GET /api/tasks...")
        results.append(("GET /api/tasks", test_get_all_tasks()))
        
        # Тест 4: Создание задачи
        print("\n4️⃣ Тестируем POST /api/tasks...")
        created_task_id = test_create_task()
        results.append(("POST /api/tasks", created_task_id is not None))
        
        if created_task_id:
            # Тест 5: Получение задачи по ID
            print("\n5️⃣ Тестируем GET /api/tasks/{id}...")
            results.append((f"GET /api/tasks/{created_task_id}", test_get_task(created_task_id)))
            
            # Тест 6: Обновление задачи
            print("\n6️⃣ Тестируем PUT /api/tasks/{id}...")
            results.append((f"PUT /api/tasks/{created_task_id}", test_update_task(created_task_id)))
            
            # Тест 7: Переключение статуса
            print("\n7️⃣ Тестируем PATCH /api/tasks/{id}/toggle...")
            results.append((f"PATCH /api/tasks/{created_task_id}/toggle", test_toggle_task(created_task_id)))
            
            # Тест 8: Валидация
            print("\n8️⃣ Тестируем валидацию...")
            results.append(("Валидация", test_create_task_validation()))
            
            # Тест 9: Удаление задачи
            print("\n9️⃣ Тестируем DELETE /api/tasks/{id}...")
            results.append((f"DELETE /api/tasks/{created_task_id}", test_delete_task(created_task_id)))
        
        # Итог
        print("\n" + "="*60)
        print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
        print("="*60)
        
        passed = 0
        total = len(results)
        
        for test_name, success in results:
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"{status}: {test_name}")
            if success:
                passed += 1
        
        print(f"\nИтого: {passed}/{total} тестов пройдено успешно")
        
        if passed == total:
            print("\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ! API работает корректно.")
            return 0
        else:
            print(f"\n⚠️ {total - passed} тестов не прошли. Проверьте API.")
            return 1
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Не удалось подключиться к {BASE_URL}")
        print("Убедитесь, что Flask приложение запущено командой: python ваш_файл.py")
        return 1
    except Exception as e:
        print(f"\n❌ Произошла ошибка: {e}")
        return 1

if __name__ == "__main__":
    # Проверяем, запущено ли приложение
    try:
        response = requests.get(BASE_URL, timeout=2)
    except:
        print("⚠️ Внимание: Flask приложение не отвечает.")
        print("Запустите приложение в отдельном терминале, затем запустите этот тест.")
        user_input = input("Продолжить тестирование? (y/n): ")
        if user_input.lower() != 'y':
            sys.exit(1)
    
    sys.exit(run_all_tests())
    print()