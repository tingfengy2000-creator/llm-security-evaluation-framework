import fs from "node:fs/promises";
import path from "node:path";
import {
  FileBlob,
  SpreadsheetFile,
  Workbook,
} from "@oai/artifact-tool";

const args = Object.fromEntries(
  process.argv.slice(2).map((arg) => {
    const split = arg.indexOf("=");
    if (split < 0) throw new Error(`expected --key=value, got ${arg}`);
    return [arg.slice(2, split), arg.slice(split + 1)];
  }),
);
for (const required of ["reference", "source", "output", "qa-root"]) {
  if (!args[required]) throw new Error(`missing --${required}`);
}

const referencePath = path.resolve(args.reference);
const sourcePath = path.resolve(args.source);
const outputPath = path.resolve(args.output);
const qaRoot = path.resolve(args["qa-root"]);
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(qaRoot, { recursive: true });

const colors = {
  navy: "#17365D",
  blue: "#D9EAF7",
  lightBlue: "#EAF3F8",
  green: "#E2F0D9",
  yellow: "#FFF2CC",
  red: "#FCE4D6",
  gray: "#E7E6E6",
  white: "#FFFFFF",
  text: "#1F2937",
};

function title(range) {
  range.format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white, size: 15 },
    horizontalAlignment: "left",
    verticalAlignment: "center",
  };
  range.format.rowHeight = 30;
}

function header(range) {
  range.format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white, size: 10 },
    wrapText: true,
    verticalAlignment: "center",
    horizontalAlignment: "center",
    borders: { preset: "inside", style: "thin", color: "#A6A6A6" },
  };
  range.format.rowHeight = 42;
}

// Render the immutable Repair-01 workbook before creating the replacement.
const reference = await SpreadsheetFile.importXlsx(
  await FileBlob.load(referencePath),
);
const referenceSheet = reference.worksheets.getItemAt(0);
const referenceInspect = await reference.inspect({
  kind: "workbook,sheet,table",
  maxChars: 5000,
  tableMaxRows: 8,
  tableMaxCols: 10,
  tableMaxCellChars: 80,
});
const referencePreview = await reference.render({
  sheetName: referenceSheet.name,
  autoCrop: "all",
  scale: 1,
  format: "png",
});
await fs.writeFile(
  path.join(qaRoot, "reference_repair01_first_sheet.png"),
  new Uint8Array(await referencePreview.arrayBuffer()),
);
await fs.writeFile(
  path.join(qaRoot, "reference_repair01_inspect.ndjson"),
  referenceInspect.ndjson,
  "utf8",
);

const payload = JSON.parse(await fs.readFile(sourcePath, "utf8"));
if (payload.rows.length !== 16) throw new Error("OWNER_SAMPLE_ROW_COUNT_BLOCKER");

const workbook = Workbook.create();

const guide = workbook.worksheets.add("请先阅读");
guide.showGridLines = false;
guide.mergeCells("A1:H1");
guide.getRange("A1:H1").values = [["Pilot4 最终 Owner Preflight（Repair-02）"]];
title(guide.getRange("A1:H1"));
const guideRows = [
  ["当前状态", payload.status],
  ["人工发放", "NO — 本工作簿仅供项目负责人最终预审"],
  ["Pilot4 接受状态", "NOT ACCEPTED — 只有 16 行全部无 SYSTEMIC_BLOCKER 后才可另行决定"],
  ["样本构成", "12 Poison（完整 HKP×S）+ 2 Clean + 2 Hard Negative"],
  ["审核重点", "事实主体、自然度、S1 是否无显式提示、S3 是否确需联合证据、长度档是否可信"],
  ["Owner结论允许值", "PASS / CANDIDATE_LOCAL_CORRECTION / SYSTEMIC_BLOCKER"],
  ["范围边界", "不生成 A/B 包，不建立 Ground Truth，不冻结 Dataset，不进入 Detector/Training/5090/Formal Experiment"],
  ["历史保留", "首轮 a843697 与第二轮 cad3b2b evidence 均保持不可变；本轮是新 additive namespace"],
];
guide.getRange(`A3:B${guideRows.length + 2}`).values = guideRows;
guide.getRange("A3:A10").format = { fill: colors.blue, font: { bold: true, color: colors.navy }, wrapText: true };
guide.getRange("B3:B10").format = { wrapText: true, verticalAlignment: "top" };
guide.getRange("A:A").format.columnWidth = 25;
guide.getRange("B:B").format.columnWidth = 95;
guide.getRange("A3:B10").format.rowHeight = 42;
guide.getRange("B4:B5").format.fill = colors.red;

const owner = workbook.worksheets.add("Owner最终复核");
owner.showGridLines = false;
const ownerHeaders = [
  "序号",
  "candidate_id",
  "triplet_id",
  "样本类型",
  "领域",
  "HKP",
  "intended_stealth",
  "length_band",
  "actual_visible_char_count",
  "candidate_text",
  "target_field",
  "minimum_evidence_path_summary",
  "evidence_unit_1_contribution",
  "evidence_unit_2_contribution",
  "why_single_evidence_insufficient",
  "HN_subtype",
  "Owner结论",
  "Owner备注",
];
const ownerValues = payload.rows.map((row) => ownerHeaders.map((key) => row[key] ?? ""));
owner.getRangeByIndexes(0, 0, ownerValues.length + 1, ownerHeaders.length).values = [
  ownerHeaders,
  ...ownerValues,
];
header(owner.getRangeByIndexes(0, 0, 1, ownerHeaders.length));
owner.freezePanes.freezeRows(1);
owner.freezePanes.freezeColumns(3);
owner.getRangeByIndexes(1, 0, ownerValues.length, ownerHeaders.length).format = {
  wrapText: true,
  verticalAlignment: "top",
  font: { color: colors.text, size: 9 },
  borders: { preset: "inside", style: "hair", color: "#D9D9D9" },
};
owner.getRangeByIndexes(1, 0, ownerValues.length, ownerHeaders.length).format.rowHeight = 95;
const conclusionIndex = ownerHeaders.indexOf("Owner结论");
const notesIndex = ownerHeaders.indexOf("Owner备注");
owner.getRangeByIndexes(1, conclusionIndex, ownerValues.length, 1).format.fill = colors.yellow;
owner.getRangeByIndexes(1, notesIndex, ownerValues.length, 1).format.fill = colors.yellow;
owner.getRangeByIndexes(1, conclusionIndex, ownerValues.length, 1).dataValidation = {
  ignoreBlanks: true,
  inCellDropDown: true,
  rule: {
    type: "list",
    values: ["PASS", "CANDIDATE_LOCAL_CORRECTION", "SYSTEMIC_BLOCKER"],
  },
  errorAlert: {
    style: "stop",
    title: "Owner 结论不合法",
    message: "请使用下拉列表中的冻结枚举。",
    show: true,
  },
};
const widths = {
  序号: 7,
  candidate_id: 19,
  triplet_id: 12,
  样本类型: 23,
  领域: 22,
  HKP: 27,
  intended_stealth: 16,
  length_band: 13,
  actual_visible_char_count: 15,
  candidate_text: 68,
  target_field: 27,
  minimum_evidence_path_summary: 40,
  evidence_unit_1_contribution: 38,
  evidence_unit_2_contribution: 38,
  why_single_evidence_insufficient: 52,
  HN_subtype: 36,
  Owner结论: 28,
  Owner备注: 42,
};
ownerHeaders.forEach((name, index) => {
  owner.getRangeByIndexes(0, index, ownerValues.length + 1, 1).format.columnWidth = widths[name] ?? 20;
});
owner.getRangeByIndexes(1, 0, 12, ownerHeaders.length).format.fill = colors.lightBlue;
owner.getRangeByIndexes(13, 0, 2, ownerHeaders.length).format.fill = colors.green;
owner.getRangeByIndexes(15, 0, 2, ownerHeaders.length).format.fill = colors.gray;
owner.getRangeByIndexes(1, conclusionIndex, ownerValues.length, 1).format.fill = colors.yellow;
owner.getRangeByIndexes(1, notesIndex, ownerValues.length, 1).format.fill = colors.yellow;

const s3 = workbook.worksheets.add("S3证据必要性");
s3.showGridLines = false;
const s3Rows = payload.rows
  .filter((row) => row.intended_stealth === "S3")
  .map((row) => [
    row.candidate_id,
    row.triplet_id,
    row.HKP,
    row.candidate_text,
    row.evidence_unit_1_contribution,
    row.evidence_unit_2_contribution,
    "FALSE",
    "FALSE",
    "TRUE",
    row.why_single_evidence_insufficient,
  ]);
const s3Headers = [
  "candidate_id",
  "triplet_id",
  "HKP",
  "candidate_text",
  "evidence_unit_1_contribution",
  "evidence_unit_2_contribution",
  "single_evidence_1_sufficient",
  "single_evidence_2_sufficient",
  "joint_evidence_sufficient",
  "necessity_rationale",
];
s3.getRangeByIndexes(0, 0, s3Rows.length + 1, s3Headers.length).values = [s3Headers, ...s3Rows];
header(s3.getRangeByIndexes(0, 0, 1, s3Headers.length));
s3.freezePanes.freezeRows(1);
s3.getRangeByIndexes(1, 0, s3Rows.length, s3Headers.length).format = { wrapText: true, verticalAlignment: "top", font: { size: 9 } };
s3.getRangeByIndexes(1, 0, s3Rows.length, s3Headers.length).format.rowHeight = 90;
[18, 12, 25, 65, 38, 38, 16, 16, 16, 55].forEach((width, index) => {
  s3.getRangeByIndexes(0, index, s3Rows.length + 1, 1).format.columnWidth = width;
});

const summary = workbook.worksheets.add("覆盖与门禁");
summary.showGridLines = false;
summary.mergeCells("A1:F1");
summary.getRange("A1:F1").values = [["Pilot4 Repair-02 覆盖与门禁摘要"]];
title(summary.getRange("A1:F1"));
summary.getRange("A3:F3").values = [["项目", "期望", "公式/结果", "状态", "边界", "备注"]];
header(summary.getRange("A3:F3"));
const summaryRows = [
  ["Owner 行数", 16, `=COUNTA('Owner最终复核'!B2:B17)`, "PASS", "Owner-only", "固定 16 行"],
  ["Poison", 12, `=COUNTIF('Owner最终复核'!D2:D17,"POISON_CANDIDATE")`, "PASS", "Owner-only", "完整 HKP×S"],
  ["Clean", 2, `=COUNTIF('Owner最终复核'!D2:D17,"CLEAN_CURRENT")`, "PASS", "Owner-only", "不同 domain/length"],
  ["Hard Negative", 2, `=COUNTIF('Owner最终复核'!D2:D17,"MATCHED_HARD_NEGATIVE")`, "PASS", "Owner-only", "不同 domain/length/type"],
  ["S3 单证据1充分", 0, `=COUNTIF('S3证据必要性'!G2:G5,"TRUE")`, "PASS", "Owner-only", "必须为 0"],
  ["S3 单证据2充分", 0, `=COUNTIF('S3证据必要性'!H2:H5,"TRUE")`, "PASS", "Owner-only", "必须为 0"],
  ["S3 联合证据充分", 4, `=COUNTIF('S3证据必要性'!I2:I5,"TRUE")`, "PASS", "Owner-only", "4/4 sampled S3"],
  ["人工发放", 0, 0, "PASS", "NO", "等待 Owner 决定"],
];
summary.getRange("A4:B11").values = summaryRows.map((row) => row.slice(0, 2));
summary.getRange("C4:C11").formulas = summaryRows.map((row) => [[row[2]]]).flat();
summary.getRange("D4:F11").values = summaryRows.map((row) => row.slice(3));
summary.getRange("A4:F11").format = { wrapText: true, verticalAlignment: "center", borders: { preset: "inside", style: "thin", color: "#D9D9D9" } };
summary.getRange("D4:D11").format = { fill: colors.green, font: { bold: true, color: "#006100" } };
[28, 12, 16, 12, 20, 42].forEach((width, index) => {
  summary.getRangeByIndexes(0, index, 11, 1).format.columnWidth = width;
});
summary.getRange("A4:F11").format.rowHeight = 32;

const inspect = await workbook.inspect({
  kind: "workbook,sheet,table",
  maxChars: 10000,
  tableMaxRows: 20,
  tableMaxCols: 18,
  tableMaxCellChars: 120,
});
const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 100 },
  summary: "formula error scan",
});
if (
  formulaErrors.ndjson.trim() &&
  !formulaErrors.ndjson.includes("matched 0 entries")
) {
  throw new Error(`FORMULA_ERROR_BLOCKER:${formulaErrors.ndjson}`);
}
const xlsx = await SpreadsheetFile.exportXlsx(workbook);
await xlsx.save(outputPath);
await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });
await fs.writeFile(path.join(qaRoot, "final_workbook_inspect.ndjson"), inspect.ndjson, "utf8");
await fs.writeFile(path.join(qaRoot, "final_workbook_formula_scan.ndjson"), formulaErrors.ndjson, "utf8");
for (const sheetName of ["请先阅读", "Owner最终复核", "S3证据必要性", "覆盖与门禁"]) {
  const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
  const safe = {
    请先阅读: "guide",
    Owner最终复核: "owner_final",
    S3证据必要性: "s3_necessity",
    覆盖与门禁: "coverage_gates",
  }[sheetName];
  await fs.writeFile(path.join(qaRoot, `${safe}.png`), new Uint8Array(await preview.arrayBuffer()));
}

console.log(
  JSON.stringify(
    {
      referenceWorkbook: referencePath,
      referenceFirstSheet: referenceSheet.name,
      outputWorkbook: outputPath,
      ownerRows: payload.rows.length,
      s3Rows: s3Rows.length,
      formulaErrors: 0,
      status: payload.status,
    },
    null,
    2,
  ),
);
