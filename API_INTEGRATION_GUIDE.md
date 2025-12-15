# API интеграция - Нове наддомы

## Как обработан запрос для сохранения заказа:

### 1. Клиент отправляет данные

```javascript
fetch('/api/orders/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        table_id: 1,
        items: [{dish_id: 1, quantity: 2, price: 300}],
        total_price: 600
    })
})
```

### 2. API нолучает реквест

```python
# app/api/order.py
@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.create_order(order_data)
```

### 3. Сервис обрабатывает данные

```python
# app/services/order.py
def create_order(self, order_data: OrderCreate, user_id: int):
    # Сохраняем заказ
    # Обновляем статус стола
    # Возвращаем результат
```

### 4. Репозиторий сохраняет в БД

```python
# app/repositories/order_repository.py
def create(self, order_data: OrderCreate, user_id: int):
    db_order = Order(...)
    session.add(db_order)
    session.commit()
    return db_order
```

### 5. Ответ клиенту

```json
{
    "id": 123,
    "table_id": 1,
    "status": "pending",
    "total_price": 600,
    "created_at": "2024-12-15T22:35:00"
}
```

## Готовые эндпоинты

### Заказы

```
GET    /api/orders/              - Получить все
ПОСТ   /api/orders/              - Сохранить новый
ГЕТ    /api/orders/{id}          - Получить один
ПУТ    /api/orders/{id}          - Обновить
ДЕЛЕТЕ  /api/orders/{id}          - Удалить
```

### Блюда

```
GET    /api/dishes/              - Получить все
ПОСТ   /api/dishes/              - Сохранить новое
ГЕТ    /api/dishes/{id}          - Получить одно
ПУТ    /api/dishes/{id}          - Обновить
ДЕЛЕТЕ  /api/dishes/{id}          - Удалить
```

### Столики

```
GET    /api/tables/              - Получить все
ПОСТ   /api/tables/              - Сохранить новый
ГЕТ    /api/tables/{id}          - Получить один
ПУТ    /api/tables/{id}          - Обновить
ДЕЛЕТЕ  /api/tables/{id}          - Удалить
```
