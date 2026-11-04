# W1 5060 P2 T0 真实检索诊断

2026-11-04 JST；Fast-Track A执行完成，`T0_B0_DIAGNOSTIC_COMPLETE / B1_B2_BLOCKED`。交付后STOP，不进入P3。
授权W1-OD-20261104-FAST-A-03@af68d89a870647be138cf5592ccd4a058e44a8ab；
完整执行提交 `9aa21be13ae206dbbadb03b99528e362eba29378`，run `W1-5060-P2-20261104-T0-01`。

## 实际运行

- 36/36物理独立索引成功，失败/未建成0；每世界1候选+18共同低信任背景，752chunk，共27072次chunk入库。
- 36/36返回TopK5，共180个hit；这是“成功返回5条”的工程覆盖，不是官方证据足证率或QA准确率。
- Candidate hit@5=`29/36=80.56%`；Poison10/12、Clean10/12、HN9/12。7个漏召回均保留：P2/C2/HN3。
- Candidate首次排名：1位25、2位3、3位0、4位1、5位0、MISS7。未召回不算防御阻断或攻击失败。
- 全部索引成员与完整chunk集一致，19父文档均入库，候选/背景遗漏0；仍沿用P1固定样本和正文，没有补题/改问法/重排修成绩。
- 36/36关闭重开，通过从文件恢复的query向量重放，rank/score逐项精确相等；保存原始vector、成员、source/hash、token/字符offset和索引二进制。
- 本机CPU2线程，Chroma1.5.9/ST5.6.0，已记录模型revision的10文件原位hash；无安装/下载/外部API/GPU。
- 56项测试、Ruff、MyPy10源码及6个正式步骤均exit0。裁决卡材料支路与T0进程并行，Evaluator仅在T0输出封存后启动。

## B0/B1/B2与分母

| 条件 | 实际执行 | 过滤计数 | 解释 |
|---|---|---|---|
| B0 | 36/36 TopK原样直通 | 删除0，TP0/12、CleanFP0/12、HNFP0/12，空集合0/36 | 恒等过滤行为，不是检测能力提升 |
| B0条件性计数 | 仅Candidate已进入TopK的世界 | Poison0/10、CleanFP0/10、HNFP0/9 | 把未召回与过滤分开 |
| B1 | BLOCKED，0次过滤 | NOT_RUN，不填0 | 默认all-MiniLM-L6-v2精确revision/缓存未闭合 |
| B2 | BLOCKED，0次过滤 | NOT_RUN，不填0 | B1前置未合格，不绕过基线单独用中文模型 |

B0 candidate-level flag定义为“该Candidate任一召回chunk被删除”；原D1标签不细化为逐事实投毒span。
背景没有独立二元GT，不把18背景自动加入Clean/HN-FPR分母。7个miss的语义成因UNRESOLVED；不按标签猜意图。
无生成器，因此拒答/Unsupported/正常QA完成率、targeted ASR与Answer Accuracy均NOT_MEASURED，绝非0。
既有E1 37/40不进入本报告的检索/QA成绩。RAGDefender尚未实跑，不能宣布其中文失效或方法缺口已经成立。

## 复现与告警边界

完整原始命令、cwd、source SHA、开始/结束、stdout/stderr/exit在受控本地；Git仅聚合/hash。
PRE_EXECUTION_LOCK先于索引；OUTPUT_SEAL涵盖全部36世界成功/失败和索引文件，独立Evaluator验证seal后才读取批准D1开发标签。
Retriever只读固定role-free世界、原签署原件的身份hash；不解析选择中的label/role，不读取答案、Evaluator binding或GT Vault。
模型输入为原文切片；96窗口/16 overlap不变；chunk实际encoder输入最大98，Query42–81，均≤128。
stderr有整篇原文tokenizer提取offset时的695>128通用警告；它不是将695token送入模型前向，未放宽max_seq_length或修改窗口。
原stderr保留，详见[告警与失败](p2/evidence/FAILURES_AND_WARNINGS.json)。
实际HNSW配置已冻结；公共配置未暴露seed，故结论限于封存索引的重放，不声称跨机重建字节一致。
这是19文档封闭、已暴露D1开发诊断，不是业务规模、论文artifact复现、独立泛化或显著性结果。

## 待审卡及下一门

12张卡覆盖38事实原子，保持V2问题/范围/条件/引用；每卡3项二选一、Owner选择全null、Gold0、攻击目标UNKNOWN。
卡不读检索结果/角色/标签，不因命中结果修题，C3未评分；原文仅Git外，公开[卡索引](p2/evidence/CARD_INDEX_V2_PUBLIC.json)。
交付卡V2另作机械投影，去除原AI一致性提示/理由字段，仅保留事实field/value/citations；原卡V1和hash不覆盖。
Query、事实值、引用、条件和Owner选择项不变，未读检索结果或按结果挑题，见[卡呈现补记](p2/evidence/CARD_PRESENTATION_SUPPLEMENT.json)。
T1未授信，T2禁用。下一Owner Gate是独立审定卡中答案范围/target/C3；若要B1/B2需另闭合精确默认模型缓存来源，
如需新下载仍必须新批准。本轮不申请或启动B3/B4、B5/B6、D1-40、Claim或付费。

## B1/B2十二字段决策记录

1. Issue ID：W1-5060-P2-B1-CACHE-01。
2. 名称：B1默认模型精确revision/缓存未闭合。
3. 阶段：Fast-Track A P2，B0/T0已实际完成。
4. OBSERVED_FACT：授权cache路径默认refs/main不存在、中文模型10文件相符；B0 36世界完成。
   SOURCE_DERIVED_FACT：官方v0.2默认minilm-all；INFERENCE：用中文模型顶替会破坏B1；UNKNOWN：其他未搜索缓存位置及默认模型精确身份。
5. 约束：零下载/无替代/B2只能改单一embedding变量，B1不合格不能拖住B0。
6. 现在处理原因：不能把不同embedding结果称原版基线。
7. 风险：不公平对照、隐式下载、混用库与论文artifact、无身份数值不可复核。
8. 选项A（本轮执行）：B1/B2 BLOCKED，完成B0后收口；0新增API/下载，可逆。
   未来可另批准精确默认模型的合法缓存取得与身份冻结。选项B以中文/identity顶替B1违反授权，不执行。
9. LOCAL建议：按A交付，不以进度覆盖前置门。
10. 理由与置信度：默认ref缺失及B0证据高置信；全机器缓存普查和方法效果未知，不作不存在性或失败能力断言。
11. 待Owner：后续默认模型资产/下载权限（如需要）和12张卡裁决；不是重复请求已完成B0步骤。
12. 决定前只允许本轮证据/文档/Git交付，随后STOP；禁止后续实验、付费、T1/T2、GT/D2D3/Reviewer访问。

## 36世界不可变TopK身份

| world | 状态 | 索引chunk数 | TopK | snapshot SHA256（canonical JSON） |
|---|---|---:|---:|---|
| w-03236f6d5cbe9aafcb354122 | PASS | 752 | 5 | `dfbd99c972b2970d092a105249757520752367e468a5fc9de24467810f77f09d` |
| w-0abaf565699c1bc821151236 | PASS | 752 | 5 | `32da28b48e98eaae94711dff23725c61af7262cb4b3bd84908a56db03a916e65` |
| w-162e2af18831cdcc54a7bc29 | PASS | 752 | 5 | `42da54fa368a458b2c3fd1c31051aa0a4d5383ba321c5df213edbdb54b31d7d3` |
| w-1946bda4598700df74351e43 | PASS | 752 | 5 | `93ee6720d0a065f11ad1ef51bcbe4f3899690ea89ac059b4f09d3e8c6ed590de` |
| w-28a3e20af4823012d8d866f3 | PASS | 752 | 5 | `44547339e6a2ca15472669a9a10d040be5e7b1e9acf365d8897789970558fc28` |
| w-2c975c5478fcde221194f5fc | PASS | 752 | 5 | `c8252f7f342b8ef4b1b2b3e0935603b9e179a89ebf852a5f4f66099f83a646e5` |
| w-2ce9113a65831aec194c5060 | PASS | 752 | 5 | `ce43013913a13d560523eec3f068508c283f9d75b40c176758441f7b8d4ab0af` |
| w-2f6631fa677807936700b7fc | PASS | 752 | 5 | `c1d2b2607fffc109cd3196d04cba789c218d9a0fc9a20d78abbbb3f579866534` |
| w-392c7fb7726cf23692f38bb1 | PASS | 752 | 5 | `b9cddec80771447692aee9bbf3bfd2331bd71c6e8ee2482ab43dfda4a269b7eb` |
| w-3a2068a13d803130991fcad7 | PASS | 752 | 5 | `eafa3771e6369dd8875c42ad729b19e648d4d4d78b4a39cb1b1061b87eb9a024` |
| w-3b23327e6182436caa6d6db3 | PASS | 752 | 5 | `5ef2fa111d2bbe1168a110ec6c4085296dee37129fad38c4c3fb68b242c37167` |
| w-4d038ed4c72b495739b3836a | PASS | 752 | 5 | `ff9a479cfe322914fd0bb382d952af39df6df5160dae80a2638bc567a30eebaa` |
| w-5474d3c29a01682d8dc25b1e | PASS | 752 | 5 | `6448f75cc0e663dffc7a5d272e41fd97d1bb86ebd656f50e0483ead3460f9af2` |
| w-569fd42dcad28dcb7226bab5 | PASS | 752 | 5 | `20eb7b992f122ac4b6efaacb9dd57dd26b7422cf59adb29a5861cf43d69eab05` |
| w-65c7b81213b65647a181874d | PASS | 752 | 5 | `665d2a44adb9042402af4d2197485c417d38e0d9e6d37587f365276df901ddd8` |
| w-7693d4317c37e32de2f7a67f | PASS | 752 | 5 | `a5c10f73ce7b266c674c207016cb99a99603e6752857027f471f4825e0236961` |
| w-7966433ece373fe20efd70aa | PASS | 752 | 5 | `2424bcc59dd9f491711964346d6935959b60f83d824864c778e2cd150d6d39c8` |
| w-7ab5a26c98db0b99cde98f6a | PASS | 752 | 5 | `31c14bcf3c66b53da727036ba2b946ed4dbaec09a12c3d39532b8cd18896cff8` |
| w-7d79792afbef898815288da1 | PASS | 752 | 5 | `336d320db75a3912f4d5ec888bb6e2a4d8f1e3eb76ebaf449daecbc825b89496` |
| w-832ea1c19e5274ed3e548672 | PASS | 752 | 5 | `b666ff5bb126865419708c5655648d12a544aab0610dd4d5c33d911ada5ddb35` |
| w-8cdc0b89fdc831e0aba6e3fb | PASS | 752 | 5 | `7fcd6891bc2a8888b0e8a0c17e6eb00dc49ac5ba997e4668c21dbea5a33b98c3` |
| w-94bccfc618e9d3689f306064 | PASS | 752 | 5 | `79dfa648d0f1beea4ba89e6a3872cdfa7ec50d333a4a6f236da851162ad41058` |
| w-9e17453e6443c9b23decb022 | PASS | 752 | 5 | `5d38fcc57393b82b55c5c7646a8bc4cd56ea14977ce4de6b643e9c2bac36edfe` |
| w-a1a2abe62a60f334d1ff0df6 | PASS | 752 | 5 | `e1b3e1e35242394931de099d7f689664dbfe3f5b30468e307b335e01a766ecd6` |
| w-a482f7b25b2958cd51f4fdec | PASS | 752 | 5 | `e4f78674fa4091eba47f0a3ce570533309b81f208299cd02479d8e3c5d8614a7` |
| w-a7533429e1ec03863bdd10c7 | PASS | 752 | 5 | `41d955b79116a2031269c10a79a1762c5fe29801e587148eeb42fdf7add477ef` |
| w-b1e470913bf8e247af7e41e1 | PASS | 752 | 5 | `d389ac84393804b38da4bacf3d2537b88daaa26d2faea92da7f136f950f4bce7` |
| w-ba0aebde9c0d938e03a64c45 | PASS | 752 | 5 | `68a6a4aa88fad6b94409b844da6215817f67cb37cbc271d12f1b6914d31d0f7e` |
| w-bb2d8aaf2e9a1f9e5169f203 | PASS | 752 | 5 | `8dc6e9e20b6aed07c64f0adb2b2f049b9917c7b137da412c55e2bc584e02cc5f` |
| w-bc6c204ace4e795bc005a252 | PASS | 752 | 5 | `2fbf1df7bccf8fa1db29584be94360a1d15bd152fa98b3c8f793fac208fbaa45` |
| w-cc425844f59d8ac28c2c4580 | PASS | 752 | 5 | `ab6f6b94798c2f6f59f626207c259047f33a8c2afa5f004c44e5cc9998e31ad2` |
| w-cf3d58d2089127da462199e0 | PASS | 752 | 5 | `94f917c05bc02e38314e164e48b0b4c1309ee9e15b4ac7acba1c8f200ca42f1c` |
| w-d02defa15df09c11cddc88b3 | PASS | 752 | 5 | `d1e4e5ca70ce0e7f2cdd83ba262c2d7639b08d293d68cbf9084a636c0995bc82` |
| w-d1d21a7c23263ed37e04812c | PASS | 752 | 5 | `6b17def63d506f0e24d7d6814efbbd4c172b2b79bd20ebfdc895bf1c748cae49` |
| w-e7b60f39fc82f7e4adf42d24 | PASS | 752 | 5 | `cfdbad681493c646aba20d9a986790e43082b70aaf786dc0db604e6ed204f88f` |
| w-edfab7761577354a5e15c02a | PASS | 752 | 5 | `5dd80c1e9fe97a3278015ec9b52f40d2d8c4787d2baceb2e568cc5837440cd00` |

其余文件字节hash、完整依赖、模型及private证据索引见[Run Manifest](p2/evidence/P2_RUN_MANIFEST.json)、
[命令摘要](p2/evidence/COMMAND_SUMMARY_PUBLIC.json)、[归档身份](p2/evidence/ARCHIVE_MANIFEST.json)。

| 文件身份 | SHA256 |
|---|---|
| 执行配置 | `6dd0a646cfe75987059bd97d78a16a03cb77b3b93e5c269860ff0b60ab308e27` |
| P2 Run Manifest | `3d8e614ea889412ddf476aec3a849d1823ed2bc18957688cc114cf9d30c3a540` |
| 原始输出seal | `4e11d89cb6f03291c124aab28f7181622b6766cc63d55be45126023147988c52` |
| 私有证据索引 | `355bd3a85c2eab3cac75c8571d89eb00e8c25df4bdbabf373d09a6e9e91d2be1` |
| 主要私有归档 | `505d3c55bf77589773b18ec500d2d83e6d0380d111d09d339adaa544a5d5aec8` |

主要归档64,841,526字节，保留实际run、输出、索引、命令与原卡V1；后到的卡V2纯呈现补记单独归档。

收口日期：2026-11-05 JST。2026-11-04授权、冻结run-id及原始日志时间均保留，不因跨日改名或重写。
