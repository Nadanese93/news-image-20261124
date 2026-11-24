# The World — 24 November 2026

[![bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Nadanese93/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Nadanese93/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A newspaper front page that sums up the world news of **Tuesday, 24 November 2026** in one image. The program draws the whole 1024×1024 page with Python 3.13 standard library only — its own PNG encoder, its own 5×7 bitmap font, and all artwork drawn programmatically with shapes. No network, no external fonts or images, fully deterministic (two runs write byte-identical files).

## The stories

1. **Ukraine sinks Russian warship off Libya** — Ukrainian sea drones sank the corvette *Merkury* and hit the cargo ship *MV Angara* off Benghazi; a Ka-27 helicopter was destroyed too. Sources: CNN, The Wall Street Journal, Reuters, AP.
2. **COP31 collapses** — climate talks in Antalya, Turkey ended with no fossil-fuel language, the first summit breakdown since COP15 in 2009. Sources: BBC, CNN.
3. **24 dead in factory fire** — blaze at the PT Fonusa Agung Mulia candy factory in Cikande, Banten, Indonesia; about 30 still missing. Source: Reuters.
4. **Gaza a toxic wasteland** — an Oxfam / CEOBS report finds contamination indicators across 99% of Gaza. Sources: Oxfam, CNN.
5. **Chess crown on the line** — World Chess Championship 2026 begins in Geneva: defending champion Gukesh Dommaraju vs challenger Javokhir Sindarov, Game 1 today. Sources: Chess.com, FIDE.
6. **Hit Russian ship reaches port** — the cargo ship *Sparta II*, struck by drones in the Gulf of Finland, arrives in St Petersburg under tow. Source: Reuters.

Stories 1–4 and 6 were first reported on 22–23 November but are the lead stories of the 24 November news cycle; story 5 genuinely begins on 24 November.

## How to run

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024×1024, under 1 MiB).
