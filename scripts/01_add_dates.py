from pathlib import Path
import re

# Simple lookup: specify exact profile tags if measured in different years
DATE_MAPPING = {
    # Abramov
    "abra01": "2021-08-20",
    "abra02": "2021-08-21",
    "abra03": "2021-08-22",
    "abra04": "2021-08-23",
    "abra05": "2021-08-23",
    "abra06": "2021-08-24",
    "abra07": "2021-08-24",
    "abra08": "2021-08-24",
    "abra09": "2022-07-26",
    "abra10": "2022-07-24",
    # Golubin (Explicitly differentiate 2021 vs 2022)
    "gol01_2021": "2021-07-18",
    "gol01_2022": "2022-08-08",
    "gol01": "2021-07-18",  # fallback default
    "gol02": "2021-07-19",
    "gol03": "2021-07-19",
    "gol05": "2022-08-08",
    "gol06": "2022-08-08",
    "gol07a": "2022-08-09",
    "gol07b": "2022-08-10",
    "gol07c": "2022-08-10",
    "gol07abcd": "2022-08-10",
    "GOL08": "2022_08_11",
    "gl09": "2024-08-13",
    "gl10": "2024-08-13",
    "gl11": "2024-08-13",
    "gl12": "2024-08-13",
    # Suek
    "sue01": "2021-08-02",
    "sue02": "2021-08-02",
    "sue03": "2021-08-03",
    "sue03_v": "2021-08-03",
    "sue04": "2021-08-03",
    "sue05": "2023-07-12",
    "sue06": "2023-07-12",
    "sue07": "2024-08-18",
    "sue08": "2024-08-18",
    "sue09": "2024-08-19",
    "sue10": "2024-08-19",
    "sue11": "2024-08-19",
    "sue12": "2024-08-19",
    "sue13": "2024-08-19",
    # Yakarcha
    "yak01": "2022-08-28",
    "yak02": "2022-08-29",
    # Zulmart, Karakul, no457, Bulunkul, Kumtor, no599
    "zul01": "2023-08-09",
    "zul02": "2023-08-10",
    "zul03": "2023-08-11",
    "kar01": "2023-08-07",
    "no457_01": "2023-08-16",
    "no457_02": "2023-08-17",
    "bul01": "2023-08-05",
    "kum01": "2022-08-17",
    "kum02": "2022-08-17",
    "kum04": "2022-08-19",
    "no599": "2021-07-28",
}


def add_dates(folder_path, dry_run=True):
    directory = Path(folder_path)

    for file_path in list(directory.rglob("*.dat")):
        filename = file_path.name
        stem = file_path.stem

        # Skip if already has YYYY-MM-DD date
        if re.search(r"\d{4}-\d{2}-\d{2}", stem):
            continue

        # Check for profile name match
        parts = stem.split("_")

        # Check for profile + year (e.g., GOL01_2022)
        year_match = re.search(r"(202[1-3])", stem)
        file_year = year_match.group(1) if year_match else None

        profile_key = parts[0].lower()
        if file_year and f"{profile_key}_{file_year}" in DATE_MAPPING:
            lookup_key = f"{profile_key}_{file_year}"
        else:
            lookup_key = profile_key

        if lookup_key in DATE_MAPPING:
            date = DATE_MAPPING[lookup_key]

            # Remove old standalone year/version tags before adding full date
            cleaned_stem = re.sub(
                r"_(202[1-3]|v\d+|rms)$", "", stem, flags=re.IGNORECASE
            )
            new_filename = f"{cleaned_stem}_{date}.dat"
            new_path = file_path.parent / new_filename

            if dry_run:
                print(f"[WOULD ADD DATE] {filename} -> {new_filename}")
            else:
                file_path.rename(new_path)
                print(f"[ADDED DATE] {filename} -> {new_filename}")


if __name__ == "__main__":
    # Run in dry_run=False when ready
    add_dates("./data/raw/001_ERT/002_dat", dry_run=False)