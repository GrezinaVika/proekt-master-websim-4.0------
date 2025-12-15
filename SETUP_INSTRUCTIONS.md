# Полная инструкция по внедрению исправлений

## Что было сделано:

### ✅ Созданы сервисы (app/services/)
- `users.py` - Обработка пользователей
- `order.py` - Обработка заказов
- `tables.py` - Обработка столиков
- `dishes.py` - Обработка меню

### ✅ Созданы репозитории (app/repositories/)
- `user_repository.py` - Доступ к данным пользователей
- `order_repository.py` - Доступ к данным заказов
- `table_repository.py` - Доступ к данным столиков
- `dish_repository.py` - Доступ к данным блюд

## Проверка работающей интеграции

### 1. API ОК

Проверить что все эндпоинты работают:

```bash
# Получить все заказы
curl http://localhost:8000/api/orders/

# Ответ должен быть JSON массив, не ошибка 500
```

### 2. Пример авторизации

```bash
Логин: ofikNum1
Пассворд: 123321
Роль: waiter
```

### 3. Проверка меню

```bash
curl http://localhost:8000/api/dishes/

# Должны вернуться блюда из базы
```

### 4. Проверка столиков

```bash
curl http://localhost:8000/api/tables/

# Должны вернуться таблицы из базы
```

## Архитектура системы

```
ИНТЕРФЕЙС (JavaScript)
      ↑
      │ fetch('/api/orders/', {method: 'POST', body})
      │
API РОУТЕР (app/api/order.py)
      ↑
      │ @router.post("/")
      │
СЕРВИС (app/services/order.py)
      ↑
      │ OrderService.create_order()
      ↑
РЕПОЗИТОРИЙ (app/repositories/order_repository.py)
      ↑
      │ session.add(order)
      │ session.commit()
      ↑
БАЗА ДАННЫХ (restaurant.db)
      ↑
      │ INSERT INTO orders...
      ↑
ИНТЕРФЕЙС (Success Message)
```

## Ошибки и решения

### Ошибка 500
Это означает, что нет всех нужных сервисов.

Проверьте:
- Путь к файлам сервисов
- Путь к файлам репозиториев
- Импорты в dependencies.py

### Ответ 404
Данные не найдены в базе.

Проверьте таблицы:
```bash
sqlite3 restaurant.db "SELECT * FROM orders;"
```
