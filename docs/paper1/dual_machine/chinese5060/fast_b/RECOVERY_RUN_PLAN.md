# Fast B恢复执行事前冻结（2026-11-05 JST）

控制面98228e202062b1216094acac90f83be29cc63074；run W1-5060-FAST-B-20261105-RECOVERY01。
FAST-B-04/RESOURCE-REPRO-05与恢复合同共同范围；旧14d718f checkpoint全部保留。

FORWARD_RISK_REVIEW / PAPER_RISK_REVIEW：固定原36 TopK字节，不重新检索；仅单变量embedding、原库未改、
single_hop/p2/m5。独立Evaluator在全输出封存后才能读标签；未召回、部分删除和完整删除分开。
原样库结果不等于ACSAC artifacts复现，不将B2迁移作创新或D1开发作泛化；HumanGold0，ASR/QA未测。
若源码/模型/许可/流量/缓存/参数/原始证据任何门失败，立即停止该支路；无重试、替代源或自动回退。

事前资源：D盘新增峰值2GiB（B1权重100MiB、B2既有资产只读或逐hash复制至D至500MiB、临时512MiB、
新日志/证据/归档512MiB及余量），至少20GiB安全空闲，CPU2、RAM预计6GiB、墙钟1800秒；无GPU。
当前D约311GiB空闲。原生Windows；不启动WSL/Docker/conda，不创建VHDX；既有C环境只读，不迁移/删除。
新代码、缓存、TEMP/TMP、HF/Xet/ST/Torch、bytecode（禁写）、日志和归档一律D；不承诺OS自身零C写入。

网络仅批准模型固定revision的官方HF元数据和必要文件，不发项目文本。直接HTTPS、禁环境代理、无自动重试；
每次请求持久记录status/header/body字节、redirect链；每请求额外预留1MiB保守传输开销，
实际累计响应正文/头加预留不得超过262144000字节。metadata正文最多1MiB；文件size必须先由官方tree核对，
仅model.safetensors及必需配置/tokenizer/Pooling、模型卡/许可；不whole-repo snapshot、不重复权重、无依赖下载。
元数据/重定向/失败响应也累计计量；中断或未知身份停止，不换源。下载后离线加载身份核验，再冻结实际资产清单。
完成或受阻均保存argv/cwd/time/stdout/stderr/exit、模型/输入/输出hash及私有归档，自己分支提交推送后STOP。
