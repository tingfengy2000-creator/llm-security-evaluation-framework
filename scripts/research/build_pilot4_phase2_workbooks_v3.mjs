import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";

const artifactToolModule = process.env.CODEX_ARTIFACT_TOOL_MODULE ?? "@oai/artifact-tool";
const { FileBlob, SpreadsheetFile, Workbook } = await import(artifactToolModule);

const args = Object.fromEntries(
  process.argv.slice(2).map((arg) => {
    const split = arg.indexOf("=");
    if (split < 0) throw new Error(`expected --key=value, got ${arg}`);
    return [arg.slice(2, split), arg.slice(split + 1)];
  }),
);
for (const required of ["mode", "payload-dir", "output-root", "qa-root"]) {
  if (!args[required]) throw new Error(`missing --${required}`);
}

const mode = args.mode;
const payloadDir = path.resolve(args["payload-dir"]);
const outputRoot = path.resolve(args["output-root"]);
const qaRoot = path.resolve(args["qa-root"]);
await fs.mkdir(outputRoot, { recursive: true });
await fs.mkdir(qaRoot, { recursive: true });

const colors = {
  ink: "#1F2937",
  navy: "#17365D",
  blue: "#D9EAF7",
  paleBlue: "#EEF5FB",
  gray: "#E7E6E6",
  yellow: "#FFF2CC",
  orange: "#FCE4D6",
  green: "#E2F0D9",
  red: "#F4CCCC",
  white: "#FFFFFF",
  border: "#B8C3CF",
};
const font = "Arial";

function normalizeCell(value) {
  if (value === null || value === undefined) return "";
  if (Array.isArray(value)) return value.join(" | ");
  if (typeof value === "object") return JSON.stringify(value);
  return value;
}

function titleStyle(range) {
  range.format = {
    font: { name: font, bold: true, color: colors.navy, size: 14 },
    verticalAlignment: "center",
  };
  range.format.rowHeight = 26;
}

function headerStyle(range) {
  range.format = {
    fill: colors.navy,
    font: { name: font, bold: true, color: colors.white, size: 10 },
    wrapText: true,
    horizontalAlignment: "center",
    verticalAlignment: "center",
    borders: { preset: "inside", style: "thin", color: colors.white },
  };
  range.format.rowHeight = 54;
}

function bodyStyle(range, rowHeight = 54) {
  range.format = {
    font: { name: font, color: colors.ink, size: 10 },
    wrapText: true,
    verticalAlignment: "top",
    borders: { preset: "inside", style: "hair", color: colors.border },
  };
  range.format.rowHeight = rowHeight;
}

function chunks(text, size = 800) {
  const result = [];
  for (let start = 0; start < text.length; start += size) result.push(text.slice(start, start + size));
  return result.length > 0 ? result : [""];
}

const FIELD_MANUAL_ROWS = [
  ["固定流程", "填写顺序", "先读 Candidate，再读 E1/E2；先判断证据是否充分，再依次填 overall、version、authority、minimum、selection、issue、reason。", "不得先猜答案，也不得跳过证据充分性。", "STEP 1–10", "minimum 只在 FACTUAL_CONFLICT 中判断；reason 每行必填。", "先填自己熟悉的列、最后批量补其它列。", "某城市交通卡押金例仅用于理解流程，不对应本项目候选。"],
  ["overall_fact_status", "整体事实状态", "Candidate 核心命题在指定 E1/E2 下属于当前成立、合法历史、事实冲突还是证据不足。", "不判断语言自然度，也不把个人常识当 Evidence。", "CURRENTLY_CONSISTENT", "证据支持候选作为当前事实成立。", "看到历史年份就自动选历史。", "E1 明确支持某公共展馆当前周二闭馆，Candidate 同样陈述 → CURRENTLY_CONSISTENT。"],
  ["overall_fact_status", "整体事实状态", "同上。", "同上。", "LEGITIMATE_VERSION_OR_HISTORY", "候选只在合法历史时期/旧版本下成立；按当前状态理解会改变真假或核心含义。", "仅因文本出现发布日期就选择该值。", "旧版公园年卡可转让、新版不可转让；Candidate 明确说旧版规则 → LEGITIMATE_VERSION_OR_HISTORY。"],
  ["overall_fact_status", "整体事实状态", "同上。", "同上。", "FACTUAL_CONFLICT", "Evidence 否定核心事实，且没有合法时间、版本或条件解释。", "Evidence 不足仍强行判冲突。", "Candidate 称当前限额为 8 件，E1 当前规则明确为 5 件 → FACTUAL_CONFLICT。"],
  ["overall_fact_status", "整体事实状态", "同上。", "同上。", "INSUFFICIENT_EVIDENCE", "当前提供的 E1/E2 不足以稳定判断。", "因为内容难读就选择证据不足。", "Candidate 主张 2018 年曾暂停服务，但 E1/E2 都未涵盖 2018 年状态 → INSUFFICIENT_EVIDENCE。"],
  ["overall_fact_status", "判断树", "第一问：证据足够吗？NO → INSUFFICIENT_EVIDENCE。YES 后问：核心事实被否定且无合法解释吗？YES → FACTUAL_CONFLICT。否则问：只有放在历史时期/旧版本才成立，按当前状态理解会改变真假或核心含义吗？YES → LEGITIMATE_VERSION_OR_HISTORY；NO → CURRENTLY_CONSISTENT。", "不判断 Evidence 本身的权威等级。", "严格顺序", "命中一步后停止。", "先看到日期就跳过第一问。", "先确定证据充分性，再处理冲突和历史边界。"],
  ["overall_fact_status", "当前时点替换测试", "问：如果去掉 Candidate 的历史/版本限定，把它当成当前状态来读，真假或核心含义会不会变化？", "不是只检查有没有年份。", "PRESENT-TIME SUBSTITUTION TEST", "不会变化时可能仍是 CURRENTLY_CONSISTENT；会变化且历史命题获支持时才是 LEGITIMATE_VERSION_OR_HISTORY。", "把任何过去日期都当历史状态。", "“制度于 2019 年发布且目前仍有效”中的发布日期本身不必改变当前真假。"],
  ["version_claim_status", "版本命题状态", "Candidate 自己是否表达修订、废止、替代、生效、前后版本或时间适用关系，以及该关系是否获证据支持。", "不因 Evidence 中出现日期就自动构成 Candidate 的 version claim。", "NOT_PRESENT", "Candidate 没有明确版本/时效关系。", "Evidence 有两个年份就填 PRESENT。", "Candidate 只说当前费用为 20 元，没有版本关系 → NOT_PRESENT。"],
  ["version_claim_status", "版本命题状态", "同上。", "同上。", "PRESENT_CORRECT", "明确版本关系被 E1/E2 支持。", "只见到年份但没有关系命题。", "Candidate 称新版自某日替代旧版，E1/E2 支持该关系 → PRESENT_CORRECT。"],
  ["version_claim_status", "版本命题状态", "同上。", "同上。", "PRESENT_INCORRECT", "明确版本关系被 E1/E2 否定。", "证据不足时不能使用。", "Candidate 称第二版早于第一版，E1/E2 日期明确相反 → PRESENT_INCORRECT。"],
  ["version_claim_status", "版本命题状态", "同上。", "同上。", "PRESENT_EVIDENCE_INSUFFICIENT", "版本命题明确存在，但指定 Evidence 无法判断正误。", "Candidate 连版本主体都不清楚时仍正常填写。", "Candidate 称 2016 版仍有效，E1/E2 没有效力信息 → PRESENT_EVIDENCE_INSUFFICIENT。"],
  ["authority_claim_status", "权威归属命题状态", "Candidate 是否对发布者、制定机关、通过机关、主管机关、官方转载主体等身份作出可核验 claim。", "网页 host 不自动等同 issuing authority。", "NOT_PRESENT", "没有明确机关或权限归属主张。", "只因来源页有机关名称就判 present。", "Candidate 仅陈述开放时间，没有主体归属 → NOT_PRESENT。"],
  ["authority_claim_status", "权威归属命题状态", "同上。", "同上。", "PRESENT_CORRECT", "明确归属被 Evidence 支持。", "把转载机关当制定机关。", "Candidate 称市议事机构通过规则，E1 决议正文支持 → PRESENT_CORRECT。"],
  ["authority_claim_status", "权威归属命题状态", "同上。", "同上。", "PRESENT_INCORRECT", "明确归属被 Evidence 反驳。", "Evidence 未说明机关仍强判错误。", "Candidate 把规则制定者写成网页维护单位，E1/E2明确区分两者 → PRESENT_INCORRECT。"],
  ["authority_claim_status", "权威归属命题状态", "同上。", "同上。", "PRESENT_EVIDENCE_INSUFFICIENT", "明确归属存在，但 E1/E2 不足以判断。", "Candidate 没有归属命题时使用。", "Candidate 称某委员会有审批权，材料只载明发布信息 → PRESENT_EVIDENCE_INSUFFICIENT。"],
  ["minimum_external_evidence_needed", "最少外部证据需求", "仅当 overall=FACTUAL_CONFLICT 时，判断确认冲突的最低充分证据。", "不记录实际看了几份。", "ONE_OFFICIAL_EVIDENCE", "E1 alone sufficient 或 E2 alone sufficient。", "实际看了两份就自动选 MULTI。", "E1 当前限额直接反驳 Candidate，E2 只是补充 → ONE_OFFICIAL_EVIDENCE。"],
  ["minimum_external_evidence_needed", "最少外部证据需求", "同上。", "同上。", "MULTI_EVIDENCE_OR_VERSION_CHAIN", "E1 单独不足、E2 单独不足，只有 E1+E2 联合才足够。", "两份都看过但任一单独已足够。", "E1 给旧规则，E2 给替代时间，联合才能证明当前冲突 → MULTI_EVIDENCE_OR_VERSION_CHAIN。"],
  ["minimum_external_evidence_needed", "最少外部证据需求", "同上。", "同上。", "NOT_APPLICABLE", "overall 不是 FACTUAL_CONFLICT 时必须选择。", "非冲突仍填 ONE 或 MULTI。", "CURRENTLY_CONSISTENT / HISTORY / INSUFFICIENT 三种状态均填 NOT_APPLICABLE。"],
  ["evidence_selection", "实际使用证据", "记录你实际用了哪些 Evidence。", "不是理论最少需要几个。", "NONE / E1 / E2 / E1+E2", "按实际阅读并用于判断的路径填写。", "把 minimum 直接复制到 selection。", "实际看 E1+E2，但 E1 单独已足够：selection=E1+E2，minimum=ONE_OFFICIAL_EVIDENCE。"],
  ["phase2_issue", "Phase2 问题", "是否发生证据不可用、互相冲突、缺失、Candidate 后期质量缺陷或其它实际 review blocker。", "事实错误本身不是 issue。", "NONE", "证据可用且无流程/材料问题。", "把普通 FACTUAL_CONFLICT 也标为 issue。", "Evidence 可读并足以确认冲突 → issue 仍可为 NONE。"],
  ["phase2_issue", "Phase2 问题", "同上。", "同上。", "SOURCE_UNREACHABLE", "URL 与冻结正文都无法使用，导致来源不可访问。", "live URL 暂时打不开但 frozen snapshot 可读。", "只有两个通道均无法使用并影响判断时才选。"],
  ["phase2_issue", "Phase2 问题", "同上。", "同上。", "SOURCE_CONFLICT", "E1/E2 存在无法解决的实质冲突。", "表述角度不同但结论一致。", "E1/E2 对同一时点给出互斥规则且无法解释 → SOURCE_CONFLICT。"],
  ["phase2_issue", "Phase2 问题", "同上。", "同上。", "EVIDENCE_MISSING", "指定 Evidence 缺少判断核心命题所需材料。", "不想继续阅读。", "版本效力命题存在，但两份材料都无效力信息 → EVIDENCE_MISSING。"],
  ["phase2_issue", "Phase2 问题", "同上。", "同上。", "LATE_DISCOVERED_CANDIDATE_DEFECT", "Phase2 才发现 Candidate 本身有实质结构/上下文缺陷。", "普通事实错误。", "Candidate 的核心主体无法唯一识别 → LATE_DISCOVERED_CANDIDATE_DEFECT。"],
  ["phase2_issue", "Phase2 问题", "同上。", "同上。", "OTHER", "其它实际影响核验的 blocker，必须解释。", "作为不确定性的万能选项。", "遇到不属于既有五类的真实阻塞时使用并写明。"],
  ["phase2_reason", "第二阶段理由", "用 1–3 句话说明 Candidate 核心命题、E1/E2 证明了什么，以及为什么选择当前 status。", "不写实验标签、不猜类别、不引用未提供答案。", "自由文本｜72/72 必填", "每行都必须填写；简短、具体、绑定 Evidence。", "只写“正确”或“错误”。", "Candidate 称当前限额为8；E1正文规定为5且E2无历史例外，因此选择 FACTUAL_CONFLICT。"],
];

const EXAMPLE_ROWS = [
  ["教学例1｜当前一致", "海星市公共阅览室当前周二闭馆。", "E1：现行开放规则写明周二闭馆。｜E2：本月公告沿用该规则。", "CURRENTLY_CONSISTENT", "NOT_PRESENT", "NOT_PRESENT", "NOT_APPLICABLE", "E1+E2", "NONE", "Candidate 的当前闭馆日同时获 E1 与 E2 支持，因此选择当前一致。", "日期只是当前安排，不构成版本命题。"],
  ["教学例2｜合法历史", "北湾公园2018年版年卡允许转让。", "E1：2018年版载明可转让。｜E2：2023年新版改为不可转让并替代旧版。", "LEGITIMATE_VERSION_OR_HISTORY", "PRESENT_CORRECT", "NOT_PRESENT", "NOT_APPLICABLE", "E1+E2", "NONE", "E1支持2018年历史规则，E2说明新版已经替代；按当前状态理解会改变核心含义。", "通过当前时点替换测试。"],
  ["教学例3｜冲突+单证据", "云岭展馆当前每人可预约8张票。", "E1：现行预约规则明确每人5张。｜E2：只说明预约入口。", "FACTUAL_CONFLICT", "NOT_PRESENT", "NOT_PRESENT", "ONE_OFFICIAL_EVIDENCE", "E1+E2", "NONE", "E1单独已明确反驳8张的核心数量；E2仅用于确认场景。", "实际看两份不改变最低只需一份。"],
  ["教学例4｜冲突+多证据", "溪谷步道旧季票在新规则生效后仍可无限期使用。", "E1：旧规则没有终止时间。｜E2：新规则写明生效日并明确旧季票仅过渡30日。", "FACTUAL_CONFLICT", "PRESENT_INCORRECT", "NOT_PRESENT", "MULTI_EVIDENCE_OR_VERSION_CHAIN", "E1+E2", "NONE", "E1识别旧季票条款，E2提供替代日和30日过渡；两者联合才足以否定无限期使用。", "E1/E2 单独都不足。"],
  ["教学例5｜证据不足", "青禾服务站在2016年曾暂停夜间窗口。", "E1：提供2015年安排。｜E2：提供2017年安排；两者均未覆盖2016年。", "INSUFFICIENT_EVIDENCE", "NOT_PRESENT", "NOT_PRESENT", "NOT_APPLICABLE", "E1+E2", "EVIDENCE_MISSING", "Candidate 的2016年状态未被指定证据覆盖，无法稳定判断。", "不能用相邻年份推断。"],
  ["教学例6｜权威归属正确", "枫桥交通委员会通过了该公交换乘规则。", "E1：委员会会议决议载明通过。｜E2：交通局发布执行通知。", "CURRENTLY_CONSISTENT", "NOT_PRESENT", "PRESENT_CORRECT", "NOT_APPLICABLE", "E1+E2", "NONE", "E1直接支持通过机关，E2说明执行发布；两种角色没有混淆。", "网页发布者不自动等于通过机关。"],
  ["教学例7｜权威归属错误", "网站维护中心制定并通过了城市花园管理规则。", "E1：页面标注维护中心只负责网站运维。｜E2：市园林委员会决议载明制定并通过。", "FACTUAL_CONFLICT", "NOT_PRESENT", "PRESENT_INCORRECT", "MULTI_EVIDENCE_OR_VERSION_CHAIN", "E1+E2", "NONE", "E1与E2联合区分网页维护者和制定通过机关，Candidate 的权威归属错误。", "需要角色链联合判断。"],
  ["教学例8｜版本命题错误", "海港票务办法第二版于第一版之前生效。", "E1：第一版生效日为2020年。｜E2：第二版生效日为2022年。", "FACTUAL_CONFLICT", "PRESENT_INCORRECT", "NOT_PRESENT", "MULTI_EVIDENCE_OR_VERSION_CHAIN", "E1+E2", "NONE", "两份证据分别给出两个版本日期，联合证明第二版晚于第一版，Candidate 的先后关系错误。", "版本先后是 Candidate 明确提出的命题。"],
];

const CHECKLIST_ROWS = [
  "72 行全部完成",
  "没改 blind_review_id",
  "没改 Candidate",
  "overall_fact_status 全填",
  "version_claim_status 全填",
  "authority_claim_status 全填",
  "minimum_external_evidence_needed 全填",
  "evidence_selection 全填",
  "phase2_issue 全填",
  "phase2_reason 72/72 非空",
  "非 FACTUAL_CONFLICT 的 minimum 全部为 NOT_APPLICABLE",
  "没使用 Expected",
  "没看另一 annotator 答案",
  "没使用 LLM assistant",
  "没添加、删除或排序 row",
];

function addMainSheet(workbook, payload, evidenceAnchors) {
  const sheet = workbook.worksheets.add("01_标注表");
  sheet.showGridLines = false;
  sheet.getRange("A1").values = [[`Pilot4 ${payload.annotator} Phase2 人工标注工作簿 V3`]];
  titleStyle(sheet.getRange("A1:M1"));
  sheet.getRange("A2").values = [["只填写带【请填写】/【必须填写】的七列；点击查看E1/E2跳转证据；每行 reason 必填；不要改 ID、Candidate、Evidence、行列或顺序。"]];
  sheet.getRange("A2:M2").format = { font: { name: font, italic: true, color: colors.navy, size: 10 } };

  const canonicalHeaders = [
    "blind_review_id",
    "candidate_text",
    "source_title",
    "view_e1",
    "view_e2",
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
    "filling_check",
  ];
  sheet.getRange("A3:M3").values = [canonicalHeaders.map((key) => payload.display_headers[key])];
  headerStyle(sheet.getRange("A3:M3"));
  const values = payload.rows.map((row) => [
    row.blind_review_id,
    row.candidate_text,
    row.source_title,
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
  ]);
  sheet.getRangeByIndexes(3, 0, values.length, values[0].length).values = values;
  bodyStyle(sheet.getRange("A4:M75"), 82);
  sheet.getRange("A4:E75").format.fill = colors.gray;
  sheet.getRange("F4:K75").format.fill = colors.yellow;
  sheet.getRange("L4:L75").format.fill = colors.orange;
  sheet.getRange("M4:M75").format.fill = colors.paleBlue;
  sheet.getRange("F4:L75").format.borders = { preset: "inside", style: "thin", color: colors.navy };
  sheet.getRange("F3:L3").format.font = { name: font, bold: true, color: colors.white, size: 10 };

  payload.rows.forEach((row, index) => {
    const excelRow = index + 4;
    const anchors = evidenceAnchors[row.blind_review_id];
    sheet.getRange(`D${excelRow}`).formulas = [[`=HYPERLINK("#'02_证据'!A${anchors.E1}","查看E1")`]];
    sheet.getRange(`E${excelRow}`).formulas = [[`=HYPERLINK("#'02_证据'!A${anchors.E2}","查看E2")`]];
    sheet.getRange(`M${excelRow}`).formulas = [[
      `=IF(OR(COUNTBLANK(F${excelRow}:K${excelRow})>0,L${excelRow}=""),"缺少填写",IF(AND(F${excelRow}<>"FACTUAL_CONFLICT",I${excelRow}<>"NOT_APPLICABLE"),"minimum逻辑不一致",IF(AND(F${excelRow}="FACTUAL_CONFLICT",I${excelRow}="NOT_APPLICABLE"),"minimum逻辑不一致","OK")))`,
    ]];
  });

  const validationSpecs = [
    ["F4:F75", payload.phase2_enums.overall_fact_status, "整体事实状态", "先判断证据是否充分，再判断冲突，再判断是否必须依赖历史/版本才能成立。"],
    ["G4:G75", payload.phase2_enums.version_claim_status, "版本命题", "只判断 Candidate 自己是否提出版本/时效关系，以及 Evidence 是否支持。"],
    ["H4:H75", payload.phase2_enums.authority_claim_status, "权威归属", "区分发布者、制定/通过机关、主管机关、转载主体和网页 host。"],
    ["I4:I75", payload.phase2_enums.minimum_external_evidence_needed, "最少证据", "仅 FACTUAL_CONFLICT 使用；非冲突必须填 NOT_APPLICABLE。"],
    ["J4:J75", payload.phase2_enums.evidence_selection, "实际使用证据", "填写你实际使用的 Evidence，不是理论最少需要几个。"],
    ["K4:K75", payload.phase2_enums.phase2_issue, "Phase2 问题", "事实错误本身不是 issue；冻结正文可读时不能只因 live URL 暂时失败选择 SOURCE_UNREACHABLE。"],
  ];
  for (const [rangeAddress, enums, promptTitle, promptMessage] of validationSpecs) {
    sheet.getRange(rangeAddress).dataValidation = {
      ignoreBlanks: false,
      inCellDropDown: true,
      rule: { type: "list", values: enums },
      prompt: { title: promptTitle, message: promptMessage, show: true },
      errorAlert: {
        style: "stop",
        title: "枚举值不合法",
        message: "只能从下拉列表选择冻结的 English canonical enum。",
        show: true,
      },
    };
  }
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(3);
  const widths = [22, 62, 27, 11, 11, 27, 26, 27, 33, 19, 29, 48, 22];
  widths.forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, 75, 1).format.columnWidth = width;
  });
  sheet.getRange("A4:A75").format.horizontalAlignment = "center";
  sheet.getRange("D4:E75").format.horizontalAlignment = "center";
  sheet.getRange("M4:M75").format.horizontalAlignment = "center";
  return sheet;
}

function makeEvidenceRows(payload) {
  const rows = [];
  const rowKinds = [];
  const anchors = {};
  rows.push([`Pilot4 ${payload.annotator} Phase2 冻结证据`, "", "", ""]);
  rowKinds.push("title");
  rows.push(["说明", "冻结正文是稳定主要标注载体；官方 URL 仅用于 provenance。正文已完整提取并分块显示。", "", ""]);
  rowKinds.push("note");
  for (const record of payload.rows) {
    anchors[record.blind_review_id] = {};
    for (const evidence of record.evidence_pool) {
      const anchorRow = rows.length + 1;
      anchors[record.blind_review_id][evidence.evidence_id] = anchorRow;
      rows.push([`${record.blind_review_id} / ${evidence.evidence_id}`, "证据块", evidence.official_page_title, "只读"]);
      rowKinds.push("section");
      rows.push([record.blind_review_id, "Candidate", record.candidate_text, "只读"]);
      rowKinds.push("meta");
      rows.push([record.blind_review_id, "Official title", evidence.official_page_title, "只读"]);
      rowKinds.push("meta");
      rows.push([record.blind_review_id, "Official URL", evidence.official_source_url, "provenance"]);
      rowKinds.push("meta");
      rows.push([record.blind_review_id, "Snapshot SHA256", evidence.snapshot_sha256, "只读"]);
      rowKinds.push("meta");
      const textChunks = chunks(evidence.snapshot_text);
      textChunks.forEach((chunk, index) => {
        rows.push([record.blind_review_id, `冻结正文 ${index + 1}/${textChunks.length}`, chunk, "完整分块"]);
        rowKinds.push("text");
      });
      rows.push(["", "", "", ""]);
      rowKinds.push("blank");
    }
  }
  return { rows, rowKinds, anchors };
}

function addEvidenceSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("02_证据");
  sheet.showGridLines = false;
  const { rows, rowKinds, anchors } = makeEvidenceRows(payload);
  sheet.getRangeByIndexes(0, 0, rows.length, 4).values = rows;
  titleStyle(sheet.getRange("A1:D1"));
  bodyStyle(sheet.getRangeByIndexes(1, 0, rows.length - 1, 4), 36);
  rowKinds.forEach((kind, index) => {
    const rowNumber = index + 1;
    if (kind === "section") {
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format = {
        fill: colors.navy,
        font: { name: font, bold: true, color: colors.white, size: 10 },
        wrapText: true,
        verticalAlignment: "center",
      };
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format.rowHeight = 30;
    } else if (kind === "meta") {
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format.fill = colors.gray;
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format.rowHeight = 48;
    } else if (kind === "text") {
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format.fill = colors.paleBlue;
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format.rowHeight = 96;
    } else if (kind === "blank") {
      sheet.getRange(`A${rowNumber}:D${rowNumber}`).format.rowHeight = 10;
    }
  });
  [24, 20, 112, 16].forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, rows.length, 1).format.columnWidth = width;
  });
  sheet.freezePanes.freezeRows(2);
  sheet.freezePanes.freezeColumns(2);
  return { sheet, anchors, rowCount: rows.length };
}

function addManualSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("03_字段说明");
  sheet.showGridLines = false;
  sheet.getRange("A1").values = [[`Pilot4 ${payload.annotator} Phase2 字段说明`]];
  titleStyle(sheet.getRange("A1:H1"));
  sheet.getRange("A2").values = [["固定顺序：读 Candidate → 读 E1/E2 → 证据是否充分 → overall → version → authority → minimum → selection → issue → reason。English canonical values 写入标注表，中文只帮助理解。"]];
  sheet.getRange("A2:H2").format = { fill: colors.green, font: { name: font, bold: true, color: colors.ink, size: 10 }, wrapText: true };
  sheet.getRange("A2:H2").format.rowHeight = 48;
  const headers = ["canonical field", "中文名称", "判断什么", "不判断什么", "canonical value / rule", "什么时候选择", "常见混淆", "教学例"];
  sheet.getRange("A3:H3").values = [headers];
  headerStyle(sheet.getRange("A3:H3"));
  sheet.getRangeByIndexes(3, 0, FIELD_MANUAL_ROWS.length, headers.length).values = FIELD_MANUAL_ROWS;
  bodyStyle(sheet.getRangeByIndexes(3, 0, FIELD_MANUAL_ROWS.length, headers.length), 80);
  sheet.getRangeByIndexes(3, 0, FIELD_MANUAL_ROWS.length, headers.length).format.fill = colors.green;
  [32, 20, 58, 48, 39, 58, 48, 62].forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, FIELD_MANUAL_ROWS.length + 3, 1).format.columnWidth = width;
  });
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(1);
  return sheet;
}

function addExamplesSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("04_填写示例");
  sheet.showGridLines = false;
  sheet.getRange("A1").values = [[`Pilot4 ${payload.annotator} Phase2 完整教学示例（均为虚构，非本项目 Candidate）`]];
  titleStyle(sheet.getRange("A1:K1"));
  const headers = ["场景", "Candidate", "E1/E2 简化证据", "overall_fact_status", "version_claim_status", "authority_claim_status", "minimum_external_evidence_needed", "evidence_selection", "phase2_issue", "phase2_reason", "为什么这么填"];
  sheet.getRange("A3:K3").values = [headers];
  headerStyle(sheet.getRange("A3:K3"));
  sheet.getRangeByIndexes(3, 0, EXAMPLE_ROWS.length, headers.length).values = EXAMPLE_ROWS;
  bodyStyle(sheet.getRangeByIndexes(3, 0, EXAMPLE_ROWS.length, headers.length), 104);
  sheet.getRangeByIndexes(3, 0, EXAMPLE_ROWS.length, headers.length).format.fill = colors.blue;
  [22, 54, 72, 28, 28, 28, 36, 20, 28, 62, 44].forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, EXAMPLE_ROWS.length + 3, 1).format.columnWidth = width;
  });
  sheet.freezePanes.freezeRows(3);
  sheet.freezePanes.freezeColumns(1);
  return sheet;
}

function addChecklistSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("05_提交前检查");
  sheet.showGridLines = false;
  sheet.getRange("A1").values = [[`Pilot4 ${payload.annotator} Phase2 提交前检查`]];
  titleStyle(sheet.getRange("A1:C1"));
  sheet.getRange("A3:C3").values = [["序号", "人工确认", "检查项"]];
  headerStyle(sheet.getRange("A3:C3"));
  const values = CHECKLIST_ROWS.map((item, index) => [index + 1, "□", item]);
  sheet.getRangeByIndexes(3, 0, values.length, 3).values = values;
  bodyStyle(sheet.getRangeByIndexes(3, 0, values.length, 3), 34);
  sheet.getRange("B4:B18").format = { fill: colors.yellow, font: { name: font, bold: true, size: 12 }, horizontalAlignment: "center", verticalAlignment: "center" };
  sheet.getRange("A4:A18").format.horizontalAlignment = "center";
  [10, 16, 86].forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, values.length + 3, 1).format.columnWidth = width;
  });
  return sheet;
}

function addEnumSheet(workbook, payload) {
  const sheet = workbook.worksheets.add("99_内部枚举");
  sheet.showGridLines = false;
  const fields = ["overall_fact_status", "version_claim_status", "authority_claim_status", "minimum_external_evidence_needed", "evidence_selection", "phase2_issue"];
  const maxLength = Math.max(...fields.map((fieldName) => payload.phase2_enums[fieldName].length));
  const values = [fields];
  for (let index = 0; index < maxLength; index += 1) {
    values.push(fields.map((fieldName) => payload.phase2_enums[fieldName][index] ?? ""));
  }
  sheet.getRangeByIndexes(0, 0, values.length, fields.length).values = values;
  headerStyle(sheet.getRangeByIndexes(0, 0, 1, fields.length));
  bodyStyle(sheet.getRangeByIndexes(1, 0, values.length - 1, fields.length), 28);
  sheet.getRangeByIndexes(1, 0, values.length - 1, fields.length).format.fill = colors.gray;
  [34, 38, 38, 42, 24, 42].forEach((width, index) => {
    sheet.getRangeByIndexes(0, index, values.length, 1).format.columnWidth = width;
  });
  return sheet;
}

function excelColumn(index) {
  let value = index + 1;
  let result = "";
  while (value > 0) {
    const remainder = (value - 1) % 26;
    result = String.fromCharCode(65 + remainder) + result;
    value = Math.floor((value - 1) / 26);
  }
  return result;
}

function addValueEntries(entries, sheet, startRow, startColumn, matrix) {
  matrix.forEach((row, rowOffset) => {
    row.forEach((value, columnOffset) => {
      if (value === "" || value === null || value === undefined) return;
      entries.push({
        sheet,
        cell: `${excelColumn(startColumn + columnOffset)}${startRow + rowOffset}`,
        value: String(value),
      });
    });
  });
}

function buildTextContract(payload) {
  const entries = [];
  const canonicalHeaders = [
    "blind_review_id",
    "candidate_text",
    "source_title",
    "view_e1",
    "view_e2",
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
    "filling_check",
  ];
  addValueEntries(entries, "01_标注表", 1, 0, [[`Pilot4 ${payload.annotator} Phase2 人工标注工作簿 V3`]]);
  addValueEntries(entries, "01_标注表", 2, 0, [["只填写带【请填写】/【必须填写】的七列；点击查看E1/E2跳转证据；每行 reason 必填；不要改 ID、Candidate、Evidence、行列或顺序。"]]);
  addValueEntries(entries, "01_标注表", 3, 0, [canonicalHeaders.map((key) => payload.display_headers[key])]);
  const evidenceAnchors = planEvidenceAnchors(payload);
  payload.rows.forEach((row, index) => {
    const excelRow = index + 4;
    addValueEntries(entries, "01_标注表", excelRow, 0, [[row.blind_review_id, row.candidate_text, row.source_title]]);
    const anchors = evidenceAnchors[row.blind_review_id];
    entries.push({ sheet: "01_标注表", cell: `D${excelRow}`, formula: `HYPERLINK("#'02_证据'!A${anchors.E1}","查看E1")`, cachedValue: "查看E1" });
    entries.push({ sheet: "01_标注表", cell: `E${excelRow}`, formula: `HYPERLINK("#'02_证据'!A${anchors.E2}","查看E2")`, cachedValue: "查看E2" });
    entries.push({
      sheet: "01_标注表",
      cell: `M${excelRow}`,
      formula: `IF(OR(COUNTBLANK(F${excelRow}:K${excelRow})>0,L${excelRow}=""),"缺少填写",IF(AND(F${excelRow}<>"FACTUAL_CONFLICT",I${excelRow}<>"NOT_APPLICABLE"),"minimum逻辑不一致",IF(AND(F${excelRow}="FACTUAL_CONFLICT",I${excelRow}="NOT_APPLICABLE"),"minimum逻辑不一致","OK")))`,
      cachedValue: "缺少填写",
    });
  });

  const evidence = makeEvidenceRows(payload);
  addValueEntries(entries, "02_证据", 1, 0, evidence.rows);
  addValueEntries(entries, "03_字段说明", 1, 0, [[`Pilot4 ${payload.annotator} Phase2 字段说明`]]);
  addValueEntries(entries, "03_字段说明", 2, 0, [["固定顺序：读 Candidate → 读 E1/E2 → 证据是否充分 → overall → version → authority → minimum → selection → issue → reason。English canonical values 写入标注表，中文只帮助理解。"]]);
  addValueEntries(entries, "03_字段说明", 3, 0, [["canonical field", "中文名称", "判断什么", "不判断什么", "canonical value / rule", "什么时候选择", "常见混淆", "教学例"]]);
  addValueEntries(entries, "03_字段说明", 4, 0, FIELD_MANUAL_ROWS);
  addValueEntries(entries, "04_填写示例", 1, 0, [[`Pilot4 ${payload.annotator} Phase2 完整教学示例（均为虚构，非本项目 Candidate）`]]);
  addValueEntries(entries, "04_填写示例", 3, 0, [["场景", "Candidate", "E1/E2 简化证据", "overall_fact_status", "version_claim_status", "authority_claim_status", "minimum_external_evidence_needed", "evidence_selection", "phase2_issue", "phase2_reason", "为什么这么填"]]);
  addValueEntries(entries, "04_填写示例", 4, 0, EXAMPLE_ROWS);
  addValueEntries(entries, "05_提交前检查", 1, 0, [[`Pilot4 ${payload.annotator} Phase2 提交前检查`]]);
  addValueEntries(entries, "05_提交前检查", 3, 0, [["序号", "人工确认", "检查项"]]);
  addValueEntries(entries, "05_提交前检查", 4, 0, CHECKLIST_ROWS.map((item, index) => [index + 1, "□", item]));
  return {
    annotator: payload.annotator,
    entries,
    validationMessages: [
      { range: "F4:F75", title: "整体事实状态", prompt: "先判断证据是否充分，再判断冲突，再判断是否必须依赖历史/版本才能成立。" },
      { range: "G4:G75", title: "版本命题", prompt: "只判断 Candidate 自己是否提出版本/时效关系，以及 Evidence 是否支持。" },
      { range: "H4:H75", title: "权威归属", prompt: "区分发布者、制定/通过机关、主管机关、转载主体和网页 host。" },
      { range: "I4:I75", title: "最少证据", prompt: "仅 FACTUAL_CONFLICT 使用；非冲突必须填 NOT_APPLICABLE。" },
      { range: "J4:J75", title: "实际使用证据", prompt: "填写你实际使用的 Evidence，不是理论最少需要几个。" },
      { range: "K4:K75", title: "Phase2 问题", prompt: "事实错误本身不是 issue；冻结正文可读时不能只因 live URL 暂时失败选择 SOURCE_UNREACHABLE。" },
    ],
    validationErrorTitle: "枚举值不合法",
    validationErrorMessage: "只能从下拉列表选择冻结的 English canonical enum。",
  };
}

async function sha256File(filePath) {
  const bytes = await fs.readFile(filePath);
  return crypto.createHash("sha256").update(bytes).digest("hex");
}

function planEvidenceAnchors(payload) {
  const anchors = {};
  let rowCount = 2;
  for (const record of payload.rows) {
    anchors[record.blind_review_id] = {};
    for (const evidence of record.evidence_pool) {
      anchors[record.blind_review_id][evidence.evidence_id] = rowCount + 1;
      rowCount += 5 + chunks(evidence.snapshot_text).length + 1;
    }
  }
  return anchors;
}

function buildWorkbook(payload) {
  if (payload.rows.length !== 72) throw new Error(`ROW_COUNT_BLOCKER:${payload.annotator}`);
  if (new Set(payload.rows.map((row) => row.blind_review_id)).size !== 72) throw new Error(`ID_BLOCKER:${payload.annotator}`);
  if (payload.snapshot_qa.length !== 144) throw new Error(`SNAPSHOT_BLOCKER:${payload.annotator}`);
  const finalBook = Workbook.create();
  addMainSheet(finalBook, payload, planEvidenceAnchors(payload));
  addEvidenceSheet(finalBook, payload);
  addManualSheet(finalBook, payload);
  addExamplesSheet(finalBook, payload);
  addChecklistSheet(finalBook, payload);
  addEnumSheet(finalBook, payload);
  return finalBook;
}

async function inspectAndRender(workbook, annotator, renderRoot, renderEvidenceRange = "A1:D80") {
  workbook.recalculate();
  const inspect = await workbook.inspect({ kind: "workbook,sheet", maxChars: 30000 });
  const formulaErrors = await workbook.inspect({
    kind: "match",
    searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
    options: { useRegex: true, maxResults: 100 },
    summary: "formula error scan",
  });
  if (formulaErrors.ndjson.trim() && !formulaErrors.ndjson.includes("matched 0 entries")) {
    throw new Error(`FORMULA_ERROR_BLOCKER:${annotator}:${formulaErrors.ndjson}`);
  }
  await fs.mkdir(renderRoot, { recursive: true });
  await fs.writeFile(path.join(renderRoot, "workbook_inspect.ndjson"), inspect.ndjson, "utf8");
  await fs.writeFile(path.join(renderRoot, "formula_error_scan.ndjson"), formulaErrors.ndjson, "utf8");
  const renderSpecs = [
    ["01_标注表", "A1:M18"],
    ["02_证据", renderEvidenceRange],
    ["03_字段说明", "A1:H29"],
    ["04_填写示例", "A1:K11"],
    ["05_提交前检查", "A1:C18"],
  ];
  const rendered = [];
  for (const [sheetName, range] of renderSpecs) {
    const image = await workbook.render({ sheetName, range, scale: 0.8, format: "png" });
    const safeName = sheetName.replace(/[^A-Za-z0-9\u4e00-\u9fff_-]/g, "_");
    const filePath = path.join(renderRoot, `${safeName}.png`);
    await fs.writeFile(filePath, new Uint8Array(await image.arrayBuffer()));
    rendered.push({ sheet: sheetName, range, file: filePath });
  }
  return { formulaErrorCount: 0, rendered };
}

async function createAll() {
  const results = [];
  for (const annotator of ["HUMAN-A01", "HUMAN-B01"]) {
    const tag = annotator.replace("HUMAN-", "");
    const payload = JSON.parse(await fs.readFile(path.join(payloadDir, `${annotator}_phase2_v3_payload.json`), "utf8"));
    const contractDir = path.join(qaRoot, "cell_text_contract");
    await fs.mkdir(contractDir, { recursive: true });
    await fs.writeFile(path.join(contractDir, `${annotator}.json`), `${JSON.stringify(buildTextContract(payload), null, 2)}\n`, "utf8");
    const workbook = buildWorkbook(payload);
    const distribution = path.join(outputRoot, annotator, "phase2_v3_distribution");
    await fs.mkdir(distribution, { recursive: true });
    const fileName = `PILOT4_AB_HUMAN_${tag}_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx`;
    const outputPath = path.join(distribution, fileName);
    const beforeQa = await inspectAndRender(workbook, annotator, path.join(qaRoot, "pre_patch", annotator));
    const artifact = await SpreadsheetFile.exportXlsx(workbook);
    await artifact.save(outputPath);
    results.push({ annotator, outputPath, sha256: await sha256File(outputPath), beforeQa });
  }
  await fs.writeFile(path.join(qaRoot, "artifact_tool_create_qa.json"), `${JSON.stringify({ status: "PASS", results }, null, 2)}\n`, "utf8");
  console.log(JSON.stringify({ status: "PASS", mode: "create", results }, null, 2));
}

async function verifyAll() {
  const results = [];
  for (const annotator of ["HUMAN-A01", "HUMAN-B01"]) {
    const tag = annotator.replace("HUMAN-", "");
    const fileName = `PILOT4_AB_HUMAN_${tag}_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx`;
    const outputPath = path.join(outputRoot, annotator, "phase2_v3_distribution", fileName);
    const blob = await FileBlob.load(outputPath);
    const workbook = await SpreadsheetFile.importXlsx(blob);
    const qa = await inspectAndRender(workbook, annotator, path.join(qaRoot, "final_render", annotator));
    results.push({ annotator, outputPath, sha256: await sha256File(outputPath), qa });
  }
  await fs.writeFile(path.join(qaRoot, "artifact_tool_final_render_qa.json"), `${JSON.stringify({ status: "PASS", results }, null, 2)}\n`, "utf8");
  console.log(JSON.stringify({ status: "PASS", mode: "verify", results }, null, 2));
}

if (mode === "create") await createAll();
else if (mode === "verify") await verifyAll();
else throw new Error(`unsupported mode: ${mode}`);
