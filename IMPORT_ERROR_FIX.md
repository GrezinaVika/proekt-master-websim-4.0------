# Исправление Ошибки ImportError

## Проблема

```
ImportError: cannot import name 'Dish' from 'app.models'
```

## Цауза

В вашем проекте модели расположены в отдельных файлах:

```
app/models/
  ├── dishes.py      ✓
  ├── order.py       ✓
  ├── tables.py      ✓
  ├── users.py       ✓
  └── __init__.py    (пустой)
```

Поэтому когда сервисы обычно пытались импортировать:

```python
# ОШИБКА:
from app.models import Dish  # Не работает!
```

## Решение

### ОНО ФИКСЕД:

Все сервисы и репозитории теперь импортируют модели непосредственно:

```python
# ПОРАВНО:
from app.models.dishes import Dish  ✓
from app.models.order import Order  ✓
from app.models.tables import Table  ✓
from app.models.users import User   ✓
```

## Обновленные Файлы

### Сервисы (✅ исправлены)

1. **app/services/users.py**
   - импорт: `from app.models.users import User`

2. **app/services/order.py**
   - импорты: `from app.models.order import Order`
   - `from app.models.order_items import OrderItem`
   - `from app.models.tables import Table`

3. **app/services/tables.py**
   - импорт: `from app.models.tables import Table`

4. **app/services/dishes.py**
   - импорт: `from app.models.dishes import Dish`

### Репозитории (✅ исправлены)

1. **app/repositories/user_repository.py**
   - импорт: `from app.models.users import User`

2. **app/repositories/order_repository.py**
   - импорты: `from app.models.order import Order`
   - `from app.models.order_items import OrderItem`

3. **app/repositories/table_repository.py**
   - импорт: `from app.models.tables import Table`

4. **app/repositories/dish_repository.py**
   - импорт: `from app.models.dishes import Dish`

## Что Дальше?

### 1. Обновите репо локально

```bash
git pull origin main
```

### 2. Запустите приложение

```bash
python main.py
```

### 3. У вас должно быть:

```
✅ Uvicorn running on http://127.0.0.1:8000
```

### 4. Открыть в браузере

```
http://localhost:8000
```

## Нормальные Ответы При Тестировании

### GET /api/dishes/

```bash
curl http://localhost:8000/api/dishes/
```

**Ответ:**
```json
[
  {"id": 1, "name": "Пицца", "price": 400, ...},
  {"id": 2, "name": "Паста", "price": 450, ...}
]
```

### GET /api/tables/

```bash
curl http://localhost:8000/api/tables/
```

**Ответ:**
```json
[
  {"id": 1, "table_number": 1, "status": "free", ...},
  {"id": 2, "table_number": 2, "status": "free", ...}
]
```

### GET /api/orders/

```bash
curl http://localhost:8000/api/orders/
```

**Ответ:**
```json
[
  {"id": 1, "table_id": 1, "status": "pending", "total_price": 600, ...}
]
```

## Если Ошибка Еще

### Ошибка: `ModuleNotFoundError: No module named 'app.schemas'`

```bash
# Проверьте что это такое
ls app/schemas.py

# Оно должно быть в списке
```

### Ошибка: `AttributeError: type object 'Session' has no attribute 'query'`

```python
# Проверьте SQLAlchemy версию
pip list | grep -i sqlalchemy

# Должна быть 1.x или 2.x
```

## Короткие Ответы

### Проверка

```bash
# На какой версии Пайтон?
python --version  # 3.13

# Какие пакеты установлены?
pip list | head -20

# Не стоит ли введение pytest?
python -m pytest app/services/
```

## Успех!

А теперь всё должно работать! ✅
