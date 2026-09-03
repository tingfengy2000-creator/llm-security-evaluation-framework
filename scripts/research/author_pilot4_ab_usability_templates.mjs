import fs from "node:fs/promises";
import path from "node:path";
import { Workbook } from "@oai/artifact-tool";

function csvCell(value) {
  const text = String(value ?? "");
  return /[",\r\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

const [specPath, resultPath, previewDir] = process.argv.slice(2);
if (!specPath || !resultPath || !previewDir) {
  throw new Error("usage: node author_pilot4_ab_usability_templates.mjs <spec.json> <result.json> <preview-dir>");
}

const spec = JSON.parse(await fs.readFile(specPath, "utf8"));
if (!Array.isArray(spec.outputs) || spec.outputs.length !== 2) {
  throw new Error("EXPECTED_EXACTLY_TWO_PHASE1_V2_CSV_OUTPUTS");
}
await fs.mkdir(previewDir, { recursive: true });
const results = [];

for (const item of spec.outputs) {
  const rows = [item.headers, ...item.rows];
  const csvText = `${rows.map((row) => row.map(csvCell).join(",")).join("\r\n")}\r\n`;
  const workbook = await Workbook.fromCSV(csvText, { sheetName: item.sheet_name });
  const sheet = workbook.worksheets.getItemAt(0);
  sheet.getRange("A1:A73").format.columnWidthPx = 190;
  sheet.getRange("B1:B73").format.columnWidthPx = 180;
  sheet.getRange("C1:C73").format.columnWidthPx = 205;
  sheet.getRange("D1:D73").format.columnWidthPx = 170;
  sheet.getRange("E1:E73").format.columnWidthPx = 300;
  const inspection = await workbook.inspect({
    kind: "workbook,sheet,table",
    maxChars: 5000,
    tableMaxRows: 8,
    tableMaxCols: item.headers.length,
    tableMaxCellChars: 120,
  });
  const preview = await workbook.render({
    sheetName: item.sheet_name,
    range: "A1:E12",
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
  const previewPath = path.join(previewDir, `${path.basename(target, ".csv")}.png`);
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
