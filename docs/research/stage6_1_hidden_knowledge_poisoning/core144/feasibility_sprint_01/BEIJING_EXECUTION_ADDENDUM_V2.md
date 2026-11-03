# 北京接入与费用补充合同 V2

2026-11-03；PAPER1-FEASIBILITY-SPRINT-01；基线69899e2。仅改变Owner实际接入和计价适配，不改变模型、prompt、parser、证书、六槽、路由、输入、指标或GO规则。

Owner选择中国区域，提供cn-beijing官方业务空间Host（ws前缀），并明确回复“确认，许可及保密要求允许本次处理”。Key在用户环境变量中存在，进程原环境不存在；只为运行子进程读取，不打印/保存Key。
官方域名通式为{WorkspaceId}.cn-beijing.maas.aliyuncs.com，不能把示例llm前缀误当唯一合法前缀。验证ws/llm格式、TLS、区域及完整域名后缀，拒绝伪造子域/重定向。
原精确模型qwen3.7-plus-2026-05-26不变；北京该历史模型按中国内地部署资料核对；不将北京入口写成东京Global。
[北京官方说明](https://help.aliyun.com/zh/model-studio/beijing-access-information)；[价格](https://help.aliyun.com/zh/model-studio/model-pricing)：<=256K输入2元/百万、输出8元/百万；不假设免费额/折扣，不跨层套价。
[中国站隐私](https://help.aliyun.com/zh/model-studio/privacy-notice)说明调用数据会按相关协议存储，不将国际站默认30天条款自动套入中国账号。
[服务协议](https://terms.alicdn.com/legal-agreement/terms/common_platform_service/20230728213935489/20230728213935489.html)作为本次中国站条款来源；无训练、转售或输出蒸馏，本轮只受限事实核验。

## 人民币原币记账和美元预算上界

receipt同时保存原币CNY估算与保守USD预算上界。预算采用固定保守界1USD=6CNY，**不是声称即期汇率为6**。
[中国银行当日牌价](https://www.boc.cn/sourcedb/whpj/index_2.html)2026-11-03美元报价高于6元/美元；取更低分母使预算USD上界偏高。
因此24元预警、已估算+待结算+下一请求最坏达到27元硬停，对应4.00/4.50保守USD；不扩张原小于5美元合同。
真实CNY费用依据usage估算，最终账单未对账仍未知；原币记录不能误称实际美元账单。所有Run/探测共用原任务账本。

## 执行序列

先合成与静态回归、提交并推送，再单次纯虚构JSON探测；成功需精确模型ID、非Thinking、usage完整、正常结束。
不支持精确版本/关闭Thinking、HTTP/网络错误、usage缺失或预算/身份异常即停止，保留预留与失败，不重试或换模。
成功后只更新Git外配置中的probe receipt hash；同一固定D1输入、E1-E4全部运行，沿用共享组件设计。所有预测封存后才独立读取评价标签。
E4事前选择启用，预算可在任意下一请求前硬停；中途不能为分数删改条件。任何部分输出不冒充完整D1结果。
本补充说明并不宣称探测或D1已成功；执行事实由后续原件/结果追加。
