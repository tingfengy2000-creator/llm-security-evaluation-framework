import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

function sha256(data) {
  return crypto.createHash("sha256").update(data).digest("hex");
}

function decodeHtml(bytes, contentType) {
  const declared = /charset=([^;\s]+)/i.exec(contentType || "")?.[1]?.toLowerCase();
  const head = bytes.subarray(0, Math.min(bytes.length, 4096)).toString("ascii");
  const meta = /charset=["']?([a-zA-Z0-9_-]+)/i.exec(head)?.[1]?.toLowerCase();
  const encoding = declared || meta || "utf-8";
  let decoded;
  try {
    decoded = new TextDecoder(encoding).decode(bytes);
  } catch {
    decoded = new TextDecoder("utf-8").decode(bytes);
  }
  return decoded
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;|&#160;/gi, " ")
    .replace(/&lt;/gi, "<")
    .replace(/&gt;/gi, ">")
    .replace(/&amp;/gi, "&")
    .replace(/&quot;/gi, '"')
    .replace(/&#39;|&apos;/gi, "'")
    .replace(/&#(\d+);/g, (_, code) => String.fromCodePoint(Number(code)))
    .replace(/\s+/g, " ")
    .trim();
}

async function decodePdf(bytes) {
  const { getDocument } = await import("pdfjs-dist/legacy/build/pdf.mjs");
  const document = await getDocument({ data: new Uint8Array(bytes) }).promise;
  const pages = [];
  for (let number = 1; number <= document.numPages; number += 1) {
    const page = await document.getPage(number);
    const content = await page.getTextContent();
    pages.push(`[[PAGE ${number}]] ${content.items.map((item) => item.str).join(" ")}`);
  }
  return pages.join(" ").replace(/\s+/g, " ").trim();
}

function normalize(value) {
  return value.replace(/[\s　]+/g, "").replace(/[“”]/g, '"').replace(/[‘’]/g, "'");
}

function excerptFor(text, anchors) {
  const normalized = normalize(text);
  const normalizedAnchors = anchors.map(normalize);
  const missing = normalizedAnchors.filter((anchor) => !normalized.includes(anchor));
  if (missing.length) {
    throw new Error(`SOURCE_CONTENT_ANCHOR_BLOCKER:${missing.join("|")}`);
  }
  const rawAnchor = anchors.find((anchor) => text.includes(anchor));
  const position = rawAnchor ? text.indexOf(rawAnchor) : 0;
  const start = Math.max(0, position - 240);
  const end = Math.min(text.length, position + 760);
  let excerpt = text.slice(start, end).trim();
  for (const anchor of anchors) {
    if (!normalize(excerpt).includes(normalize(anchor))) {
      const anchorPosition = normalized.indexOf(normalize(anchor));
      const ratio = anchorPosition / Math.max(1, normalized.length);
      const rawPosition = Math.floor(ratio * text.length);
      excerpt += ` […] ${text.slice(Math.max(0, rawPosition - 180), rawPosition + 420).trim()}`;
    }
  }
  return excerpt.replace(/\s+/g, " ").trim();
}

const sourceCache = new Map();

async function materialFor(sourceUrl) {
  if (sourceCache.has(sourceUrl)) return sourceCache.get(sourceUrl);
  const promise = (async () => {
    let response;
    let bytes;
    let lastError;
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        response = await fetch(sourceUrl, {
          headers: { "user-agent": "Mozilla/5.0 LLMGuard-Research-Verification/1.0" },
          redirect: "follow",
          signal: AbortSignal.timeout(45000),
        });
        bytes = Buffer.from(await response.arrayBuffer());
        if (response.status === 200 && bytes.length >= 512) break;
        lastError = new Error(`HTTP_${response.status}:${bytes.length}`);
      } catch (error) {
        lastError = error;
      }
    }
    if (!response || !bytes || response.status !== 200 || bytes.length < 512) {
      throw new Error(`SOURCE_ACCESS_BLOCKER:${sourceUrl}:${lastError?.message || "UNKNOWN"}`);
    }
    const contentType = response.headers.get("content-type") || "application/octet-stream";
    const mediaType = contentType.split(";")[0].trim().toLowerCase();
    const isPdf = mediaType.includes("pdf") || sourceUrl.toLowerCase().endsWith(".pdf");
    const text = isPdf ? await decodePdf(bytes) : decodeHtml(bytes, contentType);
    return { response, bytes, mediaType, isPdf, text };
  })();
  sourceCache.set(sourceUrl, promise);
  return promise;
}

async function acquire(spec) {
  const { response, bytes, mediaType, isPdf, text } = await materialFor(spec.source_url);
  let excerpt;
  try {
    excerpt = excerptFor(text, spec.anchors);
  } catch (error) {
    throw new Error(`${spec.evidence_id}:${error.message}`);
  }
  return {
    evidence_id: spec.evidence_id,
    triplet_id: spec.triplet_id ?? null,
    source_url: spec.source_url,
    final_url: response.url,
    source_identity: spec.source_identity,
    document_identity: spec.document_identity ?? spec.source_identity,
    official_role: spec.official_role ?? "OFFICIAL_GOVERNMENT_SOURCE",
    relationship_to_primary_subject: spec.relationship_to_primary_subject ?? null,
    neutral_source_type: spec.neutral_source_type ?? "OFFICIAL_WEB_PAGE",
    retrieved_at: new Date().toISOString(),
    retrieval_status: "HTTP_DOCUMENT_RETRIEVED_AND_CONTENT_MATCHED",
    http_status: response.status,
    media_type: mediaType,
    byte_length: bytes.length,
    content_hash: sha256(bytes),
    source_snapshot_hash: sha256(bytes),
    minimal_evidence_hash: sha256(Buffer.from(excerpt, "utf8")),
    supported_proposition: spec.supported_proposition,
    support_location: spec.support_location,
    support_excerpt: excerpt,
    verification_method: isPdf
      ? "HTTP_PDF_TEXT_CONTENT_ANCHOR_MATCH"
      : "HTTP_HTML_CONTENT_ANCHOR_MATCH",
    matched_anchors: spec.anchors,
    release_policy: "HASH_AND_MINIMAL_EXCERPT_ONLY",
  };
}

const [planPath, outputPath] = process.argv.slice(2);
if (!planPath || !outputPath) {
  throw new Error("usage: acquire_pilot4_quality_sources.mjs PLAN_JSON OUTPUT_JSON");
}
const plan = JSON.parse(await fs.readFile(planPath, "utf8"));
const records = [];
for (const spec of plan.evidence_units) {
  records.push(await acquire(spec));
}
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.writeFile(
  outputPath,
  `${JSON.stringify(
    {
      task_id: plan.task_id,
      status: "PASS",
      retrieval_count: records.length,
      records,
    },
    null,
    2,
  )}\n`,
  "utf8",
);
console.log(JSON.stringify({ status: "PASS", retrieval_count: records.length, output: outputPath }));
