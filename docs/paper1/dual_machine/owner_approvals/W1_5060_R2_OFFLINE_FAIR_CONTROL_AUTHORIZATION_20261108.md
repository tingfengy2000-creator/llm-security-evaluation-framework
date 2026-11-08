# W1-OD-20261108-5060-R2-OFFLINE-15｜R2 网页模板覆盖诊断与 RD-zh 四臂离线公平对照授权

**Date:** 2026-11-08 JST  
**Status:** `OWNER_EXPLICITLY_APPROVED / BOUNDED_OFFLINE_R2_EXECUTION`  
**Branch:** `research/paper1-chinese-defense-5060`  
**Authorization anchor:** Owner 当前监督会话明确要求继续上一段研究，按最新 R2 方向推进“网页模板覆盖诊断及 RD-zh 四臂公平对照”，并明确不得扩大为商业 API、5090 Claim、D2/D3 或正式测试许可。  
**Pre-registration:** `REVIEWER_R2_S0_CHECKPOINT_TEMPLATE_TFIDF_ROUTE_20261106.md`  
**S0 run:** `W1-5060-REVIEWER-REPLAN-S0-20261106-01`  
**Pre-authorization remote HEAD verified by control plane:** `533a6efed519f9251f4b4848306e232c9710a497`.

## PO-MHEP 十二字段

1. **Issue ID**  
   `W1-OD-20261108-5060-R2-OFFLINE-15`.

2. **Issue name**  
   解除 S0 硬检查点中与 R2 直接相关的受限离线执行门：先完成冻结 D1 TopK 的网页模板覆盖只读诊断，再完成预注册的 Stage1 词面 2×2 四臂公平对照。

3. **Discovery stage/task**  
   5060 Week 1，外部评审 R2 后、S0 已完成且 S1–S4 尚未运行的检查点。前置状态为 `S0_COMPLETE / OWNER_CHECKPOINT_PENDING`，R1-10(A) 本地固定 encoder / RD-zh 真实 D1 对照待 Owner 决定。

4. **Current facts**  
   - `OBSERVED_FACT`: 冻结 Pilot12 为 12 事实组、36 世界、TopK5 共 180 片段；历史 B2 删除 81/180，已召回候选 Poison 2/10、Clean 4/10、HN 2/9；真实 D1 RD-zh 未运行；商业 API 本阶段调用 0；Human Gold 0；正式 ASR/QA 未测。  
   - `OBSERVED_FACT`: S0 已确认 B2 Stage2 使用修复后索引与余弦/L2 归一；RD-zh char2 适配器仅完成静态测试。  
   - `SOURCE_DERIVED_FACT`: R2 评审指出上游证据存在网页导航/下载模板混杂，但约 100/189 不等于冻结 TopK180 的真实覆盖率。  
   - `INFERENCE`: 在解释 RD 的中文迁移误删前，应先控制“中文分词”和“网页模板”两个词面混杂，并保持其余变量冻结。  
   - `UNKNOWN`: D1 TopK180 的实际模板覆盖、四臂结果及 K1 最终路线在本授权前均未知。

5. **Affected existing constraints**  
   保留 2026-11-04 双机冻结合同、D1_DEV_EXPOSED、历史实验不可变、标签隔离、D2/D3 完全隔离、5090 独立线、HumanGold=0、正式指标不可宣称、S5 新 Owner 授权门、主分支不得擅自合并。仅 supersede “S0_CHECKPOINT_RELEASE 与 R1-10(A) 待定”中本文件明确列出的离线部分；R1-10(B) 不变。

6. **Why this must be handled now**  
   R2 已将网页模板确定为第三个潜在混杂；若不先做覆盖诊断与正交对照，无法判断 B2 Clean 误删来自原方法、中文分词迁移还是网页模板，从而会污染后续方法贡献与公平性结论。

7. **Downstream risks**  
   - 工程：误改原 TopK/embedding/Stage2 会破坏单变量对照。  
   - 实验：先看角色/效果再挑模板规则会形成标签泄漏与后验调参。  
   - 论文：把分词/清洗收益写成 VESA 创新会造成 novelty/fairness 风险。  
   - 复现：未固定 lexical mask、encoder revision、tie 规则和 role-free seal 会失去可重放性。  
   - 资源/安全：任何下载、在线 API、D2/D3 或跨机 Claim 都超出当前授权。

8. **Approved option / action, advantages, disadvantages, cost, risk, later-stage and paper impact, reversibility**  
   **批准方案 A：R2 bounded offline fair-control。**  
   先执行 `S0-TEMPLATE-COVERAGE_READONLY`；随后在原 36 世界/180 TopK 上运行四臂：`B2_RAW`、`RD_ZH_ONLY`、`RD_TEMPLATE_ONLY`、`RD_ZH_TEMPLATE`。模板蒙版只影响 Stage1 TF-IDF 的 `lexical_view`；原 TopK、chunk 原文、embedding/Stage2 输入、生成上下文均不得改写。允许使用本地已经缓存且 revision 与历史 B2 一致的固定 encoder；若身份/缓存缺失或需下载/替代模型，立即 STOP。  
   优点：最小代价关闭 R2 混杂，能为 K1 预注册路线提供直接证据。缺点：样本仅 36 世界，仍是开发诊断，不能形成正式统计结论。新增商业费用为 0；预期资源为本地 CPU/GPU/已有缓存。风险可通过 role-blind 预注册、封存后独立 reveal 和不可变原输入降低。全部改动为新增代码/派生结果，可逆且不改历史证据。

9. **LOCAL recommendation**  
   执行方案 A，并严格以 R2 文档的 2×2 定义为唯一四臂语义。先 role-blind 封存模板规则、span mask、四臂输出与 Run Manifest，再由独立 Evaluator 只读揭盲汇总 Poison/Clean/HN；随后按已预注册 K1-A/B/C 只做路线判定并 STOP 返回 Owner。

10. **Rationale and confidence**  
    该授权直接对应 Owner 本轮明确指令，并且是 R2 评审要求的最小公平性实验。对“允许执行此离线任务”的判断置信度高；对模板是否解释误删、RD-zh 是否改善以及 K1 分支结果均不预判。

11. **Explicit Owner decision resolved by this record**  
    - `S0_CHECKPOINT_RELEASE = YES`，**仅限本授权 R2 bounded offline task**。  
    - `R1-10(A) = APPROVED`，仅允许历史 B2 固定 revision 的本地已缓存 encoder/既有 embedding 身份用于 36 世界四臂离线过滤；0 下载、0 外部 API、0 新检索。  
    - `R1-10(B) = NOT_DECIDED`；S3 独立构造/保管方仍未指定。  
    - S1、S2、S3、S4、S5 均未因本授权自动放行。

12. **Allowed and prohibited work after this decision**  
    **允许：**  
    - 只读核验最新 Git/AGENTS/PO-MHEP/冻结 S0 证据；  
    - 在冻结 TopK180 上做 role-blind 网页模板覆盖统计；  
    - 固定高精度 `WEB_CHROME_CONFIDENT / AMBIGUOUS / NONE` 规则与 span mask；模糊项不清洗；  
    - 执行四臂离线 Stage1/Stage2 公平对照，固定 `single_hop=true,p=2,m=5,K=5`、历史 B2 encoder revision、聚类、Stage2、tie 规则；  
    - 使用已有本地缓存，不下载；生成脱敏汇总、私有 role-free 证据、Run Manifest、源码/测试与治理记录；  
    - 角色盲结果封存后，由独立 Evaluator 只读揭盲统计候选 Poison/Clean/HN，并按 R2 K1-A/B/C 规则给出路线判定。  
    **禁止：**  
    - 商业/免费在线生成 API、在线 verifier、联网检索、模型/依赖下载或替代 encoder；  
    - 修改原 TopK、原检索索引、历史 B1/B2、生成上下文、D1 问法/样本/标签/答案；  
    - 用角色/target/Gold/旧生成效果选择模板规则、mask 或参数；  
    - S1–S5 自动继续，特别是 S3 留出、S4 一次性验证与 S5 Qwen；  
    - 5090 Claim1–3、Llama 新下载、D2/D3 读取/编辑、正式测试、主研究分支合并或跨分支 cherry-pick；  
    - 将清洗/分词收益宣称为 VESA 创新，或宣称正式 ASR/Answer Accuracy/Human Gold。

## Required stop conditions

任一条件触发即 `HUMAN_DECISION_REQUIRED / Auto Continue = NO`：固定 encoder revision/缓存身份不闭合；需要新增下载/安装/联网；模板 mask 触及事实、数值、日期、版本、法条或正文且无法高置信分离；role-free seal 前发生标签/角色泄漏；四臂除预注册变量外出现其它差异；Run Manifest 无法绑定输入/源码/模型/参数；发现与冻结合同或 R2 文档冲突。

## Expected closeout

交付一个新 Run Manifest、模板覆盖脱敏汇总、四臂 role-free 结果与后封存 Evaluator 汇总、K1-A/B/C 判定、失败/异常完整记录、测试与 Git 收口。完成后 STOP，不自动进入 S1 或任何正式/付费阶段。
