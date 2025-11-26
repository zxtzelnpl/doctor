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
    const len = data.value?.data?.length ?? '-';
    numberSpan.textContent = len;
  } catch (error) {
    console.error('获取数据出错:', error);
    numberSpan.textContent = '获取数据出错';
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

    box.appendChild(text);
    box.appendChild(btn);
    box.appendChild(number);
    box.appendChild(exportBtn);
    box.appendChild(link);

    app.appendChild(box);
  }
}




init()
