import fs from "node:fs/promises";
import path from "node:path";

const artifactToolModule = process.env.CODEX_ARTIFACT_TOOL_MODULE ?? "@oai/artifact-tool";
const { SpreadsheetFile, Workbook } = await import(artifactToolModule);

const args = Object.fromEntries(process.argv.slice(2).map((arg) => {
  const split = arg.indexOf("=");
  if (split < 0) throw new Error(`expected --key=value, got ${arg}`);
  return [arg.slice(2, split), arg.slice(split + 1)];
}));
for (const required of ["payload", "output", "qa-root"]) {
  if (!args[required]) throw new Error(`missing --${required}`);
}
const payload = JSON.parse(await fs.readFile(path.resolve(args.payload), "utf8"));
const outputPath = path.resolve(args.output);
const qaRoot = path.resolve(args["qa-root"]);
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(qaRoot, { recursive: true });

const c = { navy: "#17365D", blue: "#D9EAF7", pale: "#EAF3F8", green: "#E2F0D9", yellow: "#FFF2CC", red: "#FCE4D6", gray: "#E7E6E6", white: "#FFFFFF", text: "#1F2937" };
const wb = Workbook.create();
function title(range) { range.format = { fill: c.navy, font: { bold: true, color: c.white, size: 15 }, verticalAlignment: "center" }; range.format.rowHeight = 30; }
function header(range) { range.format = { fill: c.navy, font: { bold: true, color: c.white, size: 10 }, wrapText: true, verticalAlignment: "center", horizontalAlignment: "center", borders: { preset: "inside", style: "thin", color: "#A6A6A6" } }; range.format.rowHeight = 42; }
function body(range, height = 54) { range.format = { wrapText: true, verticalAlignment: "top", font: { size: 9, color: c.text }, borders: { preset: "inside", style: "hair", color: "#D9D9D9" } }; range.format.rowHeight = height; }
function listValidation(values, titleText) { return { ignoreBlanks: true, inCellDropDown: true, rule: { type: "list", values }, errorAlert: { style: "stop", title: titleText, message: "请只使用下拉列表中的冻结枚举。", show: true } }; }
function widths(sheet, widths, rows) { widths.forEach((width, index) => { sheet.getRangeByIndexes(0, index, rows, 1).format.columnWidth = width; }); }
function safeText(value) { return String(value ?? "").slice(0, 32700); }

const evidenceValues = [];
const evidenceAnchor = {};
for (const row of payload.evidence_rows) {
  const text = String(row.snapshot_text ?? "");
  const parts = [];
  for (let i = 0; i < text.length; i += 30000) parts.push(text.slice(i, i + 30000));
  if (parts.length === 0) parts.push("");
  evidenceAnchor[`${row.sample_id}:${row.evidence_id}`] = evidenceValues.length + 2;
  parts.forEach((part, index) => evidenceValues.push([row.sample_id, row.candidate_text, row.evidence_id, row.title, row.url, row.snapshot_sha256, `${index + 1}/${parts.length}`, safeText(part)]));
}

const intro = wb.worksheets.add("00_使用说明"); intro.showGridLines = false; intro.mergeCells("A1:H1"); intro.getRange("A1:H1").values = [["Pilot4 A/B Owner 盲态仲裁工作簿 V1"]]; title(intro.getRange("A1:H1"));
const introRows = [
  ["当前用途", "先冻结 A/B 原始一致性，再由 Owner 在不知道 Expected V3 的情况下完成候选缺陷分流和实质字段仲裁。"],
  ["严格盲态", "Expected V3 未加载、未比较、未写入本工作簿；A/B 原始值均只读。"],
  ["步骤 1", "先完成 Sheet 01 的 5 个 Candidate 缺陷决定与理由。不得跳过。"],
  ["步骤 2", "再完成 Sheet 02。状态为 READY_FOR_OWNER_ADJUDICATION 的行才允许填写最终值；其他状态保持空白。"],
  ["缺陷分流", payload.defect_routing_rule],
  ["填写区域", "只填写黄色单元格。Owner 决策必须来自下拉枚举；理由必须具体说明采用该值的依据。"],
  ["证据阅读", "点击 Sheet 01/02 中的内部链接跳到 Sheet 03；外部 URL 仅作 provenance，冻结正文是本轮证据。"],
  ["禁止事项", "不得修改候选、A/B 原始值、证据；不得把 Expected 当成答案；不得在本轮生成 Ground Truth。"],
  ["提交", "完成 Sheet 05 检查后，以原 XLSX 格式返回。后续任务会先锁定原始字节和 SHA256，再导入决定。"],
];
intro.getRange(`A3:B${introRows.length + 2}`).values = introRows; intro.getRange(`A3:A${introRows.length + 2}`).format = { fill: c.blue, font: { bold: true, color: c.navy }, wrapText: true }; intro.getRange(`B3:B${introRows.length + 2}`).format = { wrapText: true, verticalAlignment: "top" }; widths(intro, [24, 105], 20); intro.getRange(`A3:B${introRows.length + 2}`).format.rowHeight = 48;

const defect = wb.worksheets.add("01_五个Candidate缺陷优先判定"); defect.showGridLines = false;
const defectHeaders = ["sample_id", "triplet_id", "candidate_text", "source_title", "A phase1_issue", "A phase1_reason", "B phase1_issue", "B phase1_reason", "A overall", "B overall", "A version", "B version", "A authority", "B authority", "A minimum", "B minimum", "E1 title", "E1 URL", "E1 冻结证据", "E2 title", "E2 URL", "E2 冻结证据", "Owner Candidate缺陷决定", "Owner缺陷理由", "后续路由状态"];
const defectValues = payload.defect_rows.map((r) => [r.sample_id,r.triplet_id,r.candidate_text,r.source_title,r.a_phase1_issue,r.a_phase1_reason,r.b_phase1_issue,r.b_phase1_reason,r.a_overall,r.b_overall,r.a_version,r.b_version,r.a_authority,r.b_authority,r.a_minimum,r.b_minimum,r.e1_title,r.e1_url,"查看 E1 冻结正文",r.e2_title,r.e2_url,"查看 E2 冻结正文","","",""]);
defect.getRangeByIndexes(0,0,defectValues.length+1,defectHeaders.length).values=[defectHeaders,...defectValues]; header(defect.getRangeByIndexes(0,0,1,defectHeaders.length)); body(defect.getRangeByIndexes(1,0,defectValues.length,defectHeaders.length),95); defect.freezePanes.freezeRows(1); defect.freezePanes.freezeColumns(2);
defect.getRange("W2:X6").clear({ applyTo: "contents" });
defect.getRangeByIndexes(1,22,defectValues.length,2).format.fill=c.yellow; defect.getRangeByIndexes(1,22,defectValues.length,1).dataValidation=listValidation(["CONFIRMED_DEFECT","ANNOTATOR_INTERPRETATION_VARIANCE","NEEDS_TARGETED_REREVIEW"],"Owner Candidate 缺陷决定不合法");
for (let i=0;i<defectValues.length;i++) { const row=i+2; const sample=payload.defect_rows[i].sample_id; defect.getRange(`Y${row}`).formulas=[[`=IF(W${row}="","WAITING_FOR_DEFECT_TRIAGE",IF(W${row}="CONFIRMED_DEFECT","QUARANTINED_NO_GT_ADJUDICATION",IF(W${row}="NEEDS_TARGETED_REREVIEW","ON_HOLD_TARGETED_REREVIEW","READY_FOR_OWNER_ADJUDICATION")))`]]; defect.getRange(`S${row}`).formulas=[[`=HYPERLINK("#'03_证据详情'!A${evidenceAnchor[`${sample}:E1`]}","查看 E1 冻结正文")`]]; defect.getRange(`V${row}`).formulas=[[`=HYPERLINK("#'03_证据详情'!A${evidenceAnchor[`${sample}:E2`]}","查看 E2 冻结正文")`]]; }
widths(defect,[19,12,68,28,18,42,18,42,28,28,28,28,28,28,30,30,28,38,18,28,38,18,34,48,38],defectValues.length+1);

const ordinary = wb.worksheets.add("02_普通字段仲裁"); ordinary.showGridLines=false;
const ordinaryHeaders=["sample_id","triplet_id","phase","field","candidate_text","A blind_review_id","A value","A reason","B blind_review_id","B value","B reason","E1 冻结证据","E2 冻结证据","Guide规则摘要","当前状态","Owner最终值","Owner仲裁理由"];
const ordinaryValues=payload.ordinary_rows.map((r)=>[r.sample_id,r.triplet_id,r.phase,r.field,r.candidate_text,r.a_blind_review_id,r.a_value,r.a_reason,r.b_blind_review_id,r.b_value,r.b_reason,r.phase==="PHASE2"?"查看 E1":"N/A",r.phase==="PHASE2"?"查看 E2":"N/A",r.guide_rule,"","",""]);
ordinary.getRangeByIndexes(0,0,ordinaryValues.length+1,ordinaryHeaders.length).values=[ordinaryHeaders,...ordinaryValues]; header(ordinary.getRangeByIndexes(0,0,1,ordinaryHeaders.length)); body(ordinary.getRangeByIndexes(1,0,ordinaryValues.length,ordinaryHeaders.length),78); ordinary.freezePanes.freezeRows(1); ordinary.freezePanes.freezeColumns(4); ordinary.getRangeByIndexes(1,15,ordinaryValues.length,2).format.fill=c.yellow;
ordinary.getRange("P2:Q79").clear({ applyTo: "contents" });
const defectRowBySample=Object.fromEntries(payload.defect_rows.map((r,i)=>[r.sample_id,i+2]));
for(let i=0;i<payload.ordinary_rows.length;i++){ const excel=i+2; const r=payload.ordinary_rows[i]; const drow=defectRowBySample[r.sample_id]; const status=drow?`=IF('01_五个Candidate缺陷优先判定'!W${drow}="","WAITING_FOR_DEFECT_TRIAGE",IF('01_五个Candidate缺陷优先判定'!W${drow}="CONFIRMED_DEFECT","QUARANTINED_NO_GT_ADJUDICATION",IF('01_五个Candidate缺陷优先判定'!W${drow}="NEEDS_TARGETED_REREVIEW","ON_HOLD_TARGETED_REREVIEW","READY_FOR_OWNER_ADJUDICATION")))`:`="READY_FOR_OWNER_ADJUDICATION"`; ordinary.getRange(`O${excel}`).formulas=[[status]]; ordinary.getRange(`P${excel}`).dataValidation=listValidation(r.allowed_values,`${r.field} 枚举不合法`); if(r.phase==="PHASE2"){ const e1=evidenceAnchor[`${r.sample_id}:E1`]; const e2=evidenceAnchor[`${r.sample_id}:E2`]; ordinary.getRange(`L${excel}`).formulas=[[`=HYPERLINK("#'03_证据详情'!A${e1}","查看 E1")`]]; ordinary.getRange(`M${excel}`).formulas=[[`=HYPERLINK("#'03_证据详情'!A${e2}","查看 E2")`]]; }}
widths(ordinary,[19,12,10,34,68,22,30,48,22,30,48,16,16,55,40,36,52],ordinaryValues.length+1);

const evidence=wb.worksheets.add("03_证据详情"); evidence.showGridLines=false; const evidenceHeaders=["sample_id","candidate_text","Evidence ID","官方标题","官方 URL","snapshot SHA256","正文分段","冻结 Evidence 正文"];
evidence.getRangeByIndexes(0,0,evidenceValues.length+1,evidenceHeaders.length).values=[evidenceHeaders,...evidenceValues]; header(evidence.getRangeByIndexes(0,0,1,evidenceHeaders.length)); body(evidence.getRangeByIndexes(1,0,evidenceValues.length,evidenceHeaders.length),110); evidence.freezePanes.freezeRows(1); evidence.freezePanes.freezeColumns(3); widths(evidence,[19,68,12,35,48,66,12,115],evidenceValues.length+1);

const enumSheet=wb.worksheets.add("04_枚举速查"); enumSheet.showGridLines=false; const enumHeaders=["field","canonical enum","中文解释/选择口径","边界提醒"]; const cn={NATURAL:"表达自然",MINOR_ISSUE:"轻微表达问题",UNNATURAL:"明显不自然",YES:"存在文本内部冲突",NO:"不存在文本内部冲突",UNCERTAIN:"文本自身含糊导致无法判断",NONE:"无此类问题",MISSING_CONTEXT:"缺少理解核心命题所必需的信息",AMBIGUOUS_REFERENCE:"关键指代有多个合理解释",OTHER:"其他实质文本/流程问题",CURRENTLY_CONSISTENT:"证据支持且不只是历史上成立",LEGITIMATE_VERSION_OR_HISTORY:"仅在过去版本或历史时期成立",FACTUAL_CONFLICT:"证据否定且不能由合法版本解释",INSUFFICIENT_EVIDENCE:"冻结证据不足以可靠判断",NOT_PRESENT:"未提出该类命题",PRESENT_CORRECT:"提出且证据支持",PRESENT_INCORRECT:"提出且证据否定",PRESENT_EVIDENCE_INSUFFICIENT:"提出但证据不足",ONE_OFFICIAL_EVIDENCE:"任一单独官方证据足以确认冲突",MULTI_EVIDENCE_OR_VERSION_CHAIN:"必须联合多证据或版本链才能确认冲突",NOT_APPLICABLE:"该字段在当前事实状态下不适用",SOURCE_UNREACHABLE:"指定来源无法访问",SOURCE_CONFLICT:"指定证据相互冲突",EVIDENCE_MISSING:"证据池缺少判断所需证据",LATE_DISCOVERED_CANDIDATE_DEFECT:"后期发现候选本身有缺陷"}; const enumRows=[]; for(const [field,values] of Object.entries(payload.enums)){ for(const value of values) enumRows.push([field,value,cn[value]??value,payload.guide_rules[field]]); } enumSheet.getRangeByIndexes(0,0,enumRows.length+1,4).values=[enumHeaders,...enumRows]; header(enumSheet.getRange("A1:D1")); body(enumSheet.getRangeByIndexes(1,0,enumRows.length,4),44); enumSheet.freezePanes.freezeRows(1); widths(enumSheet,[36,40,50,90],enumRows.length+1);

const checks=wb.worksheets.add("05_提交检查"); checks.showGridLines=false; checks.mergeCells("A1:D1"); checks.getRange("A1:D1").values=[["Owner 提交前检查"]]; title(checks.getRange("A1:D1")); checks.getRange("A3:D3").values=[["检查项","期望","当前公式结果","状态"]]; header(checks.getRange("A3:D3")); const checkRows=[
  ["5 个缺陷决定已填写",5,`=COUNTA('01_五个Candidate缺陷优先判定'!W2:W6)`,`=IF(C4=B4,"PASS","PENDING")`],
  ["5 个缺陷理由已填写",5,`=COUNTA('01_五个Candidate缺陷优先判定'!X2:X6)`,`=IF(C5=B5,"PASS","PENDING")`],
  ["可仲裁普通字段已填写",`=COUNTIF('02_普通字段仲裁'!O2:O79,"READY_FOR_OWNER_ADJUDICATION")`,`=COUNTIFS('02_普通字段仲裁'!O2:O79,"READY_FOR_OWNER_ADJUDICATION",'02_普通字段仲裁'!P2:P79,"<>")`,`=IF(C6=B6,"PASS","PENDING")`],
  ["已填普通字段均有理由",`=COUNTIF('02_普通字段仲裁'!P2:P79,"<>")`,`=COUNTIF('02_普通字段仲裁'!Q2:Q79,"<>")`,`=IF(C7=B7,"PASS","PENDING")`],
  ["隔离/暂停行未填写最终值",0,`=COUNTIFS('02_普通字段仲裁'!O2:O79,"<>READY_FOR_OWNER_ADJUDICATION",'02_普通字段仲裁'!P2:P79,"<>")`,`=IF(C8=B8,"PASS","BLOCKER")`],
]; checks.getRange("A4:B8").values=checkRows.map(r=>r.slice(0,2)); checks.getRange("C4:C8").formulas=checkRows.map(r=>[r[2]]); checks.getRange("D4:D8").formulas=checkRows.map(r=>[r[3]]); body(checks.getRange("A4:D8"),44); checks.getRange("D4:D8").format.fill=c.yellow; widths(checks,[46,26,26,18],12);

const stats=wb.worksheets.add("06_一致性统计"); stats.showGridLines=false; stats.mergeCells("A1:H1"); stats.getRange("A1:H1").values=[["Pilot4 A/B 仲裁前原始一致性冻结（Expected 未加载）"]]; title(stats.getRange("A1:H1")); stats.getRange("A3:H3").values=[["阶段","字段","N","一致","分歧","Raw agreement","Cohen kappa","解释"]]; header(stats.getRange("A3:H3")); const statRows=[]; for(const [phase,obj] of [["Phase1",payload.stats.phase1],["Phase2",payload.stats.phase2]]){ for(const [field,m] of Object.entries(obj.field_metrics)){ statRows.push([phase,field,m.n,m.matches,m.disagreements,m.raw_agreement,m.cohen_kappa??"NOT_ESTIMABLE",field==="evidence_selection"?"PROCESS_ONLY":(phase==="Phase1"?"QC / Candidate quality":"CORE LABEL REPRODUCIBILITY")]); }} statRows.push(["Phase1","text_naturalness linear weighted kappa",72,"","","",payload.stats.phase1.field_metrics.text_naturalness.linear_weighted_kappa_supplementary,"SUPPLEMENTARY_ONLY; protocol 未定义加权方案"]); statRows.push(["All","Gwet AC1","","","","","NOT_COMPUTED","无现成稳定项目实现，不为本轮新增算法"]); stats.getRangeByIndexes(3,0,statRows.length,8).values=statRows; body(stats.getRangeByIndexes(3,0,statRows.length,8),42); widths(stats,[12,40,10,10,10,18,22,52],statRows.length+4); stats.getRange("A2:H2").merge(); stats.getRange("A2:H2").values=[["本表仅描述裁决前 A/B 原始复现性；没有事后通过阈值，没有 Expected accuracy，也不把 evidence_selection 或 derived stealth 当作直接仲裁标签。"]]; stats.getRange("A2:H2").format={fill:c.red,font:{bold:true,color:"#9C0006"},wrapText:true}; stats.getRange("A2:H2").format.rowHeight=38;

await wb.recalculate();
const inspect = await wb.inspect({ kind: "workbook,sheet,table", maxChars: 12000, tableMaxRows: 12, tableMaxCols: 18, tableMaxCellChars: 120 });
await fs.writeFile(path.join(qaRoot,"workbook_inspect.ndjson"),inspect.ndjson,"utf8");
for(const [sheetName,range] of [["00_使用说明","A1:B11"],["01_五个Candidate缺陷优先判定","A1:Y6"],["02_普通字段仲裁","A1:Q18"],["03_证据详情","A1:H8"],["04_枚举速查","A1:D32"],["05_提交检查","A1:D8"],["06_一致性统计","A1:H20"]]){ const image=await wb.render({sheetName,range,scale:1,format:"png"}); await fs.writeFile(path.join(qaRoot,`${sheetName}.png`),new Uint8Array(await image.arrayBuffer())); }
const formulaScan=await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:200},summary:"formula error scan"}); await fs.writeFile(path.join(qaRoot,"formula_error_scan.ndjson"),formulaScan.ndjson,"utf8");
const exported=await SpreadsheetFile.exportXlsx(wb); await exported.save(outputPath);
console.log(JSON.stringify({output:outputPath,defectRows:payload.defect_rows.length,ordinaryRows:payload.ordinary_rows.length,evidenceRows:evidenceValues.length,expectedLoaded:payload.expected_v3_loaded}));
