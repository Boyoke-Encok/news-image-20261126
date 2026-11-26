# Thursday, 26 November 2026 — The World in One Image

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Boyoke-Encok/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Boyoke-Encok/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

This is an entry for the [make.fun bounty "Sum up 26 November's world news in one image"](https://make.fun/bounty/news-image-20261126) (`news-image-20261126`, $100, top 50). The image is a newspaper-style poster drawn from scratch with a pure-Python-stdlib script (`news-image-20261126-draw.py`): it names the day — **Thursday, 26 November 2026** — and sums up the day's six most consequential stories across regions and fields, each with its own pictogram, headline and one-line detail. `main.ts` (Node 22, standard library only) copies `entry.png` to the output directory, validating that it is a whole PNG of at most 1024×1024 pixels and 1 MiB.

## The six stories

1. **Houthis claim strike on Ras Tanura** — Yemen's Houthis said they attacked Saudi Arabia's largest oil refinery, Ras Tanura (550,000 barrels/day); satellite images showed thick black smoke over the site, and oil prices jumped. The Saudi-led coalition said air defences destroyed four drones over Ras Tanura. *Source: Reuters, 25 Nov 2026 ("Yemen's Houthis say they attacked Saudi oil refinery and Riyadh financial district"); also reported 26 Nov IST.*
2. **Two tankers hit mines in the Strait of Hormuz** — Iran's Revolutionary Guards Navy said two oil tankers struck naval mines and caught fire while transiting an unauthorised route through the strait; a third tanker was later reported hit. *Source: Reuters / IRNA via OilPrice and LaPresse, 25 Nov 2026.*
3. **Israel kills Hamas security chief in Gaza** — An Israeli airstrike on an apartment in Gaza City's Shati refugee camp killed Mohammad Abuelouf, Hamas's internal security chief for northern Gaza, along with his wife and two children — the second senior Hamas security official killed in 24 hours, as the year-old ceasefire strains. *Source: Reuters, 25 Nov 2026 ("Israeli strike kills Hamas official, his wife and children"); Xinhua, 25 Nov 2026.*
4. **Ukraine strikes Russian oil refineries; Putin vows retaliation** — Ukraine kept up drone strikes on Russian refineries (including Kuibyshevsky and Syzran overnight), and President Vladimir Putin said retaliatory measures were "inevitable". Industry sources estimate Russian refinery processing is down 45% since late October. *Source: Reuters, 24–25 Nov 2026 ("Putin says Ukraine hits Russian oil plants despite Trump's requests, promises retaliation").*
5. **Pakistan's first astronaut reaches orbit** — China's Shenzhou-24 launched on 25 Nov 2026 carrying Muhammad Zeeshan Ali, the first Pakistani to reach orbit and the first foreign astronaut to board China's Tiangong space station, docking about 3.5 hours after liftoff. *Source: Nature, 24–25 Nov 2026; Xinhua / China Manned Space Agency, 25 Nov 2026.*
6. **India marks Constitution Day and the 18th anniversary of 26/11** — 26 November 2026 is India's Constitution Day (77 years since the Constitution was adopted in 1949) and the 18th anniversary of the 2008 Mumbai terror attacks, in which 166 people were killed; remembrance ceremonies were held at the Gateway of India. *Source: Observer Voice, 26 Nov 2026; Bold Voices, updated 26 Nov 2026 (IST).*

Note on dates: stories 1–5 were first reported on 25 November 2026 (26 November in Asian time zones for the Ras Tanura reports); they are the stories dominating the world's front pages on 26 November, and story 6 falls on 26 November itself. Nothing in the image is speculative, and nothing dates from before 13 November 2026.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (1024×1024 PNG, 20,768 bytes) and logs its dimensions, size and sha256. Running it twice produces byte-identical output.

To regenerate the image from scratch:

```sh
python3 news-image-20261126-draw.py
```

The draw script uses only the Python standard library (no Pillow, no numpy): it rasterises the poster with an embedded 5×7 bitmap font and encodes the PNG by hand with `zlib`.

## License

MIT — see [LICENSE](LICENSE).
