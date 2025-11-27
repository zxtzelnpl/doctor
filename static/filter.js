const buildParamsFromForm = (form) => {
  const params = new URLSearchParams();
  const elements = Array.from(form.elements);
  for (const el of elements) {
    if (!el.name) continue;
    const value = (el.value || '').trim();
    if (value) params.set(el.name, value);
  }
  return params;
};

const applyParamsToForm = (form, params) => {
  const elements = Array.from(form.elements);
  for (const el of elements) {
    if (!el.name) continue;
    const v = params.get(el.name);
    if (v !== null) el.value = v;
  }
};

const fetchSheet = async (params) => {
  const url = '/api/sheet' + (params && params.toString() ? `?${params.toString()}` : '');
  const res = await fetch(url);
  if (!res.ok) throw new Error('请求失败');
  return await res.json();
};

const renderTable = (container, headers, rows) => {
  const table = document.createElement('table');
  table.className = 'min-w-full table-auto border-collapse';

  const thead = document.createElement('thead');
  thead.className = 'bg-gray-100';
  const headerRow = document.createElement('tr');
  headers.forEach(key => {
    const th = document.createElement('th');
    th.textContent = key;
    th.className = 'px-4 py-2 text-left whitespace-nowrap border border-gray-200';
    headerRow.appendChild(th);
  });
  thead.appendChild(headerRow);
  table.appendChild(thead);

  const tbody = document.createElement('tbody');
  rows.forEach(row => {
    const tr = document.createElement('tr');
    tr.className = 'odd:bg-white even:bg-gray-50';
    headers.forEach(key => {
      const td = document.createElement('td');
      td.textContent = row[key] ?? '';
      td.className = 'px-4 py-2 whitespace-nowrap border border-gray-200';
      tr.appendChild(td);
    });
    tbody.appendChild(tr);
  });
  table.appendChild(tbody);

  container.innerHTML = '';
  container.appendChild(table);
};

const init = async () => {
  const form = document.getElementById('filter-form');
  const detailsEl = document.getElementById('details');
  const applyBtn = document.getElementById('apply-btn');
  const resetBtn = document.getElementById('reset-btn');

  const currentParams = new URLSearchParams(window.location.search);
  applyParamsToForm(form, currentParams);

  const load = async () => {
    const data = await fetchSheet(currentParams);
    const headers = Array.isArray(data.headers) ? data.headers : [];
    const rows = Array.isArray(data.data) ? data.data : [];
    renderTable(detailsEl, headers, rows);
  };

  applyBtn.onclick = async () => {
    const params = buildParamsFromForm(form);
    const qs = params.toString();
    const url = qs ? `?${qs}` : '';
    window.history.pushState({}, '', url);
    currentParams.set('x', '');
    for (const key of Array.from(currentParams.keys())) currentParams.delete(key);
    for (const [k, v] of params.entries()) currentParams.set(k, v);
    await load();
  };

  resetBtn.onclick = async () => {
    Array.from(form.elements).forEach(el => { if (el.name) el.value = ''; });
    window.history.pushState({}, '', window.location.pathname);
    currentParams.set('x', '');
    for (const key of Array.from(currentParams.keys())) currentParams.delete(key);
    await load();
  };
};

init();
