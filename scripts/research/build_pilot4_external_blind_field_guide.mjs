import fs from "node:fs/promises";
import path from "node:path";

import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";


const [mode, sourcePath, casesPath, outputRoot] = process.argv.slice(2);
if (!mode || !sourcePath || !outputRoot || !["inspect", "edit"].includes(mode)) {
  throw new Error("usage: MODE SOURCE_XLSX CASES_JSON_OR_DASH OUTPUT_ROOT");
}

const sourceBlob = await FileBlob.load(sourcePath);
const workbook = await SpreadsheetFile.importXlsx(sourceBlob);
const sheetInspection = await workbook.inspect({
  kind: "sheet",
  include: "id,name",
  maxChars: 10000,
});
const sheetSummary = (sheetInspection.ndjson ?? "")
  .split(/\r?\n/)
  .filter(Boolean)
  .map((line) => JSON.parse(line))
  .filter((item) => item.kind === "sheet");
if (sheetSummary.length === 0) {
  throw new Error("WORKBOOK_SHEET_DISCOVERY_BLOCKER");
}

async function saveRender(sheetName, destination) {
  const rendered = await workbook.render({
    sheetName,
    autoCrop: "all",
    scale: 1,
    format: "png",
  });
  await fs.writeFile(destination, new Uint8Array(await rendered.arrayBuffer()));
}

async function inspectWorkbook(root, prefix) {
  await fs.mkdir(root, { recursive: true });
  const summary = await workbook.inspect({
    kind: "workbook,sheet,table",
    maxChars: 18000,
    tableMaxRows: 8,
    tableMaxCols: 8,
    tableMaxCellChars: 120,
  });
  await fs.writeFile(path.join(root, `${prefix}_inspect.ndjson`), `${summary.ndjson}\n`, "utf8");
  const formulaErrors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 300 },
    summary: `${prefix} formula error scan`,
  });
  await fs.writeFile(
    path.join(root, `${prefix}_formula_errors.ndjson`),
    `${formulaErrors.ndjson}\n`,
    "utf8",
  );
  for (const item of sheetSummary) {
    const safe = item.name.replace(/[\\/:*?"<>|]/g, "_");
    await saveRender(item.name, path.join(root, `${safe}.png`));
  }
  return { formulaErrorScan: formulaErrors.ndjson, renderedSheetCount: sheetSummary.length };
}

if (mode === "inspect") {
  const result = await inspectWorkbook(path.resolve(outputRoot), "pre_edit");
  console.log(JSON.stringify({ status: "PASS", mode, sheets: sheetSummary, ...result }));
  process.exit(0);
}

const cases = JSON.parse(await fs.readFile(casesPath, "utf8"));
const expectedFields = [
  "text_naturalness",
  "local_internal_conflict",
  "phase1_issue",
  "phase1_reason",
  "overall_fact_status",
  "version_claim_status",
  "authority_claim_status",
  "minimum_external_evidence_needed",
  "evidence_selection",
  "phase2_issue",
  "phase2_reason",
];
if (new Set(cases.map((item) => item.field)).size !== expectedFields.length) {
  throw new Error("FIELD_GUIDE_FIELD_COVERAGE_BLOCKER");
}
for (const field of expectedFields) {
  if (!cases.some((item) => item.field === field)) {
    throw new Error(`FIELD_GUIDE_MISSING_FIELD:${field}`);
  }
}

const beforeOtherSheets = {};
for (const item of sheetSummary) {
  if (item.name === "Examples（案例）") continue;
  const sheet = workbook.worksheets.getItem(item.name);
  const used = sheet.getUsedRange();
  beforeOtherSheets[item.name] = JSON.stringify({ values: used.values, formulas: used.formulas });
}

const examples = workbook.worksheets.getItem("Examples（案例）");
const used = examples.getUsedRange();
used.clear({ applyTo: "all" });
examples.showGridLines = false;
examples.getRange("A1:E1").merge();
examples.getRange("A1").values = [["Schema V3.1 Real Case Guide / 真实案例指南"]];
examples.getRange("A2:E2").merge();
examples.getRange("A2").values = [[
  "Independent teaching fixtures only; none are External Blind Review candidates. / 仅使用独立教学案例，不含外部盲审候选。",
]];
examples.getRange("A4:E4").values = [[
  "Field / 字段",
  "Case type / 案例类型",
  "Independent fixture / 独立案例",
  "Decision / 判断",
  "Why / 理由",
]];
examples.getRangeByIndexes(4, 0, cases.length, 5).values = cases.map((item) => [
  item.field,
  item.category,
  item.fixture,
  item.decision,
  item.explanation,
]);

examples.getRange("A1:E1").format = {
  fill: "#17365D",
  font: { bold: true, color: "#FFFFFF", size: 16 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
};
examples.getRange("A2:E2").format = {
  fill: "#DCE6F1",
  font: { color: "#1F2937", italic: true, size: 10 },
  horizontalAlignment: "left",
  verticalAlignment: "center",
  wrapText: true,
};
examples.getRange("A4:E4").format = {
  fill: "#2F75B5",
  font: { bold: true, color: "#FFFFFF", size: 10 },
  horizontalAlignment: "center",
  verticalAlignment: "center",
  wrapText: true,
  borders: { preset: "outside", style: "thin", color: "#9CA3AF" },
};
const lastRow = 4 + cases.length;
examples.getRange(`A5:E${lastRow}`).format = {
  font: { size: 10, color: "#111827" },
  verticalAlignment: "top",
  wrapText: true,
  borders: {
    insideHorizontal: { style: "thin", color: "#E5E7EB" },
    bottom: { style: "thin", color: "#CBD5E1" },
  },
};
examples.getRange(`A5:A${lastRow}`).format.fill = "#EEF4FA";
examples.getRange(`B5:B${lastRow}`).format.fill = "#F8FAFC";
examples.getRange(`D5:D${lastRow}`).format.fill = "#FFF7ED";
examples.getRange(`A1:A${lastRow}`).format.columnWidth = 28;
examples.getRange(`B1:B${lastRow}`).format.columnWidth = 23;
examples.getRange(`C1:C${lastRow}`).format.columnWidth = 58;
examples.getRange(`D1:D${lastRow}`).format.columnWidth = 33;
examples.getRange(`E1:E${lastRow}`).format.columnWidth = 55;
examples.getRange("A1:E1").format.rowHeight = 30;
examples.getRange("A2:E2").format.rowHeight = 36;
examples.getRange("A4:E4").format.rowHeight = 32;
examples.getRange(`A5:E${lastRow}`).format.rowHeight = 48;
examples.freezePanes.freezeRows(4);

for (const item of sheetSummary) {
  if (item.name === "Examples（案例）") continue;
  const sheet = workbook.worksheets.getItem(item.name);
  const current = sheet.getUsedRange();
  const after = JSON.stringify({ values: current.values, formulas: current.formulas });
  if (after !== beforeOtherSheets[item.name]) {
    throw new Error(`NON_EXAMPLE_SHEET_CONTENT_CHANGED:${item.name}`);
  }
}

const workbookDir = path.resolve(outputRoot, "workbooks");
await fs.mkdir(workbookDir, { recursive: true });
const outputPath = path.join(workbookDir, "annotation_field_guide_v3_1.xlsx");
const exported = await SpreadsheetFile.exportXlsx(workbook);
await exported.save(outputPath);
const qa = await inspectWorkbook(path.resolve(outputRoot, "qa", "workbook_visual"), "post_edit");
const qaPayload = {
  status: "PASS",
  updatedSheet: "Examples（案例）",
  caseCount: cases.length,
  manualFieldCount: expectedFields.length,
  nonExampleSheetContentChanged: false,
  renderedSheetCount: qa.renderedSheetCount,
  formulaErrorScanContainsExcelError: /#REF!|#DIV\/0!|#VALUE!|#NAME\?|#N\/A/.test(
    qa.formulaErrorScan,
  ),
  outputPath,
};
if (qaPayload.formulaErrorScanContainsExcelError) {
  throw new Error("WORKBOOK_FORMULA_ERROR_BLOCKER");
}
await fs.writeFile(
  path.resolve(outputRoot, "qa", "workbook_update_qa.json"),
  `${JSON.stringify(qaPayload, null, 2)}\n`,
  "utf8",
);
console.log(JSON.stringify(qaPayload));
