# 官方API资料核验 V1

核验日期2026-11-03 JST；仅访问官方公开资料，无账号登录、模型调用或D1外传。

| 事项 | 来源派生事实 / 剩余核验 |
| --- | --- |
| 精确版本 | [模型资料](https://www.alibabacloud.com/help/en/model-studio/qwen3-7-plus)列出qwen3.7-plus与2026-05-26快照关系；本轮只用精确快照ID。文档存在不证明账号可调用 |
| 上下文 | 同页列context1000000、max input991808、max output131072；本轮主动只使用<=256000输入计价层，输出最多4096 |
| 单价 | [官方价格](https://www.alibabacloud.com/help/en/model-studio/model-pricing)东京Global精确快照：<=256K输入$0.276/M、输出$1.101/M；高层$0.826/$3.301。Japan部署对应$0.4/$1.6、高层$1.2/$4.8。不套别名优惠/缓存/免费额 |
| 地区 | [地区说明](https://www.alibabacloud.com/help/en/model-studio/regions)区分接入/存储地与推理scope。Owner批准Global；实际账号地区仍UNKNOWN |
| 东京端点 | [东京说明](https://www.alibabacloud.com/help/en/model-studio/japan-tokyo-global)只支持工作区专属端点，Global可能在境内外节点推理；scope由工作区决定。不能仅看东京域名就断言Japan-only |
| 隐私 | [官方隐私页](https://docs.modelstudio.console.alibabacloud.com/en/model-studio/privacy-notice)承诺不将用户数据用于训练，并说明调用数据存储受相关条款约束。不是零保留保证 |
| 保留 | [数据保留政策](https://www.alibabacloud.com/help/en/model-studio/data-retention-policy)默认推理prompt/response通常不超过30天，法律或服务安全有例外；有状态数据直至删除。ZDR须工作区开通及模型覆盖，不能假定当前账号已启用 |
| 参数 | [Chat API](https://www.alibabacloud.com/help/en/model-studio/qwen-api-via-openai-chat-completions)支持JSON、temperature、max_completion_tokens和enable_thinking；最多10token的输出计数偏差额外预算 |
| Thinking | [Thinking资料](https://www.alibabacloud.com/help/en/model-studio/deep-thinking)将精确Plus列为默认开启的混合模式，支持false；[错误说明](https://docs.modelstudio.console.alibabacloud.com/en/model-studio/error-code)另有不能关闭的场景说明。以本账号纯虚构探测为最终工程门，不自动变为Thinking |

当日重新核验精确账号/地区定价再运行；代码只接收官方TLS工作区端点、禁重定向/代理/搜索/tools，默认不发送任何数据。
`temperature=0`并不保证远程服务跨时间位级确定性；共享组件输出用于减少采样差异，但不能宣称整个API确定性已证。

## Owner已批准与未补全项

2026-11-03 Owner明确选择“批准外传；允许Global范围”。对应D1候选与Top5，不含角色/S/GT/预期答案/仲裁信息。
这项批准已记录，不再重复请求。同一次回复未注明实际账号区域/工作区，也没有提供可核验的许可/保密确认；本地DASHSCOPE_API_KEY和ALIBABA_CLOUD_API_KEY均未配置（仅检查是否存在，未读取/打印值）。
所缺不是新增GPU或模型授权；只需实际区域/工作区端点、许可/保密允许此处理的确认及本机安全配置Key。
这些未补全前继续本地工程，暂停所有付费请求，包括接口探测。
