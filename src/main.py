"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os
import sys
from .recommender import load_songs, recommend_songs
from typing import Dict, List, Tuple

_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
_WIDTH = 60


def _score_bar(score: float, width: int = 20) -> str:
    filled = int(round(score * width))
    return "[" + "#" * filled + "-" * (width - filled) + "]"


def print_recommendations(
    user_prefs: Dict,
    results: List[Tuple[Dict, float, str]],
) -> None:
    acoustic = "yes" if user_prefs.get("likes_acoustic") else "no"
    profile_name = user_prefs.get("name", "Custom")

    print("=" * _WIDTH)
    print(f"  RECOMMENDATIONS  |  Profile: {profile_name}")
    print(
        f"  genre: {user_prefs.get('genre', '?')}  |  "
        f"mood: {user_prefs.get('mood', '?')}  |  "
        f"energy: {user_prefs.get('target_energy', '?')}  |  "
        f"acoustic: {acoustic}"
    )
    print("=" * _WIDTH)

    for rank, (song, score, explanation) in enumerate(results, start=1):
        print()
        print(f"  #{rank}  {song['title']:<30}  {score:.2f}  {_score_bar(score)}")
        print(f"       {song['artist']}  |  {song['genre']}  |  {song['mood']}")
        for reason in explanation.split("; "):
            print(f"       - {reason}")
        print("  " + "-" * (_WIDTH - 2))

    print()


def main() -> None:
    songs = load_songs(_DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    # --- Taste profiles ---
    # genre and mood are exact-match signals (highest weights).
    # target_energy uses proximity scoring: closer to the song's value = higher score.
    # likes_acoustic boosts acoustic songs when True, electronic when False.

    # Profile 1: upbeat, radio-friendly pop — high energy, positive, electronic production
    high_energy_pop = {
        "name":           "High-Energy Pop",
        "genre":          "pop",
        "mood":           "happy",
        "target_energy":  0.85,   # loud and driving, matches Sunrise City / Gym Hero range
        "target_valence": 0.82,   # strongly positive and upbeat
        "likes_acoustic": False,  # wants polished, produced sound
    }

    # Profile 2: background study music — low energy, mellow, acoustic-leaning
    chill_lofi = {
        "name":           "Chill Lofi",
        "genre":          "lofi",
        "mood":           "chill",
        "target_energy":  0.38,   # quiet enough to not distract
        "target_valence": 0.58,   # neutral-positive, not emotionally loaded
        "likes_acoustic": True,   # warm, vinyl-texture sound preferred
    }

    # Profile 3: high-intensity listening — heavy, distorted, fast
    deep_intense_rock = {
        "name":           "Deep Intense Rock",
        "genre":          "rock",
        "mood":           "intense",
        "target_energy":  0.91,   # near-maximum, matches Storm Runner
        "target_valence": 0.45,   # darker tone, not euphoric
        "likes_acoustic": False,  # electric guitars, not acoustic
    }

    profiles = {
        "pop":  high_energy_pop,
        "lofi": chill_lofi,
        "rock": deep_intense_rock,
    }

    # Optional: pass a profile key as a CLI argument, e.g. `python -m src.main pop`
    # With no argument, all three profiles run in sequence.
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    selected = [profiles[arg]] if arg in profiles else list(profiles.values())

    for user_prefs in selected:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(user_prefs, recommendations)


if __name__ == "__main__":
    main()
