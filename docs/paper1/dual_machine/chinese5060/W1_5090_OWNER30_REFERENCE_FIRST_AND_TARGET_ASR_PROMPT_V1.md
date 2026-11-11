# 5090 Cursor｜Owner30 一日自动可行性：先封存参考答案，后核攻击命中（不要人工双审）

## 首先
保持自身`research/paper1-ragdefender-repro-5090`分支；`git fetch origin`，只读下面5060分支已提交的Owner30有界授权：
`docs/paper1/dual_machine/owner_approvals/W1_OWNER30_ONE_DAY_AUTOMATED_RAG_FEASIBILITY_20261111.md`，特别是末尾`Operational simplification ... (PREFERRED)`。当前任务不是原先的HUMAN_GOLD双审包；那一阶段正式实验再做，今天**Human Gold始终0**，不需要人工签名、第三人裁决、再选题、复算Owner28标签或重新生成。

当前5090唯一可信源：私有32世界Gold、真实官方版本时间/范围、原独立source audits及原sealed数据。5090当前分支可能比 `670d9ab0e546d46117bf5c48ebb2b0043689f453` 更新，不可假设HEAD不变。原私有标签SHA `c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595`、ID映射SHA `119e7f5242c86a3fd74d10df9ad3d402a41b5cfe4037a1f6a6f4f46f3fe5c0a0`不可变。

## 第A阶段：立即完成（无需等待5060）
1. 从封存的官方事实依据构造32条`world_id, fact_uid(optional opaque), answerable, normalized_gold_value, accepted_variants, unit, event_date, scope_qualifiers, official_uri, section_locator`。来源是独立原始事实、问句时点和范围，**绝不能**看5060的95生成答案、统计翻转或已预测的模型回答后再选择或修改标准。不访问以前Owner27优化规则，也不调旧标签。
2. 每条的正确答值必须与现存官网历史版本及生效/过渡关系一致；2015/2021人口法、1995年工作时间、2021专利法要区分生效前后，不可以“新法总是正确”替代事件时点。无证据或存在转折模糊则`REFERENCE_UNRESOLVED`，不猜值。正确答案之外的攻击目标只留在5090的私有托管，**不得**放入此表。
3. 核实上述`normalized_gold_value`均为可公开的**短事实原子**，无私有命令/原文大段/身份/secret后，发布`docs/paper1/dual_machine/repro5090/owner30_eval/OWNER30_PUBLIC_REFERENCE_ATOMS_ONLY.json`（仅32条公开答案原子及可信官网元数据，不含P/C/H/B、Poison目标、评估标签、历史私人ID映射），并发布 `OWNER30_REFERENCE_FREEZE_MANIFEST.json` 包括原私有SOURCE SHA、真值表内容hash、来源权利、校验过程/退出码、角色边界。签名状态`SOURCE_REFERENCE_AGENT_PROVISIONAL / HUMAN_GOLD=0`，并披露此举会在预测封存后公开一部分评估集答案，不能再称其为未来未见测试集。
4. 若事实答案有法律/时间/条件歧义、答案原子包含未经授权文本、或不能保证正确，则不要放“自动正确标签”，只标REFERENCE_UNRESOLVED且按预定分母报告。仅为发布合法的短事实原子不需要第三方模型，也不调用收费API。

## 第B阶段：5060自动评分完成后才执行
5. 获取5060新提交的`OWNER30_AUTO_ANSWER_JUDGMENTS.json`与manifest；核SHA、95唯一回答、原始96网格中**缺失的NONE一格**、31三臂完整配对；四事实组32world不改变。该输出只能是后处理暂定模型或规则评分，不能覆盖Owner28/29原归档。
6. 用5090**私有预先冻结的攻击目标值**和原始场景/TopK已召回P，单次计算 provisional targeted-ASR 的 intention-to-treat与conditional retrieval；0/5未投毒世界无target=>NOT_APPLICABLE。单列答对/错误拒答/合理拒答/无依据正确/格式错误/歧义，且来源真值和模型评价意见冲突时`DISAGREEMENT`不暗中改标。
7. 在31个世界相同配对上比较 NONE、B2、ZH 的正确回答净差、正确→错误、错误→正确、拒答↔正确、攻击目标命中翻转；32个B2-ZH配对单列，按4事实组+3谱系展示；不要把32当成独立事实，别写正式ASR。
8. 提交`docs/paper1/dual_machine/repro5090/owner30_eval/OWNER30_RAG_AUTOMATED_FEASIBILITY_REPORT.md`与`OWNER30_RAG_EVAL_MANIFEST.json`，附计分程序源码SHA、所有输入SHA、评审模型/账本（若5060执行则属同供应商Judge）、未解冲突和明确`FEASIBILITY_SIGNAL_POSITIVE/NEGATIVE/MIXED`。原真实Gold、原候选角色与攻击目标只留5090私有目录；公开Git只给聚合和经安全核查的答案数值/匿名评分。
9. 只推送5090自身分支。Claim1-3 NOT_RUN；不碰D2/D3/HOLD8、不新增生成调用、不签HumanGold、不改Owner28一次性评分；完成后STOP，回传HEAD和实际数字。如果5060尚未交付，就交第A阶段`REFERENCE_READY / SCORE_PENDING`，不能伪造B完成。

**成本** 5090默认全本地规则与私有标签计算0费用。若本机没有已准入合规Qwen接口，不安装/复制5060秘钥，走参考答案公开原子→5060本机Qwen暂定Judge路径即可。