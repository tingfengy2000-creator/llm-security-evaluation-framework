# Paper 1 — Owner存储边界与基线复现路线补充决策

Owner Decision ID: W1-OD-20261105-RESOURCE-REPRO-05
Date: 2026-11-05 JST
Authority: Owner在本次监督会话中的明确追加指令，脱敏转录。
Status: OWNER_CONFIRMED_RESOURCE_SCOPE_AND_REPRODUCTION_GOAL / CLAIM_EXECUTION_NOT_APPROVED
Applies prospectively to: 5060 Fast-Track B与5090 RAGDefender公开论文复现工作线；两个独立分支不合并。
Related authorization: W1-OD-20261105-FAST-B-04（原下载额度与B1/B2实验范围不变）。
Research repository: tingfengy2000-creator/llm-security-evaluation-framework
Before this supplement, latest verified 5060 remote state: c98e926a8021172dd9f45ed7dcd0a8294758851a.

## 1. Issue ID
W1-OD-20261105-RESOURCE-REPRO-05。

## 2. Issue name
调整D/E项目存储限制；使5090持续承担有用的受限复现准备；将RAGDefender主要公开可复现结果设为论文基线复现目标。

## 3. Discovery stage / task
5060 P2已真实完成36个T0检索世界、B1/B2待执行；5090已完成无权重离线Smoke、三个Artifact Claims尚未运行。

## 4. Facts, sources and uncertainty
OBSERVED_FACT (remote Git): 5060 P2报告在3ca27c9416ea630e7f82c5b98ceed93099bd57ac，T0 Candidate hit@5为29/36，B1/B2未运行；5090 Smoke记录在5def0ffc15b9fe0ea8d713c43489e5f07e965517，Claim1/2/3未运行。
SOURCE_DERIVED_FACT: 上游SecAI-Lab/RAGDefender@ba2a17efba165d45409114df2d70b030ade1e1b8的docs/reproducing-paper.md列出Claim1 PoisonedRAG、Claim2 Tan、Claim3 GARAG，用于Figure4与Figure5的部分开源模型实验；Table2/3/4/5/6/7/8覆盖度不同，部分依赖外部、手动计量或源码修改。上游文档还披露artifact的旧实现与论文公式有差异，量化环境与论文机型不同。
OWNER_CONFIRMED: 本轮Owner要求不在C盘新增项目内容、D/E盘存储空间可放宽、5090在其他任务阻断时继续有意义的工作、主要论文基线应尽量完整复现。
INFERENCE: 主Claims和适当的消融是论文公平性必需的优先路径，但并不因此获得模型许可或Claim执行批准。
UNKNOWN: 各设备实际系统/WSL/conda缓存位置、C盘是否有不可控操作系统写入、未来权重/语料许可、具体资源峰值与主要Claims实测数值。

## 5. Affected governance
AGENTS.md、PO-MHEP、双机独立分支与权限、数据/隐私/标签隔离、作者许可、原始环境与兼容环境双轨、P2历史输出不可变、每一阶段资源冻结和Owner审批门。新决定仅调整未来受控存储与计划优先级。

## 6. Why handle now
减少两台机器的无谓等待，避免受限的1GiB D/E本地存储约束意外阻碍合规归档；同时把基线论文复现从模糊愿景转换为可审查的分阶段覆盖计划，防止只做Smoke就称已复现。

## 7. Risks
WSL VHDX、用户配置、系统TEMP、HuggingFace/HF-Xet缓存、pip/conda缓存、解压临时文件隐式落C；长时间实验产生磁盘过量；未审批自动下载；人工许可/非商业条款；旧artifacts源码与论文公式偏差；在无法运行的torch2.4/sm120基础上虚构严格复现；开发集结果冒充独立评估；历史/主线污染。

## 8. Options and comparison
A — OWNER SELECTED: C盘不新增项目可控内容；后续大型文件只放D/E，取消Fast-Track B对D/E硬性1GiB全局新增磁盘上限，但每个实际任务必须事前冻结明确预计峰值、临时文件和安全剩余空间界，不能无限写盘。维持原250MiB累计下载上限、固定模型revision/文件白名单与其余全部权限。5090继续不下载的只读/离线复现矩阵审计及脚本可运行性预检。优点：减少空转；风险：缓存误写C和资源预估不足；可逆，不改旧资产。
B — NOT SELECTED: 保留所有磁盘上限且5090无任务便空闲；风险低但延迟复现准备。
C — NOT APPROVED: 立刻大量下载Llama/Vicuna/Contriever/BEIR并运行全部Claims；有望更快得到数值，但需另外核许可、下载/存储/VRAM/时长和命令，不能由这项方向性决定自动放行。

## 9. Recommendation
采用A。在现有5090工作线上并行进行原论文图表—作者脚本映射、Claim1–3输入/模型/许可/资源矩阵、可离线的调用链/副作用静态审计、确定一次性分阶段下载与运行审批包、估算磁盘显存及时间；不重复已完成Smoke，不安装pytest或加载权重，也不重写作者源码。5060在保持250MiB下载界及固定B1模型身份的前提下并行继续Fast-Track B。

## 10. Rationale / confidence
Owner新增存储和目标明确；上游三个Claim/未自动化图表的映射可查；具体模型可用性、结果及C盘副作用仍未知。对OS自身不可控的少量系统日志等，不承诺绝对零写入，但任何项目可控目录（模型、缓存、临时、数据、conda/pip、代码、归档）必须禁止写C；若技术上无法保证某个项目操作不增长C盘，停止该操作并上报。

## 11. Explicit approvals and unapproved gates
APPROVED:
- 5060的未来项目受控新增内容落D/E，放宽原Fast-Track B D/E磁盘新增1GiB硬限；每个任务在执行前冻结峰值用量和至少20GiB安全可用余量，若无法保障停止。已批准的B1官方HF网络累计下载上限250MiB不变，模型白名单、唯一revision和语义对照、36冻结TopK、12题裁决准备边界不变。
- 5090在本分支已存在环境中开展无需联网下载、不使用外部API/商业服务、不载入权重或BEIR、不执行三个Claim的原论文结果覆盖矩阵与纯离线静态/命令预检。准备分阶段Claim运行审批包，包含Fig4/Fig5开源行与Table2/3/5/6/7/8的自动化程度，必要时备注Table4额外外部框架。不再反复做已完成的虚构Smoke。可提交脱敏治理和准备文档并推送自分支，随后STOP。
- 两机需分别验证项目缓存、临时文件、WSL VHDX实际宿主位置；任何新写入C的项目可控路径须先迁至D/E或停止，禁止擅自搬迁/破坏既有环境。

NOT APPROVED: 扩大250MiB网络下载；5060除原B1固定白名单之外的新模型/依赖/BEIR；5090模型/检索器/BEIR权重数据下载、Claim运行、系统安装、付费API；D2/D3、Reviewer/正式GT、T1/T2、B3/B4/B5/B6、D1-40、跨分支/主线合并、算法语义patch；把后续兼容环境结果说成官方严格论文数值复现。上述项目必须有后续明确Owner决定。

## 12. Allowed / prohibited before next gate
允许两机上述本地审计、已批准Fast-Track B和准备阶段合规记录；禁止对未获批准的资源/模型/正式实验/原始研究资产作任何隐式改变。完成相应任务时保存执行命令、失败、SHA、Run Manifest、来源、归档索引并按AGENTS.md文档收口；两机各自分支Git commit/push后STOP，等待下一个具体资源/Claim审批。

## Reproduction success criteria (future, not an execution approval)
Phase R1: 在许可和模型/语料/命令均获批后分别运行三个作者Claim，按NQ、HotpotQA、MS MARCO、两种7B生成器及作者配置的攻击强度报告样本分母、ASR、Accuracy、失败、时延、配置哈希和偏差。标为COMPATIBILITY_ARTIFACT_REPRO，非论文原环境。
Phase R2: 根据R1和论文核心贡献优先补可自动化Table5多检索器、Table7参数消融、Table8双阶段作用、Table2/3效率/显存记录；Table6修改聚类算法属源码语义patch，必须另批；Table4多架构/13B/GPT/Gemini不自动视为首轮必跑。
Phase R3: 中英文迁移与独立D1/D2/D3治理按正式方案分别审批和执行；不由R1/2自动授权。
