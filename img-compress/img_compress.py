import os
import shutil
from PIL import Image
from typing import List


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size


def filter_files(start_path='.', ext="jpg"):
    files = []
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                if fp.endswith(f".{ext}"):
                    files.append({"name": f, "size": os.path.getsize(fp)})

    return files


def list_files(start_path:str = '.') -> List[dict]:
    files = []
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                files.append({"name": f, "size": os.path.getsize(fp)})

    return files


def size(file_list: List[dict]) -> int:
    size=0
    for f in file_list:
        size = size + f['size']
    return size


def convert_files(input, output):
    src = "input"
    dest = "working"
    src_files = list_files(src)

    for f in src_files:
        src_fp = os.path.join(src, f["name"])
        tgt_fname = os.path.splitext(f['name'])[0]+'.jpg'
        tgt_fp = os.path.join(dest, tgt_fname)
        img = Image.open(src_fp)
        out = img.convert("RGB")
        out.save(tgt_fp, "JPEG", optimize=True, quality=65)

    dest_files = list_files(dest)
    return src_files, dest_files


def display_size(size: int, unit: str = None) -> str:
    if unit == "KB":
        return str(round(size / 1024, 3)) + ' Kilobytes'
    elif unit == "MB":
        return str(round(size / (1024 * 1024), 3)) + ' Megabytes'
    elif unit == "GB":
        return str(round(size / (1024 * 1024 * 1024), 3)) + ' Gigabytes'
    else:
        return str(size) + ' bytes'


if __name__ == "__main__":
    src = "input"
    tgt = "working"

    shutil.rmtree(tgt)
    os.mkdir(tgt)

    src_files, tgt_files = convert_files(src, tgt)
    src_size = size(src_files)
    src_num = len(src_files)
    tgt_size = size(tgt_files)
    tgt_num = len(tgt_files)
    src_size = display_size(src_size,'MB')
    tgt_size = display_size(tgt_size,"MB")
    print(f"Source size: {src_size}, target size: {tgt_size}")
    print(f"# source files: {src_num}, # target files: {tgt_num}")