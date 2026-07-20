import re
from pathlib import Path


def clean_profile_name(raw_prefix):
    """Strips out redundant array tags (W5m, DD5m), standalone years (2021), and version/processing suffixes (H, rms, v1) from the raw prefix so only the clean profile name remains."""
    # List of common noise/redundant patterns to strip from the profile prefix
    patterns = [
        r"_(W|DD)\d+m",  # e.g. _W5m, _DD5m
        r"_\d{4}",  # e.g. _2021
        r"_(H|rms|v\d+)",  # e.g. _H, _rms, _v1
        r"_(RA\d+)+",  # e.g. _RA1_RA2
    ]

    cleaned = raw_prefix
    for pat in patterns:
        cleaned = re.sub(pat, "", cleaned, flags=re.IGNORECASE)

    return cleaned.strip("_")


def reformat_structure(folder_path, dry_run=True):
    directory = Path(folder_path)

    print(f"--- Running in {'DRY-RUN' if dry_run else 'REAL'} mode ---\n")

    for file_path in list(directory.rglob("*.dat")):
        filename = file_path.name
        stem = file_path.stem

        # Extract date (YYYY-MM-DD)
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", stem)

        if not date_match:
            print(f"[SKIPPED - NO DATE] {filename}")
            continue

        date = date_match.group(1)

        # Everything before the date contains the profile name and possibly old tags
        before_date = stem[: date_match.start()].strip("_")
        after_date = stem[date_match.end() :].strip("_")

        # Clean the profile prefix so 'gol02_W5m_2021_H' becomes just 'gol02' or 'GOL02'
        clean_profile = clean_profile_name(before_date)

        # Inspect the entire original stem to correctly preserve DD vs W and spacing (3m vs 5m)
        full_text = f"{before_date}_{after_date}"
        config = "DD" if "dd" in full_text.lower() else "W"

        spacing_match = re.search(r"(\d+)m", full_text, re.IGNORECASE)
        spacing = spacing_match.group(1) if spacing_match else "5"

        # Build exact unified structure: <CLEAN_PROFILE>_<YYYY-MM-DD>_<CONFIG><SPACING>m.dat
        new_filename = f"{clean_profile}_{date}_{config}{spacing}m.dat"
        new_path = file_path.parent / new_filename

        if filename == new_filename:
            print(f"[UNCHANGED] {filename}")
        elif new_path.exists() and new_path != file_path:
            print(f"[COLLISION SKIPPED] {filename} -> {new_filename} exists!")
        elif dry_run:
            print(f"[WOULD REFORMAT] {filename} -> {new_filename}")
        else:
            file_path.rename(new_path)
            print(f"[REFORMATTED] {filename} -> {new_filename}")


if __name__ == "__main__":
    TARGET_FOLDER = "./data/raw/001_ERT/002_dat"

    # Set dry_run=False when you are ready to apply the changes
    reformat_structure(TARGET_FOLDER, dry_run=False)