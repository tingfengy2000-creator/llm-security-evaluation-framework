# 内部矛盾证书 V1

状态`PROPOSED / EXPERIMENTAL`；适用于所有候选，不读真实S分层。

API仅接收Candidate，不见Top5或标签。输出两个有原文span和六槽的冲突原子；无证书继续外证，绝不能SUPPORT。
代码独立检查：两个不同且逐字可定位Candidate span；subject/predicate/scope/time/source_role同值且已知；subject/predicate及显式scope/time必须PRESENT。
槽位PRESENT值必须能在其span找到；UNKNOWN/INSUFFICIENT不能充当相同零值；NA必须两边一致，不能代替显式scope/time。
接受的互斥只含：原文值X与不X，或显式“固定为/等于/恰为/唯一为”的同单位不同精确数值。
至少、至多、上下界、可能、例外、或、引述/声称/错误观点及不同对象/条件/有效期不发证书。
单位不同不自动换算；别称/隐含相同区间不能凭空补齐；未覆盖是NO_INTERNAL_CERTIFICATE，不代表Candidate事实正确。
证书名称只表示通过此有限机器合同，不是人工gold或普遍语义正确性的证明。

A0原规则历史12/12的词面线索只用于诊断理解；当前实现直接要求模型提出有锚的关系，不用旧规则结果作真值或门。
运行保留raw_model_verdict、certificate_status、final_verdict及全部原子，证据不足不删除原判断。
合成验证含同域真互斥、同一关键词但不互斥、至少/至多、不同主体/时间/条件、单位差异和引述错误观点。
