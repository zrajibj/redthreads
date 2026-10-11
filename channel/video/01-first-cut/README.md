# Video 1 first cut (animatic)

This is a machine-made first cut of video 1, made to review the pacing and visuals before a human voice and animator take over.

- The narration is synthetic: Kokoro TTS, voice `am_michael`, speed 0.94. `tts.py` reads section 1 of `../../scripts/01-why-changing-the-government-changes-so-little.md` and writes `vo.wav` and `timing.json`.
- The animation is drawn frame by frame with pycairo (`lib.py`, `building.py`, `scenes.py`). `render.py N 4` renders a quarter of the frames to `partN.mp4` at 1920x1080 and 30 fps.
- `music.py` writes a quiet synth pad and arpeggio bed with an end sting.

The finished file (4:46, including the 20-second end screen) is not kept in git. It is stored in the project files as `video/red-threads-video-1-first-cut.mp4`.
