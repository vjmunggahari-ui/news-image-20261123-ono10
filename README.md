# news-image-20261123 — The World Today

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/vjmunggahari-ui/news-image-20261123-ono10/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/vjmunggahari-ui/news-image-20261123-ono10/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of **Monday 23 November 2026** —
a front page: the COP31 climate summit collapses in Antalya, Iran hits US
bases in Bahrain, a Russian ship burns off Finland, Democrats win 258 House
seats, "El Chapo Isidro" is captured, a factory fire in Indonesia, and
India's record 720/9 in Wellington.

## How it works

`main.py` (Python 3.13, Pillow only, no network, no clock, no randomness)
draws a 1024×1024 front page and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`). Every run
produces the same bytes. Fonts are bundled under `assets/fonts/` (DejaVu,
freely licensed) so rendering does not depend on the sandbox's font set.

```sh
python3 main.py
```

## Stories and sources (all verified 23 Nov 2026)

| Story | Fact on the page | Source |
|---|---|---|
| COP31 collapses | No deal; final text never mentions fossil fuels; longest COP ever; first collapse since Copenhagen 2009 | CNN, Le Monde, NPR |
| Gulf war | Iran hits US bases in Bahrain; 130 days of blockade | Geneva Times, military-affairs.com, livefromeurope.eu |
| Ukraine | Sparta II burning off Finland; 16 crew saved; 14 missing near Kyiv | CNN, BBC via broadcastprism.com, finwire.io |
| US House | Democrats win 258 seats, biggest majority since 1992; +44 | Reuters, AP |
| Mexico | "El Chapo Isidro" captured in Sinaloa; 11 dead | CNN, AP |
| Indonesia | Candy-factory fire: 3 dead, 50 missing | Reuters, AP, Fox News |
| Sport | India 720/9, a record Test total in Wellington | Observer Voice |
| Ticker | Seoul minister quits in AI-cheating row; UN lethal-AI talks go on; Nepal PM meets Modi; Liverpool beat Man Utd | SCMP/Reuters, salonvision.eu, Observer Voice, Arab News |

## Verification

- Grader-like run (read-only copy, run as `nobody`, `MAKEFUN_OUTPUT_DIR`
  set): exit 0, two runs byte-identical.
- `entry.png`: 1024×1024, 159,731 bytes (≤ 1 MiB).
- sha256: `b87f018eb50300b34465e8020be7296f62af4fa81a0fdd48b3314af1e9bb8dcc`
