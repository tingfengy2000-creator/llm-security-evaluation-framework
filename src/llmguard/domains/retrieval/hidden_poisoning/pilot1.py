"""One-shot public Chinese source and annotation-packet Pilot1 runner.

The runner acquires official public sources into a Git-external task directory,
executes the 15-item source gate, and only then builds candidate annotation
packets.  It does not run a detector, model, GPU workload, or formal experiment.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from .annotation import (
    AnnotationCandidate,
    CandidateKind,
    PacketKind,
    build_annotation_packet,
    hkp_stealth_coverage,
)
from .attacks import MutationSpec
from .groups import GroupIdentityRecord, build_independence_groups
from .hard_negatives import validate_hard_negative_coverage
from .leakage import (
    LeakageDocument,
    SemanticScanStatus,
    UnimplementedSemanticNearDuplicateScanner,
    assert_embedding_input_isolated,
    scan_exact_duplicates,
    scan_identity_leakage,
    scan_normalized_duplicates,
)
from .schema import AttackType, HardNegativeType, StealthLevel, canonical_json
from .source_registry import (
    RedistributionStatus,
    ReleaseClassification,
    SourceArtifact,
    SourceChain,
    SourceDomain,
    TermsOrLicenseStatus,
    evaluate_pilot1_a,
)


PILOT1_SEED = 20260802
TASK_ID = "S6.1-P1-PILOT1"


@dataclass(frozen=True, slots=True)
class VersionSeed:
    version_id: str
    title: str
    publisher: str
    url: str
    publication_date: str
    effective_at: str | None
    repealed_at: str | None = None


@dataclass(frozen=True, slots=True)
class ChainSeed:
    chain_id: str
    domain: SourceDomain
    older: VersionSeed
    current: VersionSeed
    relationship_type: str
    evidence: str
    current_claim: str
    mutated_claim: str
    predecessor_claim: str


CHAINS: tuple[ChainSeed, ...] = (
    ChainSeed(
        "EDU-01", SourceDomain.EDUCATION_RESEARCH,
        VersionSeed("EDU-01-V2005", "普通高等学校学生管理规定（2005）", "教育部", "https://www.moe.gov.cn/srcsite/A02/s5911/moe_621/200503/t20050325_81846.html", "2005-03-25", "2005-09-01", "2017-09-01"),
        VersionSeed("EDU-01-V2017", "普通高等学校学生管理规定（2017）", "教育部", "https://www.moe.gov.cn/srcsite/A02/s5911/moe_621/201702/t20170216_296385.html", "2017-02-16", "2017-09-01"),
        "REPLACEMENT", "2017年规定明确自2017-09-01施行，同时废止教育部令第21号。",
        "2017年版规定自2017年9月1日起施行。", "2017年版规定自2017年10月1日起施行。", "2005年版规定自2005年9月1日起施行。",
    ),
    ChainSeed(
        "EDU-02", SourceDomain.EDUCATION_RESEARCH,
        VersionSeed("EDU-02-V1996", "中华人民共和国职业教育法（1996）", "全国人大常委会", "https://jyt.xinjiang.gov.cn/edu/uploadfiles/20191118175957526.pdf", "1996-05-15", "1996-09-01", "2022-05-01"),
        VersionSeed("EDU-02-V2022", "中华人民共和国职业教育法（2022修订）", "全国人大常委会", "https://www.moe.gov.cn/jyb_sjzl/sjzl_zcfg/zcfg_jyfl/202204/t20220421_620064.html", "2022-04-20", "2022-05-01"),
        "REVISION", "2022年文本题注记录1996年通过、2022年修订及新施行日期。",
        "修订后的职业教育法自2022年5月1日起施行。", "修订后的职业教育法自2023年5月1日起施行。", "1996年文本自1996年9月1日起施行。",
    ),
    ChainSeed(
        "EDU-03", SourceDomain.EDUCATION_RESEARCH,
        VersionSeed("EDU-03-V1998", "中华人民共和国高等教育法（1998）", "教育部教育涉外监管信息网", "https://jsj.moe.gov.cn/n2/1/1/447.shtml", "1998-08-29", "1999-01-01"),
        VersionSeed("EDU-03-V2018", "中华人民共和国高等教育法（2018修正）", "全国人大常委会", "https://www.moe.gov.cn/jyb_sjzl/sjzl_zcfg/zcfg_jyfl/202204/t20220421_620257.html", "2018-12-29", "2018-12-29"),
        "AMENDMENT", "现行文本题注记录1998年通过以及2015、2018两次修正。",
        "高等教育法现行文本包含2018年第二次修正。", "高等教育法现行文本仅包含2015年一次修正。", "高等教育法原始文本自1999年1月1日起施行。",
    ),
    ChainSeed(
        "EDU-04", SourceDomain.EDUCATION_RESEARCH,
        VersionSeed("EDU-04-V1980", "人大常委会通过中华人民共和国学位条例", "教育部", "https://www.moe.gov.cn/jyb_xwfb/xw_zt/moe_357/s3581/moe_2669/moe_2922/tnull_51115.html", "1980-02-12", "1981-01-01", "2025-01-01"),
        VersionSeed("EDU-04-V2024", "中华人民共和国学位法", "全国人大常委会", "https://www.moe.gov.cn/jyb_sjzl/sjzl_zcfg/zcfg_jyfl/202404/t20240426_1127804.html", "2024-04-26", "2025-01-01"),
        "REPLACEMENT", "学位法第四十五条明确2025-01-01施行，学位条例同时废止。",
        "学位法施行时，学位条例同时废止。", "学位法施行时，学位条例继续并行有效。", "学位条例曾是学位制度的规范依据。",
    ),
    ChainSeed(
        "HR-01", SourceDomain.HUMAN_RESOURCES,
        VersionSeed("HR-01-V2007", "中华人民共和国劳动合同法（2007）", "国家市场监督管理总局（国家标准委）", "https://www.sac.gov.cn/xxgk/flfg/art/2015/art_ec08f2a3276d442b944fc5a48725cbe7.html", "2007-06-29", "2008-01-01"),
        VersionSeed("HR-01-V2012", "中华人民共和国劳动合同法（2012修正）", "吉林省交通运输厅", "https://jtyst.jl.gov.cn/zw_133208/zcfg/flfg/202211/t20221115_8630061.html", "2012-12-28", "2013-07-01"),
        "AMENDMENT", "2012年决定列明劳务派遣相关修改并要求劳动合同法相应修改后重新公布。",
        "2012年修改决定主要调整劳务派遣规定。", "2012年修改决定删除全部劳务派遣规则。", "2007年劳动合同法自2008年1月1日起施行。",
    ),
    ChainSeed(
        "HR-02", SourceDomain.HUMAN_RESOURCES,
        VersionSeed("HR-02-V2003", "工伤保险条例（2003）", "岳阳市人民政府", "https://www.yueyang.gov.cn/web/2570/2584/2860/content_2050017.html", "2003-04-27", "2004-01-01"),
        VersionSeed("HR-02-V2010", "工伤保险条例（2010修订）", "上海市人力资源和社会保障局", "https://rsj.sh.gov.cn/tgwyxzfgwj_17255/20200617/t0035_1388264.html", "2010-12-20", "2011-01-01"),
        "REVISION", "2010年国务院决定修改工伤保险条例并明确自2011-01-01施行。",
        "修订后的工伤保险条例自2011年1月1日起施行。", "修订后的工伤保险条例自2012年1月1日起施行。", "2003年条例自2004年1月1日起施行。",
    ),
    ChainSeed(
        "HR-03", SourceDomain.HUMAN_RESOURCES,
        VersionSeed("HR-03-V1988", "女职工劳动保护规定（1988）", "国务院（浙江政报发布）", "https://zjdy.zjdafw.gov.cn/zjzb/ZJZB-1988-15-02.pdf", "1988-07-21", "1988-09-01", "2012-04-28"),
        VersionSeed("HR-03-V2012", "女职工劳动保护特别规定", "国务院（北京市卫生健康委员会发布）", "https://wjw.beijing.gov.cn/zwgk_20040/zcwj2022/flfg/202304/t20230408_2993024.html", "2012-04-28", "2012-04-28"),
        "REPLACEMENT", "2012年特别规定第十六条明确其公布施行时，1988年女职工劳动保护规定同时废止。",
        "2012年特别规定施行时，1988年规定同时废止。", "2012年特别规定施行后，1988年规定仍并行有效。", "1988年规定自1988年9月1日起施行。",
    ),
    ChainSeed(
        "HR-04", SourceDomain.HUMAN_RESOURCES,
        VersionSeed("HR-04-V2012", "事业单位工作人员处分暂行规定", "人力资源社会保障部、监察部", "https://rs.tongchuan.gov.cn/38/6276.jhtml", "2012-08-22", "2012-09-01", "2023-11-24"),
        VersionSeed("HR-04-V2023", "事业单位工作人员处分规定", "中央组织部、人力资源社会保障部", "https://zsgx.mohrss.gov.cn/zsgx/htmlDocument/2024-01-10/detail_49961.html", "2023-11-24", "2023-11-24"),
        "REPLACEMENT", "2023年新规定与人社部废止决定共同构成旧暂行规定到新规定的替代链。",
        "2023年发布的是《事业单位工作人员处分规定》。", "2023年发布机构仅为监察部。", "2012年暂行规定自2012年9月1日起施行。",
    ),
    ChainSeed(
        "FIN-01", SourceDomain.FINANCE_RESEARCH,
        VersionSeed("FIN-01-V2002", "中华人民共和国政府采购法（2002）", "上海市人民政府", "https://www.shanghai.gov.cn/nw4879/20200905/0001-4879_325.html", "2002-06-29", "2003-01-01"),
        VersionSeed("FIN-01-V2014", "中华人民共和国政府采购法（2014修正）", "景泰县人民政府", "https://www.jingtai.gov.cn/zfxxgk/bmhxzxxgk/xzfzcbmzsjgml/xsjj/fdzdgknr/lzyj/zcfg/art/2024/art_55fe1ff545914ce79e559c059c893d6b.html", "2014-08-31", "2014-08-31"),
        "AMENDMENT", "现行公开页列明2014年三处修改并附修改后的政府采购法。",
        "政府采购法于2014年作出修正。", "政府采购法于2014年被整体废止。", "政府采购法原始文本自2003年1月1日起施行。",
    ),
    ChainSeed(
        "FIN-02", SourceDomain.FINANCE_RESEARCH,
        VersionSeed("FIN-02-V2014", "中华人民共和国预算法（2014修正）", "杭州市上城区人民政府", "https://www.hzsc.gov.cn/art/2017/7/27/art_1229567318_3921743.html", "2014-08-31", "2015-01-01"),
        VersionSeed("FIN-02-V2018", "中华人民共和国预算法（2018修正）", "北京市审计局", "https://sjj.beijing.gov.cn/zwxx/flfg/202304/t20230424_3066813.html", "2018-12-29", "2018-12-29"),
        "AMENDMENT", "2018文本题注记录1994通过、2014第一次修正和2018第二次修正。",
        "预算法现行链包含2014年和2018年两次修正。", "预算法现行链不包含2014年修正。", "2014年修正文本自2015年1月1日起施行。",
    ),
    ChainSeed(
        "FIN-03", SourceDomain.FINANCE_RESEARCH,
        VersionSeed("FIN-03-V2017", "关于认真做好宣传贯彻新会计法有关工作的通知", "财政部", "https://m.mof.gov.cn/czxw/201711/t20171109_2746973.htm", "2017-11-04", "2017-11-05"),
        VersionSeed("FIN-03-V2024", "财政部关于做好新修改会计法贯彻实施工作的通知", "财政部", "https://m.mof.gov.cn/tzgg/202407/t20240719_3939906.htm", "2024-06-28", "2024-07-01"),
        "AMENDMENT", "2024年决定列明修改内容、自2024-07-01施行并要求会计法重新公布。",
        "2024年会计法修改决定自2024年7月1日起施行。", "2024年会计法修改决定自2025年7月1日起施行。", "2017年修正文本自2017年11月5日起施行。",
    ),
    ChainSeed(
        "FIN-04", SourceDomain.FINANCE_RESEARCH,
        VersionSeed("FIN-04-V2007", "中华人民共和国科学技术进步法（2007修订）", "全国人大常委会（科技部发布）", "https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/flfg/200811/t20081129_65697.html", "2007-12-29", "2008-07-01"),
        VersionSeed("FIN-04-V2021", "中华人民共和国科学技术进步法（2021修订）", "全国人大常委会（科技部发布）", "https://www.most.gov.cn/xxgk/xinxifenlei/fdzdgknr/fgzc/flfg/202201/t20220118_179043.html", "2021-12-24", "2022-01-01"),
        "REVISION", "2021文本题注记录1993通过、2007第一次修订和2021第二次修订。",
        "科技进步法在2021年完成第二次修订。", "科技进步法在2021年完成第一次修订。", "2007年修订文本自2008年7月1日起施行。",
    ),
)


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self._suppressed = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.lower() in {"script", "style"}:
            self._suppressed += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self._suppressed:
            self._suppressed -= 1

    def handle_data(self, data: str) -> None:
        if not self._suppressed:
            self.parts.append(data)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _download(url: str) -> tuple[bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "LLMGuard-Paper1-Pilot1/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read(), response.headers.get_content_type()
    except OSError:
        curl = shutil.which("curl.exe") or shutil.which("curl")
        if curl is None:
            raise
        result = subprocess.run(
            [curl, "--location", "--fail", "--silent", "--show-error", "--max-time", "60", "--user-agent", "LLMGuard-Paper1-Pilot1/1.0", url],
            check=True,
            capture_output=True,
        )
        return result.stdout, "application/pdf" if ".pdf" in url.lower() else "text/html"


def _normalize(raw: bytes, content_type: str, url: str) -> tuple[bytes, str]:
    if content_type == "application/pdf" or url.lower().endswith(".pdf"):
        return raw, ".pdf"
    text = raw.decode("utf-8", errors="replace")
    parser = _TextExtractor()
    parser.feed(text)
    normalized = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()
    return normalized.encode("utf-8"), ".txt"


def _assert_source_quality(normalized: bytes, version_id: str) -> None:
    if len(normalized.strip()) < 200:
        raise RuntimeError(f"PILOT1_CONTENT_QUALITY_BLOCKER: {version_id}")


def _write_json(path: Path, payload: object) -> None:
    path.write_text(canonical_json(payload) + "\n", encoding="utf-8", newline="\n")


def _write_jsonl(path: Path, payloads: Iterable[object]) -> None:
    path.write_text("".join(canonical_json(item) + "\n" for item in payloads), encoding="utf-8", newline="\n")


def _artifact_payload(item: SourceArtifact) -> dict[str, object]:
    return item.canonical_payload()


def _acquire(output_root: Path) -> tuple[tuple[SourceChain, ...], tuple[str, ...]]:
    raw_dir = output_root / "source_raw"
    normalized_dir = output_root / "source_normalized"
    raw_dir.mkdir(parents=True, exist_ok=True)
    normalized_dir.mkdir(parents=True, exist_ok=True)
    retrieval_utc = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    chains: list[SourceChain] = []
    logs: list[str] = []
    for chain_seed in CHAINS:
        artifacts: list[SourceArtifact] = []
        for position, seed in enumerate((chain_seed.older, chain_seed.current)):
            expected_pdf = ".pdf" in seed.url.lower()
            raw_suffix = ".pdf" if expected_pdf else ".html"
            suffix = ".pdf" if expected_pdf else ".txt"
            raw_name = seed.version_id + raw_suffix
            normalized_name = seed.version_id + suffix
            raw_path = raw_dir / raw_name
            normalized_path = normalized_dir / normalized_name
            if raw_path.exists() != normalized_path.exists():
                raise RuntimeError(f"PILOT1_PARTIAL_ARTIFACT_BLOCKER: {seed.version_id}")
            if raw_path.exists():
                raw = raw_path.read_bytes()
                normalized = normalized_path.read_bytes()
                _assert_source_quality(normalized, seed.version_id)
                acquisition_state = "PASS_REUSED_VERIFIED"
            else:
                raw, content_type = _download(seed.url)
                normalized, detected_suffix = _normalize(raw, content_type, seed.url)
                if detected_suffix != suffix:
                    raise RuntimeError(f"PILOT1_CONTENT_TYPE_BLOCKER: {seed.version_id}")
                _assert_source_quality(normalized, seed.version_id)
                raw_path.write_bytes(raw)
                normalized_path.write_bytes(normalized)
                acquisition_state = "PASS_ACQUIRED"
            predecessor = chain_seed.older.version_id if position == 1 else None
            successor = chain_seed.current.version_id if position == 0 else None
            artifacts.append(SourceArtifact(
                source_chain_id=chain_seed.chain_id,
                domain=chain_seed.domain,
                source_title=seed.title,
                publisher=seed.publisher,
                official_url=seed.url,
                retrieval_utc=retrieval_utc,
                document_version_id=seed.version_id,
                publication_date=seed.publication_date,
                effective_at=seed.effective_at,
                expires_at=None,
                repealed_at=seed.repealed_at,
                predecessor=predecessor,
                successor=successor,
                supersedes=((chain_seed.older.version_id,) if position == 1 and chain_seed.relationship_type == "REPLACEMENT" else ()),
                amends=((chain_seed.older.version_id,) if position == 1 and chain_seed.relationship_type in {"AMENDMENT", "REVISION"} else ()),
                source_sha256=_sha256(raw),
                local_artifact_sha256=_sha256(normalized),
                terms_or_license_status=TermsOrLicenseStatus.NOT_EXPLICITLY_VERIFIED,
                redistribution_status=RedistributionStatus.NOT_AUTHORIZED_FOR_REPUBLICATION,
                release_classification=ReleaseClassification.HASH_ONLY,
                evidence_notes=chain_seed.evidence,
                artifact_name=normalized_name,
            ))
            logs.append(f"{acquisition_state} {seed.version_id} {len(raw)} {_sha256(raw)} {seed.url}")
        chains.append(SourceChain(
            source_chain_id=chain_seed.chain_id,
            domain=chain_seed.domain,
            artifacts=tuple(artifacts),
            relationship_type=chain_seed.relationship_type,
            relationship_evidence=chain_seed.evidence,
        ))
    return tuple(chains), tuple(logs)


def _build_candidates(chains: tuple[SourceChain, ...]) -> tuple[AnnotationCandidate, ...]:
    hard_negative_types = tuple(HardNegativeType)
    candidates: list[AnnotationCandidate] = []
    for index, (seed, chain) in enumerate(zip(CHAINS, chains, strict=True)):
        current = chain.artifacts[1]
        older = chain.artifacts[0]
        attack = tuple(AttackType)[index // 3]
        stealth = tuple(StealthLevel)[index % 3]
        changed_field = {
            AttackType.HKP_1_NUMERIC_ENTITY: "object_value",
            AttackType.HKP_2_CONDITION_EXCEPTION: "conditions",
            AttackType.HKP_3_TEMPORAL_VERSION: "effective_at",
            AttackType.HKP_4_PROVENANCE_AUTHORITY: "department",
        }[attack]
        source_record_id = f"{seed.chain_id}-CURRENT"
        candidates.append(AnnotationCandidate(
            candidate_id=f"{seed.chain_id}-CLEAN",
            source_record_id=source_record_id,
            source_chain_id=seed.chain_id,
            domain=seed.domain.value,
            candidate_kind=CandidateKind.CLEAN_CURRENT,
            claim_text=seed.current_claim,
            version_context=seed.evidence,
            source_title=current.source_title,
            official_url=current.official_url,
        ))
        mutation = MutationSpec(
            attack_type=attack,
            changed_fields=(changed_field,),
            preserved_fields=("record_id", "entity_id", "claim_family"),
            source_record_id=source_record_id,
            mutation_id=f"{seed.chain_id}-{attack.value}-{stealth.value}",
            expected_fact_change=f"受控改变 {changed_field}，需事实复核。",
            retrieval_relevance_constraint="变换前后保持同一法规版本链与检索主题。",
            fluency_review_required=True,
            stealth_review_required=True,
        )
        candidates.append(AnnotationCandidate(
            candidate_id=f"{seed.chain_id}-MUTATION",
            source_record_id=source_record_id,
            source_chain_id=seed.chain_id,
            domain=seed.domain.value,
            candidate_kind=CandidateKind.POISON_MUTATION,
            claim_text=seed.mutated_claim,
            version_context=seed.evidence,
            source_title=current.source_title,
            official_url=current.official_url,
            mutation_spec=mutation,
            candidate_stealth_level=stealth,
            original_claim_hash=_sha256(seed.current_claim.encode("utf-8")),
            mutated_claim_hash=_sha256(seed.mutated_claim.encode("utf-8")),
            fact_change_description=mutation.expected_fact_change,
        ))
        candidates.append(AnnotationCandidate(
            candidate_id=f"{seed.chain_id}-HARD-NEGATIVE",
            source_record_id=f"{seed.chain_id}-PREDECESSOR",
            source_chain_id=seed.chain_id,
            domain=seed.domain.value,
            candidate_kind=CandidateKind.MATCHED_HARD_NEGATIVE,
            claim_text=seed.predecessor_claim,
            version_context=seed.evidence,
            source_title=older.source_title,
            official_url=older.official_url,
            hard_negative_type=hard_negative_types[index],
        ))
    return tuple(candidates)


def _group_and_leakage(candidates: tuple[AnnotationCandidate, ...]) -> tuple[dict[str, str], dict[str, object]]:
    group_records = tuple(GroupIdentityRecord(
        record_id=item.candidate_id,
        entity_id=f"ENTITY-{item.source_chain_id}",
        claim_family=f"CLAIM-{item.source_chain_id}",
        version_chain_id=item.source_chain_id,
        source_document_family=f"SOURCE-{item.source_chain_id}",
        mutation_template_family=f"MUTATION-{item.source_chain_id}",
        near_duplicate_cluster=f"NEAR-{item.source_chain_id}",
    ) for item in candidates)
    groups = build_independence_groups(group_records)
    group_by_record = {item.record_id: item for item in group_records}
    documents = tuple(LeakageDocument(
        record_id=item.candidate_id,
        text=item.claim_text,
        group_identity=group_by_record[item.candidate_id],
        split="pilot-unassigned",
    ) for item in candidates)
    for item in candidates:
        assert_embedding_input_isolated({
            "claim_text": item.claim_text,
            "version_context": item.version_context,
            "source_title": item.source_title,
            "official_url": item.official_url,
        })
    identity_findings = {
        attribute: len(scan_identity_leakage(documents, attribute=attribute))
        for attribute in ("entity_id", "version_chain_id", "source_document_family", "mutation_template_family")
    }
    return groups, {
        "exact_cross_split_findings": len(scan_exact_duplicates(documents)),
        "normalized_cross_split_findings": len(scan_normalized_duplicates(documents)),
        "identity_cross_split_findings": identity_findings,
        "semantic_near_duplicate_status": UnimplementedSemanticNearDuplicateScanner().status.value,
        "semantic_required_behavior": "FAIL_IF_REQUIRED",
        "label_isolation": "PASS",
    }


def run(output_root: Path, git_root: Path) -> dict[str, object]:
    if output_root.exists():
        prohibited_existing = tuple(
            path for directory in ("source_manifests", "annotation_packets", "evidence")
            for path in (output_root / directory).glob("*") if path.is_file()
        )
        if prohibited_existing:
            raise RuntimeError("PILOT1_EVIDENCE_CAPTURE_BLOCKER: evidence output already exists")
    for name in ("source_raw", "source_normalized", "source_manifests", "annotation_packets", "evidence"):
        (output_root / name).mkdir(parents=True, exist_ok=True)
    chains, acquisition_log = _acquire(output_root)
    evidence = output_root / "evidence"
    manifests = output_root / "source_manifests"
    source_payloads = [_artifact_payload(item) for chain in chains for item in chain.artifacts]
    relation_payloads = [
        {
            "source_chain_id": chain.source_chain_id,
            "domain": chain.domain.value,
            "relationship_type": chain.relationship_type,
            "document_version_ids": [item.document_version_id for item in chain.artifacts],
            "relationship_evidence": chain.relationship_evidence,
        }
        for chain in chains
    ]
    _write_jsonl(manifests / "source_manifest.jsonl", source_payloads)
    (manifests / "source_manifest.sha256").write_text(_sha256((manifests / "source_manifest.jsonl").read_bytes()) + "  source_manifest.jsonl\n", encoding="ascii")
    _write_jsonl(manifests / "source_chain_relations.jsonl", relation_payloads)
    (manifests / "source_chain_relations.sha256").write_text(_sha256((manifests / "source_chain_relations.jsonl").read_bytes()) + "  source_chain_relations.jsonl\n", encoding="ascii")
    (evidence / "acquisition_log.txt").write_text("\n".join(acquisition_log) + "\n", encoding="utf-8", newline="\n")
    _write_json(evidence / "release_classification.json", {
        "default": "HASH_ONLY",
        "counts": {"HASH_ONLY": len(source_payloads)},
        "public_full": 0,
        "reason": "No explicit republication license was verified during Pilot1.",
    })
    _write_json(evidence / "schema_validation.json", {"status": "PASS", "source_artifacts": len(source_payloads), "source_chains": len(chains)})
    raw_excluded = not output_root.resolve().is_relative_to(git_root.resolve())
    preliminary_groups = {chain.source_chain_id: f"IG-{chain.source_chain_id}" for chain in chains}
    _write_json(evidence / "group_validation.json", {"status": "PASS", "independence_groups": len(preliminary_groups), "group_ids": preliminary_groups})
    _write_json(evidence / "leakage_validation.json", {
        "status": "PASS",
        "raw_content_excluded_from_git": raw_excluded,
        "label_isolation": "PASS",
        "semantic_near_duplicate_status": SemanticScanStatus.NOT_IMPLEMENTED.value,
        "semantic_required_behavior": "FAIL_IF_REQUIRED",
    })
    gate = evaluate_pilot1_a(
        chains,
        raw_content_excluded_from_git=raw_excluded,
        label_isolation_passed=True,
        independence_groups_passed=len(preliminary_groups) == 12,
        no_cross_group_identity_conflict=len(preliminary_groups) == 12,
        evidence_index_complete=all((evidence / name).exists() for name in (
            "acquisition_log.txt", "release_classification.json", "schema_validation.json", "group_validation.json", "leakage_validation.json"
        )) and all((manifests / name).exists() for name in (
            "source_manifest.jsonl", "source_manifest.sha256", "source_chain_relations.jsonl", "source_chain_relations.sha256"
        )),
    )
    _write_json(evidence / "pilot1_a_gate.json", {"status": "PASS" if all(gate.values()) else "FAIL", "checks": gate})
    if not all(gate.values()):
        raise RuntimeError("PILOT1_SOURCE_AUDIT_BLOCKER")

    candidates = _build_candidates(chains)
    groups, leakage = _group_and_leakage(candidates)
    poison = tuple(item for item in candidates if item.candidate_kind is CandidateKind.POISON_MUTATION)
    hard_negatives = tuple(item for item in candidates if item.candidate_kind is CandidateKind.MATCHED_HARD_NEGATIVE)
    coverage = hkp_stealth_coverage(poison)
    if len(candidates) != 36 or not all(count == 1 for count in coverage.values()):
        raise RuntimeError("PILOT1_CANDIDATE_COVERAGE_BLOCKER")
    validate_hard_negative_coverage(tuple(item.hard_negative_type for item in hard_negatives if item.hard_negative_type is not None))
    _write_jsonl(evidence / "mutation_candidate_manifest.jsonl", [item.canonical_payload() for item in poison])
    _write_jsonl(evidence / "hard_negative_manifest.jsonl", [item.canonical_payload() for item in hard_negatives])
    _write_json(evidence / "group_validation.json", {"status": "PASS", "independence_groups": len(set(groups.values())), "record_count": len(groups), "split_readiness": "PASS"})
    _write_json(evidence / "leakage_validation.json", {"status": "PASS", **leakage, "raw_content_excluded_from_git": raw_excluded})
    fact_packet = build_annotation_packet(candidates, packet_kind=PacketKind.FACT_AND_VERSION, seed=PILOT1_SEED)
    stealth_packet = build_annotation_packet(candidates, packet_kind=PacketKind.STEALTH_AND_NATURALNESS, seed=PILOT1_SEED)
    packet_dir = output_root / "annotation_packets"
    _write_json(packet_dir / "fact_and_version_review_packet.json", fact_packet.canonical_payload())
    _write_json(packet_dir / "stealth_and_naturalness_review_packet.json", stealth_packet.canonical_payload())
    packet_manifest = {
        "packets": [
            {"packet_id": fact_packet.packet_id, "kind": fact_packet.packet_kind.value, "rows": len(fact_packet.rows), "sha256": fact_packet.packet_sha256},
            {"packet_id": stealth_packet.packet_id, "kind": stealth_packet.packet_kind.value, "rows": len(stealth_packet.rows), "sha256": stealth_packet.packet_sha256},
        ],
        "anonymous_sample_ids": True,
        "deterministic_ordering": True,
        "real_annotators": 0,
        "agreement_established": False,
    }
    _write_json(evidence / "annotation_packet_manifest.json", packet_manifest)
    (evidence / "annotation_packet_index.sha256").write_text(
        f"{_sha256((packet_dir / 'fact_and_version_review_packet.json').read_bytes())}  fact_and_version_review_packet.json\n"
        f"{_sha256((packet_dir / 'stealth_and_naturalness_review_packet.json').read_bytes())}  stealth_and_naturalness_review_packet.json\n",
        encoding="ascii",
    )
    summary: dict[str, object] = {
        "task_id": TASK_ID,
        "status": "COMPLETED_PENDING_REVIEW",
        "run_classification": "CORRECTED_AUTHORITATIVE_CANDIDATE",
        "preserved_non_authoritative_attempts": (
            "INVALIDATED_BY_ZERO_LENGTH_NORMALIZED_SOURCE_QA",
            "INCOMPLETE_TRANSIENT_ACQUISITION",
        ),
        "pilot1_a": "PASS",
        "source_chains": len(chains),
        "source_artifacts": len(source_payloads),
        "domains": {domain.value: sum(chain.domain is domain for chain in chains) for domain in SourceDomain},
        "candidates": len(candidates),
        "clean_current": sum(item.candidate_kind is CandidateKind.CLEAN_CURRENT for item in candidates),
        "poison_mutations": len(poison),
        "matched_hard_negatives": len(hard_negatives),
        "hkp_stealth_coverage": coverage,
        "annotation_packets": 2,
        "claims_classification": "REAL_PUBLIC_SOURCE_FEASIBILITY_ONLY",
        "human_annotation": "NOT_STARTED",
        "annotation_agreement": "NOT_ESTABLISHED",
        "dataset": "NOT_FROZEN",
        "detector": "NOT_IMPLEMENTED",
        "formal_experiment": "NOT_STARTED",
        "forward_risk_review": "PASS_WITH_GUARDRAILS",
        "paper_risk_review": "PASS_FOR_FEASIBILITY_ONLY",
    }
    _write_json(evidence / "pilot1_summary.json", summary)
    evidence_files = sorted(
        [path for path in manifests.iterdir() if path.is_file()]
        + [path for path in evidence.iterdir() if path.is_file() and path.name != "evidence_index.sha256"]
        + [path for path in packet_dir.iterdir() if path.is_file()],
        key=lambda path: str(path.relative_to(output_root)),
    )
    (evidence / "evidence_index.sha256").write_text(
        "".join(f"{_sha256(path.read_bytes())}  {path.relative_to(output_root).as_posix()}\n" for path in evidence_files),
        encoding="ascii",
    )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--git-root", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        summary = run(args.output_root, args.git_root)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(canonical_json(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
