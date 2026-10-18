All three experiments are done. Everything below is on validation 2020-21, with the tuned models and seed 42. The current variant reproduces the tuned models exactly in all three experiments (checked in the code).

## X7: form window

**PR-AUC:**

| Variant | Logistic regression | Random forest | Gradient boosting | Network |
|---|---|---|---|---|
| Last 3 | 0.684 | 0.709 | 0.706 | 0.710 |
| **Last 5 (current)** | 0.706 | 0.725 | 0.715 | 0.741 |
| Last 10 | 0.717 | 0.733 | 0.734 | 0.734 |
| Season so far | 0.695 | 0.716 | 0.703 | 0.729 |
| **Career** | **0.740** | **0.744** | **0.733** | **0.750** |
| Last 5 + career | 0.721 | 0.727 | 0.722 | 0.723 |

**Change against last 5** (positive = better than last 5):

| Variant | Logistic regression | Random forest | Gradient boosting | Network |
|---|---|---|---|---|
| Last 3 | −0.022 (−0.046 to +0.004) | −0.016 (−0.043 to +0.008) | −0.009 (−0.038 to +0.012) | **−0.032 (−0.057 to −0.008)** |
| Last 10 | +0.011 (−0.016 to +0.032) | +0.008 (−0.023 to +0.033) | +0.018 (−0.013 to +0.045) | −0.007 (−0.028 to +0.013) |
| Season so far | −0.011 (−0.040 to +0.012) | −0.009 (−0.034 to +0.011) | −0.012 (−0.055 to +0.020) | −0.012 (−0.031 to +0.005) |
| **Career** | **+0.033 (−0.014 to +0.070)** | **+0.019 (−0.014 to +0.041)** | **+0.018 (−0.009 to +0.036)** | **+0.009 (−0.011 to +0.029)** |
| Last 5 + career | +0.014 (−0.007 to +0.039) | +0.002 (−0.006 to +0.011) | +0.006 (−0.012 to +0.024) | −0.019 (−0.046 to +0.012) |

Empty form in training: 3.0% of driver rows for every window except season so far (11.3%, the first race of every season). Median earlier starts in the window: 3, 5, 10, 6 (season so far), 41 (career).

## X6: rank against share of the leader's points

| Variant | Logistic regression | Random forest | Gradient boosting | Network |
|---|---|---|---|---|
| **Rank (current)**: PR-AUC | 0.706 | 0.725 | 0.715 | 0.741 |
| Share: change | +0.005 (−0.004 to +0.013) | +0.001 (−0.009 to +0.010) | −0.002 (−0.023 to +0.022) | −0.016 (−0.043 to +0.015) |
| Both: change | +0.007 (−0.002 to +0.015) | +0.001 (−0.009 to +0.012) | +0.005 (−0.008 to +0.018) | −0.027 (−0.051 to +0.002) |

In training, rank and share have a rank correlation of −0.924 for drivers and for teams. With the podium they score −0.403 against +0.396 (driver) and −0.390 against +0.396 (team). They carry the same information.

## X9: year or era

| Variant | Logistic regression | Random forest | Gradient boosting | Network |
|---|---|---|---|---|
| **(a) Base chance only (current)**: PR-AUC | 0.706 | 0.725 | 0.715 | 0.741 |
| (b) + era: change | −0.001 (−0.003 to +0.001) | −0.000 (−0.008 to +0.007) | +0.005 (−0.011 to +0.024) | −0.026 (−0.054 to +0.011) |
| (c) + year: change | −0.002 (−0.006 to +0.001) | −0.001 (−0.007 to +0.004) | −0.004 (−0.020 to +0.011) | **−0.041 (−0.067 to −0.003)** |

All test rows are in the 2022-24 era, which has no training rows, so an era column could never be used for them anyway.

## What I read from this

- **X6 and X9 are clear: keep the current features.**
  - **X6:** rank and share are almost the same information, and no change is beyond chance.
  - **X9:** era and year add nothing. The year even hurts the network beyond chance (−0.041).
- **X7 is the real question.** Career is the **highest window in all four models** (+0.009 to +0.033), and last 3 is the lowest. **But no career range excludes 0.** Also, the four models are scored on the same 39 races, so their agreement isn't four independent confirmations.

**Options for X7:**

| Option | For | Cost |
|---|---|---|
| **A. Keep last 5** | The rule we applied everywhere else (L8, L9, D2, X6, X9): don't change on a difference within chance. No rework. | Someone may ask: "career is higher in every model, why not use it?" The answer: within chance on 39 races, same rule as everywhere. Stated as a limitation. |
| B. Switch to career | Higher in all four models; consistent direction | Not beyond chance. About 30-40 minutes of rework: re-run L8, L10, D2, L9 on career form and update every number in those md sections and cells. The G1 concern (career mixes cars and seasons) is answered by the data. |
| C. Last 5 + career | Both views | Not better than career alone, and worse for the network |

**My recommendation is A**, for consistency: we've refused to change on within-chance differences everywhere else. B is defensible, though, and there's time for it (it's 15:30). If the team wants the higher-scoring window and accepts the rework, I'd do B, not C.

Which do you choose for X7? And do you confirm X6 = rank and X9 = (a)?

## X7: why keep last 5 when career scored higher

The honest answer is that it's a judgement call. Here's the reasoning, and one check that could settle it.

**1. "Higher" on 39 races isn't yet "better".** Take logistic regression: career is +0.033, but the 95% range runs from −0.014 to +0.070. That range is what we get by redrawing the 39 validation races many times. In a good share of those redraws, career comes out *worse* than last 5. The same holds for all four models: every range includes 0.

**2. We tried 6 windows and are looking at the best one.** Even if all six were equally good, one of them would come out on top by chance, and the winner of a contest usually looks better than it really is. That's why I asked for the rule before seeing the results.

**3. The four models agreeing is weaker evidence than it sounds.** They're all scored on the same 39 races. If those particular races happen to suit a long-run measure, all four models will show it at once.

**4. Consistency.** In L8, L9, D2, X6 and X9 we didn't change anything on a within-chance difference. Changing here would be the one exception, and it would need an explanation.

**The other side, fairly:** career is never worse than last 5 in any model. So switching isn't wrong, only not proven.

**A check that could settle it:** K1 used **rolling validation over 2018-21** as a check for X1. Each season is predicted by a model trained on all earlier seasons, which gives 81 races instead of 39 and a narrower range. Running career against last 5 that way takes about 2-3 minutes of compute and uses no test data.
- If career is ahead there too, beyond its range, that's real evidence for B.
- If not, A stands on firmer ground.

I'd recommend running that check before we decide.

## X6: what share and both are

**The share** is a driver's points after the previous race ÷ the points of the leader after the previous race. A made-up example: if the leader has 100 points and the driver has 50, the share is 0.50; the leader has 1.00; a driver with no points, 0. In the training rows the median share is 0.063 for drivers and 0.134 for teams, because most drivers are far behind the leader. The team share is the same with the constructors' table.

**Why it was a candidate (F5):** it keeps *how far* behind a driver is, which the rank doesn't. A driver ranked 2nd could be 1 point or 100 points behind. And it needs no invented value: a driver with no standings row has 0 points (F3), so share 0. The rank needs "last place = listed + 1" (L1).

**What we tested:** three versions of the standings group. The other 12 features and the two standings flags were the same in all three.

| Variant | Standings columns | Features |
|---|---|---|
| Rank (current) | `rank_before`, `team_rank_before` | 16 |
| Share | `share_before`, `team_share_before` (instead of the ranks) | 16 |
| Both | ranks + shares | 18 |

The share is empty in only 23 driver rows (the first race of 1950, no earlier standings) and 1,182 team rows (before 1958). Those get the training median for logistic regression and the network, as in L1.

**Result:** rank and share have a rank correlation of −0.924 (they order drivers almost identically), and no variant differs from rank beyond chance.

## X9: why the year hurts, and the point about the era

**The year.** The models train on 1950-2019 and validate on 2020-21. So **every validation year is beyond the largest year the model has ever seen.** The models handle that differently:
- **Trees** (forest, boosting) can only split on values they saw. For them, 2020 and 2021 are "the same as 2019". That's why the year does nothing for them (−0.001, −0.004).
- **Logistic regression and the network** use the year as a number on a scale. The network combines it with the other features in bends it learned only inside 1950-2019, and at 2020-21 it has to extrapolate those bends beyond their edge. That's where it goes wrong: **−0.041, range −0.067 to −0.003**, the only change in X9 beyond chance. Logistic regression gives the year a small straight-line weight, so it barely moves (−0.002).

**The era point.** The era columns are one 0/1 column per era, and each training row has exactly one of them set to 1.
- For **validation** (2020-21) that works, because its era (2014-21) has training rows from 2014-19. It just didn't help (within chance).
- For the **test** (2022-24) it breaks. That era has **no training rows**, so the test rows would have all 8 era columns at 0, a combination the model never saw in training. It can't learn anything about that era, and it might even react oddly to the all-zero pattern. So the era column can't help on the test by construction, whatever validation says.

So X9 says: keep only the base podium chance. The year risks extrapolation errors, and the era can't apply to the test era.

**What I suggest:** confirm X6 = rank and X9 = (a), and let me run the rolling-validation check for X7 before you choose between last 5 and career.



## The 95% range

**What it is.** A score measured on validation depends on *which* races happen to be in validation. We have 39 races (2020-21). With 39 other, similar races, the same model would score a bit differently. The 95% range shows **how much the score could move just because of which races we happened to get.**

**How it's computed** (the function `race_samples`, defined in cell 337):
1. Draw 39 races at random from the 39 validation races, **with replacement**: some races appear twice, some not at all. This makes a "new" validation season of similar races.
2. Compute the PR-AUC on that drawn set.
3. Repeat 1,000 times, which gives 1,000 PR-AUCs.
4. Sort them. The 25th smallest and the 25th largest bound the middle 95%. That's the range.

**A real example:** the baseline (logistic regression) scores **0.706, range 0.591 to 0.830** (L5). So with other 2020-21-like races it could plausibly have scored anywhere from about 0.59 to 0.83. The range is wide because 39 races is not many.

**For a difference between two models** (most of our tables): in each of the 1,000 draws, **both models get the same drawn races**, and we take the difference. Hard races are hard for both, so that luck cancels and the range of the difference is narrower than each model's own range. Example from X7 (logistic regression): career − last 5 = **+0.033, range −0.014 to +0.070**.
- **If the range includes 0** (as here), in some of the redraws the other variant wins. The data can't tell which is better.
- **If the whole range is on one side of 0**, the difference holds across the redraws. Example: the ablation, grid + qualifying removed: −0.088 (−0.139 to −0.045). That one is real.

**Why races and not single rows:** the rows of one race belong together. Every race has exactly 3 podiums, and a surprise result (a crash among the leaders) affects several drivers at once. Drawing single rows would pretend the 763 rows are independent and give ranges that look too precise.

## Why we use it

1. **Validation is small.** K1 measured this: the introduction's validation has 39 races and a range about 0.24 wide. So differences of about 0.02-0.03, the size of most of our differences, can't be separated from chance without it.
2. **It stops us choosing on luck.** Every decision (L8 tuning, L9 ablation, D2, X6, X7, X9) compares options that differ by a few hundredths. The range is what tells "better" apart from "higher this time".
3. **The evaluation will ask "is it really better?"** The brief wants every conclusion "backed by a plot, statistic, or controlled experiment". A score with its range answers that question with a number.

**What it doesn't cover:**
- **The randomness of the model itself** (the seed, L10): the network moved from 0.703 to 0.741 between seeds.
- **That the test seasons are a new era:** it only says how much 2020-21-like races vary.
- **95% is a convention:** it's the usual choice, not a value from our data.

This is also why the rolling-validation check for X7 helps: 81 races instead of 39 make the range narrower, so a real difference has a better chance of showing. Should I run it?



## K1: the season split (decided, recorded in the md)

**Decision:** the introduction's split.

| Set | Seasons | Rows | Races | Podiums |
|---|---|---|---|---|
| Training | 1950-2019 | 22,570 (podium rate 13.4%) | | |
| Validation | 2020-2021 | 763 | 39 | 117 (15.3%) |
| Test | 2022-2024 | 1,319 | 68 | 204 |

**Why** (from the md and cell 341):
1. **It's given by the introduction:** "train ≤ 2019, validation 2020–2021, test ≥ 2022". It's the same for every team and simple to explain.
2. **The test is a whole new era:** 2022-24 is the introduction's "ground-effect era", and no training or validation row comes from it. So the test asks whether the model still works after the rules changed.
3. **It's in time order:** every training row is earlier than every validation row, which is earlier than every test row, so nothing from the future is used. A random split by rows would put rows of the same race, and of later seasons, into training.
4. **The test is never used to choose anything.**

**The precision check that came with it** (cell 337: one validation block ending in 2021, logistic regression):

| Validation | Races | PR-AUC | 95% range width |
|---|---|---|---|
| 2014-2021 | 160 | 0.724 | 0.101 |
| 2018-2021 | 81 | 0.713 | 0.145 |
| **2020-2021 (introduction)** | **39** | 0.709 | **0.237** |

The PR-AUC barely changes with the validation size (0.709-0.734); only the width of the range does. Hence the rule in K1: **every validation score is given with its 95% range**, because with 39 races, differences of about 0.02-0.03 can't be separated from chance.

**Rolling validation over 2018-21** (fold k trains on all seasons before k and predicts season k; 81 races) **was tried as a check for X1**: it gave the same conclusion with narrower ranges. It wasn't adopted as the main validation because it's harder to explain and not the introduction's split.

**Rejected:**
- a larger validation block or rolling validation as the main one;
- percentage splits (e.g. 60/20/20 by seasons, which put 2021 into the test and mix two eras);
- a random split by rows (leaks races and later seasons).

**Limit:** 39 validation races.

**Why it matters for X7:** K1 already allows rolling validation as a check, as used for X1. Running X7 that way (last 5 against career, 81 races) stays within K1. It uses no test seasons and only adds evidence; the main validation stays 2020-21. Should I run it?




It helps with **one decision: X7, last 5 or career form.**

**The problem now:** on the 39 validation races, career scored higher than last 5 in all four models (+0.009 to +0.033), but every range crosses 0 (e.g. logistic regression −0.014 to +0.070). So the data we have can't tell us whether career is really better or got lucky on these 39 races.

**What the bigger mock adds:** 81 races (2018-21) instead of 39, each season predicted by a model trained only on the seasons before it. With twice the races, luck matters less and the ranges get narrower. So we get a clearer answer to the same question.

**The possible outcomes and what each means:**

| Outcome | What we do |
|---|---|
| Career ahead with its range above 0 in at least 2 models | Switch to career and redo L8, L10, D2, L9 (about 30-40 min). We can then say: "career was better on 81 races, beyond chance." |
| Career ahead but ranges still cross 0 | Keep last 5. We can say: "even on 81 races career isn't better beyond chance", which is a stronger answer to "why not career?" than 39 races. |
| Last 5 ahead | Keep last 5; the 2020-21 result was luck. |

**What it doesn't do:**
- It doesn't use the test seasons.
- It doesn't change anything in the notebook unless you decide to switch.
- It doesn't replace the main validation (2020-21, K1).

**Cost:** about 10-15 minutes in total, mostly re-running the notebook to rebuild the tables.

Without the check, we'd decide X7 by judgement alone: keep last 5 for consistency, or switch to career because it was higher. With it, either answer is backed by evidence. Should I run it?


The rolling check is done. Each season of 2018-21 was predicted by models trained only on the seasons before it: **81 races, 1,590 rows, 243 podiums.** The test seasons weren't used.

| Model | PR-AUC last 5 | PR-AUC career | Career − last 5 (95% range) | 2018 | 2019 | 2020 | 2021 |
|---|---|---|---|---|---|---|---|
| Logistic regression | 0.705 | 0.736 | **+0.030 (+0.009 to +0.056)** | 0.666 / 0.714 | 0.748 / 0.734 | 0.700 / 0.717 | 0.727 / 0.761 |
| Random forest | 0.721 | 0.742 | **+0.021 (+0.000 to +0.038)** | 0.695 / 0.725 | 0.764 / 0.758 | 0.686 / 0.716 | 0.774 / 0.782 |
| Gradient boosting | 0.726 | 0.750 | +0.023 (−0.000 to +0.043) | 0.711 / 0.723 | 0.786 / 0.791 | 0.684 / 0.707 | 0.759 / 0.765 |
| Network | 0.719 | 0.743 | **+0.024 (+0.001 to +0.046)** | 0.664 / 0.721 | 0.720 / 0.784 | 0.721 / 0.743 | 0.744 / 0.766 |

The season columns show last 5 / career.

**What this says:**
- **Career is better, now beyond chance in two models:** logistic regression (+0.009 to +0.056) and the network (+0.001 to +0.046). The forest and boosting ranges touch 0 at their low end (+0.000 and −0.000), which is borderline.
- **It's consistent:** career is higher in all four models overall, and in 14 of the 16 season-by-model results (only 2019 for logistic regression and the forest goes the other way).
- **The size matches the first run:** +0.021 to +0.030 here against +0.009 to +0.033 on 2020-21, so the 2020-21 result wasn't luck.

So the rule we discussed (range above 0 in at least 2 models) is met. **My recommendation is now to switch X7 to career**, and the evidence supports it.

**Switching changes everything downstream that used last 5** (L8 tuning, L10 seeds, D2, L9 ablation). Two ways to do it:

| Option | What | Cost |
|---|---|---|
| B1. Full redo | Move the X6/X7/X9 sections before L8 in the notebook, switch the form to career there, and re-run L8, L10, D2 and L9 on career | Most consistent: every choice is made on the final features. About 1-1.5 h, because all the numbers in those cells and md sections change and must be rewritten. This machine is slow at the moment. |
| **B2. Switch after the experiments** | Keep L8-L9 as run (on last 5). After X7, one cell switches to career, and **the ablation (L9) is re-run on career**. Everything after (final comparison, L4 experiments, explanations, prediction function) uses career, with the L8 settings. | About 30 min. Limit to state: the settings (L8), seed check (L10) and D2 were chosen on last 5. L8's tuning changed scores by only +0.001 to +0.003 for the three statistical models, and D2 found no fix helping, so those choices are unlikely to differ with career. |

**I recommend B2**, given the time (17:00) and what's still left: final comparison, L4 experiments, explanations, prediction function, EDA after cleaning, Run-All, report and Kaggle.

Do you choose career with B2? And do you confirm X6 = rank and X9 = (a)?