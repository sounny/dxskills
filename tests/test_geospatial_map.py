"""
Tests for Geospatial & Multi-Projection Spatial Map Visualizer.
Strict zero em dash compliance verified across all test assertions.
"""

import os
import sys
import json
import unittest
import tempfile
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from geospatial_map import (
    ProjectionEngine,
    GeoSpatialParser,
    GeoSpatialMapRenderer,
    run_geospatial_mapping,
)


class TestGeoSpatialMap(unittest.TestCase):

    def setUp(self):
        self.sample_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [7.7521, 48.5734]},
                    "properties": {"name": "ISU Strasbourg"}
                },
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [-97.7431, 30.2672]},
                    "properties": {"name": "Austin Texas"}
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[7.7521, 48.5734], [2.3522, 48.8566], [-0.1278, 51.5074]]
                    },
                    "properties": {"name": "European Academic Corridor"}
                }
            ]
        }

        self.sample_text_locations = (
            "# Spatial Research Corridors\n"
            "- Strasbourg research headquarters (48.5734, 7.7521)\n"
            "- Austin adjunct geospatial lab (30.2672, -97.7431)\n"
            "- Madison cartography center\n"
            "- Tokyo space robotics lab (35.6895, 139.6917)"
        )

    def test_projection_engine_math(self):
        # Equirectangular
        x_eq, y_eq = ProjectionEngine.equirectangular(0.0, 0.0)
        self.assertAlmostEqual(x_eq, 0.0)
        self.assertAlmostEqual(y_eq, 0.0)

        # Mercator
        x_mer, y_mer = ProjectionEngine.mercator(0.0, 0.0)
        self.assertAlmostEqual(x_mer, 0.0)
        self.assertAlmostEqual(y_mer, 0.0)

        # Winkel Tripel
        x_win, y_win = ProjectionEngine.winkel_tripel(0.0, 0.0)
        self.assertAlmostEqual(x_win, 0.0)
        self.assertAlmostEqual(y_win, 0.0)

        # Orthographic
        x_ort, y_ort = ProjectionEngine.orthographic(0.0, 0.0)
        self.assertAlmostEqual(x_ort, 0.0)
        self.assertAlmostEqual(y_ort, 0.0)

    def test_geospatial_parser_geojson(self):
        parsed = GeoSpatialParser.parse_input(json.dumps(self.sample_geojson))
        self.assertEqual(parsed["source_type"], "geojson")
        self.assertEqual(len(parsed["points"]), 2)
        self.assertEqual(len(parsed["paths"]), 1)
        self.assertEqual(parsed["points"][0]["name"], "ISU Strasbourg")

    def test_geospatial_parser_text_landmarks(self):
        parsed = GeoSpatialParser.parse_input(self.sample_text_locations)
        self.assertEqual(parsed["source_type"], "text_extracted")
        self.assertGreaterEqual(len(parsed["points"]), 3)
        names = [p["name"] for p in parsed["points"]]
        self.assertTrue(any("Strasbourg" in n for n in names))
        self.assertTrue(any("Austin" in n for n in names))

    def test_render_svg_output(self):
        parsed = GeoSpatialParser.parse_input(json.dumps(self.sample_geojson))
        svg = GeoSpatialMapRenderer.render_svg(parsed, projection="winkel", title="Test World Map")

        self.assertIn("<svg", svg)
        self.assertIn("</svg>", svg)
        self.assertIn("ISU Strasbourg", svg)
        self.assertIn("PROJ: WINKEL", svg)
        self.assertNotIn(chr(8212), svg)

    def test_render_obsidian_canvas_structure(self):
        parsed = GeoSpatialParser.parse_input(json.dumps(self.sample_geojson))
        canvas = GeoSpatialMapRenderer.render_obsidian_canvas(parsed, projection="mercator", title="Geo Canvas")

        self.assertIn("nodes", canvas)
        self.assertIn("edges", canvas)
        # Header node + 2 point nodes
        self.assertEqual(len(canvas["nodes"]), 3)

        header_node = [n for n in canvas["nodes"] if n["id"] == "node-geo-header"][0]
        self.assertIn("MERCATOR", header_node["text"].upper())

    def test_run_geospatial_mapping_file_exports(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            c_file = os.path.join(tmpdir, "map.canvas")
            s_file = os.path.join(tmpdir, "map.svg")

            parsed, canvas_data, svg_code = run_geospatial_mapping(
                json.dumps(self.sample_geojson),
                projection="equirectangular",
                title="Academic Network",
                output_canvas=c_file,
                output_svg=s_file
            )

            self.assertTrue(os.path.isfile(c_file))
            self.assertTrue(os.path.isfile(s_file))

            with open(s_file, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content)

    def test_cli_geomap_command(self):
        cli_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "dx_cli.py"))
        res = subprocess.run(
            [sys.executable, cli_path, "geomap", "--projection", "winkel", "--title", "CLI Geo Test"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("<svg", res.stdout)
        self.assertIn("CLI Geo Test", res.stdout)
        self.assertNotIn(chr(8212), res.stdout)

    def test_zero_em_dash_in_source(self):
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts", "geospatial_map.py"))
        if os.path.exists(script_path):
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertNotIn(chr(8212), content, "Found em dash in scripts/geospatial_map.py")


if __name__ == "__main__":
    unittest.main()
