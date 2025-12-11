function getParamsFromSearch() {
  const qs = new URLSearchParams(window.location.search);
  const initParams = {};
  qs.forEach((v, k) => {
    if (v !== undefined && v !== null && String(v).trim() !== "") initParams[k] = v;
  });

  return initParams;
}

function updateParamsToSearch() {
  const form = document.getElementById("filter-form");
  const names = [
    "入院日期_start",
    "入院日期_end",
    "出院日期_start",
    "出院日期_end"
  ];
  const params = getParamsFromSearch();
  names.forEach(name => {
    const el = form.querySelector(`[name="${name}"]`);

    if (el && String(el.value || "").trim() !== "") {
      params[name] = el.value
    } else {
      delete params[name];
    }
  });

  const q = toQuery(params);
  const url = `${location.pathname}${q ? `?${q}` : ""}`;
  history.replaceState(null, "", url);
}

function toQuery(params) {
  const usp = new URLSearchParams();
  Object.keys(params).forEach(k => {
    if (params[k] !== undefined && params[k] !== null) usp.set(k, params[k]);
  });
  return usp.toString();
}

async function fetchIndicators() {
  const p = getParamsFromSearch();
  const department = p["department"]
  const year = p["year"]

  const res = await fetch(`/api/indicators`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      department: department,
      year: year
    })
  });
  if (!res.ok) throw new Error("加载指标失败");
  const data = await res.json();
  let list = Array.isArray(data) ? data : [];
  return list;
}

function buildRow(indicatorItem) {
  const tr = document.createElement("tr");
  tr.className = "border-b align-top";
  const tdName = document.createElement("td");
  tdName.className = "px-3 py-2 text-gray-800";
  tdName.textContent = indicatorItem.indicator;
  const tdValue = document.createElement("td");
  tdValue.className = "px-3 py-2 text-sm text-gray-700";
  tdValue.textContent = indicatorItem.number !== undefined ? indicatorItem.number : '--';
  const tdOps = document.createElement("td");
  tdOps.className = "px-3 py-2 space-x-2";


  /** 详情按钮 */
  const btnDetail = document.createElement("button");
  btnDetail.target = "_blank";
  btnDetail.rel = "noopener noreferrer";
  btnDetail.textContent = "详情";
  btnDetail.className = "inline-block px-2 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700";
  btnDetail.addEventListener("click", () => {
    const params = getParamsFromSearch();
    const detailParams = { ...params, indicator: indicatorItem.indicator };
    const detailUrl = `/data?${toQuery(detailParams)}`;
    window.open(detailUrl, "_blank");
  });

  /** 下载按钮 */
  const btnDownload = document.createElement("button");
  btnDownload.target = "_blank";
  btnDownload.rel = "noopener noreferrer";
  btnDownload.textContent = "下载";
  btnDownload.className = "inline-block px-2 py-1 rounded bg-gray-600 text-white hover:bg-gray-700";
  btnDownload.addEventListener("click", () => {
    const params = getParamsFromSearch();
    const downloadParams = { ...params, indicator: indicatorItem.indicator };
    const downloadUrl = `/api/indicator/export?${toQuery(downloadParams)}`;
    window.open(downloadUrl, "_blank");
  });
  
  /** 加载按钮 */
  const btnLoad = document.createElement("button");
  btnLoad.type = "button";
  btnLoad.textContent = "加载";
  btnLoad.className = "inline-block px-2 py-1 rounded bg-blue-600 text-white hover:bg-blue-700";
  btnLoad.addEventListener("click", async () => {
    btnLoad.disabled = true;
    try {
      const params = getParamsFromSearch();
      const detailParams = { ...params, indicator: indicatorItem.indicator };

      const res = await fetch(`/api/indicator/detail`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(detailParams)
      });
      if (!res.ok) throw new Error("加载明细失败");
      const data = await res.json(); 
      const value = data?.value ?? '--';
      tdValue.textContent = value;
    } catch (e) {
      tdValue.textContent = String(e.message || e);
    } finally {
      btnLoad.disabled = false;
    }
  });
  tdOps.appendChild(btnDetail);
  tdOps.appendChild(btnDownload);
  tdOps.appendChild(btnLoad);
  tr.appendChild(tdName);
  tr.appendChild(tdValue);
  tr.appendChild(tdOps);
  return tr;
}

async function renderTable() {

  const tbody = document.getElementById("indicators-tbody");
  tbody.innerHTML = "";
  try {
    const list = await fetchIndicators();
    console.log('list', list);
    if (!list || list.length === 0) {
      const tr = document.createElement("tr");
      const td = document.createElement("td");
      td.colSpan = 3;
      td.className = "px-3 py-2 text-gray-500";
      td.textContent = "暂无数据";
      tr.appendChild(td);
      tbody.appendChild(tr);
      return;
    }
    list.forEach(indicatorItem => {
      const tr = buildRow(indicatorItem);
      tbody.appendChild(tr);
    });
  } catch (e) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 3;
    td.className = "px-3 py-2 text-red-600";
    td.textContent = String(e.message || e);
    tr.appendChild(td);
    tbody.appendChild(tr);
  }
}

window.addEventListener("DOMContentLoaded", () => {

  const initParams =  getParamsFromSearch();
  const form = document.getElementById("filter-form");
  
  Array.from(form.elements).forEach(el => {
    if (!el.name) return;
    if (initParams[el.name] !== undefined) el.value = initParams[el.name];
  });


  const applyBtn = document.getElementById("apply-btn");
  applyBtn.addEventListener("click", () => updateParamsToSearch());

  renderTable()
});
