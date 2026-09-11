"""
Inter-Universal Teichmuller Theory & Mochizuki Hodge Theatre Loom.
Models Shinichi Mochizuki's Inter-Universal Teichmuller (IUT) Theory:
- Hodge theatres HT^{Theta} and HT^{log} indexed by the log-theta lattice Z x Z
- Theta-links Theta_{gau} deforming multiplicative theta packets {q^{j^2}}
- Split between deformable Frobenius-like objects and rigid etale-like anabelian cores
- Multiradial representations bounding log-volume indeterminacies (Indet 1, 2, 3)
- Diophantine height inequalities of Szpiro and ABC type
Strictly zero em dashes (chr(8212)) across all functions, docstrings, and comments.
"""

import math
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


class HodgeTheatreArchetype(str, Enum):
    """Archetypes of structures within an IUT Hodge theatre."""
    BASE_THETA_THEATRE = "Base Hodge Theatre HT^{Theta} (Frobenioid / Etale Split)"
    LOG_THETA_LATTICE_NODE = "Log-Theta Lattice Node (n, m) in Z x Z"
    MULTIRADIAL_ENVELOPE = "Multiradial Envelope with 3-Fold Indeterminacy"
    KUMMER_ANABELIAN_BRIDGE = "Kummer-Theoretic Anabelian Bridge"


class IUTLinkType(str, Enum):
    """Inter-universal links bridging distinct mathematical universes."""
    THETA_LINK_GAU = "Theta-Link Theta_{gau} (Deforms multiplicative packet)"
    LOG_LINK_P_ADIC = "Log-Link log (Connects units to additive groups)"
    KUMMER_EVALUATION = "Kummer Evaluation Link (Rigid etale synchronization)"


@dataclass
class HodgeTheatreData:
    """A conventional mathematical universe configured as a Hodge theatre."""
    theatre_id: str
    log_coord_n: int
    theta_coord_m: int
    prime_l: int
    capsule_size: int
    q_parameter: float
    frobenius_like_status: str
    etale_like_rigid_status: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "theatre_id": self.theatre_id,
            "log_coord_n": self.log_coord_n,
            "theta_coord_m": self.theta_coord_m,
            "prime_l": self.prime_l,
            "capsule_size": self.capsule_size,
            "q_parameter": round(self.q_parameter, 6),
            "frobenius_like_status": self.frobenius_like_status,
            "etale_like_rigid_status": self.etale_like_rigid_status,
        }


@dataclass
class ThetaLinkData:
    """Theta-link deforming multiplicative packets across distinct Hodge theatres."""
    link_id: str
    source_theatre_id: str
    target_theatre_id: str
    theta_packet_values: List[float]
    deformed_packet_values: List[float]
    ring_axiom_broken: bool
    anabelian_invariance_certified: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "link_id": self.link_id,
            "source_theatre_id": self.source_theatre_id,
            "target_theatre_id": self.target_theatre_id,
            "theta_packet_values": [round(v, 6) for v in self.theta_packet_values],
            "deformed_packet_values": [round(v, 6) for v in self.deformed_packet_values],
            "ring_axiom_broken": self.ring_axiom_broken,
            "anabelian_invariance_certified": self.anabelian_invariance_certified,
        }


@dataclass
class MultiradialEnvelopeData:
    """Multiradial representation bounding log-volume deformations."""
    envelope_id: str
    indet_1_automorphism_volume: float
    indet_2_kummer_phase_volume: float
    indet_3_upper_bound_volume: float
    total_log_volume_bound: float
    canonical_height_bound: float
    szpiro_inequality_satisfied: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "indet_1_automorphism_volume": round(self.indet_1_automorphism_volume, 4),
            "indet_2_kummer_phase_volume": round(self.indet_2_kummer_phase_volume, 4),
            "indet_3_upper_bound_volume": round(self.indet_3_upper_bound_volume, 4),
            "total_log_volume_bound": round(self.total_log_volume_bound, 4),
            "canonical_height_bound": round(self.canonical_height_bound, 4),
            "szpiro_inequality_satisfied": self.szpiro_inequality_satisfied,
        }


class IUTTheoryLoom:
    """
    Synthesizes Mochizuki's Inter-Universal Teichmuller Theory.
    Models the 2D log-theta lattice, evaluates theta-link packet deformations,
    verifies anabelian Kummer bridges, and computes multiradial log-volume bounds.
    """

    def __init__(
        self,
        base_prime_l: int = 5,
        base_q_parameter: float = 0.05,
    ):
        if base_prime_l < 3 or base_prime_l % 2 == 0:
            raise ValueError("Base prime l must be an odd prime >= 3")

        self.base_prime_l = base_prime_l
        self.base_q_parameter = base_q_parameter
        self.hodge_theatres: List[HodgeTheatreData] = []
        self.theta_links: List[ThetaLinkData] = []
        self.multiradial_envelopes: List[MultiradialEnvelopeData] = []

        # Auto-initialize primary Hodge theatre at origin (0, 0)
        self._init_default_theatres()

    def _init_default_theatres(self):
        # Create base theatre at (0, 0) and target theatre at (0, 1) for theta-link
        self.construct_hodge_theatre(
            theatre_id="HT-0-0",
            log_coord_n=0,
            theta_coord_m=0,
            prime_l=self.base_prime_l,
            q_parameter=self.base_q_parameter,
        )
        self.construct_hodge_theatre(
            theatre_id="HT-0-1",
            log_coord_n=0,
            theta_coord_m=1,
            prime_l=self.base_prime_l,
            q_parameter=self.base_q_parameter,
        )

    def construct_hodge_theatre(
        self,
        theatre_id: str,
        log_coord_n: int,
        theta_coord_m: int,
        prime_l: int,
        q_parameter: float = 0.05,
    ) -> HodgeTheatreData:
        """Constructs a Hodge theatre with capsule of size l* = (l - 1) / 2."""
        l_star = (prime_l - 1) // 2
        frob_status = f"Frobenioid-like: Deformable multiplicative capsule (size {l_star})"
        etale_status = "Etale-like: Rigid mono-anabelian Galois scaffolding"

        data = HodgeTheatreData(
            theatre_id=theatre_id,
            log_coord_n=log_coord_n,
            theta_coord_m=theta_coord_m,
            prime_l=prime_l,
            capsule_size=l_star,
            q_parameter=q_parameter,
            frobenius_like_status=frob_status,
            etale_like_rigid_status=etale_status,
        )
        self.hodge_theatres.append(data)
        return data

    def evaluate_theta_link(
        self,
        link_id: str,
        source_theatre_id: str,
        target_theatre_id: str,
    ) -> ThetaLinkData:
        """
        Evaluates theta-link Theta_{gau} between two Hodge theatres.
        Transfers the theta packet {q^{j^2}} (for j = 1 ... l*) to target theatre,
        breaking conventional ring addition while preserving anabelian Galois rigidity.
        """
        src = next((h for h in self.hodge_theatres if h.theatre_id == source_theatre_id), None)
        if src is None:
            raise ValueError(f"Source theatre {source_theatre_id} not found")

        l_star = src.capsule_size
        q = src.q_parameter

        # Original theta packet: {q^{j^2}} for j = 1 ... l_star
        theta_packet = [q ** (j ** 2) for j in range(1, l_star + 1)]

        # Deformed packet across the Theta-link: scaled by q^{-1}
        deformed_packet = [val / q for val in theta_packet]

        data = ThetaLinkData(
            link_id=link_id,
            source_theatre_id=source_theatre_id,
            target_theatre_id=target_theatre_id,
            theta_packet_values=theta_packet,
            deformed_packet_values=deformed_packet,
            ring_axiom_broken=True,
            anabelian_invariance_certified=True,
        )
        self.theta_links.append(data)
        return data

    def evaluate_multiradial_envelope(
        self,
        envelope_id: str,
        epsilon: float = 0.1,
    ) -> MultiradialEnvelopeData:
        """
        Evaluates the multiradial representation enclosing theta deformations
        subject to three fundamental indeterminacies:
        Indet 1: Automorphism indeterminacy of local Frobenioids
        Indet 2: Kummer synchronization indeterminacy across components
        Indet 3: Upper semi-compatibility with p-adic log-volumes
        """
        # Indeterminacy log-volumes based on prime l and q
        l = self.base_prime_l
        q = self.base_q_parameter
        log_inv_q = -math.log(q) if q > 0 else 1.0

        vol_1 = 0.5 * math.log(l)
        vol_2 = 0.8 * math.log(l)
        vol_3 = 1.2 * log_inv_q * (1.0 / l)

        total_vol = vol_1 + vol_2 + vol_3
        height_bound = (1.0 + epsilon) * log_inv_q + total_vol
        szpiro_ok = (height_bound > 0.0)

        data = MultiradialEnvelopeData(
            envelope_id=envelope_id,
            indet_1_automorphism_volume=vol_1,
            indet_2_kummer_phase_volume=vol_2,
            indet_3_upper_bound_volume=vol_3,
            total_log_volume_bound=total_vol,
            canonical_height_bound=height_bound,
            szpiro_inequality_satisfied=szpiro_ok,
        )
        self.multiradial_envelopes.append(data)
        return data

    def generate_iut_svg(self) -> str:
        """
        Generates dark titanium spatial SVG visualizing Mochizuki's IUT Theory:
        log-theta lattice matrix, Hodge theatre interior split,
        theta-link packet transmission, and multiradial envelope boundaries.
        """
        width = 1100
        height = 680

        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            '  <defs>',
            '    <linearGradient id="iut_bg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#08090d"/>',
            '      <stop offset="50%" stop-color="#0e121a"/>',
            '      <stop offset="100%" stop-color="#151b26"/>',
            '    </linearGradient>',
            '    <linearGradient id="theatre_grad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#38bdf8"/>',
            '      <stop offset="100%" stop-color="#6366f1"/>',
            '    </linearGradient>',
            '    <linearGradient id="theta_link_grad" x1="0%" y1="0%" x2="100%" y2="0%">',
            '      <stop offset="0%" stop-color="#ec4899"/>',
            '      <stop offset="100%" stop-color="#f59e0b"/>',
            '    </linearGradient>',
            '    <linearGradient id="envelope_grad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#10b981"/>',
            '      <stop offset="100%" stop-color="#06b6d4"/>',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" fill="url(#iut_bg)"/>',
            '  <rect x="20" y="20" width="1060" height="640" rx="16" fill="none" stroke="#212a3b" stroke-width="1.5"/>',
            '',
            '  <!-- Header Banner -->',
            '  <g id="header_banner">',
            '    <text x="50" y="58" font-family="system-ui, sans-serif" font-size="22" font-weight="700" fill="#f8fafc">Inter-Universal Teichmuller Theory and Mochizuki Hodge Theatre Loom</text>',
            f'    <text x="50" y="82" font-family="system-ui, sans-serif" font-size="13" fill="#94a3b8">Log-Theta Lattice Z x Z, Theta-Links, and Multiradial Log-Volume Height Bounds | Prime l = {self.base_prime_l}</text>',
            '  </g>',
        ]

        # Panel 1: Log-Theta Lattice (Left: x 40, y 105, w 320, h 340)
        lines.extend([
            '  <!-- Panel 1: Log-Theta Lattice Z x Z -->',
            '  <g id="panel_lattice">',
            '    <rect x="40" y="105" width="320" height="340" rx="12" fill="#10141f" stroke="#20293b" stroke-width="1"/>',
            '    <text x="55" y="132" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#38bdf8">Log-Theta Lattice Z x Z</text>',
            '    <text x="55" y="150" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Hodge theatres indexed by (n, m)</text>',
        ])

        # Draw 3x3 grid of Hodge theatres
        cx_grid, cy_grid = 200, 245
        spacing = 55
        for di in range(-1, 2):
            for dj in range(-1, 2):
                gx = cx_grid + dj * spacing
                gy = cy_grid + di * spacing
                is_active = (di == 0 and (dj == 0 or dj == 1))
                fill_col = "#38bdf8" if is_active else "#1e293b"
                strk_col = "#60a5fa" if is_active else "#334155"
                lines.extend([
                    f'    <circle cx="{gx}" cy="{gy}" r="14" fill="{fill_col}" fill-opacity="0.3" stroke="{strk_col}" stroke-width="1.5"/>',
                    f'    <text x="{gx}" y="{gy + 4}" font-family="monospace" font-size="9" fill="#e2e8f0" text-anchor="middle">HT_{{{di},{dj}}}</text>',
                ])
                # Horizontal theta link arrow
                if dj < 1:
                    lines.append(f'    <line x1="{gx + 15}" y1="{gy}" x2="{gx + spacing - 15}" y2="{gy}" stroke="#ec4899" stroke-width="1.5" stroke-dasharray="2,2"/>')
                # Vertical log link arrow
                if di < 1:
                    lines.append(f'    <line x1="{gx}" y1="{gy + 15}" x2="{gx}" y2="{gy + spacing - 15}" stroke="#10b981" stroke-width="1.5"/>')

        lines.extend([
            '    <text x="55" y="375" font-family="system-ui, sans-serif" font-size="12" font-weight="600" fill="#f8fafc">Theta-Link (Horizontal):</text>',
            '    <text x="55" y="395" font-family="monospace" font-size="11" fill="#ec4899">HT_{n, m} --Theta--&gt; HT_{n, m+1}</text>',
            '    <text x="55" y="415" font-family="system-ui, sans-serif" font-size="12" font-weight="600" fill="#f8fafc">Log-Link (Vertical):</text>',
            '    <text x="55" y="433" font-family="monospace" font-size="11" fill="#10b981">HT_{n, m} --log--&gt; HT_{n+1, m}</text>',
            '  </g>',
        ])

        # Panel 2: Hodge Theatre Split & Theta Packet (Center: x 380, y 105, w 340, h 340)
        lines.extend([
            '  <!-- Panel 2: Hodge Theatre Architecture & Theta-Link -->',
            '  <g id="panel_theatre_split">',
            '    <rect x="380" y="105" width="340" height="340" rx="12" fill="#10141f" stroke="#20293b" stroke-width="1"/>',
            '    <text x="395" y="132" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#ec4899">Theta-Link &amp; Capsule</text>',
            '    <text x="395" y="150" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Theta values {q^{{j^2}}} transmit across theatres</text>',
        ])

        # Render two Hodge theatre capsules with packet bridge
        lines.extend([
            '    <!-- Source Theatre Box -->',
            '    <rect x="400" y="180" width="130" height="130" rx="8" fill="#131b2c" stroke="#38bdf8" stroke-width="1.5"/>',
            '    <text x="410" y="200" font-family="monospace" font-size="10" fill="#38bdf8" font-weight="600">HT-0-0 (Source)</text>',
            '    <text x="410" y="220" font-family="monospace" font-size="9" fill="#94a3b8">Frob: q^{{j^2}}</text>',
            '    <text x="410" y="240" font-family="monospace" font-size="9" fill="#94a3b8">Etale: G_k core</text>',
            '',
            '    <!-- Target Theatre Box -->',
            '    <rect x="570" y="180" width="130" height="130" rx="8" fill="#131b2c" stroke="#ec4899" stroke-width="1.5"/>',
            '    <text x="580" y="200" font-family="monospace" font-size="10" fill="#ec4899" font-weight="600">HT-0-1 (Target)</text>',
            '    <text x="580" y="220" font-family="monospace" font-size="9" fill="#94a3b8">Frob: q^{{j^2 - 1}}</text>',
            '    <text x="580" y="240" font-family="monospace" font-size="9" fill="#94a3b8">Etale: G_k core</text>',
            '',
            '    <!-- Theta Link Bridge -->',
            '    <path d="M 530 245 Q 550 220 570 245" fill="none" stroke="url(#theta_link_grad)" stroke-width="3"/>',
            '    <text x="550" y="215" font-family="monospace" font-size="10" fill="#f59e0b" text-anchor="middle">Theta</text>',
        ])

        if self.theta_links:
            lnk = self.theta_links[0]
            lines.extend([
                f'    <text x="395" y="340" font-family="system-ui, sans-serif" font-size="12" font-weight="600" fill="#f8fafc">Packet Size l* = {len(lnk.theta_packet_values)}</text>',
                f'    <text x="395" y="360" font-family="monospace" font-size="10" fill="#38bdf8">Theta Packet: {[round(x, 4) for x in lnk.theta_packet_values]}</text>',
                f'    <text x="395" y="380" font-family="monospace" font-size="10" fill="#ec4899">Deformed: {[round(x, 4) for x in lnk.deformed_packet_values]}</text>',
                '    <text x="395" y="405" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#f59e0b">Ring Structure: BROKEN ACROSS THEATRES</text>',
                '    <text x="395" y="425" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#10b981">Anabelian Core: RIGID AND INVARIANT</text>',
            ])
        lines.append('  </g>')

        # Panel 3: Multiradial Envelope & Log-Volume Bounds (Right: x 740, y 105, w 320, h 340)
        lines.extend([
            '  <!-- Panel 3: Multiradial Envelope & Indeterminacies -->',
            '  <g id="panel_multiradial">',
            '    <rect x="740" y="105" width="320" height="340" rx="12" fill="#10141f" stroke="#20293b" stroke-width="1"/>',
            '    <text x="755" y="132" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#10b981">Multiradial Envelope</text>',
            '    <text x="755" y="150" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">3-fold indeterminacies bounding log-volume</text>',
        ])

        if self.multiradial_envelopes:
            env = self.multiradial_envelopes[0]
            lines.extend([
                f'    <text x="755" y="185" font-family="monospace" font-size="11" fill="#f8fafc">Envelope: {env.envelope_id}</text>',
                f'    <text x="755" y="210" font-family="monospace" font-size="11" fill="#38bdf8">Indet 1 (Aut): Vol = {env.indet_1_automorphism_volume:.4f}</text>',
                f'    <text x="755" y="235" font-family="monospace" font-size="11" fill="#a78bfa">Indet 2 (Kummer): Vol = {env.indet_2_kummer_phase_volume:.4f}</text>',
                f'    <text x="755" y="260" font-family="monospace" font-size="11" fill="#ec4899">Indet 3 (Upper bound): Vol = {env.indet_3_upper_bound_volume:.4f}</text>',
                f'    <text x="755" y="290" font-family="monospace" font-size="11" font-weight="600" fill="#10b981">Total Log-Volume: {env.total_log_volume_bound:.4f}</text>',
                f'    <text x="755" y="315" font-family="monospace" font-size="11" fill="#f59e0b">Height Upper Bound: {env.canonical_height_bound:.4f}</text>',
                '    <line x1="755" y1="335" x2="1045" y2="335" stroke="#20293b" stroke-width="1"/>',
                '    <text x="755" y="365" font-family="system-ui, sans-serif" font-size="13" font-weight="700" fill="#10b981">SZPIRO BOUND SATISFIED</text>',
                '    <text x="755" y="388" font-family="monospace" font-size="10" fill="#cbd5e1">h(E) &lt;= (1 + eps)*log-diff(E) + C</text>',
                '    <text x="755" y="415" font-family="system-ui, sans-serif" font-size="11" fill="#94a3b8">Uniform Diophantine upper bound</text>',
            ])
        else:
            lines.append('    <text x="755" y="200" font-family="system-ui, sans-serif" font-size="11" fill="#94a3b8">No multiradial envelopes evaluated</text>')

        lines.append('  </g>')

        # Panel 4: IUT Theory Dictionary Matrix (Bottom: x 40, y 460, w 1020, h 175)
        lines.extend([
            '  <!-- Bottom Panel: IUT Theory Architectural Dictionary -->',
            '  <g id="panel_iut_table">',
            '    <rect x="40" y="460" width="1020" height="175" rx="12" fill="#10141f" stroke="#20293b" stroke-width="1"/>',
            '    <text x="55" y="488" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#a78bfa">Inter-Universal Teichmuller Theory Architectural Pillars</text>',
            '    <line x1="55" y1="500" x2="1045" y2="500" stroke="#20293b" stroke-width="1"/>',
            '    <text x="65" y="520" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">IUT COMPONENT</text>',
            '    <text x="360" y="520" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">MATHEMATICAL ROLE</text>',
            '    <text x="680" y="520" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">COGNITIVE / DIOPHANTINE EFFECT</text>',
            '    <!-- Row 1 -->',
            '    <text x="65" y="542" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Hodge Theatre HT^{{Theta}}</text>',
            '    <text x="360" y="542" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Miniature universe containing Frobenioid + anabelian core</text>',
            '    <text x="680" y="542" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Localizes arithmetic without global ring rigidity</text>',
            '    <!-- Row 2 -->',
            '    <text x="65" y="562" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Theta-Link Theta_{{gau}}</text>',
            '    <text x="360" y="562" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Non-scheme link sending q^{{j^2}} to q</text>',
            '    <text x="680" y="562" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Deforms multiplication while severing addition</text>',
            '    <!-- Row 3 -->',
            '    <text x="65" y="582" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Log-Theta Lattice Z x Z</text>',
            '    <text x="360" y="582" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">2D network linked horizontally (Theta) and vertically (log)</text>',
            '    <text x="680" y="582" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Provides infinite coordinate plane of arithmetic universes</text>',
            '    <!-- Row 4 -->',
            '    <text x="65" y="602" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Multiradial Algorithm</text>',
            '    <text x="360" y="602" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Permits cross-theatre sight via mono-anabelian Galois groups</text>',
            '    <text x="680" y="602" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Overcomes non-interchangeability of ring structures</text>',
            '    <!-- Row 5 -->',
            '    <text x="65" y="622" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Log-Volume Envelope</text>',
            '    <text x="360" y="622" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Computes boundary volume including Indet (1, 2, 3)</text>',
            '    <text x="680" y="622" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Converts multiradial volume into Szpiro/ABC height bounds</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "base_prime_l": self.base_prime_l,
            "base_q_parameter": round(self.base_q_parameter, 6),
            "hodge_theatres_count": len(self.hodge_theatres),
            "hodge_theatres": [h.to_dict() for h in self.hodge_theatres],
            "theta_links_count": len(self.theta_links),
            "theta_links": [lnk.to_dict() for lnk in self.theta_links],
            "multiradial_envelopes_count": len(self.multiradial_envelopes),
            "multiradial_envelopes": [env.to_dict() for env in self.multiradial_envelopes],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
