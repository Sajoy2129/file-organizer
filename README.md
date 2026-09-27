# File Organizer

A small Python script that sorts the files in a folder into subfolders by type.

```
my_folder/                    my_folder/
├── photo.jpg                 ├── Images/photo.jpg
├── report.pdf       ──►      ├── Documents/report.pdf
├── song.mp3                  ├── Music/song.mp3
└── backup.zip                └── Archives/backup.zip
```

It is **safe by default**: without `--apply`, it only prints what it *would* do.

## Categories

| Folder    | Extensions |
|-----------|------------|
| Images    | `.jpg .jpeg .png .gif .bmp .webp .svg .heic` |
| Documents | `.pdf .txt .doc .docx .xls .xlsx .ppt .pptx .csv .md .odt .rtf` |
| Music     | `.mp3 .wav .flac .aac .m4a .ogg` |
| Archives  | `.zip .tar .gz .rar .7z .bz2` |
| Other     | anything else |

Extensions are matched case-insensitively (`PHOTO.JPG` is an Image).

## Usage

Requires Python 3.9+. The script itself uses only the standard library.

```bash
# Preview (dry run): prints the plan, moves nothing
python3 organize.py path/to/folder

# Actually move the files
python3 organize.py path/to/folder --apply
```

Example dry-run output:

```
[DRY RUN] family_dinner.jpg -> Images/
[DRY RUN] invoice_march.pdf -> Documents/
...
Would move 20 files (Archives: 4, Documents: 8, Images: 4, Music: 4)
This was a dry run. Add --apply to move the files.
```

### What it does and doesn't touch

- Only files directly inside the folder are moved. Subfolders are left alone.
- Hidden files (like `.DS_Store`) are skipped.
- If a file with the same name already exists in the destination, it is
  **skipped, never overwritten**.
- Running it again is safe: already-sorted files are not moved again.
- There is no undo. Always do a dry run first.

## Running the tests

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```

The tests use temporary folders, so they never touch your real files.

## Project layout

```
organize.py            the script
tests/                 pytest tests
pytest.ini             pytest settings
requirements-dev.txt   development dependencies (pytest)
sample_downloads/      fake files for trying it out (not in git)
```

## Known limitations

- A file with no extension named `Other` (or `other` on macOS) crashes the
  script with `FileExistsError`, because it collides with the `Other/`
  folder the script tries to create.
