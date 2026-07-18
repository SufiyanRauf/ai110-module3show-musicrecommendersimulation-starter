# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users

One weakness I found is that the recommender treats genre as an exact match, so it ends up favoring the genres that have the most songs in my catalog. My dataset has three lofi tracks but only one reggae or metal track. A lofi listener gets a few real genre matches near the top, but a metal listener gets one real match and then filler. The filler happens because the energy score gives points to almost every song, so once a user runs out of songs in their own genre, the list just fills with whatever sits closest to their target energy. Basically it works best for common tastes and worst for niche ones.  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

Stress test output from running the five profiles in src/main.py:

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
3. Focus Flow by LoRoom - score 3.90
   because: genre match (+2.0), energy close (+0.9), acoustic bonus (+1.0)
4. Spacewalk Thoughts by Orbit Bloom - score 2.98
   because: mood match (+1.0), energy close (+0.98), acoustic bonus (+1.0)
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

I tested five listener profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, a conflicting one that wants high energy of 0.9 but a sad, melancholic mood, and an unknown genre one that likes k-pop, which is not in my catalog. For each one I looked at the top five songs and asked myself if that is what the listener would actually want.

The biggest surprise was the conflicting profile. It asks for high energy but a melancholic mood, and the song that came out on top was Winter Nocturne, a slow classical piece with very low energy. My first thought was that something was broken. But it actually makes sense once you look at the points: the genre and mood match are worth 3 together, and the energy part can only ever add up to 1, so a strong genre and mood match beats the energy even when the energy is completely wrong.

The other thing I noticed is how often Gym Hero shows up. Gym Hero is a pop song with really high energy, so any time someone asks for happy or high energy pop, it grabs 2 points just for being pop and picks up a good chunk of the energy points on top of that. Even though it is not actually tagged as happy, it still ends up near the top. It is not a bug, it is just that a loud pop song is a decent partial match for a lot of upbeat tastes.

Comparing the profiles side by side helped me see what each preference is really doing. The most interesting case is that three of my profiles all ask for the same 0.9 energy, High-Energy Pop, Deep Intense Rock, and the conflicting one, but they end up with completely different top songs. Pop gets Sunrise City, rock gets Storm Runner, and the conflicting one gets a slow classical track. That told me energy is not really the thing steering the results, the genre and mood are. Chill Lofi sits at the opposite end from those three. It wants calm acoustic music, so its list is full of quiet lofi and ambient songs that never show up for the high energy profiles, and it had the cleanest list because lofi is the one genre I have several songs for. The unknown genre profile was the weakest of all. Since k-pop is not in my catalog it never gets the genre bonus, so its scores stay low and the list is just whatever happens to be happy and around medium energy. Lofi and the k-pop profile are a good contrast for that reason, one has real matches to work with and the other has none.

Overall the outputs look valid to me. When a profile has a real genre match in my catalog the top pick makes sense, and the only strange results come from profiles that contradict themselves or ask for a genre I do not have.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
