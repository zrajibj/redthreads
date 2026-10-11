# Red Threads logo

Round 1 concepts. Set in **Anton** (SIL Open Font License) as a stand-in until the
Condensed Negation font file is available; rerun the build with that font to swap it.

- `wordmark-*`: one line, thread woven through THREADS
- `stacked-*`: RED over THREADS, thread between the lines
- `icon-rt-*`, `icon-r-*`: 1080x1080 profile icons, safe inside a circle crop
- `*-transparent`: no background, for overlays

Palette: red `#C8102E`, cream `#F2E8D5`, ink `#1E1E24`.

## Rebuild

```
python3 -m pip install fonttools cairosvg
python3 src/build_logo.py --font path/to/CondensedNegation.ttf
```

SVGs have the text converted to outlines, so they don't need the font installed.
