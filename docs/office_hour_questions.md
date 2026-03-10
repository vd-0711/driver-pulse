# Driver Pulse — Office Hour Responses

---

## OFFICE HOUR 1: Design & Discovery

**Topic: Scoping, Product Vision, and Data Understanding**

---

Hi team,

Thank you for the case study — it's a genuinely interesting product problem. We've fully explored the dataset and have our architecture locked in. I want to use this session not to ask basic questions, but to pressure-test three specific decisions we made and get your signal on whether we're calibrated correctly.

---

**Question 1: Signal prioritisation — we chose parity over hierarchy**

Our hypothesis going in was that audio (argument/conflict signals) should be weighted more heavily than motion because the *driver's* biggest concern is passenger conflict, not traffic braking. But as we dug into the data, we found that audio alone is extremely noisy — a loud radio, a phone call, a laughing passenger all register as elevated dB. Motion alone is the opposite problem: it catches every pothole.

We resolved this by giving motion a slight edge (55/45 weighting) and requiring *both signals together* for a `conflict_moment` classification. This means we only fire a high-severity flag when the physics and the audio agree.

**Our question:** Does the product intent align with this conservative approach? Specifically — is the goal to capture *every* uncomfortable moment for the driver's reflection (higher sensitivity, more false positives) or to surface only *undeniable* moments that deserve attention (lower sensitivity, fewer false positives, higher trust)? The right answer changes our threshold significantly.

---

**Question 2: The 20-minute stop problem — what counts as "driving"?**

When computing earnings velocity (₹/hr), we currently measure from shift start to now, including idle time. This means a driver who stops for 20 minutes to eat lunch will see her velocity drop sharply, even if she was on pace before the break.

We've implemented a simple constant-velocity linear model (`velocity = cumulative_earnings / elapsed_hours`). But we're wondering: should elapsed_hours be *all time since shift start* or *only active trip time*?

Using active trip time only would give a more accurate picture of driving efficiency but would overestimate what the driver will actually earn by end of shift (she can't drive 100% of the remaining time). Using total elapsed time is honest but demoralising during rest breaks.

**Our question:** What does the product team consider the right "denominator" here? Is the goal to measure efficiency (active-only) or realistic goal progress (total elapsed)?

---

**Question 3: The sensor coverage gap — is this a data bug or a feature of real-world sparsity?**

We noticed the accelerometer and audio data cover only TRIP001–TRIP030 (30 of 220 trips). The remaining 190 trips have no sensor readings at all. We treated this as a dataset constraint — our pipeline correctly produces zero flags for those trips, and we surface a coverage notice in the dashboard.

But we want to check: is this intentional (simulating a driver who only recently installed the app, or a device with limited sensor access) or a data generation artifact? If it's intentional, we'd like to know so we can address it in our design document with the right framing — e.g., "Driver Pulse degrades gracefully when sensor data is unavailable, defaulting to earnings-only mode."

---

Thanks for your time. We're not looking for the "right answer" handed to us — we just want to make sure our tradeoff reasoning is pointed in the right direction before we finalise the design doc.

---

## OFFICE HOUR 2: Engineering & Implementation

**Topic: Implementation Hurdles, Algorithm Refinement, and System Tuning**

---

Hi again,

We have a working end-to-end system: modular pipeline, structured output CSVs, and a self-contained dashboard with 130 driver profiles. Our architecture is stable. This session is about three specific engineering trade-offs we're uncertain about.

---

**Question 1: Our conflict_moment rate is lower than the reference output — and we think we know why, but want to confirm**

The reference `flagged_moments.csv` contains 43 `conflict_moment` events. Our pipeline produces 8. The difference is real and we've traced the root cause: the reference appears to fuse signals with a more generous overlap window, or uses a lower combined_score threshold for conflict classification.

Our current setup: 120-second window, combined_score ≥ 0.75 for conflict_moment. If we drop the threshold to 0.60 and widen the window to 180 seconds, we'd produce ~35–40 conflict_moments, much closer to the reference.

**The trade-off we're wrestling with:** Widening the window means we'd sometimes fuse a braking event at T=200s with an audio spike at T=380s — that's 3 minutes apart, arguably two separate incidents in a 25-minute trip. We chose 120s precisely to avoid this. We'd rather have 8 high-confidence conflict_moments than 43 where some are coincidental co-occurrences.

**Our question:** Is matching the reference count the right optimisation target, or is the reference itself a *possible* output (not a ground truth)? If judges are evaluating reasoning quality over output similarity, we want to defend our 120s/0.75 thresholds. If output similarity is the primary metric, we'll tune down.

---

**Question 2: Earnings velocity for drivers mid-shift vs just-started — should we suppress early predictions?**

We've noticed that drivers with `current_hours < 1.0` produce wildly volatile velocity readings. A driver who completed one ₹400 trip in 30 minutes shows a velocity of ₹800/hr — but that doesn't mean she'll sustain that for 7 more hours.

We're currently showing the projection to all drivers regardless of shift age. The fix is straightforward: suppress the earnings forecast (show "Insufficient data — check back in 45 minutes") for drivers with fewer than 2 completed trips or less than 45 minutes elapsed.

**Our question:** What's the right confidence threshold for showing a forecast? We're thinking 2 trips / 45 minutes elapsed, but in a real-world Uber product, would you suppress the forecast entirely or show it with a confidence band (e.g., "Projected: ₹1,100–₹1,600 based on 1 trip")?

---

**Question 3: Rolling window vs snapshot — which does the product expect?**

Our current pipeline is a **snapshot model** — it reads the current state of all data and produces a single set of outputs. This is appropriate for a hackathon pipeline that runs on a static dataset.

A production Driver Pulse would need a **streaming model** — running continuously as new sensor readings arrive, updating the flag list in real-time.

We've designed the pipeline's functions to be stateless and composable so this migration is straightforward — `detect_motion_events()` can be called on a single new reading, and `fuse_signals()` can be called incrementally. But we haven't implemented the streaming layer.

**Our question:** For evaluation purposes, is a snapshot pipeline (which is what we built) sufficient to demonstrate the system's capabilities? Or would judges expect to see at minimum a simulated streaming loop — e.g., replaying the CSV row-by-row with a 100ms delay to simulate real-time ingestion?

If the latter, we can implement this in about 2 hours as a `simulate_stream.py` companion script. We just want to prioritise correctly.

---

Thank you. We've built something we're proud of and want to defend every decision clearly. Looking forward to your feedback.
