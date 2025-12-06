function getParamsFromSearch() {
  const qs = new URLSearchParams(window.location.search);
  const initParams = {};
  qs.forEach((v, k) => {
    if (v !== undefined && v !== null && String(v).trim() !== "") initParams[k] = v;
  });

  return initParams;
}

function toQuery(params) {
  const usp = new URLSearchParams();
  Object.keys(params).forEach(k => {
    if (params[k] !== undefined && params[k] !== null) usp.set(k, params[k]);
  });
  return usp.toString();
}


const fetchData = async () => {
  const params = getParamsFromSearch();
  const indicator = params.indicator;
  if (!indicator) return;

  try {
    const response = await fetch('/api/indicator/detail', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(params)
    });

    if (!response.ok) {
      throw new Error('请求失败');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('获取数据出错:', error);
  }
}

const init = async () => {
  // 1. 从浏览器的search参数中获取indicator参数
  const params = getParamsFromSearch();
  const indicator = params['indicator'];
  const year = params['year'];
  const department = params['出院科室'];
  if (!indicator) return;

  // 2. 在标题处显示indicator参数，并绑定下载按钮
  const indicatorEl = document.getElementById('indicator');
  if (indicatorEl) indicatorEl.textContent = indicator;
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = year;
  const departmentEl = document.getElementById('department');
  if (departmentEl) departmentEl.textContent = department;
  const downloadBtn = document.getElementById('download-btn');
  if (downloadBtn) {
    downloadBtn.onclick = () => {
      const params = getParamsFromSearch();
      const downloadUrl = `/api/indicator/export?${toQuery(params)}`;
      window.open(downloadUrl, "_blank");
    };
  }

  // 3. 根据indicator参数发起请求，获取数据
  const reslut = await fetchData();
  if(!reslut) return;
  const sheet = reslut.sheet;
  if (!sheet) return;

  // 4. 将data渲染到对应的表格中，表格的header为data每一行数据的key
  const detailsEl = document.getElementById('details');
  if (!detailsEl) return;


  const headers = Array.isArray(sheet.headers) ? sheet.headers : [];
  const rows = Array.isArray(sheet.data) ? sheet.data : [];
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

  // 5. 表格放到id为details的元素中
  detailsEl.innerHTML = '';
  detailsEl.appendChild(table);

  // 6. 数据已渲染
}



init()
