# Paper1｜Owner24 一次打包、条件自动推进：本地模型加载→抽取开发→新合成可行性→D1离线过滤诊断

**决策ID**：`W1-OD-20261110-5060-FASTTRACK-CONDITIONAL-24`  
**日期**：2026-11-10 JST  
**Status**：`OWNER_SCOPE_EXPANSION / BOUNDED_CONDITIONAL_AUTO_CONTINUE / AUTHORIZED_BUT_NOT_EXECUTED`  
**唯一分支**：`research/paper1-chinese-defense-5060`  
**执行前remote HEAD**：`97ca11445fabfe898b797c72abef15995377835f`  
**Owner原话**：“能不能一次让5060多做点任务 放宽限制，我现在真的很急，很急我这个论文的研究路线”。该请求改变过去单门审批策略，授权给5060一个**四阶段、数值上限冻结、条件自动续行**的本机研究可行性执行包。对未明确说明的实验资源一律取保守限制；对研究重大修改、D2/D3、生产/外部API不扩权。本决策是Owner在已知前次Owner23A状态下提出的最新明确加速指令；不得把“放宽限制”泛化为无边界代理权限。

## 12-field PO-MHEP

1. **Issue ID**：`W1-OD-20261110-5060-FASTTRACK-CONDITIONAL-24`。
2. **Issue**：前期在Rule-only中文抽取、模型资产与PE环境上耗时，但尚无完整RAG知识污染防御正向证据。把模型运行前检查、最小推理、已暴露数据开发对照、单次暂定新数据验证与有限D1离线检索后过滤诊断合并，由5060在明确守卫下自动推进，最大化同一轮可行性信息。
3. **Discovery**：Owner23A本机静态审计 `W1-5060-OWNER23A-SCOPED-STATIC-20261110-01` 完成，CLI静态2911/2911导入符号、API-set73/73 PASS；Qwen GGUF和llama.cpp ZIP字节/SHA PASS。VC最低版本、动态CPU后端和整包notices UNKNOWN；Owner20暴露73高分但新100规则`FEASIBILITY_NO_GO`；完全不同的神经抽取与真正D1过滤收益未验证。
4. **Observed / inference / unknown**：
   - `OBSERVED` 固定权重 `Qwen/Qwen2.5-1.5B-Instruct-GGUF@91cad51170dc346986eccefdc2dd33a9da36ead9` `qwen2.5-1.5b-instruct-q4_k_m.gguf` 1,117,320,736B SHA256`6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e`；固定Windows CPU `llama.cpp b12242` ZIP 24,931,401B SHA256`4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0`；Owner23A符号检查通过，RAM实际峰值未知；许可证源码MIT/模型Apache2/LLVM OpenMP已部分核查，整包notice覆盖UNKNOWN。
   - `SOURCE_DERIVED` 固定`b12242` 的`tools/cli/cli-context.cpp` + `cli-server.h`显示`llama-cli.exe`会启动内嵌HTTP服务线程及127.0.0.1健康检查，**不能视为无套接字纯加载入口**；固定`common/common.cpp`提供`common_init_from_params(params, model_only=true)`，会在模型载入后退出，避免context及warmup，但没有已证明的现成EXE映射；`tools/completion/completion.cpp`经`common_init_from_params(params)`包含上下文及可能warmup，`--no-warmup`与`-n 1`虽受固定`common/arg.cpp`支持但不等于纯加载。
   - `INFERENCE` 优先使用固定release已解包`llama-completion.exe`进行**明确允许1 token的工程smoke**，比坚持不可证明的“零解码”入口更快且行为诚实；Qwen+确定性span verifier有机会弥补规则结构脆弱，但不保证安全或达到门槛。
   - `UNKNOWN` 本机进程内存/加载/CPU模块选择、低比特权重的query/scope抽取、现成EXE是否完全没有额外网络行为、未见合成数据表现、P0下D1污染过滤收益。
5. **Prior commitments inherited**：历史S1 FAIL、R2 K1-C、Owner20 RULE`FEASIBILITY_NO_GO`不可改；D1为`DEV_EXPOSED`，旧73+100+20均为已暴露开发/诊断，D2/D3始终完全隔离；P0必须有独立可信来源才能升权，模型抽值不可替代来源验证；ASR/AnswerAccuracy正式未测，HumanGold=0；不得动5090 Meta Llama2 Claims、主研究分支merge或正式S2–S5。旧PO-MHEP Owner需批准新科学路线/正式数据解封等原则不被废止，本条仅明确预批四个有界阶段。
6. **Why now**：研究核心是中文RAG知识污染防御而非Windows PE供应链；继续拆分许可/静态门会阻断最关键的抽取器和检索后处理效果判定。该包一次给出可证事实与失败停止，成本0新增模型/API/权重。
7. **Downstream risks**：模型错误事实与span幻觉；Q4小模型能力不足；本机DLL动态加载和内存波动；B12242 CLI本机HTTP嵌套服务可能对外暴露；同Agent生成新数据构成弱独立；在D1已有标签上后验开发不能作为独立收益；非法再分发许可证；真实未证修订可能触发P0幻觉式升级。
8. **Options**：A `OWNER FASTTRACK CHOSEN` 条件多阶段本地研究包；B继续逐门审批（低风险但难及时得到科研结论）；C放开D2/D3/商业API或无界自动运行（不可接受，明确拒绝）。授权A使用可停止状态机与固定上限。
9. **LOCAL recommendation**：执行A。阶段`F0`无模型源/资产/入口与数据准备；`F1`一次CPU本地极小生成smoke（不伪装零解码）；`F2`旧73+100+20上固定小规模模型抽取迭代及完整开发统计；`F3`仅当开发安全性门通过，用新且不与旧集重合的60主语义(40可答/20应拒识)+10配对进行一次封存后评分的暂定评估；`F4`条件满足才在D1原离线TopK既有快照进行12或至多36世界的检索后过滤诊断，基线相同输入，不触检索器/生成API。
10. **Confidence & reversibility**：资产/静态导入证据高，Qwen能否有效提取/最终防御收益未知。整包分发许可证UNKNOWN仅允许本机受控内部非发布试验，禁止再分发；不能自动等于已完全许可。所有F1–F4科学预测、数据与评分脚本freeze/sha，若安全及数据漏出即STOP。
11. **Owner approved staged scope**：
    - `F0_STATIC_AND_NEW_PROVISIONAL_SEAL=APPROVED`；
    - `F1_SINGLE_CPU_ENGINEERING_SMOKE_WITH_1_TOKEN=APPROVED_CONDITIONAL`：对固定本地现有`llama-completion.exe`与模型各一次内部工程加载/最多1 token生成；这不代表`load-only`，也不算科学试次；
    - `F2_BOUNDED_LOCAL_MODEL_DEVELOPMENT=APPROVED_CONDITIONAL`：可用旧73与已揭盲Owner20主100+20；两轮候选Prompt/schema调试上限、最多1次冻结全量193视图开发对照；只运行单模型，严格source span/verifier；
    - `F3_NEW_SYNTHETIC_PROVISIONAL_ONE_SHOT=APPROVED_CONDITIONAL`：60新语义事实(40可答/20拒识)+10从属视图，预封存、单次盲评，Agent暂定Gold不得叫HumanGold；不得用旧数据当新主集；
    - `F4_D1_EXPOSED_OFFLINE_FILTER_DIAGNOSTIC=APPROVED_CONDITIONAL`：仅D1已有许可快照，最多36检索世界/每世界原TopK5、无新检索/生成，比较Poison过滤与Clean/HN误删，标开发诊断，不声称正式ASR；
    - 阶段间符合硬守卫即可`AUTO_CONTINUE_WITHIN_BUNDLE=YES`，不用逐阶段再次询问Owner。
    - `NEW_MODEL/DEPENDENCY_DOWNLOAD_OR_INSTALL=NO`；`EXTERNAL_LLM/API/PAID_CALL=NO`；`D2/D3=LOCKED`；`5090_CLAIMS=LOCKED`；`S2-S5_FORMAL=LOCKED`；`HUMAN_GOLD_SIGNING=NO`；`MAIN_MERGE=NO`。
12. **Specific quantitative boundaries, STOP and evidence**：
    - **F0** Git和旧文件SHA与D盘权限/缓存核查，机器需可用内存+可用commit均≥8GiB、D盘剩余≥10GiB，原未知宽ACL目录不得装模型/私有新数据；仅本次工作D盘自建ACL最小化。运行时PE静态检查对`llama-completion.exe`及必要依赖完整PASS；且其固定源码和参数表可证`--no-warmup`、`-n 1`、`-ngl 0`、`-c 512`。不能给llama-cli默认server发“完全离线无套接字”授权。F0使用纯合成、无私有文本，F3新暂定案例如果创建须在F2抽取/调参前生成并封存源事实/输入/GOLD分离/accepted span并声明`NOT_INDEPENDENT_AUTHOR`。
    - **F1** 单次工程smoke，Windows Job Object limit process private commit **≤6 GiB**，墙钟≤180秒，单进程1模型；CPU-only `-ngl 0 --device none -c 512 --no-warmup -n 1`、固定无害系统合成测试文本，0私有/旧样本输入。**出站默认拒绝、禁止外网**；采用可核可撤的进程级防火墙或隔离执行区，不能证实无外网时STOP；可接受本机loopback仅若采用CLI且事前证明并隔离，但本次应优先completion不创建server。模型/EXE/DLL SHA预核、保护线程和模块列表、加载返回/1 token最多、峰值PrivateBytes/working set、CPU后端、exit、网络监测与文件改动全留证。失败**不得重复这一smoke**；如果只有非执行性启动器BUG，可修复后提交另下一批审批而不是自动第二次科学或工程加载。
    - **F2** 只有F1模型正常加载并无外网/异常且峰值<6GiB可推进；旧73+原100主+20从属共193条视图，都是DEV_EXPOSED。先从旧数据固定选择≤18视图作为Pilot，最多**两套Prompt/Schema版本**（第一套与一次修订），修正抽取适配器、JSON/严格原文span/作用域/UNKNOWN分类；不得修改Gold或Rule-V1/V2历史结果。优先使用本地已核权重通过离线一次一输入的有界推理；每条`ctx<=2048, new_tokens<=192, batch=1, threads<=8`，单条≤120秒、阶段总运行≤3小时，Job memory cap≤6GiB；若30%+程序错误/漏能绑定请STOP，错误源/未证修订不得悄然升权。只有格式/证据span校验开发单测通过，才对193视图以**同一冻结版本**最多1次全量回放并报告全部正负/拒识/跨版本/scope/延迟/内存。开发结果不是独立指标，不能声称GO。
    - **F3** 新60个独立**语义案例**（40 ANSWER/20 UNKNOWN）+10从属问句提前于F2执行前封存，至少4主题域与10来源家族，生成source-truth→evidence→query→accepted span，并校验与旧73/100/D1已暴露数据的合规近重复，无D2/D3触及；同Agent生成标`AGENT_GENERATED_PROVISIONAL / NOT_INDEPENDENT_AUTHOR / HumanGold=0`。必须先冻结模型prompt/config/verifier和输入、Gold两个封存SHA；一次执行70视图后role-free seal，Evaluator后揭盲。**F3触发门**：F2既有暴露开发案例主分母ValueHit/answerable≥60%，wrong/decided≤10%，`unsupported revision/cross-scope accepted=0`，且actual no-network/CPU/资源/P0守卫PASS。该门仅是“是否值得耗用一次暂定holdout”的操作门，**不是修改原论文≥90%/≤2%科学验收门**。F3报告正式历史科学参考门值命中≥36/40、错抽/decided≤2%，各项Wilson95、strict span/scope、20应拒识误答、10从属单列。若F3失败但已有一些价值仍维持`PROVISIONAL_NO_GO`，不可后验改Goal或复用该集作为未见测试。
    - **F4** 若F3满足≥90%和≤2%点估计门且无未证修订/跨scope升权，则一次性对原D1封存TopK做最多36世界完整离线`B2/RD-zh vs candidate + verifier`检索后过滤诊断；若F3至少有≥25/40值命中、wrong/decided≤10%且上述安全守卫PASS（但未达正式门），仅允许**最多12个预冻结、平衡Poison/Clean/HN的D1世界**作为开发异常诊断。若更差则不运行F4，结束并直接提出下一架构（例如外部source version index+跨证据核验）改进裁决。D1不新检索、不允许改TopK、Role、原Truth/Gold或生成，Poison召回、Clean/HN误删及用量必须分别评价，`RAG_ASR/FINAL_ACCURACY=NOT_MEASURED`，不得将这批称正式S2。
    - **Hard STOP**：SHA/许可底线不合、无联网隔离、资源不够/用量越界、超时、warmup/网络泄漏、C盘新缓存、模型加载错误与自动重试、Gold漏入prompt、需要新模型/权重/运行时或pip安装、D2/D3访问、API收费、模型错误导致未证版本升权、下游指标严重退化或违反既有PO-MHEP。一旦STOP，按已经完成阶段提交真实报告、保留失败，不得为了“快”静默再试。
    - **Final evidence**：每个阶段子Run ID、输入/源码/模型/运行参数SHA与受控D盘证据、真实下载/费用/模型调用计数、CPU/内存/网络/错误时序、F2全193开发与F3 60+10一次性评估及条件F4统计、与RAGDefender B2/RD-zh公平限定对照、Owner决策风险卡、Git提交推送/远端核验。用户无需另批准上述四阶段，但**不得**自动进入正式S2–S5、D2/D3或外部模型API。

**接续规则**：F0通过→F1通过→F2开发门通过→F3暂定门→F4有界D1诊断，任一失败依预注册STOP；不把任务完成数量、工程PASS或同Agent合成分数当论文科研贡献。收口 `OWNER24_FASTTRACK_COMPLETE_OR_STOP / FORMAL_S2_S5_LOCKED / AUTO_CONTINUE=NO_OUTSIDE_BUNDLE`。
