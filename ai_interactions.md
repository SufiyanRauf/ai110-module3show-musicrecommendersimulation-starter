# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The Strategy pattern. Each ranking mode is a different scoring strategy that the recommender can swap in without changing the rest of the code. The modes I made are balanced, genre-first, mood-first, and energy-focused.

**How did AI help you brainstorm or implement it?**

I described what I wanted, a few different ways to rank songs that I could switch between, and asked the AI what design pattern would fit. It suggested the Strategy pattern and explained the idea as having interchangeable algorithms behind one common interface. We talked through two ways to build it. One was a full version with a separate class for each strategy, and the other was a lighter version where each mode is just a set of weights the scorer looks up. The AI said the class version would be overkill for a project this small, so I went with the weights version. I double checked its suggestion by making sure the balanced mode still gave the exact same results as before, so I knew I had not broken the old behavior.

**How does the pattern appear in your final code?**

The strategies live in the SCORING_MODES dictionary in recommender.py, where each mode name maps to its weights. score_song takes those weights and recommend_songs looks up the weights for the chosen mode. In main.py there is a MODE setting to switch the whole run, and a compare_modes function that prints the same listener under every mode so you can see the rankings change.
