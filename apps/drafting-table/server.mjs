import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { extractStudioModel } from "../../packages/pipeline/studio-io.mjs";

const root = fileURLToPath(new URL("../../", import.meta.url));
const routes = new Map([
  ["/", ["apps/drafting-table/index.html", "text/html; charset=utf-8"]],
  ["/pipeline", ["apps/drafting-table/pipeline.html", "text/html; charset=utf-8"]],
  ["/pipeline.mjs", ["apps/drafting-table/pipeline.mjs", "text/javascript; charset=utf-8"]],
  ["/pipeline.css", ["apps/drafting-table/pipeline.css", "text/css; charset=utf-8"]],
  ["/pipeline/index.mjs", ["packages/pipeline/index.mjs", "text/javascript; charset=utf-8"]],
  ["/app.mjs", ["apps/drafting-table/app.mjs", "text/javascript; charset=utf-8"]],
  ["/styles.css", ["apps/drafting-table/styles.css", "text/css; charset=utf-8"]],
  ["/tokens.css", ["docs/design/H-01-R1/dt/tokens.css", "text/css; charset=utf-8"]],
  ["/schema/index.mjs", ["packages/schema/index.mjs", "text/javascript; charset=utf-8"]],
  ["/fixture.json", ["apps/drafting-table/hub.fixture.json", "application/json; charset=utf-8"]],
  ["/evidence/tree-41843/rough-2026-09-19/top.jpg", ["apps/drafting-table/evidence/tree-41843/rough-2026-09-19/top.jpg", "image/jpeg"]],
  ["/evidence/tree-41843/rough-2026-09-19/side.jpg", ["apps/drafting-table/evidence/tree-41843/rough-2026-09-19/side.jpg", "image/jpeg"]],
  ["/evidence/tree-41843/rough-2026-09-19/box.jpg", ["apps/drafting-table/evidence/tree-41843/rough-2026-09-19/box.jpg", "image/jpeg"]],
]);
const port = Number(process.env.PORT || 4173);

createServer(async (request, response) => {
  const pathname = new URL(request.url, "http://localhost").pathname;
  if (pathname === "/studio-model" && request.method === "POST") {
    try {
      const chunks = [];
      let size = 0;
      for await (const chunk of request) {
        size += chunk.length;
        if (size > 12 * 1024 * 1024) throw new Error("Studio archive must be under 12 MB.");
        chunks.push(chunk);
      }
      const result = extractStudioModel(Buffer.concat(chunks));
      response.writeHead(200, { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" });
      response.end(JSON.stringify(result));
    } catch (error) {
      response.writeHead(400, { "content-type": "application/json; charset=utf-8" });
      response.end(JSON.stringify({ error: error.message }));
    }
    return;
  }
  const route = routes.get(pathname);
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
