# Примеры тестирования API

## 1. Тестирование Через cURL

### Получить все блюда
```bash
curl http://localhost:8000/api/dishes/
```

### Получить доне блюдо
```bash
curl http://localhost:8000/api/dishes/1
```

### Надать новое блюдо
```bash
curl -X POST http://localhost:8000/api/dishes/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Паста
",
    "description": "Нытальянское блюдо",
    "price": 450,
    "category": "Плавные блюда"
  }'
```

### Обновить блюдо
```bash
curl -X PUT http://localhost:8000/api/dishes/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 500}'
```

### Удалить блюдо
```bash
curl -X DELETE http://localhost:8000/api/dishes/1
```

## 2. Тестирование Ордеров

### Получить все заказы
```bash
curl http://localhost:8000/api/orders/
```

### Получить один заказ
```bash
curl http://localhost:8000/api/orders/1
```

### сохранить новый заказ
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_id": 1,
    "items": [
      {"dish_id": 1, "quantity": 2, "price": 300},
      {"dish_id": 2, "quantity": 1, "price": 450}
    ],
    "total_price": 1050
  }'
```

### Обновить статус заказа
```bash
curl -X PUT http://localhost:8000/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

### Удалить заказ
```bash
curl -X DELETE http://localhost:8000/api/orders/1
```

## 3. Тестирование Таблиц

### Получить все таблицы
```bash
curl http://localhost:8000/api/tables/
```

### Получить одну таблицу
```bash
curl http://localhost:8000/api/tables/1
```

### Получить таблицу по номеру
```bash
curl http://localhost:8000/api/tables/number/5
```

### сохранить новую таблицу
```bash
curl -X POST http://localhost:8000/api/tables/ \
  -H "Content-Type: application/json" \
  -d '{
    "table_number": 5,
    "seats": 4
  }'
```

### Обновить статус таблицы
```bash
curl -X PATCH http://localhost:8000/api/tables/1/status/occupied
```

### Удалить таблицу
```bash
curl -X DELETE http://localhost:8000/api/tables/1
```

## 4. Тестирование о на JavaScript

### На вкладке девтюлс, раскройте консоль (даже короткие команды):

```javascript
// Получить все блюда
fetch('/api/dishes/')
  .then(r => r.json())
  .then(d => console.log(d))

// Получить все заказы
fetch('/api/orders/')
  .then(r => r.json())
  .then(o => console.log(o))

// Получить все таблицы
fetch('/api/tables/')
  .then(r => r.json())
  .then(t => console.log(t))

// сохранить новый заказ
fetch('/api/orders/', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    table_id: 1,
    items: [{dish_id: 1, quantity: 2, price: 300}],
    total_price: 600
  })
})
.then(r => r.json())
.then(o => console.log('Заказ сохранен:', o))

// Обновить статус заказа
fetch('/api/orders/1', {
  method: 'PUT',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({status: 'completed'})
})
.then(r => r.json())
.then(o => console.log('Статус обновлен:', o))
```

## 5. Положительные Ответы

### 200 OK - Успешное GET запрос
```json
[
  {
    "id": 1,
    "name": "Пицца Маргарита",
    "price": 400,
    "category": "Пицца"
  }
]
```

### 201 Created - Успешное POST
```json
{
  "id": 2,
  "name": "Паста",
  "price": 450,
  "category": "Плавные блюда"
}
```

### 204 No Content - Успешное DELETE
Нет тела ответа

## 6. Отрицательные Ответы

### 404 Not Found
```json
{
  "detail": "Dish not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Table with number 5 already exists"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## 7. Проверка Базы Данных

### Открыть БД
```bash
sqlite3 restaurant.db
```

### Показать таблицы
```sql
.tables
```

### Показать структуру таблицы
```sql
.schema orders
.schema dishes
.schema tables
```

### Показать заказы
```sql
SELECT * FROM orders;
SELECT * FROM orders WHERE status = 'pending';
SELECT COUNT(*) FROM orders;
```

### Показать блюда
```sql
SELECT * FROM dishes;
SELECT * FROM dishes WHERE available = 1;
SELECT COUNT(*) FROM dishes;
```

### Показать таблицы
```sql
SELECT * FROM tables;
SELECT * FROM tables WHERE status = 'free';
SELECT COUNT(*) FROM tables;
```
