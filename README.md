# news-image-20261126 — Sum up 26 November's world news in one image

make.fun bounty: **news-image-20261126**, $100, free entry
Bounty page: https://make.fun/bounty/news-image-20261126
Opens: **2026-11-26 00:00 UTC (08:00 Beijing)** · Deadline: **2026-11-28 08:00 Beijing** (2026-11-28 00:00 UTC)
Account: @fuyi-zhu — **built only, NOT submitted**
Reward split: 50 places share $100 — 1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20.
Submissions at scan time (2026-11-25 22:25 UTC): **0**.

## What it does

`main.py` (Python 3, Pillow only, no network) draws a single editorial
infographic, 1600×1280 PNG, and writes it to `/output/entry.png`.

Layout: same proven format as yesterday's news-image-20261125 entry
(which passed all stage checks on resubmission) — dark-navy background,
gold header "THE WORLD IN ONE IMAGE — 26 NOVEMBER 2026 — THURSDAY",
then a 3×2 grid of six labelled panels, each with a drawn icon,
a kicker, a large headline and one short caption. Footer lists the
six topics. No tiny text — headlines are 36pt bold, captions 26pt.
Two new icons added for today: `chart` (falling bars) and `shield`.

## Stories chosen (6) — all dated 26 November 2026 in the sources

1. **Strait of Hormuz** — US tells citizens to leave Iran now;
   Houthi strikes spread (Ras Tanura refinery hit).
2. **Trade war** — Trump administration proposes new tariffs on
   14 trading partners, incl. EU, India, China.
3. **Markets** — Asia stocks tumble (KOSPI −6.2%, Nikkei −2.8%);
   Dow closes above 50,000 for the first time.
4. **Colombia** — Troops storm an Éxito supermarket in Cartagena,
   free all remaining hostages; one captor killed.
5. **Hong Kong** — Fire engulfs residential towers in Tai Po,
   14 dead including a firefighter.
6. **Space / Mercury** — Joint Europe–Japan (ESA/JAXA) probe
   reaches Mercury after an eight-year journey.

Sources checked 2026-11-25 ~22:46 UTC: make.fun bounty page (brief +
reward split), Manila Times world page (26 Nov datelines), Libre News
26 Nov edition, Times Now live blog, 8to5 evening briefing 25 Nov,
DailyFoxNews early edition 25 Nov. Nothing was invented — every
panel is a story reported in those sources.

## Run it / verify it

```bash
cd ~/workspace/goals/make-fun/entries/news-image-20261126
python3 main.py                 # writes /output/entry.png
python3 main.py --out entry.png  # local preview copy
```

Verified 2026-11-25 ~22:47 UTC: both commands run clean; output is a
valid PNG, 1600×1280, RGB, ~152 KB (under the 1 MiB limit); two runs
produce identical bytes (md5 f476899e5272c06bbdf88bb831bb4ec0), so the
brief's "runs twice, same bytes" requirement holds. Preview copy is
in this folder as `entry.png`.

Requirements: Python 3.11+ and Pillow (`pip install pillow`).
Fonts: DejaVu Sans from `/usr/share/fonts/truetype/dejavu/`.

## Still missing before submission — DO NOT SUBMIT YET

1. **User picks the bounty first.** The 06:25 scan message already
   recommended this one (0 submissions, pipeline proven); the user
   has not replied yet. Do not submit until they confirm.
2. **GitHub repo + transcript bundle:** needs a new public repo
   owned by linked GitHub 16778738 (e.g. makefun-news-image-20261126),
   the official kit downloaded via the make.fun API, and the
   transcript bundle built with the kit CLI — same flow as the
   20261125 round-2 resubmission that passed all checks.
3. **Submission itself:** not done on purpose — no kit downloaded,
   no CLI run, no API key used, nothing pushed to GitHub.
4. **Timing note:** built at ~06:50 Beijing on 26 Nov, just before
   the bounty opens (08:00 Beijing). The day's news may still
   develop; the entry can be revised and resubmitted — last
   submission before the deadline counts, up to 10/day.
5. **Wallet is ready this time:** payout wallet
   Eb6bJckvu3Bm6a4aLXJ2i4ub3rQnngYza71h2m7VNnZm is already bound
   to @fuyi-zhu (unlike yesterday's first attempt).

## Files

- `main.py` — the program (the entry)
- `entry.png` — generated preview
- `README.md` — this file
