"""Unit tests for Autonomous Cognitive Spatial Dual-Code Working Memory Interleaver.

Strict Quality Gate: Zero em dashes anywhere.
"""

import json
from pathlib import Path
import pytest

from scripts.dual_code_interleaver import (
    DualCodeBlock,
    DualCodeInterleaver,
    DualCodeTelemetry,
    InterleaveMode,
)


def test_extract_keywords():
    text = "Distributed asynchronous consensus protocols eliminate split-brain state corruptions in clusters."
    keywords = DualCodeInterleaver.extract_keywords(text)
    assert "consensus" in keywords
    assert "distributed" in keywords
    assert "protocols" in keywords
    assert "in" not in keywords  # stopword


def test_align_empty():
    interleaver = DualCodeInterleaver()
    blocks, telemetry = interleaver.align_channels({"nodes": []}, "")
    assert telemetry.total_nodes == 0
    assert telemetry.total_verbal_sentences == 0
    assert len(blocks) == 0


def test_align_channels_and_exports(tmp_path: Path):
    interleaver = DualCodeInterleaver(mode=InterleaveMode.INTERLEAVED_STREAM)

    canvas_data = {
        "nodes": [
            {
                "id": "node-raft",
                "text": "Raft Consensus Module\n\nCoordinates cluster leader election and log replication."
            },
            {
                "id": "node-storage",
                "text": "Write-Ahead Storage Engine\n\nPersists append-only write entries to durable disk."
            }
        ]
    }

    prose = (
        "The Raft consensus module coordinates cluster leader election reliably. "
        "The write-ahead storage engine persists all append-only write entries to disk. "
        "Global network telemetry monitors health across clusters."
    )

    blocks, telemetry = interleaver.align_channels(canvas_data, prose)

    assert telemetry.total_nodes == 2
    assert telemetry.total_verbal_sentences == 3
    assert telemetry.mapped_associations_count >= 2
    assert 0.2 <= telemetry.dual_code_balance_ratio <= 1.0
    assert telemetry.cognitive_friction_reduction_pct > 0.0

    # Verify blocks content
    raft_block = next(b for b in blocks if b.node_id == "node-raft")
    assert "Raft" in raft_block.verbal_text
    assert "[Node: node-raft]" in raft_block.cross_refs

    # ASCII output
    ascii_out = interleaver.render_ascii_dual_stream(telemetry)
    assert "Dual-Code Working Memory Interleaver" in ascii_out
    assert "BLOCK #1" in ascii_out

    # Markdown export
    md_path = tmp_path / "dual_code.md"
    interleaver.export_interleaved_markdown(telemetry, md_path)
    assert md_path.exists()
    md_text = md_path.read_text(encoding="utf-8")
    assert "# Dual-Coded Working Memory Specification" in md_text
    assert "VISUAL SPATIAL ANCHOR" in md_text

    # Canvas export
    canvas_path = tmp_path / "dual_code.canvas"
    interleaver.export_canvas(telemetry, canvas_path)
    assert canvas_path.exists()
    cdata = json.loads(canvas_path.read_text(encoding="utf-8"))
    assert "nodes" in cdata
    assert len(cdata["nodes"]) >= 5
    assert len(cdata["edges"]) >= 2

    # SVG export
    svg_path = tmp_path / "dual_code.svg"
    interleaver.export_svg_dual_track(telemetry, svg_path)
    assert svg_path.exists()
    svg_text = svg_path.read_text(encoding="utf-8")
    assert "<svg" in svg_text
    assert "SPATIAL TRACK" in svg_text
    assert "VERBAL TRACK" in svg_text


def test_zero_em_dashes():
    script_file = Path(__file__).resolve().parent.parent / "scripts" / "dual_code_interleaver.py"
    test_file = Path(__file__).resolve()

    em_dash = chr(8212)
    assert em_dash not in script_file.read_text(encoding="utf-8")
    assert em_dash not in test_file.read_text(encoding="utf-8")
