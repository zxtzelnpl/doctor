const allowedYears = ['2022','2023','2024','2025'];

const loadDepartments = async (year) => {
  if (!year || !allowedYears.includes(String(year))) return [];
  try {
    const cached = localStorage.getItem(`departments:${year}`);
    if (cached) {
      const arr = JSON.parse(cached);
      if (Array.isArray(arr) && arr.length) return arr;
    }
  } catch {}
  try {
    const res = await fetch('/api/department/list', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ year }) });
    if (!res.ok) return [];
    const data = await res.json();
    const depts = Array.isArray(data.departments) ? data.departments : [];
    try { localStorage.setItem(`departments:${year}`, JSON.stringify(depts)); } catch {}
    return depts;
  } catch {
    return [];
  }
};

const renderCards = (root, departments, year) => {
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
      u.searchParams.set('department', name);
      if (year) u.searchParams.set('year', year);
      window.open(u.toString(), '_blank');
    };
    grid.appendChild(card);
  }
  root.appendChild(grid);
};

const init = async () => {
  const app = document.getElementById('app');
  const yearSelect = document.getElementById('year-select');
  const params = new URLSearchParams(window.location.search);
  const yearFromUrl = params.get('year');
  if (allowedYears.includes(String(yearFromUrl))) yearSelect.value = yearFromUrl;
  const load = async () => {
    const y = new URLSearchParams(window.location.search).get('year');
    if (!y || !allowedYears.includes(String(y))) { renderCards(app, [], y); return; }
    const departments = await loadDepartments(y);
    renderCards(app, departments, y);
  };
  yearSelect.onchange = async () => {
    const y = yearSelect.value;
    const u = new URL(window.location.href);
    if (y) u.searchParams.set('year', y); else u.searchParams.delete('year');
    window.history.pushState({}, '', u.toString());
    await load();
  };
  await load();

  const depLinks = document.getElementById('departments').querySelectorAll('a');
  depLinks.forEach(link => {
    link.onclick = (e) => {
      e.preventDefault();
      const y = yearSelect.value;
      const d = link.textContent.trim();
      if (y) {
        
        const u = new URL('/indicators', window.location.origin);
        u.searchParams.set('year', y);
        u.searchParams.set('department', d);
        window.open(u.toString(), '_blank');
      }
    };
  });
};

init();
