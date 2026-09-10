#!/usr/bin/env python3
"""
Autonomous Cognitive Spatial Audio Landmark & Acoustic Beacon Anchoring
Part of the DxSkills Cognitive Architecture Suite (https://dxskills.sounny.com)

Synthesizes localized 3D acoustic beacon soundscapes for spatial canvas hubs.
Uses binaural stereo panning, distance sound pressure attenuation, and harmonic
frequencies (432Hz, 528Hz, 639Hz) to establish auditory landmarks that guide
non-linear and dyslexic thinkers through complex conceptual spaces.

Core Principles:
- Multi-Sensory Spatial Anchoring: Audio beacons eliminate visual navigation disorientation.
- Binaural Soundstage Wayfinding: Left/Right stereo panning indicates spatial orientation.
- Zero-Dependency WAV Synthesis: Generates 16-bit PCM audio via Python standard wave library.
"""

import os
import math
import wave
import struct
import json
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple


# Harmonic Solfeggio / Spatial reference frequencies for cognitive anchoring
ANCHOR_FREQUENCIES: List[Tuple[float, str]] = [
    (432.0, "Root Grounding Anchor"),
    (528.0, "Transformation & Architecture Core"),
    (639.0, "Relational Bridge & Synthesis Hub"),
    (741.0, "Clarity & Decoupling Beacon"),
    (852.0, "Metacognitive Intuition Anchor")
]


@dataclass
class SoundstageBeacon:
    """Represents a localized acoustic sound source on a 2D canvas."""
    beacon_id: str
    node_id: str
    title: str
    x: float
    y: float
    frequency: float
    tone_label: str
    amplitude: float = 0.6
    pulse_hz: float = 0.5  # Modulation pulse rate


@dataclass
class ListenerPosition:
    """Represents the observer or reader's current location on the canvas."""
    x: float
    y: float
    facing_angle_deg: float = 0.0  # 0 deg = facing upward (negative y)


class AcousticBeaconEngine:
    """Generates localized auditory landmarks and synthesizes binaural WAV soundscapes."""

    SAMPLE_RATE: int = 44100

    def __init__(self):
        self.beacons: List[SoundstageBeacon] = []
        self.canvas_data: Dict[str, Any] = {}

    def extract_beacons_from_canvas(self, canvas_data: Dict[str, Any], max_beacons: int = 5) -> List[SoundstageBeacon]:
        """Identify major anchor nodes in canvas and assign harmonic beacon frequencies."""
        self.canvas_data = canvas_data
        self.beacons = []

        nodes = canvas_data.get("nodes", [])
        if not nodes:
            return []

        # Sort nodes by connectivity (degree) or prominence
        edges = canvas_data.get("edges", [])
        node_degrees: Dict[str, int] = {n.get("id", ""): 0 for n in nodes}
        for e in edges:
            node_degrees[e.get("fromNode", "")] = node_degrees.get(e.get("fromNode", ""), 0) + 1
            node_degrees[e.get("toNode", "")] = node_degrees.get(e.get("toNode", ""), 0) + 1

        # Select top nodes with highest edge degree, or first N nodes
        sorted_nodes = sorted(
            nodes,
            key=lambda n: node_degrees.get(n.get("id", ""), 0),
            reverse=True
        )[:max_beacons]

        for idx, n in enumerate(sorted_nodes):
            freq, label = ANCHOR_FREQUENCIES[idx % len(ANCHOR_FREQUENCIES)]
            cx = float(n.get("x", 0)) + (float(n.get("width", 260)) / 2.0)
            cy = float(n.get("y", 0)) + (float(n.get("height", 160)) / 2.0)
            title = n.get("text", f"Node {idx + 1}").split("\n")[0][:24].strip()

            beacon = SoundstageBeacon(
                beacon_id=f"beacon_{idx + 1}",
                node_id=n.get("id", f"node_{idx}"),
                title=title,
                x=cx,
                y=cy,
                frequency=freq,
                tone_label=label,
                amplitude=0.5,
                pulse_hz=0.5 + (idx * 0.25)
            )
            self.beacons.append(beacon)

        return self.beacons

    def calculate_binaural_gains(self, beacon: SoundstageBeacon, listener: ListenerPosition) -> Tuple[float, float]:
        """
        Compute left and right ear gains based on distance and azimuth angle.
        Returns: (left_gain, right_gain) in range [0.0, 1.0]
        """
        dx = beacon.x - listener.x
        dy = beacon.y - listener.y
        dist = math.hypot(dx, dy)

        # Distance attenuation: inverse square law with minimum distance clamp
        dist_clamped = max(100.0, dist)
        attenuation = min(1.0, 400.0 / dist_clamped)

        # Azimuth angle relative to listener: dx > 0 is right, dx < 0 is left
        # Map dx (-600 to +600) to pan value [-1.0, +1.0]
        pan = max(-1.0, min(1.0, dx / 400.0))

        # Constant power panning law
        angle = (pan + 1.0) * (math.pi / 4.0)  # 0 to pi/2
        left_gain = math.cos(angle) * attenuation * beacon.amplitude
        right_gain = math.sin(angle) * attenuation * beacon.amplitude

        return (left_gain, right_gain)

    def synthesize_wav(self, duration_sec: float = 4.0, listener: Optional[ListenerPosition] = None) -> bytes:
        """
        Synthesize uncompressed 16-bit stereo PCM audio bytes.
        Combines all active acoustic beacons with binaural panning.
        """
        if listener is None:
            # Default listener at centroid of beacons
            if self.beacons:
                avg_x = sum(b.x for b in self.beacons) / len(self.beacons)
                avg_y = sum(b.y for b in self.beacons) / len(self.beacons)
                listener = ListenerPosition(x=avg_x, y=avg_y)
            else:
                listener = ListenerPosition(x=0.0, y=0.0)

        num_samples = int(duration_sec * self.SAMPLE_RATE)
        sample_buffer_left = [0.0] * num_samples
        sample_buffer_right = [0.0] * num_samples

        for beacon in self.beacons:
            left_gain, right_gain = self.calculate_binaural_gains(beacon, listener)
            two_pi_f = 2.0 * math.pi * beacon.frequency
            pulse_rate = 2.0 * math.pi * beacon.pulse_hz

            for i in range(num_samples):
                t = i / float(self.SAMPLE_RATE)
                # Tremolo pulse envelope
                envelope = 0.7 + 0.3 * math.sin(pulse_rate * t)
                # Soft carrier wave with gentle 2nd harmonic
                carrier = 0.85 * math.sin(two_pi_f * t) + 0.15 * math.sin(two_pi_f * 2.0 * t)
                val = carrier * envelope

                sample_buffer_left[i] += val * left_gain
                sample_buffer_right[i] += val * right_gain

        # Normalize and pack into 16-bit signed PCM frames
        frames = bytearray()
        max_peak = 0.0001
        for i in range(num_samples):
            max_peak = max(max_peak, abs(sample_buffer_left[i]), abs(sample_buffer_right[i]))

        scale = 32000.0 / max(max_peak, 0.8)

        for i in range(num_samples):
            sl = int(max(-32767, min(32767, sample_buffer_left[i] * scale)))
            sr = int(max(-32767, min(32767, sample_buffer_right[i] * scale)))
            frames.extend(struct.pack("<hh", sl, sr))

        return bytes(frames)

    def write_wav_file(self, filepath: str, duration_sec: float = 4.0, listener: Optional[ListenerPosition] = None):
        """Write synthesized binaural soundscape directly to a .wav file."""
        raw_pcm = self.synthesize_wav(duration_sec=duration_sec, listener=listener)
        with wave.open(filepath, "wb") as wf:
            wf.setnchannels(2)  # Stereo
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(raw_pcm)

    def export_soundstage_svg(self, listener: Optional[ListenerPosition] = None, width: int = 1000, height: int = 650) -> str:
        """Generate an interactive vector SVG showing acoustic beacon coverage rings."""
        if not self.beacons:
            return '<svg xmlns="http://www.w3.org/2000/svg" width="100" height="50"></svg>'

        min_x = min(b.x for b in self.beacons)
        min_y = min(b.y for b in self.beacons)
        max_x = max(b.x for b in self.beacons)
        max_y = max(b.y for b in self.beacons)

        view_w = max(int(max_x - min_x + 300), 800)
        view_h = max(int(max_y - min_y + 300), 550)
        ox = -min_x + 150
        oy = -min_y + 150

        if listener is None:
            lx = (min_x + max_x) / 2.0 + ox
            ly = (min_y + max_y) / 2.0 + oy
        else:
            lx = listener.x + ox
            ly = listener.y + oy

        svg_lines = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_w} {view_h}" width="100%" height="100%">',
            f'  <rect width="{view_w}" height="{view_h}" fill="#09090b" rx="16" />',
            f'  <!-- Soundstage Header -->',
            f'  <text x="30" y="40" fill="#ffffff" font-size="16" font-weight="700" font-family="sans-serif">3D Acoustic Landmark &amp; Soundstage Map</text>',
            f'  <text x="30" y="60" fill="#a1a1aa" font-size="11" font-family="sans-serif">Active Audio Beacons: {len(self.beacons)} | Spatial Stereo Localization</text>',
            f'  <!-- Acoustic Sound Pressure Coverage Waves -->',
        ]

        # Draw beacon rings and markers
        for b in self.beacons:
            bx = b.x + ox
            by = b.y + oy

            # Concentric sound waves
            svg_lines.append(f'  <circle cx="{bx}" cy="{by}" r="120" fill="none" stroke="#3b82f6" stroke-opacity="0.15" stroke-dasharray="4 4" />')
            svg_lines.append(f'  <circle cx="{bx}" cy="{by}" r="75" fill="none" stroke="#3b82f6" stroke-opacity="0.3" stroke-dasharray="4 4" />')
            svg_lines.append(f'  <circle cx="{bx}" cy="{by}" r="35" fill="none" stroke="#60a5fa" stroke-opacity="0.5" />')

            # Beacon core
            svg_lines.append(f'  <circle cx="{bx}" cy="{by}" r="10" fill="#3b82f6" stroke="#ffffff" stroke-width="2" />')

            # Connecting ray to listener
            svg_lines.append(f'  <line x1="{lx}" y1="{ly}" x2="{bx}" y2="{by}" stroke="#27272a" stroke-width="1.2" stroke-dasharray="2 2" />')

            # Label
            safe_title = b.title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            svg_lines.append(f'  <text x="{bx + 16}" y="{by - 4}" fill="#f4f4f5" font-size="12" font-weight="600" font-family="sans-serif">{safe_title}</text>')
            svg_lines.append(f'  <text x="{bx + 16}" y="{by + 12}" fill="#93c5fd" font-size="10" font-family="monospace">{b.frequency} Hz ({b.tone_label})</text>')

        # Listener icon
        svg_lines.append(f'  <!-- Listener Head Position -->')
        svg_lines.append(f'  <circle cx="{lx}" cy="{ly}" r="16" fill="#18181b" stroke="#ef4444" stroke-width="2.5" />')
        svg_lines.append(f'  <circle cx="{lx}" cy="{ly}" r="5" fill="#ef4444" />')
        svg_lines.append(f'  <text x="{lx}" y="{ly + 30}" fill="#ffffff" font-size="11" font-weight="700" font-family="sans-serif" text-anchor="middle">Listener (You)</text>')

        svg_lines.append('</svg>')
        return "\n".join(svg_lines)

    @classmethod
    def export_summary(cls, beacons: List[SoundstageBeacon]) -> str:
        """Generate markdown summary table of acoustic landmark beacons."""
        lines = [
            f"# Spatial Audio Landmark & Acoustic Beacon Anchoring",
            f"",
            f"**Total Soundstage Beacons:** {len(beacons)}",
            f"**Soundstage Standard:** 44.1kHz 16-Bit Binaural Stereo PCM",
            f"",
            f"| Beacon ID | Node Title | Coordinate (X, Y) | Frequency | Harmonic Function |",
            f"| :--- | :--- | :--- | :--- | :--- |"
        ]

        for b in beacons:
            lines.append(f"| `{b.beacon_id}` | `{b.title}` | `({int(b.x)}, {int(b.y)})` | **{b.frequency} Hz** | {b.tone_label} |")

        return "\n".join(lines)


def main():
    """Quick CLI runner."""
    print("AcousticBeaconEngine Loaded.")


if __name__ == "__main__":
    main()
