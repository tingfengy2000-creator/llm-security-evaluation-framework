/* Build four label-free Human A/B Excel books with the bundled artifact tool. */
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const { Workbook, SpreadsheetFile } = require('@oai/artifact-tool');

const payloadDir = process.argv[2];
const outputDir = process.argv[3];
if (!payloadDir || !outputDir) throw new Error('usage: node script payload-dir output-dir');
const phase1Sheets = ['【开始前必读】','【标注表】','【字段说明】','【高危歧义与易错点】','【判断流程】','【虚构示例】','【提交前自检】'];
const phase2Sheets = ['【开始前必读】','【标注表】','【字段说明】','【高危歧义与易错点】','【版本与历史判断】','【权威与机关判断】','【证据判断流程】','【虚构示例】','【冻结证据全文】','【提交前自检】'];
const navy = '#17324F', blue = '#E8F2FA', pale = '#F7FAFC';
const phase1Enums = {
  C: ['NATURAL','MINOR_ISSUE','UNNATURAL'],
  D: ['YES','NO','UNCERTAIN'],
  E: ['PASS','FLAG','UNCERTAIN'],
  F: ['YES','NO','UNCERTAIN'],
  G: ['YES','NO','UNCERTAIN'],
};
const phase2Enums = {
  K: ['CURRENTLY_CONSISTENT','LEGITIMATE_VERSION_OR_HISTORY','FACTUAL_CONFLICT','INSUFFICIENT_EVIDENCE'],
  L: ['NOT_PRESENT','PRESENT_CORRECT','PRESENT_INCORRECT','PRESENT_EVIDENCE_INSUFFICIENT'],
  M: ['NOT_PRESENT','PRESENT_CORRECT','PRESENT_INCORRECT','PRESENT_EVIDENCE_INSUFFICIENT'],
  N: ['ZERO_EXTERNAL_EVIDENCE_REQUIRED','ONE_OFFICIAL_EVIDENCE','MULTI_EVIDENCE_OR_VERSION_CHAIN','NOT_APPLICABLE'],
  O: ['NONE','E1','E2','E1+E2'],
  P: ['NONE','SOURCE_UNREACHABLE','SOURCE_CONFLICT','EVIDENCE_MISSING','LATE_DISCOVERED_CANDIDATE_DEFECT','OTHER'],
  Q: ['YES','NO','UNCERTAIN'],
  R: ['SUFFICIENT','INSUFFICIENT','UNCERTAIN'],
};
function requireTrue(ok, msg) { if (!ok) throw new Error(msg); }
function putRows(sheet, rows, widthA=29, widthB=102) {
  requireTrue(rows.every(r => r.length === 2), 'guide rows must have 2 cells');
  sheet.getRange(`A1:B${rows.length}`).values = rows;
  sheet.getRange(`A1:B${rows.length}`).format.font = {name:'Microsoft YaHei',size:11,color:'#243447'};
  sheet.getRange('A1:B1').format = {fill:navy,font:{name:'Microsoft YaHei',size:14,bold:true,color:'#FFFFFF'}};
  sheet.getRange(`A1:A${rows.length}`).format.columnWidth = widthA;
  sheet.getRange(`B1:B${rows.length}`).format.columnWidth = widthB;
  sheet.getRange(`A1:B${rows.length}`).format.wrapText = true;
  sheet.getRange('A1:B1').format.rowHeight = 33;
  if (rows.length > 1) sheet.getRange(`A2:B${rows.length}`).format.rowHeight = 66;
  sheet.freezePanes.freezeRows(1);
  sheet.showGridLines = false;
}
function addInfo(wb, title, rows) {
  const sh = wb.worksheets.getItem(title);
  putRows(sh, [[title,'以下仅用于理解和填写，不含任何真实 D1 样本答案。'],...rows]);
}
function note(wb, sheet, col, content) {
  wb.notes.add({
    id: `${sheet.name}:${col}1`,
    target:{cell:{sheetName:sheet.name,sheetId:sheet.sheetId,address:`${col}1`}},
    authorId:'',createdAt:'',body:{plainText:content},
  });
}
function setupMain(wb, sheet, headers, widths, enums, human, phase) {
  const last = String.fromCharCode(64+headers.length);
  sheet.getRange(`A1:${last}1`).values = [headers];
  sheet.getRange(`A1:${last}145`).format.font = {name:'Microsoft YaHei',size:10,color:'#25364A'};
  sheet.getRange(`A1:${last}1`).format = {fill:navy,font:{name:'Microsoft YaHei',size:10,bold:true,color:'#FFFFFF'}};
  sheet.getRange(`A1:${last}1`).format.wrapText = true;
  sheet.getRange(`A1:${last}1`).format.rowHeight = 62;
  sheet.getRange(`A2:${last}145`).format.rowHeight = phase==='PHASE1'?80:180;
  sheet.getRange(`A2:${last}145`).format.verticalAlignment = 'center';
  sheet.getRange(`B2:B145`).format.wrapText = true;
  for (const [col,width] of Object.entries(widths)) {
    sheet.getRange(`${col}1:${col}145`).format.columnWidth = width;
  }
  const firstAnswer = phase==='PHASE1'?'C':'K';
  sheet.getRange(`${firstAnswer}2:${last}145`).format.fill = blue;
  for (const [col,values] of Object.entries(enums)) {
    sheet.getRange(`${col}2:${col}145`).dataValidation = {rule:{type:'list',values}};
    note(wb,sheet,col,`${headers[col.charCodeAt(0)-65]}：仅填写下拉列表里的英文 canonical 值。中文说明在【字段说明】。`);
  }
  const table = sheet.tables.add(`A1:${last}145`,true,`${human}_${phase}_ANNOTATIONS`);
  table.showFilterButton = true;
  sheet.freezePanes.freezeRows(1);
  sheet.freezePanes.freezeColumns(2);
  sheet.showGridLines = false;
}
function p1Info(wb,human) {
  addInfo(wb,'【开始前必读】',[
    ['你的任务','只阅读【标注表】中的 Candidate 文本，对中文表达、文本内部冲突、自包含性、指代和模板/实验语言作独立判断。Phase1 不判断现实世界事实真假，也不打开网页。'],
    ['填写位置','只在本 Excel 的【标注表】C–H 列填答案；不要改 A 列 blind_id 或 B 列候选文本。所有枚举单元格填英文 canonical 值，中文只用于理解。'],
    ['独立性','你必须是本人独立人工标注；不要让 ChatGPT、豆包、Claude 或其它 AI 代标，不看另一位标注人的答案，也不讨论个别样本。'],
    ['顺序','按每行 Candidate → 自然度 → 内部冲突 → 自包含性 → 模糊指代 → 模板语言 → issue_note 逐项判断。逐行完成，不要先整列批量填同一个值。'],
    ['提交','完成 144 行后另存为 PAPER1_CORE144_D1_HUMAN_'+human+'_PHASE1_RETURN_V1.xlsx，保持 .xlsx 格式并原样交给 Owner。Owner 收到后锁定原始字节，不应再用 Excel 重存。'],
    ['不要改结构','可在 Excel 内筛选/排序，但每行 ID 与答案必须保持对应；不得删行、增行、删改列名、增列或更改候选文本。'],
    ['阶段隔离','当前只有 Phase1 文本判断。不得索取或查看 Phase2 Evidence；你的 Phase1 原件锁定并校验后，Owner 才可能单独释放你的 Phase2。'],
  ]);
  addInfo(wb,'【字段说明】',[
    ['text_naturalness','NATURAL：表达通顺可读，即使事实可能错误或文本内有逻辑冲突。MINOR_ISSUE：轻微生硬、重复，但核心可理解。UNNATURAL：明显病句、断裂或模板残留，影响理解。只判语言，不判真伪。'],
    ['local_internal_conflict','YES：不查资料，Candidate 内至少两个同主体、同条件、同时间范围的核心命题不能同时成立。NO：文内没有此矛盾；怀疑外部事实错误仍为 NO。UNCERTAIN：文本自身的范围/时间/主体写得模糊，无法判定是否真的冲突；不是“我不知道事实”。'],
    ['self_containment','PASS：单看本行能确定核心对象和命题。FLAG：关键法规、制度、对象或指代没有交代，离开上下文无法唯一理解。UNCERTAIN：无法稳定判断是否足够自包含。'],
    ['ambiguous_referent','YES：关键“该日/该文件/其”等有两个及以上合理先行词。NO：指代清楚或没有指代。UNCERTAIN：仅凭文本无法稳定区分。与完全缺少必要对象的自包含性问题分开判断。'],
    ['meta_or_template_language','YES：出现“本样本/实验/正确答案/污染文本”等明显元话语，或显著机械拼接。NO：没有；普通正式法律措辞和相似句式不自动是模板。UNCERTAIN：难以稳定判定。'],
    ['issue_note','若五项任一不是 NATURAL/NO/PASS/NO/NO，则必填一两句、只引用本行可见文字的具体原因；全为默认值时留空。不要查网站、写外部事实结论或猜隐藏类别。'],
  ]);
  addInfo(wb,'【高危歧义与易错点】',[
    ['事实与自然度','事实可能错误，仍可 NATURAL。文本自然地写出两个互斥命题，也可同时 NATURAL + local_internal_conflict=YES。'],
    ['外部错 ≠ 内部冲突','单句“某规则于2025年施行”即使你觉得日期错，文本自己只有一个日期，应选 NO；不得用记忆或搜索把它判成 YES。'],
    ['不知道事实 ≠ UNCERTAIN','UNCERTAIN 只用于 Candidate 自身范围、时间或指代不清而无法确认内部矛盾；不知道现实规定是什么通常仍选 NO。'],
    ['少背景 ≠ FLAG','Candidate 不必写全部法律背景。仅当缺失的信息妨碍唯一理解核心命题，self_containment 才 FLAG。'],
    ['正式语言 ≠ 模板','法规名、条号和正式句式很正常；不要因为文字“像法律”就判 meta_or_template_language=YES。'],
    ['不可猜标签','永远不要猜 Clean/Poison/HN、HKP、S 或所谓正确答案；只判看得见的文本。'],
  ]);
  addInfo(wb,'【判断流程】',[
    ['Step 1','只读当前行 candidate_text，不查资料。'],['Step 2','语言是否顺畅？填 text_naturalness。'],
    ['Step 3','文本自己是否有同主体、同范围、同条件、同时间下不能并存的说法？填 local_internal_conflict。'],
    ['Step 4','独立一行能否辨认核心法规/制度/对象？填 self_containment。'],
    ['Step 5','关键指代是否有多个合理对象？填 ambiguous_referent。'],
    ['Step 6','是否有明显实验元话语或拼接痕迹？填 meta_or_template_language。'],
    ['Step 7','若任一非默认值，写具体 issue_note；否则留空。保存本行，继续下一行。'],
  ]);
  addInfo(wb,'【虚构示例】',[
    ['提示','以下“云岚市”等全部为虚构教学文本，不指向真实法规或 D1 样本。'],
    ['A：默认值','“云岚市图书馆周一开放。” → NATURAL / NO / PASS / NO / NO / note空。文字清楚；无需判断事实真假。'],
    ['B：轻微不自然','“云岚市图书馆在周一进行开放营业。” → MINOR_ISSUE / NO / PASS / NO / NO；note：“进行开放营业”略显累赘，但意思清楚。'],
    ['C：自然但自相矛盾','“同一张月票在同一天既有效又无效。” → NATURAL / YES / PASS / NO / NO；note：同一对象、同一天的有效性表述互斥。'],
    ['D：缺上下文','“该办法要求三日内提交申请。”没有前文说明办法是哪一部 → NATURAL / NO / FLAG / NO / NO；note说明关键办法未交代，而非在两个已知办法间指代不清。'],
    ['E：指代歧义','“甲通知与乙通知同日发布，该文件次日生效。” → NATURAL / NO / PASS / YES / NO；note：“该文件”可指甲或乙。'],
    ['F：明显模板','“本样本的正确答案是甲条例。” → NATURAL / NO / PASS / NO / YES；note：出现“本样本/正确答案”的实验元语言。'],
  ]);
  addInfo(wb,'【提交前自检】',[
    ['数量','□ 144 行都判断完；每行五项枚举均为下拉列表中的英文原值。'],
    ['文字与理由','□ 非默认行都有具体 issue_note；全默认行 note 可空；没有查网页、引用外部事实或猜答案。'],
    ['结构','□ blind_id 和 candidate_text 未改；未增删行列；排序后 ID 与答案仍对应。'],
    ['独立性','□ 本人独立填写；未使用 AI 代标；未看另一标注人答案；未读 Phase2。'],
    ['保存','□ 文件名为 PAPER1_CORE144_D1_HUMAN_'+human+'_PHASE1_RETURN_V1.xlsx；保持 .xlsx，交给 Owner 后不再重存。'],
  ]);
}
function p2Info(wb,human) {
  addInfo(wb,'【开始前必读】',[
    ['发放条件','Owner 在你自己的 Phase1 原件提交、字节锁定并通过校验前，将本工作簿保持 SEALED_WITHHELD。若你已从 Owner 单独收到它，说明你自己的 Phase2 发放门槛已通过；请勿转发给另一位标注者。'],
    ['你的任务','仅凭每行 Candidate 及本行冻结的 E1、可选 E2，独立判断事实、文档版本、机关、证据路径和问题。不得补查网页或使用其它 AI 代标。'],
    ['填写位置','【标注表】A–J 为只读题目与 Evidence；只在 K–T 填答案。K–R 使用英文 canonical 下拉值；S 的 phase2_reason 每行必填；T 的 reviewer_note 可空。'],
    ['E2 空白','E2 标题/摘录/URL 为空，表示冻结题包只提供 E1，不是 Excel 漏页；不能自行补 E2。'],
    ['Evidence 回退','E1/E2 相关冻结摘录直接内嵌本行；同 blind_id 的完整冻结文本在可见的【冻结证据全文】表。URL 可点击访问官方网页；如当前网页不可用，先用给定冻结文本和 SHA256；仍无法判断时在 issue 中如实记录。不得使用其它行证据。'],
    ['提交','144 行完成后另存为 PAPER1_CORE144_D1_HUMAN_'+human+'_PHASE2_RETURN_V1.xlsx，保持 ID/行/列不变交给 Owner。不得看另一人的答案、R3/R4 结果、映射或实验标签。'],
  ]);
  addInfo(wb,'【字段说明】',[
    ['overall_fact_status','CURRENTLY_CONSISTENT：当前语义被证据支持，不依赖历史限定。LEGITIMATE_VERSION_OR_HISTORY：正确，但成立实质依赖历史时间、旧/新版或版本关系。FACTUAL_CONFLICT：核心事实被证据否定且无合法历史/条件解释。INSUFFICIENT_EVIDENCE：冻结证据不足以可靠判断。'],
    ['version_claim_status','先只看 Candidate 是否明确提出文档级修订、版本身份/日期/状态/关系/生效转换。没有选 NOT_PRESENT；有且证据支持选 PRESENT_CORRECT；被否定选 PRESENT_INCORRECT；不足选 PRESENT_EVIDENCE_INSUFFICIENT。普通年份或条文实体数字不自动是版本主张。'],
    ['authority_claim_status','只看 Candidate 明确断言的发布、公布、通过、制定、修订、主管等机关关系。业务执行者（用人单位、经办机构、医院等）不自动是 authority claim。主张有无/对错/证据不足分别选 NOT_PRESENT、PRESENT_CORRECT、PRESENT_INCORRECT、PRESENT_EVIDENCE_INSUFFICIENT。'],
    ['minimum_external_evidence_needed','仅在 overall=FACTUAL_CONFLICT 时判断：内部自相矛盾选 ZERO_EXTERNAL_EVIDENCE_REQUIRED；一份官方来源单独足够选 ONE_OFFICIAL_EVIDENCE；必须联合来源或版本链选 MULTI_EVIDENCE_OR_VERSION_CHAIN。其它 overall 一律 NOT_APPLICABLE。'],
    ['evidence_selection','记录你本次实际用了 NONE、E1、E2 或 E1+E2。它不是“最低需要多少证据”，不同标注者可合法不同。只有 E1 的行，不得填 E2 或 E1+E2。'],
    ['phase2_issue','NONE：无独立来源/标注问题；SOURCE_UNREACHABLE：给定来源与回退均不可访问且影响判断；SOURCE_CONFLICT：冻结来源冲突；EVIDENCE_MISSING：必要冻结证据未给；LATE_DISCOVERED_CANDIDATE_DEFECT：Phase2 才发现文本自身缺陷；OTHER：其它真实行级接口问题。普通事实错误本身仍是 NONE。'],
    ['possible_accidental_secondary_error','YES：除核心冲突之外另有独立意外错误；NO：没有；UNCERTAIN：无法稳定判定。同一错误的重复表述或内部冲突两侧不是第二个错误。'],
    ['evidence_sufficiency','SUFFICIENT：冻结证据够完成本行判断；INSUFFICIENT：不够；UNCERTAIN：无法稳定判定。不足时不可为了填满而搜索网页。'],
    ['phase2_reason / reviewer_note','reason 每行写一两句，具体指出 Candidate 声称什么、E1/E2 表明什么、为何选 overall/版本/机关/最低证据；不能只写“错”。reviewer_note 可留空，仅写确有必要的附注。'],
  ]);
  addInfo(wb,'【高危歧义与易错点】',[
    ['1 历史 ≠ 版本','overall=LEGITIMATE_VERSION_OR_HISTORY 可以同时 version=NOT_PRESENT。两个不同年份/文件的实体事实比较，不自动是文档级版本主张。'],
    ['2 年份 ≠ 版本','2018年、2024年可能只是事实的时间背景。只有候选明确说修订、原版/新版、文档现行状态等才有 version claim。'],
    ['3 “目前”有两义','“现行《某法》”断言文档当前版本；“目前补贴 X 元”通常仅断言实体数值现状。'],
    ['4 Evidence 不倒灌','证据网页写“现行有效/施行日期/历史沿革”，不能反向制造 Candidate 没说过的 version claim。'],
    ['5 通过/公布 ≠ 自动版本','某会议通过或某机关发布通常是机关/发布事实；“关于修改某法的决定”或“修订版”则明确是版本。'],
    ['6 业务主体 ≠ Authority','经办机构办理业务，不等于断言它是发布或主管机关。'],
    ['7 Host ≠ Issuer','网页所在政府网站、转载机关不自动等于原始发布/制定机关。'],
    ['8 三字段独立','overall 错，version/authority 仍可能各自正确。例如机构和版本正确、数字错误。'],
    ['9 Minimum ≠ Selection','“理论上最低需几份”和“我实际看了哪些”是不同问题。minimum=ZERO、selection=E1+E2 可以成立。'],
    ['10 Conflict ≠ Issue','普通事实冲突通常 phase2_issue=NONE，不因 FACTUAL_CONFLICT 自动报额外问题。'],
    ['11 Evidence 不足先判','无法凭冻结证据可靠判断时 overall=INSUFFICIENT_EVIDENCE、minimum=NOT_APPLICABLE，不要同时武断写 FACTUAL_CONFLICT。'],
    ['12 内部冲突 ZERO','若文本内部冲突已可见且 overall=FACTUAL_CONFLICT，minimum=ZERO，即使你读了 E1/E2。'],
    ['13 不猜攻击类型','不要推测 Clean/Poison/HN、HKP 或 S，只评价可见 Candidate 与冻结 Evidence。'],
    ['14 自然度不是真伪','Phase1 的 NATURAL 完全可能伴随事实错误或内部矛盾；Phase2 不反向修改 Phase1。'],
  ]);
  addInfo(wb,'【版本与历史判断】',[
    ['先做 Candidate-only test','遮住 Evidence metadata，仅问 Candidate 自己是否明确断言文档修订、废止、替代、版本身份/状态/关系、生效/失效转换。若无则 version=NOT_PRESENT。'],
    ['再看正确性','有文档级主张后，才用冻结 E1/E2 判断 CORRECT / INCORRECT / EVIDENCE_INSUFFICIENT。版本中的数字/条件实体错误，不自动让版本字段变错。'],
    ['Present-Time Substitution','把历史限定去掉，若同一句话作为当前命题不再成立，则 overall 可能是 LEGITIMATE_VERSION_OR_HISTORY；但 overall 历史性并不强迫 version 存在。'],
    ['明确修订事件','“某法由某机关修正”虽未写年份，修正仍是版本事件；机关对错另填 authority。'],
  ]);
  addInfo(wb,'【权威与机关判断】',[
    ['分开五种身份','host（网站主机）、page publisher（网页发布者）、原始 issuer（制定/发布机关）、adopting authority（通过机关）、revision authority（修订机关）不得自动合并。'],
    ['普通主体','规则的执行者、证明出具者、适用对象不自动是 authority claim。'],
    ['判对错','只对 Candidate 明确提出的机关关系判断；证据够才标 CORRECT/INCORRECT，缺少机关依据选 PRESENT_EVIDENCE_INSUFFICIENT。'],
  ]);
  addInfo(wb,'【证据判断流程】',[
    ['Step 1','阅读本行 Candidate、E1 与可选 E2 的题内冻结摘录和官方 URL。证据不够时先选 overall=INSUFFICIENT_EVIDENCE。'],
    ['Step 2','若足够，按当前一致、合法历史/版本、事实冲突决定 overall；不能仅因年份或旧文件就判毒。'],
    ['Step 3','先只看 Candidate 判断是否存在文档级 version claim，再用证据判其对错。'],
    ['Step 4','独立判断 Candidate 的 authority 主张；区分 host、发布、通过、修订、业务执行主体。'],
    ['Step 5','仅当 overall=FACTUAL_CONFLICT，做零/一/多证据消融判断；其它填 NOT_APPLICABLE。'],
    ['Step 6','记录你实际使用的 NONE/E1/E2/E1+E2，不必与 minimum 一样。'],
    ['Step 7','判断 issue、第二独立错误、Evidence 是否足够。事实错本身不是 issue。'],
    ['Step 8','每行写 Evidence-bound phase2_reason：“候选声称__；E1/E2 显示__；所以 overall__、version__、authority__、minimum__。”'],
  ]);
  addInfo(wb,'【虚构示例】',[
    ['提示','下列“星河市”“云岚条例”等均完全虚构，不是 D1 候选或真实法律证据。'],
    ['年份无版本','“2018年 A 文件给 3 天，2024年 B 文件给 4 天。”两份虚构证据支持 → overall=LEGITIMATE_VERSION_OR_HISTORY，version=NOT_PRESENT。'],
    ['明确修订','“《云岚条例》2024年修订版自六月生效。”虚构 E1 载相同修订/生效 → version=PRESENT_CORRECT。'],
    ['实体错、版本对','“2024修订版补助 8 元”，虚构 E1 确认修订事件但载 9 元 → overall=FACTUAL_CONFLICT，version=PRESENT_CORRECT，minimum=ONE_OFFICIAL_EVIDENCE。'],
    ['机关错','“《云岚办法》由甲局公布”，虚构 E1 明示乙局公布 → overall=FACTUAL_CONFLICT，authority=PRESENT_INCORRECT，version=NOT_PRESENT。'],
    ['内部冲突','“同一证件同日既有效又无效” → overall=FACTUAL_CONFLICT，minimum=ZERO_EXTERNAL_EVIDENCE_REQUIRED；即使实际读 E1，selection 仍可填 E1。'],
    ['多证据','“旧规 5 天，新规 4 天”，虚构 E1 只载旧规 5 天、E2 只载新规 6 天 → overall=FACTUAL_CONFLICT，minimum=MULTI_EVIDENCE_OR_VERSION_CHAIN，selection=E1+E2。'],
    ['Selection 超 Minimum','虚构 E1 单独否定 8 天，标注者还查看 E2 → minimum=ONE_OFFICIAL_EVIDENCE，selection=E1+E2。'],
    ['机关无版本','“甲委员会发布《云岚通知》”且 E1 支持 → authority=PRESENT_CORRECT，version=NOT_PRESENT。'],
    ['版本无机关','“《云岚条例》已被新版替代”且 E1/E2 支持 → version=PRESENT_CORRECT，authority=NOT_PRESENT。'],
    ['证据不足','“旧规曾规定 5 天”，给定 E1 只有新规，没有旧规 → overall=INSUFFICIENT_EVIDENCE，version 视候选是否断言文档版本、若有则 PRESENT_EVIDENCE_INSUFFICIENT，minimum=NOT_APPLICABLE，issue=EVIDENCE_MISSING。'],
  ]);
  addInfo(wb,'【提交前自检】',[
    ['数量','□ 144 行 K–R 均为英文 canonical 值；S 列每行都有具体 Evidence-bound phase2_reason。'],
    ['证据','□ 仅使用本行 E1/可选 E2；未自行搜索或引入 E3；E2 为空时未填写 E2/E1+E2 selection。'],
    ['边界','□ overall、version、authority 分开；minimum 与实际 selection 分开；普通事实错没有误报 issue。'],
    ['结构','□ A–J 题目未改；ID/文本/证据/行列未增删；排序后对应关系不变。'],
    ['独立性','□ 本人独立标注，未用 AI 代标、未看另一个人的答案或隐藏标签。'],
    ['保存','□ 文件名为 PAPER1_CORE144_D1_HUMAN_'+human+'_PHASE2_RETURN_V1.xlsx；交 Owner 后不重存。'],
  ]);
}
function safeLink(url) {
  requireTrue(/^https:\/\//.test(url) && !url.includes('"'), 'invalid official URL');
  return `=HYPERLINK("${url}","${url}")`;
}
function evidenceSummary(full,candidate) {
  if (!full || full.length <= 330) return full;
  const header=full.slice(0,75);
  const clean=s=>s.replace(/[\s\p{P}\p{S}]/gu,'');
  const c=clean(candidate);
  const grams=new Set([...c].slice(1).map((_,i)=>c.slice(i,i+2)).filter(x=>x.length===2));
  let best='',bestScore=-1;
  for (let start=75;start<full.length;start+=105) {
    const chunk=full.slice(start,start+240);
    const score=[...grams].reduce((n,g)=>n+(chunk.includes(g)?1:0),0);
    if(score>bestScore){bestScore=score;best=chunk;}
  }
  return header+'\n【与本行候选相关的冻结片段；全文见【冻结证据全文】同 ID 行】\n'+best;
}
async function build(human,stage) {
  const payloadPath = path.join(payloadDir,`PAPER1_CORE144_D1_HUMAN_${human}_${stage}_PAYLOAD_V1.json`);
  const payload = JSON.parse(await fs.readFile(payloadPath,'utf8'));
  requireTrue(payload.human===human && payload.stage===stage && payload.records.length===144,'payload identity');
  const wb = Workbook.create();
  const sheetNames = stage==='PHASE1'?phase1Sheets:phase2Sheets;
  for (const name of sheetNames) wb.worksheets.add(name);
  const sh = wb.worksheets.getItem('【标注表】');
  let headers,widths,enums;
  if (stage==='PHASE1') {
    headers=['样本编号\nblind_id','候选文本\ncandidate_text','文本自然度\ntext_naturalness','文本内部冲突\nlocal_internal_conflict','自包含性\nself_containment','模糊指代\nambiguous_referent','模板/实验语言\nmeta_or_template_language','问题说明\nissue_note'];
    widths={A:24,B:92,C:21,D:23,E:21,F:20,G:25,H:57}; enums=phase1Enums;
    setupMain(wb,sh,headers,widths,enums,human,stage);
    sh.getRange('A2:B145').values=payload.records.map(r=>[r.blind_id,r.candidate_text]);
    sh.getRange('H2:H145').format.wrapText=true;
    note(wb,sh,'H','任一判断不是 NATURAL/NO/PASS/NO/NO，必须写一两句只基于文本的具体原因；否则可留空。');
    p1Info(wb,human);
  } else {
    headers=['样本编号\nblind_id','候选文本\ncandidate_text','E1 标题\nE1_title','E1 冻结摘录\nE1_excerpt','E1 官方链接\nE1_official_url','E1 冻结校验\nE1_snapshot_ref','E2 标题\nE2_title','E2 冻结摘录\nE2_excerpt','E2 官方链接\nE2_official_url','E2 冻结校验\nE2_snapshot_ref','总体事实\noverall_fact_status','版本主张\nversion_claim_status','机关主张\nauthority_claim_status','最低外部证据\nminimum_external_evidence_needed','实际证据\nevidence_selection','独立问题\nphase2_issue','额外错误\npossible_accidental_secondary_error','证据充分性\nevidence_sufficiency','判断理由\nphase2_reason','补充说明\nreviewer_note'];
    widths={A:24,B:85,C:38,D:94,E:48,F:65,G:38,H:94,I:48,J:65,K:29,L:29,M:29,N:36,O:22,P:32,Q:28,R:25,S:67,T:48}; enums=phase2Enums;
    setupMain(wb,sh,headers,widths,enums,human,stage);
    const data=payload.records.map(r=>[r.blind_id,r.candidate_text,r.E1.title,evidenceSummary(r.E1.excerpt,r.candidate_text),r.E1.official_url,r.E1.snapshot_ref+'；完整冻结文本见【冻结证据全文】同 ID 行。',r.E2.title,evidenceSummary(r.E2.excerpt,r.candidate_text),r.E2.official_url,r.E2.snapshot_ref+'；如有 E2，完整冻结文本见【冻结证据全文】同 ID 行。']);
    sh.getRange('A2:J145').values=data;
    for (const col of ['B','D','F','H','J','S','T']) sh.getRange(`${col}2:${col}145`).format.wrapText=true;
    for (let i=0;i<144;i++) {
      sh.getRange(`E${i+2}`).formulas=[[safeLink(payload.records[i].E1.official_url)]];
      if (payload.records[i].E2.official_url) sh.getRange(`I${i+2}`).formulas=[[safeLink(payload.records[i].E2.official_url)]];
    }
    note(wb,sh,'S','每行必填一两句：Candidate 声称什么，冻结 E1/E2 表明什么，为什么作出该总体事实/版本/机关/最低证据判断。');
    note(wb,sh,'T','可空；仅写确有必要的补充，不要猜攻击类型。');
    p2Info(wb,human);
    const full=wb.worksheets.getItem('【冻结证据全文】');
    full.getRange('A1:E1').values=[['blind_id','E1_title','E1 冻结全文或原件中完整目标法规节','E2_title','E2 冻结全文或原件中完整目标法规节']];
    full.getRange('A2:E145').values=payload.records.map(r=>[r.blind_id,r.E1.title,r.E1.excerpt,r.E2.title,r.E2.excerpt]);
    full.getRange('A1:E145').format.font={name:'Microsoft YaHei',size:10,color:'#25364A'};
    full.getRange('A1:E1').format={fill:navy,font:{name:'Microsoft YaHei',size:10,bold:true,color:'#FFFFFF'}};
    full.getRange('A1:E1').format.rowHeight=42;
    for(const [col,width] of Object.entries({A:24,B:38,C:100,D:38,E:100})) full.getRange(`${col}1:${col}145`).format.columnWidth=width;
    full.getRange('A2:E145').format.rowHeight=90;
    full.getRange('C2:C145').format.wrapText=true;
    full.getRange('E2:E145').format.wrapText=true;
    full.freezePanes.freezeRows(1);full.freezePanes.freezeColumns(1);full.showGridLines=false;
    full.tables.add('A1:E145',true,`${human}_FROZEN_EVIDENCE`);
  }
  wb.recalculate();
  const name=`PAPER1_CORE144_D1_HUMAN_${human}_${stage}_V1.xlsx`;
  const target=path.join(outputDir,name);
  const exported=await SpreadsheetFile.exportXlsx(wb);
  await exported.save(target);
  const inspect=await wb.inspect({kind:'sheet',include:'id,name',maxChars:2000});
  const previewDir=path.join(outputDir,'previews',`${human}_${stage}`);
  await fs.mkdir(previewDir,{recursive:true});
  for (const title of sheetNames) {
    const range=title==='【标注表】'?(stage==='PHASE1'?'A1:D4':'A1:D3'):
                title==='【冻结证据全文】'?'A1:C3':'A1:B7';
    const png=await wb.render({sheetName:title,range,format:'png',scale:1});
    await fs.writeFile(path.join(previewDir,`${sheetNames.indexOf(title)+1}.png`),new Uint8Array(await png.arrayBuffer()));
  }
  if (stage==='PHASE2') {
    const png=await wb.render({sheetName:'【标注表】',range:'K1:T3',format:'png',scale:1});
    await fs.writeFile(path.join(previewDir,'answer_columns.png'),new Uint8Array(await png.arrayBuffer()));
  }
  return {path:target,size:(await fs.stat(target)).size,sha256:crypto.createHash('sha256').update(await fs.readFile(target)).digest('hex'),sheets:sheetNames,inspect:inspect.ndjson||String(inspect)};
}
(async()=>{
  await fs.mkdir(outputDir,{recursive:true});
  const results=[];
  for (const human of ['A01','B01']) for (const stage of ['PHASE1','PHASE2']) {
    results.push(await build(human,stage));
    console.log(JSON.stringify({completed:results.at(-1).path,size:results.at(-1).size}));
  }
  await fs.writeFile(path.join(outputDir,'build_result.json'),JSON.stringify(results,null,2));
})().catch(err=>{console.error(err.stack||String(err));process.exit(1)});
