r"""
Beyond Endoscopy & Langlands Functoriality Loom.
Models Robert Langlands' Beyond Endoscopy proposal for establishing general functoriality:
- Dual group representations r: ^L G -> GL(N, C) and automorphic L-functions L(s, pi, r)
- Isolation of functorial transfers via pole residues at s = 1: Res_{s=1} L(s, pi, r)
- Poisson summation formula applied to geometric orbital integrals over rational classes
- Destructive interference and cancellation of non-transferred orbital contributions
- Altug unipotent smoothing and regularized trace kernels
- Dual-space cognitive scaffolding for non-linear, spatial, and dyslexic thinkers
Strictly zero em dashes (chr(8212)) across all functions, docstrings, and comments.
"""

import math
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


class BeyondEndoscopyArchetype(str, Enum):
    """Canonical Beyond Endoscopy settings and functorial transfers."""
    GL2_SYMMETRIC_SQUARE = "GL(2) with r = Sym^2 (Gelbart-Jacquet Functorial Lift to GL(3))"
    GL2_TIMES_GL2_RANKIN = "GL(2) x GL(2) with r = tensor (Rankin-Selberg Lift to GL(4))"
    GL3_ADJOINT_OCTET = "GL(3) with r = Adjoint (Self-Dual Classification in GL(8))"
    ALTUG_POISSON_GL2 = "GL(2) Altug Poisson Summation & Unipotent Subtraction Regularization"


@dataclass
class DualRepresentationData:
    """Representation r of Langlands dual group ^L G."""
    dual_group_label: str
    representation_r_label: str
    representation_dimension: int
    is_self_dual: bool
    functorial_target_group: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dual_group_label": self.dual_group_label,
            "representation_r_label": self.representation_r_label,
            "representation_dimension": self.representation_dimension,
            "is_self_dual": self.is_self_dual,
            "functorial_target_group": self.functorial_target_group,
        }


@dataclass
class LPoleSpectralFilter:
    """Spectral filter detecting pole residues at s = 1 of L(s, pi, r)."""
    representation_pi_label: str
    spectral_parameter: float
    central_l_value: float
    pole_residue_at_s1: float
    is_functorial_image: bool
    multiplicity_weight: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "representation_pi_label": self.representation_pi_label,
            "spectral_parameter": self.spectral_parameter,
            "central_l_value": self.central_l_value,
            "pole_residue_at_s1": self.pole_residue_at_s1,
            "is_functorial_image": self.is_functorial_image,
            "multiplicity_weight": self.multiplicity_weight,
        }


@dataclass
class PoissonGeometricSum:
    """Poisson summation harmonic component on geometric orbital integrals."""
    harmonic_index: int
    frequency_variable_xi: float
    orbital_fourier_transform: float
    destructive_phase_cancellation: float
    is_trivial_orbit: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "harmonic_index": self.harmonic_index,
            "frequency_variable_xi": self.frequency_variable_xi,
            "orbital_fourier_transform": self.orbital_fourier_transform,
            "destructive_phase_cancellation": self.destructive_phase_cancellation,
            "is_trivial_orbit": self.is_trivial_orbit,
        }


@dataclass
class AltugSmoothedKernel:
    """Altug regularized unipotent kernel smoothing parameterization."""
    smoothing_parameter_epsilon: float
    unipotent_subtraction_value: float
    regularized_orbital_integral: float
    asymptotic_convergence_order: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "smoothing_parameter_epsilon": self.smoothing_parameter_epsilon,
            "unipotent_subtraction_value": self.unipotent_subtraction_value,
            "regularized_orbital_integral": self.regularized_orbital_integral,
            "asymptotic_convergence_order": self.asymptotic_convergence_order,
        }


@dataclass
class BeyondEndoscopyEvaluation:
    """Evaluation of Beyond Endoscopy trace formula and functorial extraction."""
    poisson_geometric_total: float
    spectral_pole_residue_total: float
    trace_matching_residual: float
    functorial_lift_isolated: bool
    cancellation_efficiency_ratio: float
    cognitive_resonance_score: float
    spatial_stability_index: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "poisson_geometric_total": self.poisson_geometric_total,
            "spectral_pole_residue_total": self.spectral_pole_residue_total,
            "trace_matching_residual": self.trace_matching_residual,
            "functorial_lift_isolated": self.functorial_lift_isolated,
            "cancellation_efficiency_ratio": self.cancellation_efficiency_ratio,
            "cognitive_resonance_score": self.cognitive_resonance_score,
            "spatial_stability_index": self.spatial_stability_index,
        }


class BeyondEndoscopyLoom:
    r"""
    Autonomous Cognitive Spatial Beyond Endoscopy & Langlands Functoriality Loom.
    Models Langlands' program to extract functorial transfers from automorphic trace formulas
    via Poisson summation, unipotent smoothing, and L-function pole residue isolation.
    """

    def __init__(
        self,
        test_energy_parameter: float = 1.0,
        smoothing_epsilon: float = 0.05,
        default_archetype: str = BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value,
    ):
        self.test_energy_parameter = test_energy_parameter
        self.smoothing_epsilon = max(1e-4, smoothing_epsilon)
        self.archetype_str = default_archetype

        self.dual_rep: Optional[DualRepresentationData] = None
        self.spectral_filters: List[LPoleSpectralFilter] = []
        self.poisson_harmonics: List[PoissonGeometricSum] = []
        self.altug_kernel: Optional[AltugSmoothedKernel] = None

        self._initialize_loom()

    def _initialize_loom(self) -> None:
        """Initialize mathematical configuration based on archetype."""
        e = self.test_energy_parameter
        eps = self.smoothing_epsilon

        if self.archetype_str == BeyondEndoscopyArchetype.GL2_TIMES_GL2_RANKIN.value:
            self._init_gl2_x_gl2(e, eps)
        elif self.archetype_str == BeyondEndoscopyArchetype.GL3_ADJOINT_OCTET.value:
            self._init_gl3_adjoint(e, eps)
        elif self.archetype_str == BeyondEndoscopyArchetype.ALTUG_POISSON_GL2.value:
            self._init_altug_gl2(e, eps)
        else:
            self._init_gl2_sym2(e, eps)

    def _init_gl2_sym2(self, e: float, eps: float) -> None:
        """GL(2) with r = Sym^2 functorial lift to GL(3)."""
        self.dual_rep = DualRepresentationData(
            dual_group_label="^L G = GL(2, C)",
            representation_r_label="r = Sym^2 (Symmetric square representation)",
            representation_dimension=3,
            is_self_dual=True,
            functorial_target_group="GL(3) over F",
        )

        self.spectral_filters = [
            LPoleSpectralFilter(
                representation_pi_label="pi_triv = Trivial representation 1_GL2",
                spectral_parameter=0.0,
                central_l_value=round(2.150 * math.exp(-0.1 * e), 5),
                pole_residue_at_s1=1.0,
                is_functorial_image=True,
                multiplicity_weight=1.0,
            ),
            LPoleSpectralFilter(
                representation_pi_label="pi_dih = Monomial/Dihedral representation",
                spectral_parameter=0.75,
                central_l_value=round(1.680 * math.exp(-0.15 * e), 5),
                pole_residue_at_s1=round(0.725 * math.exp(-0.12 * e), 5),
                is_functorial_image=True,
                multiplicity_weight=round(0.725 * math.exp(-0.12 * e), 5),
            ),
            LPoleSpectralFilter(
                representation_pi_label="pi_gen = Non-dihedral cuspidal form",
                spectral_parameter=1.85,
                central_l_value=round(1.120 * math.exp(-0.2 * e), 5),
                pole_residue_at_s1=0.0,
                is_functorial_image=False,
                multiplicity_weight=0.0,
            ),
        ]

        self.poisson_harmonics = [
            PoissonGeometricSum(
                harmonic_index=0,
                frequency_variable_xi=0.0,
                orbital_fourier_transform=round(1.725 * math.exp(-0.1 * e), 5),
                destructive_phase_cancellation=1.0,
                is_trivial_orbit=True,
            ),
            PoissonGeometricSum(
                harmonic_index=1,
                frequency_variable_xi=1.0,
                orbital_fourier_transform=round(0.420 * math.exp(-0.25 * e), 5),
                destructive_phase_cancellation=0.08,
                is_trivial_orbit=False,
            ),
            PoissonGeometricSum(
                harmonic_index=2,
                frequency_variable_xi=2.0,
                orbital_fourier_transform=round(0.180 * math.exp(-0.35 * e), 5),
                destructive_phase_cancellation=0.03,
                is_trivial_orbit=False,
            ),
        ]

        unip_val = round(0.450 / (1.0 + 10.0 * eps), 5)
        reg_val = round(1.725 * math.exp(-0.1 * e) - unip_val, 5)
        self.altug_kernel = AltugSmoothedKernel(
            smoothing_parameter_epsilon=eps,
            unipotent_subtraction_value=unip_val,
            regularized_orbital_integral=reg_val,
            asymptotic_convergence_order=2.0,
        )

    def _init_gl2_x_gl2(self, e: float, eps: float) -> None:
        """GL(2) x GL(2) with r = tensor Rankin-Selberg lift to GL(4)."""
        self.dual_rep = DualRepresentationData(
            dual_group_label="^L G = GL(2, C) x GL(2, C)",
            representation_r_label="r = tensor (Exterior tensor product)",
            representation_dimension=4,
            is_self_dual=True,
            functorial_target_group="GL(4) over F",
        )

        self.spectral_filters = [
            LPoleSpectralFilter(
                representation_pi_label="pi_1 x pi_1^v = Diagonal identical pair",
                spectral_parameter=0.5,
                central_l_value=round(2.450 * math.exp(-0.1 * e), 5),
                pole_residue_at_s1=1.0,
                is_functorial_image=True,
                multiplicity_weight=1.0,
            ),
            LPoleSpectralFilter(
                representation_pi_label="pi_1 x (pi_1 tensor chi) = Twist isomorphic pair",
                spectral_parameter=1.1,
                central_l_value=round(1.550 * math.exp(-0.16 * e), 5),
                pole_residue_at_s1=round(0.650 * math.exp(-0.14 * e), 5),
                is_functorial_image=True,
                multiplicity_weight=round(0.650 * math.exp(-0.14 * e), 5),
            ),
            LPoleSpectralFilter(
                representation_pi_label="pi_1 x pi_2 = Disjoint cuspidal representations",
                spectral_parameter=2.1,
                central_l_value=round(0.920 * math.exp(-0.22 * e), 5),
                pole_residue_at_s1=0.0,
                is_functorial_image=False,
                multiplicity_weight=0.0,
            ),
        ]

        self.poisson_harmonics = [
            PoissonGeometricSum(
                harmonic_index=0,
                frequency_variable_xi=0.0,
                orbital_fourier_transform=round(1.650 * math.exp(-0.12 * e), 5),
                destructive_phase_cancellation=1.0,
                is_trivial_orbit=True,
            ),
            PoissonGeometricSum(
                harmonic_index=1,
                frequency_variable_xi=1.0,
                orbital_fourier_transform=round(0.380 * math.exp(-0.26 * e), 5),
                destructive_phase_cancellation=0.06,
                is_trivial_orbit=False,
            ),
            PoissonGeometricSum(
                harmonic_index=2,
                frequency_variable_xi=2.0,
                orbital_fourier_transform=round(0.140 * math.exp(-0.38 * e), 5),
                destructive_phase_cancellation=0.02,
                is_trivial_orbit=False,
            ),
        ]

        unip_val = round(0.520 / (1.0 + 8.0 * eps), 5)
        reg_val = round(1.650 * math.exp(-0.12 * e) - unip_val, 5)
        self.altug_kernel = AltugSmoothedKernel(
            smoothing_parameter_epsilon=eps,
            unipotent_subtraction_value=unip_val,
            regularized_orbital_integral=reg_val,
            asymptotic_convergence_order=2.0,
        )

    def _init_gl3_adjoint(self, e: float, eps: float) -> None:
        """GL(3) with r = Adjoint representation in GL(8)."""
        self.dual_rep = DualRepresentationData(
            dual_group_label="^L G = PGL(3, C)",
            representation_r_label="r = Ad (Adjoint 8-dimensional representation)",
            representation_dimension=8,
            is_self_dual=True,
            functorial_target_group="GL(8) over F",
        )

        self.spectral_filters = [
            LPoleSpectralFilter(
                representation_pi_label="pi_selfdual = Self-dual cuspidal GL(3) representation",
                spectral_parameter=1.0,
                central_l_value=round(2.820 * math.exp(-0.1 * e), 5),
                pole_residue_at_s1=round(0.920 * math.exp(-0.1 * e), 5),
                is_functorial_image=True,
                multiplicity_weight=round(0.920 * math.exp(-0.1 * e), 5),
            ),
            LPoleSpectralFilter(
                representation_pi_label="pi_generic = Non-self-dual generic representation",
                spectral_parameter=2.4,
                central_l_value=round(1.050 * math.exp(-0.25 * e), 5),
                pole_residue_at_s1=0.0,
                is_functorial_image=False,
                multiplicity_weight=0.0,
            ),
        ]

        self.poisson_harmonics = [
            PoissonGeometricSum(
                harmonic_index=0,
                frequency_variable_xi=0.0,
                orbital_fourier_transform=round(1.920 * math.exp(-0.11 * e), 5),
                destructive_phase_cancellation=1.0,
                is_trivial_orbit=True,
            ),
            PoissonGeometricSum(
                harmonic_index=1,
                frequency_variable_xi=1.0,
                orbital_fourier_transform=round(0.480 * math.exp(-0.22 * e), 5),
                destructive_phase_cancellation=0.05,
                is_trivial_orbit=False,
            ),
        ]

        unip_val = round(0.680 / (1.0 + 12.0 * eps), 5)
        reg_val = round(1.920 * math.exp(-0.11 * e) - unip_val, 5)
        self.altug_kernel = AltugSmoothedKernel(
            smoothing_parameter_epsilon=eps,
            unipotent_subtraction_value=unip_val,
            regularized_orbital_integral=reg_val,
            asymptotic_convergence_order=2.5,
        )

    def _init_altug_gl2(self, e: float, eps: float) -> None:
        """GL(2) Altug Poisson Summation and unipotent subtraction."""
        self.dual_rep = DualRepresentationData(
            dual_group_label="^L G = GL(2, C)",
            representation_r_label="r = Standard fundamental representation",
            representation_dimension=2,
            is_self_dual=False,
            functorial_target_group="GL(2) over F",
        )

        self.spectral_filters = [
            LPoleSpectralFilter(
                representation_pi_label="pi_cusp = Cuspidal automorphic representation",
                spectral_parameter=1.5,
                central_l_value=round(1.850 * math.exp(-0.12 * e), 5),
                pole_residue_at_s1=round(0.850 * math.exp(-0.1 * e), 5),
                is_functorial_image=True,
                multiplicity_weight=round(0.850 * math.exp(-0.1 * e), 5),
            ),
        ]

        self.poisson_harmonics = [
            PoissonGeometricSum(
                harmonic_index=0,
                frequency_variable_xi=0.0,
                orbital_fourier_transform=round(1.580 * math.exp(-0.1 * e), 5),
                destructive_phase_cancellation=1.0,
                is_trivial_orbit=True,
            ),
            PoissonGeometricSum(
                harmonic_index=1,
                frequency_variable_xi=1.0,
                orbital_fourier_transform=round(0.320 * math.exp(-0.28 * e), 5),
                destructive_phase_cancellation=0.04,
                is_trivial_orbit=False,
            ),
        ]

        unip_val = round(0.410 / (1.0 + 15.0 * eps), 5)
        reg_val = round(1.580 * math.exp(-0.1 * e) - unip_val, 5)
        self.altug_kernel = AltugSmoothedKernel(
            smoothing_parameter_epsilon=eps,
            unipotent_subtraction_value=unip_val,
            regularized_orbital_integral=reg_val,
            asymptotic_convergence_order=3.0,
        )

    def evaluate_beyond_endoscopy(self) -> BeyondEndoscopyEvaluation:
        """Evaluate Beyond Endoscopy trace identity and functorial extraction."""
        # Geometric side: Altug regularized zero-mode plus destructive phase sums
        geom_zero = self.altug_kernel.regularized_orbital_integral if self.altug_kernel else 1.0
        geom_fluctuations = sum(
            h.orbital_fourier_transform * h.destructive_phase_cancellation
            for h in self.poisson_harmonics
            if not h.is_trivial_orbit
        )
        geom_total = geom_zero + geom_fluctuations

        # Spectral side: sum of pole residues Res_{s=1} L(s, pi, r)
        spec_total = sum(f.multiplicity_weight for f in self.spectral_filters)

        residual = abs(geom_total - spec_total)
        functorial_isolated = spec_total > 0.0

        # Cancellation efficiency of non-functorial oscillatory orbits
        non_trivial_transforms = [h.orbital_fourier_transform for h in self.poisson_harmonics if not h.is_trivial_orbit]
        if non_trivial_transforms:
            cancellation_ratio = 1.0 - (geom_fluctuations / (sum(non_trivial_transforms) + 1e-6))
        else:
            cancellation_ratio = 1.0
        cancellation_ratio = max(0.0, min(1.0, cancellation_ratio))

        # Cognitive spatial metrics
        resonance = max(0.0, min(1.0, 1.0 - (residual / (geom_total + 1e-6))))
        stability = 0.95 if functorial_isolated else 0.70

        return BeyondEndoscopyEvaluation(
            poisson_geometric_total=round(geom_total, 5),
            spectral_pole_residue_total=round(spec_total, 5),
            trace_matching_residual=round(residual, 5),
            functorial_lift_isolated=functorial_isolated,
            cancellation_efficiency_ratio=round(cancellation_ratio, 4),
            cognitive_resonance_score=round(resonance, 4),
            spatial_stability_index=round(stability, 4),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize loom state into structured dictionary."""
        eval_data = self.evaluate_beyond_endoscopy()
        return {
            "archetype": self.archetype_str,
            "test_energy_parameter": self.test_energy_parameter,
            "smoothing_epsilon": self.smoothing_epsilon,
            "dual_representation": self.dual_rep.to_dict() if self.dual_rep else None,
            "spectral_filters": [s.to_dict() for s in self.spectral_filters],
            "poisson_harmonics": [h.to_dict() for h in self.poisson_harmonics],
            "altug_kernel": self.altug_kernel.to_dict() if self.altug_kernel else None,
            "evaluation": eval_data.to_dict(),
        }

    def generate_svg(self) -> str:
        """
        Generate publication-grade dark titanium SVG diagram of Beyond Endoscopy,
        Poisson summation, and functorial L-pole extraction with strictly zero em dashes.
        """
        eval_data = self.evaluate_beyond_endoscopy()
        width = 1040
        height = 680

        bg_dark = "#0b0f19"
        card_bg = "#111827"
        card_border = "#1f2937"
        accent_blue = "#38bdf8"
        accent_indigo = "#818cf8"
        accent_emerald = "#34d399"
        accent_amber = "#fbbf24"
        accent_rose = "#f472b6"
        text_light = "#f3f4f6"
        text_muted = "#9ca3af"

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">',
            f'  <rect width="{width}" height="{height}" fill="{bg_dark}" rx="16"/>',
            '  <defs>',
            '    <linearGradient id="grad_blue_be" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="0.2"/>',
            f'      <stop offset="100%" stop-color="{accent_indigo}" stop-opacity="0.05"/>',
            '    </linearGradient>',
            '  </defs>',
            '',
            '  <!-- Header Banner -->',
            f'  <rect x="24" y="24" width="{width - 48}" height="76" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="48" y="58" fill="{accent_blue}" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="700">',
            '    Beyond Endoscopy &amp; Langlands Functoriality Loom',
            '  </text>',
            f'  <text x="48" y="82" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="13">',
            f'    Archetype: {self.archetype_str[:55]} | Cancellation: {eval_data.cancellation_efficiency_ratio * 100:.1f}% | Residual: {eval_data.trace_matching_residual}',
            '  </text>',
            '',
            '  <!-- Left Column: Poisson Geometric Sum & Destructive Phase Cancellation -->',
            f'  <rect x="24" y="116" width="315" height="340" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="44" y="146" fill="{accent_amber}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Poisson Summation on Geometric Side',
            '  </text>',
            f'  <text x="44" y="166" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="12">',
            f'    Regularized Poisson Sum: {eval_data.poisson_geometric_total}',
            '  </text>',
        ]

        y_h = 190
        for harm in self.poisson_harmonics:
            badge = accent_emerald if harm.is_trivial_orbit else accent_indigo
            tag = "Zero Mode" if harm.is_trivial_orbit else "Oscillatory"
            svg_parts.extend([
                f'  <g transform="translate(40, {y_h})">',
                f'    <rect width="283" height="66" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
                f'    <circle cx="14" cy="24" r="6" fill="{badge}"/>',
                f'    <text x="28" y="20" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">Harmonic #{harm.harmonic_index} (xi = {harm.frequency_variable_xi})</text>',
                f'    <text x="28" y="38" fill="{text_muted}" font-family="monospace" font-size="11">Fourier Transform: {harm.orbital_fourier_transform}</text>',
                f'    <text x="28" y="56" fill="{accent_amber}" font-family="monospace" font-size="11">Phase Weight = {harm.destructive_phase_cancellation} ({tag})</text>',
                '  </g>',
            ])
            y_h += 78

        # Center Column: Altug Unipotent Smoother & Dual Representation r
        svg_parts.extend([
            f'  <rect x="355" y="116" width="320" height="340" rx="12" fill="url(#grad_blue_be)" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="375" y="146" fill="{accent_blue}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Dual Rep ^L G &amp; Altug Smoothing',
            '  </text>',
            f'  <text x="375" y="166" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="12">',
            '    Boundary subtraction and unipotent regularization',
            '  </text>',
        ])

        if self.dual_rep and self.altug_kernel:
            dr = self.dual_rep
            ak = self.altug_kernel
            svg_parts.extend([
                f'  <g transform="translate(371, 190)">',
                f'    <rect width="288" height="150" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>',
                f'    <text x="14" y="26" fill="{accent_emerald}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{dr.dual_group_label}</text>',
                f'    <text x="14" y="46" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="11">{dr.representation_r_label}</text>',
                f'    <text x="14" y="68" fill="{text_muted}" font-family="monospace" font-size="11">dim(r) = {dr.representation_dimension} | Self-Dual: {dr.is_self_dual}</text>',
                f'    <text x="14" y="88" fill="{accent_blue}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Target: {dr.functorial_target_group}</text>',
                f'    <text x="14" y="112" fill="{text_light}" font-family="monospace" font-size="11">Unipotent Subtraction: {ak.unipotent_subtraction_value}</text>',
                f'    <text x="14" y="132" fill="{accent_amber}" font-family="monospace" font-size="11">Regularized Integral: {ak.regularized_orbital_integral}</text>',
                '  </g>',
            ])

        # Indicator badge
        iso_text = "Functorial Image Isolated" if eval_data.functorial_lift_isolated else "Dispersion Threshold"
        iso_bg = accent_emerald if eval_data.functorial_lift_isolated else accent_amber
        svg_parts.extend([
            f'  <g transform="translate(371, 360)">',
            f'    <rect width="288" height="76" rx="8" fill="{card_border}" fill-opacity="0.6"/>',
            f'    <circle cx="20" cy="28" r="7" fill="{iso_bg}"/>',
            f'    <text x="38" y="26" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{iso_text}</text>',
            f'    <text x="38" y="44" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Cancellation Efficiency = {eval_data.cancellation_efficiency_ratio * 100:.1f}%</text>',
            f'    <text x="38" y="62" fill="{accent_emerald}" font-family="monospace" font-size="11">Spatial Stability = {eval_data.spatial_stability_index}</text>',
            '  </g>',
        ])

        # Right Column: Spectral L-Pole Residue Filter Res_{s=1} L(s, pi, r)
        svg_parts.extend([
            f'  <rect x="691" y="116" width="325" height="340" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="711" y="146" fill="{accent_emerald}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Spectral Side: L-Pole Filter',
            '  </text>',
            f'  <text x="711" y="166" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="12">',
            f'    Sum of Residues at s=1: {eval_data.spectral_pole_residue_total}',
            '  </text>',
        ])

        y_sp = 190
        for flt in self.spectral_filters:
            sp_color = accent_emerald if flt.is_functorial_image else accent_rose
            tag = "Functorial Pole" if flt.is_functorial_image else "No Pole at s=1"
            svg_parts.extend([
                f'  <g transform="translate(707, {y_sp})">',
                f'    <rect width="293" height="66" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
                f'    <circle cx="16" cy="24" r="6" fill="{sp_color}"/>',
                f'    <text x="30" y="20" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{flt.representation_pi_label[:28]}</text>',
                f'    <text x="14" y="38" fill="{text_muted}" font-family="monospace" font-size="11">L(1/2) = {flt.central_l_value} | lambda = {flt.spectral_parameter}</text>',
                f'    <text x="14" y="56" fill="{accent_amber}" font-family="monospace" font-size="11">Res_{{s=1}} = {flt.pole_residue_at_s1} ({tag})</text>',
                '  </g>',
            ])
            y_sp += 78

        # Bottom Row: Summary & Cognitive Spatial Access Bar
        svg_parts.extend([
            f'  <rect x="24" y="472" width="{width - 48}" height="184" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="48" y="504" fill="{accent_rose}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Cognitive Spatial Scaffolding: Beyond Endoscopy Poisson Harmonic Loom',
            '  </text>',
            f'  <text x="48" y="528" fill="{text_muted}" font-family="monospace" font-size="12">',
            f'    Residual: |I_Poisson - I_Poles| = {eval_data.trace_matching_residual} | Resonance: {eval_data.cognitive_resonance_score} | Target: {self.dual_rep.functorial_target_group if self.dual_rep else "GL(N)"}',
            '  </text>',
            '  <g transform="translate(48, 546)">',
            f'    <rect width="280" height="90" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
            f'    <text x="14" y="24" fill="{accent_blue}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">Poisson Frequency Transform</text>',
            f'    <text x="14" y="46" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Converts orbital sums to harmonics</text>',
            f'    <text x="14" y="66" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Cancels non-functorial noise</text>',
            '  </g>',
            '  <g transform="translate(352, 546)">',
            f'    <rect width="280" height="90" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
            f'    <text x="14" y="24" fill="{accent_emerald}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">L-Pole Residue Isolation</text>',
            f'    <text x="14" y="46" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Directly detects transferred forms</text>',
            f'    <text x="14" y="66" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">No intermediate endoscopic group</text>',
            '  </g>',
            '  <g transform="translate(656, 546)">',
            f'    <rect width="336" height="90" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
            f'    <text x="14" y="24" fill="{accent_amber}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">Unipotent Regularizer</text>',
            f'    <text x="14" y="46" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Altug unipotent subtraction kernel</text>',
            f'    <text x="14" y="66" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Stabilizes visual working memory</text>',
            '  </g>',
            '</svg>',
        ])
        return "\n".join(svg_parts)


def run_demo(group_name: Optional[str] = None) -> Dict[str, Any]:
    """Execute Beyond Endoscopy Loom demo."""
    archetype = BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value
    if group_name:
        for arch in BeyondEndoscopyArchetype:
            if group_name.lower() in arch.value.lower():
                archetype = arch.value
                break

    loom = BeyondEndoscopyLoom(
        test_energy_parameter=1.0,
        smoothing_epsilon=0.05,
        default_archetype=archetype,
    )
    return loom.to_dict()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Beyond Endoscopy & Langlands Functoriality Loom")
    parser.add_argument("--demo", action="store_true", help="Run demonstrator")
    parser.add_argument("--archetype", default="sym2", choices=["sym2", "rankin", "adjoint", "altug"], help="Beyond Endoscopy archetype")
    parser.add_argument("--energy", type=float, default=1.0, help="Test energy parameter")
    parser.add_argument("--epsilon", type=float, default=0.05, help="Smoothing parameter epsilon")
    parser.add_argument("--json", action="store_true", help="Output JSON structure")
    parser.add_argument("--svg", type=str, help="Save SVG visualization to destination path")

    args = parser.parse_args()

    arch_map = {
        "sym2": BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value,
        "rankin": BeyondEndoscopyArchetype.GL2_TIMES_GL2_RANKIN.value,
        "adjoint": BeyondEndoscopyArchetype.GL3_ADJOINT_OCTET.value,
        "altug": BeyondEndoscopyArchetype.ALTUG_POISSON_GL2.value,
    }
    chosen_arch = arch_map.get(args.archetype, BeyondEndoscopyArchetype.GL2_SYMMETRIC_SQUARE.value)

    loom = BeyondEndoscopyLoom(
        test_energy_parameter=args.energy,
        smoothing_epsilon=args.epsilon,
        default_archetype=chosen_arch,
    )

    if args.svg:
        svg_content = loom.generate_svg()
        with open(args.svg, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"SVG saved to {args.svg}")

    if args.json or args.demo:
        print(json.dumps(loom.to_dict(), indent=2))
    else:
        ev = loom.evaluate_beyond_endoscopy()
        print("================================================================================")
        print("  Beyond Endoscopy & Langlands Functoriality Loom")
        print("================================================================================")
        print(f"Archetype:                     {loom.archetype_str}")
        print(f"Poisson Geometric Total:       {ev.poisson_geometric_total}")
        print(f"Spectral Pole Residue Total:   {ev.spectral_pole_residue_total}")
        print(f"Trace Matching Residual:       {ev.trace_matching_residual}")
        print(f"Functorial Lift Isolated:      {ev.functorial_lift_isolated}")
        print(f"Cancellation Efficiency:       {ev.cancellation_efficiency_ratio * 100:.2f}%")
        print(f"Cognitive Resonance Score:     {ev.cognitive_resonance_score}")
        print(f"Spatial Stability Index:       {ev.spatial_stability_index}")
        print("================================================================================")
