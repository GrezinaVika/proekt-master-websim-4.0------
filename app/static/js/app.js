// app.js - Restaurant Management System Frontend
// FIXED VERSION WITH ALL WORKING FEATURES

const API_BASE_URL = '/api';
let currentUser = null;
let authToken = localStorage.getItem('authToken') || null;
let editingEmployeeId = null;
let editingDishId = null;

// ==================== API UTILITY ====================

async function apiRequest(endpoint, method = 'GET', data = null) {
    try {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...(authToken && { 'Authorization': `Bearer ${authToken}` }),
        };
        
        const config = {
            method: method,
            headers: headers,
        };
        
        if (data && (method === 'POST' || method === 'PUT')) {
            config.body = JSON.stringify(data);
        }
        
        console.log(`[${method}] ${url}`, data);
        const response = await fetch(url, config);
        
        console.log(`Response ${response.status}`);
        
        if (response.status === 401) {
            logout();
            return null;
        }
        
        if (response.status === 204) return { success: true };
        
        const text = await response.text();
        if (!text) return { success: response.ok };
        
        try {
            const json = JSON.parse(text);
            if (!response.ok) {
                console.error(`API Error ${response.status}:`, json);
                throw new Error(json.detail || json.message || `API Error ${response.status}`);
            }
            return json;
        } catch (e) {
            if (!response.ok) throw new Error(`API Error ${response.status}`);
            return text;
        }
    } catch (error) {
        console.error('API Error:', error);
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

async function login(username, password) {
    try {
        const response = await apiRequest('/auth/login', 'POST', { username, password });
        
        if (!response || !response.user) {
            showError('Неверные учетные данные');
            return false;
        }
        
        currentUser = response.user;
        authToken = response.access_token;
        
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
        localStorage.setItem('authToken', authToken);
        localStorage.setItem('userRole', currentUser.role);
        
        document.getElementById('loginUser').value = '';
        document.getElementById('loginPass').value = '';
        
        showApp();
        loadRoleData(currentUser.role);
        showSuccess(`Добро пожаловать, ${currentUser.name}!`);
        return true;
    } catch (error) {
        showError('Ошибка входа: ' + error.message);
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
        return [];
    } catch (error) {
        console.error('Get dishes error:', error);
        return [];
    }
}

async function getTables() {
    try {
        const response = await apiRequest('/tables/');
        if (response && Array.isArray(response)) return response;
        return [];
    } catch (error) {
        console.error('Get tables error:', error);
        return [];
    }
}

async function getOrders() {
    try {
        const response = await apiRequest('/orders/');
        if (response && Array.isArray(response)) return response;
        return [];
    } catch (error) {
        console.error('Get orders error:', error);
        return [];
    }
}

async function getEmployees() {
    try {
        const response = await apiRequest('/employees/');
        if (response && Array.isArray(response)) return response;
        return [];
    } catch (error) {
        console.error('Get employees error:', error);
        return [];
    }
}

async function getUserStats(userId) {
    try {
        const response = await apiRequest(`/users/${userId}/stats`);
        if (response) return response;
    } catch (error) {
        console.log('Stats API error:', error);
    }
    return { user_id: userId, total_orders: 0, active_orders: 0, occupied_tables: 0, total_employees: 0 };
}

// ==================== UI RENDERING ====================

async function loadMenu() {
    const menuContent = document.getElementById('menuContent');
    if (!menuContent) return;
    
    try {
        menuContent.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Загрузка...</div>';
        const dishes = await getDishes();
        
        if (!Array.isArray(dishes) || dishes.length === 0) {
            menuContent.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Нет блюд</div>';
            return;
        }
        
        const addDishBtn = currentUser && currentUser.role === 'admin' ? 
            '<button class="btn btn-primary" style="width: 100%; margin-bottom: 20px;" onclick="showAddDishModal()">➕ Добавить блюдо</button>' : '';
        
        menuContent.innerHTML = addDishBtn + dishes.map(dish => `
            <div class="item" data-dish-id="${dish.id}">
                <div class="name">${escapeHtml(dish.name || '')} <span style="font-size: 12px; color: #999;">(${escapeHtml(dish.category || '')})</span></div>
                <div class="desc">⏱ ${dish.cooking_time || 0} мин.</div>
                <div class="meta">${dish.price || 0} ₽</div>
                ${currentUser && currentUser.role === 'admin' ? `
                    <div style="margin-top: 8px; display: flex; gap: 6px;">
                        <button class="btn btn-secondary" style="padding: 4px 8px; font-size: 11px; flex: 1; width: auto;" onclick="showEditDishModal(${dish.id}, '${escapeHtml(dish.name)}', ${dish.price}, '${escapeHtml(dish.category)}', ${dish.cooking_time})">Edit</button>
                        <button class="btn btn-danger" style="padding: 4px 8px; font-size: 11px; flex: 1; width: auto;" onclick="deleteDish(${dish.id})">Del</button>
                    </div>
                ` : ''}
            </div>
        `).join('');
    } catch (error) {
        menuContent.innerHTML = '<div style="padding: 20px; text-align: center; color: red;">Ошибка загрузки</div>';
        console.error('Error loading menu:', error);
    }
}

async function loadTables() {
    const tablesGrid = document.getElementById('tablesGrid');
    if (!tablesGrid) return;
    
    try {
        tablesGrid.innerHTML = '<div style="padding: 20px; color: #999;">Загрузка столов...</div>';
        const tables = await getTables();
        
        if (!Array.isArray(tables) || tables.length === 0) {
            tablesGrid.innerHTML = '<div style="padding: 20px; color: #999;">Столы не найдены</div>';
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
        tablesGrid.innerHTML = '<div style="padding: 20px; text-align: center; color: red;">Ошибка загрузки столов</div>';
        console.error('Error loading tables:', error);
    }
}

async function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    if (!ordersList) return;
    
    try {
        ordersList.innerHTML = '<div style="padding: 20px; color: #999;">Загрузка заказов...</div>';
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
                <div class="meta">Статус: <span style="color: #667eea; font-weight: bold;">${statusText[order.status] || order.status}</span></div>
                <div class="meta">Сумма: <span style="color: #27ae60; font-weight: bold;">${order.total_amount || 0} ₽</span></div>
            </div>
        `).join('');
    } catch (error) {
        ordersList.innerHTML = '<div style="padding: 20px; text-align: center; color: red;">Ошибка загрузки заказов</div>';
        console.error('Error loading orders:', error);
    }
}

async function loadEmployees() {
    const tableBody = document.getElementById('employeesTableBody');
    if (!tableBody) return;
    
    try {
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">Загрузка...</td></tr>';
        const employees = await getEmployees();
        
        if (!Array.isArray(employees) || employees.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">Сотрудников нет</td></tr>';
            return;
        }
        
        const roleText = { 'waiter': '🙋 Официант', 'chef': '👩\u200d🍳 Повар', 'admin': '👨\u200d💼 Админ' };
        
        tableBody.innerHTML = employees.map(emp => `
            <tr>
                <td>#${emp.id}</td>
                <td><strong>${escapeHtml(emp.username)}</strong></td>
                <td>${escapeHtml(emp.name || '')}</td>
                <td><span class="role-badge ${emp.role}">${roleText[emp.role] || emp.role}</span></td>
                <td>
                    <div class="employee-actions">
                        <button class="btn btn-secondary" style="padding: 6px 10px; font-size: 12px; width: auto;" onclick="showEditEmployeeModal(${emp.id}, '${escapeHtml(emp.username)}', '${escapeHtml(emp.name)}', '${emp.role}')">Edit</button>
                        <button class="btn btn-danger" style="padding: 6px 10px; font-size: 12px; width: auto;" onclick="deleteEmployee(${emp.id})">Del</button>
                    </div>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: red;">Ошибка загрузки</td></tr>';
        console.error('Error loading employees:', error);
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
    
    const roleNames = { 'waiter': '🙋 Официант', 'chef': '👩\u200d🍳 Повар', 'admin': '👨\u200d💼 Админ' };
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

// ==================== DISH MANAGEMENT ====================

function showAddDishModal() {
    editingDishId = null;
    const modal = document.getElementById('employeeModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('employeeForm');
    
    if (modalTitle) modalTitle.textContent = 'Добавить блюдо';
    if (form) form.reset();
    if (modal) modal.classList.remove('hidden');
}

function showEditDishModal(dishId, name, price, category, cookingTime) {
    editingDishId = dishId;
    const modal = document.getElementById('employeeModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('employeeForm');
    const usernameField = document.getElementById('empUsername');
    const nameField = document.getElementById('empName');
    const passwordField = document.getElementById('empPassword');
    const roleField = document.getElementById('empRole');
    
    if (modalTitle) modalTitle.textContent = 'Обновить блюдо';
    if (usernameField) { usernameField.placeholder = 'Наименование'; usernameField.value = name; }
    if (nameField) { nameField.placeholder = 'Цена'; nameField.value = price; }
    if (passwordField) { passwordField.placeholder = 'Категория'; passwordField.value = category; }
    if (roleField) { roleField.style.display = 'block'; roleField.innerHTML = `<option value="${cookingTime}">Время: ${cookingTime} мин</option>`; }
    if (modal) modal.classList.remove('hidden');
}

async function saveDish() {
    const name = document.getElementById('empUsername')?.value?.trim();
    const price = parseFloat(document.getElementById('empName')?.value || 0);
    const category = document.getElementById('empPassword')?.value?.trim();
    const cookingTime = parseInt(document.getElementById('empRole')?.value || 15);
    
    if (!name || !price || !category) {
        showError('Заполните все поля');
        return;
    }
    
    try {
        if (editingDishId) {
            await apiRequest(`/dishes/${editingDishId}`, 'PUT', {
                name: name,
                price: price,
                category: category,
                cooking_time: cookingTime
            });
            showSuccess('Блюдо обновлено');
        } else {
            await apiRequest('/dishes/', 'POST', {
                name: name,
                price: price,
                category: category,
                cooking_time: cookingTime
            });
            showSuccess('Блюдо добавлено');
        }
        closeEmployeeModal();
        loadMenu();
    } catch (error) {
        showError('Ошибка: ' + error.message);
    }
}

async function deleteDish(dishId) {
    if (confirm('Удалить это блюдо?')) {
        try {
            await apiRequest(`/dishes/${dishId}`, 'DELETE');
            showSuccess('Блюдо удалено');
            loadMenu();
        } catch (error) {
            showError('Ошибка удаления: ' + error.message);
        }
    }
}

// ==================== EMPLOYEE MANAGEMENT ====================

function addEmployeeModal() {
    if (currentUser && currentUser.role !== 'admin') {
        showError('Только администратор может добавлять');
        return;
    }
    editingEmployeeId = null;
    const modal = document.getElementById('employeeModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('employeeForm');
    const usernameField = document.getElementById('empUsername');
    const nameField = document.getElementById('empName');
    const passwordField = document.getElementById('empPassword');
    
    if (modalTitle) modalTitle.textContent = 'Добавить сотрудника';
    if (form) form.reset();
    if (usernameField) { usernameField.disabled = false; usernameField.placeholder = 'Логин'; }
    if (nameField) nameField.placeholder = 'Имя';
    if (passwordField) { passwordField.placeholder = 'Пароль'; passwordField.required = true; }
    if (modal) modal.classList.remove('hidden');
}

function showEditEmployeeModal(empId, username, name, role) {
    editingEmployeeId = empId;
    const modal = document.getElementById('employeeModal');
    const modalTitle = document.getElementById('modalTitle');
    const form = document.getElementById('employeeForm');
    const usernameField = document.getElementById('empUsername');
    const nameField = document.getElementById('empName');
    const roleField = document.getElementById('empRole');
    const passwordField = document.getElementById('empPassword');
    
    if (modalTitle) modalTitle.textContent = 'Обновить сотрудника';
    if (usernameField) { usernameField.value = username; usernameField.disabled = true; }
    if (nameField) nameField.value = name;
    if (roleField) roleField.value = role;
    if (passwordField) { passwordField.value = ''; passwordField.placeholder = 'Новый пароль (не обязательно)'; passwordField.required = false; }
    if (modal) modal.classList.remove('hidden');
}

function closeEmployeeModal() {
    const modal = document.getElementById('employeeModal');
    if (modal) modal.classList.add('hidden');
    const form = document.getElementById('employeeForm');
    if (form) form.reset();
    editingEmployeeId = null;
    editingDishId = null;
}

async function saveEmployee() {
    const username = document.getElementById('empUsername')?.value?.trim();
    const name = document.getElementById('empName')?.value?.trim();
    const password = document.getElementById('empPassword')?.value?.trim();
    const role = document.getElementById('empRole')?.value?.trim();
    
    if (!username || !role) {
        showError('Укажите логин и роль');
        return;
    }
    
    if (!editingEmployeeId && !password) {
        showError('Укажите пароль');
        return;
    }
    
    if (!editingEmployeeId && !name) {
        showError('Укажите имя');
        return;
    }
    
    try {
        if (editingEmployeeId) {
            const data = { name: name, role: role };
            if (password) data.password = password;
            await apiRequest(`/employees/${editingEmployeeId}`, 'PUT', data);
            showSuccess('Сотрудник обновлен');
        } else {
            await apiRequest('/employees/', 'POST', {
                username: username,
                name: name,
                password: password,
                role: role
            });
            showSuccess('Сотрудник добавлен');
        }
        closeEmployeeModal();
        loadEmployees();
    } catch (error) {
        showError('Ошибка: ' + error.message);
    }
}

async function deleteEmployee(empId) {
    if (confirm('Удалить сотрудника?')) {
        try {
            await apiRequest(`/employees/${empId}`, 'DELETE');
            showSuccess('Сотрудник удален');
            loadEmployees();
        } catch (error) {
            showError('Ошибка удаления: ' + error.message);
        }
    }
}

// ==================== ORDER MODALS ====================

function showOrderDetails(orderId) {
    // TODO: Fetch order details from API
    getOrders().then(orders => {
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
                <div style="margin-bottom: 20px;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
                            <p style="margin: 0 0 8px 0; font-size: 12px; color: #999; text-transform: uppercase; font-weight: bold;">Номер заказа</p>
                            <h3 style="margin: 0; font-size: 24px; color: #667eea;">#${order.id}</h3>
                        </div>
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
                            <p style="margin: 0 0 8px 0; font-size: 12px; color: #999; text-transform: uppercase; font-weight: bold;">Стол</p>
                            <h3 style="margin: 0; font-size: 24px; color: #667eea;">#${order.table_id}</h3>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px; padding: 15px; background: #e8f4f8; border-radius: 8px; border-left: 4px solid #0288d1;">
                        <p style="margin: 0 0 8px 0; font-size: 12px; color: #0288d1; text-transform: uppercase; font-weight: bold;">Статус</p>
                        <p style="margin: 0; font-size: 16px; color: #0288d1; font-weight: bold;">${statusText[order.status] || order.status}</p>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <p style="margin: 0 0 10px 0; font-size: 12px; color: #999; text-transform: uppercase; font-weight: bold;">Блюда</p>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                            ${dishList.split(', ').map(dish => `
                                <span style="background: #f0f0f0; padding: 8px 12px; border-radius: 6px; font-size: 13px; color: #333;">✓ ${escapeHtml(dish)}</span>
                            `).join('')}
                        </div>
                    </div>
                    
                    <div style="padding: 20px; background: #fff3e0; border-radius: 8px; border: 2px solid #f39c12;">
                        <p style="margin: 0 0 8px 0; font-size: 12px; color: #f39c12; text-transform: uppercase; font-weight: bold;">Общая стоимость</p>
                        <h2 style="margin: 0; font-size: 32px; color: #f39c12;">${order.total_amount || 0} ₽</h2>
                    </div>
                    
                    <div style="margin-top: 15px; color: #999; font-size: 12px;">
                        <p style="margin: 0;">⏰ Время:</p>
                        <p style="margin: 4px 0 0 0;">${new Date(order.created_at).toLocaleString('ru-RU')}</p>
                    </div>
                </div>
            `;
        }
        
        if (modal) modal.classList.remove('hidden');
    });
}

function closeOrderModal() {
    const modal = document.getElementById('orderModal');
    if (modal) modal.classList.add('hidden');
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
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// ==================== EVENT HANDLERS ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Приложение загружается...');
    
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            authToken = localStorage.getItem('authToken');
            showApp();
            loadRoleData(currentUser.role);
        } catch (e) {
            localStorage.removeItem('currentUser');
            localStorage.removeItem('authToken');
            showAuth();
        }
    } else {
        showAuth();
    }
    
    const doLogin = document.getElementById('doLogin');
    if (doLogin) {
        doLogin.addEventListener('click', function(e) {
            e.preventDefault();
            const username = document.getElementById('loginUser')?.value?.trim() || '';
            const password = document.getElementById('loginPass')?.value?.trim() || '';
            
            if (!username || !password) {
                showError('Пожалуйста, введите логин и пароль');
                return;
            }
            login(username, password);
        });
    }
    
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
    
    const loginPass = document.getElementById('loginPass');
    if (loginPass) {
        loginPass.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                doLogin.click();
            }
        });
    }
    
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
            else if (tabId === 'employeesTab') loadEmployees();
        });
    });
    
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) this.classList.add('hidden');
        });
    });
    
    fetch('/api/health').then(r => {
        if (r.ok) console.log('✅ API OK');
    }).catch(() => console.log('❌ API не доступна'));
    
    console.log('✅ Приложение готово');
});

// ==================== GLOBAL EXPORTS ====================

window.login = login;
window.logout = logout;
window.addEmployeeModal = addEmployeeModal;
window.showEditEmployeeModal = showEditEmployeeModal;
window.closeEmployeeModal = closeEmployeeModal;
window.saveEmployee = saveEmployee;
window.deleteEmployee = deleteEmployee;
window.showOrderDetails = showOrderDetails;
window.closeOrderModal = closeOrderModal;
window.showAddDishModal = showAddDishModal;
window.showEditDishModal = showEditDishModal;
window.saveDish = saveDish;
window.deleteDish = deleteDish;
window.loadMenu = loadMenu;
window.loadTables = loadTables;
window.loadOrders = loadOrders;
window.loadEmployees = loadEmployees;
window.escapeHtml = escapeHtml;
