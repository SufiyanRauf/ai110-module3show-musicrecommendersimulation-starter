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

I tried the weight shift experiment. I doubled how much energy counts and cut the genre points in half, from 2.0 down to 1.0. When I ran it, the number one pick for every profile stayed the same, but the middle of the list shuffled around. Songs that were not the right genre but had a really close energy moved up. For example a chill ambient song jumped ahead of a real lofi song in the Chill Lofi list, just because its energy was almost perfect. So the change made the results different but not really more accurate. It told me that genre plus mood together still control the top pick, and energy mostly matters for breaking ties lower down. That is why I kept the original weights.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

- It only works on a tiny catalog of 17 songs, so there is not much variety.
- It does not understand lyrics, language, or what a song is actually about.
- The catalog is uneven, so lofi and pop users get better results than niche genres with only one song.
- It treats genre as an exact match, which can trap a user in one genre and miss songs they would like.
- It has no idea about a real person's history, their mood that day, or what is popular, so it is only a rough guess.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

The main thing this project taught me about recommenders is that a prediction is just a comparison. My code lines up what a user says they want against the features of each song, gives out points for the parts that match, and the songs with the most points become the guesses. There is no real understanding of the music happening, it is just measuring overlap between two lists of features.

The part that stuck with me is how unfair that can get without anyone meaning it to. Because my catalog has way more lofi songs than anything else, lofi fans get a full, accurate list and someone into metal gets one real match and a bunch of filler. That imbalance came straight from the data and from choosing to reward exact genre matches so heavily. It made me see that in a real recommender the choices about what data to include and what to score highest can decide who the system works well for and who gets left out.



