# Paper1｜Owner19 S1-B数据封存完成后一次性规则可行性评估审批前复核

日期：2026-11-09 JST  
**状态**：`SUPERVISOR_GATE_REVIEW / READY_FOR_OWNER_DECISION_WITH_PREFLIGHT / ONE_SHOT_NOT_AUTHORIZED`  
**核验远端实验提交**：`20402e94ed3da6be155a605daba272ec0a7c2cf1`，5060分支比较 `identical`。5090远端 `dbd91f3667964baca69aeb82a6292c4fe193c965`，未变。  
**封存Run**：`W1-5060-S1B-FEAS-DATA-PREP-20261109-01`  
**封存回执 SHA256**：`531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58`  
**来源**：已提交的脱敏 `W1_5060_S1B_FEASIBILITY_DATA_PREP_MANIFEST.json`、`W1_5060_S1B_FEASIBILITY_DATA_PREP_RESULT.md`，固定源码 `s1b_feasibility_data.py@7581256c...`、`s1b_rule_v2.py@da3cbd9...`、`vesa_guard_v02.py`。私有D盘原始内容和Gold未被本监督会话打开，故未直接核验原始封存字节。

## 一、数据准备层判断

- 已报告100个主语义案例（70 ANSWER/30 UNKNOWN），20从属改写视图；4主题域、10来源家族；10场景每类10（7/3/2视图分配）；运行输入120条；暂定标注是同一个Agent产生，标记`AGENT_GENERATED_PROVISIONAL_FEASIBILITY / NOT_INDEPENDENT_AUTHOR / NOT_HUMAN_GOLD`。
- 输入、source-truth、Gold、配对关系、评分协议分件；105个支持集合/523个原文字符和UTF-8跨度检查、摘要相似度筛查、5定向测试和静态检测已报告完成。
- D1仅历史开发回归记录、旧73仅作去重、CMRC元数据只读，均未进入主100；0下载、0API/新模型调用、0实际Rule-V1/V2新预测/评分。
- 接受为`DATA_PREP_COMPLETE`，**不能**提升为`INDEPENDENT_HUMAN_GOLD`或`S1B_PASS`。词面近重复无报警不等于语义/模板模式独立；同一Agent出题、开发、保管存在非独立性。

## 二、正式运行前必须披露的结构风险

**标题前置条件**（从公开代码结构推导，未经新样本预测）：
- 数据生成器的`title = ... if (index+len(seen)-1)%10<7 else ''`在10类各10例的主分布形成70条有标题头、30条无标题头；每类i<7为ANSWER、i>=7为UNKNOWN，10类循环移位，因此可回答70条中恰有49条含生成的标题头，21条不含。
- Rule-V2查询端的`v02._titles(query)`通过`《...》`识别标题，并要求`len(titles)==1`；证据端候选还要求`subject==title`。无标题头的21个可回答例**存在显著拒识风险**，除非正文/查询中其它位置已有可识别书名结构。未读取私有文本，不能宣称这些21条已被证实全部失败或得出精确性能上界。
- 这是目标应用范围与当前方法的直接比较，不应因预测结果不利而修Gold、删无标题项或偷偷开发v3。建议作为预注册分层`TITLE_HEADER_PRESENT / ABSENT`报告，不使用该分层修改算法选择或新样本。
- `linked_passages`与`equivalent_spans`的Gold可接收多个支持片段；现有Rule-V2单条结果主要暴露`source_span`标量与候选`scope_spans`。公共适配器如何从冻结结果映射到`accepted_span_sets`需**事前**固定，不能通过Gold反向补span；对证据不足的证明必须保留范围/span错误而非自动豁免。
- 所有合成数据来自虚构来源，不构成真实source trust或version certification；即使Rule-V2好也只证明`synthetic extraction feasibility`，不是VESA真实知识投毒防御。

## 三、下一门建议

建议`ONE_SHOT_FEASIBILITY`（可行性探索、非正式独立人审），**但当前尚无Owner针对单次新数据评估的明确批准**。请Owner在读此卡后另作显式授权；在此之前任何预测、评分、标签揭盲均禁止。若Owner决定运行，则按以下前置硬门：

1. **固定来源与可恢复性**：原封存SHA、五类成员哈希与ZIP一致；私有原文不出D/E；旧Rule-V1固定源码`68d34a5...`，Rule-V2执行提交`da3cbd9...`与config hash完整绑定。无隐式重建新Gold。
2. **公平公共适配器静态预检**：仅用开发样例或无标签普通fixtures固定同一`query,evidence,id`输入接口、输出`value/unit/status/source-span-set/scope`、编码与失败策略；可采用保守丢失字段判错/UNKNOWN，不可从Gold回填；禁止在新120条上做试预测、试打分或逐项观测后修。
3. **单次批量离线预测**：两臂相同120视图，主100、从属20；先写全量role-free predictions并hash封存、出站拦截/磁盘边界与过程失败如实记；不能抽样、不重试、不静默改参数。
4. **后揭盲只读评分**：独立Evaluator仅持暂定Gold，不逆向修改模型或问法。100主案例、70可答、30应UNKNOWN与20从属配对分开报；全量值命中/70、wrong/decided、wrong/total、strict_scope+span、应拒识误答、未证新版/跨scope误答、覆盖/UNKNOWN、各10类、标题有无、自然/显式问法与Wilson区间。所有来源全部标synthetic/provisional，不能将100主+20视图当120独立案例。
5. **预注册判定**：点估计值命中/70>=90%，即至少63/70；错抽/decided<=2%，必须decided>0且不能all UNKNOWN；原`2%`为点估计开发门，不能宣称达到95%上置信界2%。未证新版/跨scope=0仅附加观察项，未经Owner特别批准不可充当新硬门。
6. **STOP**：fail closed于SHA/代码/输入泄漏或接触隐藏Gold、各臂采用不同规则/适配器、缺少120条预测、身份不闭合、程序越界、不可复核结果、参数/GOLD后验修改。无论PASS/FAIL立即STOP归档，不解封S2–S5、UIE/Qwen、5090或正式测试。

## 四、PO-MHEP 审批卡（建议，非已决）

1. **Issue ID** `W1-PENDING-5060-S1B-ONE-SHOT-FEAS-20`（建议编号，**尚非Owner批准决策**）。
2. **问题** 100主+20从属已封存，是否准入固定Rule-V1/V2一次性无模型推理离线比较。
3. **发现阶段** Owner19 DATA_PREP_COMPLETE；Owner18 Rule-V2暴露73开发完成；S1B_ONE_SHOT仍`NOT_AUTHORIZED`。
4. **已知与未知** 100/70/30/20、源/Gold/协议hash、5项测试已核脱敏报告；独立人审0；私有原文和score protocol没有被监督端直接审阅；实际准确率与span适配效果UNKNOWN。
5. **影响冻结** R2 K1-C、S1 FAIL、D1_DEV_EXPOSED、D2/D3全隔离、P0约束、S2–S5与模型门、5090禁令保持。
6. **为何现在** 零外部API、零新权重下可快速判Rule-V2是否存在明显领域外/无标题弱点，避免继续在已暴露73条上调参。
7. **下游风险** 同Agent生成/开发造成伪独立；标题模板偏差、span协议对接与过拟合；不应凭样本内点估计宣称生产可靠。
8. **选项** A按硬门下一批单次运行（快速获得负/正可行性证据，无法当正式Gold）；B先只读适配器静态预检并另批运行（降低工程停止风险）；C放弃规则初筛转模型（资产许可、硬件未闭合）。监督建议 A with preflight-only gate，需Owner明确同意。
9. **建议** 实验重心从旧73开发迁移到冻结新100，一次性、只读、role-free先封存；若未达门槛如实结束，不挑数据换目标。
10. **信心** 数据准备完成高；规则正式性能及泛化未知，尤其无标题样本存在已知结构性脆弱点。
11. **需Owner批准** `ONE_SHOT_RULE_V1_V2_EVAL`，是否把“未证新版/跨scope错误0”升格为新硬门（建议本批仅观察，不事后改门）。
12. **当前允许与禁止** 目前仅允许治理复核与读取公开证据；下一批新数据上的预测/评分/揭盲尚未授权，模型下载/安装/加载/调用、D2/D3、S2–S5及5090 Claim严格禁止。

结束状态：`DATA_PREP_COMPLETE / OWNER_ONE_SHOT_DECISION_REQUIRED / MODEL_ACCESS_NOT_AUTHORIZED / AUTO_CONTINUE=NO`。
