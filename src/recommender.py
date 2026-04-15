from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "target_energy":  user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        scored = []
        for song in self.songs:
            song_dict = {
                "genre":        song.genre,
                "mood":         song.mood,
                "energy":       song.energy,
                "acousticness": song.acousticness,
            }
            score, _ = score_song(user_prefs, song_dict)
            scored.append((score, song))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [song for _, song in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = {
            "genre":          user.favorite_genre,
            "mood":           user.favorite_mood,
            "target_energy":  user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }
        song_dict = {
            "genre":        song.genre,
            "mood":         song.mood,
            "energy":       song.energy,
            "acousticness": song.acousticness,
        }
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":            int(row["id"]),
                "title":         row["title"],
                "artist":        row["artist"],
                "genre":         row["genre"],
                "mood":          row["mood"],
                "energy":        float(row["energy"]),
                "tempo_bpm":     float(row["tempo_bpm"]),
                "valence":       float(row["valence"]),
                "danceability":  float(row["danceability"]),
                "acousticness":  float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Returns (score, reasons) where score is 0.0–1.0 and reasons is a
    list of strings explaining each term's contribution.

    Weights:
        genre match   0.40
        mood match    0.30
        energy        0.20  (proximity: 1 - |song - target|)
        acousticness  0.10  (proximity toward or away from acoustic)
    """
    score = 0.0
    reasons = []

    # Genre (0.40) — exact match only
    if song["genre"] == user_prefs.get("genre", ""):
        score += 0.40
        reasons.append(f"genre '{song['genre']}' matches (+0.40)")
    else:
        reasons.append(f"genre '{song['genre']}' doesn't match '{user_prefs.get('genre', '')}' (+0.00)")

    # Mood (0.30) — exact match only
    if song["mood"] == user_prefs.get("mood", ""):
        score += 0.30
        reasons.append(f"mood '{song['mood']}' matches (+0.30)")
    else:
        reasons.append(f"mood '{song['mood']}' doesn't match '{user_prefs.get('mood', '')}' (+0.00)")

    # Energy (0.20) — proximity scoring
    target_energy = user_prefs.get("target_energy", 0.5)
    energy_proximity = 1.0 - abs(song["energy"] - target_energy)
    energy_contribution = round(0.20 * energy_proximity, 4)
    score += energy_contribution
    reasons.append(
        f"energy {song['energy']:.2f} vs target {target_energy:.2f} (+{energy_contribution:.2f})"
    )

    # Acousticness (0.10) — proximity toward acoustic or electronic
    likes_acoustic = user_prefs.get("likes_acoustic", False)
    acousticness_bonus = song["acousticness"] if likes_acoustic else 1.0 - song["acousticness"]
    acoustic_contribution = round(0.10 * acousticness_bonus, 4)
    score += acoustic_contribution
    direction = "acoustic" if likes_acoustic else "electronic"
    reasons.append(
        f"acousticness {song['acousticness']:.2f} ({direction} preference, +{acoustic_contribution:.2f})"
    )

    return round(score, 4), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song, sorts by score descending, returns the top k.
    Each result is (song_dict, score, explanation_string).
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, score, explanation))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
