"""
epistemic_uncertainty_radar.py - Autonomous Cognitive Spatial Epistemic Uncertainty Radar & Assumption Stress-Tester

Part of the DxSkills cognitive scaffolding suite (Phase 106, Cycle 102).
Grounded in Toulmin (1958) argumentation structure, Kahneman & Tversky (1982) epistemic calibration,
and Taleb (2007) structural antifragility stress-testing.

Strict constraint: Strictly zero em dashes (Unicode U+2014) anywhere.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class EpistemicClaim:
    """Individual structural claim, premise, or assumption evaluated for empirical grounding."""
    claim_id: str
    statement: str
    category: str  # ARCHITECTURE, PERFORMANCE, ERGONOMICS, SECURITY
    grounding_tier: str  # EMPIRICAL, THEORETICAL, HEURISTIC, SPECULATIVE
    confidence_score: float  # 0.0 (unverified hunch) to 1.0 (empirically proven benchmark)
    fragility_index: float  # 0.0 (robust/antifragile) to 1.0 (brittle/catastrophic failure point)
    failure_severity: str  # LOW, MODERATE, SEVERE, CRITICAL
    mitigation_strategy: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class FragilityStressVector:
    """Simulated adversarial stress test probing structural dependency resilience."""
    vector_id: str
    name: str
    stress_multiplier: float  # e.g., 2.5x load spike, 5x memory latency
    targeted_claim_ids: List[str]
    cascade_failure_probability_pct: float
    resilience_verdict: str  # ANTIFRAGILE, RESILIENT, VULNERABLE, COLLAPSED

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EpistemicTelemetry:
    """Cognitive telemetry measuring epistemic calibration, fragility bounds, and audit clarity."""
    total_claims_analyzed: int
    mean_confidence_score: float
    mean_fragility_index: float
    high_fragility_count: int
    antifragility_rating: float  # 0 to 100 overall resilience score
    epistemic_drift_risk: str  # NOMINAL, MODERATE, ELEVATED, CRITICAL
    cowan_bounded: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EpistemicRadarResult:
    """Master result bundle containing evaluated claims, stress scenarios, and radar diagram."""
    claims: List[EpistemicClaim]
    stress_vectors: List[FragilityStressVector]
    telemetry: EpistemicTelemetry
    svg_radar: str
    mitigation_table_md: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "telemetry": self.telemetry.to_dict(),
            "claims": [c.to_dict() for c in self.claims],
            "stress_vectors": [v.to_dict() for v in self.stress_vectors],
            "svg_radar": self.svg_radar,
            "mitigation_table_md": self.mitigation_table_md,
        }


class EpistemicUncertaintyRadar:
    """
    Autonomous Cognitive Spatial Epistemic Uncertainty Radar & Assumption Stress-Tester.

    Evaluates empirical grounding and confidence calibration across spatial architectural models,
    and stress-tests brittle assumptions under simulated adversarial load conditions.
    """

    GROUNDING_KEYWORDS = {
        "EMPIRICAL": ["benchmark", "measured", "telemetry", "proven", "observed", "tested", "data"],
        "THEORETICAL": ["model", "theorem", "literature", "published", "cited", "formal", "equation"],
        "HEURISTIC": ["rule of thumb", "experience", "typical", "standard", "expected", "heuristic"],
        "SPECULATIVE": ["assume", "probably", "should be", "untested", "guess", "unverified", "hope"],
    }

    def __init__(self, fragility_threshold: float = 0.60) -> None:
        self.fragility_threshold = fragility_threshold

    def evaluate_claims(
        self,
        raw_claims: List[Dict[str, Any]],
        stress_scenarios: Optional[List[Dict[str, Any]]] = None,
    ) -> EpistemicRadarResult:
        """
        Task 106.1 & 106.2: Calibrates epistemic uncertainty across architectural claims
        and stress-tests assumptions against simulated failure vectors.
        """
        if not raw_claims:
            empty_telemetry = EpistemicTelemetry(
                total_claims_analyzed=0,
                mean_confidence_score=0.0,
                mean_fragility_index=0.0,
                high_fragility_count=0,
                antifragility_rating=100.0,
                epistemic_drift_risk="NOMINAL",
                cowan_bounded=True,
            )
            return EpistemicRadarResult(
                claims=[],
                stress_vectors=[],
                telemetry=empty_telemetry,
                svg_radar="",
                mitigation_table_md="",
            )

        evaluated_claims: List[EpistemicClaim] = []
        total_conf = 0.0
        total_frag = 0.0

        for idx, item in enumerate(raw_claims):
            cid = str(item.get("id") or f"clm_{idx+1}")
            stmt = str(item.get("statement") or item.get("claim") or item.get("text") or f"Claim {idx+1}")
            cat = str(item.get("category") or "ARCHITECTURE").upper()

            # Detect grounding tier if not explicitly specified
            explicit_tier = item.get("grounding_tier") or item.get("tier")
            if explicit_tier and str(explicit_tier).upper() in self.GROUNDING_KEYWORDS:
                tier = str(explicit_tier).upper()
            else:
                stmt_lower = stmt.lower()
                tier = "HEURISTIC"  # default
                for t_name, kws in self.GROUNDING_KEYWORDS.items():
                    if any(kw in stmt_lower for kw in kws):
                        tier = t_name
                        break

            # Calibrate confidence score
            if tier == "EMPIRICAL":
                conf = float(item.get("confidence_score") or 0.95)
                frag = float(item.get("fragility_index") or 0.15)
                sev = "LOW"
                strat = "Maintain continuous automated telemetry assertions."
            elif tier == "THEORETICAL":
                conf = float(item.get("confidence_score") or 0.80)
                frag = float(item.get("fragility_index") or 0.35)
                sev = "MODERATE"
                strat = "Validate theoretical bounds under edge case distributions."
            elif tier == "HEURISTIC":
                conf = float(item.get("confidence_score") or 0.60)
                frag = float(item.get("fragility_index") or 0.65)
                sev = "SEVERE"
                strat = "Instrument profiling hooks to replace heuristic with measured metrics."
            else:  # SPECULATIVE
                conf = float(item.get("confidence_score") or 0.30)
                frag = float(item.get("fragility_index") or 0.88)
                sev = "CRITICAL"
                strat = "Isolate behind failure boundary and construct fallback redundancy."

            conf = round(max(0.05, min(1.0, conf)), 2)
            frag = round(max(0.05, min(1.0, frag)), 2)
            total_conf += conf
            total_frag += frag

            evaluated_claims.append(EpistemicClaim(
                claim_id=cid,
                statement=stmt,
                category=cat,
                grounding_tier=tier,
                confidence_score=conf,
                fragility_index=frag,
                failure_severity=sev,
                mitigation_strategy=strat,
            ))

        mean_conf = round(total_conf / max(1, len(evaluated_claims)), 2)
        mean_frag = round(total_frag / max(1, len(evaluated_claims)), 2)
        high_frag_count = sum(1 for c in evaluated_claims if c.fragility_index >= self.fragility_threshold)

        # Antifragility rating (100 = completely robust, 0 = brittle house of cards)
        antifragility = round(max(10.0, min(100.0, 100.0 - (mean_frag * 65.0) + (mean_conf * 25.0))), 1)

        if mean_frag < 0.30:
            drift_risk = "NOMINAL"
        elif mean_frag < 0.55:
            drift_risk = "MODERATE"
        elif mean_frag < 0.75:
            drift_risk = "ELEVATED"
        else:
            drift_risk = "CRITICAL"

        cowan_bounded = high_frag_count <= 4

        telemetry = EpistemicTelemetry(
            total_claims_analyzed=len(evaluated_claims),
            mean_confidence_score=mean_conf,
            mean_fragility_index=mean_frag,
            high_fragility_count=high_frag_count,
            antifragility_rating=antifragility,
            epistemic_drift_risk=drift_risk,
            cowan_bounded=cowan_bounded,
        )

        # Adversarial stress vectors (Task 106.2)
        stress_vectors: List[FragilityStressVector] = []
        scenarios = stress_scenarios or [
            {"id": "vec_1", "name": "5x Canvas Object Density Spike", "multiplier": 5.0},
            {"id": "vec_2", "name": "Adversarial Saccade Rapid Panning Jitter", "multiplier": 3.2},
            {"id": "vec_3", "name": "Phonological Memory Exhaustion Boundary", "multiplier": 4.0},
        ]

        for s in scenarios:
            vid = str(s.get("id") or f"vec_{len(stress_vectors)+1}")
            vname = str(s.get("name") or f"Stress Scenario {len(stress_vectors)+1}")
            vmult = float(s.get("multiplier", 2.0))

            # Probability of cascade failure based on mean fragility and multiplier
            fail_pct = round(min(95.0, max(5.0, mean_frag * vmult * 30.0)), 1)
            if fail_pct < 25.0:
                verdict = "ANTIFRAGILE"
            elif fail_pct < 55.0:
                verdict = "RESILIENT"
            elif fail_pct < 80.0:
                verdict = "VULNERABLE"
            else:
                verdict = "COLLAPSED"

            targeted = [c.claim_id for c in evaluated_claims if c.fragility_index >= 0.50]

            stress_vectors.append(FragilityStressVector(
                vector_id=vid,
                name=vname,
                stress_multiplier=vmult,
                targeted_claim_ids=targeted,
                cascade_failure_probability_pct=fail_pct,
                resilience_verdict=verdict,
            ))

        # Build Markdown Mitigation Table
        table_lines = [
            "| Claim ID | Category | Grounding | Confidence | Fragility | Severity | Mitigation Action |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]
        for c in evaluated_claims:
            table_lines.append(
                f"| `{c.claim_id}` | {c.category} | {c.grounding_tier} | {c.confidence_score:.2f} | "
                f"{c.fragility_index:.2f} | [{c.failure_severity}] | {c.mitigation_strategy} |"
            )
        mitigation_md = "\n".join(table_lines)

        svg_radar = self._render_radar_svg(
            claims=evaluated_claims,
            stress_vectors=stress_vectors,
            telemetry=telemetry,
        )

        return EpistemicRadarResult(
            claims=evaluated_claims,
            stress_vectors=stress_vectors,
            telemetry=telemetry,
            svg_radar=svg_radar,
            mitigation_table_md=mitigation_md,
        )

    def _render_radar_svg(
        self,
        claims: List[EpistemicClaim],
        stress_vectors: List[FragilityStressVector],
        telemetry: EpistemicTelemetry,
    ) -> str:
        """Renders dark titanium polar radar chart showing confidence vs fragility."""
        w, h = 920, 520
        t = telemetry

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">',
            '  <defs>',
            '    <linearGradient id="eurBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#090d16"/>',
            '      <stop offset="100%" stop-color="#0f172a"/>',
            '    </linearGradient>',
            '    <radialGradient id="radarRings" cx="50%" cy="50%" r="50%">',
            '      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.15"/>',
            '      <stop offset="100%" stop-color="#0284c7" stop-opacity="0.02"/>',
            '    </radialGradient>',
            '  </defs>',
            '  <rect width="100%" height="100%" fill="url(#eurBg)"/>',
            '  <!-- Header -->',
            '  <text x="40" y="44" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#f8fafc">Epistemic Uncertainty Radar &amp; Stress-Tester</text>',
            f'  <text x="40" y="68" font-family="system-ui, -apple-system, sans-serif" font-size="12" fill="#94a3b8">Toulmin &bull; Antifragility: {t.antifragility_rating}/100 &bull; Mean Conf: {t.mean_confidence_score} &bull; Fragility: {t.mean_fragility_index} &bull; Risk: [{t.epistemic_drift_risk}]</text>',
            '  <!-- Polar Radar Frame (Center: x=460, y=225) -->',
            '  <g transform="translate(460, 225)">',
            '    <!-- Concentric Web Rings -->',
            '    <circle cx="0" cy="0" r="110" fill="url(#radarRings)" stroke="#1e293b" stroke-width="1.5"/>',
            '    <circle cx="0" cy="0" r="80" fill="none" stroke="#1e293b" stroke-width="1" stroke-dasharray="3,3"/>',
            '    <circle cx="0" cy="0" r="50" fill="none" stroke="#1e293b" stroke-width="1" stroke-dasharray="3,3"/>',
            '    <circle cx="0" cy="0" r="20" fill="none" stroke="#0284c7" stroke-width="1.5"/>',
            '    <!-- Cross Axes -->',
            '    <line x1="-130" y1="0" x2="130" y2="0" stroke="#334155" stroke-width="1.5"/>',
            '    <line x1="0" y1="-130" x2="0" y2="130" stroke="#334155" stroke-width="1.5"/>',
            '    <!-- Quadrant Labels -->',
            '    <text x="0" y="-120" font-family="monospace" font-size="9" fill="#38bdf8" text-anchor="middle">HIGH CONFIDENCE (1.0)</text>',
            '    <text x="0" y="128" font-family="monospace" font-size="9" fill="#f43f5e" text-anchor="middle">SPECULATIVE (0.0)</text>',
            '    <text x="-125" y="4" font-family="monospace" font-size="9" fill="#10b981" text-anchor="end">ANTIFRAGILE</text>',
            '    <text x="125" y="4" font-family="monospace" font-size="9" fill="#f59e0b">BRITTLE</text>',
        ]

        # Plot claims as colored nodes on polar grid
        for i, c in enumerate(claims[:8]):
            # Map confidence to Y (inverted: high conf is negative Y)
            # Map fragility to X (high frag is positive X)
            node_x = round((c.fragility_index - 0.5) * 200.0, 1)
            node_y = round((0.5 - c.confidence_score) * 200.0, 1)

            color = "#10b981" if c.grounding_tier == "EMPIRICAL" else ("#38bdf8" if c.grounding_tier == "THEORETICAL" else ("#f59e0b" if c.grounding_tier == "HEURISTIC" else "#f43f5e"))
            svg_parts.extend([
                f'    <!-- Claim {c.claim_id} -->',
                f'    <circle cx="{node_x}" cy="{node_y}" r="6" fill="{color}" stroke="#f8fafc" stroke-width="1.5"/>',
                f'    <text x="{node_x + 8}" y="{node_y + 3}" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="700" fill="#f8fafc">{c.claim_id}</text>',
            ])

        svg_parts.append('  </g>')

        # Bottom Cards
        svg_parts.extend([
            '  <!-- Bottom Cards: Telemetry Badges -->',
            '  <g transform="translate(60, 385)">',
            '    <rect x="0" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="20" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Structural Antifragility</text>',
            f'    <text x="20" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#38bdf8">{t.antifragility_rating}/100</text>',
            f'    <text x="20" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Mean confidence: {t.mean_confidence_score:.2f}</text>',
            '    <rect x="270" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="290" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Brittle Failure Points</text>',
            f'    <text x="290" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#f59e0b">{t.high_fragility_count}</text>',
            f'    <text x="290" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">Cowan bounded: {t.cowan_bounded} (Limit: &lt;= 4)</text>',
            '    <rect x="540" y="0" width="240" height="90" rx="10" fill="#0b1120" stroke="#1e293b" stroke-width="1.5"/>',
            '    <text x="560" y="28" font-family="system-ui, -apple-system, sans-serif" font-size="11" fill="#94a3b8">Epistemic Drift Risk</text>',
            f'    <text x="560" y="60" font-family="system-ui, -apple-system, sans-serif" font-size="26" font-weight="800" fill="#10b981">[{t.epistemic_drift_risk}]</text>',
            f'    <text x="560" y="80" font-family="system-ui, -apple-system, sans-serif" font-size="10" fill="#64748b">{len(stress_vectors)} stress scenarios probed</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg_parts)

    def export_svg(self, result: EpistemicRadarResult, output_path: Optional[str] = None) -> str:
        """Exports SVG diagram to file or returns XML string."""
        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(result.svg_radar)
        return result.svg_radar

    def generate_ascii_report(self, result: EpistemicRadarResult) -> str:
        """Generates clean terminal ASCII table summarizing epistemic radar metrics."""
        t = result.telemetry
        lines = [
            "================================================================================",
            "   EPISTEMIC UNCERTAINTY RADAR & STRESS-TESTER (PHASE 106 / CYCLE 102)",
            "================================================================================",
            f" Claims Evaluated      : {t.total_claims_analyzed} architectural assertions",
            f" Mean Confidence Score : {t.mean_confidence_score:.2f} (0.0=Hunch, 1.0=Empirical Fact)",
            f" Mean Fragility Index  : {t.mean_fragility_index:.2f} (0.0=Antifragile, 1.0=Brittle)",
            f" High Fragility Points : {t.high_fragility_count} single points of potential failure",
            f" Antifragility Rating  : {t.antifragility_rating:.1f}/100 structural resilience",
            f" Epistemic Drift Risk  : [{t.epistemic_drift_risk}]",
            f" Cowan Bounded (N<=4)  : {'Yes [OPTIMAL]' if t.cowan_bounded else 'No [TOO MANY VULNERABILITIES]'}",
            "--------------------------------------------------------------------------------",
            " EVALUATED CLAIMS & RESILIENCE CALIBRATION",
            "--------------------------------------------------------------------------------",
        ]

        if not result.claims:
            lines.append(" (No claims evaluated; empty input)")
        else:
            for c in result.claims:
                lines.append(f" [{c.claim_id}] ({c.grounding_tier} | Conf: {c.confidence_score:.2f} | Frag: {c.fragility_index:.2f})")
                lines.append(f"       Statement : {c.statement}")
                lines.append(f"       Mitigation: {c.mitigation_strategy}")

        lines.append("--------------------------------------------------------------------------------")
        lines.append(" ADVERSARIAL STRESS SCENARIOS")
        lines.append("--------------------------------------------------------------------------------")
        for sv in result.stress_vectors:
            lines.append(f" [STRESS] '{sv.name}' (Load: {sv.stress_multiplier}x | Failure: {sv.cascade_failure_probability_pct}%)")
            lines.append(f"          Verdict: [{sv.resilience_verdict}]")

        lines.append("================================================================================")
        return "\n".join(lines)
