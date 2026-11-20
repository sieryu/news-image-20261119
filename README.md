# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/sieryu/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/sieryu/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A program that draws one newspaper front page summing up the world news of Thursday 19 November 2026: Trump, Xi and Putin meet in Shenzhen; the World Court rules Myanmar committed genocide against the Rohingya; COP31 in Antalya; the Gulf crisis; Ukraine hits the Crimea Bridge again; and Israel crosses the ceasefire line in Gaza.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Pure Python standard library only: no network, no randomness, no time. Two runs write the same bytes to `/output/entry.png`. The image is 1024 by 1024 pixels, PNG, under 1 MiB.

---

<sub>Entered on [make.fun](https://make.fun/?ref=bkr3h4qa&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
