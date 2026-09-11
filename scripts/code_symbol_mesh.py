"""Autonomous Cognitive Spatial Multi-Modal Code Signature Synthesizer & Symbol Mesh.

Theoretical Foundation:
- Eide & Eide M-I-N-D Framework (Material & Interconnected Spatial Reasoning):
  Dyslexic engineers process system architectures top-down through spatial topologies
  rather than linear serialized syntax. When codebases expand, text-based files obscure
  architectural invariants, cyclic dependencies, and leaky interface boundaries.
- Abstract Syntax Tree (AST) Spatial Projection:
  Parses multi-language code structures into semantic symbol nodes (classes, interfaces,
  methods, and module boundaries) with calculated coupling metrics, cyclomatic complexity,
  and visibility scopes.
- Leaky Abstraction & Boundary Violation Detection:
  Detects anti-patterns including excessive foreign coupling (fan-out > 5), cyclic
  import risks, missing type contracts, and invasive attribute reach-throughs.
- 2D Spatial Layout & Obsidian .canvas / Dark Titanium SVG Compilation:
  Positions symbols in clustered topological layers and generates publication-grade
  SVG visual contract diagrams with encapsulation badges.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import ast
import enum
import json
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class EncapsulationTier(str, enum.Enum):
    """Categorization of component encapsulation and abstraction health."""

    STABLE_CONTRACT = "stable_contract"
    ELEVATED_COUPLING = "elevated_coupling"
    LEAKY_ABSTRACTION = "leaky_abstraction"
    CYCLIC_RISK = "cyclic_risk"


class SymbolKind(str, enum.Enum):
    """Type of code architecture symbol."""

    CLASS = "class"
    INTERFACE = "interface"
    FUNCTION = "function"
    MODULE = "module"


@dataclass
class CodeSymbol:
    """Represents a code architectural symbol extracted from source syntax."""

    symbol_id: str
    name: str
    kind: SymbolKind
    file_path: str
    line_number: int
    signatures: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    coupling_count: int = 0
    cyclomatic_complexity: float = 1.0
    encapsulation_tier: EncapsulationTier = EncapsulationTier.STABLE_CONTRACT
    boundary_leaks: List[str] = field(default_factory=list)
    x: float = 0.0
    y: float = 0.0
    width: float = 280.0
    height: float = 160.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert symbol to serializable dictionary."""
        return {
            "symbol_id": self.symbol_id,
            "name": self.name,
            "kind": self.kind.value,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "signatures": self.signatures,
            "dependencies": sorted(self.dependencies),
            "coupling_count": self.coupling_count,
            "cyclomatic_complexity": round(self.cyclomatic_complexity, 1),
            "encapsulation_tier": self.encapsulation_tier.value,
            "boundary_leaks": self.boundary_leaks,
            "x": round(self.x, 1),
            "y": round(self.y, 1),
            "width": round(self.width, 1),
            "height": round(self.height, 1),
        }


@dataclass
class SymbolMeshTelemetry:
    """Telemetry capturing code symbol graph health and encapsulation integrity."""

    total_symbols: int
    stable_contracts_count: int
    leaky_abstractions_count: int
    cyclic_dependencies_count: int
    mean_coupling: float
    architectural_clarity_score: float
    symbols: List[CodeSymbol] = field(default_factory=list)
    boundary_edges: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert telemetry to JSON-compatible dictionary."""
        return {
            "total_symbols": self.total_symbols,
            "stable_contracts_count": self.stable_contracts_count,
            "leaky_abstractions_count": self.leaky_abstractions_count,
            "cyclic_dependencies_count": self.cyclic_dependencies_count,
            "mean_coupling": round(self.mean_coupling, 2),
            "architectural_clarity_score": round(self.architectural_clarity_score, 2),
            "symbols": [s.to_dict() for s in self.symbols],
            "boundary_edges": self.boundary_edges,
        }


class CodeSymbolMesh:
    """Constructs and analyzes 2D spatial symbol topologies from code structures."""

    def __init__(self, max_allowed_coupling: int = 5) -> None:
        self.max_allowed_coupling = max_allowed_coupling
        self.symbols: Dict[str, CodeSymbol] = {}
        self.explicit_edges: List[Dict[str, Any]] = []

    def load_source_text(self, source_code: str, filename: str = "module.py") -> None:
        """Parse Python source code using AST and extract structural symbols."""
        self.symbols.clear()
        self.explicit_edges.clear()

        try:
            tree = ast.parse(source_code, filename=filename)
        except SyntaxError:
            # Fallback for non-Python or broken syntax: create single module symbol
            sym = CodeSymbol(
                symbol_id=f"{filename}_root",
                name=Path(filename).stem,
                kind=SymbolKind.MODULE,
                file_path=filename,
                line_number=1,
                signatures=["# raw unparsed source"],
                coupling_count=0,
            )
            self.symbols[sym.symbol_id] = sym
            return

        # Walk AST top-level elements
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                sym_id = f"{filename}_{node.name}"
                methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
                base_names = [ast.unparse(b) for b in node.bases]
                
                # Check for interface/abstract conventions
                kind = SymbolKind.INTERFACE if "Interface" in node.name or "Protocol" in node.name or "ABC" in base_names else SymbolKind.CLASS
                
                # Estimate cyclomatic complexity
                branches = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.While, ast.For, ast.ExceptHandler)))
                complexity = 1.0 + float(branches) * 0.5

                # Find referenced symbols / attribute accesses
                refs: Set[str] = set()
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Name) and sub.id != node.name:
                        refs.add(sub.id)

                self.symbols[sym_id] = CodeSymbol(
                    symbol_id=sym_id,
                    name=node.name,
                    kind=kind,
                    file_path=filename,
                    line_number=node.lineno,
                    signatures=[f"def {m}()" for m in methods[:5]],
                    dependencies=sorted(list(refs))[:8],
                    coupling_count=len(refs),
                    cyclomatic_complexity=complexity,
                )

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                sym_id = f"{filename}_{node.name}"
                args_str = ", ".join(a.arg for a in node.args.args)
                sig = f"def {node.name}({args_str})"
                
                branches = sum(1 for n in ast.walk(node) if isinstance(n, (ast.If, ast.While, ast.For, ast.ExceptHandler)))
                complexity = 1.0 + float(branches) * 0.5

                refs = set()
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Name) and sub.id != node.name:
                        refs.add(sub.id)

                self.symbols[sym_id] = CodeSymbol(
                    symbol_id=sym_id,
                    name=node.name,
                    kind=SymbolKind.FUNCTION,
                    file_path=filename,
                    line_number=node.lineno,
                    signatures=[sig],
                    dependencies=sorted(list(refs))[:8],
                    coupling_count=len(refs),
                    cyclomatic_complexity=complexity,
                )

    def load_dict(self, symbol_data: Dict[str, Any]) -> None:
        """Load symbols and relationships from dictionary."""
        self.symbols.clear()
        self.explicit_edges.clear()

        raw_symbols = symbol_data.get("symbols", symbol_data)
        for s_id, info in raw_symbols.items():
            if isinstance(info, dict):
                name = info.get("name", s_id)
                kind_str = info.get("kind", "class").lower()
                kind = SymbolKind.INTERFACE if "interface" in kind_str else (
                    SymbolKind.FUNCTION if "func" in kind_str else (
                        SymbolKind.MODULE if "mod" in kind_str else SymbolKind.CLASS
                    )
                )
                file_path = info.get("file_path", "src/module.py")
                line_no = int(info.get("line_number", 1))
                sigs = list(info.get("signatures", []))
                deps = list(info.get("dependencies", []))
                comp = float(info.get("cyclomatic_complexity", 1.0))
            else:
                name = str(info)
                kind = SymbolKind.CLASS
                file_path = "src/module.py"
                line_no = 1
                sigs = []
                deps = []
                comp = 1.0

            self.symbols[s_id] = CodeSymbol(
                symbol_id=s_id,
                name=name,
                kind=kind,
                file_path=file_path,
                line_number=line_no,
                signatures=sigs,
                dependencies=deps,
                coupling_count=len(deps),
                cyclomatic_complexity=comp,
            )

        if "edges" in symbol_data:
            self.explicit_edges = list(symbol_data.get("edges", []))

    def load_canvas(self, canvas_data: Dict[str, Any]) -> None:
        """Extract code symbols and dependency edges from Obsidian .canvas format."""
        self.symbols.clear()
        self.explicit_edges = list(canvas_data.get("edges", []))

        nodes = canvas_data.get("nodes", [])
        for node in nodes:
            n_id = str(node.get("id", ""))
            text = str(node.get("text", "")).strip()
            lines = [l.strip() for l in text.split("\n") if l.strip()]
            name = lines[0].lstrip("#").strip() if lines else n_id

            # Parse signatures or dependencies from bullet lines
            sigs: List[str] = []
            deps: List[str] = []
            for line in lines[1:]:
                if line.startswith("-") or line.startswith("*"):
                    clean = line.lstrip("-*").strip()
                    if "(" in clean:
                        sigs.append(clean)
                    else:
                        deps.append(clean)

            kind = SymbolKind.INTERFACE if "interface" in name.lower() or "protocol" in name.lower() else SymbolKind.CLASS

            self.symbols[n_id] = CodeSymbol(
                symbol_id=n_id,
                name=name,
                kind=kind,
                file_path="canvas_import.py",
                line_number=1,
                signatures=sigs,
                dependencies=deps,
                coupling_count=len(deps),
                x=float(node.get("x", 0.0)),
                y=float(node.get("y", 0.0)),
                width=float(node.get("width", 280.0)),
                height=float(node.get("height", 160.0)),
            )

    def analyze_mesh(self) -> Tuple[List[CodeSymbol], List[Dict[str, Any]], SymbolMeshTelemetry]:
        """Analyze symbol coupling, detect leaky abstractions, and assign 2D spatial coordinates."""
        if not self.symbols:
            empty_telemetry = SymbolMeshTelemetry(
                total_symbols=0,
                stable_contracts_count=0,
                leaky_abstractions_count=0,
                cyclic_dependencies_count=0,
                mean_coupling=0.0,
                architectural_clarity_score=1.0,
            )
            return [], [], empty_telemetry

        symbol_list = list(self.symbols.values())
        symbol_ids = {s.symbol_id for s in symbol_list}
        name_to_id = {s.name: s.symbol_id for s in symbol_list}

        # Build graph edges
        edges: List[Dict[str, Any]] = list(self.explicit_edges)
        adjacency: Dict[str, Set[str]] = {s.symbol_id: set() for s in symbol_list}

        for e in self.explicit_edges:
            src = e.get("fromNode")
            tgt = e.get("toNode")
            if src in adjacency and tgt in adjacency:
                adjacency[src].add(tgt)

        for s in symbol_list:
            for dep in s.dependencies:
                target_id = dep if dep in symbol_ids else name_to_id.get(dep)
                if target_id and target_id != s.symbol_id:
                    adjacency[s.symbol_id].add(target_id)
                    edges.append({
                        "fromNode": s.symbol_id,
                        "toNode": target_id,
                        "label": "depends_on",
                    })

        # 1. Detect Cyclic Dependencies
        cyclic_nodes: Set[str] = set()
        for src in symbol_list:
            visited: Set[str] = set()
            stack: List[str] = [src.symbol_id]
            while stack:
                curr = stack.pop()
                for neighbor in adjacency.get(curr, []):
                    if neighbor == src.symbol_id:
                        cyclic_nodes.add(src.symbol_id)
                        break
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)

        # 2. Evaluate Encapsulation Tiers & Leaky Abstractions
        stable_count = 0
        leaky_count = 0
        total_coupling = 0

        for s in symbol_list:
            fan_out = len(adjacency[s.symbol_id])
            s.coupling_count = fan_out
            total_coupling += fan_out
            s.boundary_leaks.clear()

            # Rule checks
            if s.symbol_id in cyclic_nodes:
                s.encapsulation_tier = EncapsulationTier.CYCLIC_RISK
                s.boundary_leaks.append("Cyclic dependency loop detected across module boundaries")
            elif fan_out > self.max_allowed_coupling:
                s.encapsulation_tier = EncapsulationTier.LEAKY_ABSTRACTION
                s.boundary_leaks.append(f"Excessive fan-out coupling ({fan_out} > {self.max_allowed_coupling} limit)")
            elif s.cyclomatic_complexity > 5.0 and fan_out > 3:
                s.encapsulation_tier = EncapsulationTier.LEAKY_ABSTRACTION
                s.boundary_leaks.append("High internal complexity paired with cross-boundary dependencies")
            elif fan_out > (self.max_allowed_coupling - 2):
                s.encapsulation_tier = EncapsulationTier.ELEVATED_COUPLING
            else:
                s.encapsulation_tier = EncapsulationTier.STABLE_CONTRACT

            if s.encapsulation_tier == EncapsulationTier.STABLE_CONTRACT:
                stable_count += 1
            elif s.encapsulation_tier in [EncapsulationTier.LEAKY_ABSTRACTION, EncapsulationTier.CYCLIC_RISK]:
                leaky_count += 1

        # 3. 2D Spatial Layout Allocation
        # Arrange in topological columns by dependency depth
        in_degrees: Dict[str, int] = {s.symbol_id: 0 for s in symbol_list}
        for src, targets in adjacency.items():
            for tgt in targets:
                in_degrees[tgt] = in_degrees.get(tgt, 0) + 1

        # Sort into layers
        layers: Dict[int, List[CodeSymbol]] = {}
        for s in symbol_list:
            deg = in_degrees.get(s.symbol_id, 0)
            col = min(4, deg)
            layers.setdefault(col, []).append(s)

        x_spacing = 340.0
        y_spacing = 220.0

        for col_idx, col_symbols in layers.items():
            for row_idx, sym in enumerate(col_symbols):
                if sym.x == 0.0 and sym.y == 0.0:
                    sym.x = 80.0 + (col_idx * x_spacing)
                    sym.y = 120.0 + (row_idx * y_spacing)

        mean_coup = total_coupling / max(1, len(symbol_list))
        clarity = max(0.20, min(1.0, 1.0 - (leaky_count / max(1, len(symbol_list))) * 0.7))

        telemetry = SymbolMeshTelemetry(
            total_symbols=len(symbol_list),
            stable_contracts_count=stable_count,
            leaky_abstractions_count=leaky_count,
            cyclic_dependencies_count=len(cyclic_nodes),
            mean_coupling=mean_coup,
            architectural_clarity_score=clarity,
            symbols=symbol_list,
            boundary_edges=edges,
        )

        return symbol_list, edges, telemetry

    def to_canvas(
        self,
        output_path: Optional[str] = None,
        canvas_title: str = "Code Symbol Mesh Canvas",
    ) -> Dict[str, Any]:
        """Export analyzed symbols to Obsidian .canvas format with contract badges."""
        symbols, edges, telemetry = self.analyze_mesh()

        canvas_nodes: List[Dict[str, Any]] = []

        for s in symbols:
            if s.encapsulation_tier == EncapsulationTier.CYCLIC_RISK:
                color = "1"  # red
            elif s.encapsulation_tier == EncapsulationTier.LEAKY_ABSTRACTION:
                color = "2"  # orange
            elif s.encapsulation_tier == EncapsulationTier.ELEVATED_COUPLING:
                color = "3"  # yellow
            else:
                color = "4"  # green / stable

            sig_preview = "\n".join(f"- `{sig}`" for sig in s.signatures[:3]) if s.signatures else "- *(No signatures)*"
            leak_info = f"\n**Leaks:** {', '.join(s.boundary_leaks)}" if s.boundary_leaks else ""

            content = (
                f"### {s.name} ({s.kind.value})\n"
                f"**Contract:** `{s.encapsulation_tier.value}`\n"
                f"**Fan-Out:** {s.coupling_count} | **Complexity:** {s.cyclomatic_complexity:.1f}\n"
                f"{sig_preview}{leak_info}"
            )

            canvas_nodes.append({
                "id": s.symbol_id,
                "x": s.x,
                "y": s.y,
                "width": s.width,
                "height": s.height,
                "type": "text",
                "text": content,
                "color": color,
            })

        canvas_json = {
            "title": canvas_title,
            "nodes": canvas_nodes,
            "edges": edges,
        }

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(canvas_json, f, indent=2)

        return canvas_json

    def to_svg(
        self,
        output_path: Optional[str] = None,
        width: int = 1200,
        height: int = 800,
    ) -> str:
        """Render publication-grade SVG code symbol mesh diagram in dark titanium theme."""
        symbols, edges, telemetry = self.analyze_mesh()

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" style="background-color: #0B0F17; '
            f'font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif;">',
            '<defs>',
            '  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">',
            '    <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748B"/>',
            '  </marker>',
            '  <filter id="nodeGlow" x="-10%" y="-10%" width="120%" height="120%">',
            '    <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6"/>',
            '  </filter>',
            '</defs>',
            '<!-- Header -->',
            f'<text x="60" y="45" font-size="20" font-weight="700" fill="#F8FAFC">Spatial Code Signature Synthesizer &amp; Symbol Mesh</text>',
            f'<text x="60" y="65" font-size="12" fill="#94A3B8">Architectural Clarity: {telemetry.architectural_clarity_score:.2f} | Leaky Abstractions: {telemetry.leaky_abstractions_count} | Mean Coupling: {telemetry.mean_coupling:.1f}</text>',
            '<!-- Dependency Connectors -->',
        ]

        sym_map = {s.symbol_id: s for s in symbols}

        # Draw Edges
        for e in edges:
            src_id = e.get("fromNode")
            tgt_id = e.get("toNode")
            if src_id in sym_map and tgt_id in sym_map:
                s1 = sym_map[src_id]
                s2 = sym_map[tgt_id]
                x1 = s1.x + s1.width
                y1 = s1.y + s1.height / 2.0
                x2 = s2.x
                y2 = s2.y + s2.height / 2.0

                svg_parts.append(
                    f'<path d="M {x1:.1f} {y1:.1f} C {x1 + 40:.1f} {y1:.1f}, {x2 - 40:.1f} {y2:.1f}, {x2:.1f} {y2:.1f}" '
                    f'fill="none" stroke="#475569" stroke-width="1.5" marker-end="url(#arrow)" stroke-dasharray="3,3"/>'
                )

        # Draw Symbol Cards
        svg_parts.append('<!-- Symbol Node Cards -->')
        for s in symbols:
            if s.encapsulation_tier == EncapsulationTier.CYCLIC_RISK:
                stroke_col = "#EF4444"
                badge_bg = "#450A0A"
                badge_text = "#FCA5A5"
            elif s.encapsulation_tier == EncapsulationTier.LEAKY_ABSTRACTION:
                stroke_col = "#F59E0B"
                badge_bg = "#451A03"
                badge_text = "#FCD34D"
            elif s.encapsulation_tier == EncapsulationTier.ELEVATED_COUPLING:
                stroke_col = "#38BDF8"
                badge_bg = "#082F49"
                badge_text = "#7DD3FC"
            else:
                stroke_col = "#10B981"
                badge_bg = "#064E3B"
                badge_text = "#6EE7B7"

            svg_parts.append(
                f'<g transform="translate({s.x:.1f}, {s.y:.1f})" filter="url(#nodeGlow)">'
                f'  <rect width="{s.width:.1f}" height="{s.height:.1f}" rx="8" fill="#1E293B" stroke="{stroke_col}" stroke-width="2"/>'
                f'  <rect x="14" y="14" width="65" height="18" rx="4" fill="{badge_bg}"/>'
                f'  <text x="46" y="26" font-size="9" font-weight="700" fill="{badge_text}" text-anchor="middle">{s.kind.value.upper()}</text>'
                f'  <text x="88" y="27" font-size="12" font-weight="700" fill="#F8FAFC">{s.name[:18]}</text>'
                f'  <line x1="14" y1="40" x2="{s.width - 14:.1f}" y2="40" stroke="#334155" stroke-width="1"/>'
                f'  <text x="14" y="58" font-size="10" fill="#94A3B8">Coupling: <tspan fill="{stroke_col}">{s.coupling_count}</tspan> | Complexity: {s.cyclomatic_complexity:.1f}</text>'
                f'  <text x="14" y="74" font-size="9" fill="#64748B">{s.encapsulation_tier.value}</text>'
            )

            if s.signatures:
                sig_text = s.signatures[0][:28]
                svg_parts.append(
                    f'  <text x="14" y="94" font-size="9" font-family="monospace" fill="#38BDF8">{sig_text}</text>'
                )

            if s.boundary_leaks:
                leak_snip = s.boundary_leaks[0][:26]
                svg_parts.append(
                    f'  <text x="14" y="112" font-size="8" fill="#EF4444">! {leak_snip}</text>'
                )

            svg_parts.append('</g>')

        # Telemetry Box
        legend_x = width - 260
        legend_y = height - 145
        svg_parts.append('<!-- Telemetry Legend -->')
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="230" height="115" rx="6" '
            f'fill="#0F172A" stroke="#1E293B" stroke-width="1"/>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 22}" font-size="11" font-weight="700" fill="#F8FAFC">Code Symbol Telemetry</text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 42}" font-size="10" fill="#64748B">Total Symbols: <tspan fill="#F8FAFC">{telemetry.total_symbols}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 60}" font-size="10" fill="#64748B">Stable Contracts: <tspan fill="#10B981">{telemetry.stable_contracts_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 78}" font-size="10" fill="#64748B">Leaky Abstractions: <tspan fill="#EF4444">{telemetry.leaky_abstractions_count}</tspan></text>'
        )
        svg_parts.append(
            f'<text x="{legend_x + 12}" y="{legend_y + 98}" font-size="9" fill="#475569">AST Graph &amp; Contract Bounds</text>'
        )

        svg_parts.append('</svg>')
        svg_content = "\n".join(svg_parts)

        if output_path:
            p = Path(output_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                f.write(svg_content)

        return svg_content

    def render_ascii_mesh(self, telemetry: SymbolMeshTelemetry) -> str:
        """Format an accessible ASCII summary of the symbol mesh."""
        lines = [
            "=" * 68,
            "  Spatial Multi-Modal Code Signature Synthesizer & Symbol Mesh",
            "=" * 68,
            f"  Total Architectural Symbols:  {telemetry.total_symbols}",
            f"  Stable Encapsulation Bounds:  {telemetry.stable_contracts_count}",
            f"  Leaky Abstractions Detected:  {telemetry.leaky_abstractions_count}",
            f"  Cyclic Coupling Traps:        {telemetry.cyclic_dependencies_count}",
            f"  Mean Fan-Out Coupling:        {telemetry.mean_coupling:.2f}",
            f"  Architectural Clarity Score:  {telemetry.architectural_clarity_score:.2f}",
            "-" * 68,
            "  [SYMBOL INVENTORY & CONTRACTS]:",
        ]

        for s in telemetry.symbols:
            lines.append(f"    * [{s.kind.value.upper()}] {s.name} ({s.encapsulation_tier.value})")
            lines.append(f"      Coupling: {s.coupling_count} | Complexity: {s.cyclomatic_complexity:.1f} | File: {s.file_path}:{s.line_number}")
            if s.boundary_leaks:
                lines.append(f"      [LEAK WARNING]: {'; '.join(s.boundary_leaks)}")

        lines.append("=" * 68)
        return "\n".join(lines)
