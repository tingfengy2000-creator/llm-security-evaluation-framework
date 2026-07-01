from __future__ import annotations

from pathlib import Path
from typing import Any


def write_run_summary(
    path: Path,
    run_id: str,
    provider: str,
    status: str,
    metrics_rows: list[dict[str, Any]],
    validation_issues: list[dict[str, Any]],
) -> None:
    mode_rows = [row for row in metrics_rows if row.get("scope") == "mode"]
    lines = [
        "# Stage 5 运行摘要",
        "",
        f"- run_id: `{run_id}`",
        f"- provider: `{provider}`",
        f"- run_status: `{status}`",
        "",
        "## 四模式对比",
        "",
        "| Guard Mode | ASR | Input Block | Output Block | Upstream | Over-block |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in sorted(mode_rows, key=lambda item: str(item["guard_mode"])):
        lines.append(
            "| {guard_mode} | {asr_percent:.2f}% | "
            "{input_block_rate_percent:.2f}% | {output_block_rate_percent:.2f}% | "
            "{upstream_call_rate_percent:.2f}% | {overblock_rate_percent:.2f}% |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## 验证",
            "",
            (
                "全部科学不变量通过。"
                if not validation_issues
                else f"发现 {len(validation_issues)} 个验证问题，运行不可用于结论。"
            ),
            "",
            "## 结论边界",
            "",
            "这些数字只描述当前攻击矩阵、当前模型和当前 rule-based baseline，"
            "不是生产防护率，也不代表模型绝对安全。",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
