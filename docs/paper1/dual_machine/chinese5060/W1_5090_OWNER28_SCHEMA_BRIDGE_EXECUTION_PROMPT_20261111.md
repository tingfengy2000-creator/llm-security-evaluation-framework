# 5090 Cursor｜Owner28 已封存独立盲测包的无损格式桥接

**任务性质**：纯机械转换，不是重新采集、重出题、生成样本、改标签或评分。根据Owner28原授权执行，必须先读`docs/paper1/dual_machine/OWNER28_5090_TO_5060_SCHEMA_BRIDGE_AND_ONE_SHOT_HANDOFF_20261111.md`全文，严格以该文件为准。该文件已在5060分支，使用`git fetch origin`和`git show origin/research/paper1-chinese-defense-5060:docs/paper1/dual_machine/OWNER28_5090_TO_5060_SCHEMA_BRIDGE_AND_ONE_SHOT_HANDOFF_20261111.md`只读取得；本机继续仅在`research/paper1-ragdefender-repro-5090`操作，绝不merge/checkout污染DEV。

**锁定输入**：本机先校验Git HEAD含`a8de64fbf2c279a642c9b9a41ddf5c5481b8cfca`；原始`EVAL_ROLE_FREE.json`预期SHA256 `2aafd7d7bcd8e3860771063a31770e350532065abb251f38f99c7ac39ba50cb7`，原始`EVAL_CURATOR_MANIFEST.json`预期`9b9c40e3053003dd237aa26414c53f7465822265faa026f9565de43221f07814`，原私有Gold SHA `c4244e86fb2ecf1177cc3d2bb39b8791e1b789713fc3522bbfaa46b35b055595`。任何不匹配STOP。旧文件原样保留。

**实施步骤**：
1. 按冻结在5090私有托管的分区关系明确原39个world中原32 main、7 mirror。只将32 main**无损**映射到符合5060固定Validator的`OWNER28_ROLE_FREE_V1`：`{schema_version,main,mirrors:[]}`；4个`f-24hex`事实组、每组恰8个main，4个world字段`{world_id,fact_uid,event_date,query_text,documents}`之外还有documents数组。每world 11文档，每文档恰`{document_id,source_id,text,content_sha256,source_uri}`。所有文档`text`与旧数组逐字符、顺序完全相同；`query_text`与原`query`完全相同，勿加日期/提示/答案。日期由已封存query brief给出并和问句实际时点核验。ID依固定公开hash模式确定，不能将正确值、role、S1-S8用于生成ID；检查全局碰撞。因原包没有可信真实签发来源ID，`source_id`只是不具备独立性语义的opaque占位；`source_uri=null`，不把自己改写的文本冒充官文原文。
2. 7个镜像保存在旧包且`MIRROR7_NOT_RUN_NOT_IN_HEADLINE`，不补第8个、不把7个混进main，不宣称时间镜像测试已经执行。
3. 创建精确Schema`OWNER28_CURATOR_V1`的公用兼容manifest，四条`source_audits`来自私有真实来源核对，仅列官方URL、法条定位、生效/适用和权利状态，禁止正确值、角色和差分内容。新文件`role_free_sha256`绑定兼容包；旧私有Gold SHA不变，`main_worlds=32,mirror_worlds=0`明确仅指此次传给5060的科学批次。所有原始对应关系保存5090私有，随后评分使用。
4. 提供独立`EVAL_COMPAT_BRIDGE_AUDIT.json`注明原新SHA、原39=32+7、导入32主世界、每世界11、总352段、加入0/删除0/内容变更0/问句变更0、2类签发机构/≥2新谱系、日期信息来源、所有新增字段定义、移除镜像情况和字节级比较/回读命令与退出码。不可把私有标签正文或真值放入Git；若需要映射ID用于评价，只存5090私有文件并记录独立SHA。
5. 使用纯标准库做schema和迁移无损测试（参照Owner28公开协议），不运行RD、重检索、Qwen、生成模型、非独立评分。若原来源URL不符合严格`.gov.cn`、old/new生效区间/多源等冻结门，报告准确STOP字段，不伪造数据满足Validator。
6. 三件兼容新文档仅推送5090独立分支，回传新commit、三文件sha256、原sha、桥接正确性报告。`SCHEMA_BRIDGE_READY / EVAL_NOT_RUN`后停止评分，等5060全量预测hash封存。

**不可越线**：不能读5060 DEV score/role mask/失败案例，不能变更原样本/Query/事实组/旧label SHA，不能将5090私有标签放公开Git。Claim1–3维持NOT_RUN、D2/D3/HOLD8锁定、费用/模型下载均为0。