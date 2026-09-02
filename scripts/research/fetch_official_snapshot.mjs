import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const [url, destination] = process.argv.slice(2);
if (!url || !destination) {
  throw new Error("usage: fetch_official_snapshot.mjs URL DESTINATION");
}

const response = await fetch(url, {
  headers: { "user-agent": "LLMGuard-Research-Evidence-Snapshot/1.0" },
});
if (!response.ok) {
  throw new Error(`HTTP_${response.status}:${url}`);
}
const bytes = Buffer.from(await response.arrayBuffer());
const target = resolve(destination);
await mkdir(dirname(target), { recursive: true });
await writeFile(target, bytes, { flag: "wx" });
const sha256 = createHash("sha256").update(bytes).digest("hex");
process.stdout.write(
  `${JSON.stringify({
    status: "PASS",
    url,
    destination: target,
    bytes: bytes.length,
    sha256,
    contentType: response.headers.get("content-type"),
  })}\n`,
);
