# Paper 1｜Owner18 Rule-V2旧73开发完成后的监督复核（2026-11-09）

**状态：`SUPERVISOR_EVIDENCE_REVIEW / NO_NEW_OWNER_AUTHORIZATION / INDEPENDENT_VALIDATION_NOT_RUN`。**
实测证据远端 HEAD `33d67cfbdbc93b90bdcfa27241be6539f28c3f14`；Run `W1-5060-S1B-RULEV2-DEV-20261109-03`；源码冻结执行提交 `da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f`；私有 Manifest SHA256 `c8e6258e73cd6076e1ea25b3cdd35c0c68167d5e44122c1725da260f359d09ee`。

## 核验事实

- GitHub恢复时5060分支与报告SHA一致，5090仍 `dbd91f3667964baca69aeb82a6292c4fe193c965`。
- 开发数据为原S1完整73个view（61个不同语义案例，另12配对视图），属于`EXPOSED_DEV_FIXTURES / NOT_INDEPENDENT / NOT_HUMAN_GOLD`；三轮保留源码SHA、逐轮分母、所有失败，原S1 `S1_FAIL_STOP` 没有覆写。
- 旧Rule-V1：完整正确30/73、错误4/73、UNKNOWN39/73，有答案值命中31/61，已决定错抽4/34，应拒识误答2/12。
- Rule-V2 第01/02/03轮：完整正确分别57/58/58，错误2/2/1，UNKNOWN14/13/14；值命中58/61、60/61、59/61；已决定错抽2/59、2/60、1/59；应拒识误答均0/12。最终值命中96.72%（Wilson95% 88.81–99.10%）、已决定错抽1.69%（Wilson95% 0.30–9.00%）；**仅已暴露开发数据点估计，不能算独立通过90%/2%门**。12配对不是12个新独立事实。
- 最终14条UNKNOWN中12条本应拒识、2条有答案漏抽。唯一错误为数值相同但证据span选择不同（同一句较早的相同值）；该错误按预注册严格评分保留，不应通过改Gold或直接豁免。
- UIE Nano发布者权重/分词器许可、不可变release ID、SHA256和Windows CPU完整依赖锁仍UNKNOWN；当前Protobuf 7.35.1与要求3.20.2冲突。Qwen 1.5B资产门同样没有Owner许可；0下载、0安装、0加载、0新模型/API推理、0费用。
- 23定向单测、Ruff、MyPy通过；仓库源码支持query槽位、标量/单位、版本、scope、source char/UTF8 span与拒识；但词面有限，仍依赖`v02._titles`识别文书标题与有限字段/单位正则，开放域自然表达及实体关系未得到有效测试。
- 新方法还没有做RAGDefender检索上下文过滤的端到端效果测试；HumanGold0，正式ASR/QAAccuracy均NOT_MEASURED；S2–S5继续锁定。

## 关键科研判断

1. `RULE_V2_DEV_CANDIDATE_READY`：允许把`da3cbd9...`视为**可提交未来Owner独立验证审批的候选开发版**，不是S1-B PASS、不是确定性通用抽取能力；旧73测试若继续调参必须标暴露开发。
2. 同值多次出现应处理为候选`{value,span_set}`或在评价协议中事先说明多源span等价性，但**不得在已见73的Gold或现行规则上事后更改唯一错误**。如要调整策略，必须另立开发版本并预先固定新评分口径，不能引用旧73新分数证明通过。
3. Rule-V2明确列举词面字段、单位、标题和条件规则。未见领域外自然文档、多句/多段跨范围及新写法测试，存在被73条合成数据后验拟合风险。
4. P0坚持`UNVERIFIED_TEXT_ONLY`，中文抽取的成功不等于可信来源身份与版本真伪核验成功；无独立来源锚时不升权，不能把此开发收益写成VESA防御增益。
5. 后续两种可选执行策略：
   - `PATH_A_QUICK_RULE_ONLY_INDEPENDENT_GATE`：由与5060开发隔离的保管/审核人员独立准备新且未暴露的100个语义案例，先固定Rule-V1/Rule-V2版本与评价标准后**另签Owner单次验证许可**。优点是快速判断规则版是否可行、无新模型许可依赖；缺点是这批数据一旦揭盲便不能作为以后UIE/Qwen同等未见测试，应另留后续公平集合。
   - `PATH_B_JOINT_FOUR_ARM_INDEPENDENT_GATE`：先闭合UIE/Qwen两个模型的具体权重许可、资源与本地开发推理权限，再统一冻结Rule-V1/Rule-V2/UIE/Qwen+same verifier，四臂一次性提交同一套未见100主语义案例+20从属配对视图。优点是公平、少消耗独立标签；缺点是UIE授权不确定，Qwen现有RAM不足，耗时风险更大。任何改用Qwen都必须Owner新授权。
6. 监督推荐：`RECOMMEND_PATH_A_FOR_FAST_FEASIBILITY`，但必须**先明确不会将首次Rule-only验证数据作为后续模型盲评主集合重复使用**。更关键的优先事项是指定与5060隔离的独立来源/Gold保管方、样本许可与source span标注和测试隔离。该建议不是执行许可。

## 仍须Owner明确决定

- A规则版先行独立验证，还是B等待UIE/Qwen资产闭合后四臂共同独立验证；
- 100个不同语义案例与20个从属配对视图的**独立来源、保管人、两审阅者、冲突仲裁人**；
- 是否将未证新版/跨scope误答0作为**新一轮**另批准的安全硬门（不得回溯改旧合同）；
- 新模型下载、安装、加载、推理、独立验证和后续S2–S5均单独申请。

**STOP**：维持`MODEL_ASSET_NOT_AUTHORIZED / MODEL_INFERENCE_NOT_AUTHORIZED / S1B_INDEPENDENT_VALIDATION_NOT_AUTHORIZED / S2_TO_S5_LOCKED / AUTO_CONTINUE=NO`。
