import re
from pathlib import Path


def sync_txt_filenames(dat_folder, txt_folder, dry_run=True):
    dat_dir = Path(dat_folder)
    txt_dir = Path(txt_folder)

    if not dat_dir.exists() or not txt_dir.exists():
        print("Error: One or both folder paths do not exist!")
        return

    print(f"--- Running in {'DRY-RUN' if dry_run else 'REAL'} mode ---\n")

    # Step 1: Index all standardized .dat files by their lowercased base profile name
    # e.g., 'sue05' -> 'SUE05_2023-07-12_DD5m'
    dat_reference = {}

    for dat_path in dat_dir.rglob("*.dat"):
        stem = dat_path.stem  # e.g. SUE05_2023-07-12_DD5m
        parts = stem.split("_")

        # Extract profile key (e.g. 'sue05' or 'no457_01')
        if len(parts) >= 2 and re.match(r"^\d+$", parts[1]):
            profile_key = f"{parts[0]}_{parts[1]}".lower()
        else:
            profile_key = parts[0].lower()

        dat_reference[profile_key] = stem

    # Step 2: Iterate over all txt/data files in the target folder
    # Matches files ending in _rhoa or _topo (with or without extension)
    for txt_path in list(txt_dir.rglob("*")):
        if txt_path.is_dir():
            continue

        filename = txt_path.name
        stem = txt_path.stem  # e.g. SUE07_W5m_rhoa or yak02_W5m_rms_rhoa
        extension = txt_path.suffix  # e.g. .txt or empty

        # Detect whether it's a _rhoa or _topo file
        suffix_match = re.search(r"_(rhoa|topo)$", stem, re.IGNORECASE)
        if not suffix_match:
            print(f"[SKIPPED] {filename} (Does not end in _rhoa or _topo)")
            continue

        data_type = suffix_match.group(
            1
        ).lower()  # 'rhoa' or 'topo' (preserves lowercase)
        before_suffix = stem[: suffix_match.start()]  # e.g. yak02_W5m_rms

        # Extract profile key from the prefix
        parts = before_suffix.split("_")
        if len(parts) >= 2 and re.match(r"^\d+$", parts[1]):
            profile_key = f"{parts[0]}_{parts[1]}".lower()
        else:
            profile_key = parts[0].lower()

        # Check if we have a matching .dat reference for this profile
        if profile_key in dat_reference:
            matched_dat_stem = dat_reference[profile_key]

            # Construct final filename: <DAT_STEM>_<rhoa/topo><EXTENSION>
            new_filename = f"{matched_dat_stem}_{data_type}{extension}"
            new_path = txt_path.parent / new_filename

            if filename == new_filename:
                print(f"[UNCHANGED] {filename}")
            elif new_path.exists() and new_path != txt_path:
                print(
                    f"[COLLISION SKIPPED] {filename} -> {new_filename} already exists!"
                )
            elif dry_run:
                print(f"[WOULD RENAME] {filename} -> {new_filename}")
            else:
                txt_path.rename(new_path)
                print(f"[RENAMED] {filename} -> {new_filename}")
        else:
            print(
                f"[SKIPPED - NO MATCH] {filename} (No matching .dat reference for key '{profile_key}')"
            )


if __name__ == "__main__":
    # Adjust paths to match your folder locations
    DAT_FOLDER = "./data/raw/001_ERT/002_dat"  # Path to the folder containing your corrected .dat files
    TXT_FOLDER = "./data/raw/001_ERT/003_udf"  # Path to the folder containing the _rhoa / _topo files

    # Run in dry_run=False when ready to execute
    sync_txt_filenames(DAT_FOLDER, TXT_FOLDER, dry_run=False)