import os

BOARDS_DIR = "/home/vasanth/Desktop/personal/linux-at91/arch/arm/boot/dts"

def list_folders(path):
    return sorted([
        name for name in os.listdir(path)
        if os.path.isdir(os.path.join(path, name))
    ])


def list_baseboards(path):
    dts_files = []
    for file in os.listdir(path):
        if file.endswith(".dts"):
            dts_files.append(file)
    return dts_files


if __name__ == "__main__":
    
