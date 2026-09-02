import crypto from "node:crypto";
import fs from "node:fs/promises";


const [sourceUrl, outputPath] = process.argv.slice(2);
if (!sourceUrl || !outputPath) {
  throw new Error("usage: SOURCE_URL OUTPUT_PATH");
}

let lastError;
for (let attempt = 1; attempt <= 3; attempt += 1) {
  try {
    const response = await fetch(sourceUrl, {
      headers: {
        "user-agent": "Mozilla/5.0 LLMGuard-Research-Title-Provenance/1.0",
        accept: "text/html,application/pdf;q=0.9,*/*;q=0.5",
      },
      redirect: "follow",
      signal: AbortSignal.timeout(45000),
    });
    const bytes = Buffer.from(await response.arrayBuffer());
    if (response.status !== 200 || bytes.length < 256) {
      throw new Error(`HTTP_${response.status}_BYTES_${bytes.length}`);
    }
    await fs.writeFile(outputPath, bytes);
    console.log(JSON.stringify({
      status: response.status,
      finalUrl: response.url,
      contentType: response.headers.get("content-type") || "application/octet-stream",
      byteLength: bytes.length,
      sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    }));
    process.exit(0);
  } catch (error) {
    lastError = error;
  }
}
throw lastError;
