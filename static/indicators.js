const qs = new URLSearchParams(window.location.search);
function getParams() {
  const p = {};
  qs.forEach((v, k) => {
    if (v !== undefined && v !== null && String(v).trim() !== "") p[k] = v;
  });
  return p;
}
function setFormFromParams(form, params) {
  Array.from(form.elements).forEach(el => {
    if (!el.name) return;
    if (params[el.name] !== undefined) el.value = params[el.name];
  });
}
function serializeForm(form) {
  const obj = {};
  Array.from(form.elements).forEach(el => {
    if (!el.name) return;
    const v = el.value;
    if (v !== undefined && v !== null && String(v).trim() !== "") obj[el.name] = v;
  });
  return obj;
}
function toQuery(params) {
  const usp = new URLSearchParams();
  Object.keys(params).forEach(k => {
    if (params[k] !== undefined && params[k] !== null) usp.set(k, params[k]);
  });
  return usp.toString();
}
function updateURL(params) {
  const q = toQuery(params);
  const url = `${location.pathname}${q ? `?${q}` : ""}`;
  history.replaceState(null, "", url);
}
function indicatorNameOf(item) {
  if (typeof item === "string") return item;
  if (item === null || item === undefined) return "";
  if (item.name) return item.name;
  if (item.indicator) return item.indicator;
  if (item["指标"]) return item["指标"];
  return String(item);
}
async function fetchIndicators(params) {
  const p = { ...params };
  if (p["出院科室"] && !p.department) p.department = p["出院科室"];
  const query = toQuery(p);
  const res = await fetch(`/api/indicators${query ? `?${query}` : ""}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(p)
  });
  if (!res.ok) throw new Error("加载指标失败");
  const data = await res.json();
  let list = Array.isArray(data) ? data : (data.indicators || data.items || data.data || data.list || data.rows || []);
  if (!Array.isArray(list) && list && typeof list === "object") list = Object.keys(list);
  return list;
}
function buildRow(ind, params) {
  const name = indicatorNameOf(ind);
  const tr = document.createElement("tr");
  tr.className = "border-b align-top";
  const tdName = document.createElement("td");
  tdName.className = "px-3 py-2 text-gray-800";
  tdName.textContent = name;
  const tdValue = document.createElement("td");
  tdValue.className = "px-3 py-2 text-sm text-gray-700";
  const tdOps = document.createElement("td");
  tdOps.className = "px-3 py-2 space-x-2";
  const detailParams = { ...params, indicator: name };
  const detailUrl = `/data?${toQuery(detailParams)}`;
  const downloadUrl = `/api/indicator/export?${toQuery(detailParams)}`;
  const btnDetail = document.createElement("a");
  btnDetail.href = detailUrl;
  btnDetail.target = "_blank";
  btnDetail.rel = "noopener noreferrer";
  btnDetail.textContent = "详情";
  btnDetail.className = "inline-block px-2 py-1 rounded bg-indigo-600 text-white hover:bg-indigo-700";
  const btnDownload = document.createElement("a");
  btnDownload.href = downloadUrl;
  btnDownload.target = "_blank";
  btnDownload.rel = "noopener noreferrer";
  btnDownload.textContent = "下载";
  btnDownload.className = "inline-block px-2 py-1 rounded bg-gray-600 text-white hover:bg-gray-700";
  const btnLoad = document.createElement("button");
  btnLoad.type = "button";
  btnLoad.textContent = "加载";
  btnLoad.className = "inline-block px-2 py-1 rounded bg-blue-600 text-white hover:bg-blue-700";
  btnLoad.addEventListener("click", async () => {
    btnLoad.disabled = true;
    try {
      const query = toQuery(detailParams);
      const res = await fetch(`/api/indicator/detail?${query}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(detailParams)
      });
      if (!res.ok) throw new Error("加载明细失败");
      const data = await res.json(); 
      tdValue.innerHTML = data?.value?.data?.length || '--';
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
async function render() {
  const form = document.getElementById("filter-form");
  const initParams = getParams();
  setFormFromParams(form, initParams);
  const params = serializeForm(form);
  updateURL(params);
  const tbody = document.getElementById("indicators-tbody");
  tbody.innerHTML = "";
  try {
    const list = await fetchIndicators(params);
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
    list.forEach(ind => {
      const tr = buildRow(ind, params);
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
  const form = document.getElementById("filter-form");
  const applyBtn = document.getElementById("apply-btn");
  const resetBtn = document.getElementById("reset-btn");
  applyBtn.addEventListener("click", async () => {
    const params = serializeForm(form);
    updateURL(params);
    await render();
  });
  resetBtn.addEventListener("click", async () => {
    Array.from(form.elements).forEach(el => { if (el.name) el.value = ""; });
    updateURL({});
    await render();
  });
  render();
});
