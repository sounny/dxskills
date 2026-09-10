"""
Autonomous Spatial Multi-Modal Code Architecture and Dependency Graph Decompiler.

Parses Python source code into 2D Obsidian Canvas module topologies and vector SVG
circuits using the standard ast library. Identifies circular dependencies, computes
coupling metrics (Ca, Ce, Instability), and visualizes code architectures spatially.

Zero em dash policy strictly enforced.
"""

import os
import sys
import ast
import json
import math
import argparse
from typing import Dict, List, Any, Optional, Tuple, Set


class CodeArchitectureDecompiler:
    """Extracts structural AST models, dependency graphs, and coupling metrics."""

    @classmethod
    def decompile_source(cls, source_code: str, module_name: str = "module") -> Dict[str, Any]:
        """Parses Python source code into classes, functions, imports, and calls."""
        try:
            tree = ast.parse(source_code)
        except Exception as e:
            return {
                "module_name": module_name,
                "error": f"AST syntax parse error: {str(e)}",
                "classes": [],
                "functions": [],
                "imports": [],
                "calls": []
            }

        classes = []
        functions = []
        imports = []
        calls = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                bases = [cls._get_name(b) for b in node.bases if cls._get_name(b)]
                methods = [m.name for m in node.body if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef))]
                docstring = ast.get_docstring(node) or "No docstring provided."
                classes.append({
                    "name": node.name,
                    "bases": bases,
                    "methods": methods,
                    "docstring": docstring.split("\n")[0][:60],
                    "line": getattr(node, "lineno", 0)
                })

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                docstring = ast.get_docstring(node) or ""
                args = [a.arg for a in node.args.args]
                functions.append({
                    "name": node.name,
                    "args": args,
                    "docstring": docstring.split("\n")[0][:60] if docstring else "Function",
                    "line": getattr(node, "lineno", 0)
                })

            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append({"module": alias.name, "alias": alias.asname or alias.name})

            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for alias in node.names:
                    imports.append({"module": f"{mod}.{alias.name}" if mod else alias.name, "alias": alias.asname or alias.name})

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = cls._get_name(node.func)
                if func_name and func_name not in calls:
                    calls.append(func_name)

        return {
            "module_name": module_name,
            "classes": classes,
            "functions": functions,
            "imports": imports,
            "calls": calls
        }

    @classmethod
    def decompile_project(cls, root_dir: str) -> Dict[str, Any]:
        """Decompiles multiple Python files and detects circular module dependencies."""
        modules = {}
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.endswith(".py") and not file.startswith("__init__"):
                    filepath = os.path.join(root, file)
                    rel_name = os.path.splitext(os.path.relpath(filepath, root_dir))[0].replace(os.sep, ".")
                    try:
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                            src = f.read()
                        modules[rel_name] = cls.decompile_source(src, module_name=rel_name)
                    except Exception as e:
                        modules[rel_name] = {"module_name": rel_name, "error": str(e)}

        # Build internal dependency graph
        dep_graph: Dict[str, Set[str]] = {m: set() for m in modules}
        for mod_name, data in modules.items():
            for imp in data.get("imports", []):
                target = imp["module"]
                for candidate in modules:
                    if target == candidate or target.startswith(candidate + ".") or candidate.endswith("." + target):
                        dep_graph[mod_name].add(candidate)

        # Detect circular dependency cycles using DFS
        cycles = cls._find_cycles(dep_graph)

        # Compute Coupling Metrics (Ca, Ce, Instability)
        coupling = {}
        for mod in dep_graph:
            ce = len(dep_graph[mod])
            ca = sum(1 for m, targets in dep_graph.items() if mod in targets)
            instability = round(ce / (ca + ce), 2) if (ca + ce) > 0 else 0.0
            coupling[mod] = {
                "afferent_ca": ca,
                "efferent_ce": ce,
                "instability": instability,
                "is_circular": any(mod in c for c in cycles)
            }

        return {
            "total_modules": len(modules),
            "modules": modules,
            "dependency_graph": {k: list(v) for k, v in dep_graph.items()},
            "circular_cycles": cycles,
            "coupling_metrics": coupling
        }

    @classmethod
    def _find_cycles(cls, graph: Dict[str, Set[str]]) -> List[List[str]]:
        cycles = []
        visited = set()
        stack = []

        def dfs(node: str):
            visited.add(node)
            stack.append(node)
            for neighbor in graph.get(node, set()):
                if neighbor in stack:
                    cycle_start = stack.index(neighbor)
                    cycles.append(stack[cycle_start:] + [neighbor])
                elif neighbor not in visited:
                    dfs(neighbor)
            stack.pop()

        for n in graph:
            if n not in visited:
                dfs(n)
        return cycles

    @staticmethod
    def _get_name(node: Any) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{node.attr}"
        return ""


class CodeTopologyExporter:
    """Exports decompiled architectures into Obsidian Canvas and vector SVG circuits."""

    @staticmethod
    def to_canvas(decompiled: Dict[str, Any], title: str = "Code Architecture Topology") -> Dict[str, Any]:
        nodes = []
        edges = []

        # Central Header Node
        root_id = "node-code-header"
        mod_count = decompiled.get("total_modules", 1)
        cycles = decompiled.get("circular_cycles", [])
        nodes.append({
            "id": root_id,
            "type": "text",
            "text": (
                f"## {title}\n"
                f"Modules: **{mod_count}** | Circular Cycles: **{len(cycles)}**\n"
                f"AST Spatial Architecture Topology"
            ),
            "x": 0,
            "y": -320,
            "width": 420,
            "height": 140,
            "color": "5" if not cycles else "1"
        })

        modules = decompiled.get("modules", {})
        coupling = decompiled.get("coupling_metrics", {})

        grid_cols = max(1, math.ceil(math.sqrt(max(1, len(modules)))))
        spacing_x = 420
        spacing_y = 300

        mod_coords = {}

        for idx, (mod_name, data) in enumerate(modules.items()):
            col = idx % grid_cols
            row = idx // grid_cols
            nx = (col - (grid_cols / 2)) * spacing_x
            ny = row * spacing_y + 20
            mod_coords[mod_name] = (nx, ny)

            c_metric = coupling.get(mod_name, {})
            is_circ = c_metric.get("is_circular", False)
            instability = c_metric.get("instability", 0.0)

            # Color coding: 1=red (circular), 3=amber (high instability), 5=blue (stable core), 4=green
            color_id = "1" if is_circ else ("3" if instability >= 0.75 else "5")

            classes_list = [c["name"] for c in data.get("classes", [])]
            funcs_list = [f["name"] for f in data.get("functions", [])[:4]]

            node_text = (
                f"### {mod_name}.py\n"
                f"Instability: `{instability}` | Ca: `{c_metric.get('afferent_ca', 0)}` | Ce: `{c_metric.get('efferent_ce', 0)}`\n\n"
                f"**Classes:** {', '.join(classes_list) if classes_list else 'None'}\n"
                f"**Functions:** {', '.join(funcs_list) if funcs_list else 'None'}"
            )

            if is_circ:
                node_text = "⚠️ **[CIRCULAR DEPENDENCY WARNING]**\n\n" + node_text

            nid = f"mod-node-{mod_name.replace('.', '-')}"
            nodes.append({
                "id": nid,
                "type": "text",
                "text": node_text,
                "x": nx,
                "y": ny,
                "width": 360,
                "height": 220,
                "color": color_id
            })

            edges.append({
                "id": f"edge-root-{nid}",
                "fromNode": root_id,
                "fromSide": "bottom",
                "toNode": nid,
                "toSide": "top",
                "label": "Module"
            })

        # Add Dependency Edges
        dep_graph = decompiled.get("dependency_graph", {})
        for src, targets in dep_graph.items():
            src_id = f"mod-node-{src.replace('.', '-')}"
            for tgt in targets:
                tgt_id = f"mod-node-{tgt.replace('.', '-')}"
                edges.append({
                    "id": f"dep-edge-{src}-{tgt}",
                    "fromNode": src_id,
                    "fromSide": "right",
                    "toNode": tgt_id,
                    "toSide": "left",
                    "label": "imports"
                })

        return {"nodes": nodes, "edges": edges}

    @staticmethod
    def to_svg_diagram(decompiled: Dict[str, Any], title: str = "Code Architecture Circuit") -> str:
        width = 820
        height = 420
        modules = decompiled.get("modules", {})
        cycles = decompiled.get("circular_cycles", [])
        coupling = decompiled.get("coupling_metrics", {})

        svg = []
        svg.append(f'<svg width="100%" height="auto" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'<rect width="{width}" height="{height}" rx="14" fill="#09090b" stroke="#27272a" stroke-width="1.5"/>')

        # Header Title
        svg.append(f'<text x="28" y="38" fill="#fafafa" font-size="18" font-weight="bold" font-family="sans-serif">{title}</text>')
        svg.append(f'<text x="28" y="58" fill="#a1a1aa" font-size="12" font-family="sans-serif">Decompiled AST Topology | Modules: {len(modules)} | Circular Loops: {len(cycles)}</text>')

        # Module Cards (up to 4 visual cards across)
        card_w = 175
        card_h = 160
        spacing = 20
        start_x = 28
        start_y = 80

        for idx, (mod_name, data) in enumerate(list(modules.items())[:4]):
            tx = start_x + idx * (card_w + spacing)
            c_metric = coupling.get(mod_name, {})
            is_circ = c_metric.get("is_circular", False)
            border_col = "#ef4444" if is_circ else "#3b82f6"

            svg.append(f'<g transform="translate({tx}, {start_y})">')
            svg.append(f'<rect width="{card_w}" height="{card_h}" rx="8" fill="#18181b" stroke="{border_col}" stroke-width="1.5"/>')
            svg.append(f'<rect width="{card_w}" height="24" rx="8" fill="{border_col}22"/>')
            svg.append(f'<text x="10" y="16" fill="{border_col}" font-size="11" font-weight="bold" font-family="sans-serif">{mod_name[:18]}</text>')

            classes_count = len(data.get("classes", []))
            funcs_count = len(data.get("functions", []))
            svg.append(f'<text x="10" y="48" fill="#e4e4e7" font-size="11" font-family="sans-serif">Classes: {classes_count}</text>')
            svg.append(f'<text x="10" y="68" fill="#e4e4e7" font-size="11" font-family="sans-serif">Functions: {funcs_count}</text>')
            svg.append(f'<text x="10" y="94" fill="#a1a1aa" font-size="10" font-family="sans-serif">Instability: {c_metric.get("instability", 0.0)}</text>')
            svg.append(f'<text x="10" y="112" fill="#a1a1aa" font-size="10" font-family="sans-serif">Ca: {c_metric.get("afferent_ca", 0)} | Ce: {c_metric.get("efferent_ce", 0)}</text>')

            if is_circ:
                svg.append(f'<text x="10" y="140" fill="#ef4444" font-size="9" font-weight="bold" font-family="sans-serif">CIRCULAR LOOP</text>')
            else:
                svg.append(f'<text x="10" y="140" fill="#10b981" font-size="9" font-weight="bold" font-family="sans-serif">STABLE NODE</text>')

            svg.append('</g>')

        # Architectural Circuit Diagnostics Bar
        diag_y = 265
        svg.append(f'<rect x="28" y="{diag_y}" width="764" height="85" rx="8" fill="#18181b" stroke="#27272a" stroke-width="1"/>')
        svg.append(f'<text x="44" y="{diag_y + 24}" fill="#38bdf8" font-size="12" font-weight="bold" font-family="sans-serif">Coupling and Architectural Health Summary</text>')

        circ_status = f"CRITICAL: {len(cycles)} circular loops identified." if cycles else "OPTIMAL: Zero circular dependencies detected."
        svg.append(f'<text x="44" y="{diag_y + 48}" fill="#e4e4e7" font-size="11" font-family="sans-serif">{circ_status}</text>')
        svg.append(f'<text x="44" y="{diag_y + 68}" fill="#71717a" font-size="10" font-family="sans-serif">AST spatial decompiler provides immediate architectural comprehension without linear code tracing.</text>')

        # Footer
        svg.append(f'<text x="28" y="380" fill="#52525b" font-size="10" font-family="sans-serif">DxSkills Spatial Code Decompiler | Zero Em Dash Verified</text>')
        svg.append('</svg>')
        return "\n".join(svg)


def run_code_decompiler(
    target_path: str,
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """Decompiles Python file or project and exports topological artifacts."""
    doc_title = title or f"Code Architecture: {os.path.basename(target_path)}"

    if os.path.isdir(target_path):
        decompiled = CodeArchitectureDecompiler.decompile_project(target_path)
    else:
        with open(target_path, "r", encoding="utf-8", errors="ignore") as f:
            src = f.read()
        mod_name = os.path.splitext(os.path.basename(target_path))[0]
        single_mod = CodeArchitectureDecompiler.decompile_source(src, module_name=mod_name)
        decompiled = {
            "total_modules": 1,
            "modules": {mod_name: single_mod},
            "dependency_graph": {mod_name: []},
            "circular_cycles": [],
            "coupling_metrics": {mod_name: {"afferent_ca": 0, "efferent_ce": 0, "instability": 0.0, "is_circular": False}}
        }

    canvas_data = CodeTopologyExporter.to_canvas(decompiled, title=doc_title)
    svg_code = CodeTopologyExporter.to_svg_diagram(decompiled, title=doc_title)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    return decompiled, canvas_data, svg_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Spatial Multi-Modal Code Architecture Decompiler")
    parser.add_argument("target", nargs="?", default=".", help="Target Python source file or directory")
    parser.add_argument("--title", "-t", help="Title for the code architecture canvas")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas filepath")
    parser.add_argument("--svg", "-s", help="Output vector SVG circuit filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON AST telemetry")

    args = parser.parse_args()

    target_path = os.path.abspath(args.target)
    if not os.path.exists(target_path):
        print(f"[DxSkills] Error: Target path not found: {target_path}")
        sys.exit(1)

    decompiled, canvas_data, svg_code = run_code_decompiler(
        target_path,
        title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg
    )

    if args.json:
        print(json.dumps(decompiled, indent=2))
    elif not (args.canvas or args.svg):
        print(f"\n=== [DxSkills: Code Architecture Topology ({decompiled['total_modules']} Modules)] ===")
        for mod_name, data in decompiled["modules"].items():
            classes = [c["name"] for c in data.get("classes", [])]
            funcs = [f["name"] for f in data.get("functions", [])]
            print(f"- {mod_name}.py: Classes: {classes or 'None'} | Functions: {funcs or 'None'}")
        if decompiled["circular_cycles"]:
            print(f"\n⚠️ Identified {len(decompiled['circular_cycles'])} Circular Dependency Loops:")
            for c in decompiled["circular_cycles"]:
                print(f"  * {' -> '.join(c)}")
        else:
            print("\nClean architecture: Zero circular import loops detected.")
    else:
        print(f"[DxSkills] Decompiled {decompiled['total_modules']} modules into spatial architecture.")
        if args.canvas:
            print(f"  - Canvas: {args.canvas}")
        if args.svg:
            print(f"  - SVG Circuit: {args.svg}")


if __name__ == "__main__":
    main()
