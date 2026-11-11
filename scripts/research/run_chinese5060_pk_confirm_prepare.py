"""Freeze PK-CONFIRM role-blind inputs and the historical RD_B2 masks offline."""

from __future__ import annotations

import argparse
from pathlib import Path

import run_chinese5060_owner28 as backend

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import pk_confirm, qag

ROOT = "docs/paper1/dual_machine/repro5090/pk_confirm/"


def main() -> None:
    parser = argparse.ArgumentParser()
    for name in ("out", "assets", "upstream", "support"):
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--freeze", required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    if (
        not out.is_relative_to(qag.BASE.resolve())
        or backend.git("rev-parse", "HEAD").decode().strip() != args.freeze
        or backend.git("status", "--porcelain")
    ):
        raise ValueError("PKC_FROZEN_CHECKOUT")
    backend.git(
        "merge-base", "--is-ancestor", pk_confirm.CURATOR, backend.CURATOR_BRANCH
    )
    data = pk_confirm.validated_inputs(
        {
            name: backend.git("show", f"{pk_confirm.CURATOR}:{ROOT}{name}")
            for name in pk_confirm.INPUT_SHA
        }
    )
    plan = pk_confirm.request_plan(data)
    out.mkdir()
    backend.configure(out)
    (model, defender, baseline, _), r2 = backend.pinned_backend(args)
    masks = {}
    for row in data["worlds"]:
        texts = [p["text"] for p in row["passages"]]
        embedding = r2.model_vectors(model, texts)
        embedding_sha = qag.digest(embedding.cpu().detach().numpy().tobytes())
        trace = r2.filter_one(
            defender, baseline, texts, texts, embedding, embedding_sha
        )
        masks[row["world_id"]] = [
            i for i in range(5) if i not in trace["deleted_indices"]
        ]
    seal = {
        "freeze_commit": args.freeze,
        "curator_commit": pk_confirm.CURATOR,
        "reviewer_commit": pk_confirm.REVIEWER,
        "curator_files_sha256": pk_confirm.INPUT_SHA,
        "code_sha256": pk_confirm.code_hashes(),
        "wire_sha256": pk_confirm.plan_hash(plan),
        "input_sha256": qag.write_once(out / "INPUT.json", data),
        "rd_b2_sha256": qag.write_once(out / "RD_B2.json", masks),
        "rd_b2_backend": backend.BASE_IDENTITY,
        "other_verify": "NOT_RUN",
    }
    print(
        qag.encoded(
            seal | {"seal_sha256": qag.write_once(out / "SEAL.json", seal)}
        ).decode(),
        flush=True,
    )


if __name__ == "__main__":
    main()
