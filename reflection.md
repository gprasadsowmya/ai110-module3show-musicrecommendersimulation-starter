# Profile Comparison Reflections

## Pair 1: High-Energy Pop vs Chill Lofi

These two profiles are opposites on almost every dimension. Pop targets energy 0.85 with `likes_acoustic: False`; Lofi targets energy 0.38 with `likes_acoustic: True`. Their top-5 results share zero songs, which is exactly what you'd expect — the catalog cleanly separates high-energy electronic tracks from low-energy acoustic ones.

What's interesting is how the falloff works differently. The Lofi profile drops from 0.98 (#1 Library Rain) to 0.96 (#2 Midnight Coding) and then to 0.67 (#3 Focus Flow) — a small gap then a bigger one. The Pop profile drops from 0.98 (#1 Sunrise City) straight to 0.68 (#2 Gym Hero). The Lofi user gets two near-perfect matches because there are three lofi songs in the catalog with similar energy. The Pop user's second result is already missing the mood. This shows catalog density matters as much as scoring weights.

The acousticness term also flips completely between these two profiles. Songs like Autumn Sonata (acousticness 0.97) score near the top of the acousticness contribution for Lofi but near zero for Pop. The same feature adds or subtracts depending entirely on which side of `likes_acoustic` you're on.

---

## Pair 2: High-Energy Pop vs Deep Intense Rock

These two profiles share a preference for high energy and electronic production (`likes_acoustic: False`), so you'd expect some overlap — and there is. Gym Hero (pop, intense, energy 0.93) appeared in the top 5 for both profiles, at #2 for Pop (0.68) and #2 for Rock (0.59).

The difference is driven entirely by mood. Pop wants "happy" and Rock wants "intense." Gym Hero has mood "intense," so it scores 0.68 for Pop (genre match + no mood match) and 0.59 for Rock (no genre match + mood match). The scores are close because a genre match and a mood match are worth nearly the same weight (0.40 vs 0.30). This is a good example of the scoring formula trading off two independent signals.

What surprised me here is that Iron Reckoning (metal, angry) landed at #4 for the Rock profile with only 0.28 — below Drop Zone (EDM, energetic) at 0.29. Musically, metal is far closer to rock than EDM is. But the system treats both as equally wrong because neither passes the exact genre match. Genre adjacency is invisible to the scorer.

---

## Pair 3: Chill Lofi vs Deep Intense Rock

This is the most extreme pair. Lofi wants quiet, acoustic, chill; Rock wants loud, electronic, intense. Energy targets are 0.38 vs 0.91 — separated by 0.53 points on a 0–1 scale. Their top-5 results have no overlap at all.

The energy proximity term behaves very differently for each. For Lofi, songs like Midnight Coding (0.42) and Library Rain (0.35) land within 0.04 of the target, earning close to the full +0.20. For Rock, Storm Runner (0.91) hits the target exactly, but the songs that follow — Drop Zone (0.95), Iron Reckoning (0.97) — are only 0.04–0.06 away and still earn near-maximum energy scores. Both profiles get tight energy clusters at the top, but the Lofi cluster is quiet and the Rock cluster is loud.

The acousticness term flips sign completely between these two. Spacewalk Thoughts (acousticness 0.92) earns +0.09 for the Lofi profile and would earn only +0.01 for the Rock profile. Drop Zone (acousticness 0.03) earns +0.10 for Rock and +0.00 for Lofi. The same two songs are good candidates for one user and nearly worthless for the other — which is the correct behavior and confirms the feature is doing its job.
