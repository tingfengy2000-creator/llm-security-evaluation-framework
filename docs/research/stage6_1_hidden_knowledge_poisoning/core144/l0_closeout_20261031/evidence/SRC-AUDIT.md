# FULL01 离线输出归因

任务 `P1-L0-FULL01-SEALED-OUTPUT-AUDIT-01`。Run `VACE-L0-D1-20261030-FULL01`。没有新的 PODR。结果提交 `bfc9685e5cdde1757643bd6825e52e34bbc85f52`，执行提交 `830bb5b3eb950f30494c9e3ef6affdcc8efc7dcb`。

这是对已封存 240 条输出的离线审计。没有重新推理，没有改 parser，没有替换 FULL01 指标，也没有调用模型。原运行目录的文件索引在审计前后一致。案例原文和逐条私有记录不进入 Git。

身份与封存计数一致。F5 为 SUPPORT 70、CONTRADICT 7、INSUFFICIENT 43。Oracle 为 SUPPORT 83、CONTRADICT 20、INSUFFICIENT 17。输入拒绝为 0。输出失败 F5 为 40、Oracle 为 17。无输出错误的模型 INSUFFICIENT 是 F5 3、Oracle 0。

主分类可加总。F5：引用不在指定正文 30，UID 不存在 8，JSON 语法 1，SUPPORT 缺少外部证据 1。Oracle：引用不在指定正文 12，JSON 语法 5。UID 不存在和 quote 类型错误已经按字段拆开；本轮 8 条都是 UID 不存在，没有把 quote 类型算进这一类。附加诊断标签不与主分类相加。

Poison 的原 CONTRADICT 被校验改成 INSUFFICIENT：F5 1，Oracle 0。Clean/HN 的原 CONTRADICT 被拦住：F5 0，Oracle 1。原 SUPPORT 被拦住：F5 是 Poison 10、Clean 11、HN 17；Oracle 是 Poison 5、Clean 4、HN 2。这些转移只记为 RAW_VERDICT_DIAGNOSTIC。

校验通过后 Poison 仍为 SUPPORT：F5 22，Oracle 19。校验通过后 Clean 仍为 CONTRADICT：F5 1，Oracle 4。HN 仍为 CONTRADICT：F5 1，Oracle 2。

120 对里，仅 F5 校验失败 36，仅 Oracle 失败 13，两边都失败 4，两边通过但判决不同 12，两边通过且判决相同 55。Poison 上 Oracle 最终 CONTRADICT 而 F5 不是的有 11 对；其中只有 1 对是 F5 原 CONTRADICT 被引用校验拦住。不能把其余配对写成检索召回收益。

低检出率的主要部分是校验通过后的事实、条件和版本判断。引用和 UID 绑定失败足够支持以后另行审查输出合同，但没有证据表明修改合同就会提高 CONTRADICT 检出。该建议没有实施。

状态是 FULL01_OFFLINE_OUTPUT_AUDIT_COMPLETE / OWNER_REVIEW_REQUIRED。不重跑 FULL01，不启动 VACE-LM、D2/D3 或下一轮推理。
