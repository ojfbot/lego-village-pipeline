import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { validateHubFixture } from "./index.mjs";

const appDir = fileURLToPath(new URL("../../apps/drafting-table/", import.meta.url));
const fixture = validateHubFixture(JSON.parse(await readFile(join(appDir, "hub.fixture.json"), "utf8")));
for (const photo of fixture.tree_record.photos) {
  const bytes = await readFile(join(appDir, photo.href.slice(1)));
  const digest = createHash("sha256").update(bytes).digest("hex");
  if (digest !== photo.sha256) throw new Error(`Photo hash changed: ${photo.id}`);
}
console.log("Hub fixture and three photo hashes valid.");
