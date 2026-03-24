#!/usr/bin/env python3
import argparse
import os
import re
import sys

CHINESE_PUNCT = '，。！？、；：""【】《》…——·～「」『』（）()[]{}<>/\\|@#$%^&*_-~+=`^'
ENGLISH_PUNCT = ",.!?;:'\"()[]{}<>/\\|@#$%^&*_-~+=`^"


def is_timestamp(line):
    return bool(
        re.match(
            r"\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}$", line.strip()
        )
    )


def is_index(line):
    return bool(re.match(r"^\d+$", line.strip()))


def process_content(text):
    all_punct = CHINESE_PUNCT + ENGLISH_PUNCT
    for p in all_punct:
        text = text.replace(p, " ")
    text = re.sub(r"\s+", " ", text)
    text = text.rstrip()
    return text


def process_srt(src_path, dst_path):
    with open(src_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    output = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if is_index(stripped):
            output.append(line)
            i += 1
        elif is_timestamp(line):
            output.append(line)
            i += 1
        else:
            if stripped == "":
                output.append("\n")
                i += 1
            else:
                cleaned = process_content(line)
                output.append(cleaned + "\n")
                i += 1

    os.makedirs(os.path.dirname(dst_path), exist_ok=True) if os.path.dirname(
        dst_path
    ) else None
    with open(dst_path, "w", encoding="utf-8") as f:
        f.writelines(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert SRT punctuation to spaces")
    parser.add_argument("-i", "--input", required=True, help="Input file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    args = parser.parse_args()

    process_srt(args.input, args.output)
