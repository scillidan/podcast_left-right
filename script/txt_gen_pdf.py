#!/usr/bin/env python3
import os
import sys


def escape_typ(s):
    return s.replace("\\", "\\\\").replace('"', '""')


def process_file(src_txt, dst_dir):
    filename = os.path.basename(src_txt)
    dst_typ = os.path.join(dst_dir, filename.replace(".txt", ".typ"))

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

    os.makedirs(dst_dir, exist_ok=True)
    with open(dst_typ, "w", encoding="utf-8") as f:
        f.write(typ_content)
    print(f"Generated: {dst_typ}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <src_txt_dir> <dst_dir>")
        sys.exit(1)
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]

    for filename in os.listdir(src_dir):
        if filename.endswith(".txt"):
            src_path = os.path.join(src_dir, filename)
            process_file(src_path, dst_dir)
