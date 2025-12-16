/**
 * app.js - Restaurant Management System Frontend
 * Handles authentication, data loading, and UI management
 */

// ==================== CONSTANTS AND VARIABLES ====================

const API_BASE_URL = '/api';
let currentUser = null;
let authToken = localStorage.getItem('authToken') || null;
let isLoading = false;

// ==================== UTILITIES ====================

/**
 * Make API request with proper error handling
 * @param {string} endpoint - API endpoint
 * @param {Object} options - Fetch options
 * @returns {Promise<any>} API response data
 */
async function apiRequest(endpoint, options = {}) {
    if (isLoading && options.method !== 'GET') {
        console.warn('Another request is in progress');
        return null;
    }

    try {
        isLoading = true;
        const url = `${API_BASE_URL}${endpoint}`;
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

        const response = await fetch(finalUrl, config);

        if (response.status === 401) {
            logout();
            return null;
        }

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`API Error ${response.status}:`, errorText);

            try {
                const errorJson = JSON.parse(errorText);
                throw new Error(errorJson.detail || `HTTP ${response.status}`);
            } catch (parseError) {
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
        }

        if (response.status === 204) {
            return null;
        }

        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        showError(error.message || 'Unknown error');
        throw error;
    } finally {
        isLoading = false;
    }
}

/**
 * Show error message to user
 * @param {string} message - Error message
 */
function showError(message) {
    console.error('Error:', message);
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-notification';
    errorDiv.textContent = `❌ Ошибка: ${message}`;
    errorDiv.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: #ff6b6b;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        z-index: 10000;
        max-width: 300px;
    `;
    document.body.appendChild(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}

/**
 * Show success message to user
 * @param {string} message - Success message
 */
function showSuccess(message) {
    console.log('Success:', message);
    const successDiv = document.createElement('div');
    successDiv.className = 'success-notification';
    successDiv.textContent = `✅ ${message}`;
    successDiv.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        background: #51cf66;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        z-index: 10000;
        max-width: 300px;
    `;
    document.body.appendChild(successDiv);
    setTimeout(() => successDiv.remove(), 3000);
}

// ==================== AUTHORIZATION ====================

/**
 * User login
 * @param {string} username - Username
 * @param {string} password - Password
 * @param {string} role - User role
 * @returns {Promise<boolean>} Login success
 */
async function login(username, password, role) {
    try {
        console.log('Login attempt:', { username, role });

        const testCredentials = {
            'ofikNum1': { id: 1, name: 'Официант 1', role: 'waiter', password: '123321' },
            'adminNum1': { id: 2, name: 'Администратор', role: 'admin', password: '123321' },
            'povarNum1': { id: 3, name: 'Повар 1', role: 'chef', password: '123321' }
        };

        if (testCredentials[username] && testCredentials[username].password === password) {
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

        showError('Неверные учетные данные');
        return false;
    } catch (error) {
        console.error('Login error:', error);
        showError('Ошибка при входе');
        return false;
    }
}

/**
 * User registration (stub)
 * @param {string} username - Username
 * @param {string} password - Password
 * @param {string} role - User role
 */
async function register(username, password, role) {
    try {
        console.log('Register attempt:', { username, role });
        showSuccess('Регистрация временно недоступна. Используйте тестовые аккаунты.');
        switchToLogin();
    } catch (error) {
        console.error('Register error:', error);
        showError('Ошибка при регистрации');
    }
}

/**
 * User logout
 */
function logout() {
    currentUser = null;
    authToken = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('userRole');

    showAuth();
    showSuccess('Вы вышли из системы');
}

// ==================== DATA FETCHING ====================

/**
 * Get all dishes
 * @returns {Promise<Array>} Dishes array
 */
async function getDishes() {
    try {
        const response = await apiRequest('/dishes/');
        if (response && Array.isArray(response)) {
            return response;
        }
        if (response && response.items && Array.isArray(response.items)) {
            return response.items;
        }
        return getDemoDishes();
    } catch (error) {
        console.error('Error fetching dishes:', error);
        return getDemoDishes();
    }
}

/**
 * Demo dishes data
 * @returns {Array} Demo dishes
 */
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

/**
 * Get all tables
 * @returns {Promise<Array>} Tables array
 */
async function getTables() {
    try {
        const response = await apiRequest('/tables/');
        if (response && Array.isArray(response)) {
            return response;
        }
        return getDemoTables();
    } catch (error) {
        console.error('Error fetching tables:', error);
        return getDemoTables();
    }
}

/**
 * Demo tables data
 * @returns {Array} Demo tables
 */
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

/**
 * Get all orders
 * @returns {Promise<Array>} Orders array
 */
async function getOrders() {
    try {
        const response = await apiRequest('/orders/');
        if (response && Array.isArray(response)) {
            return response;
        }
        return getDemoOrders();
    } catch (error) {
        console.error('Error fetching orders:', error);
        return getDemoOrders();
    }
}

/**
 * Demo orders data
 * @returns {Array} Demo orders
 */
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
            items: [{ dish_id: 1, quantity: 2 }, { dish_id: 4, quantity: 2 }]
        },
        {
            id: 2,
            table_id: 4,
            status: 'cooking',
            total_amount: 800,
            created_at: oneHourAgo.toISOString(),
            waiter_id: 1,
            items: [{ dish_id: 3, quantity: 1 }, { dish_id: 5, quantity: 1 }]
        },
        {
            id: 3,
            table_id: 1,
            status: 'ready',
            total_amount: 450,
            created_at: now.toISOString(),
            waiter_id: 1,
            items: [{ dish_id: 7, quantity: 3 }]
        },
        {
            id: 4,
            table_id: 6,
            status: 'pending',
            total_amount: 1950,
            created_at: now.toISOString(),
            waiter_id: 1,
            items: [{ dish_id: 2, quantity: 1 }, { dish_id: 6, quantity: 1 }, { dish_id: 8, quantity: 2 }]
        }
    ];
}

/**
 * Get user statistics
 * @param {number} userId - User ID
 * @returns {Promise<Object>} User statistics
 */
async function getUserStats(userId) {
    try {
        const response = await apiRequest(`/users/${userId}/stats`);
        if (response) return response;
    } catch (error) {
        console.log('User stats API not available');
    }

    return {
        user_id: userId,
        total_orders: 15,
        active_orders: 3,
        occupied_tables: 2,
        total_revenue: 12500.50
    };
}

// ==================== UI RENDERING ====================

/**
 * Load and display menu
 */
async function loadMenu() {
    const menuContent = document.getElementById('menuContent');
    if (!menuContent) return;

    try {
        const dishes = await getDishes();
        const activeSection = document.querySelector('.switch-btn.active')?.dataset.section || 'main';

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

        if (activeDishes.length === 0) activeDishes = dishes;

        menuContent.innerHTML = activeDishes.map(dish => `
            <div class="item" data-dish-id="${dish.id}">
                <div class="name">${dish.name || ''}</div>
                <div class="meta">${dish.price || 0} ₽ • ${dish.cooking_time || 15} мин</div>
                ${dish.description ? `<div class="desc">${dish.description}</div>` : ''}
                ${currentUser?.role === 'admin' ? `
                    <div class="row">
                        <button class="primary small" onclick="editDish(${dish.id})">:✍️</button>
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
        menuContent.innerHTML = '<div class="info-muted">Ошибка при загружке меню</div>';
    }
}

/**
 * Load and display tables
 */
async function loadTables() {
    const tablesGrid = document.getElementById('tablesGrid');
    if (!tablesGrid) return;

    try {
        const tables = await getTables();

        tablesGrid.innerHTML = tables.map(table => `
            <div class="table ${table.status === 'occupied' || table.status === 'reserved' ? 'booked' : ''}" 
                 data-table-id="${table.id}">
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
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading tables:', error);
        tablesGrid.innerHTML = '<div class="info-muted">Ошибка при загружке столиков</div>';
    }
}

/**
 * Load and display orders
 */
async function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    if (!ordersList) return;

    try {
        let orders = await getOrders();

        if (currentUser?.role === 'chef') {
            orders = orders.filter(o => o.status === 'cooking' || o.status === 'pending');
        } else if (currentUser?.role === 'waiter' && currentUser.id) {
            orders = orders.filter(o => o.waiter_id === currentUser.id);
        }

        orders.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

        const statusIcons = { 'pending': '⏳', 'cooking': '👨‍🍳', 'ready': '✅', 'paid': '💰' };

        ordersList.innerHTML = orders.map(order => `
            <div class="order" data-order-id="${order.id}">
                <div>
                    <div style="font-weight: 700;">Заказ #${order.id} ${statusIcons[order.status] || ''}</div>
                    <div style="font-size: 13px; color: var(--muted);">
                        Стол #${order.table_id}
                    </div>
                </div>
                <div style="font-weight: 700; text-align: right;">${order.total_amount || 0} ₽</div>
            </div>
        `).join('');

        if (orders.length === 0) {
            ordersList.innerHTML = '<div class="info-muted">Нет заказов</div>';
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        ordersList.innerHTML = '<div class="info-muted">Ошибка при загружке заказов</div>';
    }
}

/**
 * Load user statistics
 */
async function loadUserStats() {
    if (!currentUser) return;

    try {
        const stats = await getUserStats(currentUser.id);
        const statOrders = document.getElementById('statOrders');
        const statActive = document.getElementById('statActive');
        const statTables = document.getElementById('statTables');

        if (statOrders) statOrders.textContent = stats.total_orders || 0;
        if (statActive) statActive.textContent = stats.active_orders || 0;
        if (statTables) statTables.textContent = stats.occupied_tables || 0;
    } catch (error) {
        console.error('Error loading user stats:', error);
    }
}

/**
 * Load and display user info
 */
function loadUserInfo() {
    const accountInfo = document.getElementById('accountInfo');
    if (!accountInfo || !currentUser) return;

    const roleNames = { 'waiter': 'Официант', 'chef': 'Повар', 'admin': 'Администратор' };

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

// ==================== VISIBILITY MANAGEMENT ====================

/**
 * Show authentication section
 */
function showAuth() {
    const authSection = document.getElementById('authSection');
    const appSection = document.getElementById('appSection');
    if (authSection) authSection.classList.remove('hidden');
    if (appSection) appSection.classList.add('hidden');
}

/**
 * Show application section
 */
function showApp() {
    const authSection = document.getElementById('authSection');
    const appSection = document.getElementById('appSection');
    if (authSection) authSection.classList.add('hidden');
    if (appSection) appSection.classList.remove('hidden');

    if (currentUser) {
        loadRoleData(currentUser.role);
    }
}

/**
 * Switch to login form
 */
function switchToLogin() {
    const tabLogin = document.getElementById('tabLogin');
    const tabRegister = document.getElementById('tabRegister');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (tabLogin) tabLogin.classList.add('active');
    if (tabRegister) tabRegister.classList.remove('active');
    if (loginForm) loginForm.classList.remove('hidden');
    if (registerForm) registerForm.classList.add('hidden');
}

/**
 * Switch to registration form
 */
function switchToRegister() {
    const tabLogin = document.getElementById('tabLogin');
    const tabRegister = document.getElementById('tabRegister');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (tabLogin) tabLogin.classList.remove('active');
    if (tabRegister) tabRegister.classList.add('active');
    if (loginForm) loginForm.classList.add('hidden');
    if (registerForm) registerForm.classList.remove('hidden');
}

/**
 * Load data based on user role
 * @param {string} role - User role
 */
function loadRoleData(role) {
    console.log('Loading data for role:', role);

    loadUserInfo();
    loadUserStats();
    loadMenu();

    if (role === 'waiter' || role === 'admin') {
        loadTables();
        loadOrders();
    }

    if (role === 'chef') {
        loadOrders();
    }

    document.querySelectorAll('[data-role]').forEach(element => {
        const requiredRole = element.dataset.role;
        if (requiredRole) {
            element.style.display = requiredRole === role ? '' : 'none';
        }
    });
}

// ==================== EVENT HANDLERS ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing app...');

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

    // Setup event listeners
    const tabLogin = document.getElementById('tabLogin');
    const tabRegister = document.getElementById('tabRegister');
    const doLogin = document.getElementById('doLogin');
    const doRegister = document.getElementById('doRegister');
    const loginPass = document.getElementById('loginPass');
    const regPass = document.getElementById('regPass');
    const logoutBtn = document.getElementById('logoutBtn');

    if (tabLogin) tabLogin.addEventListener('click', switchToLogin);
    if (tabRegister) tabRegister.addEventListener('click', switchToRegister);

    if (doLogin) {
        doLogin.addEventListener('click', function() {
            const username = document.getElementById('loginUser')?.value?.trim() || '';
            const password = document.getElementById('loginPass')?.value?.trim() || '';
            const role = document.getElementById('loginRole')?.value || 'waiter';

            if (!username || !password) {
                showError('Введите логин и пароль');
                return;
            }

            login(username, password, role);
        });
    }

    if (doRegister) {
        doRegister.addEventListener('click', function() {
            const username = document.getElementById('regUser')?.value?.trim() || '';
            const password = document.getElementById('regPass')?.value?.trim() || '';
            const role = document.getElementById('regRole')?.value || 'waiter';

            if (!username || !password) {
                showError('Введите логин и пароль');
                return;
            }

            register(username, password, role);
        });
    }

    if (loginPass) {
        loginPass.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') doLogin?.click();
        });
    }

    if (regPass) {
        regPass.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') doRegister?.click();
        });
    }

    if (logoutBtn) logoutBtn.addEventListener('click', logout);

    // Menu buttons
    document.querySelectorAll('.menu-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            document.querySelectorAll('.tabpane').forEach(tab => tab.classList.add('hidden'));
            const tabId = this.dataset.tab;
            const tabElement = document.getElementById(tabId);
            if (tabElement) tabElement.classList.remove('hidden');

            if (tabId === 'menuTab') loadMenu();
            else if (tabId === 'ordersTab') loadOrders();
            else if (tabId === 'tablesTab') loadTables();
            else if (tabId === 'accountTab') {
                loadUserInfo();
                loadUserStats();
            }
        });
    });

    // Category switches
    document.querySelectorAll('.switch-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.switch-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            loadMenu();
        });
    });

    // API health check
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

// ==================== GLOBAL EXPORTS ====================

window.login = login;
window.register = register;
window.logout = logout;
window.getDishes = getDishes;
window.getTables = getTables;
window.getOrders = getOrders;
window.getUserStats = getUserStats;

// Stub functions
window.openTableModal = (tableId) => console.log('Opening table modal:', tableId);
window.createOrderForTable = (tableId) => showSuccess(`Создание заказа для стола #${tableId}`);
window.updateOrderStatus = (orderId, status) => showSuccess(`Статус заказа #${orderId} изменен`);
window.editDish = (dishId) => showSuccess(`Редактирование блюда #${dishId}`);
window.deleteDish = (dishId) => confirm('Удалить?') && showSuccess(`Блюдо #${dishId} удалено`);
window.deleteTable = (tableId) => confirm('Удалить?') && showSuccess(`Стол #${tableId} удален`);
window.deleteOrder = (orderId) => confirm('Удалить?') && showSuccess(`Заказ #${orderId} удален`);

console.log('🚚 Restaurant Management System Frontend loaded');
