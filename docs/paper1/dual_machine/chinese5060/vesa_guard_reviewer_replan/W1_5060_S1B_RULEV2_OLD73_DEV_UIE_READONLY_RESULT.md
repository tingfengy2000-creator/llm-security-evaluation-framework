# 5060｜Owner18 Rule-V2 旧73开发与 UIE 只读审计

2026-11-09 JST · `RULE_V2_DEV_COMPLETED / S1B_INDEPENDENT_TEST_NOT_RUN / MODEL_ASSET_NOT_AUTHORIZED / S2_S5_LOCKED / AUTO_CONTINUE=NO`。工作仅覆盖 [Owner18](../../owner_approvals/W1_5060_S1B_RULEV2_DEV_AND_UIE_READONLY_AUTH_20261108.md) 的旧73开发和 UIE 官方材料只读核验。

## Rule-V2 实做与对照

原 S1 Run `W1-5060-S1-CHINESE-EXTRACTION-20261108-01`、`S1_FAIL_STOP`、源提交 `68d34a5d877206f4e6d7d9e2bdda16784145a76a`、R2 K1-C 和历史结果保留。使用原封存预测、标注和评分器复算 73/73，逐行重算结果与历史一致。三轮均复用全部 73 条暴露样本（61 个语义案例和 12 条额外显式视图），没有改标、筛样或把配对当独立事实。数据类别为 `DEVELOPMENT_REUSE / NOT_INDEPENDENT / NOT_HUMAN_GOLD`。

新模块输入为 query、原始正文和公共 schema，逐子句记录主体、属性、数值/单位、版本、日期、条件和作用域。保留候选、被拒原因、原文字符和 UTF-8 字节半开区间。独立保留全角数字及中文单位的原文定位。显式版本和时间需文本内匹配，未证修订、冲突、缺乏同范围支持时拒识。候选始终标 `UNVERIFIED_TEXT_ONLY`。只借鉴 UIE 的 schema/span 接口和 X-MADAM-RAG 的确定性候选分组思想。当前范围限可验证的标量与词面跨度，未测开放实体关系、长篇多文档或证据防御收益。P0 的可信来源约束照旧，M1/M2/M3 未运行。 [ACL UIE](https://aclanthology.org/2022.acl-long.395/) · [X-MADAM-RAG §4.2](https://arxiv.org/html/2606.12903v1#S4.SS2)

| 完整评分／原分母 | 封存 Rule-V1 | V2 01 | V2 02 | V2 03（最终） |
| --- | ---: | ---: | ---: | ---: |
| 完整正确 / 错误 / UNKNOWN（73） | 30 / 4 / 39 | 57 / 2 / 14 | 58 / 2 / 13 | 58 / 1 / 14 |
| 答案值命中 / 有答案 | 31/61 | 58/61 | 60/61 | 59/61 |
| 错抽 / 已决定 | 4/34 | 2/59 | 2/60 | 1/59 |
| 覆盖 / 拒识（73） | 34 / 39 | 59 / 14 | 60 / 13 | 59 / 14 |
| 应拒识中的误答（12） | 2 | 0 | 0 | 0 |

最终错抽占全部 1/73。值命中 96.72%（Wilson 95% 区间 88.81%–99.10%），决定后错抽 1.69%（0.30%–9.00%）。配对观测相关，区间仅是原逐条计数的描述。自然视图 46 正确、1 错误、14 UNKNOWN（61），显式视图 12/12 完整正确，12 个自然化／显式配对两边均正确。原版仅 5/12 配对两边正确。当前无 scope 字段错判，1 条 span 错误计入完整评分。全量类别、严格 scope/span、Wilson 和配对计数见[脱敏清单](W1_5060_S1B_RULEV2_OLD73_DEV_MANIFEST.json)。

历史 29 条有答案但 UNKNOWN 中，query 主体／属性未识别 13→13 正确，未抽到标量 9→8 正确和 1 UNKNOWN，多事实歧义 6→5 正确和 1 span 错误，scope 未匹配 1→1 正确。历史 4 条错误中 1 条转正确、3 条转 UNKNOWN，后者包含未证修订和跨群体两条应拒识误答。另有 1 条历史 UNKNOWN 变为 span 错误。

- 01 新增一条旧值误取，并保留一条适用对象漏绑定。02 识别同句明确替换、量词后对象，并保守处理角色作用域，旧值错误变为 span 错误。03 补上无“的”连接的角色限定，原对象错配变为 UNKNOWN。03 为保守收口，值命中较 02 降 1 条。
- 最终错误来自同一句重复的相同现值。算法定位到首次明确改值处，冻结标注要求覆盖后续重申的引文位置，按原规则计错。两条有答案 UNKNOWN 分别涉及宽泛天气问法对较窄生效条件，以及材料未明示的一般人群与例外界线。继续保留这三项失败，未调整标注或评分。
- 旧73 经过开发迭代，超过历史门槛的点估计不构成 S1-B 验收。独立验证 `NOT_RUN`，Human Gold 0，正式 ASR、Accuracy `NOT_MEASURED`。

## UIE 官方材料与 Windows CPU 依赖

固定 PaddleNLP `v2.6.1@fd2bed541ff929f6f8b350001694e553b29d4e9a` 的源码与 LICENSE 经官方 raw 只读复核，代码 Apache‑2.0。Taskflow 指向下列 BOS 资源，2026-11-09 JST HEAD 均 HTTP 200，总计 71,847,290 B。权重 ETag `-cfa770590d660cf244c5fa110ce512aa` 与加载器 MD5 不同。响应未提供可冻结的对象版本 ID 或 SHA256，独立权重／分词器使用条款、不可变发布标识、发布者 SHA256 均为 `UNKNOWN`。官方仓公开讨论无维护者答复，未联系第三方。 [源码](https://raw.githubusercontent.com/PaddlePaddle/PaddleNLP/fd2bed541ff929f6f8b350001694e553b29d4e9a/paddlenlp/taskflow/information_extraction.py) · [代码许可](https://raw.githubusercontent.com/PaddlePaddle/PaddleNLP/fd2bed541ff929f6f8b350001694e553b29d4e9a/LICENSE) · [讨论 #11252](https://github.com/PaddlePaddle/PaddleNLP/discussions/11252)

| 官方 BOS 相对路径 | HEAD 字节 | 固定源码 MD5 |
| --- | ---: | --- |
| `uie_nano_v1.1/model_state.pdparams` | 71,659,589 | `48db5206232e89ef16b66467562d90e5` |
| `uie_nano/config.json` | 610 | `e0e0a2c0d9651ed1a8492be5507590a9` |
| `uie_base/vocab.txt` | 186,807 | `1c1c1f4fd93c5bed3b4eebec4de976a8` |
| `uie_base/special_tokens_map.json` | 112 | `8b3fb1023167bb4ab9d70708eb05f6ec` |
| `uie_base/tokenizer_config.json` | 172 | `59acb0ce78e79180a2491dfd8382b28c` |

PyPI 有 PaddlePaddle CPU 2.6.2 的 Windows x64 CPython 3.12 wheel（81,105,769 B，发行 SHA256 `f90efb319603883ded4210c72f2415ccd9d0b4290ad78d6cf0a2fc67c84661b0`）和 PaddleNLP 2.6.1 的通用 wheel（2,682,308 B，`75f5c6f805be4f7bcf9a8c58164dae278d1f2511e433d7732f4571a37178d816`）。Paddle 在 Windows 要求 Protobuf 3.1.0–3.20.2，PaddleNLP 要求恰好 3.20.2，并有未锁定的 ONNX、paddle2onnx、datasets、HF Hub 等依赖。现有 Python 3.12.14、NumPy 2.5.0、Protobuf 7.35.1，Paddle/ONNX 未装。**现有环境有明确 Protobuf 冲突**。Paddle 元数据仅声明 NumPy ≥1.13，不能据此核准 NumPy 2.x ABI。完整传递依赖与散列锁 `UNKNOWN`。NumPy 1.26.4 有 Windows cp312 发行文件，仅记录静态线索。 [PaddlePaddle 元数据](https://pypi.org/pypi/paddlepaddle/2.6.2/json) · [PaddleNLP 元数据](https://pypi.org/pypi/paddlenlp/2.6.1/json) · [NumPy 元数据](https://pypi.org/pypi/numpy/1.26.4/json)

本次只读取得官方源码、许可证、HTTP 头和包元数据。权重、分词器文件、wheel 获取为 0，安装、加载、推理、模型 API 与新增费用均为 0。D/E 前置可用约 333/337 GiB；测试临时目录和私有证据在 D 盘。下一次只在发布者给出覆盖五项具体资产的许可、发行 ID/强哈希和 Windows CPU 完整依赖锁后，提交单模型资产审批。离线模型开发推理与独立验证仍各需后续 Owner 决定。

## 封存与治理

三个私有开发目录使用下表 Run ID 命名。评分前封存预测，预测器只打开旧输入白名单，不读标注，评分器验证全部旧资产并在归档后再校验。每轮 73/73 确定性回放，两个独立进程各执行一次，预测与评分退出码均为 0。

| Run ID | 冻结执行 Git SHA | 私有 ZIP SHA256 |
| --- | --- | --- |
| `W1-5060-S1B-RULEV2-DEV-20261109-01` | `a46175fe329953b848e9eea6aab1f5bccafe8168` | `fd35974487a6154a6d6acf5b95f461ee06fb760a00e58e88027c080aa79dd1b6` |
| `W1-5060-S1B-RULEV2-DEV-20261109-02` | `00b274c60dd4b2afcaa9b105aa45b374028e9319` | `f0958f67f3bb1ebbe35e328fdb4849efee15dd055a0c5233f39143edc4e3ebcb` |
| `W1-5060-S1B-RULEV2-DEV-20261109-03` | `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f` | `894e6032ecd4ba136c708a6834122a358670e9ca02de52065f7d99ed08348270` |

最终配置 SHA256 `4352bbcc97ccc5b42861611d1f6a952718af7f195acf02c6c2507f3269232b38`，私有 Run Manifest SHA256 `c8e6258e73cd6076e1ea25b3cdd35c0c68167d5e44122c1725da260f359d09ee`，逐条结果只留 D 盘。使用既有 Python 以 `-B` 分别执行 `scripts/research/run_chinese5060_s1b_rule_v2.py predict` 和 `evaluate`。QA 私有 ZIP 含 33 个日志与退出码，SHA256 `fb3f943e73d8aae96f90e1db76a71c1951d53c6e1325a726b8c84762a5dfaa69`。首次单测因“个工作日”失败，早期 MyPy 报两处类型问题，均保留。最终 pytest 23 通过、Ruff 和 MyPy 通过。

FORWARD_RISK_REVIEW 与 PAPER_RISK_REVIEW 记录。只在核对并快进的 5060 独立发布检出执行，原工作树保持原状态。历史 S1 代码／证据、B2/R2、旧108、冻结 D1、D2/D3 和 5090 均未改动。未打开新独立数据。发展集收益只用于抽取开发归因，P0 可信来源及正式对照的科学结论仍待证。

收口更新 Current Work State、Project Master、Experiment Master、Execution Log、Week 1 Tracker、Human／Agent Ledger。Owner Register 无新决定，Stage Process 无阶段切换或新门，Canonical Lessons 无可提升的验收经验，Research Plan Authority 与 README 无合同或导航变更。发布仅限当前分支，当前 Git 同步状态由实际 Git 校验。

### DOCUMENTATION_CLOSEOUT_CHECKLIST

```text
human_ledger_checked=true
human_ledger_updated_if_required=true
agent_ledger_checked=true
agent_ledger_updated=true
current_work_state_updated=true
execution_log_appended=true
experiment_master_condition_evaluated=true
owner_decision_condition_evaluated=true
stage_process_condition_evaluated=true
lessons_condition_evaluated=true
research_authority_condition_evaluated=true
README_condition_evaluated=true
cross_document_current_task_consistent=true
cross_document_status_consistent=true
cross_document_next_action_consistent=true
cross_document_blocker_consistent=true
markdown_links_valid=true
```
