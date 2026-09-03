"""Musique de fond — synthétisée ici même, donc libre de droits.
Un tapis d'accords doux, quelques notes de cloche par-dessus, une réverbération
courte. Rien d'agressif : c'est un fond, pas une chanson."""
import numpy as np
from scipy.signal import fftconvolve
from scipy.io import wavfile

SR = 44100


def note(f, t0, dur, amp, harmoniques=(1, 0.42, 0.16, 0.06), attaque=0.9, chute=None, n=None):
    """Une voix douce : attaque lente, extinction exponentielle, harmoniques faibles."""
    chute = chute if chute is not None else dur
    i0 = int(t0 * SR)
    L = int(dur * SR)
    t = np.arange(L) / SR
    env = (1 - np.exp(-t / attaque)) * np.exp(-t / chute)
    sig = np.zeros(L)
    for k, a in enumerate(harmoniques, start=1):
        detune = 1 + (k - 1) * 0.0006
        sig += a * np.sin(2 * np.pi * f * k * detune * t + k * 0.7)
    sig *= env * amp
    n[i0:i0 + L] += sig[: max(0, len(n) - i0)]


def cloche(f, t0, dur, amp, n):
    i0 = int(t0 * SR)
    L = int(dur * SR)
    t = np.arange(L) / SR
    env = np.exp(-t / (dur * 0.32))
    sig = (np.sin(2 * np.pi * f * t)
           + 0.35 * np.sin(2 * np.pi * f * 2.01 * t)
           + 0.12 * np.sin(2 * np.pi * f * 3.02 * t))
    sig *= env * amp
    n[i0:i0 + L] += sig[: max(0, len(n) - i0)]


def reverb(x, duree=1.6, melange=0.3):
    L = int(duree * SR)
    t = np.arange(L) / SR
    ir = np.random.default_rng(7).normal(0, 1, L) * np.exp(-t * 4.2)
    ir[0] = 1.0
    ir /= np.abs(ir).sum() / 2
    hum = fftconvolve(x, ir)[: len(x)]
    return (1 - melange) * x + melange * hum


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def piste(duree=17.0):
    n = np.zeros(int(duree * SR))

    # Ré majeur, quatre accords très lents : Dmaj7 – Bm7 – Gmaj7 – Asus
    accords = [
        (0.0, [50, 57, 61, 64, 69]),    # D  F# A C#
        (4.0, [47, 54, 59, 62, 66]),    # B  D  F# A
        (8.0, [43, 50, 55, 59, 62]),    # G  B  D  F#
        (12.0, [45, 52, 57, 59, 64]),   # A  E  G  B
    ]
    for t0, notes in accords:
        for j, m in enumerate(notes):
            note(midi(m), t0, 5.6, 0.15 if j else 0.19, attaque=1.1, chute=3.4, n=n)

    # quelques cloches, sur la pentatonique, jamais deux en même temps
    melodie = [
        (1.4, 78), (2.9, 81), (5.2, 76), (6.6, 78),
        (9.1, 74), (10.4, 81), (12.8, 78), (14.4, 73),
    ]
    for t0, m in melodie:
        cloche(midi(m), t0, 2.6, 0.085, n)

    # basse discrète
    for t0, m in [(0.0, 38), (4.0, 35), (8.0, 31), (12.0, 33)]:
        note(midi(m), t0, 4.4, 0.13, harmoniques=(1, 0.2, 0.05), attaque=0.6, chute=2.6, n=n)

    n = reverb(n)

    # fondu d'entrée et de sortie
    fi, fo = int(1.4 * SR), int(2.6 * SR)
    n[:fi] *= np.linspace(0, 1, fi) ** 1.6
    n[-fo:] *= np.linspace(1, 0, fo) ** 1.4

    n /= np.max(np.abs(n)) + 1e-9
    n *= 0.62

    # léger élargissement stéréo
    d = int(0.012 * SR)
    g = n.copy()
    dr = np.concatenate([np.zeros(d), n[:-d]]) * 0.94
    st = np.stack([g, dr], axis=1)
    return (st * 32767).astype(np.int16)


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).parent / "out"
    out.mkdir(exist_ok=True)
    wavfile.write(out / "musique.wav", SR, piste())
    print("musique.wav écrit")
