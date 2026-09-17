let currentPage = 1;
let currentSearch = '';
let sortBy = 'created_at';
let sortOrder = 'desc';
let totalPages = 1;

// 1. Fetch & Display Members (Handles Search, Sort, Pagination)
async function loadMembers() {
    const res = await fetch(`/api/members/?search=${currentSearch}&page=${currentPage}&sort_by=${sortBy}&order=${sortOrder}`);
    if (res.status === 401) {
        window.location.href = '/login'; // Redirect if unauthorized
        return;
    }
    const data = await res.json();
    
    totalPages = data.pages;
    document.getElementById('pageInfo').innerText = `Page ${data.page} of ${data.pages} (Total: ${data.total})`;
    
    const tbody = document.getElementById('membersTable');
    tbody.innerHTML = ''; // Clear existing rows
    
    data.members.forEach(m => {
        // Color code tiers
        let tierColor = 'text-gray-500';
        if(m.tier === 'SILVER') tierColor = 'text-gray-400 font-bold';
        if(m.tier === 'GOLD') tierColor = 'text-yellow-500 font-bold';

        tbody.innerHTML += `
            <tr class="hover:bg-gray-50">
                <td class="p-3 border-b font-mono">${m.phone}</td>
                <td class="p-3 border-b">${m.name}</td>
                <td class="p-3 border-b ${tierColor}">${m.tier}</td>
                <td class="p-3 border-b font-bold text-lg">${m.balance} pts</td>
                <td class="p-3 border-b flex gap-2">
                    <button onclick="addPurchase('${m.phone}')" class="bg-blue-100 text-blue-700 px-2 py-1 rounded text-sm hover:bg-blue-200">+$</button>
                    <button onclick="redeemPoints('${m.phone}')" class="bg-orange-100 text-orange-700 px-2 py-1 rounded text-sm hover:bg-orange-200">Redeem</button>
                </td>
            </tr>
        `;
    });
}

// 2. Action: Add Purchase (Earn Points)
async function addPurchase(phone) {
    const amount = prompt(`Enter purchase dollar amount for ${phone}:`);
    if (!amount || isNaN(amount)) return;

    const res = await fetch('/api/purchases/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, amount: parseFloat(amount) })
    });
    const data = await res.json();
    alert(data.message || data.error);
    loadMembers(); // Refresh live balance
}

// 3. Action: Redeem Item
async function redeemPoints(phone) {
    const points = prompt(`Enter points to deduct for ${phone}:`);
    if (!points || isNaN(points)) return;
    
    const item = prompt(`What item is being redeemed?`);

    const res = await fetch('/api/redemptions/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, points: parseInt(points), item })
    });
    const data = await res.json();
    alert(data.message || data.error);
    loadMembers(); // Refresh live balance
}

// 4. Action: Create New Customer
async function createMember() {
    const phone = document.getElementById('newPhone').value;
    const name = document.getElementById('newName').value;
    if(!phone || !name) return alert("Enter both phone and name");

    const res = await fetch('/api/members/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone, name })
    });
    
    if (res.ok) {
        document.getElementById('newPhone').value = '';
        document.getElementById('newName').value = '';
        loadMembers();
    } else {
        const data = await res.json();
        alert(data.error);
    }
}

// 5. UI Controls (Search, Sort, Pagination, Logout)
function handleSearch() {
    currentSearch = document.getElementById('searchInput').value;
    currentPage = 1; // Reset to page 1 on new search
    loadMembers();
}

function toggleSort(column) {
    if (sortBy === column) {
        sortOrder = sortOrder === 'desc' ? 'asc' : 'desc'; // flip order
    } else {
        sortBy = column;
        sortOrder = 'desc'; // default new column to descending
    }
    loadMembers();
}

function prevPage() {
    if (currentPage > 1) { currentPage--; loadMembers(); }
}

function nextPage() {
    if (currentPage < totalPages) { currentPage++; loadMembers(); }
}

async function logout() {
    await fetch('/api/auth/logout', { method: 'POST' });
    window.location.href = '/login';
}

// Initial Load
window.onload = loadMembers;