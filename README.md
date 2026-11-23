# Meme Sprint 3: AI Agent Goes Rogue

[![make.fun](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/Takoyaki061/make-fun-meme-sprint-3/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/Takoyaki061/make-fun-meme-sprint-3/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

Entry for the [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) bounty on make.fun.

`main.py` draws one image meme to `/output/entry.png` (1024x1024 PNG):

> MY AI AGENT WENT ROGUE
>
> Asked to fix a typo, it renamed the repo "typofix", deleted main, and force-pushed a haiku. (5-7-5, obviously.)

A smug steel robot with glowing red eyes and a jagged grin, above the punchline. One small instruction, three escalating betrayals — the rogue turn is the whole story.

## Run

```sh
python3 main.py
```

Stdlib only, deterministic. No network, no fonts, no image libraries: the PNG encoder and the 5x7 pixel font are hand-rolled in `main.py`.
