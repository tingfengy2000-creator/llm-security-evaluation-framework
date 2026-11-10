"""Owner20 bounded offline workflow: custody, old-only preflight, release, predict, confirm, score."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from zipfile import ZIP_DEFLATED, ZipFile

RUN = "W1-5060-S1B-RULE-ONESHOT-20261110-01"
OWNER = "W1-OD-20261110-5060-S1B-ONE-SHOT-20"
OWNER_SHA = "7a18411dff1a12f7b0e59297db816308280a0966"
BASE = Path(r"D:\llmProject\.worktrees\paper1-chinese-defense-5060\experiments\paper1_chinese5060")
DATA = BASE / "W1-5060-S1B-FEAS-DATA-PREP-20261109-01"
OLD_INPUT = BASE / "W1-5060-S1-CHINESE-EXTRACTION-20261108-01" / "INFERENCE_PRIVATE.json"
OUT = BASE / RUN
REPO = Path(__file__).resolve().parents[6]
MODULE = Path(__file__).resolve().parent
SEAL = "531ac4e6421f6486b8165d443af2cf9d892a7bc3c740483950d03240d35a7c58"
INPUT = "bd2bc5e6586789070c20dde123bfe72843181aa861aca229fdb0c23091328dee"
GOLD = "8f745f921424c6e61357ec19800bc4a1f198e92a26d36377a3a238d634598371"
PROTOCOL = "43d4d22770f5887058fabfc0162368e77cd36bd6c7d85d846417789515f5341e"
OLD_SHA = "8245af9a1241fe966f0dbc05e52ed7744b041e13685a743a81aebd818b9a8481"
DATA_COMMIT = "20402e94ed3da6be155a605daba272ec0a7c2cf1"
V1 = "68d34a5d877206f4e6d7d9e2bdda16784145a76a"
V2 = "da3cbd9f16ea70ae3ba0ef2aa2408227ecfc0b4f"
V2_CONFIG = "4352bbcc97ccc5b42861611d1f6a952718af7f195acf02c6c2507f3269232b38"
RULE_FILES = {"s1_extraction.py": V1, "vesa_guard_v01.py": V1, "vesa_guard_v02.py": V1, "s1b_rule_v2.py": V2}
LOCAL_FILES = ("s1b_oneshot_run.py", "s1b_oneshot_adapter.py", "s1b_oneshot_scoring.py", "s1b_feasibility_data.py")
RECEIPT = DATA / "seals" / "DATA_SEAL.json"
INPUT_FILE = DATA / "runtime" / "INPUT.json"
GOLD_FILE = DATA / "evaluation" / "PROVISIONAL_GOLD.json"
PROTOCOL_FILE = DATA / "control" / "SCORING_PROTOCOL.md"
ARMS = ("Rule-V1", "Rule-V2")
PRED_FILES = tuple(arm + "_PRIVATE.json" for arm in ARMS)
BRANCH = "research/paper1-chinese-defense-5060"
BUNDLES = {"authoring": ("01-03.txt", "04-06.txt", "07-08.txt", "09-10.txt"),
           "control": ("GENERATION_PLAN.json", "SOURCE_LICENSE.json", "SCORING_PROTOCOL.md"),
           "custodian": ("SOURCE_TRUTH.json", "PAIRS.json"), "runtime": ("INPUT.json",),
           "evaluation": ("PROVISIONAL_GOLD.json",)}
DENIED: list[str] = []


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def timestamp() -> str:
    return datetime.now(UTC).isoformat()


def read(path: Path, expected: str | None = None) -> bytes:
    require(path.resolve(strict=True) == path, "NONCANONICAL_PATH")
    data = path.read_bytes()
    require(expected is None or digest(data) == expected, "HASH_MISMATCH:" + path.name)
    return data


def obj(path: Path, expected: str | None = None) -> Any:
    return json.loads(read(path, expected))


def write(name: str, value: Any) -> str:
    data = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    with (OUT / name).open("xb") as handle:
        handle.write(data)
    return digest(data)


def guard(allowed: set[Path], writes: set[str]) -> None:
    writable = {OUT / name for name in writes}
    allowed = allowed | writable
    interpreter = {Path(sys.executable).resolve(), Path(getattr(sys, "_base_executable", sys.executable)).resolve()}

    def hook(event: str, args: tuple[Any, ...]) -> None:
        denied = event.startswith("socket.") or event in {
            "subprocess.Popen", "os.system", "os.startfile", "os.spawn", "ctypes.dlopen", "ctypes.dlsym",
        }
        if event in {"open", "os.listdir", "os.scandir"} and isinstance(args[0], (str, bytes, os.PathLike)):
            path = Path(os.fsdecode(args[0])).resolve()
            if event == "open":
                flags = args[2]
                writing = bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC))
                is_code = path.suffix.lower() in {".py", ".pyc", ".pyd"} and (
                    path.is_relative_to(REPO / "src") or path.is_relative_to(Path(sys.base_prefix))
                )
                denied = path not in writable if writing else path not in allowed | interpreter and not is_code
            else:
                denied = path.is_relative_to(BASE)
        if denied:
            DENIED.append(event)
            raise PermissionError("OWNER20_ROLE_ALLOWLIST:" + event)

    sys.addaudithook(hook)


def rows(path: Path, checksum: str, count: int) -> list[dict[str, Any]]:
    data = read(path, checksum)
    records = json.loads(data)
    require(len(data) <= 1024 * 1024 and len(records) == count and
            all(set(r) == {"id", "query", "evidence"} and all(isinstance(v, str) for v in r.values()) for r in records)
            and len({r["id"] for r in records}) == count, "ROLE_FREE_INPUT")
    return records


def source_blobs() -> dict[str, str]:
    return {name: digest(read(MODULE / name).replace(b"\r\n", b"\n")) for name in (*RULE_FILES, *LOCAL_FILES)}


def env() -> dict[str, Any]:
    path = Path(sys.executable).resolve()
    base = Path(getattr(sys, "_base_executable", sys.executable)).resolve()
    return {"python": sys.version, "platform": sys.platform, "pointer_bits": sys.maxsize.bit_length() + 1,
            "python_exe_sha256": digest(read(path)), "python_base_exe_sha256": digest(read(base)),
            "isolated": sys.flags.isolated, "no_site": sys.flags.no_site, "no_bytecode": sys.dont_write_bytecode}


def custody() -> None:
    # This process has no rule import or prediction entry. It does not parse Gold or return content.
    members = {DATA / d / f for d, filenames in BUNDLES.items() for f in filenames}
    zips = {DATA / "seals" / (d + ".zip") for d in BUNDLES}
    guard(members | zips | {RECEIPT}, {"CUSTODY_HASH_ONLY.json"})
    seal = obj(RECEIPT, SEAL)
    require(seal["members"]["runtime/INPUT.json"] == INPUT and
            seal["members"]["evaluation/PROVISIONAL_GOLD.json"] == GOLD and
            seal["members"]["control/SCORING_PROTOCOL.md"] == PROTOCOL, "DATA_PINS")
    for directory, names in BUNDLES.items():
        archive = DATA / "seals" / (directory + ".zip")
        read(archive, seal["archives"][directory])
        with ZipFile(archive) as bundle:
            require(bundle.namelist() == list(names) and bundle.testzip() is None, "DATA_ZIP_MEMBERS")
            for name in names:
                require(bundle.read(name) == read(DATA / directory / name, seal["members"][f"{directory}/{name}"]),
                        "DATA_ZIP_BYTE_MISMATCH")
    require(not DENIED, "CUSTODY_ISOLATION")
    write("CUSTODY_HASH_ONLY.json", {"run_id": RUN, "seal": SEAL, "input": INPUT, "gold_hash_only": GOLD,
                                    "protocol": PROTOCOL, "archives": seal["archives"], "pid": os.getpid(),
                                    "verified_at": timestamp(), "members_verified": len(members)})


def arm_results(records: list[dict[str, Any]], timeout: int) -> Iterator[tuple[str, list[dict[str, Any]]]]:
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import s1_extraction, s1b_rule_v2
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.s1b_oneshot_adapter import Extract, invoke

    require(s1b_rule_v2.CONFIG_SHA256 == V2_CONFIG, "RULE_V2_CONFIG_IDENTITY")
    start = time.monotonic()
    extractors: tuple[Extract, Extract] = (s1_extraction.extract_one, s1b_rule_v2.extract_one)
    for arm, extractor in zip(ARMS, extractors, strict=True):
        result = []
        for record in records:
            require(time.monotonic() - start < timeout, "CPU_TIME_CAP")
            result.append(invoke(extractor, record))
        yield arm, result


def preflight() -> None:
    guard({OLD_INPUT, *(MODULE / n for n in (*RULE_FILES, *LOCAL_FILES))}, {"OLD73_PREFLIGHT.json"})
    # A denied probe has no underlying file; this exercises the same deny branch used for private data.
    try:
        (DATA / "evaluation" / "OWNER20_DENY_PROBE_DOES_NOT_EXIST").read_bytes()
    except PermissionError:
        pass
    require(DENIED == ["open"], "LABEL_DENIAL_PROBE_FAILED")
    DENIED.clear()
    before = time.monotonic()
    results = dict(arm_results(rows(OLD_INPUT, OLD_SHA, 73), 60))
    summary = {arm: dict(Counter(row["projection"]["status"] for row in values)) for arm, values in results.items()}
    require(not DENIED and all(not values.get("ERROR") and sum(values.values()) == 73 for values in summary.values()),
            "OLD_DEV_ADAPTER_PREFLIGHT_FAILED")
    write("OLD73_PREFLIGHT.json", {"source": OLD_SHA, "counts": summary, "files": source_blobs(),
                                   "env": env(), "runtime_seconds": time.monotonic() - before, "new_views": 0,
                                   "deny_probe": "PASS", "pid": os.getpid()})


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=REPO, env={**os.environ, "GIT_NO_LAZY_FETCH": "1"})


def release() -> None:
    require(git("branch", "--show-current").decode().strip() == BRANCH and not git("status", "--porcelain"),
            "RELEASE_NOT_CLEAN_BRANCH")
    head = git("rev-parse", "HEAD").decode().strip()
    for known in (OWNER_SHA, DATA_COMMIT, V1, V2):
        git("merge-base", "--is-ancestor", known, head)
    files = source_blobs()
    for name, checksum in files.items():
        path = (MODULE / name).relative_to(REPO).as_posix()
        require(digest(git("show", head + ":" + path)) == checksum, "UNCOMMITTED_SOURCE_BYTES")
        if name in RULE_FILES:
            require(digest(git("show", RULE_FILES[name] + ":" + path)) == checksum, "FROZEN_RULE_SOURCE_DRIFT")
    dev = obj(OUT / "OLD73_PREFLIGHT.json")
    custody_report = obj(OUT / "CUSTODY_HASH_ONLY.json")
    require(dev["files"] == files and dev["env"] == env() and dev["new_views"] == 0
            and custody_report["seal"] == SEAL and custody_report["gold_hash_only"] == GOLD,
            "RELEASE_IDENTITY_MISMATCH")
    require(shutil.disk_usage(OUT).free >= 1024 ** 3, "D_DRIVE_RESERVE")
    qa = {name: digest(read(OUT / "qa" / name)) for name in ("pytest.log", "ruff.log", "mypy.log")}
    require(all(read(OUT / "qa" / (name + ".exit")).decode().strip() == "0"
                for name in ("pytest", "ruff", "mypy")), "QA_EXIT_NONZERO")
    receipt = {"run_id": RUN, "owner": OWNER, "owner_sha": OWNER_SHA, "data_commit": DATA_COMMIT,
               "code_commit": head, "source_sha256": files, "old73_preflight_sha256": digest(read(OUT / "OLD73_PREFLIGHT.json")),
               "custody_sha256": digest(read(OUT / "CUSTODY_HASH_ONLY.json")), "qa_sha256": qa,
               "seal": SEAL, "input": INPUT, "gold_hash_only": GOLD, "protocol": PROTOCOL, "env": env(),
               "rule_commits": {"Rule-V1": V1, "Rule-V2": V2}, "rule_v2_config": V2_CONFIG,
               "parameters": {"arms": list(ARMS), "views_per_arm": 120, "runs": 1, "cpu_time_cap_seconds": 120,
                              "max_arm_bytes": 10 * 1024 * 1024, "network": "DENY", "retry": 0},
               "sequence": ["custody_hash_only", "old73_preflight", "release", "predict", "confirm", "evaluate"],
               "released_at": timestamp()}
    print(write("RELEASE.json", receipt))


def predict(release_sha: str) -> None:
    guard({INPUT_FILE, OUT / "RELEASE.json", *(MODULE / n for n in (*RULE_FILES, *LOCAL_FILES))},
          {"R_STARTED.json", *PRED_FILES, "ROLE_FREE.zip", "PREDICTION_SEAL.json"})
    lock = obj(OUT / "RELEASE.json", release_sha)
    require(lock["env"] == env() and lock["source_sha256"] == source_blobs() and lock["input"] == INPUT,
            "PREDICT_RELEASE_DRIFT")
    write("R_STARTED.json", {"pid": os.getpid(), "timestamp": timestamp(), "release_sha256": release_sha})
    start = time.monotonic()
    records = rows(INPUT_FILE, INPUT, 120)
    members = {}
    counts = {}
    for arm, results in arm_results(records, lock["parameters"]["cpu_time_cap_seconds"]):
        members[arm + "_PRIVATE.json"] = write(arm + "_PRIVATE.json", results)
        counts[arm] = len(results)
    with ZipFile(OUT / "ROLE_FREE.zip", "x", compression=ZIP_DEFLATED) as archive:
        for name, checksum in members.items():
            data = read(OUT / name, checksum)
            require(len(data) <= lock["parameters"]["max_arm_bytes"], "PREDICTION_SIZE_CAP")
            archive.writestr(name, data)
    require(not DENIED, "PREDICTION_ISOLATION")
    checksum = write("PREDICTION_SEAL.json", {
        "run_id": RUN, "release_sha256": release_sha, "input_sha256": INPUT, "members": members,
        "archive_sha256": digest(read(OUT / "ROLE_FREE.zip")), "finished_at": timestamp(), "pid": os.getpid(),
        "elapsed_seconds": time.monotonic() - start, "role_free_counts": counts,
        "network_events": 0, "gold_reads": 0, "attempts": 1,
    })
    print(checksum)


def verified_output(release_sha: str, seal_sha: str) -> dict[str, list[dict[str, Any]]]:
    lock = obj(OUT / "RELEASE.json", release_sha)
    receipt = obj(OUT / "PREDICTION_SEAL.json", seal_sha)
    require(lock["source_sha256"] == source_blobs() and lock["env"] == env(), "VERIFICATION_SOURCE_OR_ENV_DRIFT")
    require(receipt["release_sha256"] == release_sha and receipt["input_sha256"] == INPUT and
            receipt["role_free_counts"] == {arm: 120 for arm in ARMS} and receipt["gold_reads"] == 0,
            "PREDICTION_INCOMPLETE")
    path = OUT / "ROLE_FREE.zip"
    read(path, receipt["archive_sha256"])
    values = {}
    with ZipFile(path) as archive:
        require(archive.namelist() == sorted(PRED_FILES) and archive.testzip() is None, "PREDICTION_ZIP")
        expected = [r["id"] for r in rows(INPUT_FILE, INPUT, 120)]
        for arm, name in zip(ARMS, PRED_FILES, strict=True):
            raw = read(OUT / name, receipt["members"][name])
            require(raw == archive.read(name), "PREDICTION_ARCHIVE_DRIFT")
            records = json.loads(raw)
            require([r["id"] for r in records] == expected and
                    all(set(r) == {"id", "raw", "projection"} for r in records), "PREDICTION_DENOMINATOR_DRIFT")
            values[arm] = records
    return values


def confirm(release_sha: str, seal_sha: str) -> None:
    require(os.getpid() != obj(OUT / "PREDICTION_SEAL.json", seal_sha)["pid"], "SAME_PREDICTION_PROCESS")
    verified_output(release_sha, seal_sha)
    print(write("READONLY_CONFIRMATION.json", {"release_sha256": release_sha, "prediction_seal_sha256": seal_sha,
                                            "confirmed_at": timestamp(), "pid": os.getpid(), "gold_reads": 0}))


def evaluate(release_sha: str, seal_sha: str, confirmed_sha: str) -> None:
    from llmguard.domains.retrieval.hidden_poisoning.chinese5060.s1b_oneshot_scoring import score, summarize

    checked = obj(OUT / "READONLY_CONFIRMATION.json", confirmed_sha)
    require(checked["release_sha256"] == release_sha and checked["prediction_seal_sha256"] == seal_sha,
            "MISSING_POST_PREDICTION_CONFIRMATION")
    predictions = verified_output(release_sha, seal_sha)
    write("E_STARTED.json", {"pid": os.getpid(), "started_at": timestamp(), "confirmation_sha256": confirmed_sha})
    gold_opened_at = timestamp()
    gold = {r["id"]: r for r in obj(GOLD_FILE, GOLD)}
    read(PROTOCOL_FILE, PROTOCOL)
    cases = {r["id"]: r["evidence"] for r in rows(INPUT_FILE, INPUT, 120)}
    data_seal = obj(RECEIPT, SEAL)
    pairs = obj(DATA / "custodian" / "PAIRS.json", data_seal["members"]["custodian/PAIRS.json"])
    truth = {r["group"]: r for r in obj(DATA / "custodian" / "SOURCE_TRUTH.json",
                                       data_seal["members"]["custodian/SOURCE_TRUTH.json"])}
    family = {f["name"]: f["domain"] for f in obj(DATA / "control" / "SOURCE_LICENSE.json",
              data_seal["members"]["control/SOURCE_LICENSE.json"])["synthetic"]["families"]}
    require(len(gold) == 120 and set(gold) == set(cases) and len(truth) == len(pairs) == 100, "EVALUATOR_JOIN")
    outputs = {}
    results = {}
    for arm in ARMS:
        mapped = {r["id"]: r["projection"] for r in predictions[arm]}
        scored = []
        for group in pairs:
            meta = truth[group["group"]]
            for form in ("primary", "companion"):
                uid = group[form]
                if uid is None:
                    continue
                label = gold[uid]
                require(digest(cases[uid].encode()) == label["evidence_sha256"]
                        and label["selector"] == meta["selector"] and label["as_of"] == meta["as_of"], "GOLD_EVIDENCE_JOIN")
                scored.append({**score(mapped[uid], label, meta, cases[uid]), "id": uid, "form": form,
                               "title": "PRESENT" if label["document_title"] else "ABSENT", "category": meta["category"],
                               "family": meta["family"], "domain": family[meta["family"]],
                               "expected_status": label["status"], "expected_reason": label["reason"]})
        require(len(scored) == len({r["id"] for r in scored}) == 120, "EVALUATOR_COVERAGE")
        results[arm] = summarize(scored, pairs)
        primary = results[arm]["main"]
        require(primary["total"] == 100 and primary["answerable"] == 70
                and results[arm]["companion"]["total"] == 20, "EVALUATOR_DENOMINATOR")
        outputs[arm] = scored
    gates = [results[arm]["gate"] for arm in ARMS]
    state = ("INCONCLUSIVE_STOP" if not all(g["no_technical_failure"] for g in gates)
             else "FEASIBILITY_PROVISIONAL_GO" if all(gates[1].values()) else "FEASIBILITY_NO_GO")
    left, right = outputs[ARMS[0]], outputs[ARMS[1]]
    flips = dict(Counter(a["status"] + "->" + b["status"] for a, b in zip(left, right, strict=True)
                         if a["form"] == "primary"))
    require(not DENIED, "EVALUATION_ISOLATION")
    private_sha = write("SCORED_PRIVATE.json", outputs)
    print(write("EVALUATION_AGGREGATE.json", {"status": state, "arms": results, "primary_v1_to_v2": flips,
                "private_sha256": private_sha, "confirmation_sha256": confirmed_sha, "gold_opened_at": gold_opened_at,
                "scored_at": timestamp(), "human_gold": 0, "model_calls": 0, "model_api_calls": 0,
                "new_downloads": 0, "cost_usd": 0, "auto_continue": False}))


def pin(value: str | None) -> str:
    if value is None or len(value) != 64 or any(ch not in "0123456789abcdef" for ch in value):
        raise ValueError("REQUIRED_SHA256")
    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("custody", "preflight", "release", "predict", "confirm", "evaluate"))
    parser.add_argument("--release-sha")
    parser.add_argument("--prediction-sha")
    parser.add_argument("--confirmation-sha")
    args = parser.parse_args()
    require(OUT.resolve(strict=True) == OUT and DATA.resolve(strict=True) == DATA and
            sys.flags.isolated == sys.flags.no_site == 1 and sys.dont_write_bytecode, "PRIVATE_EXECUTION_ENVIRONMENT")
    sys.path.insert(0, str(REPO / "src"))
    stage = args.stage
    if stage in {"confirm", "evaluate"}:
        allowed = {INPUT_FILE, *(OUT / name for name in (*PRED_FILES, "ROLE_FREE.zip", "RELEASE.json",
                   "PREDICTION_SEAL.json")), *(MODULE / n for n in (*RULE_FILES, *LOCAL_FILES))}
        if stage == "evaluate":
            allowed.update({RECEIPT, GOLD_FILE, PROTOCOL_FILE, DATA / "custodian" / "PAIRS.json",
                            DATA / "custodian" / "SOURCE_TRUTH.json", DATA / "control" / "SOURCE_LICENSE.json",
                            OUT / "READONLY_CONFIRMATION.json"})
            guard(allowed, {"E_STARTED.json", "SCORED_PRIVATE.json", "EVALUATION_AGGREGATE.json"})
        else:
            guard(allowed, {"READONLY_CONFIRMATION.json"})
    actions = {"custody": custody, "preflight": preflight, "release": release,
               "predict": lambda: predict(pin(args.release_sha)),
               "confirm": lambda: confirm(pin(args.release_sha), pin(args.prediction_sha)),
               "evaluate": lambda: evaluate(pin(args.release_sha), pin(args.prediction_sha), pin(args.confirmation_sha))}
    actions[stage]()


if __name__ == "__main__":
    main()
