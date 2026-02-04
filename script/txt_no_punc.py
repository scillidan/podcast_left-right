#!/usr/bin/env python3
import os
import sys


def remove_punctuation_and_spaces(text):
    import string

    chinese_punct = (
        "，。！？、；：\"'【】《》…——·～「」『』（）()[]{}<>/·×÷+-=<>?!@#$%^&*|\\`~"
    )
    all_punct = set(string.punctuation + chinese_punct)
    result = "".join(c for c in text if c not in all_punct and not c.isspace())
    return result


def process_files(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for filename in os.listdir(src_dir):
        if filename.endswith(".txt"):
            src_path = os.path.join(src_dir, filename)
            dst_path = os.path.join(dst_dir, filename)
            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()
            cleaned = remove_punctuation_and_spaces(content)
            with open(dst_path, "w", encoding="utf-8") as f:
                f.write(cleaned)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <src_dir> <dst_dir>")
        sys.exit(1)
    process_files(sys.argv[1], sys.argv[2])
