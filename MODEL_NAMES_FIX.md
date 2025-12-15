# Второе Исправление - НЕ ТЕ ИМЕНА МОДЕЛЕЙ

## ОШИбКА

```
ImportError: cannot import name 'Dish' from 'app.models.dishes'
```

## ПРОБЛЕМА

Классы моделей имеют другие имена:

| ОЖИДАЛи | ГЫЛИ | ФАйЛ |
|----------|-------|----------|
| `Dish` | `DishesModel` | `app/models/dishes.py` |
| `Order` | `OrderModel` | `app/models/order.py` |
| `Table` | `TablesModel` | `app/models/tables.py` |
| `User` | `User` | `app/models/users.py` |

## ОЧЕНЬ ВНОВЬ ОНО!

### Обновленные ОНО (проверь теперь)

#### Сервисы (3 файла)

```python
# app/services/dishes.py
from app.models.dishes import DishesModel  # ✅

class DishService:
    def get_all_dishes(self):
        return self.db.query(DishesModel).all()  # ✅
```

```python
# app/services/order.py
from app.models.order import OrderModel      # ✅
from app.models.tables import TablesModel   # ✅

class OrderService:
    def create_order(self, order_data, user_id):
        db_order = OrderModel(...)  # ✅
```

```python
# app/services/tables.py
from app.models.tables import TablesModel  # ✅

class TableService:
    def get_all_tables(self):
        return self.db.query(TablesModel).all()  # ✅
```

#### Репозитории (3 файла)

```python
# app/repositories/dish_repository.py
from app.models.dishes import DishesModel  # ✅

class DishRepository:
    def find_all(self):
        return self.db.query(DishesModel).all()  # ✅
```

```python
# app/repositories/order_repository.py
from app.models.order import OrderModel  # ✅

class OrderRepository:
    def create(self, order_data, user_id):
        db_order = OrderModel(...)  # ✅
```

```python
# app/repositories/table_repository.py
from app.models.tables import TablesModel  # ✅

class TableRepository:
    def find_all(self):
        return self.db.query(TablesModel).all()  # ✅
```

## ВНЮЧЕННЫЕ КОММИТЫ

| Коммит | ОПисание |
|---------|------------|
| 488bcde7 | fix: Обновлены имена моделей в сервисах |
| 3242f3df | fix: Обновлены имена моделей в репозиториях |

## НАста ПОТЮШИСОЮ

### 1. Обновите код

```bash
git pull origin main
```

### 2. Откройте исободные пакеты

```bash
# Если нужно
pip install -r requirements.txt
```

### 3. Запустите приложение

```bash
python main.py
```

### 4. Должно работать

```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 5. Протестируйте API

```bash
# Тест блюд
curl http://localhost:8000/api/dishes/

# Тест столик
curl http://localhost:8000/api/tables/

# Тест заказов
curl http://localhost:8000/api/orders/
```

## ОЧЕКИВАЕМЫЕ ОТВЕТЫ

### GET /api/dishes/

```json
[
  {
    "id": 1,
    "name": "Пицца Маргарита",
    "price": 400,
    "description": "Классическая итальянская пицца"
  }
]
```

### GET /api/tables/

```json
[
  {
    "id": 1,
    "table_number": 1,
    "capacity": 4,
    "status": "available"
  }
]
```

### GET /api/orders/

```json
[
  {
    "id": 1,
    "table_id": 1,
    "status": "created",
    "total_amount": 600
  }
]
```

## НЕРОБЛЕМЫ КЕЙ

### Ошибка: `ModuleNotFoundError: No module named 'app.schemas'`

Проверьте:
```bash
ls -la app/schemas.py
```

Он должен существовать для использования Pydantic схем.

### Ошибка: `AttributeError: type object 'Session' has no attribute 'query'`

Обновите SQLAlchemy:
```bash
pip install --upgrade sqlalchemy
```

## ОПОШОСУММА

```
✅ Обновлено: 6 файлов
✅ Названия моделей исправлены
✅ Вместо дв коммитов внесено
✅ Готов к тестированию
```

---

✨ **ТЕПЕРЬ Всё должно работать!**
