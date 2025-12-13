// База данных в памяти (временная)
const DB = {
    users: [
        { id: 1, login: 'admin', pass: 'admin', role: 'admin' },
        { id: 2, login: 'chef', pass: 'chef', role: 'chef' },
        { id: 3, login: 'waiter', pass: 'waiter', role: 'waiter' },
        { id: 4, login: 'ofikNum1', pass: '123321', role: 'waiter' },
        { id: 5, login: 'adminNum1', pass: '123321', role: 'admin' },
        { id: 6, login: 'povarNum1', pass: '123321', role: 'chef' }
    ],
    menu: {
        main: [
            { id: 'm1', name: 'Картошка с котлетами', desc: 'Картофельное пюре с котлетами из говяжьего фарша.', price: 280 },
            { id: 'm2', name: 'Макароны с фаршем', desc: 'Классические варёные макароны с куриным фаршем.', price: 230 }
        ],
        hot: [
            { id: 'h1', name: 'Борщ', desc: 'Наваристое первое блюдо с мясом и овощами (капустой, картошкой, свёклой, морковью).', price: 150 },
            { id: 'h2', name: 'Солянка', desc: 'Густой заправочный суп с острыми приправами; готовится на мясном, грибном или рыбном бульонах; сочетает компоненты щей и рассольника.', price: 160 }
        ],
        drinks: [
            { id: 'd1', name: 'Сок', desc: 'Яблочный.', price: 80 },
            { id: 'd2', name: 'Газировка', desc: 'Минеральная вода.', price: 70 }
        ],
        dessert: [
            { id: 's1', name: 'Чизкейк', desc: 'Сыросодержащий десерт; в основе смесь мягкого сыра/творога, сахара и жирного молока/сливок.', price: 150 },
            { id: 's2', name: 'Блини со сгущенкой', desc: 'Порция из 4шт', price: 120 }
        ]
    },
    tables: Array.from({ length: 9 }, (_, i) => ({ id: i + 1, orderId: null })),
    orders: []
};

let state = {
    currentUser: null,
    currentMenuSection: 'main',
    modalTable: null,
    modalSelection: {}
};

// Вспомогательные функции
function qs(id) { return document.getElementById(id); }
function qAll(sel) { return document.querySelectorAll(sel); }

// Инициализация
function init() {
    // Авторизация
    qs('tabLogin').onclick = () => toggleAuth('login');
    qs('tabRegister').onclick = () => toggleAuth('register');
    qs('doLogin').onclick = doLogin;
    qs('doRegister').onclick = doRegister;

    // Навигация по меню
    qAll('.menu-btn').forEach(b => {
        b.onclick = () => {
            qAll('.menu-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            showTab(b.dataset.tab);
        };
    });

    // Переключение разделов меню
    qAll('.switch-btn').forEach(b => {
        b.onclick = () => {
            qAll('.switch-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active');
            state.currentMenuSection = b.dataset.section;
            renderMenu();
        };
    });

    // Выход
    qs('logoutBtn').onclick = () => {
        state.currentUser = null;
        qs('appSection').classList.add('hidden');
        qs('authSection').classList.remove('hidden');
        qAll('.menu-btn').forEach(b => b.style.display = '');
    };

    renderTables();
    renderOrders();
    renderMenu();
    renderAccount();
    updateStats();

    // Показываем меню при загрузке
    showTab('menuTab');
}

function toggleAuth(mode) {
    if (mode === 'login') {
        qs('loginForm').classList.remove('hidden');
        qs('registerForm').classList.add('hidden');
        qs('tabLogin').classList.add('active');
        qs('tabRegister').classList.remove('active');
    } else {
        qs('loginForm').classList.add('hidden');
        qs('registerForm').classList.remove('hidden');
        qs('tabRegister').classList.add('active');
        qs('tabLogin').classList.remove('active');
    }
}

function doLogin() {
    const login = qs('loginUser').value.trim();
    const pass = qs('loginPass').value;
    const role = qs('loginRole').value;
    const u = DB.users.find(x => x.login === login && x.pass === pass && x.role === role);
    
    if (!u) {
        alert('Неверные данные');
        return;
    }
    
    state.currentUser = { ...u };
    enterApp();
}

function doRegister() {
    const login = qs('regUser').value.trim();
    const pass = qs('regPass').value;
    const role = qs('regRole').value;
    
    if (!login || !pass) {
        alert('Введите логин и пароль');
        return;
    }
    
    if (DB.users.find(x => x.login === login)) {
        alert('Пользователь уже существует');
        return;
    }
    
    const id = Date.now();
    DB.users.push({ id, login, pass, role });
    alert('Создано: ' + login);
    qs('regUser').value = '';
    qs('regPass').value = '';
}

function enterApp() {
    qs('authSection').classList.add('hidden');
    qs('appSection').classList.remove('hidden');
    renderAccount();
    renderTables();
    renderOrders();

    // Ролевая настройка интерфейса
    if (state.currentUser) {
        qAll('.menu-btn').forEach(b => b.style.display = '');
        if (state.currentUser.role === 'chef') {
            qAll('.menu-btn').forEach(b => {
                if (b.dataset.tab === 'tablesTab') b.style.display = 'none';
            });
        }
    }

    showTab('menuTab');
}

function showTab(id) {
    qAll('.tabpane').forEach(p => p.classList.add('hidden'));
    qs(id).classList.remove('hidden');
}

function renderMenu() {
    const list = qs('menuContent');
    list.innerHTML = '';
    const section = state.currentMenuSection;
    const items = DB.menu[section] || [];
    
    items.forEach(it => {
        const el = document.createElement('div');
        el.className = 'item';
        
        let controls = '';
        if (state.currentUser && state.currentUser.role === 'admin') {
            controls = `
                <div style="display:flex;gap:6px;margin-top:6px">
                    <button class="primary" data-cmd="edit-menu" data-id="${it.id}">Редактировать</button>
                    <button class="danger" data-cmd="del-menu" data-id="${it.id}">Удалить</button>
                </div>
            `;
        }
        
        el.innerHTML = `
            <div class="name">${it.name}</div>
            <div class="desc">${it.desc || ''}</div>
            <div class="meta">${it.price}₽</div>
            ${controls}
        `;
        
        list.appendChild(el);
    });

    // Форма добавления для администратора
    if (state.currentUser && state.currentUser.role === 'admin') {
        const form = document.createElement('div');
        form.className = 'item';
        form.style.marginTop = '10px';
        
        form.innerHTML = `
            <div style="font-weight:800">Добавить блюдо</div>
            <div style="display:flex;gap:8px;margin-top:8px">
                <input id="newName" placeholder="Название" style="flex:1;padding:8px;border-radius:6px;border:1px solid #eee"/>
                <input id="newPrice" placeholder="Цена" style="width:100px;padding:8px;border-radius:6px;border:1px solid #eee"/>
            </div>
            <div style="display:flex;gap:8px;margin-top:8px">
                <select id="newSection">
                    <option value="main">Основное</option>
                    <option value="hot">Горячее</option>
                    <option value="drinks">Напитки</option>
                    <option value="dessert">Десерт</option>
                </select>
                <button id="addMenuBtn" class="primary">Добавить</button>
            </div>
        `;
        
        list.appendChild(form);
        
        // Обработчик добавления
        setTimeout(() => {
            const btn = qs('addMenuBtn');
            if (btn) {
                btn.onclick = () => {
                    const name = qs('newName').value.trim();
                    const price = Number(qs('newPrice').value);
                    const sec = qs('newSection').value;
                    
                    if (!name || !price) {
                        alert('Введите название и цену');
                        return;
                    }
                    
                    const id = sec[0] + Date.now().toString(36);
                    DB.menu[sec].push({ id, name, desc: '', price });
                    renderMenu();
                };
            }
        }, 50);
    }
}

// Глобальные обработчики кликов
document.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    
    const menuCmd = btn.dataset.cmd;
    
    if (menuCmd === 'edit-menu') {
        const id = btn.dataset.id;
        const it = findMenuItemById(id);
        if (!it) {
            alert('Позиция не найдена');
            return;
        }
        
        const newName = prompt('Новое название', it.name) || it.name;
        const newPrice = Number(prompt('Новая цена', it.price) || it.price);
        it.name = newName;
        it.price = newPrice;
        renderMenu();
        return;
    }
    
    if (menuCmd === 'del-menu') {
        const id = btn.dataset.id;
        for (const k of Object.keys(DB.menu)) {
            const idx = DB.menu[k].findIndex(x => x.id === id);
            if (idx >= 0) {
                DB.menu[k].splice(idx, 1)[0];
                renderMenu();
                break;
            }
        }
        return;
    }
});

// Остальные функции (renderOrders, renderTables, и т.д.)
// ... продолжайте с остальным кодом из вашего исходного файла ...

function renderOrders() {
    const el = qs('ordersList');
    el.innerHTML = '';
    
    const active = DB.orders.filter(o => o.status !== 'served' && o.status !== 'canceled');
    
    active.forEach(o => {
        const total = o.items.reduce((s, it) => s + (it.price || 0), 0);
        const div = document.createElement('div');
        div.className = 'order';
        
        div.innerHTML = `
            <div>
                <div style="font-weight:700">Заказ ${o.id} — стол ${o.table} · <span style="font-weight:700">${total}₽</span></div>
                <div class="meta">${o.items.length} позиций · статус: ${o.status}</div>
                <div class="meta">Создал: ${o.assignedTo || '—'} · ${new Date(o.created).toLocaleString()}</div>
            </div>
            <div style="display:flex;flex-direction:column;gap:6px">
                ${renderOrderButtons(o)}
            </div>
        `;
        
        el.appendChild(div);
    });
    
    updateStats();
}

function renderOrderButtons(o) {
    const role = state.currentUser ? state.currentUser.role : '';
    let html = '';
    
    if (role === 'waiter') {
        html += `<button data-cmd="complete" data-id="${o.id}" class="primary">Готово</button>`;
        html += `<button data-cmd="cancel" data-id="${o.id}" class="danger">Отменить</button>`;
    } else if (role === 'chef') {
        html += `<button data-cmd="start" data-id="${o.id}" class="primary">Приготовить</button>`;
        html += `<button data-cmd="chef-ready" data-id="${o.id}" class="primary">Готово</button>`;
    } else if (role === 'admin') {
        html += `<button data-cmd="assign" data-id="${o.id}" class="primary">Назначить</button>`;
        html += `<button data-cmd="delete" data-id="${o.id}" class="danger">Удалить</button>`;
    } else {
        html += `<div class="meta">Войдите для действий</div>`;
    }
    
    return html;
}

// Добавьте обработчики для кнопок заказов
document.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    
    const cmd = btn.dataset.cmd;
    const id = btn.dataset.id;
    if (!cmd) return;
    
    const order = DB.orders.find(x => x.id === id);
    if (!order) return;
    
    if (cmd === 'start') {
        order.status = 'cooking';
        alert(`Повар начал готовить заказ ${order.id}`);
    }
    if (cmd === 'complete') {
        order.status = 'served';
        alert(`Официант завершил заказ ${order.id}`);
        const t = DB.tables.find(tt => tt.id === order.table);
        if (t) t.orderId = null;
    }
    if (cmd === 'chef-ready') {
        order.status = 'ready';
        alert(`Заказ ${order.id} помечен как готовый`);
    }
    if (cmd === 'cancel') {
        order.status = 'canceled';
        const t = DB.tables.find(tt => tt.id === order.table);
        if (t) t.orderId = null;
    }
    if (cmd === 'assign') {
        order.assignedTo = prompt('Назначить (логин)') || order.assignedTo;
    }
    if (cmd === 'delete') {
        DB.orders = DB.orders.filter(x => x.id !== id);
        const t = DB.tables.find(tt => tt.id === order.table);
        if (t) t.orderId = null;
    }
    
    renderOrders();
    renderTables();
    updateStats();
});

function renderTables() {
    const root = qs('tablesGrid');
    root.innerHTML = '';
    
    const showOnlyActive = state.currentUser && state.currentUser.role === 'chef';
    const tablesToShow = showOnlyActive ? DB.tables.filter(t => t.orderId) : DB.tables;
    
    tablesToShow.forEach(t => {
        const el = document.createElement('div');
        el.className = 'table' + (t.orderId ? ' booked' : '');
        el.innerHTML = `
            <div style="font-weight:700">Стол ${t.id}</div>
            <div class="meta">${t.orderId ? ('Заказ ' + t.orderId) : 'Свободен'}</div>
        `;
        el.onclick = () => onTableClick(t);
        root.appendChild(el);
    });
}

function onTableClick(t) {
    if (!state.currentUser) {
        alert('Войдите');
        return;
    }
    openTableModal(t);
}

function openTableModal(t) {
    const existing = document.getElementById('tableModal');
    if (existing) existing.remove();
    
    const modal = document.createElement('div');
    modal.id = 'tableModal';
    modal.className = 'modal';
    
    const card = document.createElement('div');
    card.className = 'modal-card';
    
    card.innerHTML = `
        <div class="modal-header">
            <div style="font-weight:800">Стол ${t.id}</div>
            <button id="closeTableModal" class="icon-small">✕</button>
        </div>
        <div class="modal-body">
            <div style="margin-bottom:8px;color:var(--muted)">Выберите позиции из меню для добавления в заказ.</div>
            <div id="menuSelectArea" class="menu-section"></div>
            <div style="margin-top:10px" id="currentOrderInfo"></div>
        </div>
        <div class="modal-actions">
            <button id="createOrderBtn" class="primary">Создать заказ</button>
            <button id="addItemsBtn" class="primary">Добавить к заказу</button>
            <button id="closeAction" class="icon-small">Закрыть</button>
        </div>
    `;
    
    modal.appendChild(card);
    document.body.appendChild(modal);
    
    // Построение выбора меню
    const sectionNames = { main: 'Основное', hot: 'Горячее', drinks: 'Напитки', dessert: 'Десерт' };
    const menuArea = modal.querySelector('#menuSelectArea');
    
    Object.keys(DB.menu).forEach(sec => {
        const secDiv = document.createElement('div');
        secDiv.className = 'menu-section';
        const title = sectionNames[sec] || sec;
        secDiv.innerHTML = `<div class="menu-section-title">${title}</div>`;
        
        DB.menu[sec].forEach(it => {
            const row = document.createElement('div');
            row.className = 'menu-row';
            row.innerHTML = `<label><input type="checkbox" data-id="${it.id}" /> ${it.name} — ${it.price}₽</label>`;
            secDiv.appendChild(row);
        });
        
        menuArea.appendChild(secDiv);
    });
    
    const currentInfo = modal.querySelector('#currentOrderInfo');
    if (t.orderId) {
        const ord = DB.orders.find(o => o.id === t.orderId);
        if (ord) {
            const total = ord.items.reduce((s, it) => s + (it.price || 0), 0);
            currentInfo.innerHTML = `
                <div style="font-weight:700">Текущий заказ: ${ord.id} · статус: ${ord.status} · <span style="font-weight:700">${total}₽</span></div>
                <div class="meta">Позиции: ${ord.items.length ? ord.items.map(i => i.name).join(', ') : '(пусто)'}</div>
            `;
            modal.querySelector('#createOrderBtn').style.display = 'none';
        } else {
            currentInfo.innerHTML = '<div class="meta">Ошибка: прикреплённый заказ не найден</div>';
        }
    } else {
        currentInfo.innerHTML = '<div class="meta">Стол свободен — можно создать новый заказ.</div>';
        modal.querySelector('#addItemsBtn').style.display = 'none';
    }
    
    // Обработчики
    modal.querySelector('#closeTableModal').onclick = closeTableModal;
    modal.querySelector('#closeAction').onclick = closeTableModal;
    
    modal.querySelector('#createOrderBtn').onclick = () => {
        if (!(state.currentUser.role === 'waiter' || state.currentUser.role === 'admin')) {
            alert('Только официант или администратор может создавать заказ.');
            return;
        }
        
        const checked = Array.from(modal.querySelectorAll('input[type=checkbox]:checked')).map(ch => ch.dataset.id);
        if (checked.length === 0) {
            alert('Выберите хотя бы одну позицию');
            return;
        }
        
        const order = {
            id: 'o' + Date.now(),
            table: t.id,
            items: [],
            status: 'new',
            created: Date.now(),
            assignedTo: state.currentUser.login
        };
        
        checked.forEach(pid => {
            const it = findMenuItemById(pid);
            if (it) order.items.push({ id: it.id, name: it.name, price: it.price });
        });
        
        DB.orders.push(order);
        t.orderId = order.id;
        
        closeTableModal();
        renderOrders();
        renderTables();
        updateStats();
        
        qAll('.menu-btn').forEach(b => b.classList.remove('active'));
        const ordersBtn = Array.from(qAll('.menu-btn')).find(b => b.dataset.tab === 'ordersTab');
        if (ordersBtn) ordersBtn.classList.add('active');
        showTab('ordersTab');
    };
    
    modal.querySelector('#addItemsBtn').onclick = () => {
        const ord = DB.orders.find(o => o.id === t.orderId);
        if (!ord) {
            alert('Заказ не найден');
            return;
        }
        
        const checked = Array.from(modal.querySelectorAll('input[type=checkbox]:checked')).map(ch => ch.dataset.id);
        if (checked.length === 0) {
            alert('Выберите хотя бы одну позицию');
            return;
        }
        
        checked.forEach(pid => {
            const it = findMenuItemById(pid);
            if (it) ord.items.push({ id: it.id, name: it.name, price: it.price });
        });
        
        closeTableModal();
        renderOrders();
        renderTables();
        updateStats();
        
        qAll('.menu-btn').forEach(b => b.classList.remove('active'));
        const ordersBtn2 = Array.from(qAll('.menu-btn')).find(b => b.dataset.tab === 'ordersTab');
        if (ordersBtn2) ordersBtn2.classList.add('active');
        showTab('ordersTab');
    };
}

function closeTableModal() {
    const m = document.getElementById('tableModal');
    if (m) m.remove();
}

function findMenuItemById(id) {
    for (const k of Object.keys(DB.menu)) {
        const it = DB.menu[k].find(x => x.id === id);
        if (it) return it;
    }
    return null;
}

function renderAccount() {
    const el = qs('accountInfo');
    if (!el) return;
    
    if (!state.currentUser) {
        el.innerHTML = '<div class="meta">Не вошли</div>';
        const statsEl = qs('accountTab')?.querySelector('.account-stats');
        if (statsEl) statsEl.style.display = '';
        return;
    }
    
    const role = state.currentUser.role;
    const roleRus = role === 'waiter' ? 'Официант' : role === 'chef' ? 'Повар' : role === 'admin' ? 'Администратор' : role;
    
    el.innerHTML = `
        <div style="font-weight:800">${state.currentUser.login} · ${roleRus}</div>
        <div class="meta">Зарегистрирован для демонстрации интерфейса.</div>
        <div class="account-details">
            <div>Последний вход: ${new Date().toLocaleString()}</div>
            <div>Роль: ${roleRus}</div>
        </div>
    `;
    
    const statsEl = qs('accountTab')?.querySelector('.account-stats');
    if (statsEl) {
        if (role === 'admin') {
            statsEl.style.display = 'none';
        } else {
            statsEl.style.display = '';
        }
    }
}

function updateStats() {
    qs('statOrders').textContent = DB.orders.length;
    qs('statActive').textContent = DB.orders.filter(o => o.status !== 'served' && o.status !== 'canceled').length;
    qs('statTables').textContent = DB.tables.filter(t => t.orderId).length;
}

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', init);