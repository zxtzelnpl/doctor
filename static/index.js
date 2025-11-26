const indicators = [
  '24',
  '27',
  'special',
];

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
    // 假设后端返回的数据中，数值字段为 value
    const len = data.value?.length ?? '-';
    numberSpan.textContent = len;
  } catch (error) {
    console.error('获取数据出错:', error);
    numberSpan.textContent = '获取数据出错';
  }
}

const init =  () => {
  const app = document.getElementById('app');

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



    const link = document.createElement('a');
    link.classList.add('link');
    link.textContent = '明细页面';
    link.href = '/data?indicator=' + indicator;
    link.target = '_blank';

    box.appendChild(text);
    box.appendChild(btn);
    box.appendChild(number);
    box.appendChild(link);

    app.appendChild(box);
  }
}




init()
