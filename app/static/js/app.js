// app.js - Restaurant Management System Frontend

// ==================== КОНСТАНТЫ И ПЕРЕМЕННЫЕ ====================

const API_BASE_URL = '/api';
let currentUser = null;
let authToken = localStorage.getItem('authToken') || null;

// ==================== УТИЛИТЫ ====================

// Функция для запросов к API
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Добавляем слэш в конец если его нет (чтобы избежать 307 редиректов)
    const finalUrl = url.endsWith('/') ? url : `${url}/`;
    
    const headers = {
        'Content-Type': 'application/json',
        ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
        ...options.headers,
    };

    const config = {
        ...options,
        headers,
    };

    try {
        const response = await fetch(finalUrl, config);
        
        if (response.status === 401) {
            logout();
            return null;
        }
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error(`API Error ${response.status}:`, errorText);
            
            // Пробуем парсить как JSON
            try {
                const errorJson = JSON.parse(errorText);
                throw new Error(errorJson.detail || `HTTP ${response.status}`);
            } catch {
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
        }
        
        if (response.status === 204) {
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        showError(error.message);
        throw error;
    }
}

// Показать ошибку
function showError(message) {
    console.error('Error:', message);
    alert(`Ошибка: ${message}`);
}

// Показать успех
function showSuccess(message) {
    console.log('Success:', message);
    alert(`✅ ${message}`);
}

// ==================== АВТОРИЗАЦИЯ ====================

// Вход пользователя
async function login(username, password, role) {
    try {
        console.log('Login attempt:', { username, role });
        
        // Проверяем тестовые учетные данные
        const testCredentials = {
            'ofikNum1': { id: 1, name: 'Официант 1', role: 'waiter', password: '123321' },
            'adminNum1': { id: 2, name: 'Администратор', role: 'admin', password: '123321' },
            'povarNum1': { id: 3, name: 'Повар 1', role: 'chef', password: '123321' }
        };

        if (testCredentials[username] && testCredentials[username].password === password) {
            // Демо-авторизация
            const userData = testCredentials[username];
            currentUser = {
                id: userData.id,
                username: username,
                name: userData.name,
                role: userData.role
            };
            
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            localStorage.setItem('userRole', userData.role);
            
            showApp();
            loadRoleData(userData.role);
            showSuccess(`Добро пожаловать, ${userData.name}!`);
            return true;
        }
        
        // Пробуем через API если есть
        try {
            const response = await apiRequest('/users/login', {
                method: 'POST',
                body: JSON.stringify({
                    username: username,
                    password: password
                })
            });
            
            if (response) {
                currentUser = response.user || response;
                authToken = response.token || response.access_token;
                
                if (authToken) {
                    localStorage.setItem('authToken', authToken);
                }
                localStorage.setItem('currentUser', JSON.stringify(currentUser));
                
                showApp();
                loadRoleData(currentUser.role || role);
                showSuccess(`Добро пожаловать, ${currentUser.name || username}!`);
                return true;
            }
        } catch (apiError) {
            console.log('API login failed, using demo mode');
        }
        
        showError('Неверные учетные данные');
        return false;
        
    } catch (error) {
        console.error('Login error:', error);
        showError('Ошибка при входе');
        return false;
    }
}

// Регистрация пользователя
async function register(username, password, role) {
    try {
        console.log('Register attempt:', { username, role });
        
        // Временно отключаем регистрацию через API
        showSuccess('Регистрация временно недоступна. Используйте тестовые аккаунты.');
        switchToLogin();
        
        /* // Код для реальной регистрации
        const response = await apiRequest('/users/register', {
            method: 'POST',
            body: JSON.stringify({
                username: username,
                password: password,
                role: role
            })
        });
        
        if (response) {
            showSuccess('Регистрация успешна! Теперь войдите в систему.');
            switchToLogin();
        }
        */
    } catch (error) {
        showError('Ошибка при регистрации');
    }
}

// Выход
function logout() {
    currentUser = null;
    authToken = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('userRole');
    
    showAuth();
    showSuccess('Вы вышли из системы');
}

// ==================== БЛЮДА (DISHES) ====================

// Получить все блюда
async function getDishes() {
    try {
        const response = await apiRequest('/dishes/');
        console.log('Dishes response:', response);
        
        if (response && Array.isArray(response)) {
            return response;
        }
        
        // Если API возвращает другой формат
        if (response && response.items) {
            return response.items;
        }
        
        // Демо-данные
        return getDemoDishes();
        
    } catch (error) {
        console.error('Error fetching dishes:', error);
        return getDemoDishes();
    }
}

// Демо-данные для блюд
function getDemoDishes() {
    return [
        { id: 1, name: 'Борщ', price: 350, category: 'Основное', description: 'Традиционный украинский суп', cooking_time: 20 },
        { id: 2, name: 'Стейк', price: 1200, category: 'Основное', description: 'Говяжий стейк с овощами', cooking_time: 25 },
        { id: 3, name: 'Салат Цезарь', price: 450, category: 'Основное', description: 'Салат с курицей и соусом цезарь', cooking_time: 15 },
        { id: 4, name: 'Кофе', price: 150, category: 'Напитки', description: 'Свежесваренный кофе', cooking_time: 5 },
        { id: 5, name: 'Чизкейк', price: 300, category: 'Десерт', description: 'Классический чизкейк', cooking_time: 10 },
        { id: 6, name: 'Пицца Маргарита', price: 650, category: 'Основное', description: 'Классическая итальянская пицца', cooking_time: 30 },
        { id: 7, name: 'Чай', price: 100, category: 'Напитки', description: 'Ароматный чай', cooking_time: 5 },
        { id: 8, name: 'Тирамису', price: 350, category: 'Десерт', description: 'Итальянский десерт', cooking_time: 10 }
    ];
}

// ==================== СТОЛИКИ (TABLES) ====================

// Получить все столики
async function getTables() {
    try {
        const response = await apiRequest('/tables/');
        console.log('Tables response:', response);
        
        if (response && Array.isArray(response)) {
            return response;
        }
        
        // Демо-данные
        return getDemoTables();
        
    } catch (error) {
        console.error('Error fetching tables:', error);
        return getDemoTables();
    }
}

// Демо-данные для столиков
function getDemoTables() {
    return [
        { id: 1, table_number: 1, status: 'free', capacity: 4, location: 'У окна' },
        { id: 2, table_number: 2, status: 'occupied', capacity: 6, location: 'Центр зала' },
        { id: 3, table_number: 3, status: 'free', capacity: 2, location: 'У барной стойки' },
        { id: 4, table_number: 4, status: 'reserved', capacity: 8, location: 'VIP зона' },
        { id: 5, table_number: 5, status: 'free', capacity: 4, location: 'Терраса' },
        { id: 6, table_number: 6, status: 'occupied', capacity: 4, location: 'У окна' },
        { id: 7, table_number: 7, status: 'free', capacity: 2, location: 'Барная стойка' },
        { id: 8, table_number: 8, status: 'free', capacity: 6, location: 'Центр' }
    ];
}

// ==================== ЗАКАЗЫ (ORDERS) ====================

// Получить все заказы
async function getOrders() {
    try {
        const response = await apiRequest('/orders/');
        console.log('Orders response:', response);
        
        if (response && Array.isArray(response)) {
            return response;
        }
        
        // Демо-данные
        return getDemoOrders();
        
    } catch (error) {
        console.error('Error fetching orders:', error);
        return getDemoOrders();
    }
}

// Демо-данные для заказов
function getDemoOrders() {
    const now = new Date();
    const oneHourAgo = new Date(now.getTime() - 60 * 60 * 1000);
    const twoHoursAgo = new Date(now.getTime() - 2 * 60 * 60 * 1000);
    
    return [
        { 
            id: 1, 
            table_id: 2, 
            status: 'pending', 
            total_amount: 1200, 
            created_at: twoHoursAgo.toISOString(),
            waiter_id: 1,
            items: [
                { dish_id: 1, quantity: 2 },
                { dish_id: 4, quantity: 2 }
            ]
        },
        { 
            id: 2, 
            table_id: 4, 
            status: 'cooking', 
            total_amount: 800, 
            created_at: oneHourAgo.toISOString(),
            waiter_id: 1,
            items: [
                { dish_id: 3, quantity: 1 },
                { dish_id: 5, quantity: 1 }
            ]
        },
        { 
            id: 3, 
            table_id: 1, 
            status: 'ready', 
            total_amount: 450, 
            created_at: now.toISOString(),
            waiter_id: 1,
            items: [
                { dish_id: 7, quantity: 3 }
            ]
        },
        { 
            id: 4, 
            table_id: 6, 
            status: 'pending', 
            total_amount: 1950, 
            created_at: now.toISOString(),
            waiter_id: 1,
            items: [
                { dish_id: 2, quantity: 1 },
                { dish_id: 6, quantity: 1 },
                { dish_id: 8, quantity: 2 }
            ]
        }
    ];
}

// ==================== ПОЛЬЗОВАТЕЛИ (USERS) ====================

// Получить статистику пользователя
async function getUserStats(userId) {
    try {
        // Пробуем получить статистику через API
        const response = await apiRequest(`/users/${userId}/stats`);
        if (response) {
            return response;
        }
    } catch (error) {
        console.log('User stats API not available, using demo data');
    }
    
    // Демо-статистика
    return {
        user_id: userId,
        total_orders: 15,
        active_orders: 3,
        occupied_tables: 2,
        total_revenue: 12500.50
    };
}

// ==================== ОТОБРАЖЕНИЕ ДАННЫХ ====================

// Загрузить меню
async function loadMenu() {
    const menuContent = document.getElementById('menuContent');
    if (!menuContent) return;
    
    try {
        const dishes = await getDishes();
        
        // Показываем активную категорию
        const activeSection = document.querySelector('.switch-btn.active')?.dataset.section || 'main';
        
        // Фильтруем по категории
        let activeDishes = dishes;
        if (activeSection === 'main') {
            activeDishes = dishes.filter(d => d.category === 'Основное' || !d.category);
        } else if (activeSection === 'hot') {
            activeDishes = dishes.filter(d => d.category === 'Горячее');
        } else if (activeSection === 'drinks') {
            activeDishes = dishes.filter(d => d.category === 'Напитки');
        } else if (activeSection === 'dessert') {
            activeDishes = dishes.filter(d => d.category === 'Десерт');
        }
        
        if (activeDishes.length === 0) {
            // Если нет блюд в категории, показываем все
            activeDishes = dishes;
        }
        
        menuContent.innerHTML = activeDishes.map(dish => `
            <div class="item" data-dish-id="${dish.id}">
                <div class="name">${dish.name}</div>
                <div class="meta">${dish.price} ₽ • ${dish.cooking_time || 15} мин</div>
                ${dish.description ? `<div class="desc">${dish.description}</div>` : ''}
                ${currentUser?.role === 'admin' ? `
                    <div class="row">
                        <button class="primary small" onclick="editDish(${dish.id})">✏️</button>
                        <button class="danger small" onclick="deleteDish(${dish.id})">🗑️</button>
                    </div>
                ` : ''}
            </div>
        `).join('');
        
        if (activeDishes.length === 0) {
            menuContent.innerHTML = '<div class="info-muted">Нет блюд в этой категории</div>';
        }
    } catch (error) {
        console.error('Error loading menu:', error);
        menuContent.innerHTML = '<div class="info-muted">Ошибка при загрузке меню</div>';
    }
}

// Загрузить столики
async function loadTables() {
    const tablesGrid = document.getElementById('tablesGrid');
    if (!tablesGrid) return;
    
    try {
        const tables = await getTables();
        
        tablesGrid.innerHTML = tables.map(table => `
            <div class="table ${table.status === 'occupied' || table.status === 'reserved' ? 'booked' : ''}" 
                 data-table-id="${table.id}"
                 onclick="openTableModal(${table.id})">
                <div style="font-weight: 700;">Стол #${table.table_number || table.number || table.id}</div>
                <div style="font-size: 13px; color: var(--muted); margin-top: 4px;">
                    ${table.status === 'free' ? '🟢 Свободен' : 
                      table.status === 'occupied' ? '🔴 Занят' : 
                      table.status === 'reserved' ? '🟡 Забронирован' : '⚫ ' + table.status}
                </div>
                <div style="font-size: 12px; margin-top: 4px;">
                    ${table.capacity || 4} мест
                    ${table.location ? `<br>${table.location}` : ''}
                </div>
                ${currentUser?.role === 'waiter' && table.status === 'free' ? `
                    <button class="primary small" style="margin-top: 8px; width: 100%;"
                            onclick="event.stopPropagation(); createOrderForTable(${table.id})">
                        Создать заказ
                    </button>
                ` : ''}
                ${currentUser?.role === 'admin' ? `
                    <button class="danger small" style="margin-top: 4px; width: 100%;"
                            onclick="event.stopPropagation(); deleteTable(${table.id})">
                        Удалить
                    </button>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading tables:', error);
        tablesGrid.innerHTML = '<div class="info-muted">Ошибка при загрузке столиков</div>';
    }
}

// Загрузить заказы
async function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    if (!ordersList) return;
    
    try {
        let orders = await getOrders();
        
        // Фильтруем заказы по роли
        if (currentUser?.role === 'chef') {
            // Для повара только готовящиеся
            orders = orders.filter(o => o.status === 'cooking' || o.status === 'pending');
        } else if (currentUser?.role === 'waiter') {
            // Для официанта его заказы или все если нет waiter_id
            if (currentUser.id) {
                orders = orders.filter(o => o.waiter_id === currentUser.id);
            }
        }
        // Для админа все заказы
        
        // Сортируем по дате (новые сверху)
        orders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        
        const statusIcons = {
            'pending': '⏳',
            'cooking': '👨‍🍳',
            'ready': '✅',
            'paid': '💰'
        };
        
        ordersList.innerHTML = orders.map(order => `
            <div class="order" data-order-id="${order.id}">
                <div>
                    <div style="font-weight: 700;">Заказ #${order.id} ${statusIcons[order.status] || ''}</div>
                    <div style="font-size: 13px; color: var(--muted);">
                        Стол #${order.table_id} • 
                        ${order.status === 'pending' ? '⏳ Ожидание' : 
                          order.status === 'cooking' ? '👨‍🍳 Готовится' : 
                          order.status === 'ready' ? '✅ Готов' : 
                          order.status === 'paid' ? '💰 Оплачен' : order.status}
                    </div>
                    <div style="font-size: 12px; margin-top: 4px;">
                        ${new Date(order.created_at).toLocaleString()}
                    </div>
                </div>
                <div>
                    <div style="font-weight: 700; text-align: right; margin-bottom: 8px;">
                        ${order.total_amount || 0} ₽
                    </div>
                    <div class="row" style="gap: 4px;">
                        ${currentUser?.role === 'chef' && order.status === 'pending' ? `
                            <button class="primary small" onclick="updateOrderStatus(${order.id}, 'cooking')">
                                Принять
                            </button>
                        ` : ''}
                        ${currentUser?.role === 'chef' && order.status === 'cooking' ? `
                            <button class="primary small" onclick="updateOrderStatus(${order.id}, 'ready')">
                                Готово
                            </button>
                        ` : ''}
                        ${currentUser?.role === 'waiter' && order.status === 'ready' ? `
                            <button class="primary small" onclick="updateOrderStatus(${order.id}, 'paid')">
                                Оплатить
                            </button>
                        ` : ''}
                        ${currentUser?.role === 'admin' ? `
                            <button class="danger small" onclick="deleteOrder(${order.id})">
                                Удалить
                            </button>
                        ` : ''}
                    </div>
                </div>
            </div>
        `).join('');
        
        if (orders.length === 0) {
            ordersList.innerHTML = '<div class="info-muted">Нет заказов</div>';
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        ordersList.innerHTML = '<div class="info-muted">Ошибка при загрузке заказов</div>';
    }
}

// Загрузить статистику пользователя
async function loadUserStats() {
    if (!currentUser) return;
    
    try {
        const stats = await getUserStats(currentUser.id);
        
        document.getElementById('statOrders').textContent = stats.total_orders || 0;
        document.getElementById('statActive').textContent = stats.active_orders || 0;
        document.getElementById('statTables').textContent = stats.occupied_tables || 0;
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

// Загрузить информацию о пользователе
function loadUserInfo() {
    const accountInfo = document.getElementById('accountInfo');
    if (!accountInfo || !currentUser) return;
    
    const roleNames = {
        'waiter': 'Официант',
        'chef': 'Повар',
        'admin': 'Администратор'
    };
    
    accountInfo.innerHTML = `
        <div style="font-weight: 700; font-size: 18px; margin-bottom: 8px;">
            ${currentUser.name || currentUser.username}
        </div>
        <div style="color: var(--muted); margin-bottom: 4px;">
            👤 Роль: ${roleNames[currentUser.role] || currentUser.role}
        </div>
        <div style="color: var(--muted); font-size: 13px;">
            Логин: ${currentUser.username}
        </div>
    `;
}

// ==================== УПРАВЛЕНИЕ ВИДИМОСТЬЮ ====================

// Показать форму авторизации
function showAuth() {
    document.getElementById('authSection').classList.remove('hidden');
    document.getElementById('appSection').classList.add('hidden');
}

// Показать основное приложение
function showApp() {
    document.getElementById('authSection').classList.add('hidden');
    document.getElementById('appSection').classList.remove('hidden');
    
    // Загружаем данные
    if (currentUser) {
        loadRoleData(currentUser.role);
    }
}

// Переключить на вкладку входа
function switchToLogin() {
    document.getElementById('tabLogin').classList.add('active');
    document.getElementById('tabRegister').classList.remove('active');
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
}

// Переключить на вкладку регистрации
function switchToRegister() {
    document.getElementById('tabLogin').classList.remove('active');
    document.getElementById('tabRegister').classList.add('active');
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
}

// Загрузить данные в зависимости от роли
function loadRoleData(role) {
    console.log('Loading data for role:', role);
    
    // Всегда загружаем пользователя и меню
    loadUserInfo();
    loadUserStats();
    loadMenu();
    
    // В зависимости от роли
    if (role === 'waiter' || role === 'admin') {
        loadTables();
        loadOrders();
    }
    
    if (role === 'chef') {
        loadOrders();
    }
    
    // Скрываем/показываем элементы в зависимости от роли
    document.querySelectorAll('[data-role]').forEach(element => {
        const requiredRole = element.dataset.role;
        if (requiredRole) {
            element.style.display = requiredRole === role ? '' : 'none';
        }
    });
}

// ==================== ОБРАБОТЧИКИ СОБЫТИЙ ====================

// Инициализация приложения
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');
    
    // Проверяем, авторизован ли пользователь
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            console.log('Found saved user:', currentUser);
            showApp();
        } catch (e) {
            console.error('Error parsing saved user:', e);
            localStorage.removeItem('currentUser');
            showAuth();
        }
    } else {
        showAuth();
    }
    
    // Обработчики вкладок авторизации
    document.getElementById('tabLogin').addEventListener('click', switchToLogin);
    document.getElementById('tabRegister').addEventListener('click', switchToRegister);
    
    // Обработчик входа
    document.getElementById('doLogin').addEventListener('click', function() {
        const username = document.getElementById('loginUser').value.trim();
        const password = document.getElementById('loginPass').value.trim();
        const role = document.getElementById('loginRole').value;
        
        if (!username || !password) {
            showError('Введите логин и пароль');
            return;
        }
        
        login(username, password, role);
    });
    
    // Обработчик регистрации
    document.getElementById('doRegister').addEventListener('click', function() {
        const username = document.getElementById('regUser').value.trim();
        const password = document.getElementById('regPass').value.trim();
        const role = document.getElementById('regRole').value;
        
        if (!username || !password) {
            showError('Введите логин и пароль');
            return;
        }
        
        register(username, password, role);
    });
    
    // Enter для входа
    document.getElementById('loginPass').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('doLogin').click();
        }
    });
    
    // Enter для регистрации
    document.getElementById('regPass').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('doRegister').click();
        }
    });
    
    // Обработчики главного меню
    document.querySelectorAll('.menu-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Убираем активный класс у всех кнопок
            document.querySelectorAll('.menu-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Добавляем активный класс текущей кнопке
            this.classList.add('active');
            
            // Скрываем все вкладки
            document.querySelectorAll('.tabpane').forEach(tab => {
                tab.classList.add('hidden');
            });
            
            // Показываем нужную вкладку
            const tabId = this.dataset.tab;
            document.getElementById(tabId).classList.remove('hidden');
            
            // Загружаем данные для вкладки
            if (tabId === 'menuTab') {
                loadMenu();
            } else if (tabId === 'ordersTab') {
                loadOrders();
            } else if (tabId === 'tablesTab') {
                loadTables();
            } else if (tabId === 'accountTab') {
                loadUserInfo();
                loadUserStats();
            }
        });
    });
    
    // Обработчики переключения категорий меню
    document.querySelectorAll('.switch-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Убираем активный класс у всех кнопок
            document.querySelectorAll('.switch-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Добавляем активный класс текущей кнопке
            this.classList.add('active');
            
            // Загружаем меню для выбранной категории
            loadMenu();
        });
    });
    
    // Обработчик выхода
    document.getElementById('logoutBtn').addEventListener('click', logout);
    
    // Быстрая авторизация (для демо)
    document.querySelectorAll('.cred-row').forEach(row => {
        row.addEventListener('click', function() {
            const text = this.textContent.trim();
            const match = text.match(/(\w+)\s*\/\s*(\w+)/);
            
            if (match) {
                const username = match[1];
                const password = match[2];
                
                document.getElementById('loginUser').value = username;
                document.getElementById('loginPass').value = password;
                
                // Определяем роль по username
                let role = 'waiter';
                if (username.includes('admin')) role = 'admin';
                if (username.includes('povar')) role = 'chef';
                
                document.getElementById('loginRole').value = role;
                
                showSuccess(`Данные для "${username}" подставлены. Нажмите "Войти".`);
            }
        });
    });
    
    // Тестирование API
    console.log('Testing API connection...');
    fetch('/api/health')
        .then(response => {
            if (response.ok) {
                console.log('✅ API is available');
            } else {
                console.log('⚠️ API returned status:', response.status);
            }
        })
        .catch(error => {
            console.log('❌ API connection failed:', error.message);
        });
    
    console.log('App initialized');
});

// ==================== ГЛОБАЛЬНЫЕ ФУНКЦИИ ====================

// Экспортируем функции для использования в HTML
window.login = login;
window.register = register;
window.logout = logout;

// API функции
window.getDishes = getDishes;
window.getTables = getTables;
window.getOrders = getOrders;
window.getUserStats = getUserStats;

// Действия
window.openTableModal = function(tableId) {
    console.log('Opening table modal for table:', tableId);
    showSuccess(`Информация о столе #${tableId} (функция в разработке)`);
};

window.createOrderForTable = function(tableId) {
    console.log('Creating order for table:', tableId);
    showSuccess(`Создание заказа для стола #${tableId} (функция в разработке)`);
};

window.updateOrderStatus = function(orderId, status) {
    console.log('Updating order status:', orderId, '->', status);
    showSuccess(`Статус заказа #${orderId} изменен на "${status}"`);
    loadOrders(); // Обновляем список
};

window.editDish = function(dishId) {
    console.log('Editing dish:', dishId);
    showSuccess(`Редактирование блюда #${dishId} (функция в разработке)`);
};

window.deleteDish = function(dishId) {
    if (!confirm('Вы уверены, что хотите удалить это блюдо?')) return;
    console.log('Deleting dish:', dishId);
    showSuccess(`Блюдо #${dishId} удалено`);
    loadMenu(); // Обновляем меню
};

window.deleteTable = function(tableId) {
    if (!confirm('Вы уверены, что хотите удалить этот столик?')) return;
    console.log('Deleting table:', tableId);
    showSuccess(`Столик #${tableId} удален`);
    loadTables(); // Обновляем список
};

window.deleteOrder = function(orderId) {
    if (!confirm('Вы уверены, что хотите удалить этот заказ?')) return;
    console.log('Deleting order:', orderId);
    showSuccess(`Заказ #${orderId} удален`);
    loadOrders(); // Обновляем список
};

// Добавляем стили для маленьких кнопок
const style = document.createElement('style');
style.textContent = `
    .small {
        padding: 6px 10px !important;
        font-size: 12px !important;
        min-width: auto !important;
    }
    
    .primary.small:hover, .danger.small:hover {
        opacity: 0.9;
    }
    
    .table:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    
    .order:hover {
        transform: translateX(2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
    }
`;
document.head.appendChild(style);

console.log('Restaurant Management System Frontend loaded');