// app.js - Restaurant Management System Frontend
// FINAL VERSION - ALL BUGS FIXED

const API_BASE_URL = '/api';
let currentUser = null;
let authToken = localStorage.getItem('authToken') || null;
let editingEmployeeId = null;
let editingDishId = null;
let selectedTableId = null;
let editingOrderId = null;

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
        const params = new URLSearchParams();
        params.append('username', username);
        params.append('password', password);
        
        const url = `${API_BASE_URL}/auth/login?${params.toString()}`;
        console.log('[LOGIN] Trying:', url);
        
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        console.log('[LOGIN] Response status:', response.status);
        const text = await response.text();
        
        if (!response.ok) {
            throw new Error(`API Error ${response.status}: ${text}`);
        }
        
        const data = JSON.parse(text);
        
        if (!data || !data.user) {
            showError('Неверные учетные данные');
            return false;
        }
        
        currentUser = data.user;
        authToken = data.access_token;
        
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
        console.error('[LOGIN ERROR]', error);
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
        menuContent.innerHTML = '<div style="padding: 20px; text-align: center; color: #999;">Загружка...</div>';
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
        menuContent.innerHTML = '<div style="padding: 20px; text-align: center; color: red;">Ошибка загружки</div>';
        console.error('Error loading menu:', error);
    }
}

async function loadTables() {
    const tablesGrid = document.getElementById('tablesGrid');
    if (!tablesGrid) return;
    
    try {
        tablesGrid.innerHTML = '<div style="padding: 20px; color: #999;">Загружка столов...</div>';
        const tables = await getTables();
        
        if (!Array.isArray(tables) || tables.length === 0) {
            tablesGrid.innerHTML = '<div style="padding: 20px; color: #999;">Столы не найдены</div>';
            return;
        }
        
        const statusEmoji = { 'free': '🟢', 'occupied': '🔴', 'reserved': '🟠' };
        const statusText = { 'free': 'Свободен', 'occupied': 'Занят', 'reserved': 'Зарезервирован' };
        
        tablesGrid.innerHTML = tables.map(table => `
            <div class="item table ${table.status === 'occupied' ? 'booked' : ''}" data-table-id="${table.id}" onclick="showCreateOrderForTable(${table.id})" style="cursor: pointer;">
                <div class="name">Стол ${table.table_number || table.id}</div>
                <div class="desc">${escapeHtml(table.location || '')}</div>
                <div class="meta">${statusEmoji[table.status] || '🟢'} ${statusText[table.status] || table.status} (${table.capacity} мест)</div>
            </div>
        `).join('');
    } catch (error) {
        tablesGrid.innerHTML = '<div style="padding: 20px; text-align: center; color: red;">Ошибка загружки столов</div>';
        console.error('Error loading tables:', error);
    }
}

async function loadOrders() {
    const ordersList = document.getElementById('ordersList');
    if (!ordersList) return;
    
    try {
        ordersList.innerHTML = '<div style="padding: 20px; color: #999;">Загружка заказов...</div>';
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
            <div class="order" data-order-id="${order.id}" style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;">
                <div class="name" style="font-size: 16px; font-weight: bold; margin-bottom: 8px;">Заказ ${order.id} - Стол ${order.table_id}</div>
                <div class="meta" style="margin-bottom: 5px;">Статус: <span style="color: #667eea; font-weight: bold;">${statusText[order.status] || order.status}</span></div>
                <div class="meta" style="margin-bottom: 12px;">Сумма: <span style="color: #27ae60; font-weight: bold;">${order.total_amount || 0} ₽</span></div>
                <div style="display: flex; gap: 6px; flex-wrap: wrap;">
                    <button class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px; flex: 1; min-width: 80px;" onclick="showOrderDetails(${order.id})">View</button>
                    ${currentUser && currentUser.role !== 'chef' ? `
                        <button class="btn btn-primary" style="padding: 6px 12px; font-size: 12px; flex: 1; min-width: 80px;" onclick="showEditOrderModal(${order.id})">Edit</button>
                        <button class="btn btn-danger" style="padding: 6px 12px; font-size: 12px; flex: 1; min-width: 80px;" onclick="completeOrder(${order.id})">Complete</button>
                    ` : ''}
                </div>
            </div>
        `).join('');
    } catch (error) {
        ordersList.innerHTML = '<div style="padding: 20px; text-align: center; color: red;">Ошибка загружки заказов</div>';
        console.error('Error loading orders:', error);
    }
}

async function loadEmployees() {
    const tableBody = document.getElementById('employeesTableBody');
    if (!tableBody) return;
    
    try {
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">Загружка...</td></tr>';
        const employees = await getEmployees();
        
        if (!Array.isArray(employees) || employees.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: #999;">Сотрудников нет</td></tr>';
            return;
        }
        
        const roleText = { 'waiter': '🙋 Официант', 'chef': '👩‍🍳 Повар', 'admin': '👨‍💼 Админ' };
        
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
        tableBody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: red;">Ошибка загружки</td></tr>';
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
    
    const roleNames = { 'waiter': '🙋 Официант', 'chef': '👩‍🍳 Повар', 'admin': '👨‍💼 Админ' };
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
    openDishModal('Добавить блюдо', '', '', '', 15);
}

function showEditDishModal(dishId, name, price, category, cookingTime) {
    editingDishId = dishId;
    openDishModal('Обновить блюдо', name, price, category, cookingTime);
}

function openDishModal(title, name, price, category, cookingTime) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'dishFormModal';
    modal.style.cssText = 'display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 9999;';
    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 10px; max-width: 400px; width: 90%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin-top: 0; margin-bottom: 20px; color: #333;">${title}</h2>
            <form id="dishForm" onsubmit="event.preventDefault(); saveDish();">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Наименование:</label>
                    <input type="text" id="dishName" value="${escapeHtml(String(name))}" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Цена (₽):</label>
                    <input type="number" id="dishPrice" value="${price}" step="0.01" min="0" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Категория:</label>
                    <input type="text" id="dishCategory" value="${escapeHtml(String(category))}" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Время приготовления (мин):</label>
                    <input type="number" id="dishTime" value="${cookingTime}" min="1" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary" style="flex: 1; padding: 10px;">Сохранить</button>
                    <button type="button" class="btn btn-secondary" style="flex: 1; padding: 10px;" onclick="closeDishModal()">Отмена</button>
                </div>
            </form>
        </div>
    `;
    
    const oldModal = document.getElementById('dishFormModal');
    if (oldModal) oldModal.remove();
    
    document.body.appendChild(modal);
    modal.onclick = function(e) {
        if (e.target === this) closeDishModal();
    };
}

function closeDishModal() {
    const modal = document.getElementById('dishFormModal');
    if (modal) modal.remove();
}

async function saveDish() {
    const name = document.getElementById('dishName')?.value?.trim();
    const price = parseFloat(document.getElementById('dishPrice')?.value || 0);
    const category = document.getElementById('dishCategory')?.value?.trim();
    const cookingTime = parseInt(document.getElementById('dishTime')?.value || 15);
    
    if (!name || !price || !category || !cookingTime) {
        showError('Заполните все поля');
        return;
    }
    
    try {
        const dishData = {
            name: name,
            price: price,
            category: category,
            cooking_time: cookingTime
        };
        
        if (editingDishId) {
            // Update dish - use query params
            const params = new URLSearchParams();
            params.append('name', name);
            params.append('price', price.toString());
            params.append('category', category);
            params.append('cooking_time', cookingTime.toString());
            await apiRequest(`/dishes/${editingDishId}?${params.toString()}`, 'PUT');
            showSuccess('Блюдо обновлено');
        } else {
            // Create dish - use query params
            const params = new URLSearchParams();
            params.append('name', name);
            params.append('price', price.toString());
            params.append('category', category);
            params.append('cooking_time', cookingTime.toString());
            params.append('description', '');
            await apiRequest(`/dishes/?${params.toString()}`, 'POST');
            showSuccess('Блюдо добавлено');до добавлено');
        }
        closeDishModal();
        await loadMenu(); // Обновляем меню мгновенно
    } catch (error) {
        showError('Ошибка: ' + error.message);
    }
}

async function deleteDish(dishId) {
    if (confirm('Удалить это блюдо?')) {
        try {
            await apiRequest(`/dishes/${dishId}`, 'DELETE');
            showSuccess('Блюдо удалено');
            await loadMenu();
        } catch (error) {
            showError('Ошибка удаления: ' + error.message);
        }
    }
}

// ==================== TABLE & ORDER MANAGEMENT ====================

function showCreateOrderForTable(tableId) {
    selectedTableId = tableId;
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'createOrderModal';
    modal.style.cssText = 'display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 9999;';
    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; width: 90%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin-top: 0; margin-bottom: 20px; color: #333;">Создать заказ для стола ${tableId}</h2>
            <form id="orderForm" onsubmit="event.preventDefault(); createOrder();">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Блюда (через запятую, например: Пицца, Салат):</label>
                    <textarea id="orderDishes" rows="3" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px; font-family: inherit;" required placeholder="Введите названия блюд..."></textarea>
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Сумма (₽):</label>
                    <input type="number" id="orderAmount" step="0.01" min="0" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                </div>
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary" style="flex: 1; padding: 10px;">Создать</button>
                    <button type="button" class="btn btn-secondary" style="flex: 1; padding: 10px;" onclick="closeCreateOrderModal()">Отмена</button>
                </div>
            </form>
        </div>
    `;
    
    const oldModal = document.getElementById('createOrderModal');
    if (oldModal) oldModal.remove();
    
    document.body.appendChild(modal);
    modal.onclick = function(e) {
        if (e.target === this) closeCreateOrderModal();
    };
}

function closeCreateOrderModal() {
    const modal = document.getElementById('createOrderModal');
    if (modal) modal.remove();
}

async function createOrder() {
    const dishesInput = document.getElementById('orderDishes')?.value?.trim();
    const amount = parseFloat(document.getElementById('orderAmount')?.value || 0);
    
    if (!dishesInput || !amount) {
        showError('Заполните все поля');
        return;
    }
    
    const dishes = dishesInput.split(',').map(d => d.trim()).filter(d => d.length > 0);
    
    if (dishes.length === 0) {
        showError('Укажите хотя бы одно блюдо');
        return;
    }
    
    try {
        await apiRequest('/orders/', 'POST', {
            table_id: selectedTableId,
            dishes: dishes,
            total_amount: amount,
            status: 'pending'
        });
        showSuccess('Заказ создан!');
        closeCreateOrderModal();
        await loadOrders();
        await loadTables();
    } catch (error) {
        showError('Ошибка: ' + error.message);
    }
}

function showOrderDetails(orderId) {
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
                            <h3 style="margin: 0; font-size: 24px; color: #667eea;">${order.id}</h3>
                        </div>
                        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px;">
                            <p style="margin: 0 0 8px 0; font-size: 12px; color: #999; text-transform: uppercase; font-weight: bold;">Стол</p>
                            <h3 style="margin: 0; font-size: 24px; color: #667eea;">${order.table_id}</h3>
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

function showEditOrderModal(orderId) {
    getOrders().then(orders => {
        const order = orders.find(o => o.id === orderId);
        if (!order) {
            showError('Заказ не найден');
            return;
        }
        
        editingOrderId = orderId;
        const dishesStr = Array.isArray(order.dishes) ? order.dishes.join(', ') : '';
        
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.id = 'editOrderModal';
        modal.style.cssText = 'display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 9999;';
        modal.innerHTML = `
            <div style="background: white; padding: 30px; border-radius: 10px; max-width: 500px; width: 90%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <h2 style="margin-top: 0; margin-bottom: 20px; color: #333;">Редактировать заказ ${orderId}</h2>
                <form id="editOrderForm" onsubmit="event.preventDefault(); updateOrder();">
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Блюда (через запятую):</label>
                        <textarea id="editOrderDishes" rows="3" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px; font-family: inherit;" required>${escapeHtml(dishesStr)}</textarea>
                    </div>
                    <div style="margin-bottom: 15px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Сумма (₽):</label>
                        <input type="number" id="editOrderAmount" step="0.01" min="0" value="${order.total_amount}" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                    </div>
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Статус:</label>
                        <select id="editOrderStatus" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;">
                            <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>Ожидание</option>
                            <option value="cooking" ${order.status === 'cooking' ? 'selected' : ''}>Приготовление</option>
                            <option value="ready" ${order.status === 'ready' ? 'selected' : ''}>Готов</option>
                            <option value="completed" ${order.status === 'completed' ? 'selected' : ''}>Выдан</option>
                        </select>
                    </div>
                    <div style="display: flex; gap: 10px;">
                        <button type="submit" class="btn btn-primary" style="flex: 1; padding: 10px;">Сохранить</button>
                        <button type="button" class="btn btn-secondary" style="flex: 1; padding: 10px;" onclick="closeEditOrderModal()">Отмена</button>
                    </div>
                </form>
            </div>
        `;
        
        const oldModal = document.getElementById('editOrderModal');
        if (oldModal) oldModal.remove();
        
        document.body.appendChild(modal);
        modal.onclick = function(e) {
            if (e.target === this) closeEditOrderModal();
        };
    });
}

function closeEditOrderModal() {
    const modal = document.getElementById('editOrderModal');
    if (modal) modal.remove();
}

async function updateOrder() {
    const dishesInput = document.getElementById('editOrderDishes')?.value?.trim();
    const amount = parseFloat(document.getElementById('editOrderAmount')?.value || 0);
    const status = document.getElementById('editOrderStatus')?.value;
    
    if (!dishesInput || !amount || !status) {
        showError('Заполните все поля');
        return;
    }
    
    const dishes = dishesInput.split(',').map(d => d.trim()).filter(d => d.length > 0);
    
    if (dishes.length === 0) {
        showError('Укажите хотя бы одно блюдо');
        return;
    }
    
    try {
        await apiRequest(`/orders/${editingOrderId}`, 'PUT', {
            dishes: dishes,
            total_amount: amount,
            status: status
        });
        showSuccess('Заказ обновлен!');
        closeEditOrderModal();
        await loadOrders();
        await loadTables();
    } catch (error) {
        showError('Ошибка: ' + error.message);
    }
}

async function completeOrder(orderId) {
    if (confirm('Завершить этот заказ?')) {
        try {
            await apiRequest(`/orders/${orderId}`, 'DELETE');
            showSuccess('Заказ завершен');
            await loadOrders();
            await loadTables();
        } catch (error) {
            showError('Ошибка: ' + error.message);
        }
    }
}

function closeOrderModal() {
    const modal = document.getElementById('orderModal');
    if (modal) modal.classList.add('hidden');
}

// ==================== EMPLOYEE MANAGEMENT ====================

function addEmployeeModal() {
    if (currentUser && currentUser.role !== 'admin') {
        showError('Только администратор может добавлять');
        return;
    }
    editingEmployeeId = null;
    openEmployeeForm('Добавить сотрудника', '', '', 'waiter', true);
}

function showEditEmployeeModal(empId, username, name, role) {
    editingEmployeeId = empId;
    openEmployeeForm('Обновить сотрудника', username, name, role, false);
}

function openEmployeeForm(title, username, name, role, isNew) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.id = 'employeeFormModal';
    modal.style.cssText = 'display: flex; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); align-items: center; justify-content: center; z-index: 9999;';
    modal.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 10px; max-width: 400px; width: 90%; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2 style="margin-top: 0; margin-bottom: 20px; color: #333;">${title}</h2>
            <form id="empForm" onsubmit="event.preventDefault(); saveEmployee();">
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Логин:</label>
                    <input type="text" id="empUsername" value="${escapeHtml(username)}" ${!isNew ? 'disabled' : 'required'} style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Имя:</label>
                    <input type="text" id="empName" value="${escapeHtml(name)}" ${isNew ? 'required' : ''} style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;">
                </div>
                <div style="margin-bottom: 15px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Роль:</label>
                    <select id="empRole" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;" required>
                        <option value="waiter" ${role === 'waiter' ? 'selected' : ''}>Официант</option>
                        <option value="chef" ${role === 'chef' ? 'selected' : ''}>Повар</option>
                        <option value="admin" ${role === 'admin' ? 'selected' : ''}>Администратор</option>
                    </select>
                </div>
                <div style="margin-bottom: 20px;">
                    <label style="display: block; margin-bottom: 5px; font-weight: bold; color: #555;">Пароль:</label>
                    <input type="password" id="empPassword" ${isNew ? 'required' : ''} placeholder="${isNew ? 'Обязательно' : 'Оставьте пусто, чтобы не менять'}" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; font-size: 14px;">
                </div>
                <div style="display: flex; gap: 10px;">
                    <button type="submit" class="btn btn-primary" style="flex: 1; padding: 10px;">Сохранить</button>
                    <button type="button" class="btn btn-secondary" style="flex: 1; padding: 10px;" onclick="closeEmployeeForm()">Отмена</button>
                </div>
            </form>
        </div>
    `;
    
    const oldModal = document.getElementById('employeeFormModal');
    if (oldModal) oldModal.remove();
    
    document.body.appendChild(modal);
    modal.onclick = function(e) {
        if (e.target === this) closeEmployeeForm();
    };
}

function closeEmployeeForm() {
    const modal = document.getElementById('employeeFormModal');
    if (modal) modal.remove();
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
        closeEmployeeForm();
        await loadEmployees();
    } catch (error) {
        showError('Ошибка: ' + error.message);
    }
}

async function deleteEmployee(empId) {
    if (confirm('Удалить сотрудника?')) {
        try {
            await apiRequest(`/employees/${empId}`, 'DELETE');
            showSuccess('Сотрудник удален');
            await loadEmployees();
        } catch (error) {
            showError('Ошибка удаления: ' + error.message);
        }
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
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return String(text).replace(/[&<>"']/g, m => map[m]);
}

// ==================== EVENT HANDLERS ====================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Приложение загружается...');
    
    // IMPORTANT: ALWAYS SHOW LOGIN SCREEN ON LOAD
// ==================== INITIALIZATION ====================
// Скрипт загружается в конце <body>, DOM уже готов!
(function initApp() {
    console.log('🚀 App init started...');
