#!/usr/bin/env python3
"""Synthesize ccm's notification chimes (soft, short, quiet) into sounds/*.wav."""
import math, struct, wave
from pathlib import Path

RATE = 44100
OUT = Path(__file__).resolve().parent.parent / "sounds"


def note(freq, start, dur=0.55, vol=0.22):
    """A soft music-box / marimba-ish tone: sine + a touch of octave, gentle attack, long smooth decay."""
    return (freq, start, dur, vol)


def render(notes, length):
    n = int(RATE * length)
    buf = [0.0] * n
    for freq, start, dur, vol in notes:
        s0 = int(start * RATE)
        for i in range(int(dur * RATE)):
            if s0 + i >= n:
                break
            t = i / RATE
            env = min(1.0, t / 0.012) * math.exp(-t * 7.0)       # 12 ms fade-in, soft exponential tail
            tone = math.sin(2 * math.pi * freq * t) + 0.18 * math.sin(4 * math.pi * freq * t)
            buf[s0 + i] += vol * env * tone
    fade = int(0.03 * RATE)                                       # no click at the end
    for i in range(fade):
        buf[n - fade + i] *= 1 - i / fade
    return buf


# Bluetooth headphones swallow the first 1-2+ s of audio while they wake up, so each chime starts with
# 2.5 s of digital silence: Windows opens the audio stream for it, which wakes them before the blip.
# (Faint noise here was audible as a hiss over Bluetooth.)
LEAD_IN = 2.5


def save(name, buf):
    buf = [0.0] * int(LEAD_IN * RATE) + buf
    OUT.mkdir(exist_ok=True)
    with wave.open(str(OUT / name), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(RATE)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32767)) for x in buf))


def blip(f0, f1, start, dur=0.13, vol=0.28):
    """A round water-drop 'blip': pitch glides up from f0 to f1, quick soft attack, fast decay."""
    return ("blip", f0, f1, start, dur, vol)


def render_blips(blips, length):
    n = int(RATE * length)
    buf = [0.0] * n
    for _, f0, f1, start, dur, vol in blips:
        s0, phase = int(start * RATE), 0.0
        for i in range(int(dur * RATE)):
            if s0 + i >= n:
                break
            t = i / RATE
            freq = f0 * (f1 / f0) ** min(1.0, t / (dur * 0.6))   # bubbly upward glide
            phase += 2 * math.pi * freq / RATE
            env = min(1.0, t / 0.004) * math.exp(-t * 26.0)
            buf[s0 + i] += vol * env * (math.sin(phase) + 0.08 * math.sin(2 * phase))
    fade = int(0.02 * RATE)
    for i in range(fade):
        buf[n - fade + i] *= 1 - i / fade
    return buf


# done: "bloop-blip!" — two drops, the second higher
save("done.wav", render_blips([blip(420, 760, 0.0), blip(620, 1150, 0.12)], 0.4))
# input: "blip-blip-blip?" — three quick drops, a little softer, ending up like a question
save("input.wav", render_blips([blip(520, 900, 0.0, vol=0.22), blip(520, 900, 0.11, vol=0.22),
                                blip(700, 1300, 0.22, vol=0.24)], 0.5))
print("wrote", *sorted(p.name for p in OUT.glob("*.wav")))
