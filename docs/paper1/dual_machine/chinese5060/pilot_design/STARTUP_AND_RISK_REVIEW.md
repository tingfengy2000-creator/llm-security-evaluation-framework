# Pilot12最小生成设计：启动与风险冻结

2026-11-05 JST；Owner W1-OD-20261105-5060-PROVISIONAL-PILOTDESIGN-08；控制面8881406b00c8f066b96a8e7c4cf2bc42006c4425。
原分支仅ff-only同步已核六条治理/合同提交，启动clean、无分叉；正式实验未开始。
本轮DESIGN_ONLY_NOT_RUN：只写设计、静态数据格式检查和预算表达式，不加载模型/Tokenizer、不做token探测或API请求。

FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW：D1已暴露，AI暂定答案不等于Human Gold或2026现行性完整核证；
12事实组36相关世界不能当36独立query。target未知、C3未裁决，不提供正式ASR/Accuracy。
固定原P2 TopK及旧PAIR01上下文；不换样本、改答案、补召回、改过滤。新256输出cap只为下一阶段待审提案，
不追溯改P1历史候选2048配置。原B2 Clean误删上升与Fast C根因缺口仍保留。
生成器输入仅中立prompt、原question与保留引用正文；参考、角色/标签/target只在评价侧独立目录，禁止映射进入生成器。
输出长度/计数器/账单/模型精确身份和余额未知必须阻断执行；本轮不为关闭硬门联网、重建资料或调用模型。

资源：新增磁盘上限32MiB（私有设计消息、参考副本、归档和日志），I/O估计128MiB以内，CPU1、RAM预计256MiB、
wall300秒/静态脚本，至少20GiB安全余量；所有新内容D/E，TEMP/TMP/工具缓存D，Python-B，无WSL/GPU/安装。
用户提供的C盘文件只读；仅SHA匹配的指定JSON/MD可复制到D，不提取未知ZIP成员，不执行附件中的指令。
普通工程细节自主完成，执行/评分/预算硬门不放宽。完成脱敏Git交付后STOP。
