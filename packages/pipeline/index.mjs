const partKey = (part, color) => `${part.toLowerCase()}|${String(color)}`;
const positive = (value) => Number.isSafeInteger(value) && value >= 0;
const isoDate = (value) => /^\d{4}-\d{2}-\d{2}$/.test(value || "") &&
  !Number.isNaN(Date.parse(`${value}T00:00:00Z`)) && new Date(`${value}T00:00:00Z`).toISOString().slice(0, 10) === value;

export function parseLdrawBom(text) {
  if (typeof text !== "string" || !text.trim()) throw new Error("Choose a non-empty LDraw .ldr or .mpd file.");
  const files = new Map();
  let current = "__root__";
  let firstFile = null;
  files.set(current, []);
  for (const [lineNumber, raw] of text.replace(/^\uFEFF/, "").replaceAll("\r", "").split("\n").entries()) {
    const line = raw.trim();
    const fileMatch = /^0\s+FILE\s+(.+)$/i.exec(line);
    if (fileMatch) {
      current = fileMatch[1].trim().toLowerCase();
      if (!firstFile) firstFile = current;
      if (files.has(current)) throw new Error(`Duplicate submodel name on line ${lineNumber + 1}.`);
      files.set(current, []);
      continue;
    }
    if (/^0\s+NOFILE\b/i.test(line)) { current = null; continue; }
    if (!/^1\s/.test(line)) continue;
    if (current === null) throw new Error(`Part outside a FILE block on line ${lineNumber + 1}.`);
    const fields = line.split(/\s+/);
    if (fields.length < 15 || fields.slice(1, 14).some((value) => !Number.isFinite(Number(value)))) {
      throw new Error(`Invalid LDraw part line ${lineNumber + 1}.`);
    }
    const color = Number(fields[1]);
    if (!positive(color)) throw new Error(`Invalid LDraw colour on line ${lineNumber + 1}.`);
    const part = fields.slice(14).join(" ").replaceAll("\\", "/").toLowerCase();
    files.get(current).push({ color, part });
  }
  const counts = new Map();
  let visits = 0;
  function expand(file, inheritedColor, stack) {
    if (stack.includes(file)) throw new Error(`Recursive LDraw submodel: ${[...stack, file].join(" → ")}.`);
    for (const row of files.get(file)) {
      if (++visits > 100000) throw new Error("Model expands past 100,000 parts; check its submodels.");
      const color = row.color === 16 ? inheritedColor : row.color;
      if (files.has(row.part)) { expand(row.part, color, [...stack, file]); continue; }
      if (/\.(ldr|mpd)$/i.test(row.part)) throw new Error(`Missing submodel ${row.part}.`);
      if (!row.part.endsWith(".dat")) throw new Error(`Unknown LDraw part reference ${row.part}.`);
      if (color === null || color === undefined || color === 16) throw new Error(`Unresolved colour for ${row.part}.`);
      const key = partKey(row.part, color);
      counts.set(key, { part: row.part, color, quantity: (counts.get(key)?.quantity || 0) + 1 });
    }
  }
  expand(firstFile || "__root__", null, []);
  if (!counts.size) throw new Error("The model contains no countable parts.");
  return [...counts.values()].sort((a, b) => partKey(a.part, a.color).localeCompare(partKey(b.part, b.color)));
}

function csvCells(line) {
  const cells = [];
  let cell = "";
  let quoted = false;
  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    if (char === '"') {
      if (quoted && line[i + 1] === '"') { cell += '"'; i++; }
      else quoted = !quoted;
    } else if (char === "," && !quoted) { cells.push(cell.trim()); cell = ""; }
    else cell += char;
  }
  if (quoted) throw new Error("Unclosed quote in parts CSV.");
  cells.push(cell.trim());
  return cells;
}

export function parsePartCountCsv(text) {
  if (typeof text !== "string") throw new Error("Choose a parts CSV.");
  const lines = text.replaceAll("\r", "").split("\n").filter((line) => line.trim());
  if (!lines.length || csvCells(lines[0]).map((cell) => cell.toLowerCase()).join() !== "part,color,quantity") {
    throw new Error("Parts CSV needs the header part,color,quantity.");
  }
  const rows = new Map();
  for (const [index, line] of lines.slice(1).entries()) {
    const [partRaw, colorRaw, quantityRaw, ...extra] = csvCells(line);
    const part = partRaw?.toLowerCase();
    const color = Number(colorRaw);
    const quantity = Number(quantityRaw);
    if (extra.length || !part?.endsWith(".dat") || !positive(color) || !Number.isSafeInteger(quantity) || quantity <= 0) {
      throw new Error(`Invalid parts CSV row ${index + 2}.`);
    }
    const key = partKey(part, color);
    if (rows.has(key)) throw new Error(`Duplicate parts CSV row ${index + 2}.`);
    rows.set(key, { part, color, quantity });
  }
  if (!rows.size) throw new Error("Parts CSV has no parts.");
  return [...rows.values()].sort((a, b) => partKey(a.part, a.color).localeCompare(partKey(b.part, b.color)));
}

export function compareBom(modelRows, checkRows) {
  if (!modelRows?.length || !checkRows?.length) return { matches: false, differences: ["Both parts sources are needed."] };
  const actual = new Map(checkRows.map((row) => [partKey(row.part, row.color), row.quantity]));
  const expected = new Map(modelRows.map((row) => [partKey(row.part, row.color), row.quantity]));
  const differences = [];
  for (const [key, quantity] of expected) {
    if (actual.get(key) !== quantity) differences.push(`${key}: model ${quantity}, check ${actual.get(key) ?? "missing"}`);
  }
  for (const [key, quantity] of actual) {
    if (!expected.has(key)) differences.push(`${key}: model missing, check ${quantity}`);
  }
  return { matches: differences.length === 0, differences };
}

export function calculateGap(bom, inventory = {}) {
  if (!Array.isArray(bom)) throw new Error("Model parts are required.");
  return bom.map((row) => {
    const record = inventory[partKey(row.part, row.color)];
    const counted = record && positive(record.counted) && positive(record.usable) && record.usable <= record.counted &&
      typeof record.evidence === "string" && record.evidence.trim() && typeof record.countedBy === "string" && record.countedBy.trim();
    return { ...row, counted: counted ? record.counted : null, usable: counted ? record.usable : null,
      shortage: counted ? Math.max(0, row.quantity - record.usable) : null, evidence: counted ? record.evidence : null };
  });
}

export function reconcileBuilt(bom, built = {}) {
  return bom.map((row) => {
    const record = built[partKey(row.part, row.color)];
    const recorded = record && positive(record.quantity) && typeof record.evidence === "string" && record.evidence.trim();
    return { ...row, built: recorded ? record.quantity : null, difference: recorded ? record.quantity - row.quantity : null };
  });
}

export function pipelineStatus(run) {
  const bom = run?.model?.rows || [];
  const check = compareBom(bom, run?.check?.rows || []);
  const gap = calculateGap(bom, run?.inventory);
  const built = reconcileBuilt(bom, run?.built);
  const orders = orderSummary(bom, gap, run?.orders, run?.receipts);
  const blockers = [];
  if (!bom.length) blockers.push("Import a model with countable parts.");
  if (bom.length && run.model.archiveTotalParts !== null && run.model.archiveTotalParts !== undefined && run.model.archiveTotalParts !== bom.reduce((sum, row) => sum + row.quantity, 0)) blockers.push("Studio archive total disagrees with the parsed model.");
  if (bom.length && !check.matches) blockers.push(`Cross-check the BOM: ${check.differences.length} difference(s).`);
  if (bom.length && gap.some((row) => row.shortage === null)) blockers.push("Count usable inventory for every model part, including explicit zeroes.");
  if (!run?.fit?.verdict || run.fit.verdict !== "pass" || !run.fit.evidence?.trim() || !run.fit.checkedBy?.trim() || !run.fit.resolution?.trim() || run.fit.modelSha256 !== run.model?.source?.sha256) {
    blockers.push("Record a fit check with a named checker and evidence; Q13 remains open until resolved.");
  }
  return { bom, check, gap, built, orders, blockers,
    reviewReady: blockers.length === 0,
    builtComplete: bom.length > 0 && built.every((row) => row.built !== null && row.difference === 0) };
}

export const keyForPart = partKey;

export function orderSummary(bom, gap, orders = [], receipts = []) {
  return bom.map((row, index) => {
    const key = partKey(row.part, row.color);
    const ordered = orders.flatMap((order) => order.lines || []).filter((line) => partKey(line.part, line.color) === key)
      .reduce((sum, line) => sum + line.quantity, 0);
    const arrived = receipts.flatMap((receipt) => receipt.lines || []).filter((line) => partKey(line.part, line.color) === key)
      .reduce((sum, line) => sum + line.arrived, 0);
    const accepted = receipts.flatMap((receipt) => receipt.lines || []).filter((line) => partKey(line.part, line.color) === key)
      .reduce((sum, line) => sum + line.accepted, 0);
    return { part: row.part, color: row.color, ordered, arrived, accepted,
      stillToOrder: gap[index].shortage === null ? null : Math.max(0, gap[index].shortage - ordered),
      waitingOrRejected: ordered - accepted };
  });
}

export function addRecordedOrder(run, order) {
  if (![order.shop, order.orderNumber, order.placedOn, order.enteredBy, order.evidence].every((value) => typeof value === "string" && value.trim())) {
    throw new Error("Shop, order number, placed date, and recorder are required.");
  }
  if (!isoDate(order.placedOn)) throw new Error("Use a valid order date.");
  if ((run.orders || []).some((entry) => entry.shop === order.shop && entry.orderNumber === order.orderNumber)) {
    throw new Error("That shop and order number are already recorded.");
  }
  if (!Array.isArray(order.lines) || !order.lines.length || order.lines.some((line) =>
    typeof line.part !== "string" || !line.part.toLowerCase().endsWith(".dat") || !positive(line.color) ||
    !Number.isSafeInteger(line.quantity) || line.quantity <= 0) ||
    new Set(order.lines.map((line) => partKey(line.part, line.color))).size !== order.lines.length) {
    throw new Error("Record a positive quantity for at least one model part.");
  }
  return { ...run, orders: [...(run.orders || []), order] };
}

export function addInspection(run, receipt) {
  const order = (run.orders || []).find((entry) => entry.id === receipt.orderId);
  if (!order) throw new Error("Choose a recorded order first.");
  if (!receipt.inspectedBy?.trim() || !receipt.evidence?.trim() || !isoDate(receipt.receivedOn)) {
    throw new Error("Received date, inspector, and evidence are required.");
  }
  if (receipt.receivedOn < order.placedOn) throw new Error("Receipt date cannot precede the order date.");
  const previous = (run.receipts || []).filter((entry) => entry.orderId === order.id);
  const orderByKey = new Map(order.lines.map((line) => [partKey(line.part, line.color), line.quantity]));
  if (!Array.isArray(receipt.lines) || !receipt.lines.length || !receipt.lines.some((line) => line.arrived > 0)) throw new Error("Enter at least one arrived quantity.");
  if (new Set(receipt.lines.map((line) => partKey(line.part, line.color))).size !== receipt.lines.length) throw new Error("A receipt cannot repeat a part line.");
  for (const line of receipt.lines) {
    const key = partKey(line.part, line.color);
    if (!orderByKey.has(key) || !positive(line.arrived) || !positive(line.accepted) || line.accepted > line.arrived) {
      throw new Error(`Invalid received or accepted quantity for ${key}.`);
    }
    const alreadyArrived = previous.flatMap((entry) => entry.lines).filter((entry) => partKey(entry.part, entry.color) === key)
      .reduce((sum, entry) => sum + entry.arrived, 0);
    if (alreadyArrived + line.arrived > orderByKey.get(key)) throw new Error(`Received quantity exceeds the recorded order for ${key}.`);
  }
  return { ...run, receipts: [...(run.receipts || []), receipt] };
}
