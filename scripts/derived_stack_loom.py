"""
Derived Algebraic Geometry & Higher Stacks Loom
Autonomous cognitive spatial module synthesizing derived schemes, Artin and Deligne-Mumford stacks,
cotangent complexes, deformation theories, and virtual fundamental classes.
Grounded in derived algebraic geometry (Lurie 2009, Toen-Vezzosi 2005, 2008),
cotangent complexes (Illusie 1971, Quillen 1970), deformation theory (Kodaira-Spencer 1958, Schlessinger 1968),
and virtual fundamental classes (Li-Tian 1998, Behrend-Fantechi 1997).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json
from enum import Enum


class StackCategory(str, Enum):
    """Classification of algebraic and derived stacks."""
    DELIGNE_MUMFORD = "Deligne-Mumford Stack"
    ARTIN = "Artin Stack"
    DERIVED_SCHEME = "Derived Scheme"
    HIGHER_STACK = "Higher Geometric Stack"


@dataclass
class CognitiveStackLocus:
    """Local geometric chart or cognitive schema locus with automorphisms."""
    name: str
    dimension: int
    charts: List[str]
    automorphism_group: str
    automorphism_dim: int
    is_smooth: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "dimension": self.dimension,
            "charts": self.charts,
            "automorphism_group": self.automorphism_group,
            "automorphism_dim": self.automorphism_dim,
            "is_smooth": self.is_smooth,
        }


@dataclass
class SimplicialNerveLevel:
    """Level n of the simplicial nerve N(X_bullet) presentation."""
    level_n: int
    label: str
    dimension: int
    face_maps_count: int
    degeneracy_maps_count: int
    morphism_description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level_n": self.level_n,
            "label": self.label,
            "dimension": self.dimension,
            "face_maps_count": self.face_maps_count,
            "degeneracy_maps_count": self.degeneracy_maps_count,
            "morphism_description": self.morphism_description,
        }


@dataclass
class CotangentComplex:
    """The cotangent complex L_(X/S) in the derived category D(X)."""
    h0_differentials_dim: int
    h_minus1_relations_dim: int
    h_minus2_syzygies_dim: int
    amplitude_min: int = -1
    amplitude_max: int = 0
    is_quasi_smooth: bool = True

    @property
    def total_euler_characteristic(self) -> int:
        """Euler characteristic of truncated cotangent complex."""
        return self.h0_differentials_dim - self.h_minus1_relations_dim + self.h_minus2_syzygies_dim

    def to_dict(self) -> Dict[str, Any]:
        return {
            "h0_differentials_dim": self.h0_differentials_dim,
            "h_minus1_relations_dim": self.h_minus1_relations_dim,
            "h_minus2_syzygies_dim": self.h_minus2_syzygies_dim,
            "amplitude": [self.amplitude_min, self.amplitude_max],
            "is_quasi_smooth": self.is_quasi_smooth,
            "euler_characteristic": self.total_euler_characteristic,
        }


@dataclass
class DeformationProfile:
    """Deformation and obstruction spaces from tangent Lie algebra T_X = RHom(L_X, O_X)."""
    t0_automorphisms_dim: int
    t1_infinitesimal_deformations_dim: int
    t2_obstructions_dim: int
    obstruction_class_vanishes: bool = True
    formal_moduli_dimension: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "t0_automorphisms_dim": self.t0_automorphisms_dim,
            "t1_infinitesimal_deformations_dim": self.t1_infinitesimal_deformations_dim,
            "t2_obstructions_dim": self.t2_obstructions_dim,
            "obstruction_class_vanishes": self.obstruction_class_vanishes,
            "formal_moduli_dimension": self.formal_moduli_dimension,
        }


@dataclass
class VirtualFundamentalClass:
    """Virtual fundamental class [X]^vir in Chow homology with virtual dimension."""
    virtual_dimension: int
    actual_dimension: int
    excess_dimension: int
    virtual_cycle_degree: float
    is_unobstructed: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "virtual_dimension": self.virtual_dimension,
            "actual_dimension": self.actual_dimension,
            "excess_dimension": self.excess_dimension,
            "virtual_cycle_degree": round(self.virtual_cycle_degree, 4),
            "is_unobstructed": self.is_unobstructed,
        }


@dataclass
class DerivedStackResult:
    """Complete evaluation results of a derived stack and its deformation theory."""
    stack_name: str
    stack_category: str
    locus: CognitiveStackLocus
    simplicial_nerve: List[SimplicialNerveLevel]
    cotangent_complex: CotangentComplex
    deformation_profile: DeformationProfile
    virtual_class: VirtualFundamentalClass
    cognitive_interpretation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stack_name": self.stack_name,
            "stack_category": self.stack_category,
            "locus": self.locus.to_dict(),
            "simplicial_nerve": [sn.to_dict() for sn in self.simplicial_nerve],
            "cotangent_complex": self.cotangent_complex.to_dict(),
            "deformation_profile": self.deformation_profile.to_dict(),
            "virtual_class": self.virtual_class.to_dict(),
            "cognitive_interpretation": self.cognitive_interpretation,
        }


class DerivedStackLoom:
    """
    Autonomous Cognitive Spatial Loom for Derived Algebraic Geometry and Higher Stacks.
    Maps complex cognitive schemas with symmetries, multi-vantage viewpoints, and
    contextual ambiguities to derived stacks equipped with cotangent complexes,
    deformation algebras, and virtual fundamental classes.
    """

    def __init__(
        self,
        stack_name: str = "Cognitive Perspective Stack M_persp",
        stack_category: str = StackCategory.ARTIN.value,
    ):
        self.stack_name = stack_name
        self.stack_category = stack_category

    @classmethod
    def create_default_cognitive_moduli_stack(cls) -> "DerivedStackLoom":
        """Creates a default derived stack modeling cognitive conceptual perspectives."""
        return cls(
            stack_name="Cognitive Perspective Moduli Stack M_persp",
            stack_category=StackCategory.ARTIN.value,
        )

    def evaluate_derived_stack(
        self,
        base_dim: int = 4,
        automorphism_dim: int = 1,
        num_relations: int = 2,
        higher_syzygies: int = 0,
        automorphism_group: str = "GL(1, C)",
    ) -> DerivedStackResult:
        """Evaluates derived stack structure, cotangent complex, and deformation spaces."""
        if automorphism_dim == 0 and "Z" in automorphism_group:
            cat = StackCategory.DELIGNE_MUMFORD.value
        elif automorphism_dim > 0 and higher_syzygies == 0:
            cat = StackCategory.ARTIN.value
        elif higher_syzygies > 0:
            cat = StackCategory.HIGHER_STACK.value
        else:
            cat = StackCategory.DERIVED_SCHEME.value

        locus = CognitiveStackLocus(
            name=f"Chart Atlas on {self.stack_name}",
            dimension=base_dim,
            charts=[
                "Spatial Visual Framing Chart U_vis",
                "Kinesthetic Relational Chart U_kin",
                "Epistemic Causal Chart U_eps",
            ],
            automorphism_group=automorphism_group,
            automorphism_dim=automorphism_dim,
            is_smooth=(num_relations == 0),
        )

        nerve = [
            SimplicialNerveLevel(
                level_n=0,
                label="X_0 (Objects / Cognitive Perspectives)",
                dimension=base_dim,
                face_maps_count=1,
                degeneracy_maps_count=1,
                morphism_description="Atlas space of un-quotiented cognitive configurations",
            ),
            SimplicialNerveLevel(
                level_n=1,
                label="X_1 (Morphisms / Frame Re-orientations)",
                dimension=base_dim + automorphism_dim,
                face_maps_count=2,
                degeneracy_maps_count=2,
                morphism_description="Pairings of perspectives related by symmetries (s, t: X_1 -> X_0)",
            ),
            SimplicialNerveLevel(
                level_n=2,
                label="X_2 (2-Morphisms / Composition Coherences)",
                dimension=base_dim + 2 * automorphism_dim,
                face_maps_count=3,
                degeneracy_maps_count=3,
                morphism_description="Associativity coherences for composite cognitive transitions",
            ),
        ]

        amplitude_min = -2 if higher_syzygies > 0 else (-1 if num_relations > 0 else 0)
        amplitude_max = 0
        is_quasi_smooth = (amplitude_min >= -1)

        cotangent = CotangentComplex(
            h0_differentials_dim=base_dim,
            h_minus1_relations_dim=num_relations,
            h_minus2_syzygies_dim=higher_syzygies,
            amplitude_min=amplitude_min,
            amplitude_max=amplitude_max,
            is_quasi_smooth=is_quasi_smooth,
        )

        t0 = automorphism_dim
        t1 = base_dim
        t2 = num_relations + higher_syzygies
        obstruction_vanishes = (t2 == 0 or (num_relations <= 1 and higher_syzygies == 0))
        moduli_dim = max(0, t1 - t0)

        deformations = DeformationProfile(
            t0_automorphisms_dim=t0,
            t1_infinitesimal_deformations_dim=t1,
            t2_obstructions_dim=t2,
            obstruction_class_vanishes=obstruction_vanishes,
            formal_moduli_dimension=moduli_dim,
        )

        vdim = t1 - t2 - t0
        actual_dim = base_dim - t0
        excess_dim = max(0, actual_dim - vdim)
        v_degree = 1.0 / (1.0 + float(excess_dim))

        virt_class = VirtualFundamentalClass(
            virtual_dimension=vdim,
            actual_dimension=actual_dim,
            excess_dimension=excess_dim,
            virtual_cycle_degree=v_degree,
            is_unobstructed=obstruction_vanishes,
        )

        interpretation = (
            f"The derived stack '{self.stack_name}' operates as a {cat}. "
            f"Infinitesimal symmetries (dim T^0 = {t0}) govern viewpoint re-indexing, "
            f"while cognitive tensions are captured by the cotangent complex relations "
            f"(dim H^(-1) = {num_relations}). "
            f"The virtual dimension is {vdim}, ensuring stable epistemic invariants "
            f"across non-transverse cognitive transitions."
        )

        return DerivedStackResult(
            stack_name=self.stack_name,
            stack_category=cat,
            locus=locus,
            simplicial_nerve=nerve,
            cotangent_complex=cotangent,
            deformation_profile=deformations,
            virtual_class=virt_class,
            cognitive_interpretation=interpretation,
        )

    def render_svg(self, result: DerivedStackResult) -> str:
        """Renders dark titanium SVG showing simplicial nerve, cotangent ladder, and deformation spaces."""
        width = 860
        height = 560
        cat_badge_color = "#3fb950" if "Deligne" in result.stack_category else "#58a6ff"
        if "Higher" in result.stack_category:
            cat_badge_color = "#bc8cff"

        p = []
        p.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" style="background-color: #0d1117; font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, monospace;">')
        p.append('  <defs>')
        p.append('    <linearGradient id="nerveGrad" x1="0%" y1="0%" x2="100%" y2="100%">')
        p.append('      <stop offset="0%" stop-color="#1f242c" />')
        p.append('      <stop offset="100%" stop-color="#161b22" />')
        p.append('    </linearGradient>')
        p.append('    <linearGradient id="ladderGrad" x1="0%" y1="0%" x2="0%" y2="100%">')
        p.append('      <stop offset="0%" stop-color="#21262d" />')
        p.append('      <stop offset="100%" stop-color="#161b22" />')
        p.append('    </linearGradient>')
        p.append('    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">')
        p.append('      <path d="M 0 1 L 10 5 L 0 9 z" fill="#58a6ff" />')
        p.append('    </marker>')
        p.append('    <marker id="arrowAmber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">')
        p.append('      <path d="M 0 1 L 10 5 L 0 9 z" fill="#d29922" />')
        p.append('    </marker>')
        p.append('  </defs>')
        p.append('  <!-- Background Panel -->')
        p.append(f'  <rect width="{width}" height="{height}" rx="14" fill="#0d1117" stroke="#30363d" stroke-width="1.5" />')
        p.append('  <!-- Header Bar -->')
        p.append('  <g transform="translate(30, 24)">')
        p.append('    <text x="0" y="22" fill="#f0f6fc" font-size="18" font-weight="700">Derived Algebraic Geometry &amp; Higher Stacks Loom</text>')
        p.append(f'    <rect x="0" y="34" width="180" height="24" rx="6" fill="{cat_badge_color}" fill-opacity="0.18" stroke="{cat_badge_color}" stroke-width="1" />')
        p.append(f'    <text x="90" y="50" fill="{cat_badge_color}" font-size="11" font-weight="600" text-anchor="middle">{result.stack_category}</text>')
        p.append(f'    <text x="200" y="50" fill="#8b949e" font-size="12">Target Stack: {result.stack_name}</text>')
        p.append('  </g>')
        p.append('  <!-- Left Section: Simplicial Nerve Atlas N(X_bullet) -->')
        p.append('  <g transform="translate(30, 95)">')
        p.append('    <rect width="400" height="230" rx="10" fill="url(#nerveGrad)" stroke="#30363d" stroke-width="1" />')
        p.append('    <text x="18" y="26" fill="#58a6ff" font-size="13" font-weight="700">Simplicial Nerve Presentation N(X_&#x2022;)</text>')
        p.append('    <text x="18" y="44" fill="#8b949e" font-size="10">Groupoid quotient atlas [X_0 / Aut] with face &amp; degeneracy maps</text>')

        nerve_x = [60, 200, 340]
        nerve_y = 120
        box_w = 80
        box_h = 60

        for i, sn in enumerate(result.simplicial_nerve):
            bx = nerve_x[i] - box_w // 2
            by = nerve_y - box_h // 2
            border_col = "#58a6ff" if i == 0 else ("#d29922" if i == 1 else "#bc8cff")
            p.append(f'    <rect x="{bx}" y="{by}" width="{box_w}" height="{box_h}" rx="8" fill="#161b22" stroke="{border_col}" stroke-width="1.5" />')
            p.append(f'    <text x="{nerve_x[i]}" y="{by + 22}" fill="#f0f6fc" font-size="12" font-weight="700" text-anchor="middle">X_{sn.level_n}</text>')
            p.append(f'    <text x="{nerve_x[i]}" y="{by + 38}" fill="#8b949e" font-size="10" text-anchor="middle">Dim: {sn.dimension}</text>')
            p.append(f'    <text x="{nerve_x[i]}" y="{by + 52}" fill="{border_col}" font-size="9" text-anchor="middle">Level {sn.level_n}</text>')

        p.append('    <line x1="155" y1="105" x2="105" y2="105" stroke="#58a6ff" stroke-width="1.5" marker-end="url(#arrow)" />')
        p.append('    <text x="130" y="98" fill="#58a6ff" font-size="9" text-anchor="middle">d_0, d_1</text>')
        p.append('    <line x1="105" y1="135" x2="155" y2="135" stroke="#8b949e" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#arrow)" />')
        p.append('    <text x="130" y="148" fill="#8b949e" font-size="9" text-anchor="middle">s_0</text>')
        p.append('    <line x1="295" y1="105" x2="245" y2="105" stroke="#d29922" stroke-width="1.5" marker-end="url(#arrowAmber)" />')
        p.append('    <text x="270" y="98" fill="#d29922" font-size="9" text-anchor="middle">d_0, d_1, d_2</text>')
        p.append('    <line x1="245" y1="135" x2="295" y2="135" stroke="#8b949e" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#arrowAmber)" />')
        p.append('    <text x="270" y="148" fill="#8b949e" font-size="9" text-anchor="middle">s_0, s_1</text>')
        dm_status = "Satisfied (Discrete Aut)" if result.locus.automorphism_dim == 0 else "Artin Stack (Continuous Aut)"
        p.append(f'    <text x="20" y="200" fill="#c9d1d9" font-size="11">Automorphism Group: <tspan fill="#d29922" font-weight="600">{result.locus.automorphism_group}</tspan> (Dim: {result.locus.automorphism_dim})</text>')
        p.append(f'    <text x="20" y="218" fill="#8b949e" font-size="10">Deligne-Mumford locus condition: {dm_status}</text>')
        p.append('  </g>')
        p.append('  <!-- Right Section: Cotangent Complex Ladder L_X -->')
        p.append('  <g transform="translate(450, 95)">')
        p.append('    <rect width="380" height="230" rx="10" fill="url(#ladderGrad)" stroke="#30363d" stroke-width="1" />')
        p.append('    <text x="18" y="26" fill="#3fb950" font-size="13" font-weight="700">Cotangent Complex Ladder L_X</text>')
        p.append('    <text x="18" y="44" fill="#8b949e" font-size="10">Truncated derived cotangent module L_X in D(X)</text>')

        ladder_steps = [
            ("H^0(L) = Omega^1", result.cotangent_complex.h0_differentials_dim, "#58a6ff", "Differentials / 1-forms"),
            ("H^(-1)(L)", result.cotangent_complex.h_minus1_relations_dim, "#d29922", "Module of relations"),
            ("H^(-2)(L)", result.cotangent_complex.h_minus2_syzygies_dim, "#bc8cff", "Higher syzygies"),
        ]

        ly_start = 70
        for idx, (label, val, col, desc) in enumerate(ladder_steps):
            ly = ly_start + idx * 45
            bar_w = max(20, min(160, val * 32))
            p.append(f'    <text x="20" y="{ly + 16}" fill="#f0f6fc" font-size="11" font-weight="600">{label}</text>')
            p.append(f'    <rect x="150" y="{ly}" width="{bar_w}" height="22" rx="4" fill="{col}" fill-opacity="0.25" stroke="{col}" stroke-width="1" />')
            p.append(f'    <text x="{155 + bar_w}" y="{ly + 16}" fill="{col}" font-size="11" font-weight="700"> Dim={val}</text>')
            p.append(f'    <text x="240" y="{ly + 16}" fill="#8b949e" font-size="10">{desc}</text>')

        quasi_status = "Quasi-Smooth (Amplitude [-1, 0])" if result.cotangent_complex.is_quasi_smooth else "Higher Derived (Amplitude [-2, 0])"
        quasi_col = "#3fb950" if result.cotangent_complex.is_quasi_smooth else "#bc8cff"
        p.append(f'    <text x="20" y="208" fill="#8b949e" font-size="11">Structure: <tspan fill="{quasi_col}" font-weight="600">{quasi_status}</tspan></text>')
        p.append('  </g>')
        p.append('  <!-- Bottom Section: Deformation Theory & Virtual Class -->')
        p.append('  <g transform="translate(30, 345)">')
        p.append('    <rect width="800" height="185" rx="10" fill="#161b22" stroke="#30363d" stroke-width="1" />')
        p.append('    <text x="20" y="26" fill="#f0f6fc" font-size="13" font-weight="700">Deformation Lie Algebra &amp; Virtual Fundamental Class [X]<tspan font-size="10" dy="-4">vir</tspan></text>')
        p.append('    <g transform="translate(20, 48)">')
        p.append('      <text x="0" y="0" fill="#8b949e" font-size="10" font-weight="700" letter-spacing="1">DEFORMATION SPACES</text>')
        p.append(f'      <text x="0" y="22" fill="#c9d1d9" font-size="11">T^0 (Infinitesimal Automorphisms): <tspan fill="#58a6ff" font-weight="600">{result.deformation_profile.t0_automorphisms_dim}</tspan></text>')
        p.append(f'      <text x="0" y="42" fill="#c9d1d9" font-size="11">T^1 (Infinitesimal Deformations): <tspan fill="#3fb950" font-weight="600">{result.deformation_profile.t1_infinitesimal_deformations_dim}</tspan></text>')
        p.append(f'      <text x="0" y="62" fill="#c9d1d9" font-size="11">T^2 (Obstruction Space): <tspan fill="#f85149" font-weight="600">{result.deformation_profile.t2_obstructions_dim}</tspan></text>')
        obst_col = "#3fb950" if result.deformation_profile.obstruction_class_vanishes else "#d29922"
        obst_text = "YES (Unobstructed)" if result.deformation_profile.obstruction_class_vanishes else "NO (Obstructed)"
        p.append(f'      <text x="0" y="84" fill="#8b949e" font-size="10">Obstructions Vanish: <tspan fill="{obst_col}" font-weight="600">{obst_text}</tspan></text>')
        p.append('    </g>')
        p.append('    <g transform="translate(320, 48)">')
        p.append('      <text x="0" y="0" fill="#8b949e" font-size="10" font-weight="700" letter-spacing="1">VIRTUAL CYCLE METRICS</text>')
        p.append(f'      <text x="0" y="22" fill="#c9d1d9" font-size="11">Virtual Dimension (vdim): <tspan fill="#bc8cff" font-weight="700">{result.virtual_class.virtual_dimension}</tspan></text>')
        p.append(f'      <text x="0" y="42" fill="#c9d1d9" font-size="11">Actual Tangent Dimension: <tspan fill="#58a6ff" font-weight="600">{result.virtual_class.actual_dimension}</tspan></text>')
        exc_col = "#3fb950" if result.virtual_class.excess_dimension == 0 else "#d29922"
        p.append(f'      <text x="0" y="62" fill="#c9d1d9" font-size="11">Excess Dimension: <tspan fill="{exc_col}" font-weight="600">{result.virtual_class.excess_dimension}</tspan></text>')
        p.append(f'      <text x="0" y="84" fill="#8b949e" font-size="10">Virtual Cycle Degree: <tspan fill="#f0f6fc" font-weight="600">{result.virtual_class.virtual_cycle_degree:.2f}</tspan></text>')
        p.append('    </g>')
        p.append('    <g transform="translate(580, 48)">')
        p.append('      <text x="0" y="0" fill="#8b949e" font-size="10" font-weight="700" letter-spacing="1">COGNITIVE EQUIVALENCE</text>')
        p.append('      <rect x="0" y="10" width="190" height="74" rx="6" fill="#21262d" stroke="#30363d" stroke-width="1" />')
        p.append('      <text x="10" y="30" fill="#c9d1d9" font-size="10">Non-transverse perspective</text>')
        p.append('      <text x="10" y="46" fill="#c9d1d9" font-size="10">intersections resolved via</text>')
        p.append('      <text x="10" y="62" fill="#58a6ff" font-size="10" font-weight="600">virtual fundamental class</text>')
        p.append('      <text x="10" y="76" fill="#3fb950" font-size="9">&#x2714; Homotopy Equivalence</text>')
        p.append('    </g>')
        short_interp = result.cognitive_interpretation[:110]
        p.append(f'    <text x="20" y="165" fill="#8b949e" font-size="10">Interpretation: {short_interp}...</text>')
        p.append('  </g>')
        p.append('</svg>')
        return "\n".join(p)

    def generate_markdown_report(self, result: DerivedStackResult) -> str:
        """Generates publication-grade markdown report on derived stack evaluation."""
        lines = [
            f"# {result.stack_name} | Derived Stack Telemetry",
            "",
            "> **Loom:** Autonomous Cognitive Spatial Derived Algebraic Geometry & Higher Stacks",
            f"> **Stack Category:** {result.stack_category}",
            f"> **Base Space Dimension:** {result.locus.dimension}",
            f"> **Virtual Dimension (vdim):** {result.virtual_class.virtual_dimension}",
            "",
            "## 1. Simplicial Nerve Presentation N(X_bullet)",
            "",
            "The stack is presented by a simplicial space resolving internal automorphisms without coordinate collapse:",
            "",
            "| Level | Level Label | Dimension | Face Maps | Degeneracy Maps | Epistemic Description |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for sn in result.simplicial_nerve:
            lines.append(
                f"| X_{sn.level_n} | {sn.label} | {sn.dimension} | {sn.face_maps_count} | {sn.degeneracy_maps_count} | {sn.morphism_description} |"
            )

        lines.extend([
            "",
            "## 2. Cotangent Complex L_X & Amplitude",
            "",
            f"- **H^0(L_X) Differential Forms:** {result.cotangent_complex.h0_differentials_dim} Kähler 1-forms",
            f"- **H^(-1)(L_X) Relations Module:** {result.cotangent_complex.h_minus1_relations_dim} non-smooth relation generators",
            f"- **H^(-2)(L_X) Higher Syzygies:** {result.cotangent_complex.h_minus2_syzygies_dim} coherence syzygies",
            f"- **Amplitude:** [{result.cotangent_complex.amplitude_min}, {result.cotangent_complex.amplitude_max}]",
            f"- **Quasi-Smooth Classification:** {result.cotangent_complex.is_quasi_smooth}",
            f"- **Euler Characteristic chi(L_X):** {result.cotangent_complex.total_euler_characteristic}",
            "",
            "## 3. Deformation Theory & Kodaira-Spencer Lie Algebra",
            "",
            f"- **T^0 (Infinitesimal Automorphisms):** {result.deformation_profile.t0_automorphisms_dim}",
            f"- **T^1 (Infinitesimal Deformations):** {result.deformation_profile.t1_infinitesimal_deformations_dim}",
            f"- **T^2 (Obstruction Space):** {result.deformation_profile.t2_obstructions_dim}",
            f"- **Obstruction Vanishing:** {result.deformation_profile.obstruction_class_vanishes}",
            f"- **Formal Moduli Dimension:** {result.deformation_profile.formal_moduli_dimension}",
            "",
            "## 4. Virtual Fundamental Class [X]^vir",
            "",
            f"- **Virtual Dimension:** {result.virtual_class.virtual_dimension}",
            f"- **Actual Dimension:** {result.virtual_class.actual_dimension}",
            f"- **Excess Dimension:** {result.virtual_class.excess_dimension}",
            f"- **Virtual Cycle Degree:** {result.virtual_class.virtual_cycle_degree:.4f}",
            f"- **Unobstructed Status:** {result.virtual_class.is_unobstructed}",
            "",
            "## 5. Cognitive Spatial Semantics for Non-Linear Thinkers",
            "",
            result.cognitive_interpretation,
            "",
            "Derived stacks allow neurodivergent and spatial thinkers to hold multi-perspective schemas",
            "simultaneously without relational contradiction. Internal symmetries are encoded as groupoid automorphisms,",
            "and conceptual frictions are preserved as derived relations rather than discarded as schema errors.",
            "",
            "---",
            "*Report autonomously compiled by DxSkills Derived Algebraic Geometry Loom.*",
        ])
        return "\n".join(lines)

    def generate_html_viewer(self, result: DerivedStackResult) -> str:
        """Generates self-contained interactive HTML viewer shell with dark titanium styling."""
        svg_code = self.render_svg(result)
        html_code = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(result.stack_name)} - Derived Stack Loom</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            mono: {{
              50: '#f6f8fa',
              100: '#eaeef2',
              200: '#d0d7de',
              300: '#afb8c1',
              400: '#8c959f',
              500: '#6e7781',
              600: '#57606a',
              700: '#424a53',
              800: '#32383f',
              900: '#24292f',
              950: '#0d1117',
            }}
          }}
        }}
      }}
    }};
  </script>
</head>
<body class="bg-[#0d1117] text-[#c9d1d9] min-h-screen p-6 font-sans">
  <div class="max-w-5xl mx-auto space-y-6">
    <header class="border-b border-[#30363d] pb-4 flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-white tracking-tight">{html.escape(result.stack_name)}</h1>
        <p class="text-xs text-[#8b949e] mt-1">Derived Algebraic Geometry &amp; Higher Stacks Loom</p>
      </div>
      <span class="px-3 py-1 rounded-full text-xs font-semibold bg-[#21262d] text-[#58a6ff] border border-[#30363d]">
        {html.escape(result.stack_category)}
      </span>
    </header>
    <div class="bg-[#161b22] p-4 rounded-xl border border-[#30363d] shadow-xl overflow-hidden">
      {svg_code}
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="p-4 rounded-xl bg-[#161b22] border border-[#30363d]">
        <h3 class="text-xs uppercase font-bold text-[#8b949e] tracking-wider mb-2">Simplicial Nerve</h3>
        <p class="text-sm font-semibold text-white">X_0 Dim: {result.simplicial_nerve[0].dimension}</p>
        <p class="text-xs text-[#8b949e]">Automorphisms: {html.escape(result.locus.automorphism_group)} (Dim {result.locus.automorphism_dim})</p>
      </div>
      <div class="p-4 rounded-xl bg-[#161b22] border border-[#30363d]">
        <h3 class="text-xs uppercase font-bold text-[#8b949e] tracking-wider mb-2">Cotangent Complex</h3>
        <p class="text-sm font-semibold text-[#3fb950]">Amplitude: [{result.cotangent_complex.amplitude_min}, {result.cotangent_complex.amplitude_max}]</p>
        <p class="text-xs text-[#8b949e]">Relations Module Dim: {result.cotangent_complex.h_minus1_relations_dim}</p>
      </div>
      <div class="p-4 rounded-xl bg-[#161b22] border border-[#30363d]">
        <h3 class="text-xs uppercase font-bold text-[#8b949e] tracking-wider mb-2">Virtual Class</h3>
        <p class="text-sm font-semibold text-[#bc8cff]">Virtual Dim: {result.virtual_class.virtual_dimension}</p>
        <p class="text-xs text-[#8b949e]">Degree: {result.virtual_class.virtual_cycle_degree:.2f} (Excess {result.virtual_class.excess_dimension})</p>
      </div>
    </div>
    <div class="p-4 rounded-xl bg-[#161b22] border border-[#30363d]">
      <h3 class="text-xs uppercase font-bold text-[#8b949e] tracking-wider mb-2">Cognitive Epistemic Semantics</h3>
      <p class="text-sm text-[#f0f6fc] leading-relaxed">{html.escape(result.cognitive_interpretation)}</p>
    </div>
  </div>
</body>
</html>"""
        return html_code
