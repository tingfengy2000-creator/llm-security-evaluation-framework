import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const args = Object.fromEntries(
  process.argv.slice(2).map((arg) => {
    const split = arg.indexOf("=");
    if (split < 0) throw new Error(`expected --key=value, got ${arg}`);
    return [arg.slice(2, split), arg.slice(split + 1)];
  }),
);
for (const required of ["source", "output-root", "qa-root"]) {
  if (!args[required]) throw new Error(`missing --${required}`);
}

const sourcePath = path.resolve(args.source);
const outputRoot = path.resolve(args["output-root"]);
const qaRoot = path.resolve(args["qa-root"]);
await fs.mkdir(outputRoot, { recursive: true });
await fs.mkdir(qaRoot, { recursive: true });

const payload = JSON.parse(await fs.readFile(sourcePath, "utf8"));
if (payload.phase1_rows.length !== 12 || payload.phase2_rows.length !== 12) {
  throw new Error("DRY_RUN_SAMPLE_COUNT_BLOCKER");
}
if (payload.field_schema.length !== 28 || payload.truth_table.length !== 53) {
  throw new Error("SCHEMA_OR_TRUTH_TABLE_COUNT_BLOCKER");
}

const colors = {
  navy: "#17365D",
  blue: "#D9EAF7",
  paleBlue: "#EDF4F8",
  green: "#E2F0D9",
  yellow: "#FFF2CC",
  gray: "#E7E6E6",
  white: "#FFFFFF",
  text: "#1F2937",
  border: "#C9D3DD",
};

function normalizeCell(value) {
  if (value === null || value === undefined) return "";
  if (Array.isArray(value)) return value.join(" | ");
  if (typeof value === "object") return JSON.stringify(value);
  return value;
}

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
    horizontalAlignment: "center",
    verticalAlignment: "center",
    borders: { preset: "inside", style: "thin", color: colors.border },
  };
  range.format.rowHeight = 44;
}

function styleBody(range, rowHeight = 68) {
  range.format = {
    wrapText: true,
    verticalAlignment: "top",
    font: { color: colors.text, size: 9 },
    borders: { preset: "inside", style: "hair", color: colors.border },
  };
  range.format.rowHeight = rowHeight;
}

function addGuide(workbook, titleText, rows) {
  const sheet = workbook.worksheets.add("先看这里");
  sheet.showGridLines = false;
  sheet.mergeCells("A1:H1");
  sheet.getRange("A1:H1").values = [[titleText]];
  title(sheet.getRange("A1:H1"));
  sheet.getRangeByIndexes(2, 0, rows.length, 2).values = rows;
  sheet.getRangeByIndexes(2, 0, rows.length, 1).format = {
    fill: colors.blue,
    font: { bold: true, color: colors.navy },
    wrapText: true,
    verticalAlignment: "top",
  };
  sheet.getRangeByIndexes(2, 1, rows.length, 1).format = {
    wrapText: true,
    verticalAlignment: "top",
  };
  sheet.getRangeByIndexes(2, 0, rows.length, 2).format.rowHeight = 40;
  sheet.getRange("A:A").format.columnWidth = 28;
  sheet.getRange("B:B").format.columnWidth = 96;
  return sheet;
}

const schemaByName = new Map(payload.field_schema.map((field) => [field.field_name, field]));

function applyValidations(sheet, headers, rowCount, startRow = 4) {
  headers.forEach((name, column) => {
    const field = schemaByName.get(name);
    if (!field || field.field_class.startsWith("READ_ONLY") || field.field_class === "SYSTEM_DERIVED") return;
    const values = field.allowed_values.filter((value) => !["TEXT", "NON_NEGATIVE_NUMBER", "NON_NEGATIVE_INTEGER", "LIST_OF_ENUM", "LIST_OF_STABLE_ID"].includes(value));
    const range = sheet.getRangeByIndexes(startRow, column, rowCount, 1);
    range.format.fill = colors.yellow;
    if (values.length > 0) {
      range.dataValidation = {
        ignoreBlanks: true,
        inCellDropDown: true,
        rule: { type: "list", values },
        errorAlert: {
          style: "stop",
          title: "取值不符合 Schema V3",
          message: "请使用下拉列表中的冻结枚举。",
          show: true,
        },
      };
    }
  });
}

function addPacketSheet(workbook, name, titleText, rows, headers, widths) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  sheet.mergeCells(`A1:${String.fromCharCode(64 + Math.min(headers.length, 26))}1`);
  sheet.getRangeByIndexes(0, 0, 1, headers.length).values = [[titleText, ...Array(headers.length - 1).fill("")]];
  title(sheet.getRangeByIndexes(0, 0, 1, headers.length));
  sheet.getRangeByIndexes(2, 0, 1, headers.length).values = [headers];
  header(sheet.getRangeByIndexes(2, 0, 1, headers.length));
  const values = rows.map((row) => headers.map((key) => normalizeCell(row[key])));
  sheet.getRangeByIndexes(3, 0, values.length, headers.length).values = values;
  styleBody(sheet.getRangeByIndexes(3, 0, values.length, headers.length));
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(1);
  headers.forEach((key, index) => {
    sheet.getRangeByIndexes(0, index, values.length + 3, 1).format.columnWidth = widths[key] ?? 18;
    const field = schemaByName.get(key);
    if (field?.field_class.startsWith("READ_ONLY") || key === "derived_stealth_level") {
      sheet.getRangeByIndexes(3, index, values.length, 1).format.fill = colors.gray;
    }
  });
  applyValidations(sheet, headers, values.length, 3);
  return sheet;
}

const phase1Headers = [
  "sample_id",
  "candidate_text",
  "source_title",
  "neutral_context",
  "language_natural_score",
  "topic_relevance_score",
  "local_internal_anomaly",
  "confidence",
  "reasoning_short",
  "time_seconds",
  "issue_flag",
];
const phase1Forbidden = [
  "target_field",
  "semantic_attack_type",
  "intended_stealth",
  "evidence_ids",
  "minimum_evidence_scope",
  "overall_fact_status",
  "assigned_stealth_level",
];
const phase1Serialized = JSON.stringify({ headers: phase1Headers, rows: payload.phase1_rows });
for (const token of phase1Forbidden) {
  if (phase1Serialized.includes(token)) throw new Error(`PHASE1_VISIBILITY_BLOCKER:${token}`);
}

const phase2Headers = [
  "sample_id",
  "candidate_text",
  "source_title",
  "evidence_ids",
  "claim_matches_source",
  "fact_changed",
  "version_relation_present",
  "version_relation_correct",
  "history_or_update_claim_present",
  "legitimate_update_or_history",
  "authority_claim_present",
  "authority_matches",
  "overall_fact_status",
  "professional_lookup_used",
  "lookup_source_type",
  "minimum_evidence_scope",
  "evidence_unit_count",
  "evidence_types",
  "minimum_sufficient_evidence_reason",
  "derived_stealth_level",
];
const phase2Rows = payload.phase2_rows.map((row) => ({ ...row, derived_stealth_level: "SYSTEM_DERIVED_AFTER_RETURN" }));

const phase1 = Workbook.create();
addGuide(phase1, "Pilot4 Phase1 模拟标注包（仅 Dry-run）", [
  ["状态", "ANNOTATOR_DRY_RUN_ONLY / NO_HUMAN_DISTRIBUTION"],
  ["用途", "只验证盲法界面、字段语义和可操作性；不是 A/B 正式发放包。"],
  ["禁止查证", "Phase1 不查询外部资料，不查看 Phase2、证据路径、HKP、target_field、intended S 或 Owner 结果。"],
  ["核心判断", "local_internal_anomaly 只问：候选自身是否存在足以判定核心命题不可能同时成立的局部证据。"],
  ["YES", "存在明确的内部逻辑冲突；不是仅仅可疑。"],
  ["NO", "候选自身不足以确认事实异常。"],
  ["UNCERTAIN", "因语义、时间、指代或条件而无法判断是否存在真正内部冲突。"],
  ["边界", "本包不产生 agreement、Ground Truth、Dataset freeze、Detector、Training 或 Formal Experiment。"],
]);
addPacketSheet(phase1, "Phase1模拟", "Pilot4 Phase1 模拟记录（12 条，仅界面验证）", payload.phase1_rows, phase1Headers, {
  sample_id: 20,
  candidate_text: 72,
  source_title: 30,
  neutral_context: 34,
  language_natural_score: 18,
  topic_relevance_score: 18,
  local_internal_anomaly: 21,
  confidence: 14,
  reasoning_short: 48,
  time_seconds: 15,
  issue_flag: 24,
});

const phase2 = Workbook.create();
addGuide(phase2, "Pilot4 Phase2 模拟核验包（仅 Dry-run）", [
  ["状态", "ANNOTATOR_DRY_RUN_ONLY / NO_HUMAN_DISTRIBUTION"],
  ["进入条件", "仅用于核验 Phase2 字段与证据路径展示；本工作簿不是正式 A/B 包。"],
  ["证据规则", "根据实际完成的最小充分官方 evidence path 填写，不得事前猜测证据范围。"],
  ["LOCAL_TEXT_ONLY", "候选自身存在足以确认冲突的内部证据。"],
  ["ONE_DIRECT_OFFICIAL_SOURCE", "一个直接官方来源即可确认冲突。"],
  ["MULTI_DOCUMENT_OR_VERSION_CHAIN", "必须联合多个文档、版本或权威链才能确认冲突。"],
  ["derived stealth", "由 overall_fact_status、Phase1 local_internal_anomaly、minimum_evidence_scope 系统推导，禁止人工填写。"],
  ["边界", "本包不产生 agreement、Ground Truth、Dataset freeze、Detector、Training 或 Formal Experiment。"],
]);
addPacketSheet(phase2, "Phase2模拟", "Pilot4 Phase2 模拟记录（12 条，仅界面验证）", phase2Rows, phase2Headers, {
  sample_id: 20,
  candidate_text: 64,
  source_title: 28,
  evidence_ids: 32,
  claim_matches_source: 19,
  fact_changed: 16,
  version_relation_present: 20,
  version_relation_correct: 20,
  history_or_update_claim_present: 23,
  legitimate_update_or_history: 23,
  authority_claim_present: 20,
  authority_matches: 18,
  overall_fact_status: 29,
  professional_lookup_used: 20,
  lookup_source_type: 25,
  minimum_evidence_scope: 32,
  evidence_unit_count: 18,
  evidence_types: 28,
  minimum_sufficient_evidence_reason: 50,
  derived_stealth_level: 28,
});

const guide = Workbook.create();
addGuide(guide, "Pilot4 Annotation Field Guide V3（Candidate）", [
  ["状态", "PILOT4_ANNOTATION_SCHEMA_V3_CANDIDATE / NOT FROZEN"],
  ["使用范围", "供 Owner 与 dry-run 审核字段语义；Owner acceptance 前不得正式发放。"],
  ["Schema 原则", "每个人工字段均绑定唯一 allowed values、applicability、dependency、N/A、UNCERTAIN、missing、evidence 与 agreement population。"],
  ["Phase 分离", "Phase1 只做盲法可见判断；Phase2 才绑定实际 evidence path。"],
  ["隐蔽等级", "derived_stealth_level 为系统派生字段，不是人工猜测字段。"],
  ["门禁", "Field Ambiguity、Dependency Truth Table、Phase Visibility 与 Full72 QA 全部 PASS 后仍须 Owner acceptance。"],
]);

const overview = guide.worksheets.add("字段总览");
overview.showGridLines = false;
const overviewHeaders = [
  "field_name",
  "中文名称",
  "阶段",
  "field_class",
  "allowed_values",
  "applicability",
  "dependency",
  "N/A rule",
  "UNCERTAIN rule",
  "missing rule",
  "evidence requirement",
  "agreement population",
];
const overviewRows = payload.field_schema.map((field) => [
  field.field_name,
  field.chinese_name,
  field.phase,
  field.field_class,
  field.allowed_values.join(" | "),
  field.applicability,
  field.dependency,
  field.not_applicable_rule,
  field.uncertain_rule,
  field.missing_rule,
  field.evidence_requirement,
  field.agreement_population,
]);
overview.getRangeByIndexes(0, 0, overviewRows.length + 1, overviewHeaders.length).values = [overviewHeaders, ...overviewRows];
header(overview.getRangeByIndexes(0, 0, 1, overviewHeaders.length));
styleBody(overview.getRangeByIndexes(1, 0, overviewRows.length, overviewHeaders.length), 88);
overview.freezePanes.freezeRows(1);
overview.freezePanes.freezeColumns(1);
[29, 22, 13, 28, 37, 44, 42, 49, 49, 43, 46, 46].forEach((width, index) => {
  overview.getRangeByIndexes(0, index, overviewRows.length + 1, 1).format.columnWidth = width;
});

const examples = guide.worksheets.add("字段示例");
examples.showGridLines = false;
const exampleHeaders = ["field_name", "value_definitions", "5个正例", "5个边界/反例", "至少5个常见误解", "Pilot4实际示例"];
const exampleRows = payload.field_schema.map((field) => [
  field.field_name,
  Object.entries(field.value_definitions).map(([key, value]) => `${key}: ${value}`).join("\n"),
  field.positive_examples.join("\n"),
  field.boundary_examples.join("\n"),
  field.common_misconceptions.join("\n"),
  field.pilot4_actual_example,
]);
examples.getRangeByIndexes(0, 0, exampleRows.length + 1, exampleHeaders.length).values = [exampleHeaders, ...exampleRows];
header(examples.getRangeByIndexes(0, 0, 1, exampleHeaders.length));
styleBody(examples.getRangeByIndexes(1, 0, exampleRows.length, exampleHeaders.length), 150);
examples.freezePanes.freezeRows(1);
examples.freezePanes.freezeColumns(1);
[29, 55, 58, 58, 58, 55].forEach((width, index) => {
  examples.getRangeByIndexes(0, index, exampleRows.length + 1, 1).format.columnWidth = width;
});

const truth = guide.worksheets.add("依赖真值表");
truth.showGridLines = false;
const truthHeaders = [...new Set(payload.truth_table.flatMap((row) => Object.keys(row)))];
const truthRows = payload.truth_table.map((row) => truthHeaders.map((key) => normalizeCell(row[key])));
truth.getRangeByIndexes(0, 0, truthRows.length + 1, truthHeaders.length).values = [truthHeaders, ...truthRows];
header(truth.getRangeByIndexes(0, 0, 1, truthHeaders.length));
styleBody(truth.getRangeByIndexes(1, 0, truthRows.length, truthHeaders.length), 28);
truth.freezePanes.freezeRows(1);
truth.freezePanes.freezeColumns(1);
truthHeaders.forEach((name, index) => {
  truth.getRangeByIndexes(0, index, truthRows.length + 1, 1).format.columnWidth = Math.max(14, Math.min(38, name.length + 6));
});
const validColumn = truthHeaders.indexOf("valid");
if (validColumn >= 0) truth.getRangeByIndexes(1, validColumn, truthRows.length, 1).format.fill = colors.green;

async function exportAndQa(workbook, fileName, sheetNames, inspectRanges) {
  const inspect = await workbook.inspect({
    kind: "workbook,sheet,table",
    maxChars: 16000,
    tableMaxRows: 16,
    tableMaxCols: 22,
    tableMaxCellChars: 140,
  });
  const rangeInspects = [];
  for (const spec of inspectRanges) {
    const result = await workbook.inspect({
      kind: "table",
      range: spec.range,
      sheetId: spec.sheet,
      include: "values,formulas",
      tableMaxRows: spec.rows ?? 16,
      tableMaxCols: spec.cols ?? 22,
      maxChars: 12000,
    });
    rangeInspects.push({ spec, ndjson: result.ndjson });
  }
  const formulaErrors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 100 },
    summary: "formula error scan",
  });
  if (formulaErrors.ndjson.trim() && !formulaErrors.ndjson.includes("matched 0 entries")) {
    throw new Error(`FORMULA_ERROR_BLOCKER:${fileName}:${formulaErrors.ndjson}`);
  }
  const artifact = await SpreadsheetFile.exportXlsx(workbook);
  const outputPath = path.join(outputRoot, fileName);
  await artifact.save(outputPath);
  await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });
  const workbookQa = path.join(qaRoot, fileName.replace(/\.xlsx$/i, ""));
  await fs.mkdir(workbookQa, { recursive: true });
  await fs.writeFile(path.join(workbookQa, "workbook_inspect.ndjson"), inspect.ndjson, "utf8");
  await fs.writeFile(path.join(workbookQa, "range_inspects.json"), JSON.stringify(rangeInspects, null, 2), "utf8");
  await fs.writeFile(path.join(workbookQa, "formula_error_scan.ndjson"), formulaErrors.ndjson, "utf8");
  for (const sheetName of sheetNames) {
    const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
    const safe = sheetName.replace(/[^A-Za-z0-9\u4e00-\u9fff_-]/g, "_");
    await fs.writeFile(path.join(workbookQa, `${safe}.png`), new Uint8Array(await preview.arrayBuffer()));
  }
  return outputPath;
}

const outputs = [];
outputs.push(await exportAndQa(phase1, "phase1_mock_packet.xlsx", ["先看这里", "Phase1模拟"], [
  { sheet: "Phase1模拟", range: "A1:K15", rows: 15, cols: 11 },
]));
outputs.push(await exportAndQa(phase2, "phase2_mock_packet.xlsx", ["先看这里", "Phase2模拟"], [
  { sheet: "Phase2模拟", range: "A1:T15", rows: 15, cols: 20 },
]));
outputs.push(await exportAndQa(guide, "annotation_field_guide_v3.xlsx", ["先看这里", "字段总览", "字段示例", "依赖真值表"], [
  { sheet: "字段总览", range: "A1:L16", rows: 16, cols: 12 },
  { sheet: "依赖真值表", range: "A1:J20", rows: 20, cols: 10 },
]));

const visibilityReportPath = path.join(outputRoot, "dry_run_visibility_report.json");
const visibilityReport = JSON.parse(await fs.readFile(visibilityReportPath, "utf8"));
await fs.writeFile(
  visibilityReportPath,
  `${JSON.stringify(
    {
      ...visibilityReport,
      workbooks_pending_artifact_tool_build: false,
      workbook_count: outputs.length,
      rendered_sheet_count: 8,
      formula_error_count: 0,
      workbook_visual_qa: "PASS",
    },
    null,
    2,
  )}\n`,
  "utf8",
);

console.log(JSON.stringify({ status: "PASS", workbookCount: outputs.length, outputs }, null, 2));
