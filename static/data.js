
const fetchData = async (indicator) => {
  try {
    const response = await fetch('/api/get_indicator_data', {
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

  // 2. 在标题处显示indicator参数，并绑定下载按钮
  const indicatorEl = document.getElementById('indicator');
  if (indicatorEl) indicatorEl.textContent = indicator;
  const downloadBtn = document.getElementById('download-btn');
  if (downloadBtn) {
    downloadBtn.onclick = () => {
      const url = `/api/indicator/export?indicator=${encodeURIComponent(indicator)}`;
      window.location.href = url;
    };
  }

  // 3. 根据indicator参数发起请求，获取数据
  const value = await fetchData(indicator);
  if (!value || !Array.isArray(value.data)) return;
  const admitStart = params.get('入院日期_start');
  const admitEnd = params.get('入院日期_end');
  const dischargeStart = params.get('出院日期_start');
  const dischargeEnd = params.get('出院日期_end');
  const dept = params.get('出院科室');
  const year = params.get('year');
  const month = params.get('month');
  const matchAdmission = (row) => {
    if (!admitStart && !admitEnd) return true;
    const v = row['入院日期'];
    if (!v) return false;
    const d = dayjs(String(v));
    if (!d.isValid()) return false;
    if (admitStart && d.isBefore(dayjs(admitStart))) return false;
    if (admitEnd && d.isAfter(dayjs(admitEnd))) return false;
    return true;
  };
  const matchDischarge = (row) => {
    if (!dischargeStart && !dischargeEnd && !year && !month) return true;
    const v = row['出院日期'];
    if (!v) return false;
    const d = dayjs(String(v));
    if (!d.isValid()) return false;
    if (dischargeStart && d.isBefore(dayjs(dischargeStart))) return false;
    if (dischargeEnd && d.isAfter(dayjs(dischargeEnd))) return false;
    if (year && String(d.year()) !== String(year)) return false;
    if (month && String(d.month()+1).padStart(2,'0') !== String(month).padStart(2,'0')) return false;
    return true;
  };
  const filteredRows = value.data.filter(r => {
    if (dept && String(r['出院科室']||'').indexOf(dept) === -1) return false;
    if (!matchAdmission(r)) return false;
    if (!matchDischarge(r)) return false;
    return true;
  });

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
  filteredRows.forEach(row => {
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
