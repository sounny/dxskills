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

def print_stamina_report(metrics, minutes_given=True, words_given=True):
    minutes = metrics["minutes_active"]
    words = metrics["words_drafted"]
    score = metrics["stamina_score"]
    print("\n=== [DxSkills: Cognitive Fatigue & Working Memory Stamina] ===")
    print(f"Formula result: {score} on {minutes} minutes and {words} words.")
    print("This figure is a formula on those numbers, not a measured saturation and not a medical or cognitive finding.")
    if not minutes_given:
        print("Minutes were not given. The formula used 0 minutes. It did not assume a 30 minute session.")
    if not words_given:
        print("Words were not given. The formula used 0 words. It did not assume 500 words.")
    print("No session was observed.")
    if score < 45.0:
        print(
            f"Reset Due: the formula crossed below the stated threshold of 45 "
            f"(result {score} on {minutes} minutes and {words} words). "
            "That label is the formula crossing a threshold, not an observed session."
        )
    print("\n### General note")
    print("Background only, not a finding about this run.")
    print("- The phonological loop is a working-memory idea from the Baddeley model. This sentence does not measure you.")
    print("- Some people vary linear reading with spatial diagrams. This is not a diagnosis and not evidence that a ceiling was reached.")

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
