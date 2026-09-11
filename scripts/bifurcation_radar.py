"""
Bifurcation Radar & Path-Dependency Loom
Grounding: W. Brian Arthur increasing returns and path-dependency dynamics,
David lock-in thresholds, non-linear bifurcation trees, and counterfactual analysis.
Strict rule: Zero em dashes across all code, comments, docstrings, and outputs.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
import math
import json


@dataclass
class BifurcationDecision:
    """Represents a specific architectural decision taken along a timeline branch."""
    decision_id: str
    title: str
    branch_id: str  # "primary" or counterfactual branch name
    depth: int
    complexity: float = 5.0
    downstream_deps: int = 1
    reversible: bool = True

    @property
    def commitment_weight(self) -> float:
        """Calculates switching inertia based on complexity, dependencies, and irreversibility."""
        irr_mult = 2.0 if not self.reversible else 1.0
        return max(1.0, float(self.complexity) * (1.0 + 0.3 * float(self.downstream_deps)) * irr_mult)


@dataclass
class BifurcationFork:
    """Represents a non-linear choice point with primary and counterfactual paths."""
    fork_id: str
    title: str
    root_concept: str
    primary_branch: str
    counterfactual_branches: List[str] = field(default_factory=list)
    decisions: List[BifurcationDecision] = field(default_factory=list)
    lock_in_score: float = 0.0
    status: str = "fluid"  # "fluid", "soft_lock", "hard_lock"
    switching_cost: float = 0.0


@dataclass
class MultiverseTelemetry:
    """Aggregated metrics across multi-timeline bifurcation architectures."""
    total_forks: int
    total_decisions: int
    mean_lock_in_score: float
    max_lock_in_score: float
    primary_status: str
    total_switching_cost: float
    counterfactual_entropy: float
    forks: List[BifurcationFork] = field(default_factory=list)


class BifurcationRadarLoom:
    """
    Evaluates path-dependency lock-in dynamics and renders multiverse
    branch alternatives across non-linear spatial reasoning trajectories.
    """

    def __init__(self, s_threshold: float = 120.0, coupling_lambda: float = 0.25):
        self.s_threshold = max(10.0, float(s_threshold))
        self.coupling_lambda = max(0.01, float(coupling_lambda))

    def evaluate_fork(self, fork: BifurcationFork) -> BifurcationFork:
        """
        Computes the Arthur lock-in index and switching friction for a single fork.
        """
        primary_decisions = [d for d in fork.decisions if d.branch_id == fork.primary_branch or d.branch_id == "primary"]
        if not primary_decisions:
            fork.lock_in_score = 0.0
            fork.switching_cost = 0.0
            fork.status = "fluid"
            return fork

        # Cumulative switching cost S(m) = sum(w_j * (1 + lambda * deps_j))
        total_s = 0.0
        for d in primary_decisions:
            total_s += d.commitment_weight * (1.0 + self.coupling_lambda * float(d.downstream_deps))

        fork.switching_cost = round(total_s, 2)

        # Arthur Lock-in index: Lambda = 1 - exp(-total_s / S_threshold)
        lock_in = 1.0 - math.exp(-total_s / self.s_threshold)
        fork.lock_in_score = round(min(1.0, max(0.0, lock_in)), 3)

        if fork.lock_in_score >= 0.75:
            fork.status = "hard_lock"
        elif fork.lock_in_score >= 0.40:
            fork.status = "soft_lock"
        else:
            fork.status = "fluid"

        return fork

    def evaluate_multiverse(self, forks: List[BifurcationFork]) -> MultiverseTelemetry:
        """
        Evaluates a complete multiverse decision network across multiple forks.
        """
        if not forks:
            return MultiverseTelemetry(
                total_forks=0,
                total_decisions=0,
                mean_lock_in_score=0.0,
                max_lock_in_score=0.0,
                primary_status="fluid",
                total_switching_cost=0.0,
                counterfactual_entropy=0.0,
                forks=[]
            )

        evaluated_forks: List[BifurcationFork] = []
        total_decisions = 0
        all_lock_in: List[float] = []
        total_switching = 0.0

        for f in forks:
            ef = self.evaluate_fork(f)
            evaluated_forks.append(ef)
            total_decisions += len(ef.decisions)
            all_lock_in.append(ef.lock_in_score)
            total_switching += ef.switching_cost

        mean_lock = sum(all_lock_in) / len(all_lock_in) if all_lock_in else 0.0
        max_lock = max(all_lock_in) if all_lock_in else 0.0

        if max_lock >= 0.75:
            prim_status = "hard_lock"
        elif max_lock >= 0.40:
            prim_status = "soft_lock"
        else:
            prim_status = "fluid"

        # Counterfactual entropy calculation across alternative options
        branch_counts: List[int] = [1 + len(f.counterfactual_branches) for f in evaluated_forks]
        total_branches = sum(branch_counts)
        h_cf = 0.0
        if total_branches > 0 and len(branch_counts) > 1:
            for c in branch_counts:
                p = c / float(total_branches)
                if p > 0.0:
                    h_cf -= p * math.log2(p)

        return MultiverseTelemetry(
            total_forks=len(forks),
            total_decisions=total_decisions,
            mean_lock_in_score=round(mean_lock, 3),
            max_lock_in_score=round(max_lock, 3),
            primary_status=prim_status,
            total_switching_cost=round(total_switching, 2),
            counterfactual_entropy=round(h_cf, 3),
            forks=evaluated_forks
        )

    def generate_svg(self, telemetry: MultiverseTelemetry, width: int = 920, height: int = 560) -> str:
        """
        Renders a dark titanium SVG diagram visualizing the multiverse bifurcation manifold,
        active path vectors, counterfactual ghost branches, and Arthur lock-in indicators.
        """
        forks = telemetry.forks
        if not forks:
            return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <rect width="100%" height="100%" fill="#09090b"/>
  <text x="50%" y="50%" fill="#71717a" font-family="system-ui, sans-serif" font-size="14" text-anchor="middle">No bifurcation data available</text>
</svg>'''

        svg_parts: List[str] = [
            f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="activeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#10b981"/>
    </linearGradient>
    <linearGradient id="ghostGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#71717a" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.6"/>
    </linearGradient>
    <radialGradient id="nodeGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#10b981" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="#10b981" stop-opacity="0.0"/>
    </radialGradient>
    <radialGradient id="lockGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ef4444" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#ef4444" stop-opacity="0.0"/>
    </radialGradient>
  </defs>

  <!-- Background Base Canvas -->
  <rect width="100%" height="100%" fill="#09090b" rx="14"/>
  <rect x="1" y="1" width="{width - 2}" height="{height - 2}" fill="none" stroke="#27272a" stroke-width="1.5" rx="13"/>

  <!-- Header Block -->
  <text x="32" y="38" fill="#fafafa" font-family="system-ui, sans-serif" font-size="16" font-weight="700">Multiverse Bifurcation Radar and Path-Dependency Loom</text>
  <text x="32" y="58" fill="#71717a" font-family="system-ui, sans-serif" font-size="12">Arthur Lock-in: {telemetry.max_lock_in_score} ({telemetry.primary_status.upper()}) | Switching Friction: {telemetry.total_switching_cost} | Counterfactual Entropy: {telemetry.counterfactual_entropy} bits</text>

  <!-- Legend Badges -->
  <g transform="translate({width - 320}, 22)">
    <rect width="140" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="14" cy="12" r="4" fill="#10b981"/>
    <text x="26" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Active Timeline</text>

    <rect x="150" width="150" height="24" rx="6" fill="#18181b" stroke="#27272a"/>
    <circle cx="164" cy="12" r="4" fill="#f59e0b"/>
    <text x="176" y="16" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Counterfactual Ghost</text>
  </g>
'''
        ]

        # Draw timeline tracks per fork
        track_y_start = 110.0
        track_height = (float(height) - 140.0) / max(1.0, float(len(forks)))

        for idx, f in enumerate(forks):
            y_base = track_y_start + idx * track_height + track_height * 0.45
            x_root = 80.0
            x_fork = 260.0
            x_active = 620.0
            x_end = float(width) - 60.0

            # Lock-in status color
            if f.status == "hard_lock":
                lock_color = "#ef4444"
            elif f.status == "soft_lock":
                lock_color = "#f59e0b"
            else:
                lock_color = "#10b981"

            svg_parts.append(f'''  <!-- Fork Track {idx + 1}: {f.title} -->
  <g id="track-{f.fork_id}">
    <!-- Background track guide -->
    <line x1="{x_root}" y1="{y_base:.1f}" x2="{x_fork}" y2="{y_base:.1f}" stroke="#27272a" stroke-width="2"/>

    <!-- Active Timeline Spline (Bezier curve) -->
    <path d="M {x_fork:.1f} {y_base:.1f} C {x_fork + 100:.1f} {y_base - 35:.1f}, {x_active - 100:.1f} {y_base - 35:.1f}, {x_active:.1f} {y_base - 35:.1f} L {x_end:.1f} {y_base - 35:.1f}"
          fill="none" stroke="url(#activeGrad)" stroke-width="2.5"/>

    <!-- Counterfactual Ghost Spline -->
    <path d="M {x_fork:.1f} {y_base:.1f} C {x_fork + 100:.1f} {y_base + 45:.1f}, {x_active - 100:.1f} {y_base + 45:.1f}, {x_active:.1f} {y_base + 45:.1f} L {x_end:.1f} {y_base + 45:.1f}"
          fill="none" stroke="url(#ghostGrad)" stroke-width="1.8" stroke-dasharray="4,4"/>

    <!-- Root Node -->
    <circle cx="{x_root:.1f}" cy="{y_base:.1f}" r="6" fill="#18181b" stroke="#38bdf8" stroke-width="2"/>
    <text x="{x_root:.1f}" y="{y_base - 14:.1f}" fill="#fafafa" font-family="system-ui, sans-serif" font-size="11" font-weight="600">{f.root_concept}</text>

    <!-- Fork Node -->
    <circle cx="{x_fork:.1f}" cy="{y_base:.1f}" r="7" fill="#18181b" stroke="{lock_color}" stroke-width="2.5"/>
    <text x="{x_fork:.1f}" y="{y_base + 22:.1f}" fill="#a1a1aa" font-family="system-ui, sans-serif" font-size="10">Fork: {f.title}</text>

    <!-- Active Path Label and Decisions -->
    <circle cx="{x_active:.1f}" cy="{y_base - 35:.1f}" r="5" fill="#10b981"/>
    <text x="{x_active + 12:.1f}" y="{y_base - 32:.1f}" fill="#10b981" font-family="system-ui, sans-serif" font-size="11" font-weight="600">Active: {f.primary_branch}</text>
    <text x="{x_active + 12:.1f}" y="{y_base - 18:.1f}" fill="#71717a" font-family="system-ui, sans-serif" font-size="9">Lock-in: {f.lock_in_score} | Cost: {f.switching_cost}</text>

    <!-- Counterfactual Path Label -->
    <circle cx="{x_active:.1f}" cy="{y_base + 45:.1f}" r="4" fill="#f59e0b"/>
    <text x="{x_active + 12:.1f}" y="{y_base + 48:.1f}" fill="#f59e0b" font-family="system-ui, sans-serif" font-size="10">Ghost: {", ".join(f.counterfactual_branches[:2]) if f.counterfactual_branches else "Alternative"}</text>
  </g>''')

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    def generate_markdown_report(self, telemetry: MultiverseTelemetry) -> str:
        """
        Synthesizes a publication-ready markdown compliance audit report.
        """
        lines: List[str] = [
            "# Multiverse Bifurcation Radar and Path-Dependency Audit",
            "",
            "## 1. Executive Telemetry Overview",
            f"- **Total Monitored Bifurcation Points:** {telemetry.total_forks}",
            f"- **Cumulative Architectural Decisions:** {telemetry.total_decisions}",
            f"- **Mean Arthur Lock-in Index:** {telemetry.mean_lock_in_score}",
            f"- **Maximum Lock-in Index:** {telemetry.max_lock_in_score}",
            f"- **Primary Architectural Status:** {telemetry.primary_status.upper()}",
            f"- **Total Switching Friction:** {telemetry.total_switching_cost}",
            f"- **Counterfactual Path Entropy:** {telemetry.counterfactual_entropy} bits",
            "",
            "## 2. Theoretical Grounding",
            "- **Arthur Increasing Returns & Path Dependency:** Early stochastic choices accumulate downstream commitments, rapidly elevating switching costs.",
            "- **Lock-in Index Thresholds:** Scores >= 0.75 represent structural lock-in requiring substantial rework, while scores < 0.40 denote fluid agility.",
            "- **Counterfactual Timeline Preservation:** Retaining shadow branches safeguards optionality and prevents cognitive tunnel vision.",
            "",
            "## 3. Bifurcation Fork Breakdown",
            "| Fork ID | Title | Root Concept | Primary Path | Lock-in | Status | Switching Cost | Counterfactuals |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
        ]

        for f in telemetry.forks:
            cf_str = ", ".join(f.counterfactual_branches) if f.counterfactual_branches else "none"
            lines.append(
                f"| `{f.fork_id}` | {f.title} | {f.root_concept} | **{f.primary_branch}** | {f.lock_in_score} | `{f.status}` | {f.switching_cost} | {cf_str} |"
            )

        lines.extend([
            "",
            "## 4. Strategic Recommendations",
            "- For forks with Lock-in >= 0.75, avoid introducing additional tightly coupled downstream abstractions.",
            "- Conduct periodic counterfactual retrospectives to verify that abandoned options do not become critical liabilities.",
            "- Preserve interface contracts that decouple implementation branches from core conceptual models."
        ])

        return "\n".join(lines)


def sample_bifurcation_forks() -> List[BifurcationFork]:
    """Generates an illustrative sample of architectural bifurcation forks."""
    return [
        BifurcationFork(
            fork_id="fork-backend",
            title="State Storage Paradigm",
            root_concept="Storage Layer",
            primary_branch="event_sourcing",
            counterfactual_branches=["relational_crud", "document_graph"],
            decisions=[
                BifurcationDecision("d1", "Adopt Kafka Event Log", "event_sourcing", 1, complexity=7.0, downstream_deps=3, reversible=False),
                BifurcationDecision("d2", "Implement CQRS Read Projections", "event_sourcing", 2, complexity=8.0, downstream_deps=4, reversible=False),
                BifurcationDecision("d3", "Snapshot Storage in S3", "event_sourcing", 3, complexity=5.0, downstream_deps=2, reversible=True),
            ]
        ),
        BifurcationFork(
            fork_id="fork-ui",
            title="Rendering Architecture",
            root_concept="Visual Client",
            primary_branch="vector_canvas",
            counterfactual_branches=["html_dom_grid", "webgl_threejs"],
            decisions=[
                BifurcationDecision("d4", "Custom SVG Interactive Pan/Zoom", "vector_canvas", 1, complexity=4.0, downstream_deps=2, reversible=True),
                BifurcationDecision("d5", "Bionic Focus Fixation Anchors", "vector_canvas", 2, complexity=3.5, downstream_deps=1, reversible=True),
            ]
        ),
        BifurcationFork(
            fork_id="fork-auth",
            title="Identity Federation",
            root_concept="Security Perimeter",
            primary_branch="decentralized_pki",
            counterfactual_branches=["central_oauth", "session_cookie"],
            decisions=[
                BifurcationDecision("d6", "Local Ed25519 Keypair Generation", "decentralized_pki", 1, complexity=6.0, downstream_deps=2, reversible=False),
                BifurcationDecision("d7", "WebCrypto Sub-Canvas Signing", "decentralized_pki", 2, complexity=5.5, downstream_deps=3, reversible=False),
            ]
        ),
    ]
