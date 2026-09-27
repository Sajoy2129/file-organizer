"""Sort the files in a folder into subfolders by type.

Usage:
    python3 organize.py FOLDER            # dry run: only prints what it would do
    python3 organize.py FOLDER --apply    # actually moves the files
"""

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path

# Each category maps to the file extensions that belong in it.
CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".heic"},
    "Documents": {
        ".pdf", ".txt", ".doc", ".docx", ".xls", ".xlsx",
        ".ppt", ".pptx", ".csv", ".md", ".odt", ".rtf",
    },
    "Music": {".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg"},
    "Archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"},
}
OTHER = "Other"


def get_category(path: Path) -> str:
    """Return the category name for a file, based on its extension."""
    extension = path.suffix.lower()  # "PHOTO.JPG" -> ".jpg"
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return OTHER


def plan_moves(folder: Path) -> list[tuple[Path, Path]]:
    """Build a list of (source, destination) moves without touching the disk.

    Only regular files directly inside `folder` are included.
    Subfolders and hidden files (like .DS_Store) are skipped.
    """
    moves = []
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        destination = folder / get_category(path) / path.name
        moves.append((path, destination))
    return moves


def execute_moves(moves: list[tuple[Path, Path]], dry_run: bool) -> Counter:
    """Print each move, and perform it unless this is a dry run.

    Returns a count of how many files went to each category.
    """
    prefix = "[DRY RUN] " if dry_run else ""
    counts = Counter()

    for source, destination in moves:
        category = destination.parent.name
        category_dir = destination.parent
        if category_dir.exists() and not category_dir.is_dir():
            # A plain file already has the category folder's name,
            # so the folder can't be created.
            print(f"SKIP {source.name}: a file named {category} is in the way")
            continue
        if destination.exists():
            print(f"SKIP {source.name}: {category}/{source.name} already exists")
            continue

        print(f"{prefix}{source.name} -> {category}/")
        if not dry_run:
            destination.parent.mkdir(exist_ok=True)
            shutil.move(source, destination)
        counts[category] += 1

    return counts


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sort files in a folder into subfolders by type."
    )
    parser.add_argument("folder", type=Path, help="the folder to organize")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="actually move files (default is a dry run that only prints)",
    )
    args = parser.parse_args()

    if not args.folder.is_dir():
        sys.exit(f"Error: {args.folder} is not a folder.")

    dry_run = not args.apply
    moves = plan_moves(args.folder)
    if not moves:
        print("Nothing to organize.")
        return

    counts = execute_moves(moves, dry_run)
    summary = ", ".join(f"{name}: {n}" for name, n in sorted(counts.items()))
    verb = "Would move" if dry_run else "Moved"
    print(f"\n{verb} {sum(counts.values())} files ({summary})")
    if dry_run:
        print("This was a dry run. Add --apply to move the files.")


if __name__ == "__main__":
    main()
