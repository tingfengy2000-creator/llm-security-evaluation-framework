# Owner A：逐条截断记未决，复用原件继续 V3

2026-11-03；Task PAPER1-FEASIBILITY-SPRINT-01；PODR-157。
Owner原话：“批准a，如果是这个阿里云的api调用 可以提高预算到15美金”。
此授权只覆盖既定阿里云精确模型的方案A与总预算，不授权换模/提示调参/数据修改或追加实验。

## 原件与修订边界

Attempt01执行dbc4cc1；52完整包，第53条internal正常返回、direct length/1024后硬停；原HARD_STOP、52包、159请求和709文件索引/归档保持不可变。
原归档SHA34680b4cdb7e4c90a46942f2cea7b1bebec23f73a680342270a43ee0d579481b，索引SHA9055fca39ddc455e1df7f6e6d5ff989bcc8e94e0068055c1f2c0f50f3d096ffa。
新Run为D1-DEV-BEIJING-CONT-A01，完全独立目录；启动前核验全部709个原件、归档、同一120F5字节、prompt/槽位/引用parser/评价器身份，真实标签仍不打开。
前52包逐字节复制并锁定SHA；不重新解析或覆盖原判决。第53条两次已付费请求按完整request-body SHA、模型ID及response/receipt哈希绑定后复用，不再次请求。
恢复缓存只属于第53个候选，完成该包即停用；相同正文的其他候选仍按原实验单元执行，不将缓存扩成新算法。

## 唯一输出处理变化

Owner批准后，finish_reason=length成为逐条输出失败而非整轮异常：保留原始响应、usage、正常可解析的raw_model_verdict，final_verdict强制INSUFFICIENT、parser_status=OUTPUT_LIMIT。
不补全截断JSON，不从理由猜判决，不改写原文；内部截断没有证书，继续外证；结构化截断不触发付费缺口修复。
所有组件同样处理length，不重试、不提高上限。direct1024/internal2048/structured与followup4096、全部prompt、模型、证书、六槽、路由、Top5及评价定义都不变。
HTTP/身份/非Thinking/usage/预算/原件异常仍整轮停止，不成为普通未决。旧Attempt01保持原门失败，不追溯改成成功。

## 阿里云任务总预算

Owner将同一任务阿里云API总额提高到USD15。LOCAL保留0.50未结算缓冲，预警USD14.00，硬停为已估算+待结算+下一请求最坏达到USD14.50。
沿用6CNY/USD保守预算界（不是即期汇率），对应CNY84预警/87硬停；已有3.264570CNY必须累计，不因新Run、复用或配置改名归零。
原币2/8元每百万token计价不变，usage估算与最终账单分开；免费额/缓存折扣不用于放宽门。
只允许PODR-157配置明确指定这组预算；旧配置继续适用旧4/4.5美元门，不静默改写历史。
原七天窗口、单请求串行、无自动重试和无第二服务商不变；本次不因额度增加追加实验或重复已完成预测。

## 封存与评价

新CONFIG_LOCK绑定当前源码/合同、旧原件锚与配置、同输入、模型与prompt。复用部分的不同执行来源必须披露，不宣称480条都是新增请求。
全部120×4条件的预测锁和raw索引完成后才打开评价标签；每个条件分母仍120，总Poison40/S1-S3为12/15/13、S2S3为28、Clean/HN各40。
截断与JSON/引用失败不从分母删除。真实物理费用按不可变call_id去重，各条件逻辑成本包括其使用的全部组件。
继续使用原GO/CONDITIONAL/NO-GO计数门与2000次家族配对bootstrap；不提高输出长度、不改提示、不按分数挑条件。

## FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW

这是在真实标签未打开、未评分时因工程长度门作的公开修订，不是原协议无偏完成。必须同时披露失败Attempt01与Continuation。
复制前缀、复用请求和费用归属可能错绑，故做原件哈希、逐ID/输入SHA、缓存完整性、无重推/无覆写及物理call_id冲突检查。
工程继续获批不等于新方法科学接受；D1_DEV_EXPOSED、D2D3隔离、L0历史、正式实验与泛化边界保持。
