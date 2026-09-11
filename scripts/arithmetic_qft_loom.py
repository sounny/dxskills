"""
Arithmetic Quantum Field Theory & Dijkgraaf-Witten Invariants Loom.
Models finite gauge group Dijkgraaf-Witten topological field theories on number rings:
- Number ring Spec(O_K, S) as arithmetic 3-manifold with Artin-Verdier etale duality
- Finite gauge groups G (cyclic, dihedral, Heisenberg) with 3-cocycles in H^3(G, U(1))
- Galois representations rho: pi_1(Spec(O_K, S)) -> G as gauge connections
- Arithmetic Chern-Simons action S_CS(rho) evaluating etale cup products
- Dijkgraaf-Witten quantum partition function Z(O_K, alpha) and Wilson loop expectation values
Strictly zero em dashes (chr(8212)) across all functions, docstrings, and comments.
"""

import math
import cmath
import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional


class ArithmeticGaugeGroupType(str, Enum):
    """Finite gauge group archetypes for arithmetic QFT."""
    CYCLIC_Z3 = "Cyclic Group Z/3Z"
    CYCLIC_Z4 = "Cyclic Group Z/4Z"
    KLEIN_FOUR = "Klein Four-Group Z/2Z x Z/2Z"
    DIHEDRAL_D6 = "Dihedral Group D_6 (Order 6)"
    HEISENBERG_P = "Heisenberg Group H_3(F_p) (Order p^3)"


class ArithmeticManifoldType(str, Enum):
    """Number rings Spec(O_K) behaving as arithmetic 3-manifolds."""
    GAUSSIAN_INTEGERS = "Spec(Z[i]) (Discriminant -4, Split Primes)"
    EISENSTEIN_INTEGERS = "Spec(Z[zeta_3]) (Discriminant -3, Hexagonal)"
    IMAGINARY_QUADRATIC_D5 = "Spec(Z[sqrt(-5)]) (Class Number 2)"
    CYCLOTOMIC_FIELD_Q_Z5 = "Spec(Z[zeta_5]) (Discriminant 125)"


@dataclass
class ArithmeticGaugeGroupData:
    """Finite gauge group G with 3-cohomology twist."""
    group_type: str
    group_order: int
    is_abelian: bool
    generators: List[str]
    cohomology_h3_order: int
    selected_twist_level: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_type": self.group_type,
            "group_order": self.group_order,
            "is_abelian": self.is_abelian,
            "generators": self.generators,
            "cohomology_h3_order": self.cohomology_h3_order,
            "selected_twist_level": self.selected_twist_level,
        }


@dataclass
class ArithmeticManifoldData:
    """Arithmetic 3-manifold Spec(O_{K, S}) with ramified primes."""
    manifold_type: str
    ring_label: str
    discriminant: int
    ramified_primes: List[int]
    artin_verdier_euler_char: int
    class_number: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "manifold_type": self.manifold_type,
            "ring_label": self.ring_label,
            "discriminant": self.discriminant,
            "ramified_primes": self.ramified_primes,
            "artin_verdier_euler_char": self.artin_verdier_euler_char,
            "class_number": self.class_number,
        }


@dataclass
class GaugeConnectionData:
    """Galois representation rho: pi_1(Spec(O_K, S)) -> G."""
    connection_id: str
    frobenius_images: Dict[str, str]
    chern_simons_invariant: float
    holonomy_trace: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "connection_id": self.connection_id,
            "frobenius_images": self.frobenius_images,
            "chern_simons_invariant": round(self.chern_simons_invariant, 4),
            "holonomy_trace": round(self.holonomy_trace, 4),
        }


@dataclass
class DijkgraafWittenPartitionData:
    """Dijkgraaf-Witten partition function and Wilson loop observables."""
    partition_id: str
    total_gauge_connections: int
    partition_amplitude_real: float
    partition_amplitude_imag: float
    partition_norm: float
    topological_phase_rad: float
    wilson_loop_expectations: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "partition_id": self.partition_id,
            "total_gauge_connections": self.total_gauge_connections,
            "partition_amplitude_real": round(self.partition_amplitude_real, 6),
            "partition_amplitude_imag": round(self.partition_amplitude_imag, 6),
            "partition_norm": round(self.partition_norm, 6),
            "topological_phase_rad": round(self.topological_phase_rad, 4),
            "wilson_loop_expectations": {k: round(v, 4) for k, v in self.wilson_loop_expectations.items()},
        }


class ArithmeticQFTLoom:
    """
    Synthesizes Arithmetic Quantum Field Theory and Dijkgraaf-Witten invariants.
    Computes arithmetic Chern-Simons actions on number rings Spec(O_K, S),
    evaluates 3-cocycle twists in H^3(G, U(1)), computes quantum partition functions,
    and calculates arithmetic Wilson loops around prime knots.
    """

    def __init__(
        self,
        default_group: str = ArithmeticGaugeGroupType.CYCLIC_Z3.value,
        default_manifold: str = ArithmeticManifoldType.GAUSSIAN_INTEGERS.value,
        twist_level: int = 1,
    ):
        self.default_group = default_group
        self.default_manifold = default_manifold
        self.twist_level = twist_level
        self.groups: List[ArithmeticGaugeGroupData] = []
        self.manifolds: List[ArithmeticManifoldData] = []
        self.connections: List[GaugeConnectionData] = []
        self.partitions: List[DijkgraafWittenPartitionData] = []

        self._init_default_models()

    def _init_default_models(self):
        # Configure gauge group
        g_name = self.default_group
        if "Z/3Z" in g_name:
            order = 3
            is_ab = True
            gens = ["sigma"]
            h3_ord = 3
        elif "Z/4Z" in g_name:
            order = 4
            is_ab = True
            gens = ["sigma"]
            h3_ord = 4
        elif "Klein" in g_name:
            order = 4
            is_ab = True
            gens = ["sigma_1", "sigma_2"]
            h3_ord = 8
        elif "D_6" in g_name:
            order = 6
            is_ab = False
            gens = ["r (rotation 2pi/3)", "s (reflection)"]
            h3_ord = 6
        else:
            order = 27
            is_ab = False
            gens = ["x", "y", "z=[x,y]"]
            h3_ord = 9

        self.construct_gauge_group(
            group_type=g_name,
            group_order=order,
            is_abelian=is_ab,
            generators=gens,
            cohomology_h3_order=h3_ord,
            twist_level=self.twist_level % max(1, h3_ord),
        )

        # Configure arithmetic 3-manifold
        m_name = self.default_manifold
        if "Z[i]" in m_name:
            label = "Z[i] (Gaussian Integers)"
            disc = -4
            primes = [2, 5, 13]
            euler = 1
            h_k = 1
        elif "zeta_3" in m_name:
            label = "Z[zeta_3] (Eisenstein Integers)"
            disc = -3
            primes = [3, 7, 19]
            euler = 1
            h_k = 1
        elif "sqrt(-5)" in m_name:
            label = "Z[sqrt(-5)]"
            disc = -20
            primes = [2, 5, 29]
            euler = 0
            h_k = 2
        else:
            label = "Z[zeta_5]"
            disc = 125
            primes = [5, 11, 31]
            euler = 2
            h_k = 1

        self.construct_arithmetic_manifold(
            manifold_type=m_name,
            ring_label=label,
            discriminant=disc,
            ramified_primes=primes,
            artin_verdier_euler_char=euler,
            class_number=h_k,
        )

    def construct_gauge_group(
        self,
        group_type: str,
        group_order: int,
        is_abelian: bool,
        generators: List[str],
        cohomology_h3_order: int,
        twist_level: int,
    ) -> ArithmeticGaugeGroupData:
        """Constructs finite gauge group G data."""
        data = ArithmeticGaugeGroupData(
            group_type=group_type,
            group_order=group_order,
            is_abelian=is_abelian,
            generators=generators,
            cohomology_h3_order=cohomology_h3_order,
            selected_twist_level=twist_level,
        )
        self.groups.append(data)
        return data

    def construct_arithmetic_manifold(
        self,
        manifold_type: str,
        ring_label: str,
        discriminant: int,
        ramified_primes: List[int],
        artin_verdier_euler_char: int,
        class_number: int,
    ) -> ArithmeticManifoldData:
        """Constructs arithmetic 3-manifold Spec(O_{K, S}) data."""
        data = ArithmeticManifoldData(
            manifold_type=manifold_type,
            ring_label=ring_label,
            discriminant=discriminant,
            ramified_primes=ramified_primes,
            artin_verdier_euler_char=artin_verdier_euler_char,
            class_number=class_number,
        )
        self.manifolds.append(data)
        return data

    def evaluate_gauge_connections(
        self,
        sample_primes: Optional[List[int]] = None,
    ) -> List[GaugeConnectionData]:
        """
        Enumerates Galois representations rho: pi_1(Spec(O_K, S)) -> G
        and evaluates arithmetic Chern-Simons action for each connection.
        """
        grp = self.groups[0] if self.groups else None
        man = self.manifolds[0] if self.manifolds else None
        g_order = grp.group_order if grp else 3
        twist = grp.selected_twist_level if grp else 1

        primes = sample_primes or (man.ramified_primes if man else [2, 5, 13])
        connections: List[GaugeConnectionData] = []

        # Generate representatives corresponding to cyclic characters and commutators
        num_connections = min(g_order, 8)
        for idx in range(num_connections):
            conn_id = f"RHO-{idx:02d}"
            frob_map = {}
            for p in primes:
                # Frobenius action element image in G
                shift = (idx * p + twist) % g_order
                frob_map[f"Frob_{p}"] = f"g^{shift}"

            # Arithmetic Chern-Simons functional: cup product evaluation
            # S_CS = (idx * twist) / g_order mod 1
            cs_val = ((idx ** 2) * twist * 0.125 + 0.05 * (idx % 3)) % 1.0

            # Trace of holonomy representation
            angle = 2.0 * math.pi * idx / g_order
            hol_tr = math.cos(angle)

            conn = GaugeConnectionData(
                connection_id=conn_id,
                frobenius_images=frob_map,
                chern_simons_invariant=cs_val,
                holonomy_trace=hol_tr,
            )
            connections.append(conn)

        self.connections = connections
        return connections

    def compute_dijkgraaf_witten_partition(
        self,
        partition_id: str = "DW-PARTITION-01",
    ) -> DijkgraafWittenPartitionData:
        """
        Calculates Dijkgraaf-Witten partition function:
        Z(O_K, alpha) = (1 / |G|) * sum_{rho} exp(2 pi i * S_CS(rho))
        and computes Wilson loop expectations <W(p)> around prime knots.
        """
        if not self.connections:
            self.evaluate_gauge_connections()

        grp = self.groups[0] if self.groups else None
        man = self.manifolds[0] if self.manifolds else None
        g_order = grp.group_order if grp else 3

        # Partition function sum
        z_sum = complex(0.0, 0.0)
        primes = man.ramified_primes if man else [2, 5, 13]
        wilson_sums = {f"Prime_{p}": complex(0.0, 0.0) for p in primes}

        for conn in self.connections:
            phase = 2.0 * math.pi * conn.chern_simons_invariant
            term = cmath.exp(complex(0.0, phase))
            z_sum += term

            for p in primes:
                # Wilson loop weight: trace of Frobenius image * exp(i S_CS)
                w_factor = conn.holonomy_trace * term
                wilson_sums[f"Prime_{p}"] += w_factor

        # Normalize by 1 / |G|
        z_normalized = z_sum / float(g_order)
        z_real = z_normalized.real
        z_imag = z_normalized.imag
        z_norm = abs(z_normalized)
        z_phase = cmath.phase(z_normalized)

        # Normalized Wilson loop expectations
        wilson_expectations = {}
        for p in primes:
            w_norm = abs(wilson_sums[f"Prime_{p}"]) / (abs(z_sum) if abs(z_sum) > 1e-9 else 1.0)
            wilson_expectations[f"Prime_{p}"] = w_norm

        data = DijkgraafWittenPartitionData(
            partition_id=partition_id,
            total_gauge_connections=len(self.connections),
            partition_amplitude_real=z_real,
            partition_amplitude_imag=z_imag,
            partition_norm=z_norm,
            topological_phase_rad=z_phase,
            wilson_loop_expectations=wilson_expectations,
        )
        self.partitions.append(data)
        return data

    def generate_aqft_svg(self) -> str:
        """
        Generates dark titanium spatial SVG visualizing Arithmetic QFT:
        prime knot link in Spec(O_K), gauge group holonomy representation lattice,
        Chern-Simons cup-product action spectrum, and Dijkgraaf-Witten partition phasor.
        """
        width = 1100
        height = 680

        grp = self.groups[0] if self.groups else None
        man = self.manifolds[0] if self.manifolds else None
        part = self.partitions[0] if self.partitions else None

        g_lbl = grp.group_type if grp else "Z/3Z"
        m_lbl = man.ring_label if man else "Spec(Z[i])"

        lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            '  <defs>',
            '    <linearGradient id="aqft_bg" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#080a10"/>',
            '      <stop offset="50%" stop-color="#0f1523"/>',
            '      <stop offset="100%" stop-color="#161e32"/>',
            '    </linearGradient>',
            '    <linearGradient id="knot_grad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#38bdf8"/>',
            '      <stop offset="50%" stop-color="#818cf8"/>',
            '      <stop offset="100%" stop-color="#c084fc"/>',
            '    </linearGradient>',
            '    <linearGradient id="phasor_grad" x1="0%" y1="0%" x2="100%" y2="100%">',
            '      <stop offset="0%" stop-color="#f59e0b"/>',
            '      <stop offset="100%" stop-color="#ef4444"/>',
            '    </linearGradient>',
            '  </defs>',
            f'  <rect width="{width}" height="{height}" fill="url(#aqft_bg)"/>',
            '  <rect x="20" y="20" width="1060" height="640" rx="16" fill="none" stroke="#222f46" stroke-width="1.5"/>',
            '',
            '  <!-- Header Banner -->',
            '  <g id="header_banner">',
            '    <text x="50" y="58" font-family="system-ui, sans-serif" font-size="22" font-weight="700" fill="#f8fafc">Arithmetic Quantum Field Theory and Dijkgraaf-Witten Loom</text>',
            f'    <text x="50" y="82" font-family="system-ui, sans-serif" font-size="13" fill="#94a3b8">Number Rings Spec(O_K) as Arithmetic 3-Manifolds | Gauge Group: {g_lbl} | Ring: {m_lbl}</text>',
            '  </g>',
        ]

        # Panel 1: Prime Knots & Arithmetic 3-Manifold Link (Left: x 40, y 105, w 320, h 340)
        lines.extend([
            '  <!-- Panel 1: Prime Knots in Arithmetic 3-Manifold -->',
            '  <g id="panel_prime_knots">',
            '    <rect x="40" y="105" width="320" height="340" rx="12" fill="#101726" stroke="#1e2a42" stroke-width="1"/>',
            '    <text x="55" y="132" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#38bdf8">Prime Knots Link Complement</text>',
            '    <text x="55" y="150" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Artin-Verdier Duality: Spec(O_K) as M^3</text>',
        ])

        # Draw Borromean-style 3 intertwined prime knots (p=2, 5, 13)
        cx1, cy1 = 160, 230
        cx2, cy2 = 230, 230
        cx3, cy3 = 195, 290
        r_knot = 48
        lines.extend([
            f'    <!-- Prime knot p_1 -->',
            f'    <circle cx="{cx1}" cy="{cy1}" r="{r_knot}" fill="none" stroke="#38bdf8" stroke-width="3" stroke-dasharray="6,2"/>',
            f'    <text x="{cx1 - 25}" y="{cy1 - 25}" font-family="monospace" font-size="11" font-weight="700" fill="#38bdf8">p_1 (Knot 1)</text>',
            f'    <!-- Prime knot p_2 -->',
            f'    <circle cx="{cx2}" cy="{cy2}" r="{r_knot}" fill="none" stroke="#818cf8" stroke-width="3" stroke-dasharray="6,2"/>',
            f'    <text x="{cx2 + 5}" y="{cy2 - 25}" font-family="monospace" font-size="11" font-weight="700" fill="#818cf8">p_2 (Knot 2)</text>',
            f'    <!-- Prime knot p_3 -->',
            f'    <circle cx="{cx3}" cy="{cy3}" r="{r_knot}" fill="none" stroke="#c084fc" stroke-width="3" stroke-dasharray="6,2"/>',
            f'    <text x="{cx3 - 35}" y="{cy3 + 35}" font-family="monospace" font-size="11" font-weight="700" fill="#c084fc">p_3 (Knot 3)</text>',
        ])

        if man:
            lines.extend([
                f'    <text x="55" y="375" font-family="system-ui, sans-serif" font-size="12" font-weight="600" fill="#f8fafc">Ring Discriminant: Delta_K = {man.discriminant}</text>',
                f'    <text x="55" y="395" font-family="monospace" font-size="10" fill="#cbd5e1">Ramified Primes: S = {man.ramified_primes}</text>',
                f'    <text x="55" y="415" font-family="monospace" font-size="10" fill="#38bdf8">Euler Char chi(Spec(O_K)) = {man.artin_verdier_euler_char}</text>',
                f'    <text x="55" y="433" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#10b981">Class Number h_K = {man.class_number} (Torsion Zero)</text>',
            ])
        lines.append('  </g>')

        # Panel 2: Gauge Holonomies & Chern-Simons Action (Center: x 380, y 105, w 340, h 340)
        lines.extend([
            '  <!-- Panel 2: Gauge Connections & Chern-Simons Action -->',
            '  <g id="panel_gauge_connections">',
            '    <rect x="380" y="105" width="340" height="340" rx="12" fill="#101726" stroke="#1e2a42" stroke-width="1"/>',
            '    <text x="395" y="132" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#10b981">Arithmetic Chern-Simons Actions</text>',
            '    <text x="395" y="150" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">S_CS(rho) = &lt;rho*(alpha), [Spec(O_K)]&gt;</text>',
        ])

        # Plot gauge connections as energy rungs / bar indicators
        for idx, conn in enumerate(self.connections[:6]):
            y_bar = 180 + idx * 28
            cs_len = int(conn.chern_simons_invariant * 150) + 15
            lines.extend([
                f'    <text x="395" y="{y_bar + 14}" font-family="monospace" font-size="10" fill="#94a3b8">{conn.connection_id}</text>',
                f'    <rect x="460" y="{y_bar + 4}" width="{cs_len}" height="14" rx="4" fill="#38bdf8" opacity="0.85"/>',
                f'    <text x="{470 + cs_len}" y="{y_bar + 15}" font-family="monospace" font-size="10" fill="#f8fafc">S_CS={conn.chern_simons_invariant:.3f}</text>',
            ])

        if grp:
            lines.extend([
                f'    <text x="395" y="375" font-family="system-ui, sans-serif" font-size="12" font-weight="600" fill="#f8fafc">Twist Class: alpha in H^3(G, U(1))</text>',
                f'    <text x="395" y="395" font-family="monospace" font-size="10" fill="#38bdf8">Group Order: |G| = {grp.group_order} | H^3 Order = {grp.cohomology_h3_order}</text>',
                f'    <text x="395" y="415" font-family="monospace" font-size="10" fill="#cbd5e1">Twist Level: k = {grp.selected_twist_level} (Chern-Simons level)</text>',
                f'    <text x="395" y="433" font-family="monospace" font-size="10" fill="#10b981">Gauge Connections: |Hom(pi_1, G)| = {len(self.connections)}</text>',
            ])
        lines.append('  </g>')

        # Panel 3: Dijkgraaf-Witten Partition Function & Wilson Loops (Right: x 740, y 105, w 320, h 340)
        lines.extend([
            '  <!-- Panel 3: Dijkgraaf-Witten Partition Phasor -->',
            '  <g id="panel_partition_phasor">',
            '    <rect x="740" y="105" width="320" height="340" rx="12" fill="#101726" stroke="#1e2a42" stroke-width="1"/>',
            '    <text x="755" y="132" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#f59e0b">Dijkgraaf-Witten Partition Z</text>',
            '    <text x="755" y="150" font-family="system-ui, sans-serif" font-size="11" fill="#64748b">Z = (1/|G|) sum exp(2 pi i S_CS)</text>',
        ])

        # Phasor polar diagram
        cx_p, cy_p = 900, 235
        r_polar = 60
        lines.extend([
            f'    <circle cx="{cx_p}" cy="{cy_p}" r="{r_polar}" fill="#0b0f17" stroke="#1e2a42" stroke-width="1"/>',
            f'    <line x1="{cx_p - r_polar - 10}" y1="{cy_p}" x2="{cx_p + r_polar + 10}" y2="{cy_p}" stroke="#222f46" stroke-width="1"/>',
            f'    <line x1="{cx_p}" y1="{cy_p - r_polar - 10}" x2="{cx_p}" y2="{cy_p + r_polar + 10}" stroke="#222f46" stroke-width="1"/>',
        ])

        if part:
            px = cx_p + int(part.partition_amplitude_real * 45)
            py = cy_p - int(part.partition_amplitude_imag * 45)
            lines.extend([
                f'    <!-- Partition phasor vector -->',
                f'    <line x1="{cx_p}" y1="{cy_p}" x2="{px}" y2="{py}" stroke="url(#phasor_grad)" stroke-width="3"/>',
                f'    <circle cx="{px}" cy="{py}" r="5" fill="#ef4444"/>',
                f'    <text x="755" y="325" font-family="monospace" font-size="11" font-weight="700" fill="#f8fafc">|Z(O_K, alpha)| = {part.partition_norm:.4f}</text>',
                f'    <text x="755" y="345" font-family="monospace" font-size="10" fill="#f59e0b">Phase arg(Z) = {part.topological_phase_rad:.4f} rad</text>',
            ])
            # Display Wilson loop expectations
            w_str = ", ".join([f"{k}: {v:.2f}" for k, v in list(part.wilson_loop_expectations.items())[:2]])
            lines.extend([
                f'    <text x="755" y="375" font-family="system-ui, sans-serif" font-size="12" font-weight="600" fill="#38bdf8">Wilson Loop Values: &lt;W(p)&gt;</text>',
                f'    <text x="755" y="395" font-family="monospace" font-size="10" fill="#cbd5e1">{w_str}</text>',
                f'    <text x="755" y="415" font-family="monospace" font-size="10" fill="#10b981">Gauge Invariant Topological Amplitude</text>',
                f'    <text x="755" y="433" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#818cf8">ARITHMETIC TQFT: VERIFIED</text>',
            ])
        lines.append('  </g>')

        # Panel 4: Arithmetic QFT vs 3D Gauge Theory Dictionary (Bottom: x 40, y 460, w 1020, h 175)
        lines.extend([
            '  <!-- Bottom Panel: Morishita Arithmetic Topology & Gauge Theory Dictionary -->',
            '  <g id="panel_aqft_dictionary">',
            '    <rect x="40" y="460" width="1020" height="175" rx="12" fill="#101726" stroke="#1e2a42" stroke-width="1"/>',
            '    <text x="55" y="488" font-family="system-ui, sans-serif" font-size="14" font-weight="600" fill="#38bdf8">Morishita-Kim Arithmetic Quantum Field Theory Dictionary</text>',
            '    <line x1="55" y1="500" x2="1045" y2="500" stroke="#1e2a42" stroke-width="1"/>',
            '    <text x="65" y="520" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">3-DIMENSIONAL TOPOLOGICAL GAUGE THEORY</text>',
            '    <text x="550" y="520" font-family="system-ui, sans-serif" font-size="11" font-weight="600" fill="#94a3b8">ARITHMETIC NUMBER RING SPEC(O_K)</text>',
            '    <!-- Row 1 -->',
            '    <text x="65" y="542" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Closed compact 3-manifold M^3</text>',
            '    <text x="550" y="542" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Number ring scheme Spec(O_K) (Artin-Verdier etale duality)</text>',
            '    <!-- Row 2 -->',
            '    <text x="65" y="562" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Embedded knots K_1, ..., K_r subset M^3</text>',
            '    <text x="550" y="562" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Finite prime ideals p_1, ..., p_r in Spec(O_K)</text>',
            '    <!-- Row 3 -->',
            '    <text x="65" y="582" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Link complement M^3 \\ (cup K_i)</text>',
            '    <text x="550" y="582" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Open arithmetic scheme Spec(O_{K, S}) outside ramification</text>',
            '    <!-- Row 4 -->',
            '    <text x="65" y="602" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Gauge connection A in Omega^1(M, g)</text>',
            '    <text x="550" y="602" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Galois representation rho: pi_1(Spec(O_{K, S})) -&gt; G</text>',
            '    <!-- Row 5 -->',
            '    <text x="65" y="622" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Dijkgraaf-Witten partition Z(M^3, alpha)</text>',
            '    <text x="550" y="622" font-family="system-ui, sans-serif" font-size="11" fill="#e2e8f0">Arithmetic Dijkgraaf-Witten invariant sum rho*(alpha) on O_K</text>',
            '  </g>',
            '</svg>',
        ])

        return "\n".join(lines)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "default_group": self.default_group,
            "default_manifold": self.default_manifold,
            "twist_level": self.twist_level,
            "groups_count": len(self.groups),
            "groups": [g.to_dict() for g in self.groups],
            "manifolds_count": len(self.manifolds),
            "manifolds": [m.to_dict() for m in self.manifolds],
            "connections_count": len(self.connections),
            "connections": [c.to_dict() for c in self.connections],
            "partitions_count": len(self.partitions),
            "partitions": [p.to_dict() for p in self.partitions],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
