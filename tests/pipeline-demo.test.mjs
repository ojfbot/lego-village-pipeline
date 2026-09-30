import assert from "node:assert/strict";
import test from "node:test";
import { parseLdrawBom, parsePartCountCsv, compareBom, calculateGap, pipelineStatus, reconcileBuilt } from "../packages/pipeline/index.mjs";

const model = `0 FILE ring.mpd
1 16 0 0 0 1 0 0 0 1 0 0 0 1 quadrant.ldr
1 16 0 0 0 1 0 0 0 1 0 0 0 1 quadrant.ldr
0 FILE quadrant.ldr
1 4 0 0 0 1 0 0 0 1 0 0 0 1 53400.dat
1 0 0 0 0 1 0 0 0 1 0 0 0 1 3001.dat
`;
const bom = parseLdrawBom(model);

test("a nested LDraw model produces literal part and colour quantities", () => {
  assert.deepEqual(bom, [
    { part: "3001.dat", color: 0, quantity: 2 },
    { part: "53400.dat", color: 4, quantity: 2 },
  ]);
  assert.throws(() => parseLdrawBom(model.replace("quadrant.ldr\n0 FILE", "missing.ldr\n0 FILE")), /Missing submodel/);
});

test("the independent parts export must agree before the BOM is cross-checked", () => {
  const equal = parsePartCountCsv("part,color,quantity\n3001.dat,0,2\n53400.dat,4,2\n");
  assert.deepEqual(compareBom(bom, equal), { matches: true, differences: [] });
  const wrong = parsePartCountCsv("part,color,quantity\n3001.dat,0,2\n53400.dat,4,1\n");
  assert.deepEqual(compareBom(bom, wrong), { matches: false, differences: ["53400.dat|4: model 2, check 1"] });
});

test("unknown inventory never becomes zero and unusable parts do not cover demand", () => {
  const inventory = { "3001.dat|0": { counted: 4, usable: 1, evidence: "box A count photo", countedBy: "James" } };
  assert.deepEqual(calculateGap(bom, inventory).map((row) => row.shortage), [1, null]);
  const complete = { ...inventory, "53400.dat|4": { counted: 0, usable: 0, evidence: "empty bin checked", countedBy: "James" } };
  assert.deepEqual(calculateGap(bom, complete).map((row) => row.shortage), [1, 2]);
});

test("a review remains blocked without cross-check, complete count, and evidenced fit resolution", () => {
  const check = { rows: parsePartCountCsv("part,color,quantity\n3001.dat,0,2\n53400.dat,4,2"),
    method: "separate Studio export", checkedBy: "James", evidence: "parts-list.csv", modelSha256: "abc" };
  const inventory = {
    "3001.dat|0": { counted: 2, usable: 2, evidence: "bin A", countedBy: "James" },
    "53400.dat|4": { counted: 2, usable: 2, evidence: "bin B", countedBy: "James" },
  };
  assert.equal(pipelineStatus({ model: { rows: bom }, check, inventory }).reviewReady, false);
  const modelRecord = { rows: bom, source: { sha256: "abc" } };
  const fit = { verdict: "pass", resolution: "Notched the inner corner", evidence: "model r2", checkedBy: "James", modelSha256: "abc" };
  assert.deepEqual(pipelineStatus({ model: modelRecord, check, inventory, fit }).blockers, []);
  assert.equal(pipelineStatus({ model: modelRecord, check: { ...check, method: "" }, inventory, fit }).reviewReady, false);
  assert.equal(pipelineStatus({ model: { ...modelRecord, source: { sha256: "changed" } }, check, inventory, fit }).reviewReady, false);
  assert.deepEqual(reconcileBuilt(bom, { "3001.dat|0": { quantity: 1, evidence: "built count" } }).map((row) => row.difference), [-1, null]);
});

test("a retroactive order remains distinct from an inspected receipt and usable inventory", async () => {
  const { addRecordedOrder, addInspection, orderSummary } = await import("../packages/pipeline/index.mjs");
  const order = { id: "order-1", shop: "Example shop", orderNumber: "A123", placedOn: "2026-09-29", enteredBy: "James", evidence: "email receipt",
    lines: [{ part: "53400.dat", color: 4, quantity: 2 }] };
  let run = addRecordedOrder({}, order);
  assert.equal(run.orders[0].provenance, undefined);
  run.model = { rows: bom };
  assert.equal(orderSummary(bom, run.orders, []).find((row) => row.part === "53400.dat").accepted, 0);
  const receipt = { id: "receipt-1", orderId: "order-1", receivedOn: "2026-10-01", inspectedBy: "James", evidence: "opened parcel photo",
    lines: [{ part: "53400.dat", color: 4, arrived: 2, accepted: 1 }] };
  run = addInspection(run, receipt);
  const row = orderSummary(bom, run.orders, run.receipts).find((item) => item.part === "53400.dat");
  assert.deepEqual(row, { part: "53400.dat", color: 4, ordered: 2, awaiting: 0, arrived: 2, accepted: 1, rejected: 1 });
  assert.equal(calculateGap(bom, {})[1].shortage, null);
  assert.throws(() => addInspection(run, receipt), /exceeds the recorded order/);
  assert.throws(() => addInspection(run, { ...receipt, receivedOn: "2026-09-28" }), /precede/);
});

test("a Studio archive yields its real model bytes and rejects altered ZIP content", async () => {
  const { extractStudioModel } = await import("../packages/pipeline/studio-io.mjs");
  const { readFile } = await import("node:fs/promises");
  const bytes = await readFile(new URL("./fixtures/tiny-studio.io", import.meta.url));
  const extracted = extractStudioModel(bytes);
  assert.equal(extracted.archiveTotalParts, 2);
  assert.deepEqual(parseLdrawBom(extracted.model), [{ part: "53400.dat", color: 4, quantity: 2 }]);
  const damaged = Buffer.from(bytes);
  const payloadAt = 30 + damaged.readUInt16LE(26) + damaged.readUInt16LE(28);
  damaged[payloadAt + 3] ^= 1;
  assert.throws(() => extractStudioModel(damaged));
});
