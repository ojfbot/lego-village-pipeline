import { parseLdrawBom, parsePartCountCsv, pipelineStatus, keyForPart, addRecordedOrder, addInspection } from "/pipeline/index.mjs";

const storageKey = "drafting-table-pipeline:v1";
const $ = (selector) => document.querySelector(selector);
const make = (tag, text, className) => {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
};
let run;
try { run = JSON.parse(localStorage.getItem(storageKey)) || {}; } catch { run = {}; }
if (!run || typeof run !== "object" || Array.isArray(run)) run = {};

function announce(message) { $("#pipeline-announcement").textContent = message; }
function save() {
  try { localStorage.setItem(storageKey, JSON.stringify(run)); }
  catch { announce("This browser could not save the run. Download the review packet before closing it."); }
}
function sourceLine(source) { return source ? `${source.name} · SHA-256 ${source.sha256}` : "No source loaded."; }
async function fileSource(file) {
  const bytes = await file.arrayBuffer();
  const digest = await crypto.subtle.digest("SHA-256", bytes);
  return { name: file.name, sha256: [...new Uint8Array(digest)].map((n) => n.toString(16).padStart(2, "0")).join(""),
    recordedAt: new Date().toISOString() };
}
function appendTable(target, headers, rows) {
  const table = make("table");
  const thead = make("thead");
  const heading = make("tr");
  for (const title of headers) heading.append(make("th", title));
  thead.append(heading);
  const tbody = make("tbody");
  for (const values of rows) {
    const tr = make("tr");
    for (const value of values) tr.append(make("td", String(value)));
    tbody.append(tr);
  }
  table.append(thead, tbody);
  target.append(table);
}
function field(labelText, type, id, value, min) {
  const wrap = make("div", undefined, "entry-field");
  const label = make("label", labelText);
  label.htmlFor = id;
  const input = make("input");
  input.type = type;
  input.id = id;
  input.value = value ?? "";
  if (min !== undefined) input.min = String(min);
  if (type === "number") input.step = "1";
  wrap.append(label, input);
  return wrap;
}
function partEntry(row, index, kind) {
  const key = keyForPart(row.part, row.color);
  const old = kind === "inventory" ? run.inventory?.[key] : run.built?.[key];
  const box = make("fieldset", undefined, "part-entry");
  box.dataset.partKey = key;
  const legend = make("legend", `${row.part} · colour ${row.color} · model needs ${row.quantity}`);
  box.append(legend);
  if (kind === "inventory") {
    box.append(field("Counted", "number", `counted-${index}`, old?.counted, 0));
    box.append(field("Usable", "number", `usable-${index}`, old?.usable, 0));
    box.append(field("Count evidence / location", "text", `inv-evidence-${index}`, old?.evidence));
  } else {
    box.append(field("Installed", "number", `built-${index}`, old?.quantity, 0));
    box.append(field("Build evidence / note", "text", `built-evidence-${index}`, old?.evidence));
  }
  return box;
}
function renderOrderRecord(status) {
  const orderRows = $("#order-rows");
  orderRows.replaceChildren();
  for (const [index, row] of status.bom.entries()) {
    const box = make("div", undefined, "order-entry");
    box.append(field(`${row.part} · colour ${row.color} · quantity ordered`, "number", `order-qty-${index}`, "", 0));
    orderRows.append(box);
  }
  const result = $("#order-result");
  result.replaceChildren();
  if (!run.orders?.length) result.append(make("p", "No outside orders recorded. Recording one does not change usable inventory."));
  if (status.bom.length) {
    appendTable(result, ["Part", "Colour", "Ordered", "Awaiting", "Arrived", "Accepted", "Rejected"], status.orders.map((row) =>
      [row.part, row.color, row.ordered, row.awaiting, row.arrived, row.accepted, row.rejected]));
  }
  for (const order of run.orders || []) {
    const article = make("article", undefined, "order-card");
    article.append(make("h3", `${order.shop} · ${order.orderNumber}`));
    article.append(make("p", `Placed ${order.placedOn}. Entered by ${order.enteredBy} on ${new Date(order.enteredAt).toLocaleString()}. Evidence: ${order.evidence}. Ordered is not usable stock.`));
    appendTable(article, ["Part", "Colour", "Ordered"], order.lines.map((line) => [line.part, line.color, line.quantity]));
    const receipts = (run.receipts || []).filter((receipt) => receipt.orderId === order.id);
    for (const receipt of receipts) article.append(make("p", `Inspected ${receipt.receivedOn} by ${receipt.inspectedBy}: ${receipt.lines.map((line) => `${line.part} colour ${line.color}, ${line.arrived} arrived, ${line.accepted} accepted`).join("; ")}. Evidence: ${receipt.evidence}.`));
    const form = make("form", undefined, "receipt-form input-card");
    form.dataset.orderId = order.id;
    const title = make("h4", "Receive and inspect this order");
    form.append(title);
    const date = field("Received on", "date", `received-date-${order.id}`, "");
    const inspector = field("Inspected by", "text", `inspector-${order.id}`, "");
    const evidence = field("Receipt / inspection evidence", "text", `receipt-evidence-${order.id}`, "");
    form.append(date, inspector, evidence);
    for (const [index, line] of order.lines.entries()) {
      const group = make("fieldset", undefined, "part-entry receipt-line");
      group.dataset.part = line.part;
      group.dataset.color = String(line.color);
      group.append(make("legend", `${line.part} · colour ${line.color} · ordered ${line.quantity}`));
      group.append(field("Arrived", "number", `arrived-${order.id}-${index}`, "", 0));
      group.append(field("Accepted after inspection", "number", `accepted-${order.id}-${index}`, "", 0));
      form.append(group);
    }
    const button = make("button", "Record inspection");
    button.type = "submit";
    form.append(button);
    form.addEventListener("submit", recordInspection);
    article.append(form);
    result.append(article);
  }
}

function recordInspection(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const orderId = form.dataset.orderId;
  const lines = [];
  for (const group of form.querySelectorAll(".receipt-line")) {
    const [arrivedInput, acceptedInput] = group.querySelectorAll("input");
    if (!arrivedInput.value.trim() && !acceptedInput.value.trim()) continue;
    lines.push({ part: group.dataset.part, color: Number(group.dataset.color),
      arrived: Number(arrivedInput.value), accepted: Number(acceptedInput.value) });
  }
  const receipt = { id: crypto.randomUUID(), orderId, receivedOn: form.querySelector('input[type="date"]').value,
    inspectedBy: form.querySelector(`#inspector-${orderId}`).value.trim(),
    evidence: form.querySelector(`#receipt-evidence-${orderId}`).value.trim(),
    lines, enteredAt: new Date().toISOString() };
  try { run = addInspection(run, receipt); save(); render(); announce("Inspected receipt recorded. Recount inventory before treating accepted pieces as usable."); }
  catch (error) { announce(error.message); }
}

function render() {
  const status = pipelineStatus(run);
  const modelRows = status.bom;
  $("#run-summary").textContent = modelRows.length
    ? `${modelRows.length} distinct part/colour ${modelRows.length === 1 ? "row" : "rows"} · ${status.blockers.length} open review blocker${status.blockers.length === 1 ? "" : "s"}.`
    : "Bring the real model and counted parts. Each step keeps its source attached.";
  $("#model-source").textContent = run.model ? sourceLine(run.model.source) : "No model loaded.";
  $("#check-source").textContent = run.check
    ? `${sourceLine(run.check.source)} · ${run.check.method || "Method missing"} · evidence ${run.check.evidence || "missing"} · checked by ${run.check.checkedBy || "unknown"} · ${run.checkHistory?.length || 0} earlier comparison(s) kept`
    : "No comparison loaded.";
  $("#check-method").value = run.check?.method || "";
  $("#check-evidence").value = run.check?.evidence || "";
  $("#check-person").value = run.check?.checkedBy || "";
  $("#prior-runs").textContent = run.priorRuns?.length ? `${run.priorRuns.length} earlier model run(s) are preserved in the downloaded packet.` : "No earlier model run in this browser.";
  const bom = $("#bom-result");
  bom.replaceChildren();
  if (!modelRows.length) bom.append(make("p", "No BOM yet. Import a model to start the run."));
  else {
    bom.append(make("h3", `${modelRows.length} part/colour ${modelRows.length === 1 ? "row" : "rows"} · ${modelRows.reduce((sum, row) => sum + row.quantity, 0)} pieces`));
    if (run.model.archiveTotalParts !== null && run.model.archiveTotalParts !== undefined) bom.append(make("p", `Studio archive reports ${run.model.archiveTotalParts} total parts; model parser counted ${modelRows.reduce((sum, row) => sum + row.quantity, 0)}. This is an internal consistency check.`));
    const countFinding = !run.check ? "A separate parts count is still needed to cross-check this BOM."
      : !status.check.matches ? `Counts differ: ${status.check.differences.join("; ")}`
      : !run.check.method?.trim() || !run.check.checkedBy?.trim() || !run.check.evidence?.trim() ||
        run.check.modelSha256 !== run.model.source.sha256
        ? "Counts match, but this comparison lacks a source method, evidence, or a checker tied to this model."
        : "Separate sourced count agrees, row for row.";
    bom.append(make("p", countFinding));
    appendTable(bom, ["Part", "Colour", "Model quantity"], modelRows.map((row) => [row.part, row.color, row.quantity]));
  }
  const inventoryRows = $("#inventory-rows");
  inventoryRows.replaceChildren();
  const builtRows = $("#built-rows");
  builtRows.replaceChildren();
  for (const [index, row] of modelRows.entries()) {
    inventoryRows.append(partEntry(row, index, "inventory"));
    builtRows.append(partEntry(row, index, "built"));
  }
  if (!modelRows.length) {
    inventoryRows.append(make("p", "Import the model first; the count sheet will use its exact parts."));
    builtRows.append(make("p", "Import the model first; the build record will use its exact parts."));
  }
  $("#inventory-counter").value = run.inventoryCounter || "";
  $("#fit-verdict").value = run.fit?.verdict || "block";
  $("#fit-resolution").value = run.fit?.resolution || "";
  $("#fit-evidence").value = run.fit?.evidence || "";
  $("#fit-checker").value = run.fit?.checkedBy || "";
  $("#fit-result").textContent = run.fit?.verdict === "pass"
    ? `Human fit check recorded by ${run.fit.checkedBy}. Geometry automation remains unverified.`
    : "Fit is blocked or unverified. Q13's centered inner-corner overlap remains open.";
  const known = status.gap.filter((row) => row.shortage !== null);
  $("#inventory-result").textContent = modelRows.length
    ? `${known.length} of ${modelRows.length} part/colour rows have an evidenced physical count. ${run.inventoryHistory?.length || 0} earlier count(s) kept in the packet.`
    : "No part counts can be entered until a model is loaded.";
  const gap = $("#gap-result");
  gap.replaceChildren();
  if (!modelRows.length) gap.append(make("p", "No model means no shortage calculation."));
  else {
    gap.append(make("h3", status.reviewReady ? "Evidence complete for operator review" : "Review blocked"));
    if (status.blockers.length) {
      const list = make("ul");
      for (const blocker of status.blockers) list.append(make("li", blocker));
      gap.append(list);
    } else gap.append(make("p", "All entered sources agree. This is still not a purchase release or vendor-ready order."));
    appendTable(gap, ["Part", "Colour", "Need", "Usable", "Gap"], status.gap.map((row) =>
      [row.part, row.color, row.quantity, row.usable ?? "Unknown", row.shortage ?? "Unknown"]));
  }
  renderOrderRecord(status);
  const built = $("#built-result");
  built.replaceChildren();
  if (!modelRows.length) built.append(make("p", "No build record yet."));
  else {
    built.append(make("p", status.builtComplete ? "Every installed count matches the model. The entered evidence remains part of this local record." :
      "Enter installed counts with evidence. Blank rows remain unknown, not zero."));
    appendTable(built, ["Part", "Colour", "Model", "Installed", "Difference"], status.built.map((row) =>
      [row.part, row.color, row.quantity, row.built ?? "Unknown", row.difference ?? "Unknown"]));
  }
}

$("#load-model").addEventListener("click", async () => {
  const file = $("#model-file").files[0];
  if (!file || !/\.(io|ldr|mpd)$/i.test(file.name)) { announce("Choose a Studio .io or LDraw .ldr/.mpd model first."); return; }
  try {
    let modelText;
    let archiveTotalParts = null;
    if (/\.io$/i.test(file.name)) {
      const response = await fetch("/studio-model", { method: "POST", headers: { "content-type": "application/octet-stream" }, body: await file.arrayBuffer() });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || "Could not read Studio archive.");
      modelText = result.model;
      archiveTotalParts = result.archiveTotalParts;
    } else modelText = await file.text();
    const rows = parseLdrawBom(modelText);
    const source = await fileSource(file);
    if (run.model?.source?.sha256 !== source.sha256 && run.model) {
      run.priorRuns = [...(run.priorRuns || []), { ...run, priorRuns: undefined }];
      run.check = undefined; run.checkHistory = undefined; run.inventory = undefined;
      run.inventoryHistory = undefined; run.inventoryCounter = undefined; run.fit = undefined; run.built = undefined;
    }
    if (!run.model) run.fit = undefined;
    run.model = { source, rows, archiveTotalParts };
    save(); render();
    announce(`Counted ${rows.reduce((sum, row) => sum + row.quantity, 0)} model pieces. A different model starts a new run and preserves the prior local record.`);
  } catch (error) { announce(`Could not count model: ${error.message}`); }
});

$("#load-check").addEventListener("click", async () => {
  const file = $("#check-file").files[0];
  if (!run.model) { announce("Load a model before comparing its parts."); return; }
  if (!file) { announce("Choose a parts CSV to compare."); return; }
  const method = $("#check-method").value.trim();
  const evidence = $("#check-evidence").value.trim();
  const checkedBy = $("#check-person").value.trim();
  if (!method || !evidence || !checkedBy) {
    announce("Record the separate count method, evidence, and checker before comparing."); return;
  }
  try {
    const rows = parsePartCountCsv(await file.text());
    const nextCheck = { source: await fileSource(file), rows, method, evidence, checkedBy,
      modelSha256: run.model.source.sha256, recordedAt: new Date().toISOString() };
    if (run.check) run.checkHistory = [...(run.checkHistory || []), run.check];
    run.check = nextCheck;
    save(); render();
    const status = pipelineStatus(run);
    announce(status.check.matches ? "Separate parts count matches the model rows; its recorded method is available for review." :
      `Parts count differs in ${status.check.differences.length} row(s). Read the differences before continuing.`);
  } catch (error) { announce(`Could not compare parts: ${error.message}`); }
});

$("#fit-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (!run.model) { announce("Import the layout model before recording its fit check."); return; }
  const verdict = $("#fit-verdict").value;
  const resolution = $("#fit-resolution").value.trim();
  const evidence = $("#fit-evidence").value.trim();
  const checkedBy = $("#fit-checker").value.trim();
  if (verdict === "pass" && (!resolution || !evidence || !checkedBy)) {
    announce("To record a fit pass, name the Q13 resolution, evidence, and checker."); return;
  }
  run.fit = { verdict, resolution, evidence, checkedBy, modelSha256: run.model.source.sha256, recordedAt: new Date().toISOString() };
  save(); render(); announce(verdict === "pass" ? "Human fit finding recorded with its source; no automated geometry pass is claimed." : "Fit remains blocked.");
});

$("#inventory-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (!run.model) { announce("Import a model before counting inventory."); return; }
  const countedBy = $("#inventory-counter").value.trim();
  if (!countedBy) { announce("Enter who counted the parts."); return; }
  const next = { ...(run.inventory || {}) };
  const previous = [];
  for (const [index, row] of run.model.rows.entries()) {
    const countedText = $(`#counted-${index}`).value.trim();
    const usableText = $(`#usable-${index}`).value.trim();
    const evidence = $(`#inv-evidence-${index}`).value.trim();
    if (!countedText && !usableText && !evidence) continue;
    const counted = Number(countedText), usable = Number(usableText);
    if (!countedText || !usableText || !Number.isSafeInteger(counted) || !Number.isSafeInteger(usable) ||
        counted < 0 || usable < 0 || usable > counted || !evidence) {
      announce(`Fix the physical count, usable count, and evidence for ${row.part} colour ${row.color}.`); return;
    }
    const key = keyForPart(row.part, row.color);
    const old = next[key];
    if (old?.counted === counted && old?.usable === usable && old?.evidence === evidence && old?.countedBy === countedBy) continue;
    if (old) previous.push({ key, record: old, supersededAt: new Date().toISOString() });
    next[key] = { counted, usable, evidence, countedBy, recordedAt: new Date().toISOString() };
  }
  run.inventoryHistory = [...(run.inventoryHistory || []), ...previous];
  run.inventory = next; run.inventoryCounter = countedBy;
  save(); render(); announce("Physical inventory counts recorded. Missing rows remain unknown.");
});

$("#order-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const lines = [];
  for (const [index, row] of (run.model?.rows || []).entries()) {
    const value = $(`#order-qty-${index}`).value.trim();
    if (value) lines.push({ part: row.part, color: row.color, quantity: Number(value) });
  }
  const otherPart = $("#other-part").value.trim().toLowerCase();
  const otherColor = $("#other-color").value.trim();
  const otherQty = $("#other-qty").value.trim();
  if (otherPart || otherColor || otherQty) {
    if (!otherPart || !otherColor || !otherQty) { announce("Complete the other part ID, colour, and quantity together."); return; }
    lines.push({ part: otherPart, color: Number(otherColor), quantity: Number(otherQty) });
  }
  const order = { id: crypto.randomUUID(), shop: $("#order-shop").value.trim(),
    orderNumber: $("#order-number").value.trim(), placedOn: $("#order-date").value,
    enteredBy: $("#order-recorder").value.trim(), evidence: $("#order-evidence").value.trim(),
    lines, enteredAt: new Date().toISOString(), provenance: "entered after outside purchase" };
  try { run = addRecordedOrder(run, order); save(); render(); announce("Outside order recorded. No parts became usable or built."); }
  catch (error) { announce(error.message); }
});

$("#built-form").addEventListener("submit", (event) => {
  event.preventDefault();
  if (!run.model) { announce("Import a model before recording the build."); return; }
  const next = { ...(run.built || {}) };
  for (const [index, row] of run.model.rows.entries()) {
    const quantityText = $(`#built-${index}`).value.trim();
    const evidence = $(`#built-evidence-${index}`).value.trim();
    if (!quantityText && !evidence) continue;
    const quantity = Number(quantityText);
    if (!quantityText || !Number.isSafeInteger(quantity) || quantity < 0 || !evidence) {
      announce(`Fix the installed count and evidence for ${row.part} colour ${row.color}.`); return;
    }
    next[keyForPart(row.part, row.color)] = { quantity, evidence, recordedAt: new Date().toISOString() };
  }
  run.built = next; save(); render(); announce("Built counts recorded. Differences from the model remain visible.");
});

$("#download-packet").addEventListener("click", () => {
  const status = pipelineStatus(run);
  const packet = { kind: "draft-review-packet", generatedAt: new Date().toISOString(), designPin: "H-01 R1 as-committed",
    sourceNote: "Local user-entered evidence; no purchasing authority", run, derived: status };
  const blob = new Blob([JSON.stringify(packet, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = make("a");
  link.href = url; link.download = "draft-village-review-packet.json";
  document.body.append(link); link.click(); link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  announce("Draft review packet downloaded. Open blockers and source fingerprints are included.");
});

render();
