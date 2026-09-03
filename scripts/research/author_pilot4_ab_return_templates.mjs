import fs from "node:fs/promises";
import path from "node:path";
import { Workbook } from "@oai/artifact-tool";

function csvCell(value) {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

const [specPath, resultPath, previewDir] = process.argv.slice(2);
if (!specPath || !resultPath || !previewDir) {
  throw new Error("usage: node author_pilot4_ab_return_templates.mjs <spec.json> <result.json> <preview-dir>");
}

const spec = JSON.parse(await fs.readFile(specPath, "utf8"));
if (!Array.isArray(spec.outputs) || spec.outputs.length !== 4) {
  throw new Error("EXPECTED_EXACTLY_FOUR_CSV_OUTPUTS");
}
await fs.mkdir(previewDir, { recursive: true });
const results = [];

for (const item of spec.outputs) {
  const rows = [item.headers, ...item.rows];
  const csvText = `${rows.map((row) => row.map(csvCell).join(",")).join("\r\n")}\r\n`;
  const workbook = await Workbook.fromCSV(csvText, { sheetName: item.sheet_name });
  const inspection = await workbook.inspect({
    kind: "workbook,sheet,table",
    maxChars: 5000,
    tableMaxRows: 8,
    tableMaxCols: item.headers.length,
    tableMaxCellChars: 120,
  });
  const preview = await workbook.render({
    sheetName: item.sheet_name,
    range: `A1:${String.fromCharCode(64 + item.headers.length)}12`,
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  const target = path.resolve(item.path);
  await fs.mkdir(path.dirname(target), { recursive: true });
  try {
    await fs.access(target);
    throw new Error(`TARGET_ALREADY_EXISTS:${target}`);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
  await fs.writeFile(target, `\uFEFF${csvText}`, "utf8");
  const previewName = `${path.basename(target, ".csv")}.png`;
  const previewPath = path.join(previewDir, previewName);
  await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
  results.push({
    target,
    sheet_name: item.sheet_name,
    rows: item.rows.length,
    columns: item.headers.length,
    inspection,
    preview: previewPath,
  });
}

await fs.writeFile(resultPath, `${JSON.stringify({ status: "PASS", results }, null, 2)}\n`, "utf8");
process.stdout.write(`${JSON.stringify({ status: "PASS", output_count: results.length })}\n`);
