#音檔轉字幕檔
import argparse
from pathlib import Path
import sys

import whisper


def format_srt_timestamp(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(segments, srt_path: Path) -> None:
    lines = []
    for i, seg in enumerate(segments, start=1):
        start = format_srt_timestamp(seg["start"])
        end = format_srt_timestamp(seg["end"])
        text = (seg.get("text") or "").strip()
        lines.append(str(i))
        lines.append(f"{start} --> {end}")
        lines.append(text)
        lines.append("")
    srt_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("audio", help="Path to audio file (wav/mp3/m4a, etc.)")
    p.add_argument("--out_dir", default="out", help="Output directory")
    p.add_argument("--model", default="small", help="tiny|base|small|medium|large")
    p.add_argument("--language", default="zh", help="e.g., zh, en, auto")
    args = p.parse_args()

    audio_path = Path(args.audio).expanduser().resolve()
    if not audio_path.exists():
        print(f"[ERROR] File not found: {audio_path}")
        sys.exit(1)

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = audio_path.stem
    txt_path = out_dir / f"{stem}.txt"
    srt_path = out_dir / f"{stem}.srt"

    model = whisper.load_model(args.model)

    kwargs = {}
    if args.language.lower() != "auto":
        kwargs["language"] = args.language

    result = model.transcribe(str(audio_path), **kwargs)

    txt_path.write_text((result.get("text") or "").strip() + "\n", encoding="utf-8")
    write_srt(result.get("segments") or [], srt_path)

    print(f"[OK] TXT: {txt_path}")
    print(f"[OK] SRT: {srt_path}")


if __name__ == "__main__":
    main()
