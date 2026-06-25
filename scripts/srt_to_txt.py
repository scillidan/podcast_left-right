import argparse
import os
import re


def is_timestamp(line):
    return bool(
        re.match(
            r"\d{2}:\d{2}:\d{2}[,.]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[,.]\d{3}",
            line.strip(),
        )
    )


def is_index(line):
    return bool(re.match(r"^\d+$", line.strip()))


def process_srt(src_path, dst_path):
    with open(src_path, "rb") as f:
        raw = f.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="ignore")
    lines = text.splitlines(True)

    text_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == "" or is_index(stripped) or is_timestamp(line):
            continue
        text_lines.append(stripped)

    os.makedirs(os.path.dirname(dst_path), exist_ok=True) if os.path.dirname(
        dst_path
    ) else None
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write("".join(text_lines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract plain text from SRT subtitle files"
    )
    parser.add_argument("-i", "--input", required=True, help="Input SRT file")
    parser.add_argument("-o", "--output", required=True, help="Output text file")
    args = parser.parse_args()

    process_srt(args.input, args.output)
