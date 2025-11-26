const indicators = [
  'abc',
  'def',
];

const handleClick = (e) => {
  const btn = e.target;
  const number = btn.previousElementSibling;
  number.textContent = '123';
}

const init =  () => {
  const app = document.getElementById('app');

  for (const indicator of indicators) {

    const box = document.createElement('div');
    box.classList.add('item');

    const text = document.createElement('span');
    text.classList.add('text');
    text.textContent = indicator;

    const number = document.createElement('span');
    number.classList.add('number');
    number.textContent = '-';

    const btn = document.createElement('button');
    btn.classList.add('btn');
    btn.textContent = '获取数据'; 
    btn.addEventListener('click', handleClick, false);

    const link = document.createElement('a');
    link.classList.add('link');
    link.textContent = '明细页面';
    link.href = '/data?indicator=' + indicator;
    link.target = '_blank';

    box.appendChild(text);
    box.appendChild(number);
    box.appendChild(btn);
    box.appendChild(link);

    app.appendChild(box);
  }
}




init()
