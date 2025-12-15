# Чек-лист интеграции

## Файлы сервисов

- [x] `app/services/__init__.py` - создан
- [x] `app/services/users.py` - создан
- [x] `app/services/order.py` - создан
- [x] `app/services/tables.py` - создан
- [x] `app/services/dishes.py` - создан

## Файлы репозиториев

- [x] `app/repositories/__init__.py` - создан
- [x] `app/repositories/user_repository.py` - создан
- [x] `app/repositories/order_repository.py` - создан
- [x] `app/repositories/table_repository.py` - создан
- [x] `app/repositories/dish_repository.py` - создан

## API интеграция

- [x] `app/api/dependencies.py` - водопроводы добавлены
- [x] `app/api/order.py` - обработка оформлена
- [x] `app/api/dishes.py` - обработка оформлена
- [x] `app/api/tables.py` - обработка оформлена

## Тестирование

### GET реквесты
- [x] GET `/api/orders/` - возвращает данные
- [x] GET `/api/dishes/` - возвращает данные
- [x] GET `/api/tables/` - возвращает данные

### POST реквесты
- [x] POST `/api/orders/` - сохраняет в базу
- [x] POST `/api/dishes/` - сохраняет в базу
- [x] POST `/api/tables/` - сохраняет в базу

### PUT реквесты
- [x] PUT `/api/orders/{id}` - обновляет в базе
- [x] PUT `/api/dishes/{id}` - обновляет в базе
- [x] PUT `/api/tables/{id}` - обновляет в базе

### DELETE реквесты
- [x] DELETE `/api/orders/{id}` - удаляет из базы
- [x] DELETE `/api/dishes/{id}` - удаляет из базы
- [x] DELETE `/api/tables/{id}` - удаляет из базы

## JavaScript интеграция

- [x] `app/static/js/app.js` - отправляет fetch реквесты
- [x] `createOrder()` - сохраняет в базу
- [x] `updateOrderStatus()` - обновляет статус
- [x] `getTables()` - отдает все столики
- [x] `getDishes()` - отдает все блюда
