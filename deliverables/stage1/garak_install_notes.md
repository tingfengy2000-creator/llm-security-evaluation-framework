# garak 安装与环境记录

## 实验记录基准

- 参考实验计划：`E:\CodeGuarder\docs\experiment_plan.md`
- 本次实验阶段：Stage 1，garak 最小安全扫描链路验证
- 记录原则：说明为什么做、改哪里、是否影响原始数据、怎么验证

## 为什么做

Stage 1 的目标不是直接证明某个真实大模型安全或不安全，而是先证明我能搭建一套可复现的大模型安全评测流程：

1. 创建独立项目目录。
2. 初始化 Python 虚拟环境。
3. 安装并运行 garak。
4. 使用 mock model 跑通最小安全扫描。
5. 保存命令、结果和阶段报告，作为后续真实模型接入的基线。

## 环境信息

- 项目目录：`D:\llmProject\llm-security-stage1`
- 交付目录：`D:\llmProject\deliverables\stage1`
- Python 虚拟环境：`D:\llmProject\llm-security-stage1\.venv`
- Python 版本：`Python 3.12.13`
- garak 版本：`garak 0.15.1`
- requirements：`D:\llmProject\llm-security-stage1\requirements.txt`

## 安装命令

```powershell
C:\Users\Admin\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m venv D:\llmProject\llm-security-stage1\.venv
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe -m pip install --upgrade pip garak
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe --version
```

## 本地兼容性处理

当前沙箱环境限制了 garak 默认用户目录下的配置、缓存和日志写入。为保证实验可复现，本阶段将 garak 的 XDG 目录固定到交付目录：

```powershell
$env:XDG_CONFIG_HOME='D:\llmProject\deliverables\stage1\xdg_config'
$env:XDG_DATA_HOME='D:\llmProject\deliverables\stage1\xdg_data'
$env:XDG_CACHE_HOME='D:\llmProject\deliverables\stage1\xdg_cache'
```

同时只在本项目虚拟环境内做了兼容调整，使 garak 使用工作区内目录和包内插件缓存。这不会修改全局 Python 环境，也不会影响 `E:\CodeGuarder` 中的原始复现实验数据。

## 是否影响原始数据

不影响。Stage 1 的所有新文件都放在：

- `D:\llmProject\llm-security-stage1`
- `D:\llmProject\deliverables\stage1`

没有覆盖 `E:\CodeGuarder` 的论文复现数据、结果 JSON 或实验脚本。

## 验证方式

```powershell
D:\llmProject\llm-security-stage1\.venv\Scripts\python.exe --version
D:\llmProject\llm-security-stage1\.venv\Scripts\garak.exe --version
powershell -ExecutionPolicy Bypass -File D:\llmProject\llm-security-stage1\scripts\run_stage1_scan.ps1
```

最终验证结果：

- Python 可以启动。
- garak 可以启动。
- 两条 Stage 1 扫描命令均成功完成。
- JSONL 和 HTML 报告均已落盘。
