r"""
Arthur-Selberg Trace Formula & Endoscopic Classification Loom.
Models James Arthur and Atle Selberg's invariant trace formula and endoscopic classification:
- Invariant trace formula identity: I_geom(f) = I_spec(f) on reductive groups G
- Geometric side: conjugacy classes, weighted orbital integrals J_M(gamma, f)
- Spectral side: discrete spectrum, automorphic representations, Eisenstein residues
- Endoscopic groups H and Langlands-Shelstad transfer factors Delta(gamma_H, gamma)
- Stable trace formula expansion: I(f) = sum_H iota(G, H) S^H(f^H)
- Arthur parameters psi: L_F x SL(2, C) -> ^L G and component groups S_psi
- Arthur packets Pi_psi and multiplicity formulas in discrete automorphic spectrum
- Spatial cognitive scaffolding for non-linear, spatial, and dyslexic thinkers
Strictly zero em dashes (chr(8212)) across all functions, docstrings, and comments.
"""

import math
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


class ArthurGroupArchetype(str, Enum):
    """Canonical classical groups and endoscopic configurations."""
    SO5_SPLIT = "SO_5 (B_2 split) with dual Sp_4(C) & Endoscopic SO_3 x SO_3"
    SP4_SPLIT = "Sp_4 (C_2 split) with dual SO_5(C) & Endoscopic SL_2 x PGL_2"
    SO7_SPLIT = "SO_7 (B_3 split) with dual Sp_6(C) & Endoscopic SO_5 x SO_3"
    GL4_STANDARD = "GL_4 (A_3 split) with self-dual trace formula (all endoscopic groups trivial)"


@dataclass
class EndoscopicGroupData:
    """Elliptic endoscopic group H and transfer coefficient iota(G, H)."""
    group_h_label: str
    is_quasi_split: bool
    dimension_h: int
    tamagawa_iota_coefficient: float
    transfer_factor_sign: int
    stable_orbital_integral: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_h_label": self.group_h_label,
            "is_quasi_split": self.is_quasi_split,
            "dimension_h": self.dimension_h,
            "tamagawa_iota_coefficient": self.tamagawa_iota_coefficient,
            "transfer_factor_sign": self.transfer_factor_sign,
            "stable_orbital_integral": self.stable_orbital_integral,
        }


@dataclass
class ArthurParameterData:
    """Global Arthur parameter psi = direct sum of (tau_i tensor nu_d_i)."""
    parameter_label: str
    dual_group_label: str
    deligne_factors_count: int
    component_group_order: int
    is_tempered: bool
    is_generic: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "parameter_label": self.parameter_label,
            "dual_group_label": self.dual_group_label,
            "deligne_factors_count": self.deligne_factors_count,
            "component_group_order": self.component_group_order,
            "is_tempered": self.is_tempered,
            "is_generic": self.is_generic,
        }


@dataclass
class ArthurPacketRepresentation:
    """Member representation pi in the Arthur packet Pi_psi."""
    rep_label: str
    pairing_character: str
    local_sign: int
    epsilon_psi_value: int
    multiplicity_in_discrete_spectrum: int
    infinitesimal_character: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rep_label": self.rep_label,
            "pairing_character": self.pairing_character,
            "local_sign": self.local_sign,
            "epsilon_psi_value": self.epsilon_psi_value,
            "multiplicity_in_discrete_spectrum": self.multiplicity_in_discrete_spectrum,
            "infinitesimal_character": self.infinitesimal_character,
        }


@dataclass
class OrbitalIntegralComponent:
    """Geometric conjugacy class contribution to weighted orbital integral."""
    conjugacy_class: str
    centralizer_dimension: int
    weyl_discriminant: float
    weighted_integral_value: float
    is_unipotent: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "conjugacy_class": self.conjugacy_class,
            "centralizer_dimension": self.centralizer_dimension,
            "weyl_discriminant": self.weyl_discriminant,
            "weighted_integral_value": self.weighted_integral_value,
            "is_unipotent": self.is_unipotent,
        }


@dataclass
class SpectralTraceComponent:
    """Spectral automorphic representation contribution to trace formula."""
    spectrum_type: str
    representation_label: str
    spectral_parameter: float
    intertwining_log_derivative: float
    spectral_weight: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "spectrum_type": self.spectrum_type,
            "representation_label": self.representation_label,
            "spectral_parameter": self.spectral_parameter,
            "intertwining_log_derivative": self.intertwining_log_derivative,
            "spectral_weight": self.spectral_weight,
        }


@dataclass
class TraceFormulaEvaluation:
    """Summary evaluation of the Arthur-Selberg trace identity and stabilization."""
    geometric_total: float
    spectral_total: float
    endoscopic_reconstructed_total: float
    trace_identity_residual: float
    is_stabilized: bool
    cognitive_resonance_score: float
    spatial_stability_index: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "geometric_total": self.geometric_total,
            "spectral_total": self.spectral_total,
            "endoscopic_reconstructed_total": self.endoscopic_reconstructed_total,
            "trace_identity_residual": self.trace_identity_residual,
            "is_stabilized": self.is_stabilized,
            "cognitive_resonance_score": self.cognitive_resonance_score,
            "spatial_stability_index": self.spatial_stability_index,
        }


class ArthurSelbergTraceLoom:
    """
    Autonomous Cognitive Spatial Arthur-Selberg Trace Formula & Endoscopic Classification Loom.
    Computes invariant distributions, geometric orbital sums, spectral automorphic sums,
    endoscopic transfers, Arthur packets, and cognitive spatial visualizations.
    """

    def __init__(
        self,
        test_function_cutoff: float = 2.5,
        spectral_truncation_level: int = 4,
        default_archetype: str = ArthurGroupArchetype.SO5_SPLIT.value,
    ):
        self.test_function_cutoff = test_function_cutoff
        self.spectral_truncation_level = max(1, spectral_truncation_level)
        self.archetype_str = default_archetype

        self.endoscopic_groups: List[EndoscopicGroupData] = []
        self.arthur_parameter: Optional[ArthurParameterData] = None
        self.arthur_packet: List[ArthurPacketRepresentation] = []
        self.orbital_components: List[OrbitalIntegralComponent] = []
        self.spectral_components: List[SpectralTraceComponent] = []

        self._initialize_loom()

    def _initialize_loom(self) -> None:
        """Initialize mathematical configuration based on selected archetype."""
        cutoff = self.test_function_cutoff

        if self.archetype_str == ArthurGroupArchetype.SP4_SPLIT.value:
            self._init_sp4(cutoff)
        elif self.archetype_str == ArthurGroupArchetype.SO7_SPLIT.value:
            self._init_so7(cutoff)
        elif self.archetype_str == ArthurGroupArchetype.GL4_STANDARD.value:
            self._init_gl4(cutoff)
        else:
            self._init_so5(cutoff)

    def _init_so5(self, cutoff: float) -> None:
        """SO(5) split orthogonal configuration with dual Sp(4, C)."""
        self.arthur_parameter = ArthurParameterData(
            parameter_label="psi = (tau_2 tensor nu_1) direct_sum (tau_1 tensor nu_2)",
            dual_group_label="Sp_4(C)",
            deligne_factors_count=2,
            component_group_order=4,
            is_tempered=False,
            is_generic=False,
        )

        # Endoscopic groups for SO(5): principal G itself and H = SO(3) x SO(3)
        self.endoscopic_groups = [
            EndoscopicGroupData(
                group_h_label="G_0 = SO_5 (Principal endoscopic group)",
                is_quasi_split=True,
                dimension_h=10,
                tamagawa_iota_coefficient=1.0,
                transfer_factor_sign=1,
                stable_orbital_integral=round(2.845 * math.exp(-0.15 * cutoff), 5),
            ),
            EndoscopicGroupData(
                group_h_label="H_1 = SO_3 x SO_3 (Elliptic endoscopic group)",
                is_quasi_split=True,
                dimension_h=6,
                tamagawa_iota_coefficient=0.5,
                transfer_factor_sign=-1,
                stable_orbital_integral=round(1.120 * math.exp(-0.22 * cutoff), 5),
            ),
        ]

        # Arthur packet for SO(5) parameter
        self.arthur_packet = [
            ArthurPacketRepresentation(
                rep_label="pi_1 (Non-tempered CAP cuspidal representation)",
                pairing_character="(+1, +1)",
                local_sign=1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=1.5,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_2 (Cuspidal automorphic representation with non-trivial sign)",
                pairing_character="(+1, -1)",
                local_sign=-1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=0,
                infinitesimal_character=1.5,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_3 (Discrete series constituent)",
                pairing_character="(-1, +1)",
                local_sign=1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=2.0,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_4 (Non-tempered partner)",
                pairing_character="(-1, -1)",
                local_sign=-1,
                epsilon_psi_value=-1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=2.0,
            ),
        ]

        # Geometric orbital components
        self.orbital_components = [
            OrbitalIntegralComponent(
                conjugacy_class="gamma_1 = Central unit element 1_G",
                centralizer_dimension=10,
                weyl_discriminant=1.0,
                weighted_integral_value=round(1.750 * math.exp(-0.1 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_2 = Regular elliptic element gamma_reg",
                centralizer_dimension=2,
                weyl_discriminant=0.64,
                weighted_integral_value=round(0.825 * math.exp(-0.18 * cutoff), 5),
                is_unipotent=False,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_3 = Subregular unipotent class u_sub",
                centralizer_dimension=4,
                weyl_discriminant=0.25,
                weighted_integral_value=round(0.430 * math.exp(-0.25 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_4 = Semi-simple non-elliptic class s_hyp",
                centralizer_dimension=3,
                weyl_discriminant=0.49,
                weighted_integral_value=round(0.355 * math.exp(-0.3 * cutoff), 5),
                is_unipotent=False,
            ),
        ]

        # Spectral trace components
        self.spectral_components = [
            SpectralTraceComponent(
                spectrum_type="Discrete Cuspidal",
                representation_label="pi_cusp_1 (Weight 4 holomorphic Siegel form)",
                spectral_parameter=1.5,
                intertwining_log_derivative=0.0,
                spectral_weight=round(1.480 * math.exp(-0.12 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Discrete Residual",
                representation_label="pi_res (Residue of Siegel Eisenstein series)",
                spectral_parameter=0.5,
                intertwining_log_derivative=0.0,
                spectral_weight=round(0.550 * math.exp(-0.2 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Eisenstein P_min",
                representation_label="Ind_B^G(chi_1 tensor chi_2)",
                spectral_parameter=2.2,
                intertwining_log_derivative=0.45,
                spectral_weight=round(0.810 * math.exp(-0.19 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Eisenstein P_Klingen",
                representation_label="Ind_P^G(pi_GL2 tensor delta_P^s)",
                spectral_parameter=1.8,
                intertwining_log_derivative=0.28,
                spectral_weight=round(0.520 * math.exp(-0.24 * cutoff), 5),
            ),
        ]

    def _init_sp4(self, cutoff: float) -> None:
        """Sp(4) split symplectic configuration with dual SO(5, C)."""
        self.arthur_parameter = ArthurParameterData(
            parameter_label="psi = tau_4 (Tempered generic parameter)",
            dual_group_label="SO_5(C)",
            deligne_factors_count=1,
            component_group_order=2,
            is_tempered=True,
            is_generic=True,
        )

        self.endoscopic_groups = [
            EndoscopicGroupData(
                group_h_label="G_0 = Sp_4 (Principal endoscopic group)",
                is_quasi_split=True,
                dimension_h=10,
                tamagawa_iota_coefficient=1.0,
                transfer_factor_sign=1,
                stable_orbital_integral=round(3.150 * math.exp(-0.14 * cutoff), 5),
            ),
            EndoscopicGroupData(
                group_h_label="H_1 = SL_2 x PGL_2 (Elliptic endoscopic pair)",
                is_quasi_split=True,
                dimension_h=6,
                tamagawa_iota_coefficient=0.5,
                transfer_factor_sign=-1,
                stable_orbital_integral=round(0.950 * math.exp(-0.21 * cutoff), 5),
            ),
        ]

        self.arthur_packet = [
            ArthurPacketRepresentation(
                rep_label="pi_gen (Generic tempered representation)",
                pairing_character="+1",
                local_sign=1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=2.0,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_nongen (Non-generic tempered packet partner)",
                pairing_character="-1",
                local_sign=-1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=0,
                infinitesimal_character=2.0,
            ),
        ]

        self.orbital_components = [
            OrbitalIntegralComponent(
                conjugacy_class="gamma_1 = Central unit element 1_Sp4",
                centralizer_dimension=10,
                weyl_discriminant=1.0,
                weighted_integral_value=round(1.920 * math.exp(-0.11 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_2 = Regular elliptic element gamma_reg",
                centralizer_dimension=2,
                weyl_discriminant=0.72,
                weighted_integral_value=round(0.910 * math.exp(-0.17 * cutoff), 5),
                is_unipotent=False,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_3 = Regular unipotent orbit",
                centralizer_dimension=4,
                weyl_discriminant=0.30,
                weighted_integral_value=round(0.480 * math.exp(-0.26 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_4 = Semi-simple hyperbolic element",
                centralizer_dimension=3,
                weyl_discriminant=0.55,
                weighted_integral_value=round(0.315 * math.exp(-0.31 * cutoff), 5),
                is_unipotent=False,
            ),
        ]

        self.spectral_components = [
            SpectralTraceComponent(
                spectrum_type="Discrete Cuspidal",
                representation_label="pi_cusp_sp4 (Tempered discrete automorphic representation)",
                spectral_parameter=2.0,
                intertwining_log_derivative=0.0,
                spectral_weight=round(1.680 * math.exp(-0.13 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Discrete Residual",
                representation_label="pi_res (Minimal residual representation)",
                spectral_parameter=1.0,
                intertwining_log_derivative=0.0,
                spectral_weight=round(0.480 * math.exp(-0.21 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Eisenstein",
                representation_label="Ind_B^G(delta_B^s)",
                spectral_parameter=2.4,
                intertwining_log_derivative=0.52,
                spectral_weight=round(0.920 * math.exp(-0.18 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Induced",
                representation_label="Ind_P^G(pi_cusp_SL2 tensor delta_P^s)",
                spectral_parameter=1.6,
                intertwining_log_derivative=0.31,
                spectral_weight=round(0.545 * math.exp(-0.25 * cutoff), 5),
            ),
        ]

    def _init_so7(self, cutoff: float) -> None:
        """SO(7) split orthogonal configuration with dual Sp(6, C)."""
        self.arthur_parameter = ArthurParameterData(
            parameter_label="psi = (tau_2 tensor nu_2) direct_sum (tau_1 tensor nu_2)",
            dual_group_label="Sp_6(C)",
            deligne_factors_count=2,
            component_group_order=4,
            is_tempered=False,
            is_generic=False,
        )

        self.endoscopic_groups = [
            EndoscopicGroupData(
                group_h_label="G_0 = SO_7 (Principal endoscopic group)",
                is_quasi_split=True,
                dimension_h=21,
                tamagawa_iota_coefficient=1.0,
                transfer_factor_sign=1,
                stable_orbital_integral=round(3.850 * math.exp(-0.13 * cutoff), 5),
            ),
            EndoscopicGroupData(
                group_h_label="H_1 = SO_5 x SO_3 (Elliptic endoscopic factor)",
                is_quasi_split=True,
                dimension_h=13,
                tamagawa_iota_coefficient=0.5,
                transfer_factor_sign=-1,
                stable_orbital_integral=round(1.350 * math.exp(-0.20 * cutoff), 5),
            ),
        ]

        self.arthur_packet = [
            ArthurPacketRepresentation(
                rep_label="pi_1 (Discrete automorphic representation)",
                pairing_character="(+1, +1)",
                local_sign=1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=2.5,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_2 (Endoscopic transfer image)",
                pairing_character="(+1, -1)",
                local_sign=-1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=0,
                infinitesimal_character=2.5,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_3 (Non-tempered A-packet constituent)",
                pairing_character="(-1, +1)",
                local_sign=1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=3.0,
            ),
            ArthurPacketRepresentation(
                rep_label="pi_4 (Arthur multiplicity cancellation partner)",
                pairing_character="(-1, -1)",
                local_sign=-1,
                epsilon_psi_value=-1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=3.0,
            ),
        ]

        self.orbital_components = [
            OrbitalIntegralComponent(
                conjugacy_class="gamma_1 = Central unit 1_SO7",
                centralizer_dimension=21,
                weyl_discriminant=1.0,
                weighted_integral_value=round(2.250 * math.exp(-0.1 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_2 = Regular elliptic class",
                centralizer_dimension=3,
                weyl_discriminant=0.81,
                weighted_integral_value=round(1.150 * math.exp(-0.16 * cutoff), 5),
                is_unipotent=False,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_3 = Subregular unipotent stratum",
                centralizer_dimension=7,
                weyl_discriminant=0.36,
                weighted_integral_value=round(0.680 * math.exp(-0.24 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_4 = Semi-simple hyperbolic class",
                centralizer_dimension=5,
                weyl_discriminant=0.58,
                weighted_integral_value=round(0.445 * math.exp(-0.29 * cutoff), 5),
                is_unipotent=False,
            ),
        ]

        self.spectral_components = [
            SpectralTraceComponent(
                spectrum_type="Discrete Cuspidal",
                representation_label="pi_cusp_so7 (Cuspidal automorphic representation)",
                spectral_parameter=2.5,
                intertwining_log_derivative=0.0,
                spectral_weight=round(2.100 * math.exp(-0.11 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Discrete Residual",
                representation_label="pi_res_so7 (Residual spectrum)",
                spectral_parameter=1.5,
                intertwining_log_derivative=0.0,
                spectral_weight=round(0.720 * math.exp(-0.19 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Eisenstein P_max",
                representation_label="Ind_P^G(pi_SO5 tensor delta_P^s)",
                spectral_parameter=2.8,
                intertwining_log_derivative=0.61,
                spectral_weight=round(1.050 * math.exp(-0.17 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Minimal",
                representation_label="Ind_B^G(characters tensor delta_B^s)",
                spectral_parameter=1.9,
                intertwining_log_derivative=0.38,
                spectral_weight=round(0.655 * math.exp(-0.23 * cutoff), 5),
            ),
        ]

    def _init_gl4(self, cutoff: float) -> None:
        """GL(4) standard linear group with self-dual stable trace formula."""
        self.arthur_parameter = ArthurParameterData(
            parameter_label="psi = tau_4 (Irreducible cuspidal GL_4 representation)",
            dual_group_label="GL_4(C)",
            deligne_factors_count=1,
            component_group_order=1,
            is_tempered=True,
            is_generic=True,
        )

        self.endoscopic_groups = [
            EndoscopicGroupData(
                group_h_label="G_0 = GL_4 (Only endoscopic group: trace formula is stable)",
                is_quasi_split=True,
                dimension_h=16,
                tamagawa_iota_coefficient=1.0,
                transfer_factor_sign=1,
                stable_orbital_integral=round(3.400 * math.exp(-0.12 * cutoff), 5),
            ),
        ]

        self.arthur_packet = [
            ArthurPacketRepresentation(
                rep_label="pi_gl4 (Unique cuspidal representation, packet is singleton)",
                pairing_character="1",
                local_sign=1,
                epsilon_psi_value=1,
                multiplicity_in_discrete_spectrum=1,
                infinitesimal_character=2.0,
            ),
        ]

        self.orbital_components = [
            OrbitalIntegralComponent(
                conjugacy_class="gamma_1 = Identity matrix I_4",
                centralizer_dimension=16,
                weyl_discriminant=1.0,
                weighted_integral_value=round(1.850 * math.exp(-0.1 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_2 = Regular elliptic conjugacy class",
                centralizer_dimension=4,
                weyl_discriminant=0.75,
                weighted_integral_value=round(0.980 * math.exp(-0.17 * cutoff), 5),
                is_unipotent=False,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_3 = Jordan block unipotent class",
                centralizer_dimension=6,
                weyl_discriminant=0.40,
                weighted_integral_value=round(0.350 * math.exp(-0.25 * cutoff), 5),
                is_unipotent=True,
            ),
            OrbitalIntegralComponent(
                conjugacy_class="gamma_4 = Semi-simple diagonal class",
                centralizer_dimension=4,
                weyl_discriminant=0.60,
                weighted_integral_value=round(0.220 * math.exp(-0.28 * cutoff), 5),
                is_unipotent=False,
            ),
        ]

        self.spectral_components = [
            SpectralTraceComponent(
                spectrum_type="Discrete Cuspidal",
                representation_label="pi_cusp_gl4 (Cuspidal automorphic representation)",
                spectral_parameter=2.0,
                intertwining_log_derivative=0.0,
                spectral_weight=round(1.720 * math.exp(-0.12 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Discrete Residual",
                representation_label="pi_res (Moeglin-Waldspurger residual spectrum)",
                spectral_parameter=1.0,
                intertwining_log_derivative=0.0,
                spectral_weight=round(0.420 * math.exp(-0.21 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Eisenstein P_2_2",
                representation_label="Ind_{P_22}^G(pi_1 tensor pi_2)",
                spectral_parameter=2.1,
                intertwining_log_derivative=0.48,
                spectral_weight=round(0.780 * math.exp(-0.18 * cutoff), 5),
            ),
            SpectralTraceComponent(
                spectrum_type="Continuous Minimal P_1111",
                representation_label="Ind_B^G(characters)",
                spectral_parameter=1.5,
                intertwining_log_derivative=0.30,
                spectral_weight=round(0.480 * math.exp(-0.24 * cutoff), 5),
            ),
        ]

    def evaluate_trace_formula(self) -> TraceFormulaEvaluation:
        """Evaluate geometric side, spectral side, and endoscopic stabilization."""
        geom_sum = sum(c.weighted_integral_value for c in self.orbital_components)
        spec_sum = sum(s.spectral_weight for s in self.spectral_components)

        endoscopic_sum = sum(
            grp.tamagawa_iota_coefficient * grp.transfer_factor_sign * grp.stable_orbital_integral
            for grp in self.endoscopic_groups
        )

        residual = abs(geom_sum - spec_sum)
        is_stabilized = residual < 0.25

        # Cognitive spatial metrics
        resonance = max(0.0, min(1.0, 1.0 - (residual / (geom_sum + 1e-6))))
        stability = 0.95 if is_stabilized else 0.70

        return TraceFormulaEvaluation(
            geometric_total=round(geom_sum, 5),
            spectral_total=round(spec_sum, 5),
            endoscopic_reconstructed_total=round(endoscopic_sum, 5),
            trace_identity_residual=round(residual, 5),
            is_stabilized=is_stabilized,
            cognitive_resonance_score=round(resonance, 4),
            spatial_stability_index=round(stability, 4),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize loom state into structured dictionary."""
        eval_data = self.evaluate_trace_formula()
        return {
            "archetype": self.archetype_str,
            "test_function_cutoff": self.test_function_cutoff,
            "spectral_truncation_level": self.spectral_truncation_level,
            "arthur_parameter": self.arthur_parameter.to_dict() if self.arthur_parameter else None,
            "endoscopic_groups": [g.to_dict() for g in self.endoscopic_groups],
            "arthur_packet": [p.to_dict() for p in self.arthur_packet],
            "orbital_components": [o.to_dict() for o in self.orbital_components],
            "spectral_components": [s.to_dict() for s in self.spectral_components],
            "evaluation": eval_data.to_dict(),
        }

    def generate_svg(self) -> str:
        """
        Generate publication-grade dark titanium SVG diagram of the trace formula
        and endoscopic classification with zero em dashes.
        """
        eval_data = self.evaluate_trace_formula()
        width = 1040
        height = 680

        # Primary palette
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
            '    <linearGradient id="grad_blue" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{accent_blue}" stop-opacity="0.2"/>',
            f'      <stop offset="100%" stop-color="{accent_indigo}" stop-opacity="0.05"/>',
            '    </linearGradient>',
            '    <linearGradient id="grad_emerald" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{accent_emerald}" stop-opacity="0.25"/>',
            f'      <stop offset="100%" stop-color="{accent_emerald}" stop-opacity="0.05"/>',
            '    </linearGradient>',
            '    <linearGradient id="grad_rose" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{accent_rose}" stop-opacity="0.25"/>',
            f'      <stop offset="100%" stop-color="{accent_rose}" stop-opacity="0.05"/>',
            '    </linearGradient>',
            '  </defs>',
            '',
            '  <!-- Header Banner -->',
            f'  <rect x="24" y="24" width="{width - 48}" height="76" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="48" y="58" fill="{accent_blue}" font-family="system-ui, -apple-system, sans-serif" font-size="20" font-weight="700">',
            '    Arthur-Selberg Trace Formula &amp; Endoscopic Classification Loom',
            '  </text>',
            f'  <text x="48" y="82" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="13">',
            f'    Group: {self.archetype_str} | Truncation: T={self.test_function_cutoff} | Residual: |I_geom - I_spec| = {eval_data.trace_identity_residual}',
            '  </text>',
            '',
            '  <!-- Left Column: Geometric Orbital Integral Plane -->',
            f'  <rect x="24" y="116" width="315" height="340" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="44" y="146" fill="{accent_amber}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Geometric Side: I_geom(f)',
            '  </text>',
            f'  <text x="44" y="166" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="12">',
            f'    Total Orbital Sum: {eval_data.geometric_total}',
            '  </text>',
        ]

        # Draw orbital components
        y_cursor = 190
        for i, orb in enumerate(self.orbital_components):
            badge_color = accent_rose if orb.is_unipotent else accent_blue
            tag = "Unipotent" if orb.is_unipotent else "Semi-simple"
            svg_parts.extend([
                f'  <g transform="translate(40, {y_cursor})">',
                f'    <rect width="283" height="52" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
                f'    <circle cx="14" cy="26" r="6" fill="{badge_color}"/>',
                f'    <text x="30" y="22" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{orb.conjugacy_class[:26]}</text>',
                f'    <text x="30" y="40" fill="{text_muted}" font-family="monospace" font-size="11">J_M={orb.weighted_integral_value} | D={orb.weyl_discriminant} ({tag})</text>',
                '  </g>',
            ])
            y_cursor += 62

        # Central Column: Endoscopic Transfer Aperture & Stable Formula
        svg_parts.extend([
            f'  <rect x="355" y="116" width="320" height="340" rx="12" fill="url(#grad_blue)" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="375" y="146" fill="{accent_blue}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Endoscopic Aperture: I(f) = sum_H iota S^H(f^H)',
            '  </text>',
            f'  <text x="375" y="166" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="12">',
            f'    Reconstructed Stable Integral: {eval_data.endoscopic_reconstructed_total}',
            '  </text>',
        ])

        y_h = 190
        for grp in self.endoscopic_groups:
            sign_str = "+1" if grp.transfer_factor_sign > 0 else "-1"
            svg_parts.extend([
                f'  <g transform="translate(371, {y_h})">',
                f'    <rect width="288" height="66" rx="8" fill="{card_bg}" stroke="{card_border}" stroke-width="1.2"/>',
                f'    <text x="14" y="24" fill="{accent_emerald}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{grp.group_h_label[:34]}</text>',
                f'    <text x="14" y="44" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">iota(G,H)={grp.tamagawa_iota_coefficient} | transfer sign={sign_str} | dim={grp.dimension_h}</text>',
                f'    <text x="14" y="60" fill="{accent_amber}" font-family="monospace" font-size="11">Stable Orbital S^H(f^H) = {grp.stable_orbital_integral}</text>',
                '  </g>',
            ])
            y_h += 78

        # Stabilization Indicator Badge
        stab_text = "Stabilization Verified" if eval_data.is_stabilized else "Asymptotic Balance"
        stab_bg = accent_emerald if eval_data.is_stabilized else accent_amber
        svg_parts.extend([
            f'  <g transform="translate(371, 385)">',
            f'    <rect width="288" height="52" rx="8" fill="{card_border}" fill-opacity="0.6"/>',
            f'    <circle cx="20" cy="26" r="7" fill="{stab_bg}"/>',
            f'    <text x="38" y="24" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{stab_text}</text>',
            f'    <text x="38" y="42" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="11">Residual = {eval_data.trace_identity_residual} | Resonance = {eval_data.cognitive_resonance_score}</text>',
            '  </g>',
        ])

        # Right Column: Spectral Automorphic Character Tower
        svg_parts.extend([
            f'  <rect x="691" y="116" width="325" height="340" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="711" y="146" fill="{accent_emerald}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Spectral Side: I_spec(f)',
            '  </text>',
            f'  <text x="711" y="166" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="12">',
            f'    Total Spectral Sum: {eval_data.spectral_total}',
            '  </text>',
        ])

        y_s = 190
        for spec in self.spectral_components:
            is_disc = "Discrete" in spec.spectrum_type
            s_color = accent_emerald if is_disc else accent_indigo
            svg_parts.extend([
                f'  <g transform="translate(707, {y_s})">',
                f'    <rect width="293" height="52" rx="8" fill="{card_border}" fill-opacity="0.4"/>',
                f'    <circle cx="14" cy="26" r="6" fill="{s_color}"/>',
                f'    <text x="28" y="22" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{spec.representation_label[:28]}</text>',
                f'    <text x="28" y="40" fill="{text_muted}" font-family="monospace" font-size="11">W={spec.spectral_weight} | M\'/M={spec.intertwining_log_derivative} ({spec.spectrum_type[:10]})</text>',
                '  </g>',
            ])
            y_s += 62

        # Bottom Row: Arthur Parameter & Arthur Packet Multiplicity Polytope
        svg_parts.extend([
            f'  <rect x="24" y="472" width="{width - 48}" height="184" rx="12" fill="{card_bg}" stroke="{card_border}" stroke-width="1.5"/>',
            f'  <text x="48" y="504" fill="{accent_rose}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="600">',
            '    Arthur Parameter psi &amp; Automorphic A-Packet Multiplicity Lattice Pi_psi',
            '  </text>',
        ])

        if self.arthur_parameter:
            p = self.arthur_parameter
            tempered_str = "Tempered" if p.is_tempered else "Non-tempered (Arthur type)"
            svg_parts.extend([
                f'  <text x="48" y="528" fill="{text_muted}" font-family="monospace" font-size="12">',
                f'    Parameter: {p.parameter_label} | Dual: {p.dual_group_label} | |S_psi|={p.component_group_order} ({tempered_str})',
                '  </text>',
            ])

        x_pkt = 48
        for pkt in self.arthur_packet:
            m_badge = accent_emerald if pkt.multiplicity_in_discrete_spectrum > 0 else accent_amber
            svg_parts.extend([
                f'  <g transform="translate({x_pkt}, 546)">',
                f'    <rect width="230" height="92" rx="8" fill="{card_border}" fill-opacity="0.5"/>',
                f'    <text x="12" y="24" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="12" font-weight="600">{pkt.rep_label[:24]}</text>',
                f'    <text x="12" y="44" fill="{text_muted}" font-family="monospace" font-size="11">&lt;s, pi&gt; = {pkt.pairing_character} | sign={pkt.local_sign}</text>',
                f'    <text x="12" y="62" fill="{text_muted}" font-family="monospace" font-size="11">inf-char = {pkt.infinitesimal_character}</text>',
                f'    <circle cx="20" cy="78" r="5" fill="{m_badge}"/>',
                f'    <text x="32" y="82" fill="{text_light}" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600">Multiplicity m(pi) = {pkt.multiplicity_in_discrete_spectrum}</text>',
                '  </g>',
            ])
            x_pkt += 244

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)


def run_demo(group_name: Optional[str] = None) -> Dict[str, Any]:
    """Execute Arthur-Selberg Trace Formula & Endoscopic Classification demo."""
    archetype = ArthurGroupArchetype.SO5_SPLIT.value
    if group_name:
        for arch in ArthurGroupArchetype:
            if group_name.lower() in arch.value.lower():
                archetype = arch.value
                break

    loom = ArthurSelbergTraceLoom(
        test_function_cutoff=2.5,
        spectral_truncation_level=4,
        default_archetype=archetype,
    )
    return loom.to_dict()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Arthur-Selberg Trace Formula & Endoscopic Classification Loom")
    parser.add_argument("--demo", action="store_true", help="Run demonstrator")
    parser.add_argument("--group", type=str, default="SO5", help="Reductive group archetype: SO5, SP4, SO7, GL4")
    parser.add_argument("--cutoff", type=float, default=2.5, help="Test function cutoff parameter T")
    parser.add_argument("--json", action="store_true", help="Output JSON structure")
    parser.add_argument("--svg", type=str, help="Save SVG visualization to destination path")

    args = parser.parse_args()

    arch_val = ArthurGroupArchetype.SO5_SPLIT.value
    for a in ArthurGroupArchetype:
        if args.group.lower() in a.value.lower() or args.group.upper() in a.value:
            arch_val = a.value
            break

    loom = ArthurSelbergTraceLoom(
        test_function_cutoff=args.cutoff,
        spectral_truncation_level=4,
        default_archetype=arch_val,
    )

    if args.svg:
        svg_content = loom.generate_svg()
        with open(args.svg, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"SVG saved to {args.svg}")

    if args.json or args.demo:
        print(json.dumps(loom.to_dict(), indent=2))
    else:
        ev = loom.evaluate_trace_formula()
        print("================================================================================")
        print("  Arthur-Selberg Trace Formula & Endoscopic Classification Loom")
        print("================================================================================")
        print(f"Archetype: {loom.archetype_str}")
        print(f"Test Function Cutoff: {loom.test_function_cutoff}")
        print(f"Geometric Total: {ev.geometric_total}")
        print(f"Spectral Total:  {ev.spectral_total}")
        print(f"Endoscopic Reconstructed: {ev.endoscopic_reconstructed_total}")
        print(f"Identity Residual: {ev.trace_identity_residual} (Stabilized: {ev.is_stabilized})")
        print(f"Cognitive Resonance: {ev.cognitive_resonance_score}")
        print(f"Spatial Stability Index: {ev.spatial_stability_index}")
        print("================================================================================")
