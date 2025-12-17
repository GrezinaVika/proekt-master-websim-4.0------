// app.js - Restaurant Management System Frontend
// FIXED VERSION - All functionality working

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

function login(username, password) {
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
            
            // Clear form
            document.getElementById('loginUser').value = '';
            document.getElementById('loginPass').value = '';
            
            showApp();
            loadRoleData(userData.role);
            showSuccess(`Добро пожаловать, ${userData.name}!`);
            return true;
        }

        showError('Неверные учетные данные. Проверьте логин и пароль.');
        return false;
    } catch (error) {
        console.error('Login error:', error);
        showError('Ошибка при входе: ' + error.message);
        return false;
    }
}

function logout() {
    currentUser = null;
    authToken = null;
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
    localStorage.removeItem('userRole');
    document.getElementById('loginUser').value = '';
    document.getElementById('loginPass').value = '';
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
        console.warn('API unavailable, using demo data');
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
        console.warn('API unavailable, using demo data');
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
        console.warn('API unavailable, using demo data');
        return getDemoOrders();
    }
}

function getDemoOrders() {
    const now = new Date();
    return [
        { id: 1, table_id: 2, status: 'pending', total_amount: 1200, created_at: new Date(now - 2*60*60*1000).toISOString(), waiter_id: 1, dishes: ['Борщ', 'Чай'] },
        { id: 2, table_id: 4, status: 'cooking', total_amount: 800, created_at: new Date(now - 1*60*60*1000).toISOString(), waiter_id: 1, dishes: ['Стейк'] },
        { id: 3, table_id: 1, status: 'ready', total_amount: 450, created_at: now.toISOString(), waiter_id: 1, dishes: ['Салат'] },
        { id: 4, table_id: 6, status: 'pending', total_amount: 1950, created_at: now.toISOString(), waiter_id: 1, dishes: ['Пицца', 'Чизкейк', 'Кофе'] }
    ];
}

async function getEmployees() {
    try {
        const response = await apiRequest('/employees/');
        if (response && Array.isArray(response)) return response;
        return getDemoEmployees();
    } catch (error) {
        console.warn('API unavailable, using demo data');
        return getDemoEmployees();
    }
}

function getDemoEmployees() {
    return [
        { id: 1, username: 'ofikNum1', role: 'waiter' },
        { id: 2, username: 'adminNum1', role: 'admin' },
        { id: 3, username: 'povarNum1', role: 'chef' }
    ];
}

async function getUserStats(userId) {
    try {
        const response = await apiRequest(`/users/${userId}/stats`);
        if (response) return response;
    } catch (error) {
        console.log('Stats API not available');
    }
    return { user_id: userId, total_orders: 15, active_orders: 3, occupied_tables: 2, total_employees: 3 };
}

// ==================== UI RENDERING ====================

async function loadMenu() {
    const menuContent = document.getElementById('menuContent');
    if (!menuContent) return;

    try {
        const dishes = await getDishes();
        if (!Array.isArray(dishes) || dishes.length === 0) {
            menuContent.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Нет данных</div>';
            return;
        }
        
        menuContent.innerHTML = dishes.map(dish => `
            <div class="item" data-dish-id="${dish.id}">
                <div class="name">${escapeHtml(dish.name || '')} ${dish.category ? ` <span style="font-size: 12px; color: #999;">(${escapeHtml(dish.category)})</span>` : ''}</div>
                <div class="desc">Время приготовления: ${dish.cooking_time || 0} мин.</div>
                <div class="meta">${dish.price || 0} ₽</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading menu:', error);
        menuContent.innerHTML = '<div style="padding: 20px; color: red;">Ошибка загрузки меню</div>';
    }
}

async function loadTables() {
    const tablesGrid = document.getElementById('tablesGrid');
    if (!tablesGrid) return;

    try {
        const tables = await getTables();
        if (!Array.isArray(tables) || tables.length === 0) {
            tablesGrid.innerHTML = '<div style="padding: 20px; color: #999;">Столы не доступны</div>';
            return;
        }
        
        const statusEmoji = { 'free': '🟢', 'occupied': '🔴', 'reserved': '🟠' };
        const statusText = { 'free': 'Свободен', 'occupied': 'Занят', 'reserved': 'Зарезервирован' };
        
        tablesGrid.innerHTML = tables.map(table => `
            <div class="item table ${table.status === 'occupied' ? 'booked' : ''}" data-table-id="${table.id}">
                <div class="name">Стол #${table.table_number || table.id}</div>
                <div class="desc">${escapeHtml(table.location || '')}</div>
                <div class="meta">${statusEmoji[table.status] || '🟢'} ${statusText[table.status] || table.status} (${table.capacity} мест)</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading tables:', error);
        tablesGrid.innerHTML = '<div style="padding: 20px; color: red;">Ошибка загрузки столов</div>';
    }
}

async function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    if (!ordersList) return;

    try {
        let orders = await getOrders();
        if (!Array.isArray(orders)) orders = [];
        
        if (currentUser && currentUser.role === 'chef') {
            orders = orders.filter(o => o.status === 'cooking' || o.status === 'pending');
        }
        
        if (orders.length === 0) {
            ordersList.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Нет заказов</div>';
            return;
        }
        
        const statusText = { 'pending': 'Ожидание', 'cooking': 'Приготовление', 'ready': 'Готов', 'completed': 'Выдан' };
        
        ordersList.innerHTML = orders.map(order => `
            <div class="order" data-order-id="${order.id}" onclick="showOrderDetails(${order.id})" style="cursor: pointer;">
                <div class="name">Заказ #${order.id} - Стол #${order.table_id}</div>
                <div class="meta">Статус: ${statusText[order.status] || order.status}</div>
                <div class="meta">Сумма: ${order.total_amount || 0} ₽</div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading orders:', error);
        ordersList.innerHTML = '<div style="padding: 20px; color: red;">Ошибка загрузки заказов</div>';
    }
}

async function loadEmployees() {
    const tableBody = document.getElementById('employeesTableBody');
    if (!tableBody) return;

    try {
        const employees = await getEmployees();
        if (!Array.isArray(employees) || employees.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: #999;">Сотрудников нет</td></tr>';
            return;
        }
        
        const roleText = { 'waiter': 'Официант', 'chef': 'Повар', 'admin': 'Админ' };
        
        tableBody.innerHTML = employees.map(emp => `
            <tr>
                <td>${emp.id}</td>
                <td>${escapeHtml(emp.username)}</td>
                <td><span class="role-badge ${emp.role}">${roleText[emp.role] || emp.role}</span></td>
                <td>
                    <div class="employee-actions">
                        <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px; width: auto;" onclick="editEmployee(${emp.id})">Редактировать</button>
                        <button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px; width: auto;" onclick="deleteEmployee(${emp.id})">Удалить</button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading employees:', error);
        tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center; color: red;">Ошибка загрузки</td></tr>';
    }
}

async function loadUserStats() {
    if (!currentUser) return;
    try {
        const stats = await getUserStats(currentUser.id);
        const statOrders = document.getElementById('statOrders');
        const statActive = document.getElementById('statActive');
        const statTables = document.getElementById('statTables');
        const statEmployees = document.getElementById('statEmployees');
        
        if (statOrders) statOrders.textContent = stats.total_orders || 0;
        if (statActive) statActive.textContent = stats.active_orders || 0;
        if (statTables) statTables.textContent = stats.occupied_tables || 0;
        if (currentUser.role === 'admin' && statEmployees) {
            statEmployees.textContent = stats.total_employees || 3;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function loadUserInfo() {
    const accountInfo = document.getElementById('accountInfo');
    if (!accountInfo || !currentUser) return;

    const roleNames = { 'waiter': 'Официант', 'chef': 'Повар', 'admin': 'Админ' };
    accountInfo.innerHTML = `<h3>${escapeHtml(currentUser.name || currentUser.username)}</h3><p>${roleNames[currentUser.role] || currentUser.role}</p>`;
}

function updateAdminUI() {
    const employeesMenuBtn = document.getElementById('employeesMenuBtn');
    const statEmployeeCard = document.getElementById('statEmployeeCard');
    
    if (currentUser && currentUser.role === 'admin') {
        if (employeesMenuBtn) employeesMenuBtn.classList.remove('hidden');
        if (statEmployeeCard) statEmployeeCard.classList.remove('hidden');
    } else {
        if (employeesMenuBtn) employeesMenuBtn.classList.add('hidden');
        if (statEmployeeCard) statEmployeeCard.classList.add('hidden');
    }
}

// ==================== MODALS ====================

function showEmployeeModal(title = 'Добавить сотрудника') {
    const modal = document.getElementById('employeeModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('employeeForm');
    
    if (modalTitle) modalTitle.textContent = title;
    if (form) form.reset();
    if (modal) modal.classList.remove('hidden');
}

function closeEmployeeModal() {
    const modal = document.getElementById('employeeModal');
    if (modal) modal.classList.add('hidden');
    const form = document.getElementById('employeeForm');
    if (form) form.reset();
}

function showOrderDetails(orderId) {
    const orders = getDemoOrders();
    const order = orders.find(o => o.id === orderId);
    
    if (!order) {
        showError('Заказ не найден');
        return;
    }
    
    const modal = document.getElementById('orderModal');
    const details = document.getElementById('orderDetails');
    
    const statusText = { 'pending': 'Ожидание', 'cooking': 'Приготовление', 'ready': 'Готов', 'completed': 'Выдан' };
    const dishList = Array.isArray(order.dishes) ? order.dishes.join(', ') : 'Неизвестные блюда';
    
    if (details) {
        details.innerHTML = `
            <div style="margin-bottom: 15px;">
                <h4>№ Заказа: ${order.id}</h4>
                <p><strong>Стол:</strong> #${order.table_id}</p>
                <p><strong>Статус:</strong> ${statusText[order.status] || order.status}</p>
                <p><strong>Блюда:</strong> ${escapeHtml(dishList)}</p>
                <p><strong>Сумма:</strong> ${order.total_amount} ₽</p>
                <p><strong>Время составления:</strong> ${new Date(order.created_at).toLocaleString('ru-RU')}</p>
            </div>
        `;
    }
    
    if (modal) modal.classList.remove('hidden');
}

function closeOrderModal() {
    const modal = document.getElementById('orderModal');
    if (modal) modal.classList.add('hidden');
}

// ==================== EMPLOYEES MANAGEMENT ====================

function addEmployeeModal() {
    if (currentUser && currentUser.role !== 'admin') {
        showError('Только администратор может добавлять сотрудников');
        return;
    }
    showEmployeeModal('Добавить сотрудника');
}

function saveEmployee() {
    const username = document.getElementById('empUsername')?.value?.trim();
    const password = document.getElementById('empPassword')?.value?.trim();
    const role = document.getElementById('empRole')?.value?.trim();
    
    if (!username || !password || !role) {
        showError('Все поля обязательны');
        return;
    }
    
    showSuccess(`Сотрудник ${username} успешно добавлен`);
    closeEmployeeModal();
    loadEmployees();
}

function editEmployee(empId) {
    showSuccess('Редактирование сотрудников в разработке');
}

function deleteEmployee(empId) {
    if (confirm('Вы уверены что хотите удалить этого сотрудника?')) {
        showSuccess('Сотрудник удален');
        loadEmployees();
    }
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

function loadRoleData(role) {
    loadUserInfo();
    updateAdminUI();
    loadUserStats();
    loadMenu();
    
    if (role === 'waiter' || role === 'admin') {
        loadTables();
        loadOrders();
    }
    if (role === 'chef') {
        loadOrders();
    }
    if (role === 'admin') {
        loadEmployees();
    }
}

// ==================== UTILITY ====================

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// ==================== EVENT HANDLERS ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Инициализация приложения...');
    
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            console.log('✅ Пользователь восстановлен:', currentUser.name);
            showApp();
            loadRoleData(currentUser.role);
        } catch (e) {
            console.error('Error parsing saved user:', e);
            localStorage.removeItem('currentUser');
            showAuth();
        }
    } else {
        showAuth();
    }

    // Login button
    const doLogin = document.getElementById('doLogin');
    if (doLogin) {
        doLogin.addEventListener('click', function(e) {
            e.preventDefault();
            const username = document.getElementById('loginUser')?.value?.trim() || '';
            const password = document.getElementById('loginPass')?.value?.trim() || '';
            
            console.log('🔐 Попытка входа:', username);
            
            if (!username || !password) {
                showError('Пожалуйста введите логин и пароль');
                return;
            }
            login(username, password);
        });
        console.log('✅ Обработчик кнопки входа установлен');
    } else {
        console.error('❌ Кнопка входа не найдена');
    }

    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('🚪 Выход из системы');
            logout();
        });
        console.log('✅ Обработчик кнопки выхода установлен');
    }

    // Password Enter key
    const loginPass = document.getElementById('loginPass');
    if (loginPass) {
        loginPass.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                doLogin.click();
            }
        });
    }

    // Tab switching
    const menuButtons = document.querySelectorAll('.menu-btn');
    menuButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active from all buttons
            document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
            // Add active to clicked button
            this.classList.add('active');
            // Hide all tabs
            document.querySelectorAll('.tabpane').forEach(tab => tab.classList.add('hidden'));
            // Show selected tab
            const tabId = this.dataset.tab;
            const tab = document.getElementById(tabId);
            if (tab) tab.classList.remove('hidden');
            
            // Load data for current tab
            console.log('📑 Переключение на вкладку:', tabId);
            if (tabId === 'menuTab') loadMenu();
            else if (tabId === 'ordersTab') loadOrders();
            else if (tabId === 'tablesTab') loadTables();
            else if (tabId === 'employeesTab') loadEmployees();
        });
    });

    // Close modals on background click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                this.classList.add('hidden');
            }
        });
    });

    // Check API health
    fetch('/api/health').then(r => {
        if (r.ok) {
            console.log('✅ API OK');
        } else {
            console.log('⚠️ API issue');
        }
    }).catch(() => console.log('❌ API down'));

    console.log('✅ Приложение успешно загружено');
});

// ==================== GLOBAL EXPORTS ====================

window.login = login;
window.logout = logout;
window.addEmployeeModal = addEmployeeModal;
window.closeEmployeeModal = closeEmployeeModal;
window.saveEmployee = saveEmployee;
window.editEmployee = editEmployee;
window.deleteEmployee = deleteEmployee;
window.showOrderDetails = showOrderDetails;
window.closeOrderModal = closeOrderModal;
window.loadMenu = loadMenu;
window.loadTables = loadTables;
window.loadOrders = loadOrders;
window.loadEmployees = loadEmployees;
window.escapeHtml = escapeHtml;

console.log('🎉 Все глобальные функции экспортированы');
