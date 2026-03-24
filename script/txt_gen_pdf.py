#!/usr/bin/env python3
import argparse
import os
import sys


def escape_typ(s):
    return s.replace("\\", "\\\\").replace('"', '""')


def process_file(src_txt, dst_typ):
    with open(src_txt, "r", encoding="utf-8") as f:
        content = f.read()

    typ_content = f"""#set page(
  paper: "a5",
  flipped: true,
  margin: 5%,
)
#set text(font: "Sarasa Mono SC", size: 8pt)

{escape_typ(content)}
"""

    os.makedirs(os.path.dirname(dst_typ), exist_ok=True) if os.path.dirname(
        dst_typ
    ) else None
    with open(dst_typ, "w", encoding="utf-8") as f:
        f.write(typ_content)
    print(f"Generated: {dst_typ}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Typst PDF from text files")
    parser.add_argument("-i", "--input", required=True, help="Input file")
    parser.add_argument("-o", "--output", required=True, help="Output file")
    args = parser.parse_args()

    process_file(args.input, args.output)
