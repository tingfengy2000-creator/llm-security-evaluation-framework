# Git 上传前检查

1. 执行 `git fetch origin --prune`，确认本地没有落后远端。
2. 运行 `scripts/git_preflight.ps1`。
3. 确认 Stage 5 与 Stage 5 Paper 测试通过。
4. 确认历史 baseline 无差异。
5. 确认没有真实凭据、`.env`、Authorization 或 raw provider trace。
6. 确认 `.venv/`、`__pycache__/`、运行缓存和临时目录未被跟踪。
7. 检查大于 10 MB 的文件是否需要 Git LFS 或在线地址。
8. 检查 `experiments/registry.json` 的路径、状态和结论边界。
9. 比较关键目录本地与远端的跟踪文件数量。
10. 人工查看 `git status --short --ignored` 和待提交 diff。
11. 使用功能分支推送并通过 Pull Request 合并到 `main`。

本次 Stage 1–5 同步审计见 `STAGE1_5_SYNC_AUDIT_2026-07-16.md`。
