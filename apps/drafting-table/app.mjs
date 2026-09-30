import {
  STORAGE_VERSION,
  changeDisposition,
  normalizeDispositions,
  prioritySummary,
  validateHubFixture,
} from "/schema/index.mjs";

const storageKey = "drafting-table-demo:v1";
const sessionKey = "drafting-table-demo:session";
const list = document.querySelector("#priority-list");
const lede = document.querySelector("#lede");
const announcements = document.querySelector("#announcements");
const themeButton = document.querySelector("#theme-toggle");
const treeRecord = document.querySelector("#tree-record");
const photoGallery = document.querySelector("#photo-gallery");

function makeSessionId() {
  try {
    let id = sessionStorage.getItem(sessionKey);
    if (!id) {
      id = crypto.randomUUID();
      sessionStorage.setItem(sessionKey, id);
    }
    return id;
  } catch {
    return crypto.randomUUID();
  }
}

const sessionId = makeSessionId();
let fixture;
let state = {};

function readSavedState() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "null");
    return normalizeDispositions(saved, fixture.priorities, sessionId);
  } catch {
    return {};
  }
}

function saveState() {
  try {
    localStorage.setItem(storageKey, JSON.stringify({ version: STORAGE_VERSION, items: state }));
    return true;
  } catch {
    return false;
  }
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function actionButton(label, fullLabel, priorityId, action, onClick) {
  const button = element("button", "", label);
  button.type = "button";
  button.setAttribute("aria-label", fullLabel);
  button.dataset.priorityId = priorityId;
  button.dataset.action = action;
  button.addEventListener("click", onClick);
  return button;
}

function setPriority(id, disposition, action) {
  state = changeDisposition(state, id, disposition, sessionId, fixture.priorities);
  const stored = saveState();
  const priority = fixture.priorities.find((item) => item.id === id);
  render();
  const target = list.querySelector(`button[data-priority-id="${id}"][data-action="${disposition === "open" ? action : "undo"}"]`);
  target?.focus();
  if (disposition === "done") announcements.textContent = `${priority.title} marked done in this demo only. ${priority.unlocks}`;
  else if (disposition === "parked") announcements.textContent = `${priority.title} parked for this session. It returns next session.`;
  else announcements.textContent = `${priority.title} is back on the list.`;
  if (!stored) announcements.textContent += " This browser did not save the change.";
}

function renderPriority(priority, index, currentId) {
  const status = state[priority.id]?.status || "open";
  const card = element("li", "priority");
  card.dataset.status = status;
  card.dataset.current = String(status === "open" && priority.id === currentId);
  card.append(element("span", "priority-number", status === "done" ? "✓" : status === "parked" ? "○" : String(index + 1)));
  card.append(element("p", "priority-meta", status === "done" ? "Done" : status === "parked" ? "Parked for this session" : priority.effort_label));
  card.append(element("h3", "", priority.title));
  card.append(element("p", "priority-why", status === "done" ? `Marked done in this demo only. Next: ${priority.unlocks}` : status === "parked" ? "Still here when you want it. Nothing else is waiting on you for this today." : priority.why));

  if (status === "open") {
    const link = element("a", "priority-action", priority.action_label);
    link.href = priority.action_href;
    if (priority.action_href.startsWith("https://")) {
      link.target = "_blank";
      link.rel = "noopener noreferrer";
      link.setAttribute("aria-label", `${priority.action_label} (opens a new tab)`);
    }
    card.append(link);
  }

  const controls = element("div", "priority-controls");
  if (status === "open") {
    controls.append(actionButton("Done", `Mark ${priority.title} done`, priority.id, "done", () => setPriority(priority.id, "done", "done")));
    controls.append(actionButton("Not today", `Park ${priority.title} for this session`, priority.id, "parked", () => setPriority(priority.id, "parked", "parked")));
  } else {
    controls.append(actionButton("Undo", `Put ${priority.title} back on the list`, priority.id, "undo", () => setPriority(priority.id, "open", status)));
  }
  card.append(controls);
  return card;
}

function renderTreeRecord() {
  const tree = fixture.tree_record;
  treeRecord.replaceChildren();
  treeRecord.append(element("p", "record-source", `Tree ${tree.set_id} · ${tree.epistemic_state} in ${tree.source_ref} on ${tree.recorded_on}`));
  const values = [
    ["Base", `${tree.base_studs[0]} × ${tree.base_studs[1]} studs`],
    ["Height", `${tree.height_bricks} bricks`],
    ["Base height", `${tree.base_height_bricks} bricks`],
    ["Branch overhang", `radius ${tree.branch_overhang_radius_studs} studs`],
    ["Clearance", `${tree.clear_height_bricks} bricks`],
  ];
  const details = element("dl", "measurement-list");
  for (const [label, value] of values) {
    details.append(element("dt", "", label), element("dd", "", value));
  }
  treeRecord.append(details);
  treeRecord.append(element("p", "record-evidence", `Evidence here: ${tree.verification}. A recheck in this demo does not revise DEC-016.`));
}

function renderPhotos() {
  photoGallery.replaceChildren();
  for (const photo of fixture.tree_record.photos) {
    const figure = element("figure", "photo");
    const link = element("a");
    link.href = photo.href;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.setAttribute("aria-label", `Open original photo: ${photo.label} (new tab)`);
    const image = element("img");
    image.src = photo.href;
    image.alt = photo.alt;
    image.loading = "lazy";
    link.append(image);
    figure.append(link, element("figcaption", "", photo.label));
    photoGallery.append(figure);
  }
}

function render() {
  const currentId = fixture.priorities.find((priority) => !state[priority.id])?.id;
  list.replaceChildren(...fixture.priorities.map((priority, index) => renderPriority(priority, index, currentId)));
  list.setAttribute("aria-busy", "false");
  lede.textContent = prioritySummary(fixture.priorities, state);
}

function setTheme(blueprint) {
  document.body.classList.toggle("dt-blueprint", blueprint);
  themeButton.setAttribute("aria-pressed", String(blueprint));
  themeButton.textContent = blueprint ? "Paper view" : "Blueprint view";
  try {
    localStorage.setItem("drafting-table-demo:theme", blueprint ? "blueprint" : "paper");
  } catch {
    // The theme still works for this page.
  }
}

themeButton.addEventListener("click", () => setTheme(!document.body.classList.contains("dt-blueprint")));
try {
  setTheme(localStorage.getItem("drafting-table-demo:theme") === "blueprint");
} catch {
  setTheme(false);
}

try {
  const response = await fetch("/fixture.json");
  if (!response.ok) throw new Error(`Fixture request failed (${response.status}).`);
  fixture = validateHubFixture(await response.json());
  state = readSavedState();
  saveState();
  renderTreeRecord();
  renderPhotos();
  render();
} catch (error) {
  list.setAttribute("aria-busy", "false");
  list.replaceChildren(element("li", "error", `The demo could not load its village fixture. ${error.message}`));
  lede.textContent = "The village priorities are unavailable.";
}
