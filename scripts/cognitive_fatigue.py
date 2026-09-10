#!/usr/bin/env python3
"""
DxSkills Cognitive Fatigue Diagnostics & Spatial Reset Module
Implements Baddeley Working Memory phonological saturation estimation and terminal reset guides.

Strict Rule: NO em dashes anywhere (use hyphens, commas, or parentheses).
"""

import time
import sys

def calculate_cognitive_stamina(minutes_active, words_drafted=0, edits_count=0):
    """
    Estimates remaining working memory stamina based on duration and phonological load.
    Based on Sweller Cognitive Load Theory and Cowan working memory limits.
    """
    base_stamina = 100.0

    duration_penalty = min(60.0, minutes_active * 1.2)
    volume_penalty = min(25.0, (words_drafted + edits_count * 2) * 0.05)
    current_stamina = max(10.0, round(base_stamina - duration_penalty - volume_penalty, 1))

    if current_stamina >= 75.0:
        status = "Optimal Focus"
        zone = "Green"
        recommendation = "Peak cognitive velocity. Continue rapid idea capture."
    elif current_stamina >= 45.0:
        status = "Moderate Load"
        zone = "Amber"
        recommendation = "Working memory buffer filling up. Switch to structured tables or bullet chunks."
    else:
        status = "Phonological Saturation"
        zone = "Red (Reset Due)"
        recommendation = "Phonological loop ceiling reached. Take a 60-second spatial reset or switch to voice dictation."

    return {
        "minutes_active": minutes_active,
        "words_drafted": words_drafted,
        "stamina_score": current_stamina,
        "status": status,
        "zone": zone,
        "recommendation": recommendation
    }

def print_stamina_report(metrics):
    print("\n=== [DxSkills: Cognitive Fatigue & Working Memory Stamina] ===")
    print(f"> **Stamina Score:** {metrics['stamina_score']}% ({metrics['status']})")
    print(f"> **Session Duration:** {metrics['minutes_active']} minutes | **Phonological Buffer:** {metrics['zone']}")
    print("\n### Cognitive Science Analysis")
    print("- **Phonological Loop:** Continuous linear reading and typing exhausts working memory buffers (Baddeley Model).")
    print("- **Spatial Detachment:** Non-linear thinkers recover peak output by decoupling gaze and transitioning to spatial diagrams.")
    print("\n### Recommended Action")
    print(f"> {metrics['recommendation']}")

def run_terminal_box_breathing(cycles=3):
    phases = [
        ("Inhale Slowly (Nose)", 4, ">>>>"),
        ("Hold Lungs Full", 4, "===="),
        ("Exhale Smoothly (Mouth)", 4, "<<<<"),
        ("Hold Lungs Empty", 4, "....")
    ]
    print("\n=== [DxSkills: 60-Second Spatial Detachment Guide] ===")
    print("Gaze at an object 20+ feet away. Release linear tension from the neck and eyes.\n")
    try:
        for c in range(1, cycles + 1):
            print(f"--- [Cycle {c} of {cycles}] ---")
            for name, duration, visual in phases:
                for s in range(duration, 0, -1):
                    sys.stdout.write(f"\r[{visual}] {name}: {s}s remaining... ")
                    sys.stdout.flush()
                    time.sleep(1)
            print("\r[OK] Cycle complete.                        ")
        print("\n[DxSkills] Spatial reset complete. Working memory cleared. Resume fresh!")
    except KeyboardInterrupt:
        print("\n\n[DxSkills] Reset aborted. Welcome back.")

if __name__ == "__main__":
    report = calculate_cognitive_stamina(minutes_active=25, words_drafted=450)
    print_stamina_report(report)
