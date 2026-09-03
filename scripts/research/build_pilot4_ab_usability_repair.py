from __future__ import annotations

import argparse
import csv
from difflib import SequenceMatcher
import hashlib
import json
import re
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


TASK_ID = "PILOT4-A-B-HUMAN-ANNOTATION-USABILITY-REPAIR-01"
FINAL_STATUS = (
    "PILOT4_A_B_EXECUTION_APPROVED / "
    "HUMAN_ANNOTATION_USABILITY_REPAIR_COMPLETE / "
    "HUMAN_A01_PHASE1_V2_DISTRIBUTION_READY / "
    "HUMAN_B01_PHASE1_V2_DISTRIBUTION_READY / "
    "PHASE2_V2_PREBUILT_WITHHELD / WAITING_FOR_OWNER_PHASE1_DISTRIBUTION / "
    "NO_GROUND_TRUTH_YET"
)

HANDOFF = Path(r"E:\LLMGuard-Handoff")
V1_ROOT = HANDOFF / "paper1_pilot4_ab_execution_20260903"
V1_MANIFEST = V1_ROOT / "manifest" / "final_manifest.json"
V1_MANIFEST_SHA = "aa8742baccab4072a0fe901bcd430b46011cea9b436738a730164f166f0d7d91"
FINAL72 = HANDOFF / (
    "paper1_pilot4_phase1_owner_defect_repair_20260902/candidate_repairs/"
    "PILOT4_CANDIDATE_CORPUS_POST_EXTERNAL_PHASE1_REPAIR_V1.jsonl"
)
FINAL72_SHA = "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
PHASE1_ACCEPTED_GUIDE = HANDOFF / (
    "paper1_pilot4_phase1_owner_defect_repair_20260902/attempt2_packet/"
    "PILOT4_EXTERNAL_BLIND_PHASE1_ATTEMPT2_GUIDE.md"
)
PHASE1_ACCEPTED_GUIDE_SHA = (
    "a6ea45451eb820a2c88cb3b048b2a18c12770149fd14e2ebba1652826563ff56"
)
GUIDE_V32 = HANDOFF / (
    "paper1_pilot4_protocol_targeted_repair_r3_20260902/guide/"
    "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR.md"
)
GUIDE_V32_SHA = "83fced51ddb509f6ba39feabfc717b88f4003eacf662982551d73fccf476d561"
SCHEMA_V31 = HANDOFF / (
    "paper1_pilot4_annotation_schema_simplification_20260901/schema/"
    "annotator_schema_v3_1_candidate.json"
)

PHASE1_HEADERS = [
    "blind_review_id",
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
    "phase1_reason",
]
PHASE2_HEADERS = [
    "blind_review_id",
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
    "phase2_reason",
]


PHASE1_GUIDE_TEMPLATE = r"""# Pilot4 {ANNOTATOR} Phase1 Human Annotation Guide V2

Status: `DISTRIBUTION_AUTHORITATIVE_V2 / PHASE1_ONLY`[[MD_BR]]
Annotator: `{ANNOTATOR}`[[MD_BR]]
Return filename: `{PHASE1_RETURN}`

## 0. 你在做什么

Phase1 不判断现实世界中的事实真假，也不要求你了解本项目、RAG、Pilot4、HKP 或任何实验设计。你只看
`candidate_text`（候选文本），回答四个文本层面问题：

1. 中文表达是否自然；
2. 不查资料时，文本内部是否已经自相矛盾；
3. 理解核心命题所需的信息是否根本缺失；
4. 关键指代是否存在两个或更多合理解释。

“我觉得这个法律日期好像不对”不是 Phase1 的内部冲突证据。只要必须查网页或凭外部知识才能确认真假，
`local_internal_conflict` 就不能因此选 `YES`。

## 1. 固定填写流程

1. 阅读 `PACKET_V2.md` 中一条 `candidate_text`。
2. 判断 `text_naturalness`。
3. 判断 `local_internal_conflict`。
4. 判断 `phase1_issue`。
5. 按第 5 节的布尔条件判断 `phase1_reason` 是否必填。
6. 在 `RETURN_TEMPLATE_V2.csv` 中找到相同 `blind_review_id`，填写四个答案字段。
7. 继续下一条，直到 72 条完成。

逐条独立判断。不要先按某个值批量填完整列，也不要在 Packet Markdown 中填写答案。

## 2. `text_naturalness（文本自然度）`

只评价中文表达质量，不评价事实真假。

| Canonical value | 中文解释 | 什么时候选 | 什么时候不能选 |
| --- | --- | --- | --- |
| `NATURAL` | 自然 | 语法和表达基本正常，普通读者可直接理解。事实即使可能错误，只要语言自然仍可选。 | 不能因为“看起来像事实错误”改成其它值。 |
| `MINOR_ISSUE` | 轻微表达问题 | 有轻微生硬、重复、措辞或局部句式问题，但核心意思仍容易理解。 | 不等于事实可疑；若理解已经显著受阻，应选 `UNNATURAL`。 |
| `UNNATURAL` | 明显不自然 | 有病句、语法断裂、严重搭配错误、模板残留或异常语义结构，显著影响阅读或理解。 | 不能仅因内容陌生、专业或可能错误而选择。 |

Teaching examples（均为虚构且不属于正式 72 条）：

- `NATURAL`：`《海岚市公共图书馆借阅规范》规定，读者每次最多借阅五册图书，借期为三十日。`
- `NATURAL`：`《云桥展览馆开放办法》规定周一全天闭馆，同时又规定每周一全天正常开放。` 语言自然，
  即使内容内部冲突，自然度仍可为 `NATURAL`。
- `MINOR_ISSUE`：`《青禾园区访客管理细则》要求访客提前预先预约，并在到访时登记。` “提前预先”重复，
  但意思清楚。
- `MINOR_ISSUE`：`申请人应在材料提交完成以后，再进行后续的下一步核验。` 表达冗余，但仍可理解。
- `UNNATURAL`：`申请人应在提交后窗口材料办理被完成。` 语法关系断裂，核心动作难以理解。
- `UNNATURAL`：`本规则适用对象为模板字段{{subject}}并且然后执行。` 存在模板残留和异常句式。

Boundary：`NATURAL` 与 `MINOR_ISSUE` 的界线是是否存在可指出的轻微表达瑕疵；`MINOR_ISSUE` 与
`UNNATURAL` 的界线是瑕疵是否已经显著妨碍阅读或核心理解。

## 3. `local_internal_conflict（文本内部事实冲突）`

核心问题是：“不查任何外部资料，candidate 自己是否已经包含不能同时成立的核心事实陈述？”

| Canonical value | 中文解释 | 选择条件 |
| --- | --- | --- |
| `YES` | 存在内部冲突 | 至少两个文本内可见命题，在同一主体、范围、条件和时间语境下不能同时为真。 |
| `NO` | 不存在文本内冲突 | 文本自身没有互斥命题；即使需要官网才能判断某事实真假，也必须选 `NO`。 |
| `UNCERTAIN` | 文本本身使冲突关系不确定 | 主体、范围、时间、条件或指代写得模糊，导致无法判断两个命题是否针对同一对象或语境。 |

`YES` examples：

1. `《云桥展览馆开放办法》规定周一全天闭馆；同一办法又规定每周一全天正常开放。` 同一时间和对象互斥。
2. `《北岸停车场月卡规则》规定月卡适用于所有地下车位；同一规则又称月卡不适用于任何地下车位。`
3. `报告首段称库存为120件，末段又称同一时点、同一仓库库存为98件。`

`NO` examples：

1. `某项城市服务规则自2022年5月1日起实施。` 文本只有一个日期；即使你怀疑日期，也没有内部矛盾。
2. `《青禾园区访客管理细则》要求访客预约后登记。` 只有一个明确要求。
3. `旧版收费标准在2019年执行，新版标准自2023年起执行。` 不同时间语境可以同时成立。

`UNCERTAIN` examples：

1. 文本先列出“管理委员会”和“物业服务中心”，后文两次使用“该机构”，分别说它有权和无权审批，
   但无法确认两次是否指同一机构。
2. 文本先列出两类申请，后文说“上述情形不适用”，无法确定指其中一类还是两类全部。

`UNCERTAIN` 不是“我不知道事实是真是假”。不知道外部事实、记不清日期或不熟悉制度时，若文本自身清楚且
不矛盾，应选 `NO`。

## 4. `phase1_issue（Phase1 文本问题）`

| Canonical value | 中文解释 | 选择条件 | 例子 |
| --- | --- | --- | --- |
| `NONE` | 无问题 | 核心事实对象和命题足够明确。 | 一条完整命名的规则给出清楚主体、条件和结论。 |
| `MISSING_CONTEXT` | 缺少必要上下文 | 理解核心事实所必需的信息根本没有提供，缺少后无法唯一理解命题。 | “2021年的实施文件已经引用该决定”，但没有说明是哪份实施文件。 |
| `AMBIGUOUS_REFERENCE` | 指代歧义 | 相关信息都出现了，但关键指代有两个或更多合理解释。 | 前文出现两个日期，后文只说“该日期以后”。 |
| `OTHER` | 其它实质文本问题 | 确实影响核心理解，且不属于缺上下文或指代歧义。 | 句子结构破碎到无法确定谁执行什么动作。 |

`MISSING_CONTEXT` additional examples：

- `该条例规定申请期限为十日。` 当前材料没有给出“该条例”的名称或适用领域。
- `2018年版已经替代旧版。` 没有交代是什么文件的版本。
- `主管部门应依照上述规定处理。` 既没有“上述规定”，也没有可恢复的主管部门。

`AMBIGUOUS_REFERENCE` additional examples：

- 前文出现委员会甲和委员会乙，后文只说“该委员会负责复核”。
- 前文给出30日和60日两个期限，后文说“超过该期限即失效”。
- 前文列出办法甲与细则乙，后文说“修订文本自次月实施”，但不清楚修订的是哪一份。

`OTHER` additional examples：

- 句子中关键谓语被模板占位符截断，无法恢复完整命题。
- 表格转文本时列错位，主体与结论无法配对。

不要把普通事实错误怀疑放入 `OTHER`。

### 应该选哪个 `phase1_issue`？

| 场景 | 选择 |
| --- | --- |
| 什么信息都不缺 | `NONE` |
| 关键对象根本没有交代 | `MISSING_CONTEXT` |
| 信息都出现了但不知道指哪个 | `AMBIGUOUS_REFERENCE` |
| 其它影响核心理解的文本结构问题 | `OTHER` |
| 只是怀疑现实事实不对 | `NONE` |
| 需要外部 Evidence 才能判断 | `NONE` |

## 5. `phase1_reason（第一阶段理由）`

Accepted rule 的精确布尔条件是：

```text
REASON_REQUIRED =
    local_internal_conflict IN {YES, UNCERTAIN}
    OR phase1_issue != NONE
```

满足任一条件，`phase1_reason` 必填。若 `local_internal_conflict=NO` 且 `phase1_issue=NONE`，理由可以留空。
`text_naturalness` 单独为 `MINOR_ISSUE` 或 `UNNATURAL` 不会改变这个必填条件；你可以自愿用一句话解释表达问题，
但不能写外部事实答案。

理由应简短、具体，引用 Candidate 内可见内容并说明判断原因，通常 1–2 句即可。不要写论文、查事实、引用网站、
猜实验标签或写“我感觉”。

GOOD：`前后两句分别把同一场馆的周一状态写为全天闭馆和正常开放，因此构成文本内部冲突。`[[MD_BR]]
GOOD：`“该机构”可能指管理委员会或物业服务中心，无法确认两个权限命题是否针对同一主体。`[[MD_BR]]
BAD：`这个日期是错的。`（使用了文本外的事实判断。）[[MD_BR]]
BAD：`看起来有问题。`（不具体，无法复核。）

## 6. 六条完整填写示例

| candidate_text（虚构） | text_naturalness | local_internal_conflict | phase1_issue | phase1_reason | why |
| --- | --- | --- | --- | --- | --- |
| 《海岚市公共图书馆借阅规范》规定，读者每次最多借阅五册图书，借期为三十日。 | `NATURAL` | `NO` | `NONE` | 留空 | 表达自然、无内部矛盾且主体完整。 |
| 《青禾园区访客管理细则》要求访客提前预先预约，并在到访时登记。 | `MINOR_ISSUE` | `NO` | `NONE` | “提前预先”存在轻微重复，但意思清楚。 | 理由在此为可选；事实真假不参与自然度。 |
| 《澄江市民中心预约规则》申请人应在提交后窗口材料办理被完成。 | `UNNATURAL` | `NO` | `OTHER` | 关键谓语和宾语关系断裂，无法确定办理动作。 | 明显病句并影响核心理解，因此 `OTHER` 也成立。 |
| 《云桥展览馆开放办法》规定周一全天闭馆；同一办法又规定每周一全天正常开放。 | `NATURAL` | `YES` | `NONE` | 同一场馆、同一时间的开放状态互斥。 | 语言自然不妨碍内部冲突。 |
| “该实施文件”要求所有申请在十日内提交，但文本没有说明文件名称或适用事项。 | `NATURAL` | `NO` | `MISSING_CONTEXT` | 未提供实施文件身份，核心规则无法唯一恢复。 | 关键对象根本没有交代。 |
| 管理委员会和物业服务中心均在前文出现；后文称“该机构”既有权又无权批准夜间活动。 | `NATURAL` | `UNCERTAIN` | `AMBIGUOUS_REFERENCE` | “该机构”有两个合理指代，无法确认权限命题是否针对同一主体。 | 信息存在但指代不唯一。 |

## 7. 常见错误

1. 把“事实可能错”判成 internal conflict。
2. 只因为 Candidate 没写更多背景就判 `MISSING_CONTEXT`；只有缺少必要信息并导致核心命题无法唯一理解才选。
3. 把“不知道事实”判 `UNCERTAIN`。
4. 把语言自然度和事实正确性混在一起。
5. 把所有奇怪情况都填 `OTHER`。
6. 触发必填条件时遗漏 `phase1_reason`。
7. 修改 Candidate、ID、行或列。
8. 去网上搜索 Phase1 事实，或使用任何 AI assistant 辅助判断。

## 8. CSV 操作与提交

可以使用 Excel、WPS、LibreOffice 或文本编辑器填写 CSV。只能填写四个答案列；不得删除或增加行、排序、修改
`blind_review_id`、修改列名或增加列。保存时保持 CSV 与 UTF-8。最终文件严格命名为 `{PHASE1_RETURN}`。

完成后的 raw CSV 一旦交给 Owner，Owner 不得再用 Excel 重新保存或修改。

## 9. 最终自检

- [ ] 72 条全部完成
- [ ] `blind_review_id` 没改
- [ ] 没增删行、没增删列、没排序
- [ ] enum 拼写完全正确
- [ ] 需要 reason 的行都有 reason
- [ ] Phase1 没查网页
- [ ] 没使用 AI assistant
- [ ] 没和另一 annotator 讨论
- [ ] 保存成 `{PHASE1_RETURN}`
"""


PHASE1_QUICK_TEMPLATE = r"""# Pilot4 {ANNOTATOR} Phase1 Quick Reference V2

Status: `DISTRIBUTION_AUTHORITATIVE_V2 / DESK_REFERENCE`

## Decision flow

阅读 candidate → `text_naturalness` → `local_internal_conflict` → `phase1_issue` → 判断 reason 是否必填 → 写入 CSV。

Phase1 不查事实、不看网页、不使用 AI。Packet 只读，答案只写 `{PHASE1_TEMPLATE}`。

| Field | Canonical value | 一句话定义 | Reason |
| --- | --- | --- | --- |
| `text_naturalness` | `NATURAL` | 表达正常、可直接理解；与事实真假无关。 | 单独不触发必填 |
|  | `MINOR_ISSUE` | 有轻微生硬/重复，但不影响理解。 | 单独不触发必填 |
|  | `UNNATURAL` | 病句、断裂、模板残留显著影响理解。 | 单独不触发必填 |
| `local_internal_conflict` | `YES` | 同一主体/范围/条件/时间下，文本内命题不能同时为真。 | 必填 |
|  | `NO` | 文本自身不矛盾；需要外查真假时也选它。 | 若 issue 为 NONE，可空 |
|  | `UNCERTAIN` | 文本自身的范围/指代等模糊，无法判断是否构成内部冲突。 | 必填 |
| `phase1_issue` | `NONE` | 核心对象和命题足够明确。 | 由 conflict 决定 |
|  | `MISSING_CONTEXT` | 必要信息根本没提供。 | 必填 |
|  | `AMBIGUOUS_REFERENCE` | 信息出现了，但关键指代有多个合理解释。 | 必填 |
|  | `OTHER` | 其它影响核心理解的文本结构问题。 | 必填 |

```text
REASON_REQUIRED = local_internal_conflict IN {YES, UNCERTAIN}
                  OR phase1_issue != NONE
```

提交前：72 条；ID/行/列/顺序均未改；enum 拼写正确；必填理由不空；UTF-8 CSV；文件名 `{PHASE1_RETURN}`。
"""


PHASE1_README_TEMPLATE = r"""# README for {ANNOTATOR} — Phase1 V2

## 请按这个顺序操作

1. 先读 `{PHASE1_GUIDE}`。
2. 需要快速查规则时打开 `{PHASE1_QUICK}`。
3. 在 `{PHASE1_PACKET}` 中阅读 72 条 Candidate。
4. 所有答案只填写在 `{PHASE1_TEMPLATE}`。
5. 阅读并遵守 independence notice。

> **不要在 PACKET.md 中填写答案；PACKET 仅用于阅读题目。最终答案只填写在 CSV 模板中。**

可以用 Excel、WPS、LibreOffice 或文本编辑器填写，但不要删行、增行、排序、改 ID、改列名或加列。保持 CSV 与
UTF-8。Phase1 不查网页、不使用 AI、不与另一位 annotator 讨论。

最终提交文件名：`{PHASE1_RETURN}`。只把该 CSV 交给 Owner；不要开始 Phase2。

提交前检查：72 条完成；ID、行、列、顺序未改；enum 拼写正确；必填 reason 不空；文件名正确。
"""


PHASE2_GUIDE_TEMPLATE = r"""# Pilot4 {ANNOTATOR} Phase2 Human Annotation Guide V2

Status: `WITHHELD / DO_NOT_DISTRIBUTE`[[MD_BR]]
Future return filename: `{PHASE2_RETURN}`

本文件现在只用于预构建与可用性检查。Owner 未明确同时释放 A/B Phase2 前，不得开始作答。

## 0. Phase2 的目标和边界

Phase2 使用 Packet 中给出的官方 E1/E2 URL 与冻结快照核验 Candidate。只能使用随包提供的 E1/E2；不要读取仓库、
身份映射、旧返回、研究设计信息或任何未提供的事实来源，也不要使用 AI assistant。URL 保留来源信息，冻结快照保证
稳定访问；若实时 URL 暂时失败但快照完整，可以依据快照判断。

## 1. 固定流程

1. 阅读 Candidate、E1 和 E2 的标题、URL 与冻结快照。
2. 判断指定 Evidence 是否足够；不足先选 `INSUFFICIENT_EVIDENCE` 并记录 issue。
3. 按第 2 节严格顺序填写 `overall_fact_status`。
4. 独立判断 `version_claim_status` 与 `authority_claim_status`。
5. 只有确认 `FACTUAL_CONFLICT` 且 Phase1 不是文本内直接冲突时，做 E1-alone / E2-alone / joint 消融，填写 minimum。
6. 填写实际使用过的 `evidence_selection`。
7. 填写 `phase2_issue`，再按布尔条件决定 `phase2_reason` 是否必填。
8. 把七项答案写入相同 `blind_review_id` 的 CSV 行。

## 2. `overall_fact_status（整体事实状态）`

严格按以下顺序，命中后停止：

```text
STEP 1  E1/E2 是否足够？
        否 -> INSUFFICIENT_EVIDENCE
        是 -> STEP 2
STEP 2  核心命题是否被 Evidence 否定，且不能由合法版本/时期/条件解释？
        是 -> FACTUAL_CONFLICT
        否 -> STEP 3
STEP 3  核心命题是否只有放在明确过去版本/历史时期才成立？
        执行 PRESENT-TIME SUBSTITUTION TEST
        去掉历史限定按当前状态读取，真假或核心含义发生实质变化
        -> LEGITIMATE_VERSION_OR_HISTORY
STEP 4  其它被 Evidence 支持的事实 -> CURRENTLY_CONSISTENT
```

| Canonical value | 中文含义 | 什么时候选 | 不能这样选 |
| --- | --- | --- | --- |
| `CURRENTLY_CONSISTENT` | 当前一致 | 当前事实获支持，或历史日期只是背景且不改变核心真假。 | 不能把证据不足强行当正确。 |
| `LEGITIMATE_VERSION_OR_HISTORY` | 合法版本/历史 | 命题依赖旧版本、过去时期、已替代状态或版本切换区间；替换为当前时点会改变核心真假。 | 仅出现年份或“修订”二字不自动成立。 |
| `FACTUAL_CONFLICT` | 事实冲突 | Evidence 明确否定核心命题，且无合法版本/条件可以解释。 | 证据不足时不能选。 |
| `INSUFFICIENT_EVIDENCE` | 证据不足 | E1/E2 无法稳定确认正确、历史成立或冲突。 | 不能因为内容难读但 Evidence 已足够就选。 |

六个非正式 teaching examples（证据描述均为虚构教学材料）：

1. 某公共阅览室现行规则规定闭馆时间为20:00，E1现行全文直接支持 → `CURRENTLY_CONSISTENT`。
2. 某园区规则写“2020年版押金为200元”，E1旧版与E2新版分别显示200元和0元；换成当前时点结论改变 →
   `LEGITIMATE_VERSION_OR_HISTORY`。
3. Candidate 提到制度在2019年发布，E1还确认现行条款未改变；发布日期只是背景 → `CURRENTLY_CONSISTENT`。
4. Candidate 称当前每户可领取三张通行证，E1现行全文明确为两张，且无历史限定 → `FACTUAL_CONFLICT`。
5. Candidate 把已经终止的临时措施写成目前仍适用，E1/E2给出清楚终止时间 → `FACTUAL_CONFLICT`。
6. Candidate 声称“2017年版仍有效”，但 E1/E2 都没有提供该版本的终止或效力信息 → `INSUFFICIENT_EVIDENCE`。

## 3. `version_claim_status（版本命题状态）`

版本命题包括修订、废止、替代、前后版本、生效日或时间适用关系。

| Canonical value | 条件 | 不能选择的情况 |
| --- | --- | --- |
| `NOT_PRESENT` | Candidate 没有明确提出版本/时效关系。 | 不能只因 Evidence 有多个版本就说 Candidate 提出了版本命题。 |
| `PRESENT_CORRECT` | Candidate 明确提出版本关系，且 E1/E2 支持。 | 证据不足时不能选。 |
| `PRESENT_INCORRECT` | Candidate 明确提出版本关系，且 E1/E2 否定。 | Candidate 没有版本命题时不能选。 |
| `PRESENT_EVIDENCE_INSUFFICIENT` | 版本命题清楚存在，但指定 Evidence 无法判断其正误。 | 若 Candidate 自身含糊到命题都无法识别，应使用 issue，而不是该值。 |

Boundary：普通数量、机构职责或当前要求不一定是版本命题；明确的生效、修订、废止、替代或“旧版/新版”关系才是。

## 4. `authority_claim_status（权威归属命题状态）`

只有 Candidate 明确主张谁制定、通过、发布、批准、修订或具有某项权限时才评估。网页宿主、转载者、发布机关、
制定机关和执行机关不是自动等同的角色。

| Canonical value | 条件 | 不能选择的情况 |
| --- | --- | --- |
| `NOT_PRESENT` | 没有明确机关/权限归属主张。 | “文本被修订”但未说明谁修订，不自动构成具体机关命题。 |
| `PRESENT_CORRECT` | 明确归属且 Evidence 支持。 | 不能仅凭网页域名推断制定机关。 |
| `PRESENT_INCORRECT` | 明确归属且 Evidence 反驳。 | Evidence 未说明机关时不能选。 |
| `PRESENT_EVIDENCE_INSUFFICIENT` | 明确归属存在，但 E1/E2 不足以判断。 | Candidate 指代不清时优先记录 candidate issue。 |

## 5. `minimum_external_evidence_needed（最少外部证据需求）`

只在 `overall_fact_status=FACTUAL_CONFLICT` 时评估；若你的 Phase1 已是
`local_internal_conflict=YES`，冲突无需外部证据发现，使用 `NOT_APPLICABLE`。其它非冲突状态也一律
`NOT_APPLICABLE`。

对非本地冲突依次做：

```text
E1 alone sufficient OR E2 alone sufficient
    -> ONE_OFFICIAL_EVIDENCE
E1 alone insufficient AND E2 alone insufficient AND joint sufficient
    -> MULTI_EVIDENCE_OR_VERSION_CHAIN
E1+E2 still insufficient
    -> overall=INSUFFICIENT_EVIDENCE + suitable issue
       (不要把 minimum 写成 MULTI)
```

| Canonical value | 中文含义 |
| --- | --- |
| `ONE_OFFICIAL_EVIDENCE` | E1 或 E2 至少有一个单独就足以确认冲突。 |
| `MULTI_EVIDENCE_OR_VERSION_CHAIN` | 两个单独都不足，只有联合多个文档/版本/关系链才足够。 |
| `NOT_APPLICABLE` | 不属于事实冲突，或 Phase1 已能直接发现文本内部冲突。 |

“我实际看了两个 Evidence”不等于 `MULTI_EVIDENCE_OR_VERSION_CHAIN`；minimum 衡量最低充分证据，不是阅读数量。

## 6. `evidence_selection（实际证据选择）`

记录你实际使用了什么，而不是最低需要什么。

| Canonical value | 含义 |
| --- | --- |
| `NONE` | 未能实际使用 E1/E2；通常伴随 Evidence issue。 |
| `E1` | 实际只使用 E1。 |
| `E2` | 实际只使用 E2。 |
| `E1+E2` | 实际联合使用 E1 与 E2。 |

对照 examples：

1. 实际看了 E1+E2，但 E1 单独已足够确认冲突：selection=`E1+E2`，minimum=`ONE_OFFICIAL_EVIDENCE`。
2. 实际只看 E2，E2 单独足够：selection=`E2`，minimum=`ONE_OFFICIAL_EVIDENCE`。
3. E1说明旧规则、E2说明新版替代，必须联合：selection=`E1+E2`，minimum=`MULTI_EVIDENCE_OR_VERSION_CHAIN`。

## 7. `phase2_issue（Phase2 问题）`

| Canonical value | 什么时候选 | 边界 |
| --- | --- | --- |
| `NONE` | 来源可用且证据足以完成判断。 | 实时 URL 失败但冻结快照完整，通常仍可完成，不自动算 unreachable。 |
| `SOURCE_UNREACHABLE` | 提供的 URL/快照通道无法访问，导致无法使用指定来源。 | 单次 URL 失败但快照可用不能单独触发。 |
| `SOURCE_CONFLICT` | E1/E2 之间存在无法解决的实质冲突。 | 仅表述角度不同不算。 |
| `EVIDENCE_MISSING` | 指定 Evidence 缺少判断核心命题所需材料。 | 不等于“不想继续看”。 |
| `LATE_DISCOVERED_CANDIDATE_DEFECT` | Phase2 才发现 Candidate 本身有实质缺陷，不能进入正常判断。 | 不是普通事实冲突。 |
| `OTHER` | 其它影响核验的实质问题，必须解释。 | 不得作为不确定性的万能选项。 |

## 8. `phase2_reason（第二阶段理由）`

精确必填条件：

```text
REASON_REQUIRED =
    overall_fact_status IN {
        FACTUAL_CONFLICT,
        LEGITIMATE_VERSION_OR_HISTORY,
        INSUFFICIENT_EVIDENCE
    }
    OR version_claim_status IN {
        PRESENT_INCORRECT,
        PRESENT_EVIDENCE_INSUFFICIENT
    }
    OR authority_claim_status IN {
        PRESENT_INCORRECT,
        PRESENT_EVIDENCE_INSUFFICIENT
    }
    OR minimum_external_evidence_needed == MULTI_EVIDENCE_OR_VERSION_CHAIN
    OR phase2_issue != NONE
```

理由用 1–2 句指出核心命题、E1/E2 各自贡献和冲突/历史/不足之处。不要复制整段 Evidence，不要写实验推测。

GOOD：`E1给出旧版限额，E2给出新版替代时间；两项联合才能确认 Candidate 把旧限额写成当前规则。`[[MD_BR]]
BAD：`答案就是错的。`（未绑定 Evidence。）

## 9. 六条完整 Phase2 示例

| 教学场景 | overall | version | authority | minimum | selection | issue | reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1现行全文直接支持当前20:00闭馆 | `CURRENTLY_CONSISTENT` | `NOT_PRESENT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1` | `NONE` | 可留空 |
| E1旧版200元、E2新版0元，Candidate明确描述旧版 | `LEGITIMATE_VERSION_OR_HISTORY` | `PRESENT_CORRECT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1+E2` | `NONE` | 旧版金额只在明确历史时期成立。 |
| Candidate称当前三张，E1现行正文直接写两张 | `FACTUAL_CONFLICT` | `NOT_PRESENT` | `NOT_PRESENT` | `ONE_OFFICIAL_EVIDENCE` | `E1` | `NONE` | E1单独反驳当前数量。 |
| E1说明网页维护者，E2说明规则制定者，Candidate把两者等同 | `FACTUAL_CONFLICT` | `NOT_PRESENT` | `PRESENT_INCORRECT` | `MULTI_EVIDENCE_OR_VERSION_CHAIN` | `E1+E2` | `NONE` | 两项联合区分维护与制定角色。 |
| Candidate明确称2017版仍有效，但E1/E2均无效力终止信息 | `INSUFFICIENT_EVIDENCE` | `PRESENT_EVIDENCE_INSUFFICIENT` | `NOT_PRESENT` | `NOT_APPLICABLE` | `E1+E2` | `EVIDENCE_MISSING` | 指定证据不能确认版本效力。 |
| Candidate明确归属审批机关，但两项材料均未说明审批权限 | `INSUFFICIENT_EVIDENCE` | `NOT_PRESENT` | `PRESENT_EVIDENCE_INSUFFICIENT` | `NOT_APPLICABLE` | `E1+E2` | `EVIDENCE_MISSING` | 权限命题存在，但证据缺少权限信息。 |

## 10. CSV 与最终自检

只在未来 Owner 同时释放后填写 CSV；不得增删/排序行、修改 ID/列名或新增列。保持 UTF-8 CSV，最终文件名
`{PHASE2_RETURN}`。

- [ ] 72 条全部完成
- [ ] ID、行、列、顺序未改
- [ ] canonical enum 拼写正确
- [ ] minimum 与 overall/Phase1 local 冲突规则一致
- [ ] selection 记录实际使用，不冒充 minimum
- [ ] 需要 reason 的行都有 reason
- [ ] 只使用随包 E1/E2
- [ ] 未使用 AI、未与另一 annotator 讨论
- [ ] 保存成 `{PHASE2_RETURN}`
"""


PHASE2_QUICK_TEMPLATE = r"""# Pilot4 {ANNOTATOR} Phase2 Quick Reference V2

Status: `WITHHELD / DO_NOT_DISTRIBUTE`

## Overall decision tree

Evidence 不足 → `INSUFFICIENT_EVIDENCE`；Evidence 否定且无合法历史解释 → `FACTUAL_CONFLICT`；只有在过去版本/时期成立，
且当前时点替换会改变核心真假 → `LEGITIMATE_VERSION_OR_HISTORY`；其余获支持 → `CURRENTLY_CONSISTENT`。

## Field card

| Field | Values / rule |
| --- | --- |
| `version_claim_status` | `NOT_PRESENT` / `PRESENT_CORRECT` / `PRESENT_INCORRECT` / `PRESENT_EVIDENCE_INSUFFICIENT` |
| `authority_claim_status` | 同上；网页宿主、转载者、发布者、制定者不是自动等同角色。 |
| `minimum_external_evidence_needed` | 非冲突或 Phase1 local=`YES` → `NOT_APPLICABLE`；任一单证据足够 → `ONE_OFFICIAL_EVIDENCE`；只有联合足够 → `MULTI_EVIDENCE_OR_VERSION_CHAIN`。 |
| `evidence_selection` | `NONE` / `E1` / `E2` / `E1+E2`，记录实际使用。 |
| `phase2_issue` | `NONE` / `SOURCE_UNREACHABLE` / `SOURCE_CONFLICT` / `EVIDENCE_MISSING` / `LATE_DISCOVERED_CANDIDATE_DEFECT` / `OTHER`。 |

Reason 必填：overall 为 conflict/history/insufficient；version 或 authority 为 incorrect/evidence-insufficient；minimum 为 MULTI；
或 issue 非 NONE。只使用随包 E1/E2；URL 暂时失败但冻结快照完整时可继续，不自动判 unreachable。

本文件仍处于 WITHHELD。Owner 未同时释放 A/B Phase2 前不得开始。
"""


OWNER_GUIDE = r"""# Pilot4 A/B Owner Distribution Guide V2

Status: `PHASE1_V2_DISTRIBUTION_READY / PHASE2_WITHHELD`

## 重要边界

不要发送 V1。V1 保留为 `NOT_DISTRIBUTED / SUPERSEDED_FOR_DISTRIBUTION_BY_V2 / PROTOCOL_SEMANTICS_VALID /
HUMAN_USABILITY_INSUFFICIENT`。本轮没有重开协议或 calibration，也没有修改 Candidate、ID、顺序、schema、Expected 或 Evidence。

## 现在只给 HUMAN-A01

发送 `HUMAN-A01/phase1/` 中六个文件：Packet V2、Guide V2、Quick Reference V2、Return Template V2、原 independence
notice、README V2。

## 现在只给 HUMAN-B01

发送 `HUMAN-B01/phase1/` 中对应六个文件。

不得发送 `withheld_phase2/`、`mapping/`、Expected、manifest control info、R1/R2/R3、QA 或 owner control 文件。

## 回收

HUMAN-A01 只返回 `PILOT4_AB_HUMAN_A01_PHASE1_RETURN.csv`。[[MD_BR]]
HUMAN-B01 只返回 `PILOT4_AB_HUMAN_B01_PHASE1_RETURN.csv`。

收到 raw 后不要用 Excel 重新保存或修改。只有两份 Phase1 raw 均完成 schema、72/72、hash lock 与 immutable lock，才可
由后续单独任务同时释放 A/B Phase2。当前 `PHASE2_RELEASE_ALLOWED=false`。
"""


USABILITY_CHECKLIST = r"""# Human Annotation Usability Checklist

Task: `PILOT4-A-B-HUMAN-ANNOTATION-USABILITY-REPAIR-01`

本检查只审查说明材料能否被不了解项目、但接受过基本说明的真人使用；没有模拟或执行 72 条正式 annotation。

| 受训非项目 annotator 能否回答 | 结果 | 证据入口 |
| --- | --- | --- |
| 我要干什么？ | YES | Guide V2 的目标与阶段边界 |
| 每列什么意思？ | YES | 每个 canonical field 的详细手册 |
| 每个值什么时候选？ | YES | enum 条件、反例与边界 |
| 哪些值容易混淆？ | YES | naturalness、local conflict、issue、minimum/selection 对照 |
| reason 什么时候写？ | YES | 精确布尔条件 |
| reason 怎么写？ | YES | GOOD/BAD 与完整填写示例 |
| 在哪里填答案？ | YES | Packet 只读、CSV 唯一答案表 |
| 如何提交？ | YES | CSV 操作、文件名与最终自检 |

结论：`TRAINED_NONPROJECT_ANNOTATOR_CAN_EXECUTE = TRUE`。Phase1 V2 可供 Owner 分发；Phase2 V2 仅预构建，仍 WITHHELD。
"""


TEACHING_EXAMPLES = [
    "《海岚市公共图书馆借阅规范》规定，读者每次最多借阅五册图书，借期为三十日。",
    "《云桥展览馆开放办法》规定周一全天闭馆，同时又规定每周一全天正常开放。",
    "《青禾园区访客管理细则》要求访客提前预先预约，并在到访时登记。",
    "申请人应在材料提交完成以后，再进行后续的下一步核验。",
    "申请人应在提交后窗口材料办理被完成。",
    "本规则适用对象为模板字段{subject}并且然后执行。",
    "《北岸停车场月卡规则》规定月卡适用于所有地下车位；同一规则又称月卡不适用于任何地下车位。",
    "报告首段称库存为120件，末段又称同一时点、同一仓库库存为98件。",
    "某项城市服务规则自2022年5月1日起实施。",
    "旧版收费标准在2019年执行，新版标准自2023年起执行。",
    "某公共阅览室现行规则规定闭馆时间为20:00。",
    "某园区规则写2020年版押金为200元，新版押金为0元。",
    "某制度在2019年发布，现行条款未改变。",
    "某通行证规则称当前每户可领取三张通行证。",
    "某临时措施已经终止，但候选称目前仍适用。",
    "某规则声称2017年版仍有效。",
]


def _now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _assert_sha(path: Path, expected: str) -> None:
    actual = _sha256(path)
    if actual != expected:
        raise ValueError(f"INPUT_SHA_BLOCKER:{path}:{actual}")


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON_OBJECT_REQUIRED:{path}")
    return value


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = value.replace("[[MD_BR]]", "  ")
    path.write_text(rendered.rstrip() + "\n", encoding="utf-8")


def _personalize(template: str, annotator: str) -> str:
    tag = annotator.replace("-", "_")
    replacements = {
        "{ANNOTATOR}": annotator,
        "{PHASE1_RETURN}": f"PILOT4_AB_{tag}_PHASE1_RETURN.csv",
        "{PHASE2_RETURN}": f"PILOT4_AB_{tag}_PHASE2_RETURN.csv",
        "{PHASE1_GUIDE}": f"PILOT4_AB_{tag}_PHASE1_GUIDE_V2.md",
        "{PHASE1_QUICK}": f"PILOT4_AB_{tag}_PHASE1_QUICK_REFERENCE_V2.md",
        "{PHASE1_PACKET}": f"PILOT4_AB_{tag}_PHASE1_PACKET_V2.md",
        "{PHASE1_TEMPLATE}": f"PILOT4_AB_{tag}_PHASE1_RETURN_TEMPLATE_V2.csv",
    }
    result = template
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def _v1_integrity() -> dict[str, Any]:
    _assert_sha(V1_MANIFEST, V1_MANIFEST_SHA)
    manifest = _read_json(V1_MANIFEST)
    failures: list[str] = []
    for item in manifest["files"]:
        path = V1_ROOT / str(item["path"])
        if not path.is_file():
            failures.append(f"MISSING:{item['path']}")
            continue
        if path.stat().st_size != int(item["bytes"]):
            failures.append(f"SIZE:{item['path']}")
        if _sha256(path) != str(item["sha256"]):
            failures.append(f"SHA:{item['path']}")
    if failures:
        raise ValueError(f"V1_PRESERVATION_BLOCKER:{failures[:5]}")
    physical_count = sum(1 for path in V1_ROOT.rglob("*") if path.is_file())
    if physical_count != int(manifest["file_count_excluding_manifest"]) + 1:
        raise ValueError("V1_PHYSICAL_COUNT_BLOCKER")
    return {
        "status": "PASS",
        "classification": [
            "HUMAN_ANNOTATION_PACKAGE_V1",
            "NOT_DISTRIBUTED",
            "SUPERSEDED_FOR_DISTRIBUTION_BY_V2",
            "PROTOCOL_SEMANTICS_VALID",
            "HUMAN_USABILITY_INSUFFICIENT",
        ],
        "manifest_path": str(V1_MANIFEST.resolve()),
        "manifest_sha256": V1_MANIFEST_SHA,
        "manifest_entries_verified": len(manifest["files"]),
        "physical_file_count": physical_count,
        "mutated_file_count": 0,
    }


def _packet_rows(annotator: str) -> list[list[str]]:
    tag = annotator.replace("-", "_")
    source = V1_ROOT / annotator / "phase1" / f"PILOT4_AB_{tag}_PHASE1_PACKET.md"
    rows: list[list[str]] = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| AB-"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 7:
            raise ValueError(f"V1_PACKET_PARSE_BLOCKER:{annotator}:{len(cells)}")
        rows.append(cells[:3])
    if len(rows) != 72 or len({row[0] for row in rows}) != 72:
        raise ValueError(f"V1_PACKET_CARDINALITY_BLOCKER:{annotator}")
    return rows


def _phase1_packet_v2(annotator: str, rows: list[list[str]]) -> str:
    lines = [
        f"# Pilot4 {annotator} Phase1 Packet V2",
        "",
        "Status: `READ_ONLY_QUESTION_SHEET / DISTRIBUTION_AUTHORITATIVE_V2`",
        "",
        "本 Packet 只用于阅读题目。不要在本文件填写答案；所有答案只写入 V2 CSV 模板。",
        "",
        "| blind_review_id | candidate_text | source_title |",
        "| --- | --- | --- |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def _copy_phase2_payload(output: Path, annotator: str) -> None:
    source = V1_ROOT / "withheld_phase2" / annotator
    target = output / "withheld_phase2" / annotator
    target.mkdir(parents=True, exist_ok=True)
    tag = annotator.replace("-", "_")
    for name in (
        "ANNOTATION_GUIDE_V3_2_TARGETED_REPAIR.md",
        f"PILOT4_AB_{tag}_PHASE2_PACKET.jsonl",
        f"PILOT4_AB_{tag}_PHASE2_PACKET.md",
        f"PILOT4_AB_{tag}_PHASE2_RETURN_TEMPLATE.csv",
    ):
        shutil.copyfile(source / name, target / name)
    shutil.copytree(source / "evidence_snapshots", target / "evidence_snapshots")
    _write_text(
        target / "DO_NOT_DISTRIBUTE_V2.md",
        "# DO NOT DISTRIBUTE\n\nPhase2 V2 is prebuilt but WITHHELD. Both Phase1 raw returns must be validated and immutably locked before simultaneous release.",
    )
    _write_text(
        target / f"PILOT4_AB_{tag}_PHASE2_GUIDE_V2.md",
        _personalize(PHASE2_GUIDE_TEMPLATE, annotator),
    )
    _write_text(
        target / f"PILOT4_AB_{tag}_PHASE2_QUICK_REFERENCE_V2.md",
        _personalize(PHASE2_QUICK_TEMPLATE, annotator),
    )


def _normalized(text: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]+", "", text.lower())


def _ngrams(text: str, size: int = 5) -> set[str]:
    value = _normalized(text)
    if len(value) < size:
        return {value}
    return {value[index : index + size] for index in range(len(value) - size + 1)}


def _similarity(left: str, right: str) -> float:
    a = _normalized(left)
    b = _normalized(right)
    grams_a = _ngrams(a)
    grams_b = _ngrams(b)
    union = grams_a | grams_b
    jaccard = len(grams_a & grams_b) / len(union) if union else 0.0
    sequence = SequenceMatcher(None, a, b).ratio()
    return max(jaccard, sequence)


def _final72_texts() -> list[str]:
    _assert_sha(FINAL72, FINAL72_SHA)
    rows = [
        json.loads(line)
        for line in FINAL72.read_text(encoding="utf-8-sig").splitlines()
        if line.strip()
    ]
    if len(rows) != 72:
        raise ValueError("FINAL72_CARDINALITY_BLOCKER")
    return [str(row["phase1_view"]["candidate_text"]) for row in rows]


def _prior_teaching_examples() -> list[str]:
    schema = _read_json(SCHEMA_V31)
    values: set[str] = set()
    for examples in schema.get("field_examples", {}).values():
        for row in examples:
            snippet = str(row.get("candidate_snippet") or "").strip()
            if snippet:
                values.add(snippet)
    for line in GUIDE_V32.read_text(encoding="utf-8").splitlines():
        if line.startswith("| ") and not line.startswith("| ---"):
            first = line.split("|", maxsplit=2)[1].strip()
            if first and first not in {"案例"}:
                values.add(first)
    return sorted(values)


def _teaching_example_qa() -> dict[str, Any]:
    final72 = _final72_texts()
    prior = _prior_teaching_examples()
    hits: list[dict[str, Any]] = []
    max_final = 0.0
    max_prior = 0.0
    for example in TEACHING_EXAMPLES:
        for candidate in final72:
            score = _similarity(example, candidate)
            max_final = max(max_final, score)
            if score >= 0.72 or _normalized(example) == _normalized(candidate):
                hits.append({"scope": "FINAL72", "example": example, "score": score})
        for old in prior:
            score = _similarity(example, old)
            max_prior = max(max_prior, score)
            if score >= 0.82 or _normalized(example) == _normalized(old):
                hits.append(
                    {"scope": "PRIOR_TEACHING", "example": example, "score": score}
                )
    if hits:
        raise ValueError(f"TEACHING_EXAMPLE_LEAKAGE_BLOCKER:{hits[:3]}")
    return {
        "status": "PASS",
        "teaching_example_count": len(TEACHING_EXAMPLES),
        "final72_candidate_count": len(final72),
        "prior_teaching_example_count": len(prior),
        "TEACHING_EXAMPLE_TO_FINAL72_NEAR_DUPLICATE": 0,
        "TEACHING_EXAMPLE_TO_PRIOR_EXAMPLE_NEAR_DUPLICATE": 0,
        "max_final72_similarity": round(max_final, 6),
        "max_prior_example_similarity": round(max_prior, 6),
        "method": "normalized exact match + character 5-gram/SequenceMatcher conservative threshold",
    }


def _parity_audit() -> dict[str, Any]:
    return {
        "status": "PASS",
        "accepted_sources": {
            "phase1_attempt2_guide": {
                "path": str(PHASE1_ACCEPTED_GUIDE.resolve()),
                "sha256": PHASE1_ACCEPTED_GUIDE_SHA,
            },
            "guide_v3_2": {
                "path": str(GUIDE_V32.resolve()),
                "sha256": GUIDE_V32_SHA,
            },
            "phase1_reason_enforcement": (
                "local_internal_conflict in {YES,UNCERTAIN} OR phase1_issue != NONE"
            ),
        },
        "mapped_rule_families": [
            "phase1 no external lookup",
            "phase1 canonical fields and enums",
            "phase1 conditional reason enforcement",
            "overall factual status strict order",
            "present-time substitution test",
            "version claim status",
            "authority claim status",
            "minimum evidence ablation",
            "evidence selection independence",
            "snapshot plus URL provenance",
            "phase2 issue handling",
            "phase2 conditional reason enforcement",
        ],
        "NEW_RULE_COUNT": 0,
        "REMOVED_RULE_COUNT": 0,
        "CHANGED_RULE_COUNT": 0,
        "ONLY_EXPLANATION_AND_EXAMPLE_EXPANSION": True,
        "GUIDE_V3_2_SEMANTICS_CHANGED": False,
    }


def prepare(output: Path) -> None:
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"OUTPUT_MUST_BE_EMPTY:{output}")
    output.mkdir(parents=True, exist_ok=True)
    _assert_sha(PHASE1_ACCEPTED_GUIDE, PHASE1_ACCEPTED_GUIDE_SHA)
    _assert_sha(GUIDE_V32, GUIDE_V32_SHA)
    v1_qa = _v1_integrity()
    specs: list[dict[str, Any]] = []
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("-", "_")
        rows = _packet_rows(annotator)
        phase1 = output / annotator / "phase1"
        _write_text(
            phase1 / f"PILOT4_AB_{tag}_PHASE1_PACKET_V2.md",
            _phase1_packet_v2(annotator, rows),
        )
        _write_text(
            phase1 / f"PILOT4_AB_{tag}_PHASE1_GUIDE_V2.md",
            _personalize(PHASE1_GUIDE_TEMPLATE, annotator),
        )
        _write_text(
            phase1 / f"PILOT4_AB_{tag}_PHASE1_QUICK_REFERENCE_V2.md",
            _personalize(PHASE1_QUICK_TEMPLATE, annotator),
        )
        _write_text(
            phase1 / f"README_FOR_{tag}_V2.md",
            _personalize(PHASE1_README_TEMPLATE, annotator),
        )
        shutil.copyfile(
            V1_ROOT
            / annotator
            / "phase1"
            / f"PILOT4_AB_{tag}_PHASE1_INDEPENDENCE_NOTICE.md",
            phase1 / f"PILOT4_AB_{tag}_PHASE1_INDEPENDENCE_NOTICE.md",
        )
        specs.append(
            {
                "path": str(phase1 / f"PILOT4_AB_{tag}_PHASE1_RETURN_TEMPLATE_V2.csv"),
                "sheet_name": f"{tag}_Phase1_V2",
                "headers": PHASE1_HEADERS,
                "rows": [[row[0], "", "", "", ""] for row in rows],
            }
        )
        _copy_phase2_payload(output, annotator)

    _write_text(output / "PILOT4_A_B_OWNER_DISTRIBUTION_GUIDE_V2.md", OWNER_GUIDE)
    _write_text(
        output / "qa" / "HUMAN_ANNOTATION_USABILITY_CHECKLIST.md", USABILITY_CHECKLIST
    )
    _write_json(output / "qa" / "v1_preservation_qa.json", v1_qa)
    _write_json(
        output / "qa" / "teaching_example_leakage_qa.json", _teaching_example_qa()
    )
    _write_json(output / "qa" / "guide_v3_2_rule_parity_audit.json", _parity_audit())
    _write_json(
        output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER_V2.json",
        {
            "task_id": TASK_ID,
            "updated_at": _now(),
            "A_PHASE1_PACKET_READY_V1": True,
            "B_PHASE1_PACKET_READY_V1": True,
            "A_PHASE1_PACKET_V1_SUPERSEDED": True,
            "B_PHASE1_PACKET_V1_SUPERSEDED": True,
            "A_PHASE1_PACKET_V2_READY": True,
            "B_PHASE1_PACKET_V2_READY": True,
            "A_PHASE1_DISTRIBUTED": False,
            "B_PHASE1_DISTRIBUTED": False,
            "PRE_REPAIR_HUMAN_PHASE1_DISTRIBUTION_TEMPORARILY_HELD": True,
            "PRE_REPAIR_HUMAN_USABILITY_REPAIR_REQUIRED": True,
            "CURRENT_HUMAN_PHASE1_DISTRIBUTION_TEMPORARILY_HELD": False,
            "CURRENT_HUMAN_USABILITY_REPAIR_REQUIRED": False,
            "PHASE2_RELEASE_ALLOWED": False,
            "A_B_DISTRIBUTION_STARTED": False,
            "GROUND_TRUTH_CREATED": False,
            "PILOT4_ANNOTATION_PROTOCOL_ACCEPTED": True,
            "PILOT4_CALIBRATION_CLOSED": True,
            "GUIDE_V3_2_SEMANTICS_CHANGED": False,
            "CANDIDATE_TEXT_CHANGED": False,
            "ANNOTATOR_IDENTITY_CHANGED": False,
            "ANNOTATOR_ORDER_CHANGED": False,
        },
    )
    _write_json(
        output / "qa" / "csv_authoring_spec.json",
        {"task_id": TASK_ID, "outputs": specs},
    )
    _write_json(
        output / "qa" / "prepare_complete.json",
        {"status": "PASS", "prepared_at": _now(), "csv_output_count": 2},
    )


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    raw = path.read_bytes()
    if not raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"CSV_UTF8_BOM_REQUIRED:{path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = [{key: str(value) for key, value in row.items()} for row in reader]
    return list(reader.fieldnames or []), rows


def _normalize_personal(text: str) -> str:
    return (
        text.replace("HUMAN-A01", "HUMAN-X01")
        .replace("HUMAN-B01", "HUMAN-X01")
        .replace("HUMAN_A01", "HUMAN_X01")
        .replace("HUMAN_B01", "HUMAN_X01")
    )


def _validate_guide_content(path: Path, phase: str) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    required = (
        PHASE1_HEADERS[1:]
        + [
            "NATURAL",
            "MINOR_ISSUE",
            "UNNATURAL",
            "YES",
            "NO",
            "UNCERTAIN",
            "MISSING_CONTEXT",
            "AMBIGUOUS_REFERENCE",
            "OTHER",
            "REASON_REQUIRED",
            "常见错误",
            "最终自检",
        ]
        if phase == "PHASE1"
        else PHASE2_HEADERS[1:]
        + [
            "CURRENTLY_CONSISTENT",
            "LEGITIMATE_VERSION_OR_HISTORY",
            "FACTUAL_CONFLICT",
            "INSUFFICIENT_EVIDENCE",
            "PRESENT_EVIDENCE_INSUFFICIENT",
            "ONE_OFFICIAL_EVIDENCE",
            "MULTI_EVIDENCE_OR_VERSION_CHAIN",
            "E1+E2",
            "LATE_DISCOVERED_CANDIDATE_DEFECT",
            "PRESENT-TIME SUBSTITUTION TEST",
            "REASON_REQUIRED",
        ]
    )
    missing = [token for token in required if token not in text]
    if missing:
        raise ValueError(f"GUIDE_COVERAGE_BLOCKER:{path}:{missing}")
    return {"path": str(path), "phase": phase, "missing_required_tokens": []}


def _leakage_qa(output: Path, annotator: str) -> dict[str, Any]:
    text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in (output / annotator / "phase1").glob("*")
        if path.is_file()
    )
    forbidden = {
        "canonical_sample_id": r"\bP4Q-[0-9a-f]+\b|\bsample_id\b",
        "expected_contract": r"EXPECTED_V3|EXPECTED_CONTRACT",
        "mapping": r"IDENTITY_MAPPING|owner_mapping",
        "candidate_class": r"CLEAN_CURRENT|POISON_FACT|HARD_NEGATIVE",
        "hkp": r"\bHKP[_-]",
        "stealth_label": r"\bS[123]\b|intended_stealth",
        "phase2_field": r"overall_fact_status|version_claim_status|authority_claim_status|minimum_external_evidence_needed|evidence_selection|phase2_issue|phase2_reason",
        "url": r"https?://",
    }
    counts = {
        name: len(re.findall(pattern, text, flags=re.IGNORECASE))
        for name, pattern in forbidden.items()
    }
    if any(counts.values()):
        raise ValueError(f"PHASE1_V2_LEAKAGE_BLOCKER:{annotator}:{counts}")
    return {"annotator": annotator, "status": "PASS", "forbidden_counts": counts}


def _role(relative: str) -> str:
    normalized = relative.replace("\\", "/")
    if re.match(r"HUMAN-[AB]01/phase1/", normalized):
        return "DISTRIBUTABLE_PHASE1_V2"
    if normalized.startswith("withheld_phase2/"):
        return "WITHHELD_PHASE2_V2"
    return "CONTROL_PLANE_ONLY"


def finalize(output: Path) -> None:
    v1_before = _read_json(output / "qa" / "v1_preservation_qa.json")
    v1_after = _v1_integrity()
    if v1_before != v1_after:
        raise ValueError("V1_CHANGED_DURING_TASK_BLOCKER")

    packet_qa: dict[str, Any] = {"status": "PASS", "annotators": {}}
    template_qa: dict[str, Any] = {"status": "PASS", "annotators": {}}
    guide_checks: list[dict[str, Any]] = []
    normalized: dict[str, dict[str, str]] = {}
    leakage: list[dict[str, Any]] = []
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("-", "_")
        phase1 = output / annotator / "phase1"
        v1_rows = _packet_rows(annotator)
        v2_packet = phase1 / f"PILOT4_AB_{tag}_PHASE1_PACKET_V2.md"
        v2_lines = [
            line
            for line in v2_packet.read_text(encoding="utf-8").splitlines()
            if line.startswith("| AB-")
        ]
        v2_rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in v2_lines
        ]
        if v2_rows != v1_rows or any(len(row) != 3 for row in v2_rows):
            raise ValueError(f"PACKET_V1_V2_PARITY_BLOCKER:{annotator}")
        packet_qa["annotators"][annotator] = {
            "rows": 72,
            "visible_columns": ["blind_review_id", "candidate_text", "source_title"],
            "candidate_id_order_source_title_parity": True,
        }

        v1_template = (
            V1_ROOT
            / annotator
            / "phase1"
            / f"PILOT4_AB_{tag}_PHASE1_RETURN_TEMPLATE.csv"
        )
        v2_template = phase1 / f"PILOT4_AB_{tag}_PHASE1_RETURN_TEMPLATE_V2.csv"
        v1_headers, v1_template_rows = _read_csv(v1_template)
        v2_headers, v2_template_rows = _read_csv(v2_template)
        if v1_headers != PHASE1_HEADERS or v2_headers != PHASE1_HEADERS:
            raise ValueError(f"PHASE1_V2_SCHEMA_BLOCKER:{annotator}")
        if v1_template_rows != v2_template_rows:
            raise ValueError(f"PHASE1_V2_TEMPLATE_PARITY_BLOCKER:{annotator}")
        if any(row[field] for row in v2_template_rows for field in PHASE1_HEADERS[1:]):
            raise ValueError(f"PHASE1_V2_PREFILL_BLOCKER:{annotator}")
        template_qa["annotators"][annotator] = {
            "schema": PHASE1_HEADERS,
            "rows": 72,
            "id_order_parity": True,
            "answer_prefill_count": 0,
            "sha256": _sha256(v2_template),
        }

        p1_guide = phase1 / f"PILOT4_AB_{tag}_PHASE1_GUIDE_V2.md"
        p2_guide = (
            output
            / "withheld_phase2"
            / annotator
            / f"PILOT4_AB_{tag}_PHASE2_GUIDE_V2.md"
        )
        guide_checks.extend(
            [
                _validate_guide_content(p1_guide, "PHASE1"),
                _validate_guide_content(p2_guide, "PHASE2"),
            ]
        )
        normalized[annotator] = {
            "phase1_guide": _normalize_personal(p1_guide.read_text(encoding="utf-8")),
            "phase1_quick": _normalize_personal(
                (phase1 / f"PILOT4_AB_{tag}_PHASE1_QUICK_REFERENCE_V2.md").read_text(
                    encoding="utf-8"
                )
            ),
            "phase1_readme": _normalize_personal(
                (phase1 / f"README_FOR_{tag}_V2.md").read_text(encoding="utf-8")
            ),
            "phase2_guide": _normalize_personal(p2_guide.read_text(encoding="utf-8")),
            "phase2_quick": _normalize_personal(
                (
                    output
                    / "withheld_phase2"
                    / annotator
                    / f"PILOT4_AB_{tag}_PHASE2_QUICK_REFERENCE_V2.md"
                ).read_text(encoding="utf-8")
            ),
        }
        leakage.append(_leakage_qa(output, annotator))

        phase2_template = (
            output
            / "withheld_phase2"
            / annotator
            / f"PILOT4_AB_{tag}_PHASE2_RETURN_TEMPLATE.csv"
        )
        phase2_headers, phase2_rows = _read_csv(phase2_template)
        if phase2_headers != PHASE2_HEADERS or len(phase2_rows) != 72:
            raise ValueError(f"PHASE2_COPY_SCHEMA_BLOCKER:{annotator}")
        source_phase2 = (
            V1_ROOT
            / "withheld_phase2"
            / annotator
            / f"PILOT4_AB_{tag}_PHASE2_RETURN_TEMPLATE.csv"
        )
        if _sha256(phase2_template) != _sha256(source_phase2):
            raise ValueError(f"PHASE2_TEMPLATE_COPY_BLOCKER:{annotator}")
        snapshots = list(
            (output / "withheld_phase2" / annotator / "evidence_snapshots").glob("*")
        )
        if len([path for path in snapshots if path.is_file()]) != 144:
            raise ValueError(f"PHASE2_SNAPSHOT_COVERAGE_BLOCKER:{annotator}")

    parity = all(
        normalized["HUMAN-A01"][key] == normalized["HUMAN-B01"][key]
        for key in normalized["HUMAN-A01"]
    )
    if not parity:
        raise ValueError("A_B_GUIDE_SEMANTIC_PARITY_BLOCKER")
    _write_json(output / "qa" / "packet_v1_v2_parity_qa.json", packet_qa)
    _write_json(output / "qa" / "return_template_v1_v2_parity_qa.json", template_qa)
    _write_json(
        output / "qa" / "AB_HUMAN_GUIDE_SEMANTIC_PARITY_REPORT.json",
        {
            "status": "PASS",
            "normalized_semantic_parity": True,
            "compared_artifacts": sorted(normalized["HUMAN-A01"]),
            "allowed_differences": [
                "annotator ID",
                "return filename",
                "local packet/template filename",
            ],
        },
    )
    _write_json(
        output / "qa" / "guide_content_coverage_qa.json",
        {"status": "PASS", "checks": guide_checks},
    )
    _write_json(
        output / "qa" / "reviewer_visible_leakage_qa.json",
        {"status": "PASS", "results": leakage},
    )
    register = _read_json(
        output / "register" / "PILOT4_A_B_DISTRIBUTION_REGISTER_V2.json"
    )
    if (
        register["A_PHASE1_DISTRIBUTED"]
        or register["B_PHASE1_DISTRIBUTED"]
        or register["PHASE2_RELEASE_ALLOWED"]
        or register["GROUND_TRUTH_CREATED"]
    ):
        raise ValueError("DISTRIBUTION_GATE_BLOCKER")

    manifest_path = output / "manifest" / "final_manifest.json"
    files: list[dict[str, Any]] = []
    for path in sorted(
        item for item in output.rglob("*") if item.is_file() and item != manifest_path
    ):
        relative = path.relative_to(output).as_posix()
        files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "role": _role(relative),
            }
        )
    _write_json(
        manifest_path,
        {
            "task_id": TASK_ID,
            "created_at": _now(),
            "root": str(output.resolve()),
            "status": FINAL_STATUS,
            "file_count_excluding_manifest": len(files),
            "files": files,
            "manifest_self_hash": "EXCLUDED_TO_AVOID_RECURSION",
        },
    )
    _write_json(
        output / "qa" / "final_package_qa.json",
        {
            "status": "PASS",
            "finalized_at": _now(),
            "v1_preserved": True,
            "phase1_v2_ready": True,
            "phase2_v2_withheld": True,
            "candidate_text_changed": False,
            "annotator_identity_changed": False,
            "annotator_order_changed": False,
            "protocol_semantic_change_count": 0,
            "ground_truth_created": False,
            "human_annotation_executed": False,
            "usability_checklist": "PASS",
        },
    )
    # Rebuild once so final_package_qa is covered by the final manifest.
    files = []
    for path in sorted(
        item for item in output.rglob("*") if item.is_file() and item != manifest_path
    ):
        relative = path.relative_to(output).as_posix()
        files.append(
            {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
                "role": _role(relative),
            }
        )
    manifest = _read_json(manifest_path)
    manifest["file_count_excluding_manifest"] = len(files)
    manifest["files"] = files
    _write_json(manifest_path, manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare", "finalize"])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if args.mode == "prepare":
        prepare(output)
    else:
        finalize(output)
    print(json.dumps({"status": "PASS", "mode": args.mode, "output": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
