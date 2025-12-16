// app.js - Restaurant Management System Frontend

const API_BASE_URL = '/api';
let currentUser = null;
let authToken = localStorage.getItem('authToken') || null;

// ==================== API UTILITY ====================

async function apiRequest(endpoint, options = {}) {
    try {
        const url = `${API_BASE_URL}${endpoint}`;
        const finalUrl = url.endsWith('/') ? url : `${url}/`;

        const headers = {
            'Content-Type': 'application/json',
            ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
            ...options.headers,
        };

        const config = { ...options, headers };
        const response = await fetch(finalUrl, config);

        if (response.status === 401) {
            logout();
            return null;
        }

        if (!response.ok) {
            const errorText = await response.text();
            console.error(`API Error ${response.status}:`, errorText);
            throw new Error(`HTTP ${response.status}`);
        }

        if (response.status === 204) return null;
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showError(error.message);
        throw error;
    }
}

function showError(message) {
    console.error('Error:', message);
    alert(`❌ Ошибка: ${message}`);
}

function showSuccess(message) {
    console.log('Success:', message);
    alert(`✅ ${message}`);
}

// ==================== AUTH ====================

async function login(username, password, role) {
    try {
        const testCredentials = {
            'ofikNum1': { id: 1, name: 'Официант 1', role: 'waiter', password: '123321' },
            'adminNum1': { id: 2, name: 'Админ', role: 'admin', password: '123321' },
            'povarNum1': { id: 3, name: 'Повар', role: 'chef', password: '123321' }
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

        showError('Неверные данные');
        return false;
    } catch (error) {
        console.error('Login error:', error);
        showError('Ошибка при входе');
        return false;
    }
}

async function register(username, password, role) {
    showSuccess('Регистрация временно недоступна');
    switchToLogin();
}

function logout() {
    currentUser = null;
    authToken = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('userRole');
    showAuth();
    showSuccess('Вы вышли из системы');
}

// ==================== DATA FETCH ====================

async function getDishes() {
    try {
        const response = await apiRequest('/dishes/');
        if (response && Array.isArray(response)) return response;
        if (response && response.items && Array.isArray(response.items)) return response.items;
        return getDemoDishes();
    } catch (error) {
        return getDemoDishes();
    }
}

function getDemoDishes() {
    return [
        { id: 1, name: 'Борщ', price: 350, category: 'Основное', cooking_time: 20 },
        { id: 2, name: 'Стейк', price: 1200, category: 'Основное', cooking_time: 25 },
        { id: 3, name: 'Салат', price: 450, category: 'Основное', cooking_time: 15 },
        { id: 4, name: 'Кофе', price: 150, category: 'Напитки', cooking_time: 5 },
        { id: 5, name: 'Чизкейк', price: 300, category: 'Десерт', cooking_time: 10 },
        { id: 6, name: 'Пицца', price: 650, category: 'Основное', cooking_time: 30 },
        { id: 7, name: 'Чай', price: 100, category: 'Напитки', cooking_time: 5 },
        { id: 8, name: 'Тирамису', price: 350, category: 'Десерт', cooking_time: 10 }
    ];
}

async function getTables() {
    try {
        const response = await apiRequest('/tables/');
        if (response && Array.isArray(response)) return response;
        return getDemoTables();
    } catch (error) {
        return getDemoTables();
    }
}

function getDemoTables() {
    return [
        { id: 1, table_number: 1, status: 'free', capacity: 4, location: 'У окна' },
        { id: 2, table_number: 2, status: 'occupied', capacity: 6, location: 'Центр' },
        { id: 3, table_number: 3, status: 'free', capacity: 2, location: 'Бар' },
        { id: 4, table_number: 4, status: 'reserved', capacity: 8, location: 'VIP' },
        { id: 5, table_number: 5, status: 'free', capacity: 4, location: 'Терраса' },
        { id: 6, table_number: 6, status: 'occupied', capacity: 4, location: 'У окна' },
        { id: 7, table_number: 7, status: 'free', capacity: 2, location: 'Бар' },
        { id: 8, table_number: 8, status: 'free', capacity: 6, location: 'Центр' }
    ];
}

async function getOrders() {
    try {
        const response = await apiRequest('/orders/');
        if (response && Array.isArray(response)) return response;
        return getDemoOrders();
    } catch (error) {
        return getDemoOrders();
    }
}

function getDemoOrders() {
    const now = new Date();
    return [
        { id: 1, table_id: 2, status: 'pending', total_amount: 1200, created_at: new Date(now - 2*60*60*1000).toISOString(), waiter_id: 1 },
        { id: 2, table_id: 4, status: 'cooking', total_amount: 800, created_at: new Date(now - 1*60*60*1000).toISOString(), waiter_id: 1 },
        { id: 3, table_id: 1, status: 'ready', total_amount: 450, created_at: now.toISOString(), waiter_id: 1 },
        { id: 4, table_id: 6, status: 'pending', total_amount: 1950, created_at: now.toISOString(), waiter_id: 1 }
    ];
}

async function getUserStats(userId) {
    try {
        const response = await apiRequest(`/users/${userId}/stats`);
        if (response) return response;
    } catch (error) {
        console.log('Stats API not available');
    }
    return { user_id: userId, total_orders: 15, active_orders: 3, occupied_tables: 2, total_revenue: 12500.50 };
}

// ==================== UI RENDERING ====================

async function loadMenu() {
    const menuContent = document.getElementById('menuContent');
    if (!menuContent) return;

    try {
        const dishes = await getDishes();
        menuContent.innerHTML = dishes.map(dish => `
            <div class="item" data-dish-id="${dish.id}">
                <div class="name">${dish.name || ''}</div>
                <div class="meta">${dish.price || 0} ₽</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading menu:', error);
        if (menuContent) menuContent.innerHTML = '<div>Error loading menu</div>';
    }
}

async function loadTables() {
    const tablesGrid = document.getElementById('tablesGrid');
    if (!tablesGrid) return;

    try {
        const tables = await getTables();
        tablesGrid.innerHTML = tables.map(table => `
            <div class="item" data-table-id="${table.id}">
                <div class="name">Стол #${table.table_number || table.id}</div>
                <div class="meta">${table.status === 'free' ? '🟢' : '🔴'} ${table.capacity} мест</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading tables:', error);
    }
}

async function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    if (!ordersList) return;

    try {
        let orders = await getOrders();
        if (currentUser && currentUser.role === 'chef') {
            orders = orders.filter(o => o.status === 'cooking' || o.status === 'pending');
        }
        
        ordersList.innerHTML = orders.map(order => `
            <div class="order" data-order-id="${order.id}">
                <div class="name">Заказ #${order.id} - Стол #${order.table_id}</div>
                <div class="meta">${order.total_amount || 0} ₽</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

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
        console.error('Error loading stats:', error);
    }
}

function loadUserInfo() {
    const accountInfo = document.getElementById('accountInfo');
    if (!accountInfo || !currentUser) return;

    const roleNames = { 'waiter': 'Официант', 'chef': 'Повар', 'admin': 'Админ' };
    accountInfo.innerHTML = `<h3>${currentUser.name || currentUser.username}</h3><p>${roleNames[currentUser.role] || currentUser.role}</p>`;
}

// ==================== VISIBILITY ====================

function showAuth() {
    const auth = document.getElementById('authSection');
    const app = document.getElementById('appSection');
    if (auth) auth.classList.remove('hidden');
    if (app) app.classList.add('hidden');
}

function showApp() {
    const auth = document.getElementById('authSection');
    const app = document.getElementById('appSection');
    if (auth) auth.classList.add('hidden');
    if (app) app.classList.remove('hidden');
}

function switchToLogin() {
    const tab = document.getElementById('tabLogin');
    const form = document.getElementById('loginForm');
    if (tab) tab.classList.add('active');
    if (form) form.classList.remove('hidden');
}

function switchToRegister() {
    const tab = document.getElementById('tabRegister');
    const form = document.getElementById('registerForm');
    if (tab) tab.classList.add('active');
    if (form) form.classList.remove('hidden');
}

function loadRoleData(role) {
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
}

// ==================== EVENT HANDLERS ====================

document.addEventListener('DOMContentLoaded', function() {
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            showApp();
        } catch (e) {
            localStorage.removeItem('currentUser');
            showAuth();
        }
    } else {
        showAuth();
    }

    const doLogin = document.getElementById('doLogin');
    const doRegister = document.getElementById('doRegister');
    const logoutBtn = document.getElementById('logoutBtn');
    const tabLogin = document.getElementById('tabLogin');
    const tabRegister = document.getElementById('tabRegister');
    const loginPass = document.getElementById('loginPass');

    if (tabLogin) tabLogin.addEventListener('click', switchToLogin);
    if (tabRegister) tabRegister.addEventListener('click', switchToRegister);

    if (doLogin) {
        doLogin.addEventListener('click', function() {
            const username = document.getElementById('loginUser')?.value?.trim() || '';
            const password = document.getElementById('loginPass')?.value?.trim() || '';
            if (!username || !password) {
                showError('Введите данные');
                return;
            }
            login(username, password);
        });
    }

    if (doRegister) {
        doRegister.addEventListener('click', function() {
            const username = document.getElementById('regUser')?.value?.trim() || '';
            const password = document.getElementById('regPass')?.value?.trim() || '';
            if (!username || !password) {
                showError('Введите данные');
                return;
            }
            register(username, password);
        });
    }

    if (loginPass) {
        loginPass.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && doLogin) doLogin.click();
        });
    }

    if (logoutBtn) logoutBtn.addEventListener('click', logout);

    document.querySelectorAll('.menu-btn').forEach(button => {
        button.addEventListener('click', function() {
            document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            document.querySelectorAll('.tabpane').forEach(tab => tab.classList.add('hidden'));
            const tabId = this.dataset.tab;
            const tab = document.getElementById(tabId);
            if (tab) tab.classList.remove('hidden');
            if (tabId === 'menuTab') loadMenu();
            else if (tabId === 'ordersTab') loadOrders();
            else if (tabId === 'tablesTab') loadTables();
        });
    });

    fetch('/api/health').then(r => console.log(r.ok ? '✅ API OK' : '⚠️ API issue')).catch(() => console.log('❌ API down'));
});

// ==================== EXPORTS ====================

window.login = login;
window.register = register;
window.logout = logout;
window.addEmployeeModal = function() { showSuccess('Функция в разработке'); };

console.log('🚚 App loaded');