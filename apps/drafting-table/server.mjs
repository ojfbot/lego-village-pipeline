import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../../", import.meta.url));
const routes = new Map([
  ["/", ["apps/drafting-table/index.html", "text/html; charset=utf-8"]],
  ["/app.mjs", ["apps/drafting-table/app.mjs", "text/javascript; charset=utf-8"]],
  ["/styles.css", ["apps/drafting-table/styles.css", "text/css; charset=utf-8"]],
  ["/tokens.css", ["packages/tokens/tokens.css", "text/css; charset=utf-8"]],
  ["/design-tokens.css", ["docs/design/H-01-R1/dt/tokens.css", "text/css; charset=utf-8"]],
  ["/schema/index.mjs", ["packages/schema/index.mjs", "text/javascript; charset=utf-8"]],
  ["/fixture.json", ["apps/drafting-table/hub.fixture.json", "application/json; charset=utf-8"]],
  ["/evidence/tree-41843/rough-2026-09-19/top.jpg", ["apps/drafting-table/evidence/tree-41843/rough-2026-09-19/top.jpg", "image/jpeg"]],
  ["/evidence/tree-41843/rough-2026-09-19/side.jpg", ["apps/drafting-table/evidence/tree-41843/rough-2026-09-19/side.jpg", "image/jpeg"]],
  ["/evidence/tree-41843/rough-2026-09-19/box.jpg", ["apps/drafting-table/evidence/tree-41843/rough-2026-09-19/box.jpg", "image/jpeg"]],
]);
const port = Number(process.env.PORT || 4173);

createServer(async (request, response) => {
  const route = routes.get(new URL(request.url, "http://localhost").pathname);
  if (!route) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
    return;
  }
  try {
    const body = await readFile(new URL(route[0], `file://${root}`));
    response.writeHead(200, {
      "content-type": route[1],
      "cache-control": "no-store",
      "x-content-type-options": "nosniff",
    });
    response.end(body);
  } catch {
    response.writeHead(500, { "content-type": "text/plain; charset=utf-8" });
    response.end("Could not read the demo file");
  }
}).listen(port, "127.0.0.1", () => {
  console.log(`Drafting Table demo: http://127.0.0.1:${port}`);
});
