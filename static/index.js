const loadDepartments = async () => {
  try {
    const cached = localStorage.getItem('departments');
    if (cached) {
      const arr = JSON.parse(cached);
      if (Array.isArray(arr) && arr.length) return arr;
    }
  } catch {}
  try {
    const res = await fetch('/api/department/list', { method: 'POST' });
    if (!res.ok) return [];
    const data = await res.json();
    const depts = Array.isArray(data.departments) ? data.departments : [];
    try { localStorage.setItem('departments', JSON.stringify(depts)); } catch {}
    return depts;
  } catch {
    return [];
  }
};

const renderCards = (root, departments) => {
  root.innerHTML = '';
  const grid = document.createElement('div');
  grid.className = 'card-grid';
  if (!departments.length) {
    const empty = document.createElement('div');
    empty.className = 'empty';
    empty.textContent = '暂无科室数据';
    root.appendChild(empty);
    return;
  }
  for (const name of departments) {
    const card = document.createElement('div');
    card.className = 'card';
    const title = document.createElement('div');
    title.className = 'card-title';
    title.textContent = name;
    card.appendChild(title);
    card.onclick = () => {
      const u = new URL('/indicators', window.location.origin);
      u.searchParams.set('出院科室', name);
      window.location.href = u.toString();
    };
    grid.appendChild(card);
  }
  root.appendChild(grid);
};

const init = async () => {
  const app = document.getElementById('app');
  const departments = await loadDepartments();
  renderCards(app, departments);
};

init();
