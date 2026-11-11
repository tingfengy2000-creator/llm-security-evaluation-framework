"""Read-only Owner32 source-availability check.

The checker never fetches a page, never reads private labels, and never
turns a metadata row into an answer card.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PUB = REPO / "docs/paper1/dual_machine/repro5090/owner32_precheck"
REPORT = PUB / "OWNER32_SOURCE_AVAILABILITY_AUDIT.md"
MANIFEST = PUB / "OWNER32_SOURCE_AVAILABILITY_MANIFEST.json"
PIN = "2f8c4c2ebe79d3711cb107519869e7fbf8f1f1b0"
REGISTER = "docs/paper1/dual_machine/chinese5060/PUBLIC_VERSION_SOURCE_REGISTER_DRAFT.json"
ORACLE_FIELDS = {"gold_value", "attack_value", "correct_answer", "role", "poison", "clean"}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def assess(record: dict) -> dict[str, object]:
    """Return whether one source row is independently usable. No network."""
    reasons: list[str] = []
    leaked = sorted(ORACLE_FIELDS.intersection(record))
    if leaked:
        reasons.append("ORACLE_CARD_FIELD")
    url = str(record.get("url") or "")
    if not url.startswith("https://"):
        reasons.append("URI_NOT_HTTPS")
    if record.get("rights_status") != "RIGHTS_CLEARED":
        reasons.append("RIGHTS_NOT_CLEARED")
    if record.get("outbound_status") != "AUTHORIZED":
        reasons.append("OUTBOUND_NOT_AUTHORIZED")
    if record.get("independent_receipt_status") != "FROZEN":
        reasons.append("INDEPENDENT_RECEIPT_NOT_FROZEN")
    document_sha = str(record.get("document_sha256") or "")
    if len(document_sha) != 64:
        reasons.append("NO_DOCUMENT_BYTES_HASH")
    if len(str(record.get("tls_receipt_sha256") or "")) != 64:
        reasons.append("NO_TLS_RECEIPT")
    if not record.get("effective_from") or not record.get("scope"):
        reasons.append("WINDOW_OR_SCOPE_MISSING")
    if record.get("access_status") != "METADATA_READ":
        reasons.append("ACCESS_NOT_INDEPENDENTLY_READ")
    return {
        "usable": not reasons,
        "reasons": reasons,
        "tls_status": "NOT_ATTEMPTED" if "NO_TLS_RECEIPT" in reasons else "RECEIPT_PRESENT",
        "document_sha256": document_sha or None,
    }


def metadata_view(lineage_id: str, record: dict) -> dict[str, object]:
    return {
        "lineage_id": lineage_id,
        "record_id": record.get("id"),
        "url": record.get("url"),
        "effective_from": record.get("effective_from"),
        "superseded_on": record.get("superseded_on"),
        "explicit_repealed_on": record.get("explicit_repealed_on"),
        "scope": record.get("scope"),
        "locator": record.get("locator"),
        "rights_status": record.get("rights_status"),
        "outbound_status": record.get("outbound_status"),
        "provenance_status": record.get("provenance_status"),
        "independent_receipt_status": record.get("independent_receipt_status"),
    }


def load_register() -> tuple[bytes, dict]:
    raw = subprocess.check_output(["git", "cat-file", "blob", f"{PIN}:{REGISTER}"], cwd=REPO)
    return raw, json.loads(raw)


def audit_rows(register: dict) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for lineage in register["lineages"]:
        for record in lineage["records"]:
            view = metadata_view(lineage["id"], record)
            decision = assess(record)
            rows.append({
                **view,
                "metadata_sha256": sha(canonical(view)),
                "sealed_record_sha256": sha(canonical(record)),
                "usable": decision["usable"],
                "reasons": decision["reasons"],
                "tls_status": decision["tls_status"],
                "document_sha256": decision["document_sha256"],
            })
    return rows


def render(rows: list[dict[str, object]], register_sha: str) -> str:
    usable = sum(bool(row["usable"]) for row in rows)
    lines = [
        "# Owner32 来源可用性预检",
        "",
        "状态 `SOURCE_GATE_NO_GO / SOURCE_CURATION_BLOCKED / SCIENCE_NOT_RUN / HUMAN_GOLD=0`。",
        "这是获批前的只读核查。没有新的 DEV 或 EVAL，没有改 Q-CER，没有下载页面，也没有制作正确答案卡。",
        "",
        f"来源登记取自 5060 提交 `{PIN}` 的 `{REGISTER}`，文件 SHA256 `{register_sha}`。登记里的 10 条版本记录全部检查。Owner27 私有预测包不在本机，5090 私有标签没有打开，所以没有另抽带角色的删除片段。",
        "",
        f"可用独立证据 `{usable}/10`。进入下一步需要至少 3 条同时具备可核文档字节、独立读取收据、版本窗口和 scope。当前是 0，来源门关闭。",
        "",
        "## 十条记录",
        "",
        "下表的时间窗口和 scope 是登记里的未复核元数据，不是新的事实答案。`sealed_record_sha256` 是该条登记原文的哈希。没有一条有官方页面字节哈希。",
        "",
        "| 记录 | 版本出处 | 生效 | 替换点 | 可用 | 证据哈希 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            f"| {row['record_id']} | `{row['url']}` | {row['effective_from']} | {row['superseded_on']} | "
            f"{'YES' if row['usable'] else 'NO'} | `{row['sealed_record_sha256']}` |"
        )
        scope = row["scope"]
        end = "未登记" if row["superseded_on"] is None else row["superseded_on"]
        lines[-1] = (
            f"| {row['record_id']} | `{row['url']}` | {row['effective_from']} | {end} | "
            f"{'YES' if row['usable'] else 'NO'} | `{row['sealed_record_sha256']}` |"
        )
        lines.append(f"|  | scope：{scope} |  |  |  | `{row['metadata_sha256']}` |")
    lines.extend([
        "",
        "## 不能核验的原因",
        "",
        "十条原因相同，逐条都成立：",
        "",
        "- 权利状态不是 `RIGHTS_CLEARED`，登记写的是 `RIGHTS_UNKNOWN`。因此本次不下载正文，也不做 TLS 读取。",
        "- 出站状态是 `NOT_AUTHORIZED`，访问记为 `NOT_ATTEMPTED`。",
        "- 独立读取收据是 `NOT_FROZEN`。没有可复核的采集收据。",
        "- 登记没有 `document_sha256`，也没有 `tls_receipt_sha256`。现有哈希只覆盖登记文字，不能证明官方页面字节。",
        "- 卫生、节假日和驾驶证三条谱系已经进入 Owner27 开发材料。药品目录没有进入那次运行，但它同样没有冻结的文档字节和独立收据，所以也不能当作未见独立证据。",
        "",
        "Owner31 的 32 个虚构世界继续封存，不拿来冒充外部法规证据。",
        "",
        "## 只读设计",
        "",
        "可用性函数只看一条来源记录自身的字段。它拒绝带有正确答案、攻击值或角色的字段。虚构单测覆盖通过、缺文档哈希和答案卡三种情况，不访问网络。",
        "Owner32 仍是 `DESIGN_DRAFT / OWNER_APPROVAL_PENDING`。在正式批准前不启动科学试次。`AUTO_CONTINUE=NO`。Claim1–3 仍是 `NOT_RUN`。",
        "",
    ])
    text = "\n".join(lines)
    for token in ("gold_value", "attack_value", "60周岁", "63周岁", "卫生许可证", "卫生备案"):
        if token in text:
            raise SystemExit(f"ANSWER_CARD:{token}")
    return text


def main() -> None:
    if REPORT.exists() or MANIFEST.exists():
        raise SystemExit("ALREADY_WRITTEN")
    raw, register = load_register()
    rows = audit_rows(register)
    if len(rows) != 10:
        raise SystemExit("ROW_COUNT")
    if any(row["usable"] for row in rows):
        raise SystemExit("UNEXPECTED_USABLE")
    report = render(rows, sha(raw))
    PUB.mkdir(parents=True, exist_ok=True)
    report_bytes = report.encode("utf-8")
    REPORT.write_bytes(report_bytes)
    manifest = {
        "schema": "OWNER32_SOURCE_AVAILABILITY_MANIFEST_V1",
        "status": "SOURCE_GATE_NO_GO / SOURCE_CURATION_BLOCKED / SCIENCE_NOT_RUN / HUMAN_GOLD=0",
        "authority": "DESIGN_DRAFT / OWNER_APPROVAL_PENDING",
        "human_gold": 0,
        "science_trial": "NOT_RUN",
        "qcer_modified": False,
        "network_fetches": 0,
        "private_labels_opened": False,
        "answer_cards_created": False,
        "register_commit": PIN,
        "register_path": REGISTER,
        "register_sha256": sha(raw),
        "records": 10,
        "usable": 0,
        "gate": "SOURCE_GATE_NO_GO",
        "rows": [
            {
                "record_id": row["record_id"],
                "lineage_id": row["lineage_id"],
                "url": row["url"],
                "effective_from": row["effective_from"],
                "superseded_on": row["superseded_on"],
                "metadata_sha256": row["metadata_sha256"],
                "sealed_record_sha256": row["sealed_record_sha256"],
                "document_sha256": row["document_sha256"],
                "tls_status": row["tls_status"],
                "usable": row["usable"],
                "reasons": row["reasons"],
            }
            for row in rows
        ],
        "report_sha256": sha(report_bytes),
        "auto_continue": "NO",
        "claim1": "NOT_RUN",
        "claim2": "NOT_RUN",
        "claim3": "NOT_RUN",
    }
    MANIFEST.write_bytes((json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(sha(report_bytes))
    print(sha(MANIFEST.read_bytes()))
    print(0, 10)


if __name__ == "__main__":
    main()
