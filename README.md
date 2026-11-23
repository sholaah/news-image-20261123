# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sholaah/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sholaah/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

A program that renders Monday 23 November 2026's world news as one Economist-style cover image: a cream page, a red "THE WORLD TODAY" masthead, the date as a huge title, and a drawn scene of the empty COP31 conference hall under a cracked globe for the lead story — the climate summit collapsing with no deal on fossil fuels — with two secondary stories below it (oil tankers struck and burning in the Strait of Hormuz; Russian cruise missiles landing in Poland as NATO meets) and the Ukrainian drone strike on a Russian warship in Libya in the footer. The image is pre-rendered with Pillow by build_image.py and copied to the output directory by main.py, so the entrypoint is deterministic and needs no network.

## Run it

```sh
python3 build_image.py && MAKEFUN_OUTPUT_DIR=./output python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=s0dzaxys&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
