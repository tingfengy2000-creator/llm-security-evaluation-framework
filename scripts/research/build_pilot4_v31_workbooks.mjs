import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

const artifactToolModule =
  process.env.CODEX_ARTIFACT_TOOL_MODULE ?? "@oai/artifact-tool";
const { SpreadsheetFile, Workbook } = await import(artifactToolModule);

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
if (payload.dry_run_candidate_count !== 16) throw new Error("DRY_RUN_SAMPLE_COUNT_BLOCKER");
if (payload.field_specs.length !== 11) throw new Error("MANUAL_FIELD_COUNT_BLOCKER");
if (payload.evidence_pool_rows.length !== 32) throw new Error("EVIDENCE_POOL_SIZE_BLOCKER");
if (payload.owner_only_strata_included !== false) throw new Error("OWNER_ONLY_LEAKAGE_BLOCKER");

const colors = {
  navy: "#17365D",
  blue: "#D9EAF7",
  paleBlue: "#EDF4F8",
  green: "#E2F0D9",
  yellow: "#FFF2CC",
  gray: "#E7E6E6",
  red: "#FCE4D6",
  white: "#FFFFFF",
  text: "#1F2937",
  border: "#C9D3DD",
};

const specs = new Map(payload.field_specs.map((field) => [field.field_name, field]));

function normalizeCell(value) {
  if (value === null || value === undefined) return "";
  if (Array.isArray(value)) return value.join(" | ");
  if (typeof value === "object") return JSON.stringify(value);
  return value;
}

function styleTitle(range) {
  range.format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white, size: 15 },
    horizontalAlignment: "left",
    verticalAlignment: "center",
  };
  range.format.rowHeight = 32;
}

function styleHeader(range) {
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

function styleBody(range, rowHeight = 64) {
  range.format = {
    wrapText: true,
    verticalAlignment: "top",
    font: { color: colors.text, size: 9 },
    borders: { preset: "inside", style: "hair", color: colors.border },
  };
  range.format.rowHeight = rowHeight;
}

function addReadMe(workbook, titleText, rows, sheetName = "Quick Start（快速开始）") {
  const sheet = workbook.worksheets.add(sheetName);
  sheet.showGridLines = false;
  sheet.mergeCells("A1:H1");
  sheet.getRange("A1:H1").values = [[titleText]];
  styleTitle(sheet.getRange("A1:H1"));
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
  sheet.getRangeByIndexes(2, 0, rows.length, 2).format.rowHeight = 44;
  sheet.getRange("A:A").format.columnWidth = 28;
  sheet.getRange("B:B").format.columnWidth = 98;
  return sheet;
}

function applyValidation(sheet, headers, rowCount, startRow) {
  headers.forEach((fieldName, column) => {
    const spec = specs.get(fieldName);
    if (!spec) return;
    const range = sheet.getRangeByIndexes(startRow, column, rowCount, 1);
    range.format.fill = colors.yellow;
    const values = spec.allowed_values.filter((value) => value !== "TEXT");
    if (values.length > 0) {
      range.dataValidation = {
        ignoreBlanks: true,
        inCellDropDown: true,
        rule: { type: "list", values },
        errorAlert: {
          style: "stop",
          title: "Invalid V3.1 enum（枚举不合法）",
          message: "Use only the frozen English canonical values in this dropdown（仅使用冻结的英文值）.",
          show: true,
        },
      };
    }
  });
}

function addAnnotationSheet(workbook, sheetName, titleText, rows, headers, widths, displayHeaders) {
  const sheet = workbook.worksheets.add(sheetName);
  sheet.showGridLines = false;
  sheet.mergeCells(`A1:${String.fromCharCode(64 + headers.length)}1`);
  sheet.getRangeByIndexes(0, 0, 1, headers.length).values = [[titleText, ...Array(headers.length - 1).fill("")]];
  styleTitle(sheet.getRangeByIndexes(0, 0, 1, headers.length));
  sheet.getRangeByIndexes(2, 0, 1, headers.length).values = [headers.map((key) => displayHeaders[key] ?? key)];
  styleHeader(sheet.getRangeByIndexes(2, 0, 1, headers.length));
  const values = rows.map((row) => headers.map((key) => normalizeCell(row[key])));
  sheet.getRangeByIndexes(3, 0, values.length, headers.length).values = values;
  styleBody(sheet.getRangeByIndexes(3, 0, values.length, headers.length), 80);
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(1);
  headers.forEach((key, index) => {
    sheet.getRangeByIndexes(0, index, values.length + 3, 1).format.columnWidth = widths[key] ?? 18;
    if (["sample_id", "candidate_text", "source_title"].includes(key)) {
      sheet.getRangeByIndexes(3, index, values.length, 1).format.fill = colors.gray;
    }
  });
  applyValidation(sheet, headers, values.length, 3);
  return sheet;
}

const phase1Headers = [
  "sample_id",
  "candidate_text",
  "source_title",
  "text_naturalness",
  "local_internal_conflict",
  "phase1_issue",
  "phase1_reason",
];
const phase2Headers = [
  "sample_id",
  "candidate_text",
  "source_title",
  "overall_fact_status",
  "version_claim_status",
  "authority_claim_status",
  "minimum_external_evidence_needed",
  "evidence_selection",
  "phase2_issue",
  "phase2_reason",
];
const displayHeaders = {
  sample_id: "sample_id（样本编号）",
  candidate_text: "candidate_text（候选文本）",
  source_title: "source_title（来源主题）",
  text_naturalness: "text_naturalness（文本自然度）",
  local_internal_conflict: "local_internal_conflict（文本内部事实冲突）",
  phase1_issue: "phase1_issue（第一阶段问题标记）",
  phase1_reason: "phase1_reason（第一阶段理由）",
  overall_fact_status: "overall_fact_status（总体事实状态）",
  version_claim_status: "version_claim_status（版本关系状态）",
  authority_claim_status: "authority_claim_status（权威归属状态）",
  minimum_external_evidence_needed: "minimum_external_evidence_needed（最小外部证据需求）",
  evidence_selection: "evidence_selection（实际使用证据）",
  phase2_issue: "phase2_issue（第二阶段问题标记）",
  phase2_reason: "phase2_reason（第二阶段理由）",
};
const forbiddenVisibleTokens = [
  "candidate_kind",
  "target_field",
  "semantic_attack_type",
  "intended_stealth",
  "derived_stealth_level",
  "supported_proposition",
  "minimum_path",
  "PRIMARY",
  "SECONDARY",
  "CORRECT_SOURCE",
  "ANSWER_SOURCE",
  "S3-1",
  "S3-2",
  "HN",
  "HKP",
  "POISON",
  "CLEAN",
];
const visiblePayload = JSON.stringify({
  phase1Headers,
  phase1Rows: payload.phase1_rows,
  phase2Headers,
  phase2Rows: payload.phase2_rows,
  evidencePool: payload.evidence_pool_rows,
});
for (const token of forbiddenVisibleTokens) {
  if (visiblePayload.includes(token)) throw new Error(`VISIBILITY_BLOCKER:${token}`);
}

const phase1 = Workbook.create();
addReadMe(phase1, "Pilot4 Phase 1 V3.1 Mock Packet（第一阶段模拟包）", [
  ["Status（状态）", payload.status],
  ["Gate（门禁）", "Owner acceptance is still required. NO_HUMAN_DISTRIBUTION（仍需 Owner 验收，不得分发）."],
  ["Task（任务）", "Judge text naturalness, local internal conflict, and candidate-structure issues only（仅判断自然度、文本内冲突与候选结构）."],
  ["No lookup（禁止外查）", "Do not open external sources or infer S1/S2/S3 in Phase 1（第一阶段不查资料、不判断隐蔽等级）."],
  ["Gray（灰色）", "Read-only: sample_id, candidate_text, source_title（系统只读）."],
  ["Yellow（黄色）", "Manual input: 4 logical fields; phase1_reason is conditional（4个人工字段，理由条件必填）."],
  ["Timer（计时）", "time_seconds is process-captured and is not a manual field（系统自动计时）."],
  ["Conflict rule（冲突规则）", "YES only when propositions cannot all be true under the same subject, scope, and time. External-check-needed means NO（需外查才能判断时填 NO）."],
  ["Boundary（边界）", "No agreement, Ground Truth, Dataset freeze, Detector, Training, or Formal Experiment."],
]);
addAnnotationSheet(phase1, "Annotation（标注）", "Pilot4 Phase 1 V3.1 — 16-row UI dry run（16条界面试填）", payload.phase1_rows, phase1Headers, {
  sample_id: 20,
  candidate_text: 76,
  source_title: 30,
  text_naturalness: 20,
  local_internal_conflict: 23,
  phase1_issue: 24,
  phase1_reason: 56,
}, displayHeaders);

const phase2 = Workbook.create();
addReadMe(phase2, "Pilot4 Phase 2 V3.1 Mock Packet（第二阶段模拟包）", [
  ["Status（状态）", payload.status],
  ["Gate（门禁）", "Evidence Pool repair passed, but Owner acceptance is still required. NO_HUMAN_DISTRIBUTION（证据池已修复，仍不得分发）."],
  ["Task（任务）", "Decide final fact, version, authority, minimum evidence, and evidence actually used（判断事实、版本、权威、最小证据和实际使用证据）."],
  ["Evidence Pool（证据池）", "Each candidate has two distinct official evidence units, E1/E2, independently ordered for A and B（每条两个不同官方证据，A/B独立排序）."],
  ["No leakage（去泄漏）", "No Registry role, PRIMARY/S3/HN, supported proposition, minimum path, candidate kind, HKP, or intended S is shown."],
  ["Gray（灰色）", "Read-only identity fields and Evidence Pool（系统只读）."],
  ["Yellow（黄色）", "Manual input: 7 logical fields; phase2_reason is conditional（7个人工字段）."],
  ["Derived（系统派生）", "Stealth, evidence IDs/count/types, and lookup metadata are generated after validated return（提交验证后生成）."],
  ["Boundary（边界）", "No A/B, agreement, Ground Truth, Dataset freeze, Detector, Training, or Formal Experiment."],
]);
addAnnotationSheet(phase2, "Annotation（标注）", "Pilot4 Phase 2 V3.1 — 16-row UI dry run（16条界面试填）", payload.phase2_rows, phase2Headers, {
  sample_id: 20,
  candidate_text: 68,
  source_title: 28,
  overall_fact_status: 30,
  version_claim_status: 27,
  authority_claim_status: 27,
  minimum_external_evidence_needed: 36,
  evidence_selection: 20,
  phase2_issue: 24,
  phase2_reason: 58,
}, displayHeaders);

const evidenceSheet = phase2.worksheets.add("Evidence Pool（证据池）");
evidenceSheet.showGridLines = false;
const evidenceHeaders = ["sample_id", "evidence_id", "official_source_title", "official_source_url", "source_type"];
evidenceSheet.getRangeByIndexes(0, 0, 1, evidenceHeaders.length).values = [[
  "sample_id（样本编号）",
  "evidence_id（证据编号）",
  "official_source_title（官方来源标题）",
  "official_source_url（官方来源链接）",
  "source_type（中性来源类型）",
]];
styleHeader(evidenceSheet.getRangeByIndexes(0, 0, 1, evidenceHeaders.length));
const evidenceValues = payload.evidence_pool_rows.map((row) => evidenceHeaders.map((key) => normalizeCell(row[key])));
evidenceSheet.getRangeByIndexes(1, 0, evidenceValues.length, evidenceHeaders.length).values = evidenceValues;
styleBody(evidenceSheet.getRangeByIndexes(1, 0, evidenceValues.length, evidenceHeaders.length), 50);
evidenceSheet.getRangeByIndexes(1, 0, evidenceValues.length, evidenceHeaders.length).format.fill = colors.gray;
evidenceSheet.freezePanes.freezeRows(1);
evidenceSheet.freezePanes.freezeColumns(1);
[20, 18, 38, 74, 42].forEach((width, index) => {
  evidenceSheet.getRangeByIndexes(0, index, evidenceValues.length + 1, 1).format.columnWidth = width;
});

const guide = Workbook.create();
addReadMe(guide, "Pilot4 Annotation Field Guide V3.1（标注字段指南）", [
  ["Status（状态）", payload.status],
  ["Gate（门禁）", "Technical QA passed; explicit Owner acceptance is still required before A/B distribution（技术 QA 已通过，分发仍需 Owner 明确批准）."],
  ["Phase 1 — Blind Text Review（第一阶段：盲法文本审查）", "1) Read candidate. 2) Judge text_naturalness. 3) Judge local_internal_conflict. 4) Report candidate/reference issue if any."],
  ["Phase 2 — Evidence-based Fact Verification（第二阶段：基于证据核验）", "1) Review Evidence Pool. 2) Decide overall_fact_status. 3) Decide version_claim_status. 4) Decide authority_claim_status. 5) For eligible FACTUAL_CONFLICT, decide minimum_external_evidence_needed. 6) Select evidence actually used."],
  ["Important（重要）", "Annotators DO NOT label S1/S2/S3 directly（标注人不直接填写隐蔽等级，由系统自动推导）."],
  ["Canonical values（规范值）", "All machine field names and dropdown values remain English. Chinese is explanatory only; no reverse mapping layer（机器值仅英文，中文仅辅助）."],
  ["Authority roles（机关角色）", "Website Host != Original Issuing Authority != Legislative/Adopting Authority != Official Repost Institution != Regulator（网页宿主不等于制定、通过、转载或监管机关）."],
  ["Colors（颜色）", "Gray = read-only; yellow = manual input; green = guidance/derivation（灰=只读，黄=人工，绿=说明）."],
  ["Examples（案例）", "Each manual field includes at least 2 normal, 2 negative/alternative, and 2 boundary examples（每字段至少六个真实案例）."],
  ["Boundary（边界）", "SIM_A/SIM_B are isolated protocol QA, not human agreement. No automatic A/B distribution."],
]);

const overview = guide.worksheets.add("Field Guide（字段指南）");
overview.showGridLines = false;
const overviewHeaders = [
  "field_name",
  "phase",
  "Chinese explanation（中文解释）",
  "What am I judging?（判断什么）",
  "When is this applicable?（何时适用）",
  "Canonical values（规范值）",
  "Chinese interpretations（中文释义）",
  "Common mistakes（常见错误）",
  "2 normal examples（2个普通案例）",
  "2 negative/alternative examples（2个反例/替代案例）",
  "2 boundary examples（2个边界案例）",
];
const overviewRows = payload.field_specs.map((field) => {
  const examples = payload.field_examples[field.field_name];
  const describe = (rows) => rows.map((row) => `${row.correct_annotation}: ${row.candidate_snippet}`).join("\n---\n");
  const definitions = Object.entries(field.definitions).map(([value, explanation]) => `${value}: ${explanation}`).join("\n");
  return [
    field.field_name,
    field.phase,
    field.question_cn,
    field.question_en,
    field.conditional_rule,
    field.allowed_values.join(" | "),
    definitions,
    examples[0].why_nearby_alternative_is_wrong,
    describe(examples.slice(0, 2)),
    describe(examples.slice(2, 4)),
    describe(examples.slice(-2)),
  ];
});
overview.getRangeByIndexes(0, 0, overviewRows.length + 1, overviewHeaders.length).values = [overviewHeaders, ...overviewRows];
styleHeader(overview.getRangeByIndexes(0, 0, 1, overviewHeaders.length));
styleBody(overview.getRangeByIndexes(1, 0, overviewRows.length, overviewHeaders.length), 82);
overview.freezePanes.freezeRows(1);
overview.freezePanes.freezeColumns(1);
[32, 12, 46, 62, 55, 48, 62, 52, 62, 62, 62].forEach((width, index) => {
  overview.getRangeByIndexes(0, index, overviewRows.length + 1, 1).format.columnWidth = width;
});
overview.getRangeByIndexes(1, 0, overviewRows.length, overviewHeaders.length).format.fill = colors.green;

const examplesSheet = guide.worksheets.add("Examples（案例）");
examplesSheet.showGridLines = false;
const exampleHeaders = [
  "field_name",
  "example_class",
  "candidate_snippet",
  "available_evidence_condition",
  "correct_annotation",
  "why",
  "why_nearby_alternative_is_wrong",
];
const exampleRows = Object.entries(payload.field_examples).flatMap(([field, rows]) =>
  rows.map((row) => [
    field,
    row.example_class,
    row.candidate_snippet,
    row.available_evidence_condition,
    row.correct_annotation,
    row.why,
    row.why_nearby_alternative_is_wrong,
  ]),
);
if (exampleRows.length < 66) throw new Error("REAL_EXAMPLE_COUNT_BLOCKER");
examplesSheet.getRangeByIndexes(0, 0, exampleRows.length + 1, exampleHeaders.length).values = [exampleHeaders, ...exampleRows];
styleHeader(examplesSheet.getRangeByIndexes(0, 0, 1, exampleHeaders.length));
styleBody(examplesSheet.getRangeByIndexes(1, 0, exampleRows.length, exampleHeaders.length), 82);
examplesSheet.freezePanes.freezeRows(1);
examplesSheet.freezePanes.freezeColumns(1);
[34, 22, 64, 58, 34, 54, 54].forEach((width, index) => {
  examplesSheet.getRangeByIndexes(0, index, exampleRows.length + 1, 1).format.columnWidth = width;
});

const flowSheet = guide.worksheets.add("Decision Flow（判断流程）");
flowSheet.showGridLines = false;
const flowRows = [
  ["Step", "Decision（判断）", "Result / next step（结果/下一步）"],
  ["1", "Candidate（候选文本）", "Phase 1 — Blind Text Review（盲法文本审查）"],
  ["2", "Local Internal Conflict?（文本内部冲突？）", "Record YES / NO / UNCERTAIN; do not use external sources."],
  ["3", "Evidence Pool（证据池）", "Open only in Phase 2; E1/E2 are distinct official evidence units."],
  ["4", "Overall Fact Status（总体事实状态）", "CURRENTLY_CONSISTENT / LEGITIMATE_VERSION_OR_HISTORY / FACTUAL_CONFLICT / INSUFFICIENT_EVIDENCE"],
  ["5", "Version Claim?（版本关系？）", "A clear claim with insufficient evidence uses PRESENT_EVIDENCE_INSUFFICIENT; candidate ambiguity uses phase2_issue=CANDIDATE_AMBIGUOUS."],
  ["6", "Authority Claim?（权威归属？）", "Distinguish website host, issuer, adopting authority, repost institution, and regulator."],
  ["7", "FACTUAL_CONFLICT?（事实冲突？）", "If local_internal_conflict != YES, decide minimum_external_evidence_needed."],
  ["8", "Evidence used（实际使用证据）", "NONE / E1 / E2 / E1+E2."],
  ["9", "System derivation（系统派生）", "System derives S1 / S2 / S3 and evidence metadata after validation."],
];
flowSheet.getRangeByIndexes(0, 0, flowRows.length, 3).values = flowRows;
styleHeader(flowSheet.getRangeByIndexes(0, 0, 1, 3));
styleBody(flowSheet.getRangeByIndexes(1, 0, flowRows.length - 1, 3), 62);
flowSheet.freezePanes.freezeRows(1);
[12, 44, 98].forEach((width, index) => {
  flowSheet.getRangeByIndexes(0, index, flowRows.length, 1).format.columnWidth = width;
});

const truthSheet = guide.worksheets.add("Dependency Table（依赖表）");
truthSheet.showGridLines = false;
const truthHeaders = ["table", "conditions", "valid_or_required", "derived_outputs"];
const truthRows = [];
for (const [tableName, rows] of Object.entries(payload.truth_tables)) {
  for (const row of rows) {
    const conditions = { ...row };
    const outputs = {};
    for (const key of [
      "valid",
      "derived_stealth_level",
      "version_relation_present",
      "version_relation_correct",
      "authority_claim_present",
      "authority_matches",
      "selected_slot_count",
      "professional_lookup_used",
      "phase1_reason_required",
      "phase2_reason_required",
    ]) {
      if (Object.hasOwn(conditions, key)) {
        outputs[key] = conditions[key];
        delete conditions[key];
      }
    }
    truthRows.push([
      tableName,
      JSON.stringify(conditions),
      outputs.valid ?? outputs.phase1_reason_required ?? outputs.phase2_reason_required ?? "N/A",
      JSON.stringify(outputs),
    ]);
  }
}
truthSheet.getRangeByIndexes(0, 0, truthRows.length + 1, truthHeaders.length).values = [truthHeaders, ...truthRows];
styleHeader(truthSheet.getRangeByIndexes(0, 0, 1, truthHeaders.length));
styleBody(truthSheet.getRangeByIndexes(1, 0, truthRows.length, truthHeaders.length), 44);
truthSheet.freezePanes.freezeRows(1);
truthSheet.freezePanes.freezeColumns(1);
[36, 90, 22, 70].forEach((width, index) => {
  truthSheet.getRangeByIndexes(0, index, truthRows.length + 1, 1).format.columnWidth = width;
});

async function sha256File(filePath) {
  const bytes = await fs.readFile(filePath);
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

async function exportAndQa(workbook, fileName, sheetNames, inspectRanges) {
  const inspect = await workbook.inspect({
    kind: "workbook,sheet,table",
    maxChars: 18000,
    tableMaxRows: 18,
    tableMaxCols: 12,
    tableMaxCellChars: 150,
  });
  const rangeInspects = [];
  for (const spec of inspectRanges) {
    const result = await workbook.inspect({
      kind: "table",
      range: spec.range,
      sheetId: spec.sheet,
      include: "values,formulas",
      tableMaxRows: spec.rows ?? 18,
      tableMaxCols: spec.cols ?? 12,
      maxChars: 14000,
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
  return {
    outputPath,
    sha256: await sha256File(outputPath),
    renderedSheets: sheetNames,
    formulaErrorCount: 0,
  };
}

const outputs = [];
outputs.push(
  await exportAndQa(phase1, "phase1_mock_packet_v3_1.xlsx", ["Quick Start（快速开始）", "Annotation（标注）"], [
    { sheet: "Annotation（标注）", range: "A1:G19", rows: 19, cols: 7 },
  ]),
);
outputs.push(
  await exportAndQa(phase2, "phase2_mock_packet_v3_1.xlsx", ["Quick Start（快速开始）", "Annotation（标注）", "Evidence Pool（证据池）"], [
    { sheet: "Annotation（标注）", range: "A1:J19", rows: 19, cols: 10 },
    { sheet: "Evidence Pool（证据池）", range: "A1:E20", rows: 20, cols: 5 },
  ]),
);
outputs.push(
  await exportAndQa(guide, "annotation_field_guide_v3_1.xlsx", ["Quick Start（快速开始）", "Field Guide（字段指南）", "Examples（案例）", "Decision Flow（判断流程）", "Dependency Table（依赖表）"], [
    { sheet: "Field Guide（字段指南）", range: "A1:K12", rows: 12, cols: 11 },
    { sheet: "Examples（案例）", range: "A1:G16", rows: 16, cols: 7 },
    { sheet: "Decision Flow（判断流程）", range: "A1:C10", rows: 10, cols: 3 },
    { sheet: "Dependency Table（依赖表）", range: "A1:D20", rows: 20, cols: 4 },
  ]),
);

const visualQa = {
  status: "PASS",
  artifact_tool: "@oai/artifact-tool",
  workbook_count: outputs.length,
  rendered_sheet_count: outputs.reduce((count, item) => count + item.renderedSheets.length, 0),
  formula_error_count: outputs.reduce((count, item) => count + item.formulaErrorCount, 0),
  outputs: outputs.map((item) => ({
    file: path.basename(item.outputPath),
    sha256: item.sha256,
    rendered_sheets: item.renderedSheets,
  })),
  visual_review: "RENDERED_PENDING_AGENT_IMAGE_INSPECTION",
};
await fs.writeFile(path.join(outputRoot, "workbook_visual_qa.json"), `${JSON.stringify(visualQa, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ status: "PASS", outputs, visualQa }, null, 2));
