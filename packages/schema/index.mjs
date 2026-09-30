export const FIXTURE_VERSION = 1;
export const STORAGE_VERSION = 1;

const dispositions = new Set(["done", "parked"]);
const validSourceKinds = new Set(["fact", "question", "finding"]);

function nonempty(value) {
  return typeof value === "string" && value.trim().length > 0;
}

export function validateHubFixture(value) {
  const errors = [];
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error("Hub fixture must be an object.");
  }
  if (value.version !== FIXTURE_VERSION) errors.push("version must be 1");
  if (value.design_pin !== "H-01 R1 as-committed") errors.push("design_pin must name the committed H-01 R1 cut");
  if (value.data_kind !== "demo_fixture") errors.push("data_kind must be demo_fixture");
  const tree = value.tree_record;
  if (!tree || typeof tree !== "object" || Array.isArray(tree)) {
    errors.push("tree_record must be an object");
  } else {
    if (tree.set_id !== "41843" || tree.source_ref !== "DEC-016" || tree.epistemic_state !== "measured") {
      errors.push("tree_record must identify the DEC-016 measurement of tree 41843");
    }
    if (!nonempty(tree.recorded_on) || !nonempty(tree.verification)) {
      errors.push("tree_record must carry its date and verification limit");
    }
    if (!Array.isArray(tree.photos) || tree.photos.length !== 3) {
      errors.push("tree_record.photos must contain the three rough inventory photos");
    } else {
      const photoIds = new Set();
      for (const photo of tree.photos) {
        if (!nonempty(photo.id) || photoIds.has(photo.id) || !nonempty(photo.label) || !nonempty(photo.alt) ||
            !/^\/evidence\/tree-41843\/rough-2026-09-19\/[a-z]+\.jpg$/.test(photo.href || "") ||
            !/^[a-f0-9]{64}$/.test(photo.sha256 || "")) {
          errors.push("tree_record.photos contains an invalid or duplicate photo");
        }
        photoIds.add(photo.id);
      }
    }
    if (!Array.isArray(tree.base_studs) || tree.base_studs.length !== 2 || !tree.base_studs.every((n) => Number.isInteger(n) && n > 0)) {
      errors.push("tree_record.base_studs must contain two positive integers");
    }
    for (const key of ["height_bricks", "base_height_bricks", "branch_overhang_radius_studs", "clear_height_bricks"]) {
      if (!Number.isInteger(tree[key]) || tree[key] <= 0) errors.push(`tree_record.${key} must be a positive integer`);
    }
  }
  if (!Array.isArray(value.priorities) || value.priorities.length !== 3) {
    errors.push("priorities must contain exactly three items");
  } else {
    const ids = new Set();
    for (const [index, item] of value.priorities.entries()) {
      const at = `priorities[${index}]`;
      if (!item || typeof item !== "object" || Array.isArray(item)) {
        errors.push(`${at} must be an object`);
        continue;
      }
      if (!nonempty(item.id) || ids.has(item.id)) errors.push(`${at}.id must be unique and nonempty`);
      ids.add(item.id);
      for (const key of ["title", "why", "effort_label", "action_label", "action_href", "unlocks"]) {
        if (!nonempty(item[key])) errors.push(`${at}.${key} must be nonempty`);
      }
      if (!item.source_ref || !validSourceKinds.has(item.source_ref.kind) || !nonempty(item.source_ref.id)) {
        errors.push(`${at}.source_ref must identify a fact, question, or finding`);
      }
      if (typeof item.action_href === "string" && !/^https:\/\/[^\s]+$/.test(item.action_href) && !/^#[a-z0-9-]+$/.test(item.action_href)) {
        errors.push(`${at}.action_href must be an HTTPS URL or local anchor`);
      }
    }
  }
  if (errors.length) throw new Error(`Invalid Hub fixture: ${errors.join("; ")}.`);
  return value;
}

export function normalizeDispositions(raw, priorities, sessionId) {
  const result = {};
  if (!raw || raw.version !== STORAGE_VERSION || !raw.items || typeof raw.items !== "object") return result;
  for (const priority of priorities) {
    const entry = raw.items[priority.id];
    if (!entry || !dispositions.has(entry.status)) continue;
    if (entry.status === "parked" && entry.sessionId !== sessionId) continue;
    result[priority.id] = { status: entry.status, sessionId: entry.sessionId };
  }
  return result;
}

export function changeDisposition(current, id, status, sessionId, priorities) {
  if (!priorities.some((priority) => priority.id === id)) throw new Error("Unknown priority.");
  if (status !== "open" && !dispositions.has(status)) throw new Error("Unknown disposition.");
  const next = { ...current };
  if (status === "open") delete next[id];
  else next[id] = { status, sessionId };
  return next;
}

export function prioritySummary(priorities, state) {
  const open = priorities.filter((item) => !state[item.id]).length;
  const done = priorities.filter((item) => state[item.id]?.status === "done").length;
  if (open === 0 && done === priorities.length) return "All three closed. Nothing here needs you.";
  if (open === 0) return "Nothing open today. Parked items return in your next session.";
  if (open === priorities.length) return "Three small steps, in order. None has a deadline tonight.";
  return `${open} left. ${done ? `${done} done.` : "The rest can wait."}`;
}
