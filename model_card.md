# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

MusicalAuraMatch 1.0

---

## 2. Intended Use

MusicalAuraMatch is a classroom project, not a real product. It suggests songs from a small fixed catalog by matching them to a made up taste profile. It assumes each user can be boiled down to one favorite genre, one favorite mood, a target energy level, and whether they like acoustic music. It is meant for exploring how recommenders work, not for real users. It should not be used for real recommendations. And it is not fair or complete, because the catalog is tiny and uneven.

---

## 3. How the Model Works

The goal is to guess which songs a listener will like and put the best ones at the top. Each song has a genre, a mood, an energy level, and a few other numbers like how acoustic it is. The user gives a favorite genre, a favorite mood, a target energy, and whether they like acoustic music. The model gives every song a score. A song earns 2 points if its genre matches, 1 point if its mood matches, up to 1 more point for having an energy level close to what the user wants, and 1 bonus point if the user likes acoustic music and the song is very acoustic. Then it picks the top five by score, but it lowers a song's score if another song by the same artist is already in the list, so one artist does not take over. Each pick shows the reason it was chosen. The main change from the starter code was filling in this scoring and adding the reasons.

---

## 4. Data

The catalog has 17 songs. I started with 10 and added 7 more to cover more genres and moods. Each song has a title, artist, genre, mood, and five number features: energy, tempo, valence, danceability, and acousticness. The genres include pop, lofi, rock, jazz, ambient, hip hop, edm, classical, country, metal, r&b, and reggae. The data is small and uneven, lofi has three songs while most genres only have one. There are no lyrics, no language, and no artist popularity, so a lot of what makes people actually like a song is missing.

---

## 5. Strengths

The model works best for users whose favorite genre has a few songs in the catalog, like a lofi or pop fan. For those users the top picks feel right, they get songs that match on genre, mood, and energy all at once. It is also good at giving a clear reason for every pick, which makes the results easy to understand. When I tested a chill lofi profile, the top songs were exactly the calm, quiet tracks I expected.

---

## 6. Limitations and Bias

One weakness I found is that the recommender treats genre as an exact match, so it ends up favoring the genres that have the most songs in my catalog. My dataset has three lofi tracks but only one reggae or metal track, so a lofi listener gets a few real genre matches near the top, but a metal listener gets one real match and then filler. The filler happens because the energy score gives points to almost every song, so once a user runs out of songs in their own genre, the list just fills with whatever sits closest to their target energy. Basically it works best for common tastes and worst for niche ones.

---

## 7. Evaluation

I tested five listener profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, a conflicting one that wants high energy of 0.9 but a sad, melancholic mood, and an unknown genre one that likes k-pop, which is not in my catalog. For each one I looked at the top five songs and asked myself if that is what the listener would actually want.

The biggest surprise was the conflicting profile. It asks for high energy but a melancholic mood, and the song that came out on top was Winter Nocturne, a slow classical piece with very low energy. My first thought was that something was broken. But it actually makes sense once you look at the points: the genre and mood match are worth 3 together, and the energy part can only ever add up to 1, so a strong genre and mood match beats the energy even when the energy is completely wrong.

The other thing I noticed is how often Gym Hero shows up. Gym Hero is a pop song with really high energy, so any time someone asks for happy or high energy pop, it grabs 2 points just for being pop and picks up a good chunk of the energy points on top of that. Even though it is not actually tagged as happy, it still ends up near the top. It is not a bug, it is just that a loud pop song is a decent partial match for a lot of upbeat tastes.

Comparing the profiles side by side helped me see what each preference is really doing. The most interesting case is that three of my profiles all ask for the same 0.9 energy, High-Energy Pop, Deep Intense Rock, and the conflicting one, but they end up with completely different top songs. Pop gets Sunrise City, rock gets Storm Runner, and the conflicting one gets a slow classical track. That told me energy is not really the thing steering the results, the genre and mood are. Chill Lofi sits at the opposite end from those three. It wants calm acoustic music, so its list is full of quiet lofi and ambient songs that never show up for the high energy profiles, and it had the cleanest list because lofi is the one genre I have several songs for. The unknown genre profile was the weakest of all. Since k-pop is not in my catalog it never gets the genre bonus, so its scores stay low and the list is just whatever happens to be happy and around medium energy. Lofi and the k-pop profile are a good contrast for that reason, one has real matches to work with and the other has none.

Overall the outputs look valid to me. When a profile has a real genre match in my catalog the top pick makes sense, and the only strange results come from profiles that contradict themselves or ask for a genre I do not have.

The raw terminal output for all five profiles is below:

```
=== High-Energy Pop ===
Profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
1. Sunrise City by Neon Echo - score 3.92
   because: genre match (+2.0), mood match (+1.0), energy close (+0.92)
2. Gym Hero by Max Pulse - score 2.97
   because: genre match (+2.0), energy close (+0.97)
3. Rooftop Lights by Indigo Parade - score 1.86
   because: mood match (+1.0), energy close (+0.86)
4. Storm Runner by Voltline - score 0.99
   because: energy close (+0.99)
5. Neon Pulse by Ravelight - score 0.95
   because: energy close (+0.95)
```

```
=== Chill Lofi ===
Profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.3, 'likes_acoustic': True}
1. Library Rain by Paper Lanterns - score 4.95
   because: genre match (+2.0), mood match (+1.0), energy close (+0.95), acoustic bonus (+1.0)
2. Midnight Coding by LoRoom - score 4.88
   because: genre match (+2.0), mood match (+1.0), energy close (+0.88), acoustic bonus (+1.0)
3. Spacewalk Thoughts by Orbit Bloom - score 2.98
   because: mood match (+1.0), energy close (+0.98), acoustic bonus (+1.0)
4. Focus Flow by LoRoom - score 2.90
   because: genre match (+2.0), energy close (+0.9), acoustic bonus (+1.0), diversity penalty (-1.0)
5. Coffee Shop Stories by Slow Stereo - score 1.93
   because: energy close (+0.93), acoustic bonus (+1.0)
```

```
=== Deep Intense Rock ===
Profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
1. Storm Runner by Voltline - score 3.99
   because: genre match (+2.0), mood match (+1.0), energy close (+0.99)
2. Gym Hero by Max Pulse - score 1.97
   because: mood match (+1.0), energy close (+0.97)
3. Neon Pulse by Ravelight - score 0.95
   because: energy close (+0.95)
4. Concrete Kings by Blockwise - score 0.94
   because: energy close (+0.94)
5. Iron Verdict by Ashfall - score 0.93
   because: energy close (+0.93)
```

```
=== Conflicting High-Energy Sad ===
Profile: {'genre': 'classical', 'mood': 'melancholic', 'energy': 0.9}
1. Winter Nocturne by Clara Voss - score 3.32
   because: genre match (+2.0), mood match (+1.0), energy close (+0.32)
2. Storm Runner by Voltline - score 0.99
   because: energy close (+0.99)
3. Gym Hero by Max Pulse - score 0.97
   because: energy close (+0.97)
4. Neon Pulse by Ravelight - score 0.95
   because: energy close (+0.95)
5. Concrete Kings by Blockwise - score 0.94
   because: energy close (+0.94)
```

```
=== Unknown Genre ===
Profile: {'genre': 'kpop', 'mood': 'happy', 'energy': 0.5}
1. Rooftop Lights by Indigo Parade - score 1.74
   because: mood match (+1.0), energy close (+0.74)
2. Sunrise City by Neon Echo - score 1.68
   because: mood match (+1.0), energy close (+0.68)
3. Slow Sunday by Vela Grey - score 1.00
   because: energy close (+1.0)
4. Island Time by Coral Sound - score 0.98
   because: energy close (+0.98)
5. Dusty Backroads by Hazel Pines - score 0.95
   because: energy close (+0.95)
```

---

## 8. Future Work

- Add partial credit for related genres, so a lofi fan can also get ambient or jazz songs that fit the same mood.
- Grow the catalog and balance it, so every genre has a fair number of songs instead of just one.
- Use more of the features I already have, like valence and danceability, instead of leaning so much on genre and energy.

---

## 9. Personal Reflection

The biggest thing I learned is that a recommender is really just a scoring rule plus a sort. Once I saw that every song gets a number and the list is just sorted by that number, the whole idea stopped feeling like magic. My biggest learning moment was watching the conflicting profile pick a slow classical song even though it asked for high energy. That is when the point weights actually clicked for me, because I could see genre and mood outweighing the energy.

AI tools helped me a lot with the boring parts, like writing the CSV loader and remembering Python syntax. They were also good for talking through the scoring math and for ideas on edge case profiles to test. I did have to double-check them though. A few times the AI wanted to over explain simple functions or claimed a result that was not quite right, so I ran the code myself and checked the actual output before trusting it.

What surprised me most is how much a simple set of if statements can feel like a real recommendation. There is no machine learning here, just adding points, but the top picks still felt right for most profiles. It made me realize the big apps probably start from simple rules like this before they get fancy.

If I kept working on this I would add partial credit for similar genres, grow the dataset so it is more balanced, and use more of the features I already collect. I would also like to let a user pick more than one favorite genre, since real taste is never just one thing.
