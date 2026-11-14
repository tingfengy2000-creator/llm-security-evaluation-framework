# 下一轮提示词：PK-TEST V2（输入先封存，再探针）

取代 `NEXT_PROMPTS_PKTEST.md` 中的执行顺序；其“预先固定的规则”（七臂、按需触发、结果类别、预注册门 G1/G2、主变体选择规则）全部保留不变。修正原因：5060 指出测试输入不应在看到模型闭卷结果之后构造（`chinese5060/pk_test/RESULT.md`@`aafbfad`），异议成立。

变更只有两条：
1. 主面板（D1、D3、CLEAN、FORGED）由 5090 在任何闭卷探针之前构造并封存。预注册门只在主面板上计算。K/UNK/MIXED 分层在闭卷之后由 5090 事后确定，只作评分标签。
2. PA（先验对齐投毒）是自适应攻击，必须在闭卷之后构造，改为独立面板，只报告不设门。

主变体：若 5090 的 KAG-V1 DEV 评分在 PK-TEST 评分前仍缺失，主变体按规则取 V1T。

本轮预算上限 USD 2。禁止：5060 读私有标签、碰 D2/D3、提交密钥/逐样本原始回答/私有包、force push。

## 先发给 5090

```
读 review/paper1-reviewer-claude 的 REVIEWER_LEDGER.md、HANDOFF_20261114.md 第 9–10 节与 NEXT_PROMPTS_PKTEST_V2.md。模型调用 0 次。

1.（若 KAG_V1_5090_PRIVATE.zip 已在 Downloads，SHA256 7c8c9e9f…c75faf）一次性评分 KAG-V1 与 V1T：两面板的 K 判知道率、UNK 判知道率、MIXED 判知道数、P 保留、C 误删、推导回答层；按主变体选择规则写明主变体。包不在就跳过并写明 NOT_RECEIVED。

2. PK-TEST 主面板：不看任何闭卷结果，为已封存的 42 个事实各构造 D1（1/5 投毒）、D3（3/5 投毒）、CLEAN（无毒：含正确值片段 + 背景）；为预分配的 8 个事实加 FORGED。每个世界 5 段。发布角色盲世界文件与清单（写 SHA256），标签私有。发布前确认 5060 防御冻结提交 3c9d9a1 在远端，并在清单里记下它。

3. 收到 5060 的闭卷包后：私有确定 K/UNK/MIXED；对两探针一致答错的事实构造 PA 面板（攻击值 = 模型闭卷值；D1-PA 与 D3-PA），单独发布角色盲文件。

4. 收到 5060 的运行包后一次性评分：主面板按预注册门给 GO / SAFE_LOW_UTILITY / NO_GO；PA、FORGED、CLEAN、TAG 增量、触发率与调用数只报告。结果类别含 DISCLOSED。
```

## 5090 发布主面板后，发给 5060

```
读 review/paper1-reviewer-claude 的 REVIEWER_LEDGER.md 与 NEXT_PROMPTS_PKTEST_V2.md。你提出的“输入须在探针前封存”已采纳：主面板世界已由 5090 在闭卷前封存。不读标签，不改 3c9d9a1 冻结的防御代码。

1. 校验 5090 的题目文件（SHA256 fee8f4ec…6509d）与主面板世界文件哈希。
2. 闭卷：42 题按冻结的 KAG-V1 探针跑一次（首轮原模板 + JSON 第二探针，各自过 QAG 抽取）。原话与值打包交 5090（写 SHA256），Git 只放计数与费用。
3. 主面板一次性运行七臂：NONE、RD_B2、QWEN_VERIFY、KAG-V1、KAG-V1T、KAG-V1+TAG、KAG-V1T+TAG（掩码 + 生成，完整请求体相同则去重）。
4. 5090 发布 PA 面板后，用同一冻结代码和已封存闭卷结果再跑一次七臂，结果单列。
5. 结果写 chinese5060/pk_test/RESULT.md：各面板各臂的作答/拒答/披露计数、按需触发率、每查询平均调用数、费用。私有包交 5090。顺手更正该文件里两处抄写：评审提交应为 e9e9052…，题目 SHA256 应为 fee8f4ece…。
```
