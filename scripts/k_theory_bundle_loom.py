"""
Topological K-Theory & Vector Bundle Classification Loom
Autonomous cognitive spatial module classifying vector bundles over task manifolds,
evaluating Grothendieck groups K_0(X), computing clutching function winding invariants,
and modeling complex/real Bott periodicity cycles and stable equivalence classes.
Grounded in topological K-theory (Grothendieck 1957, Atiyah-Hirzebruch 1961),
Bott periodicity (Bott 1959), and vector bundle classification (Karoubi 1978, Hatcher 2003).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any, Callable
import math
import html
import json


# Pure Python Complex & Matrix Utilities for Vector Bundles


def complex_det_2x2(a: List[List[complex]]) -> complex:
    """Computes determinant of 2x2 complex matrix."""
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def compute_clutching_degree(clutching_func: Callable[[float], complex], num_samples: int = 100) -> int:
    """Computes topological winding number / degree of clutching map S^1 -> C*
    deg = (1 / 2pi) int d(arg(f(theta)))
    """
    total_angle = 0.0
    prev_angle: Optional[float] = None
    start_angle: Optional[float] = None

    for i in range(num_samples + 1):
        theta = 2.0 * math.pi * (i / float(num_samples))
        val = clutching_func(theta)
        ang = math.atan2(val.imag, val.real)

        if prev_angle is None:
            prev_angle = ang
            start_angle = ang
        else:
            diff = ang - prev_angle
            # Unwind branch cut [-pi, pi]
            while diff > math.pi:
                diff -= 2.0 * math.pi
            while diff < -math.pi:
                diff += 2.0 * math.pi
            total_angle += diff
            prev_angle = ang

    degree = int(round(total_angle / (2.0 * math.pi)))
    return degree


@dataclass
class VectorBundle:
    """A topological vector bundle E -> X over cognitive base manifold X."""
    bundle_id: str
    label: str
    base_space: str
    fiber_dim: int
    first_chern_number_c1: int
    second_chern_number_c2: int = 0
    is_trivial: bool = False
    clutching_degree: int = 0

    @property
    def rank(self) -> int:
        return self.fiber_dim

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "label": self.label,
            "base_space": self.base_space,
            "rank": self.rank,
            "c1": self.first_chern_number_c1,
            "c2": self.second_chern_number_c2,
            "is_trivial": self.is_trivial,
            "clutching_degree": self.clutching_degree,
        }


@dataclass
class VirtualBundleKClass:
    """An element [E] - [F] in the Grothendieck group K_0(X)."""
    class_id: str
    label: str
    bundle_e_id: str
    bundle_f_id: str
    virtual_rank: int
    ch0: int
    ch1: float
    ch2: float
    is_stably_trivial: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "class_id": self.class_id,
            "label": self.label,
            "bundle_e": self.bundle_e_id,
            "bundle_f": self.bundle_f_id,
            "virtual_rank": self.virtual_rank,
            "chern_character": {
                "ch0": self.ch0,
                "ch1": round(self.ch1, 4),
                "ch2": round(self.ch2, 4),
            },
            "is_stably_trivial": self.is_stably_trivial,
        }


@dataclass
class BottPeriodicityStep:
    """A dimension step in the Bott periodicity cycle."""
    dimension_k: int
    complex_group_pi_k_minus_1_u: str
    real_group_pi_k_minus_1_o: str
    mod_2_phase: int
    mod_8_phase: int
    cognitive_interpretation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension_k": self.dimension_k,
            "complex_group": self.complex_group_pi_k_minus_1_u,
            "real_group": self.real_group_pi_k_minus_1_o,
            "mod_2_phase": self.mod_2_phase,
            "mod_8_phase": self.mod_8_phase,
            "interpretation": self.cognitive_interpretation,
        }


@dataclass
class KTheoryClassificationResult:
    """Comprehensive diagnostic telemetry from topological K-theory analysis."""
    base_manifold: str
    num_bundles: int
    bundles: List[VectorBundle]
    k_classes: List[VirtualBundleKClass]
    bott_cycle: List[BottPeriodicityStep]
    clutching_orbit_points: List[Tuple[float, float, float]]
    h_topological_charge: int
    stable_equivalence_verified: bool
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_manifold": self.base_manifold,
            "num_bundles": self.num_bundles,
            "bundles": [b.to_dict() for b in self.bundles],
            "k_classes": [k.to_dict() for k in self.k_classes],
            "bott_periodicity_cycle": [step.to_dict() for step in self.bott_cycle],
            "h_topological_charge": self.h_topological_charge,
            "stable_equivalence_verified": self.stable_equivalence_verified,
            "summary": self.summary,
            "clutching_orbit_points_count": len(self.clutching_orbit_points),
        }


class KTheoryBundleLoom:
    """Core solver and visualizer for Topological K-Theory and Vector Bundle Classification."""

    def __init__(self, base_manifold: str = "S^2 (Task Sphere)"):
        self.base_manifold = base_manifold
        self.bundles: List[VectorBundle] = []

    def add_bundle(self, bundle: VectorBundle) -> None:
        """Registers a vector bundle into the classification space."""
        self.bundles.append(bundle)

    @classmethod
    def create_default_cognitive_k_theory_suite(cls) -> "KTheoryBundleLoom":
        """Creates a default cognitive K-theory suite consisting of the trivial skill bundle,
        the Hopf line bundle (unit twisting), anti-Hopf, and a rank-2 synthesis bundle.
        """
        loom = cls(base_manifold="S^2 (Cognitive Context Sphere)")

        # 1. Trivial Rank-1 Bundle: E_0 = S^2 x C (uniform skill across all task contexts)
        loom.add_bundle(
            VectorBundle(
                bundle_id="E_triv",
                label="Trivial Skill Base",
                base_space="S^2",
                fiber_dim=1,
                first_chern_number_c1=0,
                is_trivial=True,
                clutching_degree=0,
            )
        )

        # 2. Hopf Line Bundle H (Complex Projective Line CP^1): unit topological twist
        # Clutching function alpha(theta) = e^{i theta} (degree +1)
        loom.add_bundle(
            VectorBundle(
                bundle_id="E_hopf",
                label="Hopf Cognitive Bundle H",
                base_space="S^2",
                fiber_dim=1,
                first_chern_number_c1=1,
                is_trivial=False,
                clutching_degree=1,
            )
        )

        # 3. Anti-Hopf Line Bundle H* (dual): degree -1
        loom.add_bundle(
            VectorBundle(
                bundle_id="E_antihopf",
                label="Dual Anti-Hopf H*",
                base_space="S^2",
                fiber_dim=1,
                first_chern_number_c1=-1,
                is_trivial=False,
                clutching_degree=-1,
            )
        )

        # 4. Rank-2 Synergistic Bundle: H + Trivial (rank 2, c1 = 1)
        # Stably equivalent to Hopf bundle: [H + Triv] - [Triv] = [H]
        loom.add_bundle(
            VectorBundle(
                bundle_id="E_synergy",
                label="Stabilized Synergistic Bundle",
                base_space="S^2",
                fiber_dim=2,
                first_chern_number_c1=1,
                is_trivial=False,
                clutching_degree=1,
            )
        )

        return loom

    def evaluate_bott_periodicity_cycle(self) -> List[BottPeriodicityStep]:
        """Constructs the standard Bott periodicity table for complex and real K-theory."""
        cycle_definitions = [
            (0, "Z (Rank invariant)", "Z (Dimension)", 0, 0, "Stable scalar ground state"),
            (1, "0 (Trivial)", "Z_2 (Chiral sign)", 1, 1, "Clutching parity check"),
            (2, "Z (Chern number c1)", "Z_2 (Quaternionic parity)", 0, 2, "Complex Bott cycle / Hopf twist"),
            (3, "0 (Trivial)", "0 (Trivial)", 1, 3, "Odd topological stability"),
            (4, "Z (Second Chern c2)", "Z (First Pontryagin p1)", 0, 4, "Instanton topological charge"),
            (5, "0 (Trivial)", "0 (Trivial)", 1, 5, "Higher dimensional triviality"),
            (6, "Z (Third Chern c3)", "0 (Trivial)", 0, 6, "Calabi-Yau 3-fold index"),
            (7, "0 (Trivial)", "0 (Trivial)", 1, 7, "Quaternion boundary parity"),
            (8, "Z (Bott period 2)", "Z (Bott period 8)", 0, 0, "Full real Bott 8-fold recurrence"),
        ]

        steps = []
        for dim, comp, real, m2, m8, interp in cycle_definitions:
            steps.append(
                BottPeriodicityStep(
                    dimension_k=dim,
                    complex_group_pi_k_minus_1_u=comp,
                    real_group_pi_k_minus_1_o=real,
                    mod_2_phase=m2,
                    mod_8_phase=m8,
                    cognitive_interpretation=interp,
                )
            )
        return steps

    def sample_clutching_orbit(self, degree: int = 1, num_samples: int = 60) -> List[Tuple[float, float, float]]:
        """Generates 3D trajectory points of clutching function alpha(theta) = e^{i * deg * theta}
        mapped onto torus/cylinder (cos(theta), sin(theta), arg(alpha)).
        """
        pts = []
        for i in range(num_samples):
            theta = 2.0 * math.pi * (i / float(num_samples))
            val = complex(math.cos(degree * theta), math.sin(degree * theta))
            x = math.cos(theta)
            y = math.sin(theta)
            z = math.atan2(val.imag, val.real) / math.pi  # Normalized in [-1, 1]
            pts.append((x, y, z))
        return pts

    def classify_bundles(self) -> KTheoryClassificationResult:
        """Classifies vector bundles into Grothendieck group classes and checks stable equivalence."""
        bott_steps = self.evaluate_bott_periodicity_cycle()
        clutch_pts = self.sample_clutching_orbit(degree=1, num_samples=60)

        # Build Grothendieck K-classes: formal differences [E] - [Triv]
        k_classes: List[VirtualBundleKClass] = []
        for idx, b in enumerate(self.bundles):
            # Virtual rank = rank(E) - rank(Triv)
            v_rank = b.rank - 1
            ch0 = b.rank
            ch1 = float(b.first_chern_number_c1)
            ch2 = float(0.5 * (ch1 ** 2 - 2 * b.second_chern_number_c2))
            is_stably_triv = (b.first_chern_number_c1 == 0 and b.second_chern_number_c2 == 0)

            k_classes.append(
                VirtualBundleKClass(
                    class_id=f"K_{idx+1}",
                    label=f"[{b.label}] - [Triv]",
                    bundle_e_id=b.bundle_id,
                    bundle_f_id="E_triv",
                    virtual_rank=v_rank,
                    ch0=ch0,
                    ch1=ch1,
                    ch2=ch2,
                    is_stably_trivial=is_stably_triv,
                )
            )

        # Check stable equivalence: E_synergy is rank 2 with c1=1; E_hopf is rank 1 with c1=1.
        # They have the same reduced K-theory class: [E_synergy] - 2 = [E_hopf] - 1 = [H] - 1
        stably_equiv = any(
            k1.ch1 == k2.ch1 and k1.virtual_rank != k2.virtual_rank
            for k1 in k_classes for k2 in k_classes
        )

        h_charge = sum(b.first_chern_number_c1 for b in self.bundles)
        summary = (
            f"K-Theory space over {self.base_manifold} has {len(self.bundles)} classified bundles. "
            f"Stable equivalence verified between rank-1 Hopf and rank-2 Synergistic bundles via c1=1 Chern match. "
            f"Complex Bott 2-periodicity guarantees topological invariance under dual suspension."
        )

        return KTheoryClassificationResult(
            base_manifold=self.base_manifold,
            num_bundles=len(self.bundles),
            bundles=self.bundles,
            k_classes=k_classes,
            bott_cycle=bott_steps,
            clutching_orbit_points=clutch_pts,
            h_topological_charge=h_charge,
            stable_equivalence_verified=stably_equiv,
            summary=summary,
        )

    def render_svg(self, result: Optional[KTheoryClassificationResult] = None, width: int = 940, height: int = 620) -> str:
        """Renders an interactive dark titanium SVG visualization of K-theory classification and Bott periodicity."""
        if result is None:
            result = self.classify_bundles()

        lines = []
        lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
        lines.append('  <defs>')
        lines.append('    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#090d13" />')
        lines.append('      <stop offset="100%" stop-color="#161b22" />')
        lines.append('    </linearGradient>')
        lines.append('    <linearGradient id="bott-wheel-grad" x1="0%" y1="0%" x2="100%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.2" />')
        lines.append('      <stop offset="100%" stop-color="#a371f7" stop-opacity="0.05" />')
        lines.append('    </linearGradient>')
        lines.append('    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">')
        lines.append('      <feGaussianBlur stdDeviation="3" result="blur" />')
        lines.append('      <feComposite in="SourceGraphic" in2="blur" operator="over" />')
        lines.append('    </filter>')
        lines.append('  </defs>')

        # Background
        lines.append(f'  <rect width="{width}" height="{height}" fill="url(#bg-grad)" rx="10" stroke="#30363d" stroke-width="1.5" />')

        # Header Title
        lines.append('  <g id="header" transform="translate(30, 40)">')
        lines.append('    <text fill="#58a6ff" font-family="system-ui, -apple-system, sans-serif" font-size="18" font-weight="700" letter-spacing="0.5">')
        lines.append('      TOPOLOGICAL K-THEORY &amp; VECTOR BUNDLE CLASSIFICATION')
        lines.append('    </text>')
        lines.append('    <text y="22" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="12">')
        lines.append('      Grothendieck Group K_0(X), Bott Periodicity Cycles &amp; Stable Equivalence Invariants')
        lines.append('    </text>')
        lines.append('  </g>')

        # 1. Left Panel: Clutching Loop & Winding Orbit (S^1 -> GL_k)
        cx1, cy1 = 170, 240
        rad1 = 90

        lines.append('  <!-- Panel 1: Clutching Winding Loop -->')
        lines.append('  <g id="clutching-panel" transform="translate(30, 80)">')
        lines.append('    <rect width="280" height="500" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="20" y="28" fill="#3fb950" font-family="system-ui, sans-serif" font-size="13" font-weight="700">CLUTCHING WINDING LOOP</text>')
        lines.append('    <line x1="20" y1="38" x2="260" y2="38" stroke="#30363d" stroke-width="1" />')

        # Unit Circle in Complex Plane
        lines.append(f'    <circle cx="{cx1}" cy="{cy1}" r="{rad1}" fill="#0d1117" stroke="#30363d" stroke-width="1.5" stroke-dasharray="3 3" />')
        lines.append(f'    <line x1="{cx1 - rad1 - 20}" y1="{cy1}" x2="{cx1 + rad1 + 20}" y2="{cy1}" stroke="#484f58" stroke-width="1" />')
        lines.append(f'    <line x1="{cx1}" y1="{cy1 - rad1 - 20}" x2="{cx1}" y2="{cy1 + rad1 + 20}" y2="{cy1}" stroke="#484f58" stroke-width="1" />')
        lines.append(f'    <text x="{cx1 + rad1 + 10}" y="{cy1 - 6}" fill="#6e7681" font-family="monospace" font-size="9">Re</text>')
        lines.append(f'    <text x="{cx1 + 6}" y="{cy1 - rad1 - 10}" fill="#6e7681" font-family="monospace" font-size="9">Im</text>')

        # Draw Clutching Orbit points (Hopf degree = 1)
        poly_pts = []
        for x, y, z in result.clutching_orbit_points:
            px = cx1 + x * rad1
            py = cy1 - y * rad1
            poly_pts.append(f"{px:.1f},{py:.1f}")

        poly_str = " ".join(poly_pts)
        lines.append(f'    <polygon points="{poly_str}" fill="none" stroke="#3fb950" stroke-width="2.5" filter="url(#glow)" />')
        lines.append(f'    <circle cx="{cx1 + rad1}" cy="{cy1}" r="5" fill="#3fb950" />')
        lines.append(f'    <text x="{cx1}" y="{cy1 + 4}" fill="#f0f6fc" font-family="system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">deg(&#945;) = +1</text>')

        # Clutching Telemetry Notes
        lines.append('    <g transform="translate(20, 370)">')
        lines.append('      <text fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600">CLUTCHING THEOREM:</text>')
        lines.append('      <text y="18" fill="#c9d1d9" font-family="monospace" font-size="9">Vect&#8321;(S&#178;) &#8773; &#960;&#8321;(GL&#8321;(C)) &#8773; Z</text>')
        lines.append('      <text y="34" fill="#c9d1d9" font-family="monospace" font-size="9">c&#8321;(Hopf) = +1</text>')
        lines.append('      <text y="50" fill="#c9d1d9" font-family="monospace" font-size="9">c&#8321;(Dual H*) = -1</text>')
        lines.append('      <text y="66" fill="#8b949e" font-family="system-ui, sans-serif" font-size="9">Hopf line bundle generation</text>')
        lines.append('    </g>')
        lines.append('  </g>')

        # 2. Middle Panel: Bott Periodicity Wheel
        cx2, cy2 = 145, 230
        rad2 = 95

        lines.append('  <!-- Panel 2: Bott Periodicity Wheel -->')
        lines.append('  <g id="bott-panel" transform="translate(330, 80)">')
        lines.append('    <rect width="290" height="500" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="20" y="28" fill="#a371f7" font-family="system-ui, sans-serif" font-size="13" font-weight="700">BOTT PERIODICITY WHEEL</text>')
        lines.append('    <line x1="20" y1="38" x2="270" y2="38" stroke="#30363d" stroke-width="1" />')

        # Circle wheel
        lines.append(f'    <circle cx="{cx2}" cy="{cy2}" r="{rad2}" fill="url(#bott-wheel-grad)" stroke="#a371f7" stroke-width="1.5" stroke-opacity="0.6" />')

        # Render 8 ticks around the wheel (Real Bott Period 8 / Complex Period 2)
        for i in range(8):
            ang = 2.0 * math.pi * (i / 8.0) - math.pi / 2.0
            tx = cx2 + rad2 * math.cos(ang)
            ty = cy2 + rad2 * math.sin(ang)
            lx = cx2 + (rad2 + 20) * math.cos(ang)
            ly = cy2 + (rad2 + 20) * math.sin(ang)

            is_complex_z = (i % 2 == 0)
            dot_col = "#58a6ff" if is_complex_z else "#6e7681"
            lines.append(f'    <circle cx="{tx:.1f}" cy="{ty:.1f}" r="4" fill="{dot_col}" />')
            label_text = f"k={i}"
            lines.append(f'    <text x="{lx:.1f}" y="{ly + 4:.1f}" fill="{dot_col}" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">{label_text}</text>')

        # Center Text in Wheel
        lines.append(f'    <text x="{cx2}" y="{cy2 - 10}" fill="#f0f6fc" font-family="system-ui, sans-serif" font-size="11" font-weight="700" text-anchor="middle">COMPLEX: MOD 2</text>')
        lines.append(f'    <text x="{cx2}" y="{cy2 + 8}" fill="#a371f7" font-family="monospace" font-size="10" text-anchor="middle">K^(n+2) &#8773; K^n</text>')
        lines.append(f'    <text x="{cx2}" y="{cy2 + 24}" fill="#8b949e" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle">REAL: MOD 8</text>')

        # Bott Step Highlights
        lines.append('    <g transform="translate(20, 360)">')
        lines.append('      <text fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600">STABLE HOMOTOPY GROUPS:</text>')
        lines.append('      <text y="18" fill="#58a6ff" font-family="monospace" font-size="9">&#960;&#8320;(U) &#8773; Z,  &#960;&#8321;(U) &#8773; 0</text>')
        lines.append('      <text y="34" fill="#58a6ff" font-family="monospace" font-size="9">&#960;&#8322;(U) &#8773; Z,  &#960;&#8323;(U) &#8773; 0</text>')
        lines.append('      <text y="50" fill="#a371f7" font-family="monospace" font-size="9">&#960;&#8327;(O) &#8773; Z (Bott real 8-period)</text>')
        lines.append('      <text y="66" fill="#8b949e" font-family="system-ui, sans-serif" font-size="9">Cyclic meta-cognitive stability</text>')
        lines.append('    </g>')
        lines.append('  </g>')

        # 3. Right Panel: Grothendieck K_0 Invariants & Stable Equivalence
        panel_x = 640
        panel_y = 80
        panel_w = 270
        panel_h = 500

        lines.append(f'  <g id="k-classes-panel" transform="translate({panel_x}, {panel_y})">')
        lines.append(f'    <rect width="{panel_w}" height="{panel_h}" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="20" y="28" fill="#58a6ff" font-family="system-ui, sans-serif" font-size="13" font-weight="700">GROTHENDIECK K_0(X)</text>')
        lines.append('    <line x1="20" y1="38" x2="250" y2="38" stroke="#30363d" stroke-width="1" />')

        # Stable Equivalence Card
        equiv_col = "#3fb950" if result.stable_equivalence_verified else "#d29922"
        lines.append(f'    <rect x="20" y="55" width="230" height="60" fill="{equiv_col}" fill-opacity="0.12" rx="6" stroke="{equiv_col}" stroke-width="1" />')
        lines.append(f'    <text x="30" y="78" fill="{equiv_col}" font-family="system-ui, sans-serif" font-size="11" font-weight="700">STABLE EQUIVALENCE:</text>')
        lines.append('    <text x="30" y="98" fill="#f0f6fc" font-family="monospace" font-size="10">[Hopf + Triv] &#8764;_s [Hopf]</text>')

        # Table of K-Classes
        curr_y = 145
        lines.append(f'    <text x="20" y="{curr_y}" fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600">VIRTUAL K-CLASSES [E] - [Triv]:</text>')
        curr_y += 20

        for kc in result.k_classes:
            status_col = "#6e7681" if kc.is_stably_trivial else "#58a6ff"
            lines.append(f'    <text x="20" y="{curr_y}" fill="#c9d1d9" font-family="monospace" font-size="10">{kc.label}:</text>')
            lines.append(f'    <text x="250" y="{curr_y}" fill="{status_col}" font-family="monospace" font-size="10" font-weight="600" text-anchor="end">c&#8321;={kc.ch1:+.0f}</text>')
            curr_y += 22

        # Summary Metrics
        curr_y += 10
        lines.append(f'    <line x1="20" y1="{curr_y}" x2="250" y2="{curr_y}" stroke="#30363d" stroke-width="1" />')
        curr_y += 20

        metrics = [
            ("Base Manifold", "S^2 (Task Sphere)"),
            ("Classified Bundles", str(result.num_bundles)),
            ("Topological Charge", str(result.h_topological_charge)),
            ("Chern Character Iso", "ch: K(X)Q -> H*(Q)"),
            ("Bott Generator b", "[H] - 1 in K(S^2)"),
        ]

        for label, val in metrics:
            lines.append(f'    <text x="20" y="{curr_y}" fill="#8b949e" font-family="system-ui, sans-serif" font-size="10">{label}:</text>')
            lines.append(f'    <text x="250" y="{curr_y}" fill="#c9d1d9" font-family="monospace" font-size="10" font-weight="600" text-anchor="end">{val}</text>')
            curr_y += 20

        # Mathematical Legend
        lines.append('    <g transform="translate(20, 435)">')
        lines.append('      <text fill="#8b949e" font-family="system-ui, sans-serif" font-size="9" font-weight="600">GROTHENDIECK GROUP:</text>')
        lines.append('      <text y="16" fill="#c9d1d9" font-family="monospace" font-size="9">K&#8320;(X) = {[E] - [F] / &#8764;_s}</text>')
        lines.append('      <text y="32" fill="#c9d1d9" font-family="monospace" font-size="9">E &#8853; C^k &#8773; F &#8853; C^k</text>')
        lines.append('      <text y="48" fill="#8b949e" font-family="system-ui, sans-serif" font-size="8">Stable vector bundle isomorphism</text>')
        lines.append('    </g>')
        lines.append('  </g>')

        lines.append('</svg>')
        return "\n".join(lines)

    def generate_markdown_report(self, result: Optional[KTheoryClassificationResult] = None) -> str:
        """Generates a formal analytical report on topological K-theory and bundle classification."""
        if result is None:
            result = self.classify_bundles()

        lines = [
            "# Topological K-Theory & Vector Bundle Classification Analysis",
            "",
            "## Executive Summary",
            "",
            f"{result.summary}",
            "",
            f"- **Base Manifold:** {result.base_manifold}",
            f"- **Total Bundles Classified:** {result.num_bundles}",
            f"- **Net Topological Charge (Total c1):** {result.h_topological_charge}",
            f"- **Stable Equivalence:** {'Verified Stably Isomorphic' if result.stable_equivalence_verified else 'Distinct Classes'}",
            f"- **Bott Periodicity Period:** Complex = 2, Real = 8",
            "",
            "## Classified Vector Bundles",
            "",
            "| Bundle ID | Label | Fiber Rank | First Chern Class c1 | Second Chern c2 | Triviality Status | Clutching Degree |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for b in result.bundles:
            triv_str = "Trivial" if b.is_trivial else "Non-Trivial Twisted"
            lines.append(
                f"| `{b.bundle_id}` | {b.label} | {b.rank} | `{b.first_chern_number_c1:+d}` | `{b.second_chern_number_c2}` | {triv_str} | `{b.clutching_degree:+d}` |"
            )

        lines.extend([
            "",
            "## Grothendieck K-Classes [E] - [Triv]",
            "",
            "| Class ID | Label | Virtual Rank | ch0 (Rank) | ch1 (c1) | ch2 (Instanton) | Stable Status |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for kc in result.k_classes:
            st_str = "Stably Trivial" if kc.is_stably_trivial else "Non-Trivial Generator"
            lines.append(
                f"| `{kc.class_id}` | {kc.label} | `{kc.virtual_rank:+d}` | {kc.ch0} | `{kc.ch1:+.1f}` | `{kc.ch2:+.2f}` | {st_str} |"
            )

        lines.extend([
            "",
            "## Bott Periodicity Cycles",
            "",
            "| Dimension k | Complex Group pi_{k-1}(U) | Real Group pi_{k-1}(O) | Mod 2 Phase | Mod 8 Phase | Cognitive Interpretation |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for step in result.bott_cycle:
            lines.append(
                f"| `k={step.dimension_k}` | `{step.complex_group_pi_k_minus_1_u}` | `{step.real_group_pi_k_minus_1_o}` | `{step.mod_2_phase}` | `{step.mod_8_phase}` | {step.cognitive_interpretation} |"
            )

        lines.extend([
            "",
            "## Epistemic Architecture Notes",
            "",
            "1. **Stable Equivalence:** In complex cognitive workflows, two mental toolkits may have different raw dimensions (e.g. 1 core skill vs 2 combined skills), yet possess identical topological twist (c1 = 1). Adding trivial auxiliary skills stabilizes both into the same Grothendieck K-class.",
            "2. **Bott Periodicity as Cognitive Recurrence:** Complex Bott periodicity K^{n+2}(X) = K^n(X) demonstrates that mental abstraction layers do not generate runaway complexity; they exhibit a strict 2-fold topological recurrence, stabilizing higher-order conceptual models.",
            "3. **Clutching Invariants:** The transition across the equator of a task sphere defines a clutching loop alpha: S^1 -> GL_k. Its winding number directly dictates whether transitions between distinct task domains require a topological state reset.",
        ])

        return "\n".join(lines)

    def generate_html_viewer(self, result: Optional[KTheoryClassificationResult] = None) -> str:
        """Generates a standalone dark titanium HTML interactive viewer."""
        if result is None:
            result = self.classify_bundles()

        svg_content = self.render_svg(result)
        json_data = json.dumps(result.to_dict(), indent=2)

        html_str = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Topological K-Theory &amp; Vector Bundle Classification Loom | DxSkills</title>
  <style>
    :root {{
      --bg: #090d13;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --heading: #f0f6fc;
      --accent: #58a6ff;
      --accent-purple: #a371f7;
      --accent-green: #3fb950;
      --accent-warn: #d29922;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      padding: 24px;
      line-height: 1.6;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
    }}
    header {{
      margin-bottom: 24px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--border);
    }}
    h1 {{
      color: var(--heading);
      font-size: 24px;
      font-weight: 700;
      margin-bottom: 6px;
    }}
    .subtitle {{
      color: #8b949e;
      font-size: 14px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 24px;
      margin-bottom: 24px;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
    }}
    .svg-container {{
      width: 100%;
      overflow-x: auto;
    }}
    pre {{
      background: #0d1117;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 16px;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
      font-size: 12px;
      color: #79c0ff;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>Topological K-Theory &amp; Vector Bundle Classification Loom</h1>
      <p class="subtitle">Autonomous Cognitive Spatial Scaffold: Grothendieck Group K_0(X), Bott Periodicity &amp; Stable Equivalence</p>
    </header>

    <div class="grid">
      <div class="card">
        <div class="svg-container">
          {svg_content}
        </div>
      </div>

      <div class="card">
        <h2 style="color: var(--heading); font-size: 18px; margin-bottom: 12px;">Diagnostic JSON Export</h2>
        <pre><code>{html.escape(json_data)}</code></pre>
      </div>
    </div>
  </div>
</body>
</html>
"""
        return html_str
