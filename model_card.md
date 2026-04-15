# Model Card: VibeMatch 1.0

---

## 1. Model Name

**VibeMatch 1.0**

A content-based music recommender that scores songs against a user taste profile and returns the top matches.

---

## 2. Goal / Task

The system takes a user's preferred genre, mood, energy level, and acoustic preference. It scores every song in the catalog against those preferences. It returns the top 5 songs with the highest scores.

It does not learn from listening history. It does not update over time. Every recommendation comes purely from comparing song features to a fixed profile.

---

## 3. Data Used

The catalog has 20 songs in a CSV file. Each song has 10 fields: id, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness.

The dataset covers 17 genres and 16 moods. 10 songs came from the starter file. 10 were added manually to increase genre diversity.

Limits:
- 15 out of 17 genres have only one song in the catalog
- All feature values were assigned by hand, not measured from real audio
- No songs in non-English languages or from non-Western music traditions
- No real user listening data was used

---

## 4. Algorithm Summary

Each song gets a score between 0.0 and 1.0. Higher means a better match.

The score is built from four parts:

- **Genre match**: +0.40 if the song's genre matches the user's target, otherwise +0.00
- **Mood match**: +0.30 if the song's mood matches, otherwise +0.00
- **Energy**: up to +0.20 based on how close the song's energy is to the user's target value. A song is not rewarded for being high or low — only for being close.
- **Acousticness**: up to +0.10 based on whether the user prefers acoustic or electronic sound. The score shifts toward whichever the user wants.

Genre and mood are binary — they either match or they don't. Energy and acousticness are continuous — they reward closeness rather than a threshold.

---

## 5. Observed Behavior / Biases

**The single-genre trap creates unequal results across users.**

15 of 17 genres have exactly one song. A classical or reggae user gets one strong match at position #1 and then four near-random results in positions #2–5. A lofi user gets three strong matches because there are three lofi songs. The catalog doesn't serve all users equally, even though the scoring logic treats them the same way.

**Genre outweighs mood.**

Genre carries 0.40 weight and mood carries 0.30. A pop song with the wrong mood (0.40 + 0.00 = 0.40) can beat a non-pop song with the right mood (0.00 + 0.30 = 0.30). The system is more loyal to genre than to emotional fit.

**Mood exact-match ignores similar moods.**

"Relaxed" and "chill" mean nearly the same thing, but the system treats them as completely different. A jazz/relaxed song scores 0.00 on mood for a user who wants "chill." There is no partial credit for adjacent moods.

**Genre adjacency is invisible.**

Metal and EDM are treated as equally wrong for a rock user because neither passes the exact genre check. The system has no concept that metal is closer to rock than EDM is.

---

## 6. Evaluation Process

Three profiles were tested by running `python -m src.main pop`, `python -m src.main lofi`, and `python -m src.main rock`:

| Profile | Genre | Mood | Energy | Acoustic |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.85 | no |
| Chill Lofi | lofi | chill | 0.38 | yes |
| Deep Intense Rock | rock | intense | 0.91 | no |

For each profile, position #1 was an exact genre and mood match with a score near 1.0. That held for all three: Sunrise City (0.98), Library Rain (0.98), Storm Runner (0.99).

Two results were unexpected. First, Gym Hero (pop, intense) outranked Rooftop Lights (indie pop, happy) for the pop profile even though Rooftop Lights had the right mood. Genre weight won over mood weight. Second, Iron Reckoning (metal, angry) tied with Drop Zone (EDM, energetic) at 0.28 for the rock profile. Metal is much closer to rock than EDM is, but both scored 0 on genre and 0 on mood, so the system could not tell them apart.

Profile pairs were also compared. Pop and Lofi had zero shared songs in their top 5. Pop and Rock shared one song (Gym Hero) because both prefer high energy and electronic production — mood was the only difference. Lofi and Rock were completely opposite on every dimension and had no overlap.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**

This is a classroom simulation. It is designed to demonstrate how content-based filtering works. It works on a small fixed catalog with a manually set user profile. It is for learning, not deployment.

**Not intended for:**

- Real music apps or production systems
- Users with complex taste that spans multiple genres or moods
- Personalization based on play history, skips, or ratings
- Catalogs larger than a few hundred songs without reworking the scoring and catalog balance

---

## 8. Ideas for Improvement

**1. Group similar genres.**
Instead of exact genre match, cluster related genres (rock, metal, punk → "heavy"). A rock user would get partial credit for a metal song instead of zero. This directly fixes the genre adjacency problem.

**2. Score mood by similarity, not exact match.**
Map moods onto a scale: chill → relaxed → neutral → focused → intense. Award partial credit based on distance. This would stop "relaxed" from scoring the same as "angry" for a user who wants "chill."

**3. Enforce catalog balance.**
Require at least 3 songs per genre before including that genre. This stops niche-genre users from getting one good result and four random ones. Alternatively, add a diversity check that prevents the top 5 from being dominated by a single genre.

---

## 9. Personal Reflection

**Biggest learning moment**

The biggest learning moment was running the Deep Intense Rock profile and watching Iron Reckoning (metal) tie with Drop Zone (EDM) at 0.28. Metal is obviously closer to rock than EDM is. But the system had no way to know that. It only knows whether a genre string matches exactly. That gap — between what feels obvious to a human and what the algorithm can actually see — is something I didn't fully appreciate until I watched it happen in the output. It made the limitations of rule-based systems feel real, not just theoretical.

**Using AI tools — what helped and what needed checking**

AI tools were useful for scaffolding quickly. The scoring formula, the CSV loader, the formatted output — those came together fast. Where I had to slow down and verify was around the weight values and the feature selection. The AI suggested reasonable defaults, but "reasonable" doesn't mean correct for this specific catalog. I had to manually check that a genre-weight of 0.40 actually produced the ranking behavior I expected, not just assume it would. The bias analysis was also something I had to reason through myself — the AI could describe a formula, but it couldn't tell me whether the formula was fair for a classical music listener until I looked at the actual scores.

**What surprised me about simple algorithms feeling like recommendations**

I expected the output to feel mechanical. It didn't. When the Chill Lofi profile returned Library Rain and Midnight Coding at the top, it genuinely felt like something a person might suggest. The system doesn't know anything about music — it's just arithmetic on four numbers — but the output looked intentional. That surprised me. It suggests that a lot of what makes a recommendation feel "smart" is just matching a few strong signals correctly, not deep understanding. Genre and mood alone carry 70% of the score. Get those two right and the result reads as sensible even if the math underneath is trivial.

**What I'd try next**

First, I'd replace exact genre matching with a similarity cluster — group rock, metal, and punk together so adjacent genres get partial credit. That one change would fix the biggest flaw in the current system. Second, I'd add a diversity check to stop the top 5 from being the same genre every time. If positions 1 and 2 both match the genre, position 3 should actively look for something different. Third, I'd want to test the system against real user feedback — give someone a profile and ask them whether the top 5 results actually match how they feel. Right now I have no idea whether my weights reflect how real people weigh genre vs mood vs energy. That's the only data that would actually matter.
