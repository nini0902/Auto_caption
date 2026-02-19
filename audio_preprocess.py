#音檔轉字幕
import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("video", help="Path to a video file")
    p.add_argument("--out_dir", default="out_audio", help="Output directory")
    p.add_argument("--sr", type=int, default=16000, help="Sample rate (Hz)")
    p.add_argument("--mono", action="store_true", help="Force mono channel")
    args = p.parse_args()

    video_path = Path(args.video).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = video_path.stem
    raw_wav = out_dir / f"{stem}_raw.wav"
    clean_wav = out_dir / f"{stem}_clean.wav"

    # 1) Extract raw audio (WAV)
    cmd_extract = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
    ]
    if args.mono:
        cmd_extract += ["-ac", "1"]
    cmd_extract += [
        "-ar",
        str(args.sr),
        "-c:a",
        "pcm_s16le",
        str(raw_wav),
    ]
    run(cmd_extract)

    # 2) Audio pre-processing (simple but effective):
    #    - highpass: remove low-frequency rumble
    #    - lowpass : remove high-frequency hiss
    #    - loudnorm: normalize loudness
    audio_filter = (
        "highpass=f=80,"
        "lowpass=f=8000,"
        "dynaudnorm=f=150:g=25:m=10:p=0.98"
    )

    cmd_clean = [
        "ffmpeg",
        "-y",
        "-i",
        str(raw_wav),
        "-af",
        audio_filter,
        "-c:a",
        "pcm_s16le",
        str(clean_wav),
    ]
    run(cmd_clean)

    print("OK")
    print(f"RAW  : {raw_wav}")
    print(f"CLEAN: {clean_wav}")


if __name__ == "__main__":
    main()
