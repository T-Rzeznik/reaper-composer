#!/usr/bin/env python3
"""
generate_stem.py — local, $0-per-clip music stem generation for reaper-composer.

Generates a single instrument/texture audio clip from a text prompt using Meta's
MusicGen (small) via Hugging Face transformers, and writes a mono WAV to disk.
The agent then drops that WAV on the Reaper timeline with reaper_insert_media.

Runs on CPU (slow but free) or a CUDA GPU if available. The first run downloads
the model (~1.2 GB for musicgen-small) into the Hugging Face cache.

Dependencies (one-time):
    pip install "transformers>=4.40" torch scipy

Usage:
    python generate_stem.py --prompt "warm analog pad, deep house, no drums" \
        --duration 8 --out C:/Users/me/.reaper-composer/stems/proj/pad.wav

    # --bpm / --key are optional conveniences appended to the prompt text:
    python generate_stem.py --prompt "deep rolling sub bass, dry, no drums" \
        --bpm 124 --key "F minor" --duration 8 --out bass.wav

On success the ONLY stdout line is the final output path (for the caller to
capture); all progress/diagnostics go to stderr.
"""
import argparse
import os
import sys


def eprint(*a):
    print(*a, file=sys.stderr, flush=True)


def main():
    p = argparse.ArgumentParser(description="Generate a music stem with local MusicGen.")
    p.add_argument("--prompt", required=True, help="Text description of the stem.")
    p.add_argument("--out", required=True, help="Output .wav path (absolute preferred).")
    p.add_argument("--duration", type=float, default=8.0,
                   help="Approx length in seconds (default 8).")
    p.add_argument("--bpm", type=float, default=None, help="Optional; appended to the prompt.")
    p.add_argument("--key", type=str, default=None, help="Optional; appended to the prompt.")
    p.add_argument("--model", default="facebook/musicgen-small", help="Hugging Face model id.")
    p.add_argument("--guidance", type=float, default=3.0,
                   help="Classifier-free guidance scale (default 3.0).")
    p.add_argument("--seed", type=int, default=None,
                   help="Optional seed for reproducible / varied retries.")
    args = p.parse_args()

    try:
        import numpy as np
        import torch
        from scipy.io import wavfile
        from transformers import AutoProcessor, MusicgenForConditionalGeneration
    except ImportError as e:
        eprint(f"ERROR: missing dependency: {e}")
        eprint("Install the stem-generation deps with:")
        eprint('  pip install "transformers>=4.40" torch scipy')
        eprint("(CPU works but is slow; a CUDA GPU is much faster. "
               "First run downloads ~1.2 GB.)")
        sys.exit(2)

    # Fold optional bpm/key into the prompt so the agent can pass them as flags.
    prompt = args.prompt
    extras = []
    if args.bpm:
        extras.append(f"{int(args.bpm)} BPM")
    if args.key:
        extras.append(f"in the key of {args.key}")
    if extras:
        prompt = f"{prompt}, {', '.join(extras)}"

    device = "cuda" if torch.cuda.is_available() else "cpu"
    eprint(f"[stem] device={device} model={args.model}")
    eprint(f"[stem] prompt: {prompt}")

    if args.seed is not None:
        torch.manual_seed(args.seed)

    processor = AutoProcessor.from_pretrained(args.model)
    model = MusicgenForConditionalGeneration.from_pretrained(args.model).to(device)

    sr = model.config.audio_encoder.sampling_rate  # 32000 Hz for musicgen
    # MusicGen emits ~50 audio frames (tokens) per second of output.
    max_new_tokens = int(args.duration * 50) + 4

    inputs = processor(text=[prompt], padding=True, return_tensors="pt").to(device)

    eprint(f"[stem] generating ~{args.duration:.1f}s ({max_new_tokens} tokens)... "
           "this can take 1-3 min per clip on CPU.")
    with torch.no_grad():
        audio = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            guidance_scale=args.guidance,
        )

    # Shape: (batch, channels, samples) -> take first item, first channel (mono).
    wav = audio[0, 0].cpu().numpy().astype("float32")

    # Light peak-normalize to avoid clipping, then to 16-bit PCM.
    peak = float(np.max(np.abs(wav))) or 1.0
    wav = wav / peak * 0.97
    pcm = (wav * 32767.0).astype(np.int16)

    out = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wavfile.write(out, sr, pcm)

    eprint(f"[stem] wrote {out} ({len(pcm) / sr:.1f}s @ {sr} Hz)")
    # The single stdout line: the final path, for the caller to capture.
    print(out)


if __name__ == "__main__":
    main()
