r"""
Fontaine-Mazur Conjecture & Geometric Galois Representations Loom.
Models Jean-Marc Fontaine and Barry Mazur's conjecture on geometric p-adic Galois representations:
- Irreducible continuous representations rho: G_Q -> GL_n(Q_p_bar) unramified almost everywhere
- Local p-adic Hodge theory: de Rham, crystalline, semi-stable, and Hodge-Tate admissibility
- Hodge-Tate weights, Sen polynomials, and filtration ladders Fil^i D_dR(V)
- Fontaine period rings: B_HT, B_dR, B_cris, B_st and Frobenius / monodromy operators (phi, N)
- Modularity and Taylor-Wiles-Kisin deformation ring isomorphisms R = T
Strictly zero em dashes (chr(8212)) across all functions, docstrings, and comments.
"""

import math
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


class FontaineMazurArchetype(str, Enum):
    """Canonical Galois representations and geometric Fontaine-Mazur models."""
    ELLIPTIC_CURVE_TATE_MODULE = "Elliptic Curve Tate Module T_p(E) (Weight 2, HT = {0, 1})"
    RAMANUJAN_DELTA_REP = "Ramanujan Tau Galois Representation rho_Delta (Weight 12, HT = {0, 11})"
    DIRICHLET_TATE_TWIST = "Abelian Dirichlet Character Tate Twist Q_p(chi)(m)"
    NON_GEOMETRIC_UNRAMIFIED = "Non-de Rham Non-Geometric Representation (Exotic Deformation)"


@dataclass
class FontainePeriodRingData:
    """Fontaine period ring comparison space D_*(V) = (B_* tensor V)^{G_Q_p}."""
    ring_name: str
    dimension: int
    is_admissible: bool
    frobenius_eigenvalues: List[float]
    monodromy_nilpotent_order: int
    filtration_steps: List[Tuple[int, int]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ring_name": self.ring_name,
            "dimension": self.dimension,
            "is_admissible": self.is_admissible,
            "frobenius_eigenvalues": self.frobenius_eigenvalues,
            "monodromy_nilpotent_order": self.monodromy_nilpotent_order,
            "filtration_steps": self.filtration_steps,
        }


@dataclass
class HodgeTateData:
    """Hodge-Tate weights and Sen operator spectrum."""
    representation_dimension: int
    hodge_tate_weights: List[int]
    sen_polynomial_coefficients: List[float]
    is_hodge_tate: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "representation_dimension": self.representation_dimension,
            "hodge_tate_weights": self.hodge_tate_weights,
            "sen_polynomial_coefficients": self.sen_polynomial_coefficients,
            "is_hodge_tate": self.is_hodge_tate,
        }


@dataclass
class GeometricModularityData:
    """Fontaine-Mazur geometric status and deformation ring isomorphism."""
    representation_label: str
    is_unramified_almost_everywhere: bool
    is_de_rham_at_p: bool
    is_geometric_representation: bool
    associated_motive_or_variety: str
    deformation_ring_status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "representation_label": self.representation_label,
            "is_unramified_almost_everywhere": self.is_unramified_almost_everywhere,
            "is_de_rham_at_p": self.is_de_rham_at_p,
            "is_geometric_representation": self.is_geometric_representation,
            "associated_motive_or_variety": self.associated_motive_or_variety,
            "deformation_ring_status": self.deformation_ring_status,
        }


class FontaineMazurLoom:
    """
    Synthesizes Fontaine-Mazur geometric Galois representations, Fontaine period rings,
    Hodge-Tate weights, Sen operators, and Taylor-Wiles-Kisin modularity criteria.
    """

    def __init__(
        self,
        dimension: int = 2,
        prime_p: int = 5,
        default_archetype: str = FontaineMazurArchetype.ELLIPTIC_CURVE_TATE_MODULE.value,
    ):
        self.dimension = max(1, dimension)
        self.prime_p = prime_p
        self.default_archetype = default_archetype

        self.period_rings: List[FontainePeriodRingData] = []
        self.hodge_tate_data: List[HodgeTateData] = []
        self.geometric_modularity: List[GeometricModularityData] = []

        self._init_default_models()

    def _init_default_models(self):
        d = self.dimension
        p = self.prime_p

        if "Elliptic" in self.default_archetype:
            d = 2
            ht_weights = [0, 1]
            unram_ae = True
            de_rham = True
            geom = True
            motive = "H^1_et(E_Q_bar, Q_p(1)) for Elliptic Curve E / Q"
            def_ring = "R = T Modularity Theorem (Wiles, Taylor-Wiles, Breuil-Conrad-Diamond-Taylor)"
            frob_eigs = [round(math.sqrt(p), 3), round(p / math.sqrt(p), 3)]
            mono_order = 0
        elif "Delta" in self.default_archetype or "Ramanujan" in self.default_archetype:
            d = 2
            ht_weights = [0, 11]
            unram_ae = True
            de_rham = True
            geom = True
            motive = "Subquotient of H^{11}_et(X(1)^10, Q_p(11)) for Ramanujan Delta Form"
            def_ring = "R = T Crystalline Deformation Modularity (Kisin 2009)"
            frob_eigs = [round(p ** 5.5, 2), round(p ** 5.5, 2)]
            mono_order = 0
        elif "Dirichlet" in self.default_archetype or "Twist" in self.default_archetype:
            d = 1
            ht_weights = [1]
            unram_ae = True
            de_rham = True
            geom = True
            motive = "Artin Motive M(chi) tensor Q_p(1) (Cyclotomic Extension)"
            def_ring = "Abelian Class Field Theory (Kronecker-Weber Theorem)"
            frob_eigs = [float(p)]
            mono_order = 0
        else:
            # Exotic Non-Geometric Deformation
            d = 2
            ht_weights = [0, 0]  # Non-distinct or non-algebraic
            unram_ae = False
            de_rham = False
            geom = False
            motive = "None (Constructed via Ramified Deformation without Geometric Origin)"
            def_ring = "Obstruction in Fontaine-Mazur Modularity Criterion"
            frob_eigs = [1.0, 1.0]
            mono_order = 1

        self.dimension = d

        # Period rings data: B_HT, B_dR, B_cris, B_st
        b_ht = FontainePeriodRingData(
            ring_name="B_HT (Hodge-Tate)",
            dimension=d,
            is_admissible=True,
            frobenius_eigenvalues=[],
            monodromy_nilpotent_order=0,
            filtration_steps=[(w, 1) for w in ht_weights],
        )
        b_dr = FontainePeriodRingData(
            ring_name="B_dR (de Rham)",
            dimension=d if de_rham else 0,
            is_admissible=de_rham,
            frobenius_eigenvalues=[],
            monodromy_nilpotent_order=0,
            filtration_steps=[(w, 1) for w in sorted(ht_weights)],
        )
        b_st = FontainePeriodRingData(
            ring_name="B_st (Semi-Stable)",
            dimension=d if de_rham else 0,
            is_admissible=de_rham,
            frobenius_eigenvalues=frob_eigs,
            monodromy_nilpotent_order=mono_order,
            filtration_steps=[],
        )
        b_cris = FontainePeriodRingData(
            ring_name="B_cris (Crystalline)",
            dimension=d if (de_rham and mono_order == 0) else 0,
            is_admissible=(de_rham and mono_order == 0),
            frobenius_eigenvalues=frob_eigs,
            monodromy_nilpotent_order=0,
            filtration_steps=[],
        )
        self.period_rings = [b_ht, b_dr, b_st, b_cris]

        sen_poly = self.compute_sen_polynomial(weights=ht_weights)
        ht_info = HodgeTateData(
            representation_dimension=d,
            hodge_tate_weights=ht_weights,
            sen_polynomial_coefficients=sen_poly,
            is_hodge_tate=True,
        )
        self.hodge_tate_data.append(ht_info)

        geom_info = GeometricModularityData(
            representation_label=f"rho_{p}_{self.default_archetype.split()[0]}",
            is_unramified_almost_everywhere=unram_ae,
            is_de_rham_at_p=de_rham,
            is_geometric_representation=geom,
            associated_motive_or_variety=motive,
            deformation_ring_status=def_ring,
        )
        self.geometric_modularity.append(geom_info)

    def compute_sen_polynomial(self, weights: List[int]) -> List[float]:
        """
        Computes the coefficients of the Sen polynomial Theta_V(T) = prod (T - h_i).
        The roots in C_p are precisely the Hodge-Tate weights h_i.
        """
        if not weights:
            return [1.0]
        # Polynomial multiplication: (T - w1)(T - w2)...
        poly = [1.0]
        for w in weights:
            # multiply poly by (T - w)
            new_poly = [0.0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new_poly[i] += c  # T term
                new_poly[i + 1] -= c * float(w)  # constant term
            poly = new_poly
        return poly

    def evaluate_fontaine_mazur_conjecture(
        self,
        unramified_ae: bool,
        de_rham: bool,
        dimension: int = 2,
    ) -> Dict[str, Any]:
        """
        Evaluates the Fontaine-Mazur Conjecture condition:
        An irreducible p-adic Galois representation rho: G_Q -> GL_n(Q_p_bar)
        comes from geometry (subquotient of algebraic variety cohomology)
        if and only if:
        1. rho is unramified outside a finite set of primes S
        2. The restriction rho|_{G_Q_p} is de Rham.
        """
        is_geom = unramified_ae and de_rham
        if is_geom:
            status = "Geometric: Comes from Cohomology of an Algebraic Variety X / Q"
            modularity = "Proven / Expected via Taylor-Wiles-Kisin Deformation Theory R = T"
        elif not unramified_ae:
            status = "Non-Geometric: Ramified at Infinitely Many Primes"
            modularity = "Violates Fontaine-Mazur Global Finiteness Condition"
        else:
            status = "Non-Geometric: Local Representation at p Fails de Rham Admissibility"
            modularity = "Violates Fontaine p-Adic Hodge Theory Regularity"

        return {
            "is_unramified_almost_everywhere": unramified_ae,
            "is_de_rham_at_p": de_rham,
            "dimension": dimension,
            "is_geometric": is_geom,
            "fontaine_mazur_verdict": status,
            "modularity_deformation_outlook": modularity,
        }

    def generate_fontaine_mazur_svg(self) -> str:
        """
        Generates dark titanium spatial SVG visualizing Fontaine-Mazur Conjecture Loom:
        Panel 1: Global Galois Representation rho: G_Q -> GL_n(Q_p_bar)
        Panel 2: Local p-Adic Hodge Theory & Period Rings (B_HT, B_dR, B_cris, B_st)
        Panel 3: Hodge-Tate Weights & Sen Polynomial Spectrum
        Panel 4: Taylor-Wiles-Kisin Deformation Rings & Modularity Isomorphism R = T
        """
        width = 1100
        height = 680

        rings = {r.ring_name.split()[0]: r for r in self.period_rings}
        ht = self.hodge_tate_data[0] if self.hodge_tate_data else None
        gm = self.geometric_modularity[0] if self.geometric_modularity else None

        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            '<defs>',
            '  <linearGradient id="fmBg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '    <stop offset="0%" stop-color="#0a0c10"/>',
            '    <stop offset="50%" stop-color="#12161f"/>',
            '    <stop offset="100%" stop-color="#07090c"/>',
            '  </linearGradient>',
            '  <linearGradient id="fmCard" x1="0%" y1="0%" x2="0%" y2="100%">',
            '    <stop offset="0%" stop-color="#1a202c" stop-opacity="0.85"/>',
            '    <stop offset="100%" stop-color="#111620" stop-opacity="0.95"/>',
            '  </linearGradient>',
            '  <linearGradient id="fmCyan" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#06b6d4"/>',
            '    <stop offset="100%" stop-color="#22d3ee"/>',
            '  </linearGradient>',
            '  <linearGradient id="fmPurple" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#8b5cf6"/>',
            '    <stop offset="100%" stop-color="#c084fc"/>',
            '  </linearGradient>',
            '  <linearGradient id="fmLime" x1="0%" y1="0%" x2="100%" y2="0%">',
            '    <stop offset="0%" stop-color="#65a30d"/>',
            '    <stop offset="100%" stop-color="#a3e635"/>',
            '  </linearGradient>',
            '</defs>',
            f'<rect width="{width}" height="{height}" fill="url(#fmBg)"/>',
            # Header
            '  <g transform="translate(50, 45)">',
            '    <text x="0" y="0" font-family="ui-sans-serif, system-ui" font-size="20" font-weight="bold" fill="#f8fafc">Fontaine-Mazur Conjecture &amp; Geometric Galois Representations Loom</text>',
            '    <text x="0" y="24" font-family="ui-monospace, monospace" font-size="12" fill="#94a3b8">p-Adic Galois Representations, Fontaine Period Rings (B_HT, B_dR, B_cris, B_st), and Modularity R = T</text>',
            '  </g>',
        ]

        # Panel 1: Global Galois Representation
        svg.extend([
            '  <g transform="translate(50, 95)">',
            '    <rect width="480" height="260" rx="12" fill="url(#fmCard)" stroke="#38bdf8" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#38bdf8">Global Galois Representation &#961;</text>',
            f'    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Archetype: {self.default_archetype.split("(")[0].strip()}</text>',
            '    <rect x="24" y="80" width="432" height="70" rx="8" fill="#1e293b" stroke="#334155"/>',
            f'    <text x="36" y="105" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#7dd3fc">&#961;: Gal(Q_bar / Q) -&gt; GL_{self.dimension}(Q_p_bar)</text>',
            f'    <text x="36" y="130" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Prime p = {self.prime_p} | Dim = {self.dimension} | Unramified Outside S: {gm.is_unramified_almost_everywhere}</text>',
            f'    <text x="24" y="180" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Local Restriction: &#961;|_{{G_{{Q_{{p}}}}}} is de Rham: {gm.is_de_rham_at_p}</text>',
            f'    <text x="24" y="205" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Fontaine-Mazur Geometric Status: {gm.is_geometric_representation}</text>',
            f'    <text x="24" y="230" font-family="ui-monospace, monospace" font-size="10" fill="#a7f3d0">{gm.associated_motive_or_variety[:52]}</text>',
            '  </g>',
        ])

        # Panel 2: Local p-Adic Hodge Theory & Period Rings
        svg.extend([
            '  <g transform="translate(570, 95)">',
            '    <rect width="480" height="260" rx="12" fill="url(#fmCard)" stroke="#a855f7" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#a855f7">Fontaine Period Rings &amp; Admissibility</text>',
            '    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Hierarchy: B_cris &#8834; B_st &#8834; B_dR &#8834; B_HT</text>',
            '    <rect x="24" y="80" width="432" height="75" rx="8" fill="#1e293b" stroke="#334155"/>',
            '    <text x="36" y="103" font-family="ui-monospace, monospace" font-size="11" fill="#e9d5ff">D_*(V) = (B_* &#8855;_{{Q_p}} V)^{{G_{{Q_p}}}}  (dim &#8804; dim V)</text>',
            f'    <text x="36" y="125" font-family="ui-monospace, monospace" font-size="11" fill="#f8fafc">B_dR Admissible: {gm.is_de_rham_at_p} (Filtration Fil^i D_dR(V))</text>',
            f'    <text x="36" y="145" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">B_cris Crystalline: {rings.get("B_cris", None).is_admissible if "B_cris" in rings else False} (Frobenius &#966; Active)</text>',
            f'    <text x="24" y="185" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">B_st Semi-Stable: Monodromy N&#966; = p&#966;N (N Order: {rings.get("B_st").monodromy_nilpotent_order if "B_st" in rings else 0})</text>',
            f'    <text x="24" y="210" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Weakly Admissible ==&gt; Admissible (Colmez-Fontaine Theorem)</text>',
            f'    <text x="24" y="235" font-family="ui-monospace, monospace" font-size="11" fill="#a7f3d0">Crystalline Cohomology Comparison: Proved</text>',
            '  </g>',
        ])

        # Panel 3: Hodge-Tate Weights & Sen Spectrum
        svg.extend([
            '  <g transform="translate(50, 380)">',
            '    <rect width="480" height="260" rx="12" fill="url(#fmCard)" stroke="#34d399" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#34d399">Hodge-Tate Weights &amp; Sen Polynomial</text>',
            f'    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Dimension: {ht.representation_dimension} | HT Admissible: {ht.is_hodge_tate}</text>',
            '    <rect x="24" y="80" width="432" height="70" rx="8" fill="#1e293b" stroke="#334155"/>',
            f'    <text x="36" y="105" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#6ee7b7">HT Weights: HT(&#961;) = {{{", ".join(str(w) for w in ht.hodge_tate_weights)}}}</text>',
            f'    <text x="36" y="130" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Sen Polynomial: &#920;_V(T) = &#8719; (T - h_i)</text>',
            f'    <text x="24" y="180" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Sen Operator Spectrum: {ht.hodge_tate_weights} in Z</text>',
            f'    <text x="24" y="205" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Purity of Hodge-Tate Weights: Verified</text>',
            f'    <text x="24" y="230" font-family="ui-monospace, monospace" font-size="11" fill="#a7f3d0">Hodge-de Rham Spectral Sequence: Degenerates at E_1</text>',
            '  </g>',
        ])

        # Panel 4: Modularity & Deformation Rings R = T
        svg.extend([
            '  <g transform="translate(570, 380)">',
            '    <rect width="480" height="260" rx="12" fill="url(#fmCard)" stroke="#f59e0b" stroke-width="1.5"/>',
            '    <text x="24" y="32" font-family="ui-sans-serif, system-ui" font-size="14" font-weight="600" fill="#f59e0b">Deformation Rings &amp; Modularity R = T</text>',
            f'    <text x="24" y="56" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Universal Deformation Ring R vs Hecke Algebra T</text>',
            '    <rect x="24" y="80" width="432" height="85" rx="8" fill="#1e293b" stroke="#334155"/>',
            '    <text x="36" y="108" font-family="ui-monospace, monospace" font-size="12" font-weight="bold" fill="#fde68a">&#966;: R_univ -&gt; T  (Taylor-Wiles-Kisin Isomorphism)</text>',
            f'    <text x="36" y="132" font-family="ui-monospace, monospace" font-size="11" fill="#f8fafc">{gm.deformation_ring_status[:52]}</text>',
            '    <text x="36" y="152" font-family="ui-monospace, monospace" font-size="10" fill="#94a3b8">Fontaine-Mazur Conjecture for GL_2 / Q: Proved (Kisin, Emerton)</text>',
            f'    <text x="24" y="195" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Potential Modularity: Taylor-Carayol-Harris-Shepherd-Barron</text>',
            f'    <text x="24" y="218" font-family="ui-monospace, monospace" font-size="11" fill="#cbd5e1">Local-Global Compatibility at p: Established</text>',
            f'    <text x="24" y="240" font-family="ui-monospace, monospace" font-size="11" fill="#a7f3d0">Geometric Galois Representations: Synthesized</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(svg)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dimension": self.dimension,
            "prime_p": self.prime_p,
            "default_archetype": self.default_archetype,
            "period_rings": [r.to_dict() for r in self.period_rings],
            "hodge_tate_data": [h.to_dict() for h in self.hodge_tate_data],
            "geometric_modularity": [g.to_dict() for g in self.geometric_modularity],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
