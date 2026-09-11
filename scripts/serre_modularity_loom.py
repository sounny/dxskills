r"""
Serre's Modularity Conjecture & Odd Galois Representations Loom.
Models Jean-Pierre Serre's modularity conjecture and the Khare-Wintenberger theorem:
- Continuous, irreducible, odd representations rho_bar: G_Q -> GL_2(F_p_bar)
- Strict parity condition: det(rho_bar(c)) = -1 for complex conjugation c
- Serre's explicit optimal invariants: level N(rho_bar), weight k(rho_bar), character epsilon(rho_bar)
- Local inertia group actions: tame inertia characters psi_1, psi_2 and Fontaine-Laffaille weights
- Modularity lifting and Taylor-Wiles-Kisin deformation towers
Strictly zero em dashes (chr(8212)) across all functions, docstrings, and comments.
"""

import math
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


class SerreModularityArchetype(str, Enum):
    """Canonical odd mod p Galois representations and Serre modularity models."""
    WEIGHT_TWO_ELLIPTIC = "Elliptic Curve Residual Representation rho_bar_{E, p} (k = 2, Level N)"
    RAMANUJAN_DELTA_MOD_P = "Ramanujan Delta mod p Representation rho_bar_{Delta, p} (k = 12, Level 1)"
    DIHEDRAL_INDUCTION = "Dihedral Induced Representation Ind_{G_K}^{G_Q}(chi) (CM Form)"
    EVEN_NON_MODULAR = "Even Galois Representation det(rho_bar(c)) = +1 (Non-Modular Obstruction)"


@dataclass
class OddGaloisRepresentationData:
    """Residual mod p Galois representation rho_bar: G_Q -> GL_2(F_p_bar)."""
    representation_id: str
    prime_p: int
    dimension: int
    is_odd: bool
    is_irreducible: bool
    artin_conductor_prime_to_p: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "representation_id": self.representation_id,
            "prime_p": self.prime_p,
            "dimension": self.dimension,
            "is_odd": self.is_odd,
            "is_irreducible": self.is_irreducible,
            "artin_conductor_prime_to_p": self.artin_conductor_prime_to_p,
        }


@dataclass
class SerreInvariantsData:
    """Serre's optimal level N, weight k, and Nebentypus character epsilon."""
    serre_level_n: int
    serre_weight_k: int
    serre_character_epsilon: str
    tame_inertia_weights: List[int]
    is_fontaine_laffaille: bool
    is_companion_form_pair: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "serre_level_n": self.serre_level_n,
            "serre_weight_k": self.serre_weight_k,
            "serre_character_epsilon": self.serre_character_epsilon,
            "tame_inertia_weights": self.tame_inertia_weights,
            "is_fontaine_laffaille": self.is_fontaine_laffaille,
            "is_companion_form_pair": self.is_companion_form_pair,
        }


@dataclass
class KhareWintenbergerModularityData:
    """Serre modularity status and Khare-Wintenberger lifting proof."""
    is_modular: bool
    modular_eigenform_space: str
    proof_reference: str
    deformation_lifting_status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_modular": self.is_modular,
            "modular_eigenform_space": self.modular_eigenform_space,
            "proof_reference": self.proof_reference,
            "deformation_lifting_status": self.deformation_lifting_status,
        }


class SerreModularityLoom:
    """
    Synthesizes Serre's Modularity Conjecture, Serre optimal invariants (N, k, epsilon),
    tame inertia characters, and Khare-Wintenberger deformation lifting.
    """

    def __init__(
        self,
        level_n: int = 11,
        prime_p: int = 5,
        default_archetype: str = SerreModularityArchetype.WEIGHT_TWO_ELLIPTIC.value,
    ):
        self.level_n = max(1, level_n)
        self.prime_p = prime_p
        self.default_archetype = default_archetype

        self.representations: List[OddGaloisRepresentationData] = []
        self.serre_invariants: List[SerreInvariantsData] = []
        self.modularity_data: List[KhareWintenbergerModularityData] = []

        self._init_default_models()

    def _init_default_models(self):
        n = self.level_n
        p = self.prime_p

        if "Elliptic" in self.default_archetype:
            n = 11
            k = 2
            is_odd = True
            is_irred = True
            tame_weights = [0, 1]
            fl = True
            comp = False
            mod = True
            space = f"S_2(Gamma_0({n}))"
            proof = "Khare-Wintenberger (2009), Kisin (2009), Wiles (1995)"
            deform = "Unramified deformation lift to characteristic 0 established"
        elif "Delta" in self.default_archetype or "Ramanujan" in self.default_archetype:
            n = 1
            k = 12
            is_odd = True
            is_irred = True
            tame_weights = [0, 11]
            fl = (12 <= p + 1)
            comp = True
            mod = True
            space = "S_12(SL_2(Z))"
            proof = "Deligne (1971), Khare-Wintenberger (2009)"
            deform = "Crystalline deformation lift to Ramanujan Delta cusp form"
        elif "Dihedral" in self.default_archetype or "CM" in self.default_archetype:
            n = 23
            k = 1
            is_odd = True
            is_irred = True
            tame_weights = [0, 0]
            fl = True
            comp = False
            mod = True
            space = f"S_1(Gamma_0({n}), (*/23))"
            proof = "Hecke (1926), Deligne-Serre (1974)"
            deform = "Artin representation weight 1 induction from imaginary quadratic field"
        else:
            # Even Galois representation (obstruction)
            n = 1
            k = 2
            is_odd = False  # det(rho_bar(c)) = +1
            is_irred = True
            tame_weights = [0, 1]
            fl = False
            comp = False
            mod = False
            space = "None (No classical holomorphic cusp form can generate even Galois representation)"
            proof = "Serre Parity Obstruction: All modular Galois representations are strictly odd"
            deform = "Deformation obstruction: trace of complex conjugation violates Eichler-Shimura"

        rep = OddGaloisRepresentationData(
            representation_id=f"RHO-BAR-P{p}-N{n}",
            prime_p=p,
            dimension=2,
            is_odd=is_odd,
            is_irreducible=is_irred,
            artin_conductor_prime_to_p=n,
        )
        self.representations.append(rep)

        inv = SerreInvariantsData(
            serre_level_n=n,
            serre_weight_k=k,
            serre_character_epsilon=f"Trivial mod {n}" if n <= 11 else f"Legendre (*/{n})",
            tame_inertia_weights=tame_weights,
            is_fontaine_laffaille=fl,
            is_companion_form_pair=comp,
        )
        self.serre_invariants.append(inv)

        mod_data = KhareWintenbergerModularityData(
            is_modular=mod,
            modular_eigenform_space=space,
            proof_reference=proof,
            deformation_lifting_status=deform,
        )
        self.modularity_data.append(mod_data)

    def compute_serre_weight_level_one(
        self,
        a: int,
        b: int,
        prime_p: int,
    ) -> int:
        """
        Computes Serre weight k(rho_bar) when restriction to tame inertia
        is of level 1: rho_bar|_{I_p} ~ chi_p^a + chi_p^b with 0 <= a <= b <= p - 2.
        Serre recipe: k = 1 + p*a + b (or 1 + a + p*b depending on ordering).
        In the standard Fontaine-Laffaille normalization: k = 1 + b - a.
        """
        if a > b:
            a, b = b, a
        return 1 + (b - a)

    def evaluate_serre_conjecture(
        self,
        is_odd: bool,
        is_irreducible: bool,
        level_n: int,
        weight_k: int,
    ) -> Dict[str, Any]:
        """
        Evaluates Serre's modularity criterion:
        A representation rho_bar: G_Q -> GL_2(F_p_bar) is modular
        if and only if it is odd (det rho_bar(c) = -1) and irreducible.
        """
        is_modular = is_odd and is_irreducible
        if is_modular:
            verdict = f"Modular: Arises from Hecke eigenform f in S_{weight_k}(Gamma_0({level_n}))"
            lifting = "Khare-Wintenberger Deformation Ladder: Solvable Base Change and Modularity Lifting"
        elif not is_odd:
            verdict = "Non-Modular: Fails Serre Parity Condition (Representation is Even)"
            lifting = "Parity Obstruction: No Classical Holomorphic Modular Form Corresponds to Even Rep"
        else:
            verdict = "Reducible: Split into 1-Dimensional Characters (Eisenstein Modularity)"
            lifting = "Reducible Case: Governed by Class Field Theory and Dirichlet Characters"

        return {
            "is_odd": is_odd,
            "is_irreducible": is_irreducible,
            "is_modular": is_modular,
            "serre_verdict": verdict,
            "lifting_mechanism": lifting,
        }

    def generate_serre_svg(self) -> str:
        """
        Generates dark titanium spatial SVG visualizing Serre Modularity Loom:
        Panel 1: Residual Representation rho_bar: G_Q -> GL_2(F_p_bar) & Odd Parity
        Panel 2: Serre Optimal Invariants (Level N, Weight k, Character epsilon)
        Panel 3: Local Tame Inertia Characters & Fontaine-Laffaille Range
        Panel 4: Khare-Wintenberger Modularity Proof & Deformation Tower
        """
        width = 1100
        height = 680

        rep = self.representations[0] if self.representations else None
        inv = self.serre_invariants[0] if self.serre_invariants else None
        mod = self.modularity_data[0] if self.modularity_data else None

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            '<defs>',
            '  <linearGradient id="smBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#0a0c10"/>',
            '    <stop offset="50%" stop-color="#12161f"/>',
            '    <stop offset="100%" stop-color="#07090c"/>',
            '  </linearGradient>',
            '  <linearGradient id="smCard" x1="0%" y1="0%" x2="0%" y2="100%">',
            '    <stop offset="0%" stop-color="#1a202c" stop-opacity="0.85"/>',
            '    <stop offset="100%" stop-color="#111620" stop-opacity="0.95"/>',
            '  </linearGradient>',
            '  <linearGradient id="smEmerald" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#059669"/>',
            '    <stop offset="100%" stop-color="#34d399"/>',
            '  </linearGradient>',
            '  <linearGradient id="smAmber" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#d97706"/>',
            '    <stop offset="100%" stop-color="#fbbf24"/>',
            '  </linearGradient>',
            '</defs>',
            f'<rect width="{width}" height="{height}" fill="url(#smBg)"/>',
            # Header
            '  <g transform="translate(50, 45)">',
            '    <text x="0" y="0" font-family="ui-sans-serif, system-ui" font-size="20" font-weight="bold" fill="#f8fafc">Serre\'s Modularity Conjecture &amp; Odd Galois Representations Loom</text>',
            '    <text x="0" y="24" font-family="ui-monospace, monospace" font-size="12" fill="#94a3b8">Residual Galois Representations, Serre Optimal Invariants (N, k, &#949;), and Khare-Wintenberger Lifting</text>',
            '  </g>',
        ]

        # Panel 1: Residual Representation & Parity
        svg.extend([
            '  <g transform="translate(50, 95)">',
            '    <rect width="480" height="260" rx="12" fill="url(#smCard)" stroke="#34d399" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#34d399">Residual Galois Representation &#961;_bar</text>',
            f'    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Archetype: {self.default_archetype.split("(")[0].strip()}</text>',
            '    <rect x="24" y="80" width="432" height="70" rx="8" fill="#1e293b" stroke="#334155"/>',
            f'    <text x="36" y="105" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#6ee7b7">&#961;_bar: Gal(Q_bar / Q) -&gt; GL_2(F_{rep.prime_p}_bar)</text>',
            f'    <text x="36" y="130" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Odd Parity: det(&#961;_bar(c)) = {"-1 (Odd)" if rep.is_odd else "+1 (Even)"} | Irreducible: {rep.is_irreducible}</text>',
            f'    <text x="24" y="180" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Prime-to-p Artin Conductor: N(&#961;_bar) = {rep.artin_conductor_prime_to_p}</text>',
            f'    <text x="24" y="205" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Serre Modularity Status: {mod.is_modular}</text>',
            f'    <text x="24" y="230" font-family="ui-monospace, monospace" font-size="10" fill="#a7f3d0">{mod.modular_eigenform_space}</text>',
            '  </g>',
        ])

        # Panel 2: Serre Optimal Invariants
        svg.extend([
            '  <g transform="translate(570, 95)">',
            '    <rect width="480" height="260" rx="12" fill="url(#smCard)" stroke="#38bdf8" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#38bdf8">Serre Invariants (N, k, &#949;)</text>',
            '    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Minimal Modular Form Parameters</text>',
            '    <rect x="24" y="80" width="432" height="75" rx="8" fill="#1e293b" stroke="#334155"/>',
            f'    <text x="36" y="103" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#7dd3fc">Level N = {inv.serre_level_n} | Weight k = {inv.serre_weight_k}</text>',
            f'    <text x="36" y="125" font-family="ui-monospace, monospace" font-size="11" fill="#f8fafc">Nebentypus: &#949; = {inv.serre_character_epsilon}</text>',
            f'    <text x="36" y="145" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Fontaine-Laffaille Admissible: {inv.is_fontaine_laffaille}</text>',
            f'    <text x="24" y="185" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Companion Form Pair (Weight p + 1 - k): {inv.is_companion_form_pair}</text>',
            f'    <text x="24" y="210" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Weight Lowering (Mazur Principle / Ribet Level Optimization): Proved</text>',
            f'    <text x="24" y="235" font-family="ui-monospace, monospace" font-size="11" fill="#a7f3d0">Minimal Conductor Lower Bound: Satisfied</text>',
            '  </g>',
        ])

        # Panel 3: Local Tame Inertia
        svg.extend([
            '  <g transform="translate(50, 380)">',
            '    <rect width="480" height="260" rx="12" fill="url(#smCard)" stroke="#fbbf24" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#fbbf24">Local Tame Inertia Actions I_p</text>',
            f'    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Inertia Characters &#968;_1, &#968;_2</text>',
            '    <rect x="24" y="80" width="432" height="70" rx="8" fill="#1e293b" stroke="#334155"/>',
            f'    <text x="36" y="105" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#fde68a">&#961;_bar|_{{I_p}} ~ diag(&#968;^{inv.tame_inertia_weights[0]}, &#968;^{inv.tame_inertia_weights[-1]})</text>',
            f'    <text x="36" y="130" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Tame Weights: {inv.tame_inertia_weights} in Range [0, p - 1]</text>',
            f'    <text x="24" y="180" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Action on Inertia Subgroup: Level 1 vs Level 2 Characters</text>',
            f'    <text x="24" y="205" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Fontaine-Laffaille Theory: Crystalline Lifting Bound k &#8804; p + 1</text>',
            f'    <text x="24" y="230" font-family="ui-monospace, monospace" font-size="11" fill="#a7f3d0">Breuil-Mezard Conjecture: Weight Multiplicities Match Geometry</text>',
            '  </g>',
        ])

        # Panel 4: Khare-Wintenberger Proof
        svg.extend([
            '  <g transform="translate(570, 380)">',
            '    <rect width="480" height="260" rx="12" fill="url(#smCard)" stroke="#c084fc" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#c084fc">Khare-Wintenberger Modularity Proof</text>',
            f'    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Proof Framework (2009)</text>',
            '    <rect x="24" y="80" width="432" height="85" rx="8" fill="#1e293b" stroke="#334155"/>',
            '    <text x="36" y="108" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#e9d5ff">Theorem: Serre\'s Conjecture is True in Full Generality</text>',
            f'    <text x="36" y="132" font-family="ui-monospace, monospace" font-size="11" fill="#f8fafc">{mod.proof_reference[:52]}</text>',
            f'    <text x="36" y="152" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Modularity Lifting &amp; Potential Modularity Deformations</text>',
            f'    <text x="24" y="195" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Solvable Base Change: Reduction to Level 1 and Weight 2</text>',
            f'    <text x="24" y="218" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">L-Function Analytic Continuation &amp; Langlands Correspondence</text>',
            f'    <text x="24" y="240" font-family="ui-monospace, monospace" font-size="11" fill="#a7f3d0">All Odd Residual Representations are Modular: Proved</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "level_n": self.level_n,
            "prime_p": self.prime_p,
            "default_archetype": self.default_archetype,
            "representations": [r.to_dict() for r in self.representations],
            "serre_invariants": [i.to_dict() for i in self.serre_invariants],
            "modularity_data": [m.to_dict() for m in self.modularity_data],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
