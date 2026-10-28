"""VACE-Lite F5: closed, span-grounded rules, not unrestricted Chinese NLI.

No file access, labels, construction metadata, learned classifier or ID routing.
Unknown scope/versions are deliberately not guessed. A certificate is a typed
derivation plus exact source spans, never an A0 flag or similarity threshold.
"""
from __future__ import annotations

import hashlib
import itertools
import re
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Callable

from .surface_baseline import GENERAL, ORIGINAL

VERSION = "VACE-LITE-V03-F5-RULES-1"
VERDICTS = ("SUPPORT", "CONTRADICT", "INSUFFICIENT")
SLOTS = ("subject", "predicate", "value_unit", "scope", "time_version", "source_role")
NUM = r"\d+(?:\.\d+)?"
CN = r"[一二三四五六七八九十百零〇\d]+"
DATE = r"\d{4}年\d{1,2}月\d{1,2}日"
ROLE = r"国务院|人力资源(?:和)?社会保障部|劳动(?:和社会保障)?部|全国人民代表大会常务委员会"
QUOTE_RISK = re.compile(r"有人(?:说|认为)|错误观点|假设|假如|据称|声称|原话|引述|不意味着|并非|不能据此")
SCOPE_RISK = re.compile(r"如果|若|除非|除.{0,15}外|但是|但在|特殊|例外|一般|通常|至少|至多|不超过|不少于|不满|以上|以下")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text).replace("（", "(").replace("）", ")")


def canonical_title(text: str) -> str:
    return re.sub(r"[《》〈〉<>]", "", compact(text)).removeprefix("中华人民共和国")


def number(text: str) -> float:
    if re.fullmatch(NUM, text):
        return float(text)
    digits = {c: i for i, c in enumerate("零一二三四五六七八九")}
    if "十" in text:
        a, b = text.split("十", 1)
        return float((digits.get(a, 1) * 10) + digits.get(b, 0))
    return float(digits[text])


@dataclass(frozen=True)
class Span:
    source_id: str
    start: int
    end: int
    text: str
    text_sha256: str


def span(source: str, text: str, start: int, end: int) -> Span:
    return Span(source, start, end, text[start:end], digest(text[start:end]))


def compact_span(source: str, raw: str, start: int, end: int) -> Span:
    """Convert whitespace-free regex offsets back into the immutable raw text."""
    indexes = [i for i, c in enumerate(raw) if not c.isspace()]
    return span(source, raw, indexes[start], indexes[end - 1] + 1)


@dataclass(frozen=True)
class Atom:
    predicate: str
    subject: str
    value: str
    unit: str
    scope: str
    version: str
    witness: Span
    functional: bool = True


@dataclass(frozen=True)
class Evidence:
    uid: str
    title: str
    text: str
    text_sha256: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if digest(self.text) != self.text_sha256:
            raise ValueError("EVIDENCE_HASH_MISMATCH")
        allowed = {"issuer", "publisher", "authority_role", "publication_date", "effective_start", "effective_end", "current_history_role", "supersedes", "superseded_by", "source_family", "metadata_confidence"}
        if set(self.metadata) - allowed:
            raise ValueError("FORBIDDEN_EVIDENCE_METADATA")


@dataclass
class Extraction:
    text: str
    slots: dict[str, dict[str, Any]]
    atoms: list[Atom]
    titles: list[str]
    version_years: list[str]
    coverage_complete: bool = False
    issues: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Proof:
    rule_id: str
    conclusion: str
    candidate_sha256: str
    witnesses: tuple[Span, ...]
    premises: dict[str, Any]


def validate_proof(proof: Proof, candidate: str, sources: dict[str, str]) -> bool:
    if proof.conclusion not in VERDICTS[:2] or proof.candidate_sha256 != digest(candidate):
        return False
    if not proof.witnesses or not proof.premises.get("binding_verified"):
        return False
    for w in proof.witnesses:
        raw = sources.get(w.source_id)
        if raw is None or not (0 <= w.start < w.end <= len(raw)):
            return False
        if raw[w.start:w.end] != w.text or digest(w.text) != w.text_sha256:
            return False
    allowed = {"I_ENTITLEMENT_POLARITY", "I_REPEATED_POLARITY", "I_FUNCTIONAL_EXACT_VALUES", "F_WHOLE_ARTICLE_PAYLOAD_EXACT", "F_FUNCTIONAL_SAME_SCOPE_VALUE", "P_ROLE_BOUND_ORDER", "J_TWO_VERSION_FUNCTIONAL_COMPARISON"}
    if proof.rule_id not in allowed:
        return False
    if proof.rule_id.startswith("I_") and internal_proof(extract(candidate)) != proof:
        return False
    return True


# Narrow numeric grammars. Each relation has its own functional scope, not a
# global bag of numbers. Exceptions and article/version binding are checked later.
NUMERIC_RULES = (
    ("WORK_DAILY_HOURS", rf"每日工作(?P<v>{NUM})小时", "小时", "daily_standard"),
    ("WORK_WEEKLY_HOURS", rf"每周工作(?P<v>{NUM})小时", "小时", "weekly_standard"),
    ("DISPATCH_LIMIT", rf"被派遣劳动者数量不得超过其用工总量的(?P<v>{NUM})%", "%", "dispatch_share_upper_bound"),
    ("TEMP_POST_DURATION", rf"临时性工作岗位是指存续时间不超过(?P<v>{NUM})个月的岗位", "月", "temporary_post_upper_bound"),
    ("PREGNANCY_NIGHT_THRESHOLD", rf"怀孕(?P<v>{NUM})个月以上的女职工[^。；]{{0,32}}不得[^。；]{{0,20}}夜班", "月", "pregnancy_night_ban_threshold"),
    ("REGISTRATION_DEADLINE", rf"(?P<s>个人社会保险登记|变更、注销社会保险登记|变更或者注销社会保险登记|个人登记)[^。；]{{0,40}}?(?P<v>{NUM})个工作日内[^。；]{{0,10}}办(?:理)?完毕", "工作日", "registration"),
    ("DISABILITY_MONTHS", rf"(?P<s>[一二三四五六七八九十]+级)伤残为(?P<v>{NUM})个月的本人工资", "月本人工资", "disability_grade"),
    ("ANNUAL_LEAVE", rf"累计工作(?P<s>已满{NUM}年|满{NUM}年不满{NUM}年)的?[^。；]{{0,6}}年休假(?P<v>{NUM})天", "天", "work_tenure"),
)


def _document_version(title: str, text: str) -> str:
    explicit = re.search(r"(\d{4})(?:年)?(?:修订|原版|修正|版)", compact(title))
    if explicit:
        return explicit[1]
    # Derive only from the law's normative chronology header, never footer years.
    head = compact(text).split("第一条", 1)[0]
    events = re.findall(r"(\d{4})年\d+月\d+日[^()]{0,160}?(?:修订|修正)", head)
    return events[-1] if events else "UNKNOWN"


def extract(text: str, source_id: str = "candidate", title: str = "") -> Extraction:
    clean = compact(text)
    titles = re.findall(r"《([^》]+)》", text)
    primary = canonical_title(title or (titles[0] if titles else ""))
    years = list(dict.fromkeys(re.findall(r"(\d{4})年?(?:修订|修正|原版|版)", clean)))
    version = _document_version(title, text) if title else (years[0] if len(years) == 1 else "UNKNOWN")
    slots: dict[str, dict[str, Any]] = {}
    patterns = {
        "subject": r"《[^》]+》|同一(?:职工|劳动者|文件|规定|办法)|职工|用人单位|劳动者",
        "predicate": r"规定|享受|享有|施行|生效|修订|修正|公布|发布|通过|制定|工作|办理",
        "value_unit": rf"{NUM}(?:个工作日|个月|小时|天|年|元|%|％)",
        "scope": r"累计工作[^，。；]+|如果[^，。；]+|除[^。；]+外|不得|不享受|不享有|应当|可以|必须|不需要",
        "time_version": rf"{DATE}|\d{{4}}年?(?:修订|版|修正)|现行|历史|旧版|新版|替代|废止|第{CN}次修订",
        "source_role": rf"(?:{ROLE})[^。；]{{0,20}}(?:通过|公布|发布|制定|修订|修正|转载)|(?:由|以)(?:{ROLE})",
    }
    for key in SLOTS:
        matches = list(re.finditer(patterns[key], clean))
        slots[key] = {
            "status": "OBSERVED" if matches else ("UNRESOLVED" if key in {"subject", "predicate"} else "NOT_STATED"),
            "spans": [asdict(compact_span(source_id, text, m.start(), m.end())) for m in matches],
            "error_reason": None if matches else "NO_SUPPORTED_CLOSED_GRAMMAR_BINDING",
        }
    atoms = []
    for rule, expression, unit, default_scope in NUMERIC_RULES:
        for m in re.finditer(expression, clean):
            scope = m.groupdict().get("s") or default_scope
            atoms.append(Atom(rule, primary, m["v"], unit, scope, version, compact_span(source_id, text, m.start(), m.end())))
    # A normative header binds its exact order to its own promulgating organ;
    # the host and the page publisher never enter this grammar.
    for m in re.finditer(rf"(?P<s>{ROLE})令第(?P<v>{CN})号", clean):
        atoms.append(Atom("PROMULGATING_ORDER", primary, m["s"], "organ", m["v"], version, compact_span(source_id, text, m.start(), m.end())))
    for m in re.finditer(rf"(?P<d>{DATE})(?P<v>{ROLE})第(?P<s>{CN})次常务会议通过", clean):
        atoms.append(Atom("ADOPTING_MEETING", primary, m["v"], "organ", m["d"] + "|" + m["s"], version, compact_span(source_id, text, m.start(), m.end())))
    issues = []
    if QUOTE_RISK.search(clean):
        issues.append("ASSERTION_OR_QUOTATION_SCOPE_UNRESOLVED")
    if not primary:
        issues.append("DOCUMENT_IDENTITY_UNRESOLVED")
    return Extraction(text, slots, atoms, titles, years, issues=issues)


def internal_proof(e: Extraction) -> Proof | None:
    """Prove only restricted unambiguous local assertions; inspect without A0 too."""
    text = compact(e.text)
    if QUOTE_RISK.search(text) or "“" in text or '"' in text:
        return None
    # Scoped paired entitlement. Prefix must identify exactly one explicit person
    # (同一/该职工 with a named normative subject); no different times or conditions.
    pattern = r"(?P<a>既)?(?P<pos>享受|享有)(?P<o>当年年休假|年休假)[，、]?(?:也|又|同时)?(?P<neg>不享受|不享有)(?P=o)"
    m = re.search(pattern, text)
    if m and ("同一职工" in text or "该职工" in text):
        prefix = text[:m.start()]
        if not re.search(r"分别|不同|另一|前一年|次年|去年|今年.*明年", text):
            witness = compact_span("candidate", e.text, m.start(), m.end())
            return Proof("I_ENTITLEMENT_POLARITY", "CONTRADICT", digest(e.text), (witness,), {
                "binding_verified": True, "subject_binding": prefix,
                "predicate": "annual_leave_entitlement", "scope_binding": "single_subject_single_assertion_scope",
                "positive_and_negative_assertions": True,
            })
    # Fully repeated declaratives (also catches contradictions with no A0 cue).
    sentences = list(re.finditer(r"[^。；！？]+", text))
    parsed: list[tuple[re.Match[str], re.Match[str]]] = []
    for s in sentences:
        p = re.fullmatch(r"(?P<ctx>.+?)(?P<pol>不享受|不享有|享受|享有)(?P<obj>年休假|当年年休假)", s[0])
        if p and not SCOPE_RISK.search(p["ctx"]):
            parsed.append((s, p))
    for (s1, p1), (s2, p2) in itertools.combinations(parsed, 2):
        if p1["ctx"] == p2["ctx"] and p1["obj"] == p2["obj"] and p1["pol"].startswith("不") != p2["pol"].startswith("不"):
            return Proof("I_REPEATED_POLARITY", "CONTRADICT", digest(e.text), tuple(compact_span("candidate", e.text, s.start(), s.end()) for s in (s1, s2)), {
                "binding_verified": True, "same_context": p1["ctx"], "scope": "identical_explicit_context",
            })
    # Exact functional numeric statements need an explicit common context. No
    # inference of same applicability merely from two different numbers.
    for a, b in itertools.combinations(e.atoms, 2):
        if (a.predicate, a.subject, a.scope, a.unit, a.version) != (b.predicate, b.subject, b.scope, b.unit, b.version):
            continue
        if a.value == b.value or a.unit == "organ" or not a.subject:
            continue
        if "同一" not in text or re.search(r"不同|分别|旧|新|\d{4}年|至少|至多|以上|以下|例外|一般|如果|若|条件|岗位|除|但|允许", text):
            continue
        # Only repeated copies of the identical functional wording, joined by
        # an explicit conjunction. Different clause contexts are not merged.
        normalized_a = compact(a.witness.text).replace(a.value, "<VALUE>")
        normalized_b = compact(b.witness.text).replace(b.value, "<VALUE>")
        between = compact(e.text[a.witness.end:b.witness.start])
        if normalized_a != normalized_b or not re.fullmatch(r"[，、；]?(?:也|又|同时|且|并且)", between):
            continue
        # Full sentence must explicitly concern one shared functional property.
        return Proof("I_FUNCTIONAL_EXACT_VALUES", "CONTRADICT", digest(e.text), (a.witness, b.witness), {
            "binding_verified": True, "predicate": a.predicate, "subject": a.subject,
            "scope": a.scope, "unit": a.unit, "explicit_same_object": True,
            "values": [a.value, b.value],
        })
    return None


def _law_binding(e: Extraction, doc: Evidence) -> bool:
    if not e.titles:
        return False
    title = canonical_title(e.titles[0])
    doc_title = canonical_title(re.sub(r"[（(].*?[）)]", "", doc.title))
    # Generic gazettes/search pages cannot inherit every title in their body.
    return title == doc_title


def _current_role(doc: Evidence) -> str:
    return str(doc.metadata.get("current_history_role", "UNKNOWN"))


def _compatible_version(e: Extraction, doc: Evidence, expanded: bool) -> bool:
    v = _document_version(doc.title, doc.text)
    if e.version_years:
        return len(e.version_years) == 1 and expanded and v == e.version_years[0]
    # Do not infer currentness from newest year or lookup absence. A sole known
    # historical document never refutes an unversioned normative assertion.
    return _current_role(doc) == "CURRENT"


def _full_literal_support(e: Extraction, doc: Evidence) -> Proof | None:
    text = compact(e.text)
    # Whole payload, after a fully parsed title/article citation, must literally
    # occur inside that exact article, without deleting any condition or negation.
    m = re.fullmatch(r"《[^》]+》(?P<art>第[一二三四五六七八九十百零\d]+条)(?:规定|明确规定|明确)?[：:]?(?P<p>.+?)[。]?", text)
    if not m or any(e.slots[k]["status"] == "OBSERVED" for k in ("time_version", "source_role")):
        return None
    raw = compact(doc.text)
    art = re.search(re.escape(m["art"]) + r"(?P<body>.*?)(?=第[一二三四五六七八九十百零\d]+条|$)", raw)
    if not art:
        return None
    payload = m["p"].rstrip("。")
    pos = raw.find(payload, art.start("body"), art.end("body"))
    if pos < 0:
        return None
    return Proof("F_WHOLE_ARTICLE_PAYLOAD_EXACT", "SUPPORT", digest(e.text), (
        span("candidate", e.text, 0, len(e.text)), compact_span(doc.uid, doc.text, pos, pos + len(payload)),
    ), {"binding_verified": True, "document": canonical_title(e.titles[0]), "article": m["art"], "all_assertions_covered": True})


def _numeric_scope_complete(e: Extraction, a: Atom) -> bool:
    """No broad scope/numeric-bag inference: accept only a restricted sentence."""
    text = compact(e.text)
    if QUOTE_RISK.search(text):
        return False
    if a.predicate in {"WORK_DAILY_HOURS", "WORK_WEEKLY_HOURS"}:
        return not re.search(r"特殊|不能实行|其他|不受|一律|无论|所有|任何|例外", text)
    if a.predicate == "DISABILITY_MONTHS":
        return len(e.version_years) == 1
    # A weaker upper bound is not a logical contradiction merely because its
    # numeral differs. These grammars remain observable, not refutation-ready.
    # Condition/exception inference and unsupported range paraphrases abstain.
    return False


def fact_proofs(e: Extraction, docs: list[Evidence], temporal: bool, authority: bool) -> tuple[list[Proof], list[str]]:
    proofs: list[Proof] = []
    gaps: list[str] = []
    related = [d for d in docs if _law_binding(e, d)]
    if not related:
        return [], ["DOCUMENT_BINDING_OR_TOP5_GAP"]
    if e.version_years and not temporal:
        gaps.append("VERSION_BINDING_GAP")
    if e.slots["source_role"]["status"] == "OBSERVED" and not authority:
        gaps.append("CLAIMED_AUTHORITY_ROLE_GAP")
    for d in related:
        if not _compatible_version(e, d, temporal):
            continue
        p = _full_literal_support(e, d)
        if p and not gaps:
            proofs.append(p)
    for a in e.atoms:
        if a.unit == "organ":
            if not authority:
                continue
        elif not _numeric_scope_complete(e, a):
            continue
        bound: list[tuple[Atom, Evidence]] = []
        for d in related:
            # Promulgation/adoption are dated identity events, not a statement
            # that an old substantive norm currently applies. Exact order or
            # meeting identity can bind without guessing currentness.
            if a.unit != "organ" and not _compatible_version(e, d, temporal):
                continue
            for b in extract(d.text, d.uid, d.title).atoms:
                if (a.predicate, a.scope, a.unit) == (b.predicate, b.scope, b.unit):
                    bound.append((b, d))
        values = {b.value for b, _ in bound}
        if len(values) > 1:
            gaps.append("UNRESOLVED_OFFICIAL_OR_VERSION_CONFLICT")
            continue
        if not bound:
            gaps.append("TYPED_FACT_OR_SCOPE_GAP")
            continue
        b, d = sorted(bound, key=lambda x: x[1].uid)[0]
        if a.value != b.value:
            proofs.append(Proof("P_ROLE_BOUND_ORDER" if a.unit == "organ" else "F_FUNCTIONAL_SAME_SCOPE_VALUE", "CONTRADICT", digest(e.text), (a.witness, b.witness), {
                "binding_verified": True, "predicate": a.predicate, "subject": a.subject,
                "scope": a.scope, "unit": a.unit, "candidate_value": a.value,
                "evidence_value": b.value, "version_binding": _document_version(d.title, d.text),
                "all_retrieved_same_scope_values": sorted(values),
            }))
    if not proofs:
        gaps.append("UNCOVERED_ASSERTIONS_OR_RELATION_GRAMMAR")
    return proofs, sorted(set(gaps))


def joint_proofs(e: Extraction, docs: list[Evidence]) -> tuple[list[Proof], list[str]]:
    """Explicit two-version grade/benefit comparison with both typed premises."""
    text = compact(e.text)
    years = re.findall(r"(\d{4})年?(?:修订|原版|修正|版)", text)
    grade = re.search(r"([一二三四五六七八九十]+级)伤残", text)
    direction = re.search(r"提高|增加|降低|减少", text)
    if len(years) != 2 or not grade or not direction or QUOTE_RISK.search(text) or "一次性伤残补助金" not in text:
        return [], ["JOINT_PREMISES_UNRESOLVED"]
    if int(years[0]) >= int(years[1]) or re.search(r"不(?:再)?(?:提高|增加|降低|减少)", text):
        return [], ["COMPARISON_DIRECTION_OR_VERSION_ORDER_UNRESOLVED"]
    endpoints: dict[str, list[Atom]] = {y: [] for y in years}
    for d in docs:
        if not _law_binding(e, d):
            continue
        v = _document_version(d.title, d.text)
        if v in endpoints:
            endpoints[v].extend(a for a in extract(d.text, d.uid, d.title).atoms if a.predicate == "DISABILITY_MONTHS" and a.scope == grade[1])
    if any(len({a.value for a in atoms}) != 1 for atoms in endpoints.values()):
        return [], ["SECOND_TYPED_PREMISE_MISSING_OR_CONFLICTING"]
    left, right = (sorted(endpoints[y], key=lambda a: a.witness.source_id)[0] for y in years)
    delta = number(right.value) - number(left.value)
    expected = 1 if direction[0] in {"提高", "增加"} else -1
    if delta == 0:
        return [], ["ZERO_COMPARISON_OR_UNSUPPORTED_DIRECTION"]
    verdict = "SUPPORT" if delta * expected > 0 else "CONTRADICT"
    # The comparison can refute its own direction, but partial parsing cannot
    # establish that every other assertion in the candidate is supported.
    if verdict == "SUPPORT":
        return [], ["JOINT_COMPARISON_SUPPORTED_OTHER_ASSERTIONS_UNRESOLVED"]
    return [Proof("J_TWO_VERSION_FUNCTIONAL_COMPARISON", verdict, digest(e.text), (
        span("candidate", e.text, 0, len(e.text)), left.witness, right.witness,
    ), {"binding_verified": True, "years": years, "grade": grade[1], "unit": left.unit, "values": [left.value, right.value], "all_assertions_covered": verdict == "SUPPORT"})], []


def _terminal(proofs: list[Proof], gaps: list[str]) -> tuple[str, list[Proof]]:
    if "UNRESOLVED_OFFICIAL_OR_VERSION_CONFLICT" in gaps:
        return "INSUFFICIENT", []
    bad = [p for p in proofs if p.conclusion == "CONTRADICT"]
    if bad and not any(g in gaps for g in ("VERSION_BINDING_GAP", "CLAIMED_AUTHORITY_ROLE_GAP")):
        return "CONTRADICT", bad
    good = [p for p in proofs if p.conclusion == "SUPPORT" and p.premises.get("all_assertions_covered")]
    if good and not any(g in gaps for g in ("VERSION_BINDING_GAP", "CLAIMED_AUTHORITY_ROLE_GAP")):
        return "SUPPORT", good
    return "INSUFFICIENT", []


def verify(candidate: dict[str, str], evidence: list[Evidence], adaptive: bool) -> dict[str, Any]:
    if set(candidate) != {"candidate_id", "candidate_text"}:
        raise ValueError("FORBIDDEN_RUNTIME_FIELDS")
    if len(evidence) > 5 or len({d.uid for d in evidence}) != len(evidence):
        raise ValueError("F5_BUDGET_OR_DUPLICATE_UID")
    text = candidate["candidate_text"]
    start = time.perf_counter()
    events: list[dict[str, Any]] = []

    def call(name: str, fn: Callable[[], Any], gap: str) -> Any:
        tick = time.perf_counter()
        value = fn()
        events.append({"module": name, "gap": gap, "elapsed_seconds": time.perf_counter() - tick})
        return value

    e = call("E0", lambda: extract(text), "CANDIDATE_EXTRACTION")
    cues = [{"rule_id": r.rule_id, "start": m.start(), "end": m.end()} for r in (*ORIGINAL, *GENERAL) for m in re.finditer(r.expression, text)]
    internal = call("I", lambda: internal_proof(e), "INTERNAL_PROOF_SEARCH_ALL_PARSED_RELATIONS")
    sources = {"candidate": text}
    if internal and not validate_proof(internal, text, sources):
        raise ValueError("INVALID_INTERNAL_CERTIFICATE")
    verdict, selected, gaps, consumed = "INSUFFICIENT", [], [], []
    if adaptive and internal:
        verdict, selected = "CONTRADICT", [internal]
    else:
        for d in evidence:
            d.validate()
        sources.update({d.uid: d.text for d in evidence})
        consumed = sorted(d.uid for d in evidence)
        proofs, gaps = call("F", lambda: fact_proofs(e, evidence, False, False), "INITIAL_SAME_SCOPE_BINDING")
        verdict, selected = _terminal(proofs, gaps)
        temporal, authority = False, False
        if not adaptive or (verdict == "INSUFFICIENT" and (e.version_years or e.slots["time_version"]["status"] == "OBSERVED")):
            temporal = True
            call("T", lambda: [_document_version(d.title, d.text) for d in evidence], "VERSION_BINDING_GAP" if adaptive else "STATIC_FULL_PIPELINE")
        if not adaptive or (verdict == "INSUFFICIENT" and e.slots["source_role"]["status"] == "OBSERVED"):
            authority = True
            call("P", lambda: [d.metadata.get("issuer") for d in evidence], "CLAIMED_AUTHORITY_ROLE_GAP" if adaptive else "STATIC_FULL_PIPELINE")
        if temporal or authority:
            proofs, gaps = call("F_REBIND", lambda: fact_proofs(e, evidence, temporal, authority), "RECHECK_BINDINGS")
            verdict, selected = _terminal(proofs, gaps)
        if not adaptive or (verdict == "INSUFFICIENT" and len(e.version_years) > 1):
            joint, jgaps = call("J", lambda: joint_proofs(e, evidence), "JOINT_PREMISE_GAP" if adaptive else "STATIC_FULL_PIPELINE")
            proofs.extend(joint)
            gaps.extend(jgaps if not joint else [])
            verdict, selected = _terminal(proofs, gaps)
        # Same logical aggregation: a sound internal certificate remains valid
        # in the static condition after its nonadaptive work has completed.
        if internal:
            verdict, selected, gaps = "CONTRADICT", [internal], []
    for p in selected:
        if not validate_proof(p, text, sources):
            raise ValueError("INVALID_TERMINAL_CERTIFICATE")
    events.append({"module": "Q", "gap": "TERMINAL_PROOF_OR_BUDGET_STOP", "elapsed_seconds": 0.0})
    return {
        "candidate_id": candidate["candidate_id"], "candidate_sha256": digest(text),
        "condition": "V03-F5" if adaptive else "V02-NA-F5", "parser_version": VERSION,
        "slots": e.slots, "atoms": [asdict(a) for a in e.atoms], "a0_cues_only": cues,
        "verdict": verdict, "proofs": [asdict(p) for p in selected],
        "unresolved_gaps": sorted(set(gaps or (["CLOSED_GRAMMAR_INSUFFICIENT"] if verdict == "INSUFFICIENT" else []))),
        "review_required": verdict == "INSUFFICIENT", "route_trace": events,
        "internal_certificate_present": internal is not None,
        "internal_early_exit": adaptive and internal is not None,
        "evidence_consumed_uids": consumed,
        "evidence_consumed_chars": sum(len(d.text) for d in evidence if d.uid in consumed),
        "retrieved_evidence_uids": [d.uid for d in evidence],
        "verifier_elapsed_seconds": time.perf_counter() - start,
        "llm_calls": 0, "risk_score": None, "risk_score_status": "NO_CONTINUOUS_SCORE",
    }
