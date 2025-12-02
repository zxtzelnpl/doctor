const loadIndicators = async () => {
  try {
    const res = await fetch('/api/indicators', { method: 'POST' });
    if (!res.ok) return [];
    const data = await res.json();
    return Array.isArray(data.indicators) ? data.indicators : [];
  } catch {
    return [];
  }
};

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

const fetchIndicatorValue = async (indicator) => {
  const res = await fetch('/api/get_indicator_data', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ indicator })
  });
  if (!res.ok) return null;
  return await res.json();
};

const matchAdmissionDate = (row, start, end) => {
  if (!start && !end) return true;
  const v = row['入院日期'];
  if (!v) return false;
  const d = dayjs(String(v));
  if (!d.isValid()) return false;
  if (start && d.isBefore(dayjs(start))) return false;
  if (end && d.isAfter(dayjs(end))) return false;
  return true;
};

const matchDischargeDate = (row, start, end) => {
  if (!start && !end) return true;
  const v = row['出院日期'];
  if (!v) return false;
  const d = dayjs(String(v));
  if (!d.isValid()) return false;
  if (start && d.isBefore(dayjs(start))) return false;
  if (end && d.isAfter(dayjs(end))) return false;
  return true;
};

const applyFilters = (rows, params) => {
  const admitStart = params.get('入院日期_start');
  const admitEnd = params.get('入院日期_end');
  const dischargeStart = params.get('出院日期_start');
  const dischargeEnd = params.get('出院日期_end');
  const dept = params.get('出院科室');
  return rows.filter(r => {
    if (dept && String(r['出院科室'] || '').indexOf(dept) === -1) return false;
    if (!matchAdmissionDate(r, admitStart, admitEnd)) return false;
    if (!matchDischargeDate(r, dischargeStart, dischargeEnd)) return false;
    return true;
  });
};

const renderActions = (container, indicator, params) => {
  container.innerHTML = '';
  const downloadBtn = document.createElement('button');
  downloadBtn.className = 'px-3 py-1.5 rounded bg-blue-600 text-white hover:bg-blue-700';
  downloadBtn.textContent = '下载当前筛选详情';
  downloadBtn.onclick = () => {
    const u = new URL('/api/indicator/export', window.location.origin);
    u.searchParams.set('indicator', indicator);
    for (const [k,v] of params.entries()) u.searchParams.set(k, v);
    window.location.href = u.toString();
  };
  const detailLink = document.createElement('a');
  detailLink.className = 'px-3 py-1.5 rounded bg-gray-200 text-gray-800 hover:bg-gray-300';
  detailLink.textContent = '打开详情页';
  const u2 = new URL('/data', window.location.origin);
  u2.searchParams.set('indicator', indicator);
  for (const [k,v] of params.entries()) u2.searchParams.set(k, v);
  detailLink.href = u2.toString();
  detailLink.target = '_blank';
  container.appendChild(downloadBtn);
  container.appendChild(detailLink);
};

const renderHierarchy = (container, rows, indicator, baseParams) => {
  container.innerHTML = '';
  const valid = rows.filter(r => dayjs(r['出院日期']).isValid());
  const byYear = _.groupBy(valid, r => dayjs(r['出院日期']).format('YYYY'));
  const years = _.sortBy(_.keys(byYear));
  for (const y of years) {
    const yearDiv = document.createElement('div');
    yearDiv.className = 'border rounded p-3';
    const top = document.createElement('div');
    top.className = 'flex items-center gap-3';
    const title = document.createElement('span');
    title.textContent = `${y} 年：${byYear[y].length}`;
    top.appendChild(title);
    const yearParams = new URLSearchParams(baseParams.toString());
    yearParams.set('year', y);
    const yearDownload = document.createElement('button');
    yearDownload.className = 'px-2 py-1 rounded bg-blue-600 text-white';
    yearDownload.textContent = '下载详情';
    yearDownload.onclick = () => {
      const u = new URL('/api/indicator/export', window.location.origin);
      u.searchParams.set('indicator', indicator);
      for (const [k,v] of yearParams.entries()) u.searchParams.set(k, v);
      window.location.href = u.toString();
    };
    const yearLink = document.createElement('a');
    yearLink.className = 'px-2 py-1 rounded bg-gray-200 text-gray-800';
    yearLink.textContent = '详情页面';
    const u2 = new URL('/data', window.location.origin);
    u2.searchParams.set('indicator', indicator);
    for (const [k,v] of yearParams.entries()) u2.searchParams.set(k, v);
    yearLink.href = u2.toString();
    yearLink.target = '_blank';
    top.appendChild(yearDownload);
    top.appendChild(yearLink);
    yearDiv.appendChild(top);
    const months = _.sortBy(_.keys(_.groupBy(byYear[y], r => dayjs(r['出院日期']).format('MM'))));
    const list = document.createElement('ul');
    list.className = 'mt-2 grid grid-cols-2 md:grid-cols-4 gap-2';
    const monthCount = _.countBy(byYear[y], r => dayjs(r['出院日期']).format('MM'));
    for (const m of months) {
      const li = document.createElement('li');
      li.className = 'flex items-center gap-2';
      const tag = document.createElement('span');
      tag.textContent = `${m} 月：${monthCount[m]}`;
      const monthParams = new URLSearchParams(yearParams.toString());
      monthParams.set('month', m);
      const monthDownload = document.createElement('button');
      monthDownload.className = 'px-2 py-1 rounded bg-blue-600 text-white';
      monthDownload.textContent = '下载详情';
      monthDownload.onclick = () => {
        const u = new URL('/api/indicator/export', window.location.origin);
        u.searchParams.set('indicator', indicator);
        for (const [k,v] of monthParams.entries()) u.searchParams.set(k, v);
        window.location.href = u.toString();
      };
      const monthLink = document.createElement('a');
      monthLink.className = 'px-2 py-1 rounded bg-gray-200 text-gray-800';
      monthLink.textContent = '详情页面';
      const u3 = new URL('/data', window.location.origin);
      u3.searchParams.set('indicator', indicator);
      for (const [k,v] of monthParams.entries()) u3.searchParams.set(k, v);
      monthLink.href = u3.toString();
      monthLink.target = '_blank';
      li.appendChild(tag);
      li.appendChild(monthDownload);
      li.appendChild(monthLink);
      list.appendChild(li);
    }
    yearDiv.appendChild(list);
    container.appendChild(yearDiv);
  }
};

const init = async () => {
  const form = document.getElementById('filter-form');
  const actions = document.getElementById('actions');
  const tree = document.getElementById('tree');
  const applyBtn = document.getElementById('apply-btn');
  const resetBtn = document.getElementById('reset-btn');
  const indicatorSelect = document.getElementById('indicator-select');
  const indicators = await loadIndicators();
  indicatorSelect.innerHTML = '';
  for (const name of indicators) {
    const opt = document.createElement('option');
    opt.value = name;
    opt.textContent = name;
    indicatorSelect.appendChild(opt);
  }
  const currentParams = new URLSearchParams(window.location.search);
  applyParamsToForm(form, currentParams);
  const load = async () => {
    const indicator = new FormData(form).get('indicator') || indicatorSelect.value || '';
    if (!indicator) return;
    const res = await fetchIndicatorValue(indicator);
    if (!res || !Array.isArray(res.value?.data)) return;
    const rows = applyFilters(res.value.data, currentParams);
    renderActions(actions, indicator, currentParams);
    renderHierarchy(tree, rows, indicator, currentParams);
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
  await load();
};

init();
