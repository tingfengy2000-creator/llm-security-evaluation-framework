# 中文事实关系核验 V1

状态`PROPOSED / EXPERIMENTAL`；不改变旧L0的prompt/parser。

六槽为subject/predicate/value_unit/scope_condition/time_version/source_role。
每项有PRESENT/NOT_APPLICABLE/UNKNOWN/INSUFFICIENT，后三种值为空，不转成零/SAFE；PRESENT是对应原文span中的实际短语。
Candidate和Evidence原子均保存UID与连续逐字span。关系显式连接Candidate原子至外证原子，可一对多，不由来源host推断制定机关。
匹配subject/predicate/scope/time/source_role后接受模型的SUPPORT/CONTRADICT关系；数值不同不是自动反证。没有对齐/存在缺口则未决。
SUPPORT还要求模型声明全部重要断言已抽取、每个Candidate原子都有有效外证支持且无冲突/缺口。
外部CONTRADICT至少一条有绑定的反证且无未解义务；保留全部合法更新/历史版本/角色区别。
格式/引用失败为INSUFFICIENT，raw判决不覆盖；补查不会修JSON或重试错引文。

按需模块：当首次结构化核验为未决、parser通过且missing_obligations包含scope_condition/time_version/source_role/joint_evidence时，最多一次同Top5补查。
补查只收到原Candidate、原Top5和实际缺口名，不见先前标签、Oracle映射、参考答案或错误案例反馈。
无新检索、无扩池、无多Agent、无训练/下载。第二次仍未决就停止；旧输出和新增成本一起保留。
E3/E4对同一Candidate完全共享结构化组件与补查，区别只有E3是否内部证书早退。

局限：模型声明的语义关系与coverage_complete不是独立事实证明；别称归一化、隐含日期和跨span关系可能被保守拒绝。
合成合同通过仅说明程序边界；只有实际D1同骨干配对结果才能判断可行性，之后仍需未暴露数据验证。
参考[FactCG原论文](https://aclanthology.org/2025.naacl-long.258/)，仅借鉴多跳关系表示；不下载其模型/训练数据，不引入GNN，不称复现。
