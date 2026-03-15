#!/usr/bin/env python3
import os
import subprocess
import sys


def get_m4a_files():
    m4a_files = []
    for f in sorted(os.listdir(".")):
        if f.endswith(".m4a"):
            m4a_files.append(f[:-4])
    return m4a_files


def get_existing_mp4_files():
    existing = set()
    if os.path.exists("mp4"):
        for f in os.listdir("mp4"):
            if f.endswith(".mp4"):
                existing.add(f[:-4])
    return existing


def check_txt_exists(name):
    return os.path.exists(f"txt/{name}.txt")


def check_srt_exists(name):
    return os.path.exists(f"srt/{name}.srt")


def run_cmd(cmd, desc):
    print(f"[ ] {desc}...", end=" ", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("OK")
        return True
    else:
        print("FAIL")
        if result.stderr:
            print(result.stderr)
        return False


def process_file(name):
    print(f"\nProcessing: {name}")
    os.makedirs("txt_no_punc", exist_ok=True)
    os.makedirs("txt-pdf", exist_ok=True)
    os.makedirs("txt-pdf-jpg", exist_ok=True)
    os.makedirs("mp4", exist_ok=True)
    os.makedirs("srt_punc_to_spc", exist_ok=True)

    if not run_cmd(
        ["python", "script/txt_no_punc.py", f"txt/{name}.txt", "txt_no_punc/"],
        "txt_no_punc",
    ):
        return False

    if not run_cmd(
        ["python", "script/txt_gen_pdf.py", f"txt_no_punc/{name}.txt", "txt-pdf/"],
        "txt_gen_pdf",
    ):
        return False

    if not run_cmd(
        ["typst", "compile", f"txt-pdf/{name}.typ", f"txt-pdf/{name}.pdf"],
        "typst compile",
    ):
        return False

    if not run_cmd(
        [
            "magick",
            "-density",
            "300",
            f"txt-pdf/{name}.pdf[0]",
            "-resize",
            "x1080",
            "-background",
            "white",
            "-alpha",
            "remove",
            "-quality",
            "90",
            f"txt-pdf-jpg/{name}.pdf.jpg",
        ],
        "magick convert",
    ):
        return False

    if not run_cmd(
        [
            "ffmpeg",
            "-loop",
            "1",
            "-framerate",
            "1",
            "-i",
            f"txt-pdf-jpg/{name}.pdf.jpg",
            "-i",
            f"{name}.m4a",
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-c:a",
            "copy",
            "-pix_fmt",
            "yuv420p",
            "-shortest",
            "-y",
            f"mp4/{name}.mp4",
        ],
        "ffmpeg mp4",
    ):
        return False

    if check_srt_exists(name):
        if not run_cmd(
            [
                "python",
                "script/srt_punc_to_spc.py",
                f"srt/{name}.srt",
                f"srt_punc_to_spc/{name}.srt",
            ],
            "srt process",
        ):
            return False

    print(f"[OK] {name}")
    return True


def main():
    m4a_files = get_m4a_files()
    existing_mp4 = get_existing_mp4_files()

    new_files = []
    for name in m4a_files:
        if name in existing_mp4:
            continue
        if not check_txt_exists(name):
            print(f"[SKIP] {name} (no txt)")
            continue
        new_files.append(name)

    print(f"Found {len(new_files)} new files")
    if not new_files:
        print("Nothing to do.")
        return

    success = 0
    for name in new_files:
        if process_file(name):
            success += 1

    print(f"\nDone: {success}/{len(new_files)} succeeded")


if __name__ == "__main__":
    main()
