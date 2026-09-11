"""Unit tests for Autonomous Cognitive Spatial Multi-Modal Code Signature Synthesizer & Symbol Mesh.

Strict Quality Gate: Zero em dashes anywhere (use hyphens, commas, or parentheses).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from scripts.code_symbol_mesh import (
    CodeSymbol,
    CodeSymbolMesh,
    EncapsulationTier,
    SymbolKind,
    SymbolMeshTelemetry,
)


def test_empty_input_handling() -> None:
    """Ensure symbol mesh handles empty input gracefully without errors."""
    mesh = CodeSymbolMesh()
    symbols, edges, telemetry = mesh.analyze_mesh()

    assert len(symbols) == 0
    assert len(edges) == 0
    assert telemetry.total_symbols == 0
    assert telemetry.architectural_clarity_score == 1.0


def test_ast_source_parsing() -> None:
    """Verify AST parsing extracts classes, functions, signatures, and cyclomatic complexity."""
    source = '''
class SpatialRouter:
    """Dispatches spatial coordinate packets."""
    def __init__(self, buffer_size: int = 100):
        self.buffer_size = buffer_size

    def route_packet(self, packet_id: str) -> bool:
        if self.buffer_size > 0:
            return True
        return False

def standalone_helper(val: int) -> int:
    return val * 2
'''
    mesh = CodeSymbolMesh()
    mesh.load_source_text(source, filename="router.py")
    symbols, edges, telemetry = mesh.analyze_mesh()

    assert len(symbols) == 2
    sym_map = {s.name: s for s in symbols}

    assert "SpatialRouter" in sym_map
    router = sym_map["SpatialRouter"]
    assert router.kind == SymbolKind.CLASS
    assert router.line_number > 0
    assert len(router.signatures) > 0

    assert "standalone_helper" in sym_map
    helper = sym_map["standalone_helper"]
    assert helper.kind == SymbolKind.FUNCTION
    assert helper.signatures[0].startswith("def standalone_helper")


def test_coupling_and_leaky_abstraction_detection() -> None:
    """Verify detection of high fan-out coupling exceeding boundary limits."""
    mesh = CodeSymbolMesh(max_allowed_coupling=3)
    data = {
        "symbols": {
            "god_class": {
                "name": "GodController",
                "kind": "class",
                "dependencies": ["auth", "database", "logger", "email", "payment"],
                "cyclomatic_complexity": 6.0,
            },
            "auth": {"name": "AuthService", "kind": "interface", "dependencies": []},
            "database": {"name": "DatabasePool", "kind": "class", "dependencies": []},
            "logger": {"name": "EventLogger", "kind": "class", "dependencies": []},
            "email": {"name": "EmailNotifier", "kind": "class", "dependencies": []},
            "payment": {"name": "PaymentGateway", "kind": "class", "dependencies": []},
        }
    }
    mesh.load_dict(data)
    symbols, edges, telemetry = mesh.analyze_mesh()

    sym_map = {s.symbol_id: s for s in symbols}
    god = sym_map["god_class"]

    assert god.encapsulation_tier == EncapsulationTier.LEAKY_ABSTRACTION
    assert len(god.boundary_leaks) >= 1
    assert telemetry.leaky_abstractions_count >= 1
    assert telemetry.architectural_clarity_score < 1.0


def test_cyclic_dependency_detection() -> None:
    """Verify identification of circular dependency loops across components."""
    mesh = CodeSymbolMesh()
    data = {
        "symbols": {
            "module_a": {"name": "ModuleA", "kind": "module", "dependencies": ["module_b"]},
            "module_b": {"name": "ModuleB", "kind": "module", "dependencies": ["module_a"]},
            "module_c": {"name": "ModuleC", "kind": "module", "dependencies": []},
        }
    }
    mesh.load_dict(data)
    symbols, edges, telemetry = mesh.analyze_mesh()

    sym_map = {s.symbol_id: s for s in symbols}
    assert sym_map["module_a"].encapsulation_tier == EncapsulationTier.CYCLIC_RISK
    assert sym_map["module_b"].encapsulation_tier == EncapsulationTier.CYCLIC_RISK
    assert sym_map["module_c"].encapsulation_tier == EncapsulationTier.STABLE_CONTRACT
    assert telemetry.cyclic_dependencies_count == 2


def test_canvas_export(tmp_path: Path) -> None:
    """Verify export to Obsidian .canvas file with encapsulation color codes."""
    mesh = CodeSymbolMesh()
    data = {
        "symbols": {
            "api": {
                "name": "UserAPI",
                "kind": "interface",
                "signatures": ["get_user(id)", "update_user(id, data)"],
                "dependencies": ["repo"],
            },
            "repo": {
                "name": "UserRepository",
                "kind": "class",
                "signatures": ["find(id)", "save(entity)"],
                "dependencies": [],
            },
        }
    }
    mesh.load_dict(data)

    out_file = str(tmp_path / "symbol_mesh.canvas")
    res = mesh.to_canvas(out_file, canvas_title="Architecture Map")

    assert Path(out_file).exists()
    assert "nodes" in res
    assert "edges" in res
    assert len(res["nodes"]) == 2
    assert "Contract:" in res["nodes"][0]["text"]


def test_svg_export(tmp_path: Path) -> None:
    """Verify publication-grade SVG generation with dark titanium styling."""
    mesh = CodeSymbolMesh()
    data = {
        "symbols": {
            "c1": {"name": "CoreModel", "kind": "class", "dependencies": ["c2"]},
            "c2": {"name": "DatabaseDriver", "kind": "class", "dependencies": []},
        }
    }
    mesh.load_dict(data)

    out_file = str(tmp_path / "symbol_mesh.svg")
    svg_str = mesh.to_svg(out_file, width=1200, height=800)

    assert Path(out_file).exists()
    assert "<svg" in svg_str
    assert "</svg>" in svg_str
    assert "#0B0F17" in svg_str
    assert "Code Symbol Telemetry" in svg_str
    assert "CoreModel" in svg_str


def test_ascii_report() -> None:
    """Verify terminal ASCII summary report output."""
    mesh = CodeSymbolMesh()
    data = {
        "symbols": {
            "s1": {"name": "AuthService", "kind": "class", "dependencies": []},
        }
    }
    mesh.load_dict(data)
    symbols, edges, telemetry = mesh.analyze_mesh()
    report = mesh.render_ascii_mesh(telemetry)

    assert "Spatial Multi-Modal Code Signature Synthesizer & Symbol Mesh" in report
    assert "Total Architectural Symbols:" in report
    assert "AuthService" in report


def test_zero_em_dashes_in_module() -> None:
    """Verify neither script nor test contains em dashes."""
    root_dir = Path(__file__).parent.parent
    script_path = root_dir / "scripts" / "code_symbol_mesh.py"
    test_path = root_dir / "tests" / "test_code_symbol_mesh.py"

    for p in [script_path, test_path]:
        content = p.read_text(encoding="utf-8")
        assert "\u2014" not in content, f"Em dash found in {p.name}"
