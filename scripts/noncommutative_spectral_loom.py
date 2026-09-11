"""
Non-Commutative Spectral Triple & Connes Distance Loom
Autonomous cognitive spatial module synthesizing non-commutative concept algebras,
computing Dirac operator eigenspectra, evaluating Connes geodesic spectral distances,
and projecting quantum metric fluctuations and noncommutative framing commutators.
Grounded in non-commutative geometry (Connes 1994),
quantum cognition and contextuality (Aerts 2009, Busemeyer-Wang 2012),
and spectral metric spaces (Rieffel 2004, D'Andrea-Martinetti 2014).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional, Any
import math
import html
import json


# Pure Python Linear Algebra and Spectral Utilities


def matrix_zeros(rows: int, cols: int) -> List[List[float]]:
    """Creates a zero-filled matrix of size rows x cols."""
    return [[0.0] * cols for _ in range(rows)]


def matrix_identity(n: int) -> List[List[float]]:
    """Creates an identity matrix of size n x n."""
    res = matrix_zeros(n, n)
    for i in range(n):
        res[i][i] = 1.0
    return res


def matrix_add(a: List[List[float]], b: List[List[float]], scale_b: float = 1.0) -> List[List[float]]:
    """Adds matrix A and scaled matrix B: A + scale_b * B."""
    rows, cols = len(a), len(a[0])
    return [[a[r][c] + scale_b * b[r][c] for c in range(cols)] for r in range(rows)]


def matrix_mult(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Multiplies matrix A by matrix B."""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    res = matrix_zeros(rows_a, cols_b)
    for i in range(rows_a):
        for k in range(cols_a):
            if a[i][k] != 0.0:
                for j in range(cols_b):
                    res[i][j] += a[i][k] * b[k][j]
    return res


def matrix_commutator(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Computes commutator [A, B] = A*B - B*A."""
    ab = matrix_mult(a, b)
    ba = matrix_mult(b, a)
    return matrix_add(ab, ba, scale_b=-1.0)


def frobenius_norm(mat: List[List[float]]) -> float:
    """Computes Frobenius norm of matrix."""
    return math.sqrt(sum(val * val for row in mat for val in row))


def spectral_operator_norm_symm(mat: List[List[float]], max_iter: int = 100, tol: float = 1e-7) -> float:
    """Estimates operator 2-norm ||A||_op using power iteration on A^T * A."""
    n = len(mat)
    if n == 0:
        return 0.0
    # v0 = normalized vector
    v = [1.0 / math.sqrt(n)] * n
    # At * A
    at_a = matrix_zeros(n, n)
    for i in range(n):
        for j in range(n):
            for k in range(len(mat)):
                at_a[i][j] += mat[k][i] * mat[k][j]

    # Power iteration
    lambda_old = 0.0
    for _ in range(max_iter):
        # w = at_a * v
        w = [sum(at_a[i][j] * v[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x * x for x in w))
        if norm < tol:
            return 0.0
        v = [x / norm for x in w]
        # Rayleigh quotient
        lambda_val = sum(v[i] * sum(at_a[i][j] * v[j] for j in range(n)) for i in range(n))
        if abs(lambda_val - lambda_old) < tol:
            break
        lambda_old = lambda_val
    return math.sqrt(max(0.0, lambda_val))


def jacobi_eigenvalues_symm(mat: List[List[float]], max_sweeps: int = 50, tol: float = 1e-9) -> Tuple[List[float], List[List[float]]]:
    """Computes eigenvalues and eigenvectors of a real symmetric matrix via Jacobi rotations.
    Returns (eigenvalues, eigenvectors) where eigenvectors are columns of V.
    """
    n = len(mat)
    a = [[val for val in row] for row in mat]
    v = matrix_identity(n)

    for _ in range(max_sweeps):
        # Find maximum off-diagonal element
        max_off = 0.0
        p, q = 0, 1
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > max_off:
                    max_off = abs(a[i][j])
                    p, q = i, j

        if max_off < tol:
            break

        # Compute Jacobi rotation angle
        diff = a[q][q] - a[p][p]
        if abs(a[p][q]) < tol:
            c, s = 1.0, 0.0
        else:
            phi = diff / (2.0 * a[p][q])
            t = math.copysign(1.0 / (abs(phi) + math.sqrt(phi * phi + 1.0)), phi)
            c = 1.0 / math.sqrt(t * t + 1.0)
            s = t * c

        # Apply rotation to matrix A
        app = a[p][p]
        aqq = a[q][q]
        apq = a[p][q]

        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = 0.0
        a[q][p] = 0.0

        for k in range(n):
            if k != p and k != q:
                akp = a[k][p]
                akq = a[k][q]
                a[k][p] = c * akp - s * akq
                a[p][k] = a[k][p]
                a[k][q] = s * akp + c * akq
                a[q][k] = a[k][q]

        # Accumulate eigenvectors in V
        for k in range(n):
            vkp = v[k][p]
            vkq = v[k][q]
            v[k][p] = c * vkp - s * vkq
            v[k][q] = s * vkp + c * vkq

    eigenvalues = [a[i][i] for i in range(n)]
    # Sort eigenvalues ascending
    idx = sorted(range(n), key=lambda i: eigenvalues[i])
    sorted_evals = [eigenvalues[i] for i in idx]
    sorted_evecs = [[v[r][i] for i in idx] for r in range(n)]
    return sorted_evals, sorted_evecs


# Non-Commutative Spectral Triple Data Structures


@dataclass
class ConceptState:
    """A pure epistemic state / concept vector in Hilbert space H."""
    state_id: str
    label: str
    description: str
    vector: List[float] = field(default_factory=list)

    def normalize(self) -> None:
        norm = math.sqrt(sum(x * x for x in self.vector))
        if norm > 1e-9:
            self.vector = [x / norm for x in self.vector]

    def expectation_value(self, operator: List[List[float]]) -> float:
        """Calculates state expectation value: <psi | O | psi>."""
        n = len(self.vector)
        res = 0.0
        for i in range(n):
            for j in range(n):
                res += self.vector[i] * operator[i][j] * self.vector[j]
        return res

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state_id": self.state_id,
            "label": self.label,
            "description": self.description,
            "vector": [round(x, 4) for x in self.vector],
        }


@dataclass
class ConceptObservable:
    """A self-adjoint concept observable in algebra A."""
    name: str
    label: str
    matrix: List[List[float]]
    description: str = ""

    @property
    def dimension(self) -> int:
        return len(self.matrix)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "label": self.label,
            "description": self.description,
            "dimension": self.dimension,
            "trace": round(sum(self.matrix[i][i] for i in range(self.dimension)), 4),
        }


@dataclass
class ConnesDistancePair:
    """Spectral geodesic distance between two concept states."""
    state_id_a: str
    state_id_b: str
    label_a: str
    label_b: str
    connes_distance: float
    euclidean_distance: float
    optimal_observable: str
    gradient_norm: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "states": [self.state_id_a, self.state_id_b],
            "labels": [self.label_a, self.label_b],
            "connes_distance": round(self.connes_distance, 4),
            "euclidean_distance": round(self.euclidean_distance, 4),
            "optimal_observable": self.optimal_observable,
            "gradient_norm": round(self.gradient_norm, 4),
        }


@dataclass
class SpectralTripleResult:
    """Complete diagnostic result from Non-Commutative Spectral Triple analysis."""
    hilbert_dim: int
    num_observables: int
    num_states: int
    dirac_eigenvalues: List[float]
    spectral_dimension: float
    spectral_action: float
    connes_distances: List[ConnesDistancePair]
    commutator_norms: Dict[str, float]
    framing_noncommutativity_index: float
    states: List[ConceptState]
    observables: List[ConceptObservable]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hilbert_dim": self.hilbert_dim,
            "num_observables": self.num_observables,
            "num_states": self.num_states,
            "dirac_eigenvalues": [round(ev, 4) for ev in self.dirac_eigenvalues],
            "spectral_dimension": round(self.spectral_dimension, 4),
            "spectral_action": round(self.spectral_action, 4),
            "commutator_norms": {k: round(v, 4) for k, v in self.commutator_norms.items()},
            "framing_noncommutativity_index": round(self.framing_noncommutativity_index, 4),
            "connes_distances": [cd.to_dict() for cd in self.connes_distances],
            "states": [st.to_dict() for st in self.states],
            "observables": [obs.to_dict() for obs in self.observables],
        }


class NonCommutativeSpectralLoom:
    """Core solver and visualizer for Spectral Triples (A, H, D) and Connes Distance."""

    def __init__(self, hilbert_dim: int = 4):
        self.hilbert_dim = hilbert_dim
        self.dirac_operator: List[List[float]] = matrix_zeros(hilbert_dim, hilbert_dim)
        self.observables: List[ConceptObservable] = []
        self.states: List[ConceptState] = []

    def set_dirac_operator(self, d_matrix: List[List[float]]) -> None:
        """Sets the self-adjoint Dirac operator D on Hilbert space H."""
        if len(d_matrix) != self.hilbert_dim or len(d_matrix[0]) != self.hilbert_dim:
            raise ValueError(f"Dirac matrix dimension must be {self.hilbert_dim}x{self.hilbert_dim}")
        self.dirac_operator = [[val for val in row] for row in d_matrix]

    def add_observable(self, observable: ConceptObservable) -> None:
        """Adds a self-adjoint operator to algebra A."""
        if observable.dimension != self.hilbert_dim:
            raise ValueError(f"Observable dimension must match Hilbert dim {self.hilbert_dim}")
        self.observables.append(observable)

    def add_state(self, state: ConceptState) -> None:
        """Adds a pure epistemic state vector to H."""
        if len(state.vector) != self.hilbert_dim:
            raise ValueError(f"State vector must have dimension {self.hilbert_dim}")
        state.normalize()
        self.states.append(state)

    @classmethod
    def create_default_cognitive_spectral_triple(cls) -> "NonCommutativeSpectralLoom":
        """Builds a default 4-dimensional cognitive spectral triple representing
        spatial synthesis, analytical rigor, intuitive creativity, and execution cadence.
        """
        loom = cls(hilbert_dim=4)

        # 1. Dirac Operator D: Models cognitive dispersion / resonance hierarchy
        # D = diag(-1.5, -0.5, 0.5, 1.5) with off-diagonal interaction coupling
        d_mat = [
            [-1.50, 0.25, 0.10, 0.00],
            [0.25, -0.50, 0.30, 0.10],
            [0.10, 0.30, 0.50, 0.25],
            [0.00, 0.10, 0.25, 1.50],
        ]
        loom.set_dirac_operator(d_mat)

        # 2. Concept Observables in Algebra A
        # Observable A1: Spatial Architecture (Geometric vs Phonological mode)
        a1_mat = [
            [1.2, 0.4, 0.0, 0.0],
            [0.4, -0.8, 0.3, 0.0],
            [0.0, 0.3, 0.9, 0.2],
            [0.0, 0.0, 0.2, -1.1],
        ]
        loom.add_observable(
            ConceptObservable("A1", "Spatial Orientation", a1_mat, "Visual-spatial architectural representation")
        )

        # Observable A2: Analytical Precision (Formal Logic vs Heuristic Reasoning)
        a2_mat = [
            [0.8, 0.0, 0.5, 0.1],
            [0.0, 1.3, 0.2, 0.4],
            [0.5, 0.2, -1.0, 0.0],
            [0.1, 0.4, 0.0, -0.7],
        ]
        loom.add_observable(
            ConceptObservable("A2", "Analytical Proof", a2_mat, "Formal deduction and logical verification")
        )

        # Observable A3: Divergent Lateral Thinking
        a3_mat = [
            [0.1, 0.6, 0.2, 0.5],
            [0.6, 0.2, -0.4, 0.1],
            [0.2, -0.4, 0.5, 0.3],
            [0.5, 0.1, 0.3, -0.6],
        ]
        loom.add_observable(
            ConceptObservable("A3", "Lateral Synthesis", a3_mat, "Associative spatial concept linkage")
        )

        # 3. Concept States (Pure vectors in H)
        loom.add_state(ConceptState("S1", "Architectural Blueprint", "Spatial topological focus", [0.85, 0.45, 0.20, 0.10]))
        loom.add_state(ConceptState("S2", "Formal Axiomatic Logic", "Rigorous symbolic deduction", [0.15, 0.90, 0.35, 0.10]))
        loom.add_state(ConceptState("S3", "Intuitive Creative Spurt", "Unconstrained divergent thinking", [0.30, 0.20, 0.88, 0.30]))
        loom.add_state(ConceptState("S4", "Operational Delivery", "Focused implementation execution", [0.10, 0.30, 0.25, 0.90]))

        return loom

    def compute_spectral_analysis(self) -> SpectralTripleResult:
        """Solves Dirac operator eigenvalues, computes Connes distances, and analyzes commutators."""
        n = self.hilbert_dim

        # 1. Diagonalize Dirac operator D
        evals, _ = jacobi_eigenvalues_symm(self.dirac_operator)

        # 2. Spectral Dimension estimate: based on eigenvalue growth rate
        pos_evals = [abs(ev) for ev in evals if abs(ev) > 1e-4]
        if len(pos_evals) >= 2:
            log_idx = [math.log(i + 1) for i in range(len(pos_evals))]
            log_ev = [math.log(ev) for ev in sorted(pos_evals)]
            # Linear regression slope: log(ev) ~ (1 / d_s) * log(n)
            mean_x = sum(log_idx) / len(log_idx)
            mean_y = sum(log_ev) / len(log_ev)
            num = sum((log_idx[i] - mean_x) * (log_ev[i] - mean_y) for i in range(len(log_idx)))
            den = sum((log_idx[i] - mean_x)**2 for i in range(len(log_idx)))
            slope = num / max(1e-6, den)
            spectral_dim = 1.0 / max(0.1, slope) if slope > 0.05 else 1.0
        else:
            spectral_dim = 1.0

        # 3. Spectral Action Tr(f(D/Lambda)): sum of exp(-lambda^2 / 2)
        spectral_action = sum(math.exp(- (ev * ev) / 2.0) for ev in evals)

        # 4. Commutator calculations [A_i, A_j] and [D, A_i]
        commutator_norms: Dict[str, float] = {}
        total_comm_norm = 0.0
        comm_pairs = 0

        num_obs = len(self.observables)
        for i in range(num_obs):
            for j in range(i + 1, num_obs):
                oa = self.observables[i]
                ob = self.observables[j]
                comm = matrix_commutator(oa.matrix, ob.matrix)
                c_norm = frobenius_norm(comm)
                key = f"[{oa.name}, {ob.name}]"
                commutator_norms[key] = c_norm
                total_comm_norm += c_norm
                comm_pairs += 1

        framing_noncomm = total_comm_norm / max(1, comm_pairs)

        # 5. Connes Distance between all state pairs
        # d_D(w1, w2) = sup_{a: ||[D, a]|| <= 1} |w1(a) - w2(a)|
        connes_pairs: List[ConnesDistancePair] = []
        num_st = len(self.states)

        for i in range(num_st):
            for j in range(i + 1, num_st):
                s_a = self.states[i]
                s_b = self.states[j]

                # Euclidean state vector distance
                euc_dist = math.sqrt(sum((s_a.vector[k] - s_b.vector[k])**2 for k in range(n)))

                # Find supremum over available observables in algebra
                max_diff = 0.0
                best_obs_name = "None"
                best_grad_norm = 1.0

                for obs in self.observables:
                    # Compute [D, a]
                    d_a_comm = matrix_commutator(self.dirac_operator, obs.matrix)
                    op_norm = spectral_operator_norm_symm(d_a_comm)
                    grad_norm = max(1e-4, op_norm)

                    # Normalized observable satisfying ||[D, a_norm]|| <= 1
                    diff = abs(s_a.expectation_value(obs.matrix) - s_b.expectation_value(obs.matrix))
                    spectral_dist_candidate = diff / grad_norm

                    if spectral_dist_candidate > max_diff:
                        max_diff = spectral_dist_candidate
                        best_obs_name = obs.name
                        best_grad_norm = grad_norm

                # Also test projection operator difference |psi_a><psi_a| - |psi_b><psi_b|
                proj_mat = matrix_zeros(n, n)
                for r in range(n):
                    for c in range(n):
                        proj_mat[r][c] = s_a.vector[r] * s_a.vector[c] - s_b.vector[r] * s_b.vector[c]
                d_proj_comm = matrix_commutator(self.dirac_operator, proj_mat)
                proj_grad_norm = max(1e-4, spectral_operator_norm_symm(d_proj_comm))
                proj_diff = abs(s_a.expectation_value(proj_mat) - s_b.expectation_value(proj_mat))
                proj_spectral_dist = proj_diff / proj_grad_norm

                if proj_spectral_dist > max_diff:
                    max_diff = proj_spectral_dist
                    best_obs_name = "Optimal Projector"
                    best_grad_norm = proj_grad_norm

                connes_pairs.append(
                    ConnesDistancePair(
                        state_id_a=s_a.state_id,
                        state_id_b=s_b.state_id,
                        label_a=s_a.label,
                        label_b=s_b.label,
                        connes_distance=max_diff,
                        euclidean_distance=euc_dist,
                        optimal_observable=best_obs_name,
                        gradient_norm=best_grad_norm,
                    )
                )

        return SpectralTripleResult(
            hilbert_dim=n,
            num_observables=num_obs,
            num_states=num_st,
            dirac_eigenvalues=evals,
            spectral_dimension=spectral_dim,
            spectral_action=spectral_action,
            connes_distances=connes_pairs,
            commutator_norms=commutator_norms,
            framing_noncommutativity_index=framing_noncomm,
            states=self.states,
            observables=self.observables,
        )

    def render_svg(self, result: Optional[SpectralTripleResult] = None, width: int = 900, height: int = 620) -> str:
        """Renders an interactive dark titanium SVG visualization of the Non-Commutative Spectral Triple."""
        if result is None:
            result = self.compute_spectral_analysis()

        lines = []
        lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
        lines.append('  <defs>')
        lines.append('    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#090d13" />')
        lines.append('      <stop offset="100%" stop-color="#161b22" />')
        lines.append('    </linearGradient>')
        lines.append('    <linearGradient id="dirac-ladder-grad" x1="0%" y1="0%" x2="0%" y2="100%">')
        lines.append('      <stop offset="0%" stop-color="#a371f7" stop-opacity="0.8" />')
        lines.append('      <stop offset="100%" stop-color="#1f6feb" stop-opacity="0.8" />')
        lines.append('    </linearGradient>')
        lines.append('    <linearGradient id="connes-chord-grad" x1="0%" y1="0%" x2="100%" y2="0%">')
        lines.append('      <stop offset="0%" stop-color="#58a6ff" />')
        lines.append('      <stop offset="100%" stop-color="#3fb950" />')
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
        lines.append('      NON-COMMUTATIVE SPECTRAL TRIPLE &amp; CONNES DISTANCE')
        lines.append('    </text>')
        lines.append('    <text y="22" fill="#8b949e" font-family="system-ui, -apple-system, sans-serif" font-size="12">')
        lines.append('      Dirac Eigenspectrum, Noncommutative Framing Commutators &amp; Geodesic Spectral Metrics')
        lines.append('    </text>')
        lines.append('  </g>')

        # 1. Left Panel: Dirac Operator Eigenvalue Ladder
        lines.append('  <!-- Panel 1: Dirac Ladder -->')
        lines.append('  <g id="dirac-ladder" transform="translate(40, 90)">')
        lines.append('    <rect width="260" height="490" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="20" y="28" fill="#a371f7" font-family="system-ui, sans-serif" font-size="13" font-weight="700">DIRAC EIGENSPECTRUM D</text>')
        lines.append('    <line x1="20" y1="38" x2="240" y2="38" stroke="#30363d" stroke-width="1" />')

        # Draw zero line
        ladder_zero_y = 260
        lines.append(f'    <line x1="30" y1="{ladder_zero_y}" x2="230" y2="{ladder_zero_y}" stroke="#484f58" stroke-width="1" stroke-dasharray="3 3" />')
        lines.append(f'    <text x="235" y="{ladder_zero_y + 4}" fill="#6e7681" font-family="monospace" font-size="9">&#955;=0</text>')

        # Range of eigenvalues
        min_ev = min(result.dirac_eigenvalues) if result.dirac_eigenvalues else -1.0
        max_ev = max(result.dirac_eigenvalues) if result.dirac_eigenvalues else 1.0
        span_ev = max(1.0, max(abs(min_ev), abs(max_ev)))

        for idx, ev in enumerate(result.dirac_eigenvalues):
            # Map ev to y coordinate
            y_pos = ladder_zero_y - (ev / span_ev) * 170.0
            ev_col = "#a371f7" if ev >= 0 else "#58a6ff"
            lines.append(f'    <line x1="50" y1="{y_pos:.1f}" x2="210" y2="{y_pos:.1f}" stroke="{ev_col}" stroke-width="3" filter="url(#glow)" />')
            lines.append(f'    <circle cx="50" cy="{y_pos:.1f}" r="4" fill="{ev_col}" />')
            lines.append(f'    <circle cx="210" cy="{y_pos:.1f}" r="4" fill="{ev_col}" />')
            lines.append(f'    <text x="130" y="{y_pos - 6:.1f}" fill="#f0f6fc" font-family="monospace" font-size="10" font-weight="600" text-anchor="middle">&#955;_{idx+1} = {ev:+.3f}</text>')

        # Spectral summary under ladder
        lines.append(f'    <text x="20" y="440" fill="#8b949e" font-family="system-ui, sans-serif" font-size="11">Spectral Dim (d_s):</text>')
        lines.append(f'    <text x="240" y="440" fill="#a371f7" font-family="monospace" font-size="11" font-weight="600" text-anchor="end">{result.spectral_dimension:.2f}</text>')
        lines.append(f'    <text x="20" y="465" fill="#8b949e" font-family="system-ui, sans-serif" font-size="11">Spectral Action S[D]:</text>')
        lines.append(f'    <text x="240" y="465" fill="#58a6ff" font-family="monospace" font-size="11" font-weight="600" text-anchor="end">{result.spectral_action:.3f}</text>')
        lines.append('  </g>')

        # 2. Middle Panel: Connes Distance Geodesic Geometry
        lines.append('  <!-- Panel 2: Connes Distance Graph -->')
        lines.append('  <g id="connes-graph" transform="translate(320, 90)">')
        lines.append('    <rect width="320" height="490" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="20" y="28" fill="#3fb950" font-family="system-ui, sans-serif" font-size="13" font-weight="700">CONNES DISTANCE GRAPH</text>')
        lines.append('    <line x1="20" y1="38" x2="300" y2="38" stroke="#30363d" stroke-width="1" />')

        # Node coordinates for the 4 states in a circular layout
        cx, cy = 160, 190
        rad = 100
        num_s = len(result.states)
        node_coords = []
        for i in range(num_s):
            ang = 2.0 * math.pi * i / max(1, num_s) - math.pi / 2.0
            nx = cx + rad * math.cos(ang)
            ny = cy + rad * math.sin(ang)
            node_coords.append((nx, ny))

        # Draw Connes distance chords
        for cd in result.connes_distances:
            idx_a = next(k for k, s in enumerate(result.states) if s.state_id == cd.state_id_a)
            idx_b = next(k for k, s in enumerate(result.states) if s.state_id == cd.state_id_b)
            x1, y1 = node_coords[idx_a]
            x2, y2 = node_coords[idx_b]
            sw = max(1.0, min(3.5, cd.connes_distance * 2.0))
            lines.append(f'    <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="url(#connes-chord-grad)" stroke-width="{sw:.1f}" stroke-opacity="0.8" />')
            mx = (x1 + x2) / 2.0
            my = (y1 + y2) / 2.0
            lines.append(f'    <text x="{mx:.1f}" y="{my:.1f}" fill="#3fb950" font-family="monospace" font-size="9" font-weight="600" text-anchor="middle">{cd.connes_distance:.2f}</text>')

        # Draw State Nodes
        for i, (nx, ny) in enumerate(node_coords):
            st = result.states[i]
            lines.append(f'    <circle cx="{nx:.1f}" cy="{ny:.1f}" r="14" fill="#0d1117" stroke="#3fb950" stroke-width="2" filter="url(#glow)" />')
            lines.append(f'    <text x="{nx:.1f}" y="{ny + 4:.1f}" fill="#f0f6fc" font-family="system-ui, sans-serif" font-size="10" font-weight="700" text-anchor="middle">{html.escape(st.state_id)}</text>')
            # State label positioned radially outward
            ang = 2.0 * math.pi * i / max(1, num_s) - math.pi / 2.0
            lx = nx + 26 * math.cos(ang)
            ly = ny + 26 * math.sin(ang)
            lines.append(f'    <text x="{lx:.1f}" y="{ly:.1f}" fill="#c9d1d9" font-family="system-ui, sans-serif" font-size="9" text-anchor="middle">{html.escape(st.label)}</text>')

        # Distance Table Snippet
        lines.append('    <g transform="translate(16, 320)">')
        lines.append('      <text fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600">CONNES GEODESIC DISTANCES:</text>')
        dy = 18
        for cd in result.connes_distances[:4]:
            lines.append(f'      <text y="{dy}" fill="#c9d1d9" font-family="monospace" font-size="10">d_D({cd.state_id_a}, {cd.state_id_b}) = {cd.connes_distance:.3f} (Euc: {cd.euclidean_distance:.2f})</text>')
            dy += 18
        lines.append('    </g>')
        lines.append('  </g>')

        # 3. Right Panel: Commutator Dynamics & Non-Commutativity
        lines.append('  <!-- Panel 3: Commutators & Diagnostics -->')
        lines.append('  <g id="comm-panel" transform="translate(660, 90)">')
        lines.append('    <rect width="200" height="490" fill="#161b22" rx="8" stroke="#30363d" stroke-width="1.2" />')
        lines.append('    <text x="16" y="28" fill="#58a6ff" font-family="system-ui, sans-serif" font-size="13" font-weight="700">NC COMMUTATORS</text>')
        lines.append('    <line x1="16" y1="38" x2="184" y2="38" stroke="#30363d" stroke-width="1" />')

        cy_comm = 62
        lines.append(f'    <text x="16" y="{cy_comm}" fill="#8b949e" font-family="system-ui, sans-serif" font-size="10" font-weight="600">OBSERVABLE COMMUTATORS:</text>')
        cy_comm += 20
        for comm_name, c_val in result.commutator_norms.items():
            lines.append(f'    <text x="16" y="{cy_comm}" fill="#c9d1d9" font-family="monospace" font-size="10">{comm_name}:</text>')
            lines.append(f'    <text x="184" y="{cy_comm}" fill="#d29922" font-family="monospace" font-size="10" font-weight="600" text-anchor="end">{c_val:.3f}</text>')
            cy_comm += 22

        # Noncommutativity Index Box
        cy_comm += 15
        lines.append(f'    <line x1="16" y1="{cy_comm}" x2="184" y2="{cy_comm}" stroke="#30363d" stroke-width="1" />')
        cy_comm += 20
        lines.append(f'    <text x="16" y="{cy_comm}" fill="#8b949e" font-family="system-ui, sans-serif" font-size="10">FRAMING BIAS INDEX:</text>')
        cy_comm += 22
        lines.append(f'    <rect x="16" y="{cy_comm}" width="168" height="34" fill="#1f6feb" fill-opacity="0.15" rx="4" stroke="#58a6ff" stroke-width="1" />')
        lines.append(f'    <text x="100" y="{cy_comm + 22}" fill="#58a6ff" font-family="monospace" font-size="14" font-weight="700" text-anchor="middle">{result.framing_noncommutativity_index:.3f}</text>')

        # Mathematical Legend
        cy_comm += 65
        lines.append(f'    <g transform="translate(16, {cy_comm})">')
        lines.append('      <text fill="#8b949e" font-family="system-ui, sans-serif" font-size="9" font-weight="600">CONNES METRIC:</text>')
        lines.append('      <text y="16" fill="#c9d1d9" font-family="monospace" font-size="9">d_D(&#969;&#8321;, &#969;&#8322;) = sup |&#969;&#8321;(a)-&#969;&#8322;(a)|</text>')
        lines.append('      <text y="30" fill="#8b949e" font-family="system-ui, sans-serif" font-size="8">subject to ||[D, a]|| &le; 1</text>')
        lines.append('      <text y="50" fill="#8b949e" font-family="system-ui, sans-serif" font-size="9" font-weight="600">SPECTRAL TRIPLE:</text>')
        lines.append('      <text y="66" fill="#c9d1d9" font-family="monospace" font-size="9">(&#119964;, &#8459;, &#119967;)</text>')
        lines.append('      <text y="82" fill="#8b949e" font-family="system-ui, sans-serif" font-size="8">Noncommutative Geometry</text>')
        lines.append('    </g>')

        lines.append('  </g>')

        lines.append('</svg>')
        return "\n".join(lines)

    def generate_markdown_report(self, result: Optional[SpectralTripleResult] = None) -> str:
        """Generates a formal markdown analysis report on the Non-Commutative Spectral Triple."""
        if result is None:
            result = self.compute_spectral_analysis()

        lines = [
            "# Non-Commutative Spectral Triple & Connes Distance Analysis",
            "",
            "## Executive Summary",
            "",
            f"The non-commutative spectral triple (A, H, D) reveals a Hilbert state space of dimension {result.hilbert_dim}, stabilized by a self-adjoint Dirac operator with {len(result.dirac_eigenvalues)} characteristic resonance modes. Average framing non-commutativity across concept observables is {result.framing_noncommutativity_index:.4f}, demonstrating cognitive order-dependence and contextuality.",
            "",
            f"- **Hilbert Space Dimension:** {result.hilbert_dim}",
            f"- **Spectral Dimension (d_s):** {result.spectral_dimension:.3f}",
            f"- **Spectral Action S[D]:** {result.spectral_action:.4f}",
            f"- **Framing Non-Commutativity Index:** {result.framing_noncommutativity_index:.4f}",
            "",
            "## Dirac Operator Eigenvalue Spectrum",
            "",
            "| Mode | Eigenvalue (lambda) | Resonance Sign | Damping Weight exp(-lambda^2/2) |",
            "| :--- | :--- | :--- | :--- |",
        ]

        for idx, ev in enumerate(result.dirac_eigenvalues):
            sign_str = "Positive" if ev > 0 else ("Zero" if abs(ev) < 1e-4 else "Negative")
            weight = math.exp(-ev * ev / 2.0)
            lines.append(f"| Mode {idx+1} | `{ev:+.4f}` | {sign_str} | `{weight:.4f}` |")

        lines.extend([
            "",
            "## Connes Geodesic Spectral Distances",
            "",
            "| State Pair | State Labels | Connes Distance d_D | Euclidean Distance | Max-Separating Observable | Gradient Norm ||[D, a]|| |",
            "| :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for cd in result.connes_distances:
            lines.append(
                f"| `{cd.state_id_a} <-> {cd.state_id_b}` | {cd.label_a} vs {cd.label_b} | `{cd.connes_distance:.4f}` | {cd.euclidean_distance:.4f} | `{cd.optimal_observable}` | {cd.gradient_norm:.4f} |"
            )

        lines.extend([
            "",
            "## Non-Commutative Concept Observables",
            "",
            "| Observable | Label | Description | Operator Trace |",
            "| :--- | :--- | :--- | :--- |",
        ])

        for obs in result.observables:
            tr = sum(obs.matrix[k][k] for k in range(obs.dimension))
            lines.append(f"| `{obs.name}` | {obs.label} | {obs.description} | `{tr:.3f}` |")

        lines.extend([
            "",
            "## Framing Commutators [A, B]",
            "",
            "| Commutator | Frobenius Norm ||[A, B]|| | Non-Commutative Effect |",
            "| :--- | :--- | :--- |",
        ])

        for comm_name, c_val in result.commutator_norms.items():
            status = "Strong Order Effect" if c_val > 0.5 else "Weak Contextuality"
            lines.append(f"| `{comm_name}` | `{c_val:.4f}` | {status} |")

        lines.extend([
            "",
            "## Epistemic Architecture Notes",
            "",
            "1. **Connes Geodesic Distance:** In classical geometry, distance between points is measured along continuous paths. In non-commutative geometry, Connes distance measures the maximum discriminability between states across all observables whose non-commutative differential gradient satisfies ||[D, a]|| <= 1.",
            "2. **Cognitive Contextuality:** When two concept operators do not commute ([A, B] != 0), presenting concept A before B alters the epistemic state, proving that cognitive evaluation spaces cannot be represented on a purely commutative Boolean manifold.",
            "3. **Spectral Regularization:** The Dirac operator D acts as an intrinsic cognitive regularizer, preventing unbounded fluctuations and establishing an energy scale for concept state transitions.",
        ])

        return "\n".join(lines)

    def generate_html_viewer(self, result: Optional[SpectralTripleResult] = None) -> str:
        """Generates a standalone dark titanium HTML interactive viewer."""
        if result is None:
            result = self.compute_spectral_analysis()

        svg_content = self.render_svg(result)
        json_data = json.dumps(result.to_dict(), indent=2)

        html_str = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Non-Commutative Spectral Triple & Connes Distance Loom | DxSkills</title>
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
      <h1>Non-Commutative Spectral Triple & Connes Distance Loom</h1>
      <p class="subtitle">Autonomous Cognitive Spatial Scaffold: Dirac Operator Spectrum, Framing Commutators &amp; Geodesic Spectral Metrics</p>
    </header>

    <div class="grid">
      <div class="card">
        <div class="svg-container">
          {svg_content}
        </div>
      </div>

      <div class="card">
        <h2 style="color: var(--heading); font-size: 18px; margin-bottom: 12px;">Telemetry JSON Export</h2>
        <pre><code>{html.escape(json_data)}</code></pre>
      </div>
    </div>
  </div>
</body>
</html>
"""
        return html_str
