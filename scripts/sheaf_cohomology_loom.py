"""
Sheaf-Theoretic Cohomology and Epistemic Gluing Loom
Autonomous cognitive spatial module synthesizing local knowledge sections,
evaluating Cech coboundary operators, computing 0-cochain consensus and 1-cocycle obstructions,
and projecting epistemic nerve complexes of cognitive open covers.
Grounded in sheaf theory and algebraic topology (Leray 1946, Cartan 1950, Grothendieck 1957),
epistemic logic and distributed systems (Halpern-Moses 1990),
and topological data analysis on cellular sheaves (Curry 2014, Robinson 2014).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


# Pure Python Linear Algebra Utilities for Cohomological Complexes


def matrix_transpose(mat: List[List[float]]) -> List[List[float]]:
    """Transposes a 2D matrix."""
    if not mat or not mat[0]:
        return []
    rows, cols = len(mat), len(mat[0])
    return [[mat[r][c] for r in range(rows)] for c in range(cols)]


def matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Multiplies matrix A by matrix B."""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    if cols_a != rows_b:
        raise ValueError("Incompatible matrix dimensions for multiplication")
    res = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for k in range(cols_a):
            if a[i][k] != 0.0:
                for j in range(cols_b):
                    res[i][j] += a[i][k] * b[k][j]
    return res


def gaussian_elimination_rref(mat: List[List[float]], tol: float = 1e-9) -> Tuple[List[List[float]], List[int], int]:
    """Computes Reduced Row Echelon Form (RREF) using partial pivoting.
    Returns (rref_matrix, pivot_columns, rank).
    """
    if not mat or not mat[0]:
        return [], [], 0
    rows = len(mat)
    cols = len(mat[0])
    rref = [[val for val in row] for row in mat]
    pivot_cols = []
    r = 0
    for c in range(cols):
        if r >= rows:
            break
        # Find pivot
        max_val = abs(rref[r][c])
        pivot_r = r
        for i in range(r + 1, rows):
            if abs(rref[i][c]) > max_val:
                max_val = abs(rref[i][c])
                pivot_r = i
        if max_val < tol:
            continue
        # Swap rows
        if pivot_r != r:
            rref[r], rref[pivot_r] = rref[pivot_r], rref[r]
        # Normalize pivot row
        pv = rref[r][c]
        for j in range(c, cols):
            rref[r][j] /= pv
        # Eliminate column entries
        for i in range(rows):
            if i != r and abs(rref[i][c]) > tol:
                factor = rref[i][c]
                for j in range(c, cols):
                    rref[i][j] -= factor * rref[r][j]
        pivot_cols.append(c)
        r += 1
    return rref, pivot_cols, r


def compute_kernel_basis(mat: List[List[float]], tol: float = 1e-9) -> List[List[float]]:
    """Computes a basis for the nullspace (kernel) of matrix A: Ax = 0."""
    if not mat or not mat[0]:
        return []
    rows = len(mat)
    cols = len(mat[0])
    rref, pivot_cols, rank = gaussian_elimination_rref(mat, tol)
    pivot_set = set(pivot_cols)
    free_cols = [c for c in range(cols) if c not in pivot_set]

    basis = []
    for free_col in free_cols:
        vec = [0.0] * cols
        vec[free_col] = 1.0
        for r, p_col in enumerate(pivot_cols):
            vec[p_col] = -rref[r][free_col]
        # Normalize vector
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > tol:
            vec = [x / norm for x in vec]
        basis.append(vec)
    return basis


def compute_rank(mat: List[List[float]], tol: float = 1e-9) -> int:
    """Returns matrix rank via Gaussian elimination."""
    _, _, rank = gaussian_elimination_rref(mat, tol)
    return rank


# Sheaf and Open Cover Data Structures


@dataclass
class OpenSet:
    """An open set / cognitive lens in an open cover U of concept space X."""
    lens_id: str
    label: str
    domain: str
    center_x: float
    center_y: float
    radius: float
    section_val: List[float] = field(default_factory=lambda: [1.0])
    uncertainty: float = 0.05

    def to_dict(self) -> Dict[str, Any]:
        return {
            "lens_id": self.lens_id,
            "label": self.label,
            "domain": self.domain,
            "center": [round(self.center_x, 3), round(self.center_y, 3)],
            "radius": round(self.radius, 3),
            "section_val": [round(v, 4) for v in self.section_val],
            "uncertainty": round(self.uncertainty, 4),
        }


@dataclass
class PairwiseOverlap:
    """Pairwise intersection U_ij = U_i cap U_j with transition and discrepancy."""
    index_i: int
    index_j: int
    lens_id_i: str
    lens_id_j: str
    overlap_area: float
    # Difference between restricted sections: rho_j(s_j) - rho_i(s_i)
    discrepancy: List[float] = field(default_factory=list)
    discrepancy_norm: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge": [self.index_i, self.index_j],
            "lenses": [self.lens_id_i, self.lens_id_j],
            "overlap_area": round(self.overlap_area, 4),
            "discrepancy": [round(d, 4) for d in self.discrepancy],
            "discrepancy_norm": round(self.discrepancy_norm, 4),
        }


@dataclass
class TripleOverlap:
    """Triple intersection U_ijk = U_i cap U_j cap U_k."""
    index_i: int
    index_j: int
    index_k: int
    lenses: Tuple[str, str, str]
    cocycle_residual: List[float] = field(default_factory=list)
    cocycle_norm: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "triangle": [self.index_i, self.index_j, self.index_k],
            "lenses": list(self.lenses),
            "cocycle_residual": [round(r, 4) for r in self.cocycle_residual],
            "cocycle_norm": round(self.cocycle_norm, 4),
        }


@dataclass
class SheafCohomologyResult:
    """Diagnostic result of Cech cohomology computation over an epistemic cover."""
    open_sets: List[OpenSet]
    overlaps: List[PairwiseOverlap]
    triples: List[TripleOverlap]
    dim_c0: int
    dim_c1: int
    dim_c2: int
    rank_delta0: int
    rank_delta1: int
    betti_h0: int  # dim ker(delta^0): space of global consensus sections
    betti_h1: int  # dim ker(delta^1) / im(delta^0): obstruction to global gluing
    euler_characteristic: int
    global_gluing_energy: float
    consensus_index: float
    gluing_obstruction_detected: bool
    obstruction_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_open_sets": len(self.open_sets),
            "num_pairwise_overlaps": len(self.overlaps),
            "num_triple_overlaps": len(self.triples),
            "cochain_dimensions": {
                "dim_c0": self.dim_c0,
                "dim_c1": self.dim_c1,
                "dim_c2": self.dim_c2,
            },
            "coboundary_ranks": {
                "rank_delta0": self.rank_delta0,
                "rank_delta1": self.rank_delta1,
            },
            "cohomology_groups": {
                "dim_h0_global_sections": self.betti_h0,
                "dim_h1_obstructions": self.betti_h1,
                "euler_characteristic": self.euler_characteristic,
            },
            "metrics": {
                "global_gluing_energy": round(self.global_gluing_energy, 4),
                "consensus_index": round(self.consensus_index, 4),
                "gluing_obstruction_detected": self.gluing_obstruction_detected,
            },
            "obstruction_summary": self.obstruction_summary,
            "open_sets": [os.to_dict() for os in self.open_sets],
            "overlaps": [ov.to_dict() for ov in self.overlaps],
            "triples": [tr.to_dict() for tr in self.triples],
        }


class SheafCohomologyLoom:
    """Core solver and visualizer for Sheaf Cohomology and Epistemic Gluing."""

    def __init__(self, open_sets: Optional[List[OpenSet]] = None, section_dim: int = 2):
        self.open_sets: List[OpenSet] = open_sets or []
        self.section_dim = section_dim

    def add_lens(self, lens: OpenSet) -> None:
        """Adds an open set / epistemic lens to the cover."""
        self.open_sets.append(lens)

    @classmethod
    def create_default_epistemic_cover(cls) -> "SheafCohomologyLoom":
        """Creates a default epistemic cover representing five interdisciplinary lenses."""
        loom = cls(section_dim=2)
        # Five conceptual domains with overlapping spatial extents
        lenses = [
            OpenSet(
                lens_id="L1",
                label="Spatial Architecture",
                domain="Structural Engineering",
                center_x=160.0,
                center_y=160.0,
                radius=110.0,
                section_val=[1.20, 0.85],
                uncertainty=0.03,
            ),
            OpenSet(
                lens_id="L2",
                label="Environmental Physics",
                domain="Thermodynamics",
                center_x=320.0,
                center_y=140.0,
                radius=105.0,
                section_val=[1.15, 0.90],
                uncertainty=0.04,
            ),
            OpenSet(
                lens_id="L3",
                label="Urban Geography",
                domain="Sociology and Planning",
                center_x=450.0,
                center_y=230.0,
                radius=115.0,
                section_val=[1.10, 0.95],
                uncertainty=0.05,
            ),
            OpenSet(
                lens_id="L4",
                label="Computational AI",
                domain="Graph Topology and Optimization",
                center_x=370.0,
                center_y=360.0,
                radius=110.0,
                section_val=[1.05, 1.10],
                uncertainty=0.02,
            ),
            OpenSet(
                lens_id="L5",
                label="Cognitive Psychology",
                domain="Perception and Ergonomics",
                center_x=210.0,
                center_y=330.0,
                radius=110.0,
                section_val=[1.25, 0.80],
                uncertainty=0.04,
            ),
        ]
        for lens in lenses:
            loom.add_lens(lens)
        return loom

    def compute_intersections(self) -> Tuple[List[PairwiseOverlap], List[TripleOverlap]]:
        """Identifies pairwise and triple intersections based on spatial geometry."""
        n = len(self.open_sets)
        overlaps: List[PairwiseOverlap] = []

        # Find 1-simplices (pairwise overlaps)
        for i in range(n):
            for j in range(i + 1, n):
                si, sj = self.open_sets[i], self.open_sets[j]
                dx = si.center_x - sj.center_x
                dy = si.center_y - sj.center_y
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < (si.radius + sj.radius):
                    # Approximate lens overlap area
                    r1, r2 = si.radius, sj.radius
                    d = max(dist, 1e-4)
                    overlap_metric = max(0.0, (r1 + r2 - d) / (r1 + r2))
                    # Discrepancy between assigned local sections
                    sec_i = si.section_val
                    sec_j = sj.section_val
                    disc = [sec_j[k] - sec_i[k] for k in range(min(len(sec_i), len(sec_j)))]
                    disc_norm = math.sqrt(sum(v * v for v in disc))
                    overlaps.append(
                        PairwiseOverlap(
                            index_i=i,
                            index_j=j,
                            lens_id_i=si.lens_id,
                            lens_id_j=sj.lens_id,
                            overlap_area=overlap_metric,
                            discrepancy=disc,
                            discrepancy_norm=disc_norm,
                        )
                    )

        # Find 2-simplices (triple overlaps)
        # Pair map lookup
        pair_set = set((ov.index_i, ov.index_j) for ov in overlaps)
        triples: List[TripleOverlap] = []

        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if (i, j) in pair_set and (j, k) in pair_set and (i, k) in pair_set:
                        # Check spatial intersection of circles
                        # Verify center of triangle is inside all three circles
                        cx = (self.open_sets[i].center_x + self.open_sets[j].center_x + self.open_sets[k].center_x) / 3.0
                        cy = (self.open_sets[i].center_y + self.open_sets[j].center_y + self.open_sets[k].center_y) / 3.0
                        d_i = math.sqrt((cx - self.open_sets[i].center_x)**2 + (cy - self.open_sets[i].center_y)**2)
                        d_j = math.sqrt((cx - self.open_sets[j].center_x)**2 + (cy - self.open_sets[j].center_y)**2)
                        d_k = math.sqrt((cx - self.open_sets[k].center_x)**2 + (cy - self.open_sets[k].center_y)**2)
                        if d_i <= self.open_sets[i].radius and d_j <= self.open_sets[j].radius and d_k <= self.open_sets[k].radius:
                            # Cocycle condition check on 1-cochain: g_jk - g_ik + g_ij = 0
                            # Finding matching overlaps
                            g_ij = next(ov.discrepancy for ov in overlaps if ov.index_i == i and ov.index_j == j)
                            g_jk = next(ov.discrepancy for ov in overlaps if ov.index_i == j and ov.index_j == k)
                            g_ik = next(ov.discrepancy for ov in overlaps if ov.index_i == i and ov.index_j == k)
                            res = [g_jk[idx] - g_ik[idx] + g_ij[idx] for idx in range(len(g_ij))]
                            res_norm = math.sqrt(sum(v * v for v in res))
                            triples.append(
                                TripleOverlap(
                                    index_i=i,
                                    index_j=j,
                                    index_k=k,
                                    lenses=(self.open_sets[i].lens_id, self.open_sets[j].lens_id, self.open_sets[k].lens_id),
                                    cocycle_residual=res,
                                    cocycle_norm=res_norm,
                                )
                            )

        return overlaps, triples

    def build_cech_complex(self) -> SheafCohomologyResult:
        """Constructs the Cech coboundary operators delta^0 and delta^1,
        and computes sheaf cohomology dimensions.
        """
        overlaps, triples = self.compute_intersections()
        num_v = len(self.open_sets)
        num_e = len(overlaps)
        num_t = len(triples)
        d = self.section_dim

        # Cochain vector dimensions
        dim_c0 = num_v * d
        dim_c1 = num_e * d
        dim_c2 = num_t * d

        # Build delta^0 matrix: C^0 -> C^1
        # Size: (num_e * d) x (num_v * d)
        delta0 = [[0.0] * dim_c0 for _ in range(dim_c1)]
        edge_map: Dict[Tuple[int, int], int] = {}
        for e_idx, ov in enumerate(overlaps):
            edge_map[(ov.index_i, ov.index_j)] = e_idx
            i, j = ov.index_i, ov.index_j
            # (delta^0 s)_{ij} = s_j - s_i (assuming identity restriction maps)
            for k in range(d):
                row = e_idx * d + k
                col_i = i * d + k
                col_j = j * d + k
                delta0[row][col_i] = -1.0
                delta0[row][col_j] = 1.0

        # Build delta^1 matrix: C^1 -> C^2
        # Size: (num_t * d) x (num_e * d)
        delta1 = [[0.0] * dim_c1 for _ in range(dim_c2)]
        for t_idx, tr in enumerate(triples):
            i, j, k = tr.index_i, tr.index_j, tr.index_k
            e_ij = edge_map.get((i, j), -1)
            e_jk = edge_map.get((j, k), -1)
            e_ik = edge_map.get((i, k), -1)
            for m in range(d):
                row = t_idx * d + m
                if e_jk != -1:
                    delta1[row][e_jk * d + m] = 1.0
                if e_ik != -1:
                    delta1[row][e_ik * d + m] = -1.0
                if e_ij != -1:
                    delta1[row][e_ij * d + m] = 1.0

        # Ranks and Cohomology
        rank0 = compute_rank(delta0) if dim_c1 > 0 and dim_c0 > 0 else 0
        rank1 = compute_rank(delta1) if dim_c2 > 0 and dim_c1 > 0 else 0

        # H^0 = ker(delta^0). dim H^0 = dim(C^0) - rank(delta^0)
        dim_h0 = max(0, dim_c0 - rank0)

        # H^1 = ker(delta^1) / im(delta^0)
        # dim ker(delta^1) = dim(C^1) - rank(delta^1)
        # dim im(delta^0) = rank(delta^0)
        # dim H^1 = dim ker(delta^1) - dim im(delta^0) = dim(C^1) - rank(delta^1) - rank(delta^0)
        dim_ker_delta1 = max(0, dim_c1 - rank1)
        dim_h1 = max(0, dim_ker_delta1 - rank0)

        # Topological Euler characteristic: chi = num_v - num_e + num_t
        euler_char = num_v - num_e + num_t

        # Global gluing energy: sum of squared discrepancies
        gluing_energy = sum(ov.discrepancy_norm**2 for ov in overlaps)
        # Consensus index: normalized between 0 and 1
        consensus_index = math.exp(-gluing_energy / (2.0 * max(0.1, num_e)))

        has_obstruction = (dim_h1 > 0) or (gluing_energy > 0.05)

        if dim_h1 == 0 and gluing_energy < 0.01:
            summary = "Trivial cohomology (H^1 = 0). Local sections glue into a single global section."
        elif dim_h1 == 0:
            summary = f"Cohomology is exact (H^1 = 0), but metric gluing energy is {gluing_energy:.3f} across overlaps."
        else:
            summary = f"Non-trivial 1-cohomology detected (dim H^1 = {dim_h1}). Topological obstruction prevents global section synthesis."

        return SheafCohomologyResult(
            open_sets=self.open_sets,
            overlaps=overlaps,
            triples=triples,
            dim_c0=dim_c0,
            dim_c1=dim_c1,
            dim_c2=dim_c2,
            rank_delta0=rank0,
            rank_delta1=rank1,
            betti_h0=dim_h0,
            betti_h1=dim_h1,
            euler_characteristic=euler_char,
            global_gluing_energy=gluing_energy,
            consensus_index=consensus_index,
            gluing_obstruction_detected=has_obstruction,
            obstruction_summary=summary,
        )

    def render_svg(self, result: Optional[SheafCohomologyResult] = None, width: int = 880, height: int = 620) -> str:
        """Renders an interactive dark titanium SVG visualization of the epistemic nerve complex."""
        if result is None:
            result = self.build_cech_complex()

        lines = []
        lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
        lines.append('  <defs>')
        # Gradients and styles
        lines.append('    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#090d13" />')
        lines.append('      <stop offset="100%" stop-color="#161b22" />')
        lines.append('    </linearGradient>')
        lines.append('    <linearGradient id="lens-fill" x1="0%" y1="0%" x2="100%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#58a6ff" stop-opacity="0.12" />')
        lines.append('      <stop offset="100%" stop-color="#1f6feb" stop-opacity="0.04" />')
        lines.append('    </linearGradient>')
        lines.append('    <linearGradient id="triangle-fill" x1="0%" y1="0%" x2="100%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#3fb950" stop-opacity="0.25" />')
        lines.append('      <stop offset="100%" stop-color="#2ea043" stop-opacity="0.10" />')
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
        lines.append('      EPISTEMIC SHEAF COHOMOLOGY &amp; NERVE COMPLEX')
        lines.append('    </text>')
        lines.append('    <text y="22" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="12">')
        lines.append('      Cech Coboundary Operators, Obstruction 1-Cocycles &amp; Local-to-Global Semantic Gluing')
        lines.append('    </text>')
        lines.append('  </g>')

        # Coordinate Canvas Offset
        canvas_ox = 0
        canvas_oy = 20

        # 1. Render Triple Overlaps (2-simplices)
        lines.append('  <g id="triple-simplices">')
        for tr in result.triples:
            s_i = result.open_sets[tr.index_i]
            s_j = result.open_sets[tr.index_j]
            s_k = result.open_sets[tr.index_k]
            pts = f"{s_i.center_x + canvas_ox},{s_i.center_y + canvas_oy} {s_j.center_x + canvas_ox},{s_j.center_y + canvas_oy} {s_k.center_x + canvas_ox},{s_k.center_y + canvas_oy}"
            lines.append(f'    <polygon points="{pts}" fill="url(#triangle-fill)" stroke="#3fb950" stroke-width="1.2" stroke-dasharray="3 3" />')
        lines.append('  </g>')

        # 2. Render Open Cover Disks (Lenses)
        lines.append('  <g id="open-sets">')
        for os in result.open_sets:
            cx = os.center_x + canvas_ox
            cy = os.center_y + canvas_oy
            lines.append(f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{os.radius:.1f}" fill="url(#lens-fill)" stroke="#388bfd" stroke-width="1" stroke-opacity="0.4" />')
        lines.append('  </g>')

        # 3. Render Pairwise Overlap Edges (1-simplices)
        lines.append('  <g id="pairwise-edges">')
        for ov in result.overlaps:
            s_i = result.open_sets[ov.index_i]
            s_j = result.open_sets[ov.index_j]
            x1 = s_i.center_x + canvas_ox
            y1 = s_i.center_y + canvas_oy
            x2 = s_j.center_x + canvas_ox
            y2 = s_j.center_y + canvas_oy
            disc_norm = ov.discrepancy_norm
            # Color edge by discrepancy (green if near zero, yellow/red if high)
            if disc_norm < 0.05:
                edge_col = "#3fb950"
                sw = "2.0"
            elif disc_norm < 0.15:
                edge_col = "#d29922"
                sw = "2.2"
            else:
                edge_col = "#f85149"
                sw = "2.6"
            lines.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{edge_col}" stroke-width="{sw}" stroke-opacity="0.85" />')
            # Edge mid-point label
            mx = (x1 + x2) / 2.0
            my = (y1 + y2) / 2.0
            lines.append(f'    <circle cx="{mx:.1f}" cy="{my:.1f}" r="3" fill="{edge_col}" />')
            lines.append(f'    <text x="{mx:.1f}" y="{my - 6:.1f}" fill="#c9d1d9" font-family="monospace" font-size="10" text-anchor="middle">&#948;&#185;={disc_norm:.2f}</text>')
        lines.append('  </g>')

        # 4. Render Open Set Center Vertices & Local Stalks (0-simplices)
        lines.append('  <g id="nerve-vertices">')
        for idx, os in enumerate(result.open_sets):
            cx = os.center_x + canvas_ox
            cy = os.center_y + canvas_oy
            # Vertex Node
            lines.append(f'    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="#1f6feb" stroke="#58a6ff" stroke-width="2" filter="url(#glow)" />')
            # Label
            lines.append(f'    <text x="{cx:.1f}" y="{cy - 14:.1f}" fill="#f0f6fc" font-family="system-ui, sans-serif" font-size="12" font-weight="600" text-anchor="middle">{html.escape(os.lens_id)}: {html.escape(os.label)}</text>')
            # Domain and Stalk Info
            sec_str = ", ".join(f"{v:.2f}" for v in os.section_val)
            lines.append(f'    <text x="{cx:.1f}" y="{cy + 22:.1f}" fill="#8b949e" font-family="monospace" font-size="10" text-anchor="middle">s_{idx}=({sec_str})</text>')
        lines.append('  </g>')

        # 5. Right Sidebar Diagnostics Panel
        panel_x = 610
        panel_y = 40
        panel_w = 240
        panel_h = 540

        lines.append(f'  <g id="diagnostics-panel" transform="translate({panel_x}, {panel_y})">')
        lines.append(f'    <rect width="{panel_w}" height="{panel_h}" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="16" y="28" fill="#58a6ff" font-family="system-ui, sans-serif" font-size="14" font-weight="700">COHOMOLOGY METRICS</text>')
        lines.append('    <line x1="16" y1="38" x2="224" y2="38" stroke="#30363d" stroke-width="1" />')

        # Cohomology dimensions
        metrics = [
            ("Lenses |U|", str(len(result.open_sets))),
            ("Overlaps |U_ij|", str(len(result.overlaps))),
            ("Triples |U_ijk|", str(len(result.triples))),
            ("dim C^0", str(result.dim_c0)),
            ("dim C^1", str(result.dim_c1)),
            ("rank delta^0", str(result.rank_delta0)),
            ("rank delta^1", str(result.rank_delta1)),
            ("dim H^0 (Consensus)", str(result.betti_h0)),
            ("dim H^1 (Obstruction)", str(result.betti_h1)),
            ("Euler Char (chi)", str(result.euler_characteristic)),
            ("Gluing Energy", f"{result.global_gluing_energy:.4f}"),
            ("Consensus Index", f"{result.consensus_index * 100:.1f}%"),
        ]

        curr_y = 62
        for label, val in metrics:
            lines.append(f'    <text x="16" y="{curr_y}" fill="#8b949e" font-family="system-ui, sans-serif" font-size="11">{label}:</text>')
            # Highlight key cohomology numbers
            val_col = "#58a6ff"
            if label.startswith("dim H^1") and result.betti_h1 > 0:
                val_col = "#f85149"
            elif label.startswith("dim H^0"):
                val_col = "#3fb950"
            lines.append(f'    <text x="224" y="{curr_y}" fill="{val_col}" font-family="monospace" font-size="11" font-weight="600" text-anchor="end">{val}</text>')
            curr_y += 24

        # Obstruction Status Banner
        lines.append('    <line x1="16" y1="365" x2="224" y2="365" stroke="#30363d" stroke-width="1" />')
        status_col = "#3fb950" if not result.gluing_obstruction_detected else "#d29922"
        status_text = "GLOBAL CONSENSUS" if not result.gluing_obstruction_detected else "COHOMOLOGICAL OBSTRUCTION"
        lines.append(f'    <rect x="16" y="378" width="208" height="30" fill="{status_col}" fill-opacity="0.15" rx="4" stroke="{status_col}" stroke-width="1" />')
        lines.append(f'    <text x="120" y="398" fill="{status_col}" font-family="system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">{status_text}</text>')

        # Mathematical Legend
        lines.append('    <g transform="translate(16, 428)">')
        lines.append('      <text fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600">FORMULATION:</text>')
        lines.append('      <text y="18" fill="#c9d1d9" font-family="monospace" font-size="9">&#948;&#7496;(s)_ij = s_j - s_i</text>')
        lines.append('      <text y="34" fill="#c9d1d9" font-family="monospace" font-size="9">H&#7496; = ker(&#948;&#7496;) (Global)</text>')
        lines.append('      <text y="50" fill="#c9d1d9" font-family="monospace" font-size="9">H&#185; = ker(&#948;&#185;) / im(&#948;&#7496;)</text>')
        lines.append('      <text y="66" fill="#c9d1d9" font-family="monospace" font-size="9">&#967; = dim C&#7496; - dim C&#185; + dim C&#178;</text>')
        lines.append('      <text y="82" fill="#8b949e" font-family="system-ui, sans-serif" font-size="9">Exact sequence gluing check</text>')
        lines.append('    </g>')

        lines.append('  </g>')

        lines.append('</svg>')
        return "\n".join(lines)

    def generate_markdown_report(self, result: Optional[SheafCohomologyResult] = None) -> str:
        """Generates a formal analytical report on sheaf cohomology and gluing obstructions."""
        if result is None:
            result = self.build_cech_complex()

        lines = [
            "# Sheaf-Theoretic Cohomology & Epistemic Gluing Analysis",
            "",
            "## Executive Summary",
            "",
            f"{result.obstruction_summary}",
            "",
            f"- **Global Sections (H^0 Dimension):** {result.betti_h0}",
            f"- **Gluing Obstruction (H^1 Dimension):** {result.betti_h1}",
            f"- **Topological Euler Characteristic (chi):** {result.euler_characteristic}",
            f"- **Global Gluing Energy Residual:** {result.global_gluing_energy:.4f}",
            f"- **Consensus Synthesis Index:** {result.consensus_index * 100:.1f}%",
            "",
            "## Cech Cochain Complex Architecture",
            "",
            "| Complex Level | Simplex Type | Count | Total Dimension | Boundary Operator | Rank |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
            f"| **C^0** | 0-simplices (Lenses) | {len(result.open_sets)} | {result.dim_c0} | delta^0 : C^0 -> C^1 | {result.rank_delta0} |",
            f"| **C^1** | 1-simplices (Pairwise Overlaps) | {len(result.overlaps)} | {result.dim_c1} | delta^1 : C^1 -> C^2 | {result.rank_delta1} |",
            f"| **C^2** | 2-simplices (Triple Overlaps) | {len(result.triples)} | {result.dim_c2} | N/A | - |",
            "",
            "## Epistemic Lenses (Open Sets)",
            "",
            "| Lens ID | Domain Name | Discipline | Center (x, y) | Radius | Local Stalk Section |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ]

        for os in result.open_sets:
            sec_str = "(" + ", ".join(f"{v:.2f}" for v in os.section_val) + ")"
            lines.append(
                f"| `{os.lens_id}` | {os.label} | {os.domain} | ({os.center_x:.1f}, {os.center_y:.1f}) | {os.radius:.1f} | `{sec_str}` |"
            )

        lines.extend([
            "",
            "## Pairwise Overlaps & Gluing Residuals",
            "",
            "| Overlap | Lenses | Overlap Area Metric | Discrepancy Norm (delta^0) | Gluing Agreement |",
            "| :--- | :--- | :--- | :--- | :--- |",
        ])

        for ov in result.overlaps:
            status = "Consistent" if ov.discrepancy_norm < 0.08 else "Discrepancy"
            lines.append(
                f"| `{ov.lens_id_i} cap {ov.lens_id_j}` | {ov.lens_id_i} to {ov.lens_id_j} | {ov.overlap_area:.3f} | {ov.discrepancy_norm:.4f} | {status} |"
            )

        lines.extend([
            "",
            "## Theoretical Interpretation",
            "",
            "1. **Local-to-Global Synthesis:** In standard sheaf theory, a presheaf becomes a sheaf when every family of compatible local sections glues into a unique global section. Here, H^0 measures the dimension of unanimous global consensus.",
            "2. **Obstruction Holonomy:** When H^1 is non-zero, local pairwise agreements do not extend to a globally coherent conceptualization. Disagreements accumulate around triangular cycles, creating topological obstructions.",
            "3. **Epistemic Resolution:** Reducing H^1 requires updating transition homomorphisms between adjacent cognitive domains or recalibrating local sections until the coboundary energy drops below the coherence threshold.",
        ])

        return "\n".join(lines)

    def generate_html_viewer(self, result: Optional[SheafCohomologyResult] = None) -> str:
        """Generates a standalone dark titanium HTML interactive viewer."""
        if result is None:
            result = self.build_cech_complex()

        svg_content = self.render_svg(result)
        report_md = self.generate_markdown_report(result)
        json_data = json.dumps(result.to_dict(), indent=2)

        html_str = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sheaf Cohomology & Epistemic Gluing Loom | DxSkills</title>
  <style>
    :root {{
      --bg: #090d13;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --heading: #f0f6fc;
      --accent: #58a6ff;
      --accent-green: #3fb950;
      --accent-warn: #d29922;
      --accent-red: #f85149;
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
      <h1>Sheaf-Theoretic Cohomology & Epistemic Gluing Loom</h1>
      <p class="subtitle">Autonomous Cognitive Spatial Scaffold: Cech Nerve Complex, Coboundary Operators &amp; Topological Gluing Invariants</p>
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
