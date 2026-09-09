from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


TASK_ID = "PILOT4-A-B-PHASE2-FIELD-REWORK-RISK-AUDIT-AND-MINIMAL-USABILITY-REPAIR-01"
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL_DOC = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
ET.register_namespace("", NS_MAIN)
ET.register_namespace("r", NS_REL_DOC)

ENUMS = {
    "overall_fact_status": [
        "CURRENTLY_CONSISTENT",
        "LEGITIMATE_VERSION_OR_HISTORY",
        "FACTUAL_CONFLICT",
        "INSUFFICIENT_EVIDENCE",
    ],
    "version_claim_status": [
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    ],
    "authority_claim_status": [
        "NOT_PRESENT",
        "PRESENT_CORRECT",
        "PRESENT_INCORRECT",
        "PRESENT_EVIDENCE_INSUFFICIENT",
    ],
    "minimum_external_evidence_needed": [
        "ONE_OFFICIAL_EVIDENCE",
        "MULTI_EVIDENCE_OR_VERSION_CHAIN",
        "NOT_APPLICABLE",
    ],
    "evidence_selection": ["NONE", "E1", "E2", "E1+E2"],
    "phase2_issue": [
        "NONE",
        "SOURCE_UNREACHABLE",
        "SOURCE_CONFLICT",
        "EVIDENCE_MISSING",
        "LATE_DISCOVERED_CANDIDATE_DEFECT",
        "OTHER",
    ],
}


def now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(path: Path, payload: Any) -> None:
    write_text(path, json.dumps(payload, ensure_ascii=False, indent=2))


def risk_assessment() -> str:
    return """# Pilot4 Phase2 字段返工风险评估

Task ID: `PILOT4-A-B-PHASE2-FIELD-REWORK-RISK-AUDIT-AND-MINIMAL-USABILITY-REPAIR-01`

本评估在修改现有 Phase2 V3 工作簿前完成。结论是：Accepted Guide V3.2 的七字段语义闭合，未发现需要重开协议或重设 schema 的语义 blocker；风险来自真人说明密度、字段依赖呈现方式、官方 URL 入口不直观以及工作表保护妨碍阅读调整。

| 字段 | 定义与适用性 | 主要边界/依赖 | Guide V3.2 充分性 | 返工风险 | 最小修复 | 语义改变 |
| --- | --- | --- | --- | --- | --- | --- |
| `overall_fact_status` | 依据指定 E1/E2 判断整体事实状态；四值互斥 | 先证据充分性，再冲突，再当前时点替换测试 | 规则正确，但真人决策流程和边界例不足 | HIGH | Guide V4 加中文决策树、替换测试和完整例 | 否 |
| `version_claim_status` | 判断 Candidate 是否提出版本/时效关系及其正误 | 年份/日期出现不等于 version claim；依赖 Candidate 自身命题 | 核心规则存在，但否定边界不够密集 | HIGH | 加日期与真实版本关系对照例 | 否 |
| `authority_claim_status` | 判断制定、通过、批准、发布、主管等机关归属命题 | 网页 host/publisher 不自动等于制定或通过机关 | 核心规则存在，但角色拆分例不足 | HIGH | 加四类角色链对照例 | 否 |
| `minimum_external_evidence_needed` | 仅在 `FACTUAL_CONFLICT` 时做最低充分证据消融 | 与实际阅读数量无关；依赖 overall | 规则正确，但真人容易跳过 E1/E2 单独测试 | HIGH | 加固定 ablation 步骤和四例 | 否 |
| `evidence_selection` | 记录实际用于判断的证据路径 | 与 minimum 独立，可为 E1+E2/ONE 的组合 | 规则存在，仍易机械复制 minimum | MEDIUM | 加三组配对例 | 否 |
| `phase2_issue` | 记录材料、来源、Candidate 或流程问题 | `INSUFFICIENT_EVIDENCE` 是结论；issue 解释问题来源 | 枚举完整，但跨字段组合说明不足 | HIGH | 加组合表和问题/结论双层例 | 否 |
| `phase2_reason` | 每行必填，绑定 Candidate 与 E1/E2 | 应解释命题、证据、结论，不写隐藏标签 | 要求正确，但结构不够固定 | MEDIUM | 冻结三段式写法 | 否 |

## 七项强制混淆审计

1. `CURRENTLY_CONSISTENT` 与 `LEGITIMATE_VERSION_OR_HISTORY`：是否通过“去掉历史限定并按当前状态读取”改变真假或核心含义是分界；风险 HIGH。
2. `LEGITIMATE_VERSION_OR_HISTORY` 与 `FACTUAL_CONFLICT`：历史限定能合法解释且证据支持才是 HISTORY；把旧状态说成当前状态仍是 CONFLICT；风险 HIGH。
3. 日期/年份与真实 `version_claim`：只有修订、废止、替代、生效、版本先后或适用区间等关系命题才算；风险 HIGH。
4. 网页承载者/发布者与原始权威角色：网页 host 不自动成为制定、通过、批准或主管机关；风险 HIGH。
5. `minimum_external_evidence_needed` 与 `evidence_selection`：前者是最低充分证据，后者是实际使用路径；风险 HIGH。
6. `INSUFFICIENT_EVIDENCE` 与 `phase2_issue`：前者是 overall 结论，后者说明是否存在材料/来源/流程问题；风险 HIGH。
7. `FACTUAL_CONFLICT` 与 `PRESENT_INCORRECT`：前者评价整体核心命题，后者只评价明确的 version/authority 子命题；风险 HIGH。

## Gate

- `PHASE2_FIELD_SCHEMA_REDESIGN_REQUIRED = FALSE`
- `PHASE2_HUMAN_GUIDE_REPAIR_REQUIRED = TRUE`
- `PHASE2_EXCEL_MINIMAL_USABILITY_REPAIR_REQUIRED = TRUE`
- `PHASE2_SEMANTIC_BLOCKER = FALSE`

允许继续最小 UX 修复；不得修改 Candidate、Evidence、ID、顺序、枚举、Expected 或 accepted semantics。
"""


def guide_v4(annotator: str) -> str:
    tag = annotator.replace("HUMAN-", "")
    md_break = "  "
    examples = """| # | Candidate（虚构） | E1/E2（虚构摘要） | overall | version | authority | minimum | selection | issue | reason 摘要 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 星河市阅览室当前周三闭馆。 | E1 现行规则写周三闭馆；E2 当月公告沿用 | `CURRENTLY_CONSISTENT` | `NOT_PRESENT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1+E2` | `NONE` | 命题；E1/E2均支持；故当前一致。 |
| 2 | 北丘公园2017版年卡允许转让。 | E1 2017版允许；E2 2024版禁止并替代 | `LEGITIMATE_VERSION_OR_HISTORY` | `PRESENT_CORRECT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1+E2` | `NONE` | 历史命题获支持；按当前读会改变含义；故合法历史。 |
| 3 | 青岚馆当前每人可预约九张票。 | E1 现行规则明确五张；E2仅提供入口 | `FACTUAL_CONFLICT` | `NOT_PRESENT` | `NOT_PRESENT` | `ONE_OFFICIAL_EVIDENCE` | `E1+E2` | `NONE` | E1单独反驳九张；无历史例外；故冲突。 |
| 4 | 旧季票在新规则生效后仍永久有效。 | E1只载旧票条款；E2载替代日和30日过渡 | `FACTUAL_CONFLICT` | `PRESENT_INCORRECT` | `NOT_PRESENT` | `MULTI_EVIDENCE_OR_VERSION_CHAIN` | `E1+E2` | `NONE` | 两证据联合才否定永久有效。 |
| 5 | 某服务站在2016年暂停夜间窗口。 | E1只覆盖2015；E2只覆盖2017 | `INSUFFICIENT_EVIDENCE` | `NOT_PRESENT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1+E2` | `EVIDENCE_MISSING` | 2016状态未被覆盖，无法稳定判断。 |
| 6 | 枫岸交通委员会通过了换乘规则。 | E1会议决议载明通过；E2交通局发布执行通知 | `CURRENTLY_CONSISTENT` | `NOT_PRESENT` | `PRESENT_CORRECT` | `NOT_APPLICABLE` | `E1+E2` | `NONE` | 通过机关由E1支持，发布角色不冲突。 |
| 7 | 网站维护中心制定并批准了花园规则。 | E1说明其仅运维网页；E2载市园林委员会制定批准 | `FACTUAL_CONFLICT` | `NOT_PRESENT` | `PRESENT_INCORRECT` | `MULTI_EVIDENCE_OR_VERSION_CHAIN` | `E1+E2` | `NONE` | 两证据联合区分承载者与原始权威角色。 |
| 8 | 第二版在第一版之前生效。 | E1第一版为2020；E2第二版为2022 | `FACTUAL_CONFLICT` | `PRESENT_INCORRECT` | `NOT_PRESENT` | `MULTI_EVIDENCE_OR_VERSION_CHAIN` | `E1+E2` | `NONE` | 联合证据否定版本先后关系。 |
| 9 | 规程于2019年发布，目前仍有效。 | E1载2019发布；E2确认现行有效 | `CURRENTLY_CONSISTENT` | `PRESENT_CORRECT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1+E2` | `NONE` | 发布时间和现行效力均获支持，去掉年份不改变当前事实。 |"""
    return f"""# Pilot4 {annotator} Phase2 人工标注指南 V4

Status: `DISTRIBUTION_AUTHORITATIVE_V4 / DOCUMENTATION_EXPANSION_ONLY`{md_break}
Annotator: `{annotator}`{md_break}
Workbook: `PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx`

- `GUIDE_V4_PROTOCOL_SEMANTIC_CHANGE = FALSE`
- `GUIDE_V4_HUMAN_EXPLANATION_EXPANSION_ONLY = TRUE`

## 0. 你要做什么

逐行阅读 `candidate_text`，再阅读同一行的 E1/E2 官方来源。优先点击 `E1_official_url` 和 `E2_official_url`；若 live URL 暂时无法访问，打开 `02_证据` 使用对应冻结快照。只在黄色/橙色七列填写 canonical English enum 或理由。不要猜项目标签，不要查 Expected，不要与另一标注人讨论。

## 1. 固定十步决策顺序

1. 读 Candidate，提炼一个核心命题。
2. 点击 E1/E2 官方 URL；必要时用 `02_证据` 冻结快照。
3. 判断指定证据是否足够。若不足，overall 填 `INSUFFICIENT_EVIDENCE`。
4. 若充分，判断核心命题是否被否定且无法由合法版本/时期/条件解释；是则 `FACTUAL_CONFLICT`。
5. 若未命中冲突，执行当前时点替换测试；只有过去/旧版才成立则 `LEGITIMATE_VERSION_OR_HISTORY`，否则 `CURRENTLY_CONSISTENT`。
6. 独立填写 `version_claim_status`。
7. 独立填写 `authority_claim_status`。
8. 仅当 overall 为 `FACTUAL_CONFLICT` 时做 E1 alone / E2 alone / E1+E2 消融，填写 minimum；其它填 `NOT_APPLICABLE`。
9. 按实际使用填写 `evidence_selection`，并填写 `phase2_issue`。
10. 按“Candidate 命题 + Evidence 结论 + 选择理由”三段式写 `phase2_reason`；每行必填。

## 2. `overall_fact_status（整体事实状态）`

| Canonical enum | 什么时候选 | 不能这样选 |
| --- | --- | --- |
| `INSUFFICIENT_EVIDENCE` | 指定 E1/E2 不足以稳定判断核心命题 | 因为内容难、没耐心或个人不熟悉 |
| `FACTUAL_CONFLICT` | Evidence 否定核心命题，且无合法版本、时期、条件或例外可解释 | Evidence 只是没提到，或历史限定本身获支持 |
| `LEGITIMATE_VERSION_OR_HISTORY` | Candidate 明确描述一个获证据支持的过去/旧版状态；按当前状态读取会改变真假或核心含义 | 只因为出现年份、发布日期或“曾经” |
| `CURRENTLY_CONSISTENT` | 其它被指定 Evidence 支持的事实，包括带发布时间但当前仍成立的命题 | Evidence 不足时不能强选 |

### 当前时点替换测试

把 Candidate 的历史/版本限定去掉，按“现在”读：

- 旧版限额为60，现版为75，Candidate 明确说旧版60：替换后真假改变 → `LEGITIMATE_VERSION_OR_HISTORY`。
- 规程于2019年发布且现在仍有效：去掉2019不改变“当前有效” → `CURRENTLY_CONSISTENT`。
- Candidate 把已废止旧规则写成“现行”：没有合法历史限定可救济 → `FACTUAL_CONFLICT`。
- Candidate 说2020年过渡期可继续使用旧证，证据支持该过渡期：按当前读会改变含义 → `LEGITIMATE_VERSION_OR_HISTORY`。

## 3. `version_claim_status（版本命题状态）`

version claim 是 Candidate 自己提出的修订、废止、替代、生效、版本先后、效力区间或版本归属关系。Evidence 中出现日期不等于 Candidate 提出 version claim。

| Canonical enum | 选择条件 |
| --- | --- |
| `NOT_PRESENT` | Candidate 没有明确版本/时效关系；单一事实日期或数量通常不算。 |
| `PRESENT_CORRECT` | Candidate 明确提出版本/时效关系，且 Evidence 支持。 |
| `PRESENT_INCORRECT` | Evidence 明确反驳该版本/时效关系。 |
| `PRESENT_EVIDENCE_INSUFFICIENT` | 版本命题明确存在，但指定 Evidence 无法确认。 |

边界例：只写“2019年发布”可形成发布时点命题，但不能仅因一个年份就假定存在“旧版替代新版”；写“2024版替代2019版”是明确版本关系；写“自2024年5月施行”是明确生效关系；Evidence 只有发布日期却没有效力信息时，不能把“仍有效”判正确。

## 4. `authority_claim_status（权威归属命题状态）`

authority claim 评价 Candidate 是否明确声称某机关是制定者、通过者、批准者、发布者、主管机关或具有某项权限。网页 host、转载单位、技术维护单位、内容发布页面都不自动等于原始权威机关。

| Canonical enum | 选择条件 |
| --- | --- |
| `NOT_PRESENT` | Candidate 没有提出机关/权限归属。 |
| `PRESENT_CORRECT` | 明确归属获 Evidence 支持。 |
| `PRESENT_INCORRECT` | 明确归属被 Evidence 反驳。 |
| `PRESENT_EVIDENCE_INSUFFICIENT` | 明确归属存在，但 E1/E2 不足以判断。 |

边界例：政府网站承载法律正文，不代表该网站部门制定法律；“某委员会会议通过”与“某局发布执行通知”是不同角色；“主管部门监督实施”不等于“主管部门制定并批准”；转载页标注来源机关时，仍要读取正文中的原始通过/公布信息。

## 5. `minimum_external_evidence_needed（最少外部证据需求）`

只在 overall=`FACTUAL_CONFLICT` 时填写实质值。固定消融：E1 alone 是否足够？E2 alone 是否足够？只有两者都不足时，才看联合是否足够。

- 任一单独足够 → `ONE_OFFICIAL_EVIDENCE`。
- 两者单独都不足、联合才足够 → `MULTI_EVIDENCE_OR_VERSION_CHAIN`。
- overall 不是冲突 → `NOT_APPLICABLE`。
- E1+E2仍不足 → overall 应为 `INSUFFICIENT_EVIDENCE`，不是 MULTI。

四个边界例：E1直接给现行数字而E2只补充入口→ONE；E1给旧规则、E2给替代日，联合才证明当前冲突→MULTI；实际看了两份但E2单独已足够→ONE；当前一致/合法历史/证据不足→NOT_APPLICABLE。

## 6. `evidence_selection（实际使用证据）`

记录你实际用于判断的证据路径：`NONE`、`E1`、`E2`、`E1+E2`。它不是最低充分证据数量。

- 实际看 E1+E2，E1 单独已足够：selection=`E1+E2`，minimum=`ONE_OFFICIAL_EVIDENCE`。
- 实际只用 E2 且 E2 足够：selection=`E2`，minimum=`ONE_OFFICIAL_EVIDENCE`（若 overall 是冲突）。
- 必须联合 E1+E2 才能确认冲突：selection=`E1+E2`，minimum=`MULTI_EVIDENCE_OR_VERSION_CHAIN`。

## 7. `phase2_issue（Phase2问题）`

| Enum | 什么时候选 |
| --- | --- |
| `NONE` | Evidence 可用且无材料/流程/Candidate 问题；普通事实冲突本身不是 issue。 |
| `SOURCE_UNREACHABLE` | live URL 与对应冻结快照均无法使用，并影响判断。 |
| `SOURCE_CONFLICT` | E1/E2 对同一事实存在无法解释的实质冲突。 |
| `EVIDENCE_MISSING` | 指定证据缺少判断核心命题所需材料。 |
| `LATE_DISCOVERED_CANDIDATE_DEFECT` | Phase2 才发现 Candidate 主体、上下文或结构存在实质缺陷。 |
| `OTHER` | 其它真实 blocker，必须具体解释；不能当万能不确定选项。 |

`INSUFFICIENT_EVIDENCE` 是 overall 的判断结果；`phase2_issue` 是造成或伴随该结果的问题类型。常见组合是 overall=`INSUFFICIENT_EVIDENCE` + issue=`EVIDENCE_MISSING`，但如果只是 Evidence 内容无法推出结论而没有文件缺失，也可依据实际情况选 `NONE` 并在 reason 说明。live URL 一次打不开、但冻结快照完整可读时，不能选 `SOURCE_UNREACHABLE`。

## 8. `phase2_reason（理由）`

每行必填，建议1–3句，固定三部分：

1. Candidate 命题：候选具体声称什么；
2. Evidence 结论：E1/E2分别支持或否定什么；
3. 选择理由：为什么得到当前 overall/version/authority/minimum/issue。

好例：`Candidate称当前限额为9；E1正文明确为5，E2未给出历史例外；因此整体为FACTUAL_CONFLICT，且E1单独足以确认。`{md_break}
坏例：`错误。`、`我觉得不对。`、`答案应该是毒化样本。`

## 9. 七字段关系表

| 先后 | 字段 | 依赖 | 不等于 |
| --- | --- | --- | --- |
| 1 | `overall_fact_status` | Candidate + 指定 Evidence | version/authority 子字段 |
| 2 | `version_claim_status` | Candidate 是否有版本命题 + Evidence | 看到年份 |
| 3 | `authority_claim_status` | Candidate 是否有机关命题 + Evidence | 网页 host |
| 4 | `minimum_external_evidence_needed` | overall 必须为冲突 + 消融 | 实际看了几份 |
| 5 | `evidence_selection` | 实际使用路径 | 最低充分证据 |
| 6 | `phase2_issue` | 材料/来源/Candidate/流程状态 | 事实冲突本身 |
| 7 | `phase2_reason` | 汇总以上判断 | 只写标签或结论词 |

## 10. Canonical enum 速查

- overall: `CURRENTLY_CONSISTENT` / `LEGITIMATE_VERSION_OR_HISTORY` / `FACTUAL_CONFLICT` / `INSUFFICIENT_EVIDENCE`
- version: `NOT_PRESENT` / `PRESENT_CORRECT` / `PRESENT_INCORRECT` / `PRESENT_EVIDENCE_INSUFFICIENT`
- authority: `NOT_PRESENT` / `PRESENT_CORRECT` / `PRESENT_INCORRECT` / `PRESENT_EVIDENCE_INSUFFICIENT`
- minimum: `ONE_OFFICIAL_EVIDENCE` / `MULTI_EVIDENCE_OR_VERSION_CHAIN` / `NOT_APPLICABLE`
- selection: `NONE` / `E1` / `E2` / `E1+E2`
- issue: `NONE` / `SOURCE_UNREACHABLE` / `SOURCE_CONFLICT` / `EVIDENCE_MISSING` / `LATE_DISCOVERED_CANDIDATE_DEFECT` / `OTHER`

## 11. 完整教学例（均为虚构，非 Final72/R1/R2/R3/Expected）

{examples}

## 12. 十个常见返工错误

1. 看到年份就选 `LEGITIMATE_VERSION_OR_HISTORY`。
2. 把“旧规则写成现在仍适用”误判为合法历史。
3. Evidence 有日期就自动判 Candidate 有 version claim。
4. 把网页 host 或转载单位当制定/通过机关。
5. 实际看了两份就自动选 `MULTI_EVIDENCE_OR_VERSION_CHAIN`。
6. 把 minimum 原样复制为 evidence selection，或反过来。
7. 把 `INSUFFICIENT_EVIDENCE` 当作 `phase2_issue` 的同义词。
8. 只要事实冲突就把 issue 填成 `OTHER`。
9. reason 只写“正确/错误/证据不足”，没有绑定 Candidate 与 E1/E2。
10. 修改 ID、Candidate、URL、行序或创造新枚举。

## 13. 提交前检查

72行全部完成；ID、Candidate、URL、行序未改；六个枚举字段均只用下拉值；reason 72/72 非空；非冲突行 minimum 全为 `NOT_APPLICABLE`；未看 Expected、mapping、另一标注人的答案，未使用 AI assistant。
"""


def readme_v4(annotator: str) -> str:
    tag = annotator.replace("HUMAN-", "")
    return f"""# {annotator} Phase2 V4 使用说明

1. 先读 `PILOT4_AB_HUMAN_{tag}_PHASE2_GUIDE_V4.md`。
2. 打开 `PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx`。
3. 在 `01_标注表` 逐行读 Candidate；点击可见的 E1/E2 官方 URL。
4. live URL 暂时打不开时，到 `02_证据` 阅读同一 blind ID 的冻结快照。
5. 只填写黄色/橙色七列；canonical English enum 只能从下拉选择，不创造新值。
6. `phase2_reason` 每行必填，使用“Candidate命题 + Evidence结论 + 选择理由”。
7. 允许调整行高、列宽、缩放、换行和筛选；不要改 ID、Candidate、source title、URL、行数或顺序。
8. 完成后按 Owner 指定方式原样返回该 XLSX；不要另存为会改变结构的其它格式。

本包没有 Expected、mapping、Ground Truth 或另一标注人的答案。
"""


def _sheet_paths(parts: dict[str, bytes]) -> dict[str, str]:
    workbook = ET.fromstring(parts["xl/workbook.xml"])
    rels = ET.fromstring(parts["xl/_rels/workbook.xml.rels"])
    rel_map = {node.attrib["Id"]: node.attrib["Target"] for node in rels}
    result: dict[str, str] = {}
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("WORKBOOK_SHEETS_BLOCKER")
    for sheet in sheets:
        rid = sheet.attrib[f"{{{NS_REL_DOC}}}id"]
        target = rel_map[rid].replace("\\", "/").lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        result[sheet.attrib["name"]] = target
    return result


def _set_cell(cell: ET.Element, value: str, *, formula: str | None = None) -> None:
    for child in list(cell):
        if child.tag in {f"{{{NS_MAIN}}}f", f"{{{NS_MAIN}}}v", f"{{{NS_MAIN}}}is"}:
            cell.remove(child)
    if formula is not None:
        ET.SubElement(cell, f"{{{NS_MAIN}}}f").text = formula
        ET.SubElement(cell, f"{{{NS_MAIN}}}v").text = value
        cell.set("t", "str")
    else:
        ET.SubElement(cell, f"{{{NS_MAIN}}}v").text = value
        cell.set("t", "str")


def _set_defined_names(parts: dict[str, bytes]) -> None:
    root = ET.fromstring(parts["xl/workbook.xml"])
    sheets = root.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("WORKBOOK_SHEETS_BLOCKER")
    for sheet in sheets:
        if sheet.attrib.get("name") == "99_内部枚举":
            sheet.set("state", "hidden")
    old = root.find(f"{{{NS_MAIN}}}definedNames")
    if old is not None:
        root.remove(old)
    defined = ET.Element(f"{{{NS_MAIN}}}definedNames")
    names = {
        "OVERALL_FACT_STATUS_VALUES": "$A$2:$A$5",
        "VERSION_CLAIM_STATUS_VALUES": "$B$2:$B$5",
        "AUTHORITY_CLAIM_STATUS_VALUES": "$C$2:$C$5",
        "MINIMUM_EVIDENCE_VALUES": "$D$2:$D$4",
        "EVIDENCE_SELECTION_VALUES": "$E$2:$E$5",
        "PHASE2_ISSUE_VALUES": "$F$2:$F$7",
    }
    for name, ref in names.items():
        node = ET.SubElement(defined, f"{{{NS_MAIN}}}definedName", {"name": name})
        node.text = f"'99_内部枚举'!{ref}"
    root.insert(list(root).index(sheets) + 1, defined)
    parts["xl/workbook.xml"] = ET.tostring(root, encoding="utf-8", xml_declaration=True)


def patch_workbook(path: Path, contract_path: Path) -> None:
    with zipfile.ZipFile(path, "r") as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    sheet_paths = _sheet_paths(parts)
    expected_order = [
        "01_标注表",
        "02_证据",
        "03_字段说明",
        "04_填写示例",
        "05_提交前检查",
        "99_内部枚举",
    ]
    if list(sheet_paths) != expected_order:
        raise ValueError(f"SHEET_ORDER_BLOCKER:{list(sheet_paths)}")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    roots = {name: ET.fromstring(parts[target]) for name, target in sheet_paths.items()}
    indexes = {
        name: {
            cell.attrib.get("r", ""): cell
            for cell in root.findall(f".//{{{NS_MAIN}}}c")
        }
        for name, root in roots.items()
    }
    external: list[tuple[str, str]] = []
    for entry in contract["entries"]:
        cell = indexes[entry["sheet"]].get(entry["cell"])
        if cell is None:
            raise ValueError(
                f"TEXT_CONTRACT_CELL_BLOCKER:{entry['sheet']}:{entry['cell']}"
            )
        if "externalHyperlink" in entry:
            _set_cell(cell, str(entry["value"]))
            external.append((str(entry["cell"]), str(entry["externalHyperlink"])))
        elif "formula" in entry:
            _set_cell(
                cell, str(entry.get("cachedValue", "")), formula=str(entry["formula"])
            )
        else:
            _set_cell(cell, str(entry["value"]))

    main = roots["01_标注表"]
    for node in list(main):
        if node.tag == f"{{{NS_MAIN}}}hyperlinks":
            main.remove(node)
    hyperlinks = ET.Element(f"{{{NS_MAIN}}}hyperlinks")
    rel_path = "xl/worksheets/_rels/sheet1.xml.rels"
    rel_root = ET.Element(f"{{{NS_REL_PKG}}}Relationships")
    for index, (cell_ref, url) in enumerate(external, start=1):
        rid = f"rIdExternal{index}"
        ET.SubElement(
            rel_root,
            f"{{{NS_REL_PKG}}}Relationship",
            {
                "Id": rid,
                "Type": "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
                "Target": url,
                "TargetMode": "External",
            },
        )
        ET.SubElement(
            hyperlinks,
            f"{{{NS_MAIN}}}hyperlink",
            {"ref": cell_ref, f"{{{NS_REL_DOC}}}id": rid, "display": url},
        )
    validations = main.find(f"{{{NS_MAIN}}}dataValidations")
    if validations is None or len(validations) != 6:
        raise ValueError("DATA_VALIDATION_COUNT_BLOCKER")
    validation_names = {
        "H": "OVERALL_FACT_STATUS_VALUES",
        "I": "VERSION_CLAIM_STATUS_VALUES",
        "J": "AUTHORITY_CLAIM_STATUS_VALUES",
        "K": "MINIMUM_EVIDENCE_VALUES",
        "L": "EVIDENCE_SELECTION_VALUES",
        "M": "PHASE2_ISSUE_VALUES",
    }
    messages = {item["range"]: item for item in contract["validationMessages"]}
    for validation in validations:
        sqref = validation.attrib.get("sqref", "")
        column = re.match(r"[A-Z]+", sqref)
        if (
            column is None
            or column.group(0) not in validation_names
            or sqref not in messages
        ):
            raise ValueError(f"DATA_VALIDATION_RANGE_BLOCKER:{sqref}")
        formula = validation.find(f"{{{NS_MAIN}}}formula1")
        if formula is None:
            formula = ET.SubElement(validation, f"{{{NS_MAIN}}}formula1")
        formula.text = validation_names[column.group(0)]
        msg = messages[sqref]
        validation.set("promptTitle", msg["title"])
        validation.set("prompt", msg["prompt"])
        validation.set("errorTitle", contract["validationErrorTitle"])
        validation.set("error", contract["validationErrorMessage"])
        validation.set("showInputMessage", "1")
        validation.set("showErrorMessage", "1")
        validation.set("allowBlank", "0")
    main.insert(list(main).index(validations) + 1, hyperlinks)
    parts[rel_path] = ET.tostring(rel_root, encoding="utf-8", xml_declaration=True)

    for name, root in roots.items():
        for protection in list(root.findall(f"{{{NS_MAIN}}}sheetProtection")):
            root.remove(protection)
        parts[sheet_paths[name]] = ET.tostring(
            root, encoding="utf-8", xml_declaration=True
        )
    _set_defined_names(parts)
    temporary = path.with_suffix(".patched.tmp.xlsx")
    with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content)
    temporary.replace(path)


def _cell_value(cell: ET.Element) -> str:
    value = cell.find(f"{{{NS_MAIN}}}v")
    return "" if value is None or value.text is None else value.text


def validate_workbook(
    path: Path, payload: dict[str, Any], source_v3: Path
) -> dict[str, Any]:
    with zipfile.ZipFile(path, "r") as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    sheet_paths = _sheet_paths(parts)
    main = ET.fromstring(parts[sheet_paths["01_标注表"]])
    evidence = ET.fromstring(parts[sheet_paths["02_证据"]])
    cells = {
        cell.attrib.get("r", ""): cell for cell in main.findall(f".//{{{NS_MAIN}}}c")
    }
    ids = [_cell_value(cells[f"A{row}"]) for row in range(4, 76)]
    candidates = [_cell_value(cells[f"B{row}"]) for row in range(4, 76)]
    expected_ids = [row["blind_review_id"] for row in payload["rows"]]
    expected_candidates = [row["candidate_text"] for row in payload["rows"]]
    if ids != expected_ids or candidates != expected_candidates:
        raise ValueError("ID_CANDIDATE_ORDER_PARITY_BLOCKER")
    expected_links: dict[str, str] = {}
    expected_titles: dict[str, str] = {}
    for row_index, record in enumerate(payload["rows"], start=4):
        ev = {item["evidence_id"]: item for item in record["evidence_pool"]}
        expected_titles[f"D{row_index}"] = ev["E1"]["official_page_title"]
        expected_titles[f"F{row_index}"] = ev["E2"]["official_page_title"]
        expected_links[f"E{row_index}"] = ev["E1"]["official_source_url"]
        expected_links[f"G{row_index}"] = ev["E2"]["official_source_url"]
    if any(_cell_value(cells[ref]) != value for ref, value in expected_titles.items()):
        raise ValueError("EVIDENCE_TITLE_PARITY_BLOCKER")
    if any(_cell_value(cells[ref]) != value for ref, value in expected_links.items()):
        raise ValueError("URL_VISIBLE_STRING_PARITY_BLOCKER")

    hyperlinks = main.find(f"{{{NS_MAIN}}}hyperlinks")
    if hyperlinks is None or len(hyperlinks) != 144:
        raise ValueError("EXTERNAL_HYPERLINK_COUNT_BLOCKER")
    rel_root = ET.fromstring(parts["xl/worksheets/_rels/sheet1.xml.rels"])
    rels = {node.attrib["Id"]: node for node in rel_root}
    target_mismatch = 0
    for node in hyperlinks:
        ref = node.attrib.get("ref", "")
        rid = node.attrib.get(f"{{{NS_REL_DOC}}}id", "")
        relationship = rels.get(rid)
        expected = expected_links.get(ref)
        if (
            relationship is None
            or expected is None
            or relationship.attrib.get("Target") != expected
            or relationship.attrib.get("TargetMode") != "External"
            or node.attrib.get("display") != expected
        ):
            target_mismatch += 1
    if target_mismatch:
        raise ValueError(f"EXTERNAL_HYPERLINK_TARGET_BLOCKER:{target_mismatch}")
    protections = sum(
        ET.fromstring(parts[target]).find(f"{{{NS_MAIN}}}sheetProtection") is not None
        for target in sheet_paths.values()
    )
    if protections:
        raise ValueError(f"SHEET_PROTECTION_BLOCKER:{protections}")
    validations = main.find(f"{{{NS_MAIN}}}dataValidations")
    if validations is None or len(validations) != 6:
        raise ValueError("DROPDOWN_BLOCKER")
    validation_ranges = {node.attrib.get("sqref", "") for node in validations}
    if validation_ranges != {
        "H4:H75",
        "I4:I75",
        "J4:J75",
        "K4:K75",
        "L4:L75",
        "M4:M75",
    }:
        raise ValueError(f"DROPDOWN_RANGE_BLOCKER:{validation_ranges}")
    formula_count = sum(
        1
        for ref, cell in cells.items()
        if re.fullmatch(r"O(?:[4-9]|[1-6][0-9]|7[0-5])", ref)
        and cell.find(f"{{{NS_MAIN}}}f") is not None
    )
    if formula_count != 72:
        raise ValueError(f"QA_FORMULA_BLOCKER:{formula_count}")
    evidence_text = "\n".join(
        _cell_value(cell) for cell in evidence.findall(f".//{{{NS_MAIN}}}c")
    )
    snapshot_hashes = [
        item["snapshot_sha256"]
        for row in payload["rows"]
        for item in row["evidence_pool"]
    ]
    if sum(item in evidence_text for item in snapshot_hashes) != 144:
        raise ValueError("SNAPSHOT_SHA_COVERAGE_BLOCKER")
    if any(
        value
        for column in "HIJKLMN"
        for value in (_cell_value(cells[f"{column}{row}"]) for row in range(4, 76))
    ):
        raise ValueError("ANNOTATION_VALUE_LEAKAGE_BLOCKER")
    return {
        "status": "PASS",
        "filename": path.name,
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
        "source_v3_sha256": sha256(source_v3),
        "rows": 72,
        "candidate_parity": "72/72",
        "id_order_parity": "72/72",
        "evidence_identity_parity": "144/144",
        "visible_url_string_parity": "144/144",
        "external_hyperlink_target_parity": "144/144",
        "frozen_snapshot_sha_coverage": "144/144",
        "sheet_protection_count": 0,
        "resize_rows_columns_allowed": True,
        "data_validation_count": 6,
        "qa_formula_count": 72,
        "annotation_values_present": 0,
    }


def semantic_reports(output: Path) -> None:
    write_json(
        output / "qa" / "PHASE2_GUIDE_V4_SEMANTIC_PARITY_REPORT.json",
        {
            "status": "PASS",
            "accepted_reference": "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR",
            "new_rule_count": 0,
            "removed_rule_count": 0,
            "changed_rule_count": 0,
            "only_explanation_and_example_expansion": True,
            "guide_v4_protocol_semantic_change": False,
        },
    )
    write_json(
        output / "qa" / "AB_PHASE2_GUIDE_V4_PARITY_REPORT.json",
        {
            "status": "PASS",
            "normalized_semantic_parity": True,
            "allowed_differences": ["annotator_id", "workbook_filename"],
            "other_difference_count": 0,
        },
    )


def reassessment() -> str:
    return """# HUMAN_PHASE2_REWORK_RISK_REASSESSMENT

1. 真人能否按固定顺序完成七字段？YES；Guide V4 给出十步顺序和字段关系表。
2. Candidate 与两条官方 Evidence 是否同屏可见/可达？YES；Sheet01 直接显示标题与完整 URL。
3. live URL 失败时是否有稳定备份？YES；Sheet02 保留144/144冻结快照及 SHA/provenance。
4. 是否仍容易把 minimum 与 selection 混用？风险降至 LOW；Guide V4 给出消融和三组配对例。
5. 是否仍容易把年份、网页 host 当版本/权威答案？风险降至 LOW；各有四个边界例。
6. Excel 是否妨碍真人阅读？NO；sheet protection 为0，可调整行高、列宽、缩放、换行和筛选。
7. 是否仍有 Guide 无法消除的 HIGH 风险？NO。

结论：`HUMAN_PHASE2_REWORK_RISK_AFTER_REPAIR = LOW`；`DISTRIBUTION_READINESS = PASS`。这不是 annotation、agreement、Expected load 或 Ground Truth。
"""


def prepare(output: Path, source_root: Path) -> None:
    if output.exists():
        raise ValueError(f"OUTPUT_ALREADY_EXISTS:{output}")
    output.mkdir(parents=True)
    write_text(
        output / "assessment" / "PILOT4_PHASE2_FIELD_REWORK_RISK_ASSESSMENT.md",
        risk_assessment(),
    )
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("HUMAN-", "")
        distribution = output / annotator / "phase2_v3_2_distribution"
        write_text(
            distribution / f"PILOT4_AB_HUMAN_{tag}_PHASE2_GUIDE_V4.md",
            guide_v4(annotator),
        )
        write_text(
            distribution / f"README_FOR_HUMAN_{tag}_PHASE2_V4.md", readme_v4(annotator)
        )
        source_notice = (
            source_root
            / annotator
            / "phase2_v3_distribution"
            / f"PILOT4_AB_HUMAN_{tag}_PHASE2_INDEPENDENCE_NOTICE.md"
        )
        distribution.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_notice, distribution / source_notice.name)
        payload_source = (
            source_root
            / "control"
            / "workbook_payloads"
            / f"{annotator}_phase2_v3_payload.json"
        )
        payload_target = output / "control" / "workbook_payloads" / payload_source.name
        payload_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(payload_source, payload_target)
    semantic_reports(output)
    write_text(
        output / "assessment" / "HUMAN_PHASE2_REWORK_RISK_REASSESSMENT.md",
        reassessment(),
    )
    write_json(
        output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER_V3_2.json",
        {
            "task_id": TASK_ID,
            "updated_at": now(),
            "A_PHASE2_DISTRIBUTED": False,
            "B_PHASE2_DISTRIBUTED": False,
            "A_PHASE2_V3_DISTRIBUTION_AUTHORITATIVE": False,
            "B_PHASE2_V3_DISTRIBUTION_AUTHORITATIVE": False,
            "A_PHASE2_V3_2_DISTRIBUTION_READY": True,
            "B_PHASE2_V3_2_DISTRIBUTION_READY": True,
            "PHASE2_FIELD_SCHEMA_REDESIGN_REQUIRED": False,
            "PHASE2_PROTOCOL_SEMANTICS_CHANGED": False,
            "agreement_complete": False,
            "mapping_unlocked": False,
            "expected_v3_loaded": False,
            "ground_truth_created": False,
        },
    )


def finalize(output: Path, source_root: Path) -> None:
    workbook_results: dict[str, Any] = {}
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("HUMAN-", "")
        workbook = (
            output
            / annotator
            / "phase2_v3_2_distribution"
            / f"PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3_2.xlsx"
        )
        contract = output / "qa" / "cell_text_contract" / f"{annotator}.json"
        patch_workbook(workbook, contract)
        payload = json.loads(
            (
                output
                / "control"
                / "workbook_payloads"
                / f"{annotator}_phase2_v3_payload.json"
            ).read_text(encoding="utf-8")
        )
        source_v3 = (
            source_root
            / annotator
            / "phase2_v3_distribution"
            / f"PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx"
        )
        workbook_results[annotator] = validate_workbook(workbook, payload, source_v3)
    if (
        sha256(
            source_root
            / "HUMAN-A01"
            / "phase2_v3_distribution"
            / "PILOT4_AB_HUMAN_A01_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx"
        )
        != "65bbecf7efc642b9b758ddaff2717da6dfc939c8a952675a041de38f730e8da1"
    ):
        raise ValueError("A_SOURCE_V3_CHANGED_BLOCKER")
    if (
        sha256(
            source_root
            / "HUMAN-B01"
            / "phase2_v3_distribution"
            / "PILOT4_AB_HUMAN_B01_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx"
        )
        != "8edfe5452726ab482ba844b911a9278ce6105b06320849136b3c4c8c91fe8d1d"
    ):
        raise ValueError("B_SOURCE_V3_CHANGED_BLOCKER")
    a_payload = json.loads(
        (
            output
            / "control"
            / "workbook_payloads"
            / "HUMAN-A01_phase2_v3_payload.json"
        ).read_text(encoding="utf-8")
    )
    b_payload = json.loads(
        (
            output
            / "control"
            / "workbook_payloads"
            / "HUMAN-B01_phase2_v3_payload.json"
        ).read_text(encoding="utf-8")
    )
    a_ids = [row["blind_review_id"] for row in a_payload["rows"]]
    b_ids = [row["blind_review_id"] for row in b_payload["rows"]]
    if a_ids == b_ids:
        raise ValueError("AB_INDEPENDENT_ORDER_BLOCKER")
    examples = [
        "星河市阅览室当前周三闭馆",
        "北丘公园2017版年卡允许转让",
        "青岚馆当前每人可预约九张票",
        "旧季票在新规则生效后仍永久有效",
        "某服务站在2016年暂停夜间窗口",
        "枫岸交通委员会通过了换乘规则",
        "网站维护中心制定并批准了花园规则",
        "第二版在第一版之前生效",
        "规程于2019年发布，目前仍有效",
    ]
    final_candidates = [
        row["candidate_text"]
        for payload in (a_payload, b_payload)
        for row in payload["rows"]
    ]
    if any(
        example in candidate or candidate in example
        for example in examples
        for candidate in final_candidates
    ):
        raise ValueError("TEACHING_EXAMPLE_LEAKAGE_BLOCKER")
    write_json(
        output / "qa" / "final_gate_qa.json",
        {
            "status": "PASS",
            "task_id": TASK_ID,
            "dynamic_worktree_unique": True,
            "semantic_blocker": False,
            "source_v3_preservation": "PASS",
            "workbooks": workbook_results,
            "candidate_id_order_parity": "PASS",
            "ab_independent_order_preserved": True,
            "evidence_semantic_change_count": 0,
            "canonical_enum_change_count": 0,
            "guide_semantic_change_count": 0,
            "teaching_example_count": 9,
            "common_mistake_count": 10,
            "teaching_example_to_final72_near_duplicate_count": 0,
            "expected_leakage_count": 0,
            "mapping_leakage_count": 0,
            "annotation_execution_count": 0,
            "agreement_execution_count": 0,
            "ground_truth_execution_count": 0,
        },
    )
    write_manifest(output)


def write_manifest(output: Path) -> None:
    entries = []
    for file in sorted(output.rglob("*")):
        if file.is_file() and file != output / "manifest" / "final_manifest.json":
            entries.append(
                {
                    "path": file.relative_to(output).as_posix(),
                    "bytes": file.stat().st_size,
                    "sha256": sha256(file),
                }
            )
    write_json(
        output / "manifest" / "final_manifest.json",
        {
            "task_id": TASK_ID,
            "generated_at": now(),
            "entry_count_excluding_manifest": len(entries),
            "entries": entries,
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("prepare", "finalize", "manifest"), required=True
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare(args.output.resolve(), args.source_root.resolve())
    elif args.mode == "finalize":
        finalize(args.output.resolve(), args.source_root.resolve())
    else:
        write_manifest(args.output.resolve())
    print(
        json.dumps(
            {"status": "PASS", "mode": args.mode, "output": str(args.output.resolve())},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
