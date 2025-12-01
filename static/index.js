const loadIndicators = async () => {
  try {
    const res = await fetch('/api/indicators');
    if (!res.ok) return [];
    const data = await res.json();
    return Array.isArray(data.indicators) ? data.indicators : [];
  } catch {
    return [];
  }
};

const createExportHandler = (indicator) => () => {
  const url = `/api/indicator/export?indicator=${encodeURIComponent(indicator)}`;
  const a = document.createElement('a');
  a.href = url;
  a.download = '';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

const handleClick = async (e) => {
  const btn = e.target;
  const text = btn.previousElementSibling.textContent;
  const numberSpan = btn.nextElementSibling;
  const details = btn.parentElement.querySelector('.details');

  try {
    const response = await fetch('/api/indicator', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ indicator: text })
    });

    if (!response.ok) {
      throw new Error('请求失败');
    }

    const data = await response.json();
    const rows = Array.isArray(data.value?.data) ? data.value.data : [];
    const len = rows.length;
    numberSpan.textContent = len;
    renderHierarchy(details, rows);
  } catch (error) {
    console.error('获取数据出错:', error);
    numberSpan.textContent = '获取数据出错';
    if (details) details.textContent = '加载失败';
  }
}

const init =  async () => {
  const app = document.getElementById('app');

  const indicators = await loadIndicators();
  for (const indicator of indicators) {

    const box = document.createElement('div');
    box.classList.add('item');

    const text = document.createElement('span');
    text.classList.add('text');
    text.textContent = indicator;

    const btn = document.createElement('button');
    btn.classList.add('btn');
    btn.textContent = '获取数据'; 
    btn.addEventListener('click', handleClick, false);

    const number = document.createElement('span');
    number.classList.add('number');
    number.textContent = '-';

    const exportBtn = document.createElement('button');
    exportBtn.classList.add('export-btn');
    exportBtn.textContent = '导出Excel';
    exportBtn.addEventListener('click', createExportHandler(indicator), false);
    const link = document.createElement('a');
    link.classList.add('link');
    link.textContent = '明细页面';
    link.href = '/data?indicator=' + encodeURIComponent(indicator);
    link.target = '_blank';

    const details = document.createElement('div');
    details.classList.add('details');

    box.appendChild(text);
    box.appendChild(btn);
    box.appendChild(number);
    box.appendChild(exportBtn);
    box.appendChild(link);
    box.appendChild(details);

    app.appendChild(box);
  }
}




 

const parseYearMonth = (str) => {
  if (typeof str !== 'string') return { year: '', month: '' };
  const d = dayjs(str);
  if (!d.isValid()) return { year: '', month: '' };
  const y = String(d.year());
  const m = String(d.month() + 1).padStart(2, '0');
  return { year: y, month: m };
}

const renderHierarchy = (container, rows) => {
  if (!container) return;
  container.innerHTML = '';
  const byDept = _.groupBy(rows, '出院科室');
  const depts = _.keys(byDept).sort((a, b) => a.localeCompare(b, 'zh-Hans-CN'));
  for (const dept of depts) {
    const deptWrap = document.createElement('div');
    deptWrap.classList.add('dept');
    const header = document.createElement('div');
    header.classList.add('dept-header');
    const title = document.createElement('span');
    title.textContent = dept || '未分科室';
    const total = document.createElement('span');
    total.classList.add('dept-total');
    total.textContent = `总数：${byDept[dept].length}`;
    header.appendChild(title);
    header.appendChild(total);
    const ul = document.createElement('ul');
    ul.classList.add('tree');
    const valid = byDept[dept].filter(r => {
      const d = dayjs(r?.['出院日期']);
      return d.isValid();
    });
    const byYear = _.groupBy(valid, r => dayjs(r['出院日期']).format('YYYY'));
    const years = _.sortBy(_.keys(byYear));
    for (const y of years) {
      const li = document.createElement('li');
      li.classList.add('year');
      const monthCount = _.countBy(byYear[y], r => dayjs(r['出院日期']).format('MM'));
      const months = _.sortBy(_.keys(monthCount));
      const yearCount = _.sum(_.values(monthCount));
      const yearText = document.createElement('span');
      yearText.textContent = `${y}：${yearCount}`;
      li.appendChild(yearText);
      const monthUl = document.createElement('ul');
      monthUl.classList.add('months');
      for (const m of months) {
        const mli = document.createElement('li');
        const tag = document.createElement('span');
        tag.classList.add('tag');
        tag.textContent = `${m}月：${monthCount[m]}`;
        mli.appendChild(tag);
        monthUl.appendChild(mli);
      }
      li.appendChild(monthUl);
      ul.appendChild(li);
    }
    deptWrap.appendChild(header);
    deptWrap.appendChild(ul);
    container.appendChild(deptWrap);
  }
}

init()
