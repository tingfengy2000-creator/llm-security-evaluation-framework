# 5060 Codex｜Owner28 独立EVAL已到达，待5090格式桥接后一次盲预测

**重要当前事实**：5090远端已推`a8de64fbf2c279a642c9b9a41ddf5c5481b8cfca`；原Git包存在于`docs/paper1/dual_machine/repro5090/owner28_eval/EVAL_ROLE_FREE.json`，原SHA`2aafd7d7bcd8e3860771063a31770e350532065abb251f38f99c7ac39ba50cb7`，包含32主世界+7镜像。你前一轮记录的5090无交接是旧观察，不能继续作为现时阻断理由。**但原文件结构和已冻结runner不兼容，不得直接运行或修改算法**。先读`docs/paper1/dual_machine/OWNER28_5090_TO_5060_SCHEMA_BRIDGE_AND_ONE_SHOT_HANDOFF_20261111.md`全文。
1. 在`research/paper1-chinese-defense-5060`验证工作树/远端SHA。只用`git fetch origin`和`git show origin/research/paper1-ragdefender-repro-5090:<path>`只读获取5090的兼容JSON和公开兼容manifest；**不得merge、拉取5090私有标签、阅读5090真值来源报告，也不得把旧DEV改为EVAL**。
2. 目前等待5090生成`EVAL_ROLE_FREE_5060_COMPAT.json`、`EVAL_CURATOR_5060_COMPAT.json`和`EVAL_COMPAT_BRIDGE_AUDIT.json`；校验旧rolefree SHA、旧manifest SHA、新SHA及全32主世界queries和352段文本无损，镜像7个单列NOT_RUN。如果5090尚未交付，仅做只读branch检查和开发代码SHA冻结，不尝试科学运行。
3. 兼容材料满足来源、权利、4未见事实组、≥2独立新文档谱系、≥2签发类、查询/role隔离之后，在已有`scripts/research/run_chinese5060_owner28.py`先执行`check`纯准入，**完全复用原固定源码、MiniLM revision、Chroma、RAGDefender B2/RD_ZH/DATE_ONLY/NONE配置**。任何schema/模型/来源审计失败立即停止并回传精确错误；不能临时改Validator迁就样本。
4. check PASS后按Owner28合同一次性完成32主世界的TopK5检索和四臂盲预测。严格保持Git冻结代码，模型/索引/TopK相同；防御器看不到gold、错误原子、来源真值证据。封存32×5 rank、4×32预测掩码和完整SHA，先于5090评分。
5. 只以无角色ID、rank、掩码和SHA生成5090可交接的预测包；不得含候选正文或标签。由5090用**私有新旧ID映射**做一次评分、回传聚合。5090未确认预测SHA不得评分，5090的标签不得返传至5060研发进程。输出Owner28 EVAL manifest与Stage G0-G5记录，引用5090真实新SHA及Own frozen code SHA；只有被真正执行的数字才写成完成。
6. 若无法满足阶段门，提交`EVAL_BLOCKED_SCHEMA_OR_PROVENANCE`报告及已完成部分，只提交5060分支并更新Tracker；不得宣称EVAL已运行或重新做Owner27 DEV。

**不变禁止事项**：不改Owner27封存样本与结果，不改RD参数、不重跑已封存B2/RD-zh，不触D2/D3/HOLD8、不调M1/M2、无商业API/下载、不运行5090 Claims、不合并main。本任务是配合5090桥接，无新的科研实验授权。