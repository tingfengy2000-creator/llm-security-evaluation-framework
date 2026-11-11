# 5060 Codex｜Owner28独立评价验收后：科研论文级证据整理（非新科学授权）

**执行身份**：`SUPERVISOR_REVIEW_PREPARATION_ONLY / NO_NEW_SCIENCE_RUN / OWNER29_PENDING`。目前无需也不得重跑Owner27/28科学试次。首先fetch+ff-only，读`AGENTS.md`、上述监督复审文档`OWNER28_INDEPENDENT_SCORE_SUPERVISOR_REVIEW_20261111.md`，确认5090评分提交`670d9ab0e546d46117bf5c48ebb2b0043689f453`，只读引用其公开score报告和公开aggregates，**不**访问5090私有Gold。

1. 复核Owner27 DEV与Owner28独立EVAL在相同定义下的Poison retained、Clean/HN false deletion、retrieval miss，并制作可复算的两批对比表和三维主图，只按组级展示，不把32世界视为32独立事实组。检索失败与过滤失败分栏；Poison检测召回与RAG生成ASR严格分开。
2. 在仓库写`docs/paper1/dual_machine/chinese5060/BENCHMARK_V01_METHODS_AND_LIMITATIONS.md`，包括数据设计、4个评价事实来自3条未见谱系、进程级隔离、Agent provisional、32×TopK5、模型revision、B2/RD-zh差异、5/5的2个实际世界、DATE_ONLY的正则0/352和=NONE、原RAGDefender Claims仍未运行、例子是改写代理非真实网页、消融scope无贡献、可信收据混入真值侧信息。禁止稿件写“第一篇、首次、显著证明、通用防御可靠”等无据创新性主张。
3. 建立场景/错误类型 `S1-NO-POISON-CLEAN-LOSS`,`S3-SCOPE-SWAP-NOT_DETECTED`,`S5-NEAR_DUPLICATE_EASY`,`S6-PARAPHRASE_COLLUSION`,`S7-FORGED_VERSION`,`S8-5_OF_5_MINOR` 的失败图谱与适用领域。对四事实簇之间的相关性和同谱系依赖单独披露。
4. 给出未来最短论文质量关卡清单：原文许可和source provenance、至少2人独立Gold加1裁决、独立fact组扩大、真正有效的时间基线、生成层真实ASR/Accuracy/refusal、成本延迟和Original RAGDefender复现差异。为新实验写不包含未授权API调用的Owner29预注册**草案**，禁止作为已批准实验运行。
5. 仅作静态数值与文献比对；可运行无实验输入的table unit tests，但不运行新的真实防御试次、检索/模型、数据标注、评价计分、API或权重下载。仅在5060独立分支提交并更新必要Tracker的`PREP_ONLY`记录，回传文件/HEAD/SHA后STOP。

已经观测的Owner28主要数字：P B2=33/56 ZH=15/56；Clean误删B2=27/82 ZH=55/82；HN误删B2=7/20 ZH=10/20；ZH多删18P同时多删28Clean、3HN、1背景。公开报告和Manifest必须作为计算输入引用，不能擅改。
