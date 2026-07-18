import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

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
    """Object-oriented version of the recommender used by the tests."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a user, highest score first."""
        prefs = self._user_prefs(user)
        ranked = sorted(self.songs, key=lambda s: score_song(prefs, asdict(s))[0], reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a short reason string for why a song was picked."""
        prefs = self._user_prefs(user)
        score, reasons = score_song(prefs, asdict(song))
        if not reasons:
            return f"{song.title} scored {score} with no strong matches"
        return f"{song.title} scored {score}: " + ", ".join(reasons)

    @staticmethod
    def _user_prefs(user: UserProfile) -> Dict:
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

def load_songs(csv_path: str) -> List[Dict]:
    """Read the songs CSV and return them as a list of dicts."""
    songs = []
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's prefs and list the reasons why."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    if "energy" in user_prefs:
        closeness = round(1.0 - abs(song["energy"] - user_prefs["energy"]), 2)
        score += closeness
        reasons.append(f"energy close (+{closeness})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.6:
        score += 1.0
        reasons.append("acoustic bonus (+1.0)")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, then pick the top k while limiting repeat artists."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    picked = []
    used_artists = set()
    while len(picked) < k and scored:
        # pick the best remaining song, with a penalty for artists already picked
        best = None
        for song, score, reasons in scored:
            adjusted = score
            note = list(reasons)
            if song["artist"] in used_artists:
                adjusted -= 1.0
                note.append("diversity penalty (-1.0)")
            if best is None or adjusted > best[1]:
                best = (song, adjusted, note)

        song, adjusted, note = best
        explanation = ", ".join(note) if note else "no strong matches"
        picked.append((song, round(adjusted, 2), explanation))
        used_artists.add(song["artist"])
        scored = [item for item in scored if item[0] is not song]

    return picked
