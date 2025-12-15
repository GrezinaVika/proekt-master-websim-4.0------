# Быстрый Начало

## Шаг 1: Притягни изменения

```bash
cd /path/to/your/project
git pull origin main
```

## Шаг 2: Проверь новые файлы

```
app/
├── services/
│  ├── __init__.py
│  ├── users.py ✅
│  ├── order.py ✅
│  ├── tables.py ✅
│  └── dishes.py ✅
└── repositories/
   ├── __init__.py
   ├── user_repository.py ✅
   ├── order_repository.py ✅
   ├── table_repository.py ✅
   └── dish_repository.py ✅
```

## Шаг 3: Проверь документацию

- **SETUP_INSTRUCTIONS.md** - При внедрении всего
- **INTEGRATION_CHECKLIST.md** - Когда что-то не работает
- **API_INTEGRATION_GUIDE.md** - Как работает система
- **TESTING_EXAMPLES.md** - Тестируем всё
- **IMPLEMENTATION_STATUS.md** - Что сделано

## Шаг 4: Запустить Приложение

```bash
python main.py
```

## Шаг 5: Протестируйте API

```bash
# Получить все блюда
curl http://localhost:8000/api/dishes/

# Получить все заказы
curl http://localhost:8000/api/orders/

# Получить все таблицы
curl http://localhost:8000/api/tables/
```

## Шаг 6: Открыть Апликацию

http://localhost:8000

## Нормальные Тесты

1. **Авторизоваться**
   - Login: `ofikNum1`
   - Password: `123321`
   - Role: `waiter`

2. **Получить Меню**
   - На жать 2-3 секунды
   - Ндолжны нагружаться блюда

3. **Получить Таблицы**
   - На жать 2-3 секунды
   - Ндолжны нагружаться столики

4. **Сохранить Заказ**
   - Выбрать столик
   - Добавить блюда
   - Нажать "Отправить заказ"
   - Ндолжно это найтись в списке

## Проблемы?

Осм. следующие файлы:

1. **IMPLEMENTATION_STATUS.md** - что сделано
2. **INTEGRATION_CHECKLIST.md** - как определить проблему
3. **TESTING_EXAMPLES.md** - как тестируем
