# W1-OD-20261108-5060-S1-OFFLINE-16｜Owner 批准 S1 独立中文事实抽取离线验证

**日期：** 2026-11-08 JST  
**批准状态：** `OWNER_EXPLICITLY_APPROVED / BOUNDED_S1_OFFLINE_ONLY`  
**唯一分支：** `research/paper1-chinese-defense-5060`  
**前置远端 HEAD：** `920c32359a0118f217ab524a88cd771c0d48d912`  
**Owner 原话：** “批准 5060 单独进入 S1 独立中文事实抽取验证，保留 S2–S5 的后续审批门。5090还在等待 Meta's Llama2 models权限审批。”  
**证据基点：** `W1-5060-R2-FAIRCTRL-20261108-02`、提交 `5968369eaa1b3f8d1af2d9262ef5f3f145c4a83c`、预注册 K1-C，R1-06 / R2 S1 自然化要求。  
**本授权不产生新的科学试次或通过结论。**

## PO-MHEP 十二字段授权记录

1. **Issue ID:** `W1-OD-20261108-5060-S1-OFFLINE-16`。
2. **议题：** R2 K1-C 后，检验 VESA 事实值、版本与 scope 抽取器的自然中文独立开发验证门；不改变已接受的研究方向。
3. **发现阶段/任务：** 5060 S0 + R2 已完成，R2 因 Clean 误删及零可作用池进入 `K1-C / INSUFFICIENT_OR_MIXED`，S1 仍未运行。
4. **事实：**
   - `OBSERVED_FACT`: 5060 R2 四臂 36 世界完成；char2 112/180 删除，Clean 错删5/10，可信来源锚0/180；当前抽取器范围可比的已删候选为0。
   - `OBSERVED_FACT`: 5090 远端分支 `dbd91f3667964baca69aeb82a6292c4fe193c965`；Llama2访问申请已提交、未有批准凭据；Llama2未下载，Claims1–3未执行。
   - `SOURCE_DERIVED_FACT`: R1/R2 冻结设计要求 S1 ≥60 个与 D1 不同的中文带标注实例、自然化无显式答案模板、错误与拒识分离、可见 span 与版本适用范围、Wilson 区间。
   - `INFERENCE`: 在 S1 抽取可信门未验证之前，继续在旧 D1 上调试 M1/M2/M3 或启动 S2 存在研究有效性风险。
   - `UNKNOWN`: S1 的可见证据准确率、范围绑定准确率、拒识率、自然化性能及真实外推能力。
5. **受影响的冻结约束：** K1-C、R1/R2、P0 可信单调、D1_DEV_EXPOSED、D2/D3 隔离、S2 后才冻结最终方法、S3 独立造题方未指定、S4一次性门、S5新许可、HumanGold0、原 B2/R2/108 历史不可变、5090 compute-only。
6. **为何现在处理：** S1 验证直接决定 M1-safe 的前置可行性，以及 S2 的 M2/M3 事实分组与版本适用核验能否使用抽取结果。
7. **下游风险：** 同一个 Agent 同时写样本答案和看模型预测可能形成循环验证；固定“答案是X”模式会虚增准确率；过度 UNKNOWN 可绕开 wrong/decided；来源 span 与 scope 绑定错误会误放伪造版本；越权网络/数据集触碰、旧 D1 调参、5090 未批 Claim 会破坏合同；开发试验不等于独立外推或论文效果。
8. **批准选项 A：有界 S1 离线验证。**
   - **动作：** 5060 仅在自身分支新增独立 S1 工作目录与测试，使用不少于60个与 D1/D2/D3/原108隔离的独立手写中文标注实例验证冻结抽取器接口与其最小实现；先冻结测试样本的合法输入、source span、标注与哈希，再从独立的算法运行视图执行。允许独立开发样本上的透明规则修订，记录版本/失败，不许在正式 S1 封存评估结果上静默选样/改答案。
   - **优势：** 以零付费 API 成本先核准方法真实前置能力，缩小后续 S2 返工。
   - **缺点：** 若仅在同机不同职责隔离，不能宣称由外部独立人审产生真实语义 Ground Truth；真正独立人工核验未知时，标注验收须保留 `PROVISIONAL`。
   - **资源/成本：** 使用既有本地依赖/环境与 D/E 受控空间；不下载模型、依赖或在线资料；0新增商业/免费 API、0联网模型、0新检索、0费用；C盘禁止新的项目可控存储，D/E 安全余量按既有门。
   - **风险/可逆性：** 只新增源、测试与私有归档，保持旧 D1、B2/R2、历史运行不变；输入 SHA、代码 SHA、测试锁与失败记录可追踪。
   - **后续/论文：** 通过仅可作为申请 S2 的必要条件，不自动解封任何科学实验或新颖性主张。
9. **LOCAL 建议：** 采用 S1 独立手写/自然化评估：验证集≥60，开发样本与验证样本不重叠；数据作者/标注、算法、Evaluator 按角色/文件权限逻辑隔离，真实人工独立审阅如未发生必须显式标 `NOT_HUMAN_INDEPENDENT`。先看指标和失败归因，再判 S1 PASS/FAIL/INSUFFICIENT，不将其升级为正式 Gold。
10. **理由与置信度：** Owner 对 S1 的独立批准明确，范围高置信；S1 能否满足 90% 和≤2% 无法预判；小样本置信上界与真实生产可用性仍不确定。
11. **Owner 已决与未决：** `S1 = APPROVED_BOUNDED_OFFLINE`；`S2,S3,S4,S5 = NOT_APPROVED`；`R1-10(B) S3_CONSTRUCTOR = UNASSIGNED`；`5090_Llama2_ACCESS = APPLICATION_SUBMITTED / APPROVAL_UNVERIFIED`，新下载/Claim 均不授权。S1 是否通过仅由实际封存结果与既有门决定，不得 Agent 自批进入 S2。
12. **执行边界：**
   - **允许：** 独立可见中文模拟文本/合法本地数据、小范围规则抽取器实现与纯本地验证；至少60个独立验证实例；主体/属性/金额比例数值单位、日期/版本、生效时间/条件/否定例外、跨scope、伪新版声明、自然化去答案模板、网页模板/正文混排、无值/UNKNOWN；由独立封存证据计算 correct/incorrect/UNKNOWN、wrong/total、wrong/decided、coverage、span、错误类型与 Wilson 95% 区间；测试和 Git 治理收口后 STOP。
   - **禁止：** 5060读取 D2/D3 或 Reviewer/GT、给算法读样本 Gold/历史 role/target/参考答案、把 AI 自填数据宣称 Human Gold、拿 D1 后验修规则、重跑 B2/R2/旧108、任何网络/下载/商业或免费模型 API、扩大 S1 为 S2–S5、修改 P0 安全政策、5090 Llama2 下载/Claims、跨分支操作/主分支合并。

## S1 预注册验收与解释

- **总分母：** ≥60 个独立标注且具备可见 source span 的验证案例；额外 development examples 不计入正式 S1 分母。
- **必须报：** `total`、`decided`、`correct`、`wrong`、`UNKNOWN`、`wrong/total`、`wrong/decided`、coverage、abstention、全量与自然化分层、值/单位、主体属性、日期范围、source span 错误以及 Wilson 95% CI。
- **保留既有条件：** 准确率≥90%，用于 M1-safe 的已决定结果错抽点估计≤2%，不可 all-UNKNOWN。不得更换含 UNKNOWN 的分母或把 UNKNOWN 作为正确值。若两项硬门含义因实现口径发生冲突，按先验两种口径同时报告并升级 Owner，不静默改判据。
- **统计边界：** 例如 60 个已决定案例且0错时，Wilson 95% 错误率上界仍约6.0%，不能说严格证明总体错误率≤2%。所有通过结论均限 `S1_DEV_OFFLINE_GATE`，不属于真实世界鲁棒性或正式论文主效果。
- **严重错误：** 实际值错抽、同名异范围混淆、旧/新版本误判、否定例外未识别、source span 伪绑定应逐项暴露；高风险未验证更正不得以“多数认为正确”提高信任。
- **正常失败：** 若无法满足 S1 门，应保留结果与具体归因并 `S1_FAIL_STOP`；禁止后验挑样、更改 Gold 或自动启动 S2；同一开发阶段所有修订须保留版本与重跑历史。
- **独立性：** 代码、样本、评估分别隔离；如真实独立审阅者未参加，则不得标 `EXTERNALLY_INDEPENDENT_HUMAN_GOLD`，应将评估级别记为 `SEALED_SYNTHETIC_DEVELOPMENT`。

## 必须停止条件

新依赖/网络或模型身份不明、样本与旧 D1/D2/D3 污染、标注/答案泄露到 extractor、来源许可/明文不能安全使用、评估语义与既有 R1 冲突、证据/Run Manifest 不全、未知磁盘资源风险或任何 PO-MHEP 升级项。停止时保存已完成数据、异常、条件变化，报告十二字段决策卡，`Auto Continue=NO`。

## 期望交付

S1 专用 Run ID、独立验证样本/标注的私有 SHA、可复现抽取器源码/参数、role-free outputs SHA、隔离 Evaluator 汇总、混淆类型表、模板/自然化分层、Wilson CI、S1 唯一 PASS/FAIL/INSUFFICIENT 结论、错误与 UNKNOWN 残余风险、测试/静态检查/秘密扫描、Git commit+push 和停止记录。真实私有正文、Gold、来源信息和密钥不上传 Git。
