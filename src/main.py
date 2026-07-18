"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# A few different listeners to stress test the scoring, including some
# tricky ones (conflicting prefs, and a genre that isn't in the catalog).
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.3, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
    "Conflicting High-Energy Sad": {"genre": "classical", "mood": "melancholic", "energy": 0.9},
    "Unknown Genre": {"genre": "kpop", "mood": "happy", "energy": 0.5},
}


def show_recommendations(name, user_prefs, songs, k=5):
    recommendations = recommend_songs(user_prefs, songs, k=k)
    print(f"=== {name} ===")
    print(f"Profile: {user_prefs}")
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{i}. {song['title']} by {song['artist']} - score {score:.2f}")
        print(f"   because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")
    for name, prefs in PROFILES.items():
        show_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
