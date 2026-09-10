# Titan Protocol

A typing adventure for kids. Four storylines, seventeen stages, sixty-eight
story chapters and a boss fight against a Titan at the end of every stage.

Single file, no build step, no dependencies. Open `index.html` and play.

## Design rules

The game is built for a young learner who needs accuracy-first practice
rather than speed drills. These are deliberate and worth keeping:

- **No timers anywhere.** No countdown, no words-per-minute readout, no
  "beat your best time". Progress bars count words, never seconds.
- **Accuracy is the only score the player sees.** Speed is tracked, but it
  is shown only in the grown-up panel inside Settings.
- **Backspace is disabled.** A wrong key does nothing at all — no buzzer,
  no lost life. Find the right key and carry on. This avoids rehearsing
  the wrong finger movement.
- **Real words only.** Never `fff jjj fjf`. Every word list is
  key-constrained: a word may only use keys taught in that stage or earlier.
  Verify this before adding any word.
- **The frame stays fixed, the rewards vary.** Layout, colours and sounds
  are identical session to session; all novelty lives in the story chapters
  and the Titan dossiers.
- **Every sensory channel is switchable** — art, animation, sound effects,
  music, speech, contrast and text size — so the game can be turned down on
  a difficult day without losing progress.
- **Weakest keys are silently over-sampled** in the next word lists. The
  player is never told which they are.

## Structure

Everything is in `index.html`:

- `RIG` / `SCENES` — the animated SVG Titans and backdrops, drawn in code.
- `TITANS` — the sixteen Titans and their dossier text.
- `CONTENT` — the four storylines. Each level carries its word list and the
  story chapter unlocked by finishing it. This is the block to edit.
- `MOVES` / `FINISHER` — battle strike names and the charged finisher.
- `MUSIC` — soundtrack loader and the fallback generated score.
- `TUTORIAL` — the spotlight walkthrough on the front page.

Progress is stored in `localStorage`, so it is per-browser and per-origin.

## Players

Several people can share one browser. Each player has their own progress,
dossiers, story chapters **and settings** — sensory preferences differ from
child to child, so text size, contrast, animation and sound are all saved
per player rather than globally.

- On first run a player named Nolan is created and the game opens straight
  into the map. With one player there is no picker to get past.
- With two or more players the game asks who is playing on every load.
- Players are added, renamed and deleted from the Players screen, and each
  picks a Titan as their avatar.

Storage keys: `titan-protocol-players` holds the roster, and each player's
save lives at `titan-protocol-save-<id>`. A pre-profiles save under
`titan-protocol-v2` is migrated into the first player automatically.

## Music

The game looks for four files and uses them if present:

```
music/explore.mp3    map, storylines, exercises
music/battle.mp3     boss fights
music/story.mp3      story chapters
music/victory.mp3    the chapter after beating a Titan
```

If any are missing or cannot be decoded, it generates its own score in the
browser instead. Swap which track plays where by renaming the files.

Tracks included here are **Descent**, **Song of the Forge**, **Dragon's
Lullaby** and **Simulacra** by [Scott Buckley](https://www.scottbuckley.com.au),
used under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
See `music/CREDITS.txt`.

## Deploying

Static site — no configuration needed. On Vercel, import the repository and
deploy; `index.html` is served at the root and `music/` alongside it.

Use the stable production URL rather than a per-deployment preview URL:
progress lives in `localStorage`, which is scoped to the origin, so playing
on a preview URL means losing it on the next deploy.

## Notice

A non-commercial fan project. Godzilla, King Kong and the other Titans are
the property of Toho Co., Ltd. and Legendary Entertainment. This project is
not affiliated with, authorised by, or endorsed by either.
