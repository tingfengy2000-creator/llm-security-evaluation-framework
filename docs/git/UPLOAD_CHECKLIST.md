# Git 上传前检查

1. 运行 `scripts/git_preflight.ps1`。
2. 确认 Stage 5 与 Stage 5 Paper 测试通过。
3. 确认历史 baseline 无差异。
4. 确认没有真实凭据、`.env` 或 raw provider trace。
5. 检查大于 10 MB 的文件是否需要 LFS 或在线地址。
6. 检查 `experiments/registry.json` 路径完整。
7. 人工查看 `git status --short --ignored` 后再提交。
