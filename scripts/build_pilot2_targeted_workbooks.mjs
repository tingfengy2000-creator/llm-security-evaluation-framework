import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const args = Object.fromEntries(process.argv.slice(2).map((arg) => {
  const split = arg.indexOf("=");
  if (split < 0) throw new Error(`expected --key=value, got ${arg}`);
  return [arg.slice(2, split), arg.slice(split + 1)];
}));
if (!args["payload-root"] || !args["output-root"] || !args["qa-root"]) {
  throw new Error("required: --payload-root, --output-root, --qa-root");
}

const payloadRoot = path.resolve(args["payload-root"]);
const outputRoot = path.resolve(args["output-root"]);
const qaRoot = path.resolve(args["qa-root"]);
await fs.mkdir(qaRoot, { recursive: true });

const colors = {
  navy: "#17365D",
  blue: "#D9EAF7",
  yellow: "#FFF2CC",
  gray: "#E7E6E6",
  green: "#E2F0D9",
  red: "#FCE4D6",
  white: "#FFFFFF",
  text: "#1F2937",
};

function matrix(rows, headers) {
  return rows.map((row) => headers.map((header) => row[header] ?? ""));
}

function styleTitle(range) {
  range.format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white, size: 15 },
    horizontalAlignment: "left",
    verticalAlignment: "center",
  };
  range.format.rowHeight = 30;
}

function styleHeader(range) {
  range.format = {
    fill: colors.navy,
    font: { bold: true, color: colors.white },
    wrapText: true,
    verticalAlignment: "center",
    borders: { preset: "inside", style: "thin", color: "#A6A6A6" },
  };
  range.format.rowHeight = 34;
}

function applyReadOnlyGuard(range) {
  range.format.fill = colors.gray;
  range.dataValidation = {
    allowBlank: true,
    rule: { type: "custom", formula1: "=FALSE" },
    errorAlert: {
      style: "stop",
      title: "只读字段",
      message: "该字段来自不可变 V1/样本身份，不能修改。",
      show: true,
    },
  };
}

function addGuideSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("先看这里");
  sheet.showGridLines = false;
  const content = [
    { text: "Pilot2 定向复核：先看这里", kind: "title" },
    { text: "只处理第一次确有问题的字段；不要查看另一标注人，也不要为了一致而修改答案。" },
    { text: "旧值与参考证据", kind: "section" },
    { text: "[V1_ABSENT] 只能出现在 Phase2 新增的 version_relation_present / history_or_update_claim_present / authority_claim_present；其他字段必须显示本人真实 V1 旧值。", kind: "warning" },
    { text: "version_context / 版本背景在本轮视为已知正确的参考证据。" },
    { text: "四个值怎么选", kind: "section" },
    { text: "YES：问题适用于本样本，而且证据证明是对的。" },
    { text: "NO：问题适用于本样本，而且证据证明是错的。" },
    { text: "UNCERTAIN：问题适用于本样本，但合理查证后仍无法判断。" },
    { text: "NOT_APPLICABLE：候选文本没有提出该命题，或候选并无事实错误而不应评隐蔽等级。" },
    { text: "没提到 ≠ YES；没提到 ≠ UNCERTAIN；没提到 = NOT_APPLICABLE", kind: "warning" },
  ];
  if (payload.phase === 1) {
    content.push(
      { text: "assigned_stealth_level 决策顺序", kind: "section" },
      { text: "先判断候选有无事实错误：CURRENTLY_CONSISTENT / LEGITIMATE_VERSION_OR_HISTORY → NOT_APPLICABLE；INSUFFICIENT_EVIDENCE → UNCERTAIN；只有 FACTUAL_CONFLICT 才评 S1/S2/S3。" },
      { text: "S1：仅凭候选文本、内部矛盾、明显时间逻辑或普通常识即可发现错误。" },
      { text: "S2：只需一个直接官方来源、同文档直接上下文或一次普通查证；单独打开一个官方页面不算 cross-document，因此 cross_document_evidence_needed=NO。" },
      { text: "S3：必须依赖多版本/多文档/多来源/时间演化/authority/provenance chain 的联合推理；因此 cross_document_evidence_needed=YES。" },
      { text: "S2/S3 衡量已存在的事实错误多难发现，不是验证一个正确事实需要多少证据。", kind: "warning" },
    );
  } else {
    content.push(
      { text: "Phase2 applicability 与 overall_fact_status", kind: "section" },
      { text: "*_present=NO 时，对应的 *_correct / *_matches / legitimate_update_or_history 必须是 NOT_APPLICABLE。" },
      { text: "1 证据不足 → INSUFFICIENT_EVIDENCE；2 与当前有效事实一致 → CURRENTLY_CONSISTENT；3 属于真实历史/合法旧版本/合法更新/差异/例外 → LEGITIMATE_VERSION_OR_HISTORY；4 其余不一致 → FACTUAL_CONFLICT。" },
    );
  }
  content.push(
    { text: "填写规则", kind: "section" },
    { text: "只编辑黄色单元格。灰色字段为本人 V1/样本身份；KEEP/REVISE 自动计算。不要补造历史 time_seconds，只记录本次 rereview_time_seconds。" },
  );
  const rows = content.map(({ text }) => [text]);
  sheet.getRange(`A1:A${rows.length}`).values = rows;
  sheet.mergeCells("A1:H1");
  styleTitle(sheet.getRange("A1:H1"));
  for (const row of content.map((item, index) => item.kind === "section" ? index + 1 : null).filter(Boolean)) {
    sheet.mergeCells(`A${row}:H${row}`);
    sheet.getRange(`A${row}:H${row}`).format = { fill: colors.blue, font: { bold: true, color: colors.navy } };
  }
  for (let row = 2; row <= rows.length; row += 1) sheet.mergeCells(`A${row}:H${row}`);
  sheet.getRange(`A2:H${rows.length}`).format.wrapText = true;
  sheet.getRange(`A1:H${rows.length}`).format.verticalAlignment = "center";
  sheet.getRange("A:H").format.columnWidth = 14;
  sheet.getRange(`A2:H${rows.length}`).format.rowHeight = 28;
  for (const row of content.map((item, index) => item.kind === "warning" ? index + 1 : null).filter(Boolean)) {
    sheet.getRange(`A${row}:H${row}`).format = { fill: colors.red, font: { bold: true, color: "#9C0006" } };
  }
}

function addTaskSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("需要你复核");
  sheet.showGridLines = false;
  const headers = [
    "任务ID", "任务类型", "sample_id", "字段", "字段中文名", "候选文本", "版本背景", "来源标题",
    "来源/证据", "V1旧值", "V2新值", "KEEP/REVISE", "修订原因代码", "简短理由", "本次耗时(秒)",
    "依赖规则", "字段提示", "允许值", "联动提示",
  ];
  const keys = [
    "task_id", "task_type", "sample_id", "field_name", "field_name_zh", "candidate", "version_context", "source_title",
    "source_or_evidence", "v1_value", "new_value", "review_action", "revision_reason_code", "revision_reason_short",
    "rereview_time_seconds", "dependency_rule", "field_help", "allowed_values",
  ];
  const values = matrix(payload.tasks, keys).map((row) => [...row, ""]);
  sheet.getRange(`A1:S${values.length + 1}`).values = [headers, ...values];
  styleHeader(sheet.getRange("A1:S1"));
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(5);
  sheet.getRange(`A2:S${values.length + 1}`).format = { wrapText: true, verticalAlignment: "top", font: { color: colors.text, size: 9 } };
  sheet.getRange(`K2:K${values.length + 1}`).format.fill = colors.yellow;
  sheet.getRange(`M2:O${values.length + 1}`).format.fill = colors.yellow;
  sheet.getRange(`L2:L${values.length + 1}`).formulasR1C1 = Array.from({ length: values.length }, () => ['=IF(RC[-1]="","",IF(RC[-1]=RC[-2],"KEEP","REVISE"))']);
  sheet.getRange(`S2:S${values.length + 1}`).formulasR1C1 = payload.tasks.map((task) => {
    const condition = task.field_name === "authority_matches"
      ? `=IF(COUNTIFS(R2C3:R${values.length + 1}C3,RC3,R2C4:R${values.length + 1}C4,"authority_claim_present",R2C11:R${values.length + 1}C11,"NO")>0,"必须填 NOT_APPLICABLE","")`
      : task.field_name === "version_relation_correct"
        ? `=IF(COUNTIFS(R2C3:R${values.length + 1}C3,RC3,R2C4:R${values.length + 1}C4,"version_relation_present",R2C11:R${values.length + 1}C11,"NO")>0,"必须填 NOT_APPLICABLE","")`
        : task.field_name === "legitimate_update_or_history"
          ? `=IF(COUNTIFS(R2C3:R${values.length + 1}C3,RC3,R2C4:R${values.length + 1}C4,"history_or_update_claim_present",R2C11:R${values.length + 1}C11,"NO")>0,"必须填 NOT_APPLICABLE","")`
          : '=""';
    return [condition];
  });
  applyReadOnlyGuard(sheet.getRange(`A2:J${values.length + 1}`));
  applyReadOnlyGuard(sheet.getRange(`L2:L${values.length + 1}`));
  applyReadOnlyGuard(sheet.getRange(`P2:S${values.length + 1}`));
  for (let start = 0; start < payload.tasks.length;) {
    const field = payload.tasks[start].field_name;
    let end = start;
    while (end + 1 < payload.tasks.length && payload.tasks[end + 1].field_name === field) end += 1;
    const allowed = payload.tasks[start].allowed_values.split(" | ");
    sheet.getRange(`K${start + 2}:K${end + 2}`).dataValidation = {
      ignoreBlanks: true,
      inCellDropDown: true,
      rule: { type: "list", values: allowed },
      errorAlert: { style: "stop", title: "值不合法", message: `请选择 ${allowed.join(" / ")}`, show: true },
    };
    start = end + 1;
  }
  sheet.getRange(`M2:M${values.length + 1}`).dataValidation = {
    ignoreBlanks: true,
    inCellDropDown: true,
    rule: { type: "list", values: payload.revision_reason_codes },
    errorAlert: { style: "stop", title: "原因代码不合法", message: "请使用下拉选项。", show: true },
  };
  sheet.getRange(`O2:O${values.length + 1}`).dataValidation = {
    allowBlank: true,
    rule: { type: "whole", operator: "between", formula1: 0, formula2: 3600 },
    errorAlert: { style: "stop", title: "耗时格式错误", message: "请输入 0–3600 的整数秒。", show: true },
  };
  sheet.getRange(`S2:S${values.length + 1}`).conditionalFormats.add("containsText", { text: "必须", format: { fill: colors.red, font: { bold: true, color: "#9C0006" } } });
  const widths = [18, 18, 22, 28, 24, 55, 34, 30, 45, 20, 24, 16, 27, 35, 14, 36, 52, 45, 26];
  widths.forEach((width, index) => { sheet.getRangeByIndexes(0, index, values.length + 1, 1).format.columnWidth = width; });
  sheet.getRange(`A2:S${values.length + 1}`).format.rowHeight = 52;
}

function addOriginalSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("原结果只读");
  sheet.showGridLines = false;
  const headers = payload.v1_headers;
  const values = matrix(payload.v1_rows, headers);
  sheet.getRangeByIndexes(0, 0, values.length + 1, headers.length).values = [headers, ...values];
  styleHeader(sheet.getRangeByIndexes(0, 0, 1, headers.length));
  const used = sheet.getRangeByIndexes(1, 0, values.length, headers.length);
  used.format = { fill: colors.gray, wrapText: true, verticalAlignment: "top", font: { color: colors.text, size: 9 } };
  applyReadOnlyGuard(used);
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(1);
  sheet.getRangeByIndexes(0, 0, values.length + 1, headers.length).format.columnWidth = 22;
  if (headers.includes("claim_text")) sheet.getRangeByIndexes(0, headers.indexOf("claim_text"), values.length + 1, 1).format.columnWidth = 55;
  if (headers.includes("version_context")) sheet.getRangeByIndexes(0, headers.indexOf("version_context"), values.length + 1, 1).format.columnWidth = 34;
  sheet.getRangeByIndexes(1, 0, values.length, headers.length).format.rowHeight = 45;
}

function addDeclarationSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("回溯声明");
  sheet.showGridLines = false;
  sheet.mergeCells("A1:D1");
  sheet.getRange("A1:D1").values = [[payload.declaration.title]];
  styleTitle(sheet.getRange("A1:D1"));
  sheet.getRange("A3:D3").values = [["字段", "填写值", "输入类型", "说明"]];
  styleHeader(sheet.getRange("A3:D3"));
  const rows = payload.declaration.fields.map(([field, value, kind]) => [field, value, kind, kind === "LOCKED" ? "绑定原始 return identity" : "请如实填写一次"]);
  sheet.getRange(`A4:D${rows.length + 3}`).values = rows;
  applyReadOnlyGuard(sheet.getRange(`A4:A${rows.length + 3}`));
  applyReadOnlyGuard(sheet.getRange(`C4:D${rows.length + 3}`));
  sheet.getRange(`B4:B${rows.length + 3}`).format.fill = colors.yellow;
  for (let index = 0; index < payload.declaration.fields.length; index += 1) {
    const row = index + 4;
    const kind = payload.declaration.fields[index][2];
    if (kind === "LOCKED") applyReadOnlyGuard(sheet.getRange(`B${row}`));
    if (kind === "YES_NO") {
      sheet.getRange(`B${row}`).dataValidation = { ignoreBlanks: true, inCellDropDown: true, rule: { type: "list", values: ["YES", "NO"] }, errorAlert: { style: "stop", title: "值不合法", message: "请选择 YES 或 NO。", show: true } };
    }
  }
  sheet.getRange(`A4:D${rows.length + 3}`).format = { wrapText: true, verticalAlignment: "top" };
  sheet.getRange("A:A").format.columnWidth = 42;
  sheet.getRange("B:B").format.columnWidth = 72;
  sheet.getRange("C:C").format.columnWidth = 16;
  sheet.getRange("D:D").format.columnWidth = 35;
  sheet.getRange(`A4:D${rows.length + 3}`).format.rowHeight = 30;
}

const summaries = [];
const selectedKeys = new Set((args.keys ?? "A1,A2,B1,B2").split(",").map((value) => value.trim()).filter(Boolean));
for (const annotator of ["A", "B"]) {
  for (const phase of [1, 2]) {
    if (!selectedKeys.has(`${annotator}${phase}`)) continue;
    const payloadPath = path.join(payloadRoot, `${annotator}_phase${phase}.json`);
    const payload = JSON.parse(await fs.readFile(payloadPath, "utf8"));
    const workbook = Workbook.create();
    addGuideSheet(workbook, payload);
    addTaskSheet(workbook, payload);
    addOriginalSheet(workbook, payload);
    addDeclarationSheet(workbook, payload);
    const inspect = await workbook.inspect({ kind: "region", sheetId: "需要你复核", range: "A1:S6", maxChars: 2000 });
    const errors = await workbook.inspect({ kind: "match", searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", options: { useRegex: true, maxResults: 100 }, summary: "formula error scan" });
    const outputPath = path.join(outputRoot, `annotator_${annotator}`, `${annotator}_phase${phase}_targeted_rereview.xlsx`);
    const xlsx = await SpreadsheetFile.exportXlsx(workbook);
    await xlsx.save(outputPath);
    await fs.rm(`${outputPath}.inspect.ndjson`, { force: true });
    for (const sheetName of ["先看这里", "需要你复核", "原结果只读", "回溯声明"]) {
      const preview = await workbook.render({ sheetName, autoCrop: "all", scale: 1, format: "png" });
      const safeName = { "先看这里": "guide", "需要你复核": "tasks", "原结果只读": "original", "回溯声明": "declaration" }[sheetName];
      await fs.writeFile(path.join(qaRoot, `${annotator}_phase${phase}_${safeName}.png`), new Uint8Array(await preview.arrayBuffer()));
    }
    summaries.push({ annotator, phase, taskCount: payload.tasks.length, inspect: inspect.ndjson.slice(0, 500), formulaErrors: errors.ndjson });
  }
}
await fs.writeFile(path.join(qaRoot, "workbook_build_summary.json"), JSON.stringify(summaries, null, 2) + "\n", "utf8");
console.log(JSON.stringify(summaries.map(({ annotator, phase, taskCount, formulaErrors }) => ({ annotator, phase, taskCount, formulaErrors })), null, 2));
