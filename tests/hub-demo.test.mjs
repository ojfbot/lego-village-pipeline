import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import {
  changeDisposition,
  normalizeDispositions,
  prioritySummary,
  validateHubFixture,
} from "../packages/schema/index.mjs";

const fixture = validateHubFixture(JSON.parse(await readFile(new URL("../apps/drafting-table/hub.fixture.json", import.meta.url), "utf8")));

test("the committed village fixture names the design cut and three distinct sources", () => {
  assert.equal(fixture.design_pin, "H-01 R1 as-committed");
  assert.deepEqual(fixture.priorities.map((item) => item.source_ref.kind), ["fact", "question", "finding"]);
  assert.equal(new Set(fixture.priorities.map((item) => item.id)).size, 3);
  assert.equal(fixture.priorities[0].id, "tree-base");
  assert.match(fixture.priorities[0].title, /Recheck/);
  assert.equal(fixture.tree_record.source_ref, "DEC-016");
  assert.deepEqual(fixture.tree_record.base_studs, [16, 16]);
  assert.equal(fixture.tree_record.height_bricks, 40);
  assert.equal(fixture.tree_record.base_height_bricks, 8);
  assert.equal(fixture.tree_record.branch_overhang_radius_studs, 28);
  assert.equal(fixture.tree_record.clear_height_bricks, 10);
  assert.deepEqual(fixture.tree_record.photos.map((photo) => photo.id), ["top", "side", "box"]);
  assert.match(fixture.tree_record.verification, /do not independently verify/);
});

test("a fixture with an unsafe action or duplicate priority fails before rendering", () => {
  const unsafe = structuredClone(fixture);
  unsafe.priorities[0].action_href = "javascript:alert(1)";
  unsafe.priorities[1].id = unsafe.priorities[0].id;
  assert.throws(() => validateHubFixture(unsafe), /action_href.*unique/);
});

test("done persists across sessions while parked returns on the next session", () => {
  let state = {};
  state = changeDisposition(state, "tree-base", "done", "session-a", fixture.priorities);
  state = changeDisposition(state, "train", "parked", "session-a", fixture.priorities);
  const saved = { version: 1, items: state };
  assert.deepEqual(Object.keys(normalizeDispositions(saved, fixture.priorities, "session-a")), ["tree-base", "train"]);
  assert.deepEqual(Object.keys(normalizeDispositions(saved, fixture.priorities, "session-b")), ["tree-base"]);
  assert.equal(prioritySummary(fixture.priorities, normalizeDispositions(saved, fixture.priorities, "session-b")), "2 left. 1 done.");
});

test("undo restores a priority without altering the other choices", () => {
  const current = {
    "tree-base": { status: "done", sessionId: "session-a" },
    train: { status: "parked", sessionId: "session-a" },
  };
  const next = changeDisposition(current, "tree-base", "open", "session-a", fixture.priorities);
  assert.deepEqual(next, { train: current.train });
  assert.equal(current["tree-base"].status, "done");
});
