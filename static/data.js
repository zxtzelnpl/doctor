
const fetchData = async (indicator) => {
  try {
    const response = await fetch('/api/indicator', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ indicator })
    });

    if (!response.ok) {
      throw new Error('请求失败');
    }

    const data = await response.json();
    return data.value;
  } catch (error) {
    console.error('获取数据出错:', error);
  }
}

const init = async () => {
  // 1. 从浏览器的search参数中获取indicator参数
  const params = new URLSearchParams(window.location.search);
  const indicator = params.get('indicator');
  if (!indicator) return;

  // 2. 根据indicator参数发起请求，获取数据
  const value = await fetchData(indicator);
  if (!value || !Array.isArray(value.data)) return;

  // 3. 将数据的长度放到id为indicator的元素中
  const indicatorEl = document.getElementById('indicator');
  if (indicatorEl) indicatorEl.textContent = value.data.length;

  // 4. 将data渲染到对应的表格中，表格的header为data每一行数据的key
  const detailsEl = document.getElementById('details');
  if (!detailsEl) return;

  const headers = Array.isArray(value.headers) ? value.headers : [];
  const table = document.createElement('table');
  table.className = 'min-w-full table-auto border-collapse';

  // 表头
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

  // 表体
  const tbody = document.createElement('tbody');
  value.data.forEach(row => {
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

  // 5. 表格放到id为details的元素中
  detailsEl.innerHTML = '';
  detailsEl.appendChild(table);
}



init()
