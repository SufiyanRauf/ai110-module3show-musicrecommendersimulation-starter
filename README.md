# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My version is a small content-based recommender. It reads a list of songs from a CSV
file and compares them against a simple user taste profile. The profile has a favorite
genre, a favorite mood, a target energy level, and whether the person likes acoustic
music. Each song gets a score based on how well it matches, then the songs are sorted and
the top few are printed with a short reason for why each one was picked.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real recommenders like Spotify or YouTube mostly work by mixing two ideas. One is
collaborative filtering, which looks at what other people with similar taste listened to,
and the other is content-based filtering, which looks at the actual attributes of a song
like its energy or genre. They also watch stuff like skips and replays and how long you
listen, then feed all that into big ML models. My version is much smaller and only does
the content-based part. It compares a user's stated taste to each song's attributes and
scores how well they line up. I went with a simple scoring rule instead of chasing
accuracy, mostly because I wanted to be able to see why each song got recommended instead
of just trusting a number. That reason can be something like a matching genre or a close
energy level.

What each Song uses:

- genre, for example pop, lofi, or rock
- mood, for example happy, chill, or intense
- energy, on a scale of 0 to 1
- acousticness, on a scale of 0 to 1
- it also stores tempo_bpm, valence, and danceability. I might add those to the score later.

What the UserProfile stores:

- favorite_genre
- favorite_mood
- target_energy, a 0 to 1 value for the energy level they want
- likes_acoustic, either true or false

How a score is computed: each song earns points for a genre match, a mood match, how
close its energy is to target_energy, and an acoustic bonus if the user likes acoustic
songs. A higher total means a better fit.

How songs get chosen: every song is scored, the list is sorted from high to low, and the
top few are returned. How many come back is set by a number called k, which is 5 by
default.

The finalized scoring recipe, with the exact points each song can earn:

- genre match: +2.0 if the song genre matches my favorite genre
- mood match: +1.0 if the song mood matches my favorite mood
- energy closeness: up to +1.0, worked out as 1 minus how far the song energy is from my target energy
- acoustic bonus: +1.0 if I like acoustic music and the song acousticness is above 0.6

So the most a song can score is 5.0. I made genre worth twice as much as mood on purpose.
Genre feels like the bigger sign of whether a song is even my kind of music, and mood
already overlaps with the energy score, so weighting mood just as high would basically
judge the same thing twice.

The taste profile I am testing with is a chill lofi listener: favorite genre lofi,
favorite mood chill, target energy 0.3, and likes acoustic set to true.

Biases I expect: since genre is worth the most, the system leans too hard on the one genre
I picked. The +2.0 genre bonus is big enough to tip close calls, so a lofi song can still
beat a non-lofi song that fits my mood and energy a bit better. It would not beat a song
that nails mood, energy, and acoustic all at once, but on the close ones the genre points
decide it. So I mostly end up getting more lofi and not much else, which is kind of a
filter bubble. I could fix it later by lowering the genre weight or giving partial credit
for related genres.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 17

Profile: genre=pop, mood=happy, energy=0.8

Top recommendations:

1. Sunrise City by Neon Echo - score 3.98
   because: genre match (+2.0), mood match (+1.0), energy close (+0.98)

2. Gym Hero by Max Pulse - score 2.87
   because: genre match (+2.0), energy close (+0.87)

3. Rooftop Lights by Indigo Parade - score 1.96
   because: mood match (+1.0), energy close (+0.96)

4. Concrete Kings by Blockwise - score 0.96
   because: energy close (+0.96)

5. Night Drive Loop by Neon Echo - score 0.95
   because: energy close (+0.95)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



