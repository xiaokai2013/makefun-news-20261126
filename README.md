# The World — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/xiaokai2013/makefun-news-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/xiaokai2013/makefun-news-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-image front page summing up Thursday 26 November 2026's world news,
built for the make.fun `news-image-20261126` bounty.

## The day, in seven stories

1. **Russia hits Kyiv mall in overnight barrage** — missiles and 113 drones
   hit 20 sites; two die in Kharkiv. Kyiv says its drone killed five in
   occupied Zaporizhia.
2. **Tanker fire kills 31 on Cairo ring road** — fuel lorry overturns in
   Giza; 21 hurt, cars charred. Toll confirmed Thursday.
3. **UK writes to 100,000 veterans** — first such letters since the Cold
   War. Ministers stress: no mobilisation.
4. **Kim vows wider tactical nuclear arsenal** — KCNA photos show
   centrifuges; Kim calls nuclear status "irreversible".
5. **Houthis claim Jeddah, Jazan port strikes** — coalition says eight
   drones downed; Ras Tanura also named in claim.
6. **World hits back at US tariff plan** — Democrats slam 25% duties on 14
   economies; Brazil and Singapore push back.
7. **Iraq jails eight Frenchmen for life over IS** — court sentences the
   men for joining Islamic State in Syria.

## How it is built

- `render.py` draws the front page ("WireFront" layout: serif nameplate,
  dark lead banner with a drawn blast motif, a 2×3 grid of dispatches with
  drawn icons) from `news.json` with Pillow, and writes `entry.png`
  (1024×1024, deterministic — two runs produce identical bytes).
- `main.py` is the entrypoint the grader runs: standard library only, it
  copies the shipped `entry.png` to `/output/entry.png` (the grading
  sandbox has no Pillow and no fonts).

## Run it

```sh
python3 render.py        # regenerate entry.png
python3 -P -s main.py    # grader-style: writes /output/entry.png
```

Sources: Al Jazeera, Reuters, AP, AFP, The Telegraph, Yonhap, KCNA,
Xinhua, SCMP.
