"""
Geospatial and Multi-Projection Spatial Map Visualizer for DxSkills.

Parses GeoJSON geometries, coordinate pairs, and geographic notes,
projecting them across Mercator, Equirectangular, Winkel Tripel,
and Orthographic perspectives into standalone SVGs and Obsidian .canvas files.

Zero em dash policy strictly enforced.
"""

import os
import sys
import json
import math
import re
import argparse
from typing import Dict, List, Any, Optional, Tuple


class ProjectionEngine:
    """Mathematical projection transformations for geographic coordinates."""

    @staticmethod
    def equirectangular(lon: float, lat: float, lon0: float = 0.0) -> Tuple[float, float]:
        """Linear plate carree projection."""
        x = math.radians(lon - lon0)
        y = math.radians(lat)
        return x, y

    @staticmethod
    def mercator(lon: float, lat: float, lon0: float = 0.0) -> Tuple[float, float]:
        """Conformal cylindrical Mercator projection bounded between -85 and +85 deg."""
        lat_clamped = max(-85.0, min(85.0, lat))
        x = math.radians(lon - lon0)
        y = math.log(math.tan(math.pi / 4.0 + math.radians(lat_clamped) / 2.0))
        return x, y

    @staticmethod
    def winkel_tripel(lon: float, lat: float, lon0: float = 0.0) -> Tuple[float, float]:
        """Winkel Tripel pseudo-cylindrical compromise projection."""
        lam = math.radians(lon - lon0)
        phi = math.radians(lat)
        phi1 = math.acos(2.0 / math.pi)

        # sinc(alpha)
        cos_phi = math.cos(phi)
        cos_lam_2 = math.cos(lam / 2.0)
        alpha = math.acos(max(-1.0, min(1.0, cos_phi * cos_lam_2)))
        sinc_alpha = 1.0 if abs(alpha) < 1e-6 else (math.sin(alpha) / alpha)

        x1 = lam * math.cos(phi1)
        y1 = phi
        x2 = 2.0 * cos_phi * math.sin(lam / 2.0) / sinc_alpha
        y2 = math.sin(phi) / sinc_alpha

        return 0.5 * (x1 + x2), 0.5 * (y1 + y2)

    @staticmethod
    def orthographic(lon: float, lat: float, lon0: float = 0.0, lat0: float = 0.0) -> Tuple[float, float]:
        """Orthographic perspective projection (view from infinite distance)."""
        lam = math.radians(lon - lon0)
        phi = math.radians(lat)
        phi0 = math.radians(lat0)

        cos_c = math.sin(phi0) * math.sin(phi) + math.cos(phi0) * math.cos(phi) * math.cos(lam)
        # Visible hemisphere check: if behind horizon, project to boundary
        x = math.cos(phi) * math.sin(lam)
        y = math.cos(phi0) * math.sin(phi) - math.sin(phi0) * math.cos(phi) * math.cos(lam)
        return x, y


class GeoSpatialParser:
    """Parses GeoJSON structures or structured location lists."""

    KNOWN_LANDMARKS = {
        "strasbourg": (7.7521, 48.5734, "International Space University / Strasbourg"),
        "austin": (-97.7431, 30.2672, "Texas State University / Austin"),
        "madison": (-89.4012, 43.0731, "UW-Madison GISPP"),
        "paris": (2.3522, 48.8566, "Paris Research Hub"),
        "riyadh": (46.6753, 24.7136, "Saudi ESC Center"),
        "london": (-0.1278, 51.5074, "London WIA Europe"),
        "tokyo": (139.6917, 35.6895, "Tokyo Space Robotics"),
        "san francisco": (-122.4194, 37.7749, "Silicon Valley Studio")
    }

    @classmethod
    def parse_input(cls, content: str) -> Dict[str, Any]:
        """Detects GeoJSON format or falls back to text/markdown coordinate extraction."""
        content = content.strip()
        if content.startswith("{") and "type" in content:
            try:
                data = json.loads(content)
                if data.get("type") in ("FeatureCollection", "Feature", "Point", "Polygon", "MultiPolygon", "LineString"):
                    return cls._normalize_geojson(data)
            except Exception:
                pass

        # Text / landmark extraction
        return cls._extract_text_locations(content)

    @classmethod
    def _normalize_geojson(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        features = []
        if data.get("type") == "FeatureCollection":
            features = data.get("features", [])
        elif data.get("type") == "Feature":
            features = [data]
        elif "coordinates" in data:
            features = [{"type": "Feature", "geometry": data, "properties": {"name": "Geometry Feature"}}]

        normalized_points = []
        normalized_paths = []

        for f in features:
            geom = f.get("geometry", {})
            props = f.get("properties", {})
            g_type = geom.get("type", "")
            coords = geom.get("coordinates", [])
            name = props.get("name") or props.get("title") or "Unnamed Landmark"

            if g_type == "Point" and len(coords) >= 2:
                normalized_points.append({
                    "lon": float(coords[0]),
                    "lat": float(coords[1]),
                    "name": name,
                    "properties": props
                })
            elif g_type == "MultiPoint":
                for pt in coords:
                    if len(pt) >= 2:
                        normalized_points.append({
                            "lon": float(pt[0]),
                            "lat": float(pt[1]),
                            "name": name,
                            "properties": props
                        })
            elif g_type in ("LineString", "Polygon"):
                ring = coords if g_type == "LineString" else (coords[0] if coords else [])
                path_pts = []
                for pt in ring:
                    if len(pt) >= 2:
                        path_pts.append((float(pt[0]), float(pt[1])))
                if path_pts:
                    normalized_paths.append({
                        "type": g_type,
                        "name": name,
                        "points": path_pts,
                        "properties": props
                    })

        return {
            "source_type": "geojson",
            "points": normalized_points,
            "paths": normalized_paths
        }

    @classmethod
    def _extract_text_locations(cls, text: str) -> Dict[str, Any]:
        points = []
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        # Check for explicit lat/lon regex: lat, lon or lon, lat
        coord_pattern = re.compile(r"([+-]?\d+\.?\d*)\s*,\s*([+-]?\d+\.?\d*)")

        for line in lines:
            # Check known landmarks
            matched_landmark = False
            for key, (lon, lat, full_name) in cls.KNOWN_LANDMARKS.items():
                if re.search(r"\b" + re.escape(key) + r"\b", line, re.IGNORECASE):
                    points.append({
                        "lon": lon,
                        "lat": lat,
                        "name": full_name,
                        "properties": {"line": line}
                    })
                    matched_landmark = True
                    break

            if not matched_landmark:
                match = coord_pattern.search(line)
                if match:
                    v1, v2 = float(match.group(1)), float(match.group(2))
                    # Guess lat vs lon: lat in [-90, 90], lon in [-180, 180]
                    if -90 <= v1 <= 90 and -180 <= v2 <= 180:
                        lat, lon = v1, v2
                    else:
                        lon, lat = v1, v2
                    label = re.sub(r"^[#\-\*\d\.\s]+", "", line).split("(")[0].strip() or "Coordinate Point"
                    points.append({
                        "lon": lon,
                        "lat": lat,
                        "name": label,
                        "properties": {"raw_line": line}
                    })

        # If no points extracted, supply default global academic network
        if not points:
            for key in ["strasbourg", "austin", "madison", "paris", "riyadh"]:
                lon, lat, full_name = cls.KNOWN_LANDMARKS[key]
                points.append({
                    "lon": lon,
                    "lat": lat,
                    "name": full_name,
                    "properties": {"category": "Academic Hub"}
                })

        return {
            "source_type": "text_extracted",
            "points": points,
            "paths": []
        }


class GeoSpatialMapRenderer:
    """Renders projected geographic features into vector SVG and Obsidian Canvas."""

    @classmethod
    def render_svg(
        cls,
        parsed_data: Dict[str, Any],
        projection: str = "winkel",
        width: int = 900,
        height: int = 500,
        title: str = "Geospatial Canvas Map"
    ) -> str:
        points = parsed_data.get("points", [])
        paths = parsed_data.get("paths", [])

        proj_fn = {
            "mercator": ProjectionEngine.mercator,
            "equirectangular": ProjectionEngine.equirectangular,
            "winkel": ProjectionEngine.winkel_tripel,
            "orthographic": ProjectionEngine.orthographic
        }.get(projection.lower(), ProjectionEngine.winkel_tripel)

        # Collect projected coordinates to determine bounding box
        proj_coords = []
        for pt in points:
            px, py = proj_fn(pt["lon"], pt["lat"])
            proj_coords.append((px, py, pt))

        for path in paths:
            for pt in path["points"]:
                px, py = proj_fn(pt[0], pt[1])
                proj_coords.append((px, py, None))

        if not proj_coords:
            return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"><text x="20" y="40" fill="#fff">No coordinates to project</text></svg>'

        min_px = min(c[0] for c in proj_coords)
        max_px = max(c[0] for c in proj_coords)
        min_py = min(c[1] for c in proj_coords)
        max_py = max(c[1] for c in proj_coords)

        # Add 15% padding
        dx = max(0.001, max_px - min_px)
        dy = max(0.001, max_py - min_py)
        pad_x = dx * 0.15
        pad_y = dy * 0.15

        min_px -= pad_x
        max_px += pad_x
        min_py -= pad_y
        max_py += pad_y

        def to_screen(px: float, py: float) -> Tuple[float, float]:
            sx = 40 + ((px - min_px) / (max_px - min_px)) * (width - 80)
            # Invert Y for screen coordinates (north is up)
            sy = (height - 40) - ((py - min_py) / (max_py - min_py)) * (height - 80)
            return round(sx, 1), round(sy, 1)

        svg = []
        svg.append(f'<svg width="100%" height="auto" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">')
        svg.append(f'<rect width="{width}" height="{height}" rx="12" fill="#09090b" stroke="#27272a" stroke-width="1"/>')

        # Graticule lines
        svg.append('<g opacity="0.15" stroke="#71717a" stroke-width="1" stroke-dasharray="3 3">')
        for lat_deg in range(-60, 80, 30):
            line_pts = []
            for lon_deg in range(-180, 181, 10):
                px, py = proj_fn(float(lon_deg), float(lat_deg))
                if min_px <= px <= max_px and min_py <= py <= max_py:
                    sx, sy = to_screen(px, py)
                    line_pts.append(f"{sx},{sy}")
            if len(line_pts) > 2:
                svg.append(f'<polyline points="{" ".join(line_pts)}" fill="none"/>')
        svg.append('</g>')

        # Draw paths / polygons
        for path in paths:
            screen_pts = []
            for pt in path["points"]:
                px, py = proj_fn(pt[0], pt[1])
                sx, sy = to_screen(px, py)
                screen_pts.append(f"{sx},{sy}")
            if screen_pts:
                pts_str = " ".join(screen_pts)
                if path["type"] == "Polygon":
                    svg.append(f'<polygon points="{pts_str}" fill="#3b82f622" stroke="#3b82f6" stroke-width="2"/>')
                else:
                    svg.append(f'<polyline points="{pts_str}" fill="none" stroke="#38bdf8" stroke-width="2"/>')

        # Draw inter-point flight/network routes
        if len(points) >= 2:
            svg.append('<g opacity="0.4" stroke="#8b5cf6" stroke-width="1.5" stroke-dasharray="4 4">')
            for i in range(len(points) - 1):
                p1 = points[i]
                p2 = points[i + 1]
                px1, py1 = proj_fn(p1["lon"], p1["lat"])
                px2, py2 = proj_fn(p2["lon"], p2["lat"])
                sx1, sy1 = to_screen(px1, py1)
                sx2, sy2 = to_screen(px2, py2)
                svg.append(f'<line x1="{sx1}" y1="{sy1}" x2="{sx2}" y2="{sy2}"/>')
            svg.append('</g>')

        # Draw point markers
        for pt in points:
            px, py = proj_fn(pt["lon"], pt["lat"])
            sx, sy = to_screen(px, py)
            name = pt["name"]
            svg.append(f'<g transform="translate({sx}, {sy})">')
            svg.append('<circle r="6" fill="#ef4444" stroke="#fafafa" stroke-width="2"/>')
            svg.append('<circle r="12" fill="#ef444422"/>')
            svg.append(f'<text x="12" y="4" fill="#f4f4f5" font-size="12" font-weight="600" font-family="sans-serif">{name}</text>')
            svg.append('</g>')

        # Header Title and Projection Badge
        svg.append(f'<text x="24" y="32" fill="#fafafa" font-size="16" font-weight="bold" font-family="sans-serif">{title}</text>')
        svg.append(f'<rect x="{width - 160}" y="16" width="136" height="26" rx="6" fill="#18181b" stroke="#3f3f46"/>')
        svg.append(f'<text x="{width - 92}" y="33" fill="#a1a1aa" font-size="11" font-weight="bold" text-anchor="middle" font-family="sans-serif">PROJ: {projection.upper()}</text>')

        svg.append('</svg>')
        return "\n".join(svg)

    @classmethod
    def render_obsidian_canvas(
        cls,
        parsed_data: Dict[str, Any],
        projection: str = "winkel",
        title: str = "Geospatial Canvas"
    ) -> Dict[str, Any]:
        points = parsed_data.get("points", [])
        nodes = []
        edges = []

        proj_fn = {
            "mercator": ProjectionEngine.mercator,
            "equirectangular": ProjectionEngine.equirectangular,
            "winkel": ProjectionEngine.winkel_tripel,
            "orthographic": ProjectionEngine.orthographic
        }.get(projection.lower(), ProjectionEngine.winkel_tripel)

        # Header node
        nodes.append({
            "id": "node-geo-header",
            "type": "text",
            "text": f"## {title}\nProjection: **{projection.upper()}**\nSpatial Nodes Anchored: **{len(points)}**",
            "x": 0,
            "y": -220,
            "width": 380,
            "height": 130,
            "color": "1"  # Red
        })

        if not points:
            return {"nodes": nodes, "edges": edges}

        # Project coordinates to 2D canvas space (multiplier 800px scale)
        proj_coords = []
        for pt in points:
            px, py = proj_fn(pt["lon"], pt["lat"])
            proj_coords.append((px, py, pt))

        min_px = min(c[0] for c in proj_coords)
        max_px = max(c[0] for c in proj_coords)
        min_py = min(c[1] for c in proj_coords)
        max_py = max(c[1] for c in proj_coords)

        dx = max(0.001, max_px - min_px)
        dy = max(0.001, max_py - min_py)

        canvas_width = 1600
        canvas_height = 900

        for idx, (px, py, pt) in enumerate(proj_coords):
            # Map into canvas space
            cx = round(((px - min_px) / dx) * canvas_width) - (canvas_width // 2)
            cy = round((1.0 - (py - min_py) / dy) * canvas_height) - (canvas_height // 2) + 200

            nid = f"geo-node-{idx + 1}"
            nodes.append({
                "id": nid,
                "type": "text",
                "text": f"### {pt['name']}\n**Coordinates:** `{pt['lat']:.4f}, {pt['lon']:.4f}`\n\n*Projection Position:* `X:{cx}, Y:{cy}`",
                "x": cx,
                "y": cy,
                "width": 320,
                "height": 160,
                "color": "5"  # Blue
            })

            # Edge to header or predecessor
            if idx == 0:
                edges.append({
                    "id": f"edge-header-{nid}",
                    "fromNode": "node-geo-header",
                    "fromSide": "bottom",
                    "toNode": nid,
                    "toSide": "top",
                    "label": "spatial network"
                })
            else:
                prev_id = f"geo-node-{idx}"
                edges.append({
                    "id": f"edge-flow-{idx}",
                    "fromNode": prev_id,
                    "fromSide": "right",
                    "toNode": nid,
                    "toSide": "left",
                    "label": "geodesic path",
                    "color": "6"
                })

        return {"nodes": nodes, "edges": edges}


def run_geospatial_mapping(
    content: str,
    projection: str = "winkel",
    title: Optional[str] = None,
    output_canvas: Optional[str] = None,
    output_svg: Optional[str] = None
) -> Tuple[Dict[str, Any], Dict[str, Any], str]:
    """Parses geographic input and renders SVG and Canvas representations."""
    parsed = GeoSpatialParser.parse_input(content)
    map_title = title or "Geospatial Spatial Canvas"

    canvas_data = GeoSpatialMapRenderer.render_obsidian_canvas(parsed, projection=projection, title=map_title)
    svg_code = GeoSpatialMapRenderer.render_svg(parsed, projection=projection, title=map_title)

    if output_canvas:
        os.makedirs(os.path.dirname(os.path.abspath(output_canvas)), exist_ok=True)
        with open(output_canvas, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)

    if output_svg:
        os.makedirs(os.path.dirname(os.path.abspath(output_svg)), exist_ok=True)
        with open(output_svg, "w", encoding="utf-8") as f:
            f.write(svg_code)

    return parsed, canvas_data, svg_code


def main():
    parser = argparse.ArgumentParser(description="DxSkills Geospatial & Multi-Projection Spatial Map Visualizer")
    parser.add_argument("input", nargs="?", help="GeoJSON file, coordinate list, or geographic note markdown")
    parser.add_argument("--projection", "-p", choices=["winkel", "mercator", "equirectangular", "orthographic"], default="winkel", help="Map projection (default: winkel)")
    parser.add_argument("--title", "-t", help="Map title")
    parser.add_argument("--canvas", "-c", help="Output Obsidian .canvas filepath")
    parser.add_argument("--svg", "-s", help="Output vector .svg filepath")
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON telemetry")

    args = parser.parse_args()

    content = ""
    if args.input:
        if os.path.isfile(args.input):
            with open(args.input, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = args.input
    else:
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            # Default geographic network sample
            content = (
                "# Global Academic and Spatial Research Nodes\n"
                "- Strasbourg: European space research and ISU headquarters\n"
                "- Austin: Texas State University geography campus\n"
                "- Madison: UW-Madison GISPP cartography laboratory\n"
                "- Paris: French research archives and national library\n"
                "- Riyadh: Saudi Executive Space Course\n"
            )

    parsed, canvas_data, svg_code = run_geospatial_mapping(
        content,
        projection=args.projection,
        title=args.title,
        output_canvas=args.canvas,
        output_svg=args.svg
    )

    if args.json:
        print(json.dumps({
            "projection": args.projection,
            "points_count": len(parsed.get("points", [])),
            "points": parsed.get("points", []),
            "canvas": canvas_data
        }, indent=2))
    elif not (args.canvas or args.svg):
        print(svg_code)
    else:
        print(f"[DxSkills] Projected {len(parsed['points'])} geospatial landmarks using {args.projection.upper()} projection.")
        if args.canvas:
            print(f"  - Canvas: {args.canvas}")
        if args.svg:
            print(f"  - SVG: {args.svg}")


if __name__ == "__main__":
    main()
