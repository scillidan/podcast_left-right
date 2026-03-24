#!/usr/bin/env python3
import argparse
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


def process_file(src_path, dst_path):
    with open(src_path, "r", encoding="utf-8") as f:
        content = f.read()
    cleaned = remove_punctuation_and_spaces(content)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True) if os.path.dirname(
        dst_path
    ) else None
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(cleaned)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove punctuation and spaces from text files"
    )
    parser.add_argument("-i", "--input", required=True, help="Input file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    args = parser.parse_args()

    process_file(args.input, args.output)
