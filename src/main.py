"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, SCORING_MODES
from tabulate import tabulate


# A few different listeners to stress test the scoring, including some
# tricky ones (conflicting prefs, and a genre that isn't in the catalog).
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    "Conflicting High-Energy Sad": {"genre": "classical", "mood": "melancholic", "energy": 0.9},
    "Unknown Genre": {"genre": "kpop", "mood": "happy", "energy": 0.5},
}

# Change this to try a different ranking strategy for the stress test:
# "balanced", "genre-first", "mood-first", or "energy-focused".
MODE = "balanced"


def show_recommendations(name, user_prefs, songs, k=5, mode="balanced"):
    recommendations = recommend_songs(user_prefs, songs, k=k, mode=mode)
    rows = []
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([i, song["title"], song["artist"], f"{score:.2f}", explanation])
    print(f"=== {name} ===")
    print(f"Profile: {user_prefs}")
    print(tabulate(rows, headers=["#", "Song", "Artist", "Score", "Why"], tablefmt="grid", disable_numparse=True))
    print()


def compare_modes(name, user_prefs, songs, k=3):
    # show how the same listener's top picks change under each scoring mode
    print(f"##### Scoring mode comparison: {name} #####\n")
    for mode in SCORING_MODES:
        show_recommendations(f"{name} - {mode}", user_prefs, songs, k=k, mode=mode)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")
    for name, prefs in PROFILES.items():
        show_recommendations(name, prefs, songs, mode=MODE)

    mixed = {"genre": "pop", "mood": "chill", "energy": 0.5}
    compare_modes("Mixed taste - pop, chill, mid energy", mixed, songs)


if __name__ == "__main__":
    main()
