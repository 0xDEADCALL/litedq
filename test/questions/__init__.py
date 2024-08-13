from pathlib import Path
from zipfile import ZipFile

# Extremely crackhead way of doing this,
# but it should work for now, do NOT replicate in any other system

# Find where are we
current_path = Path(__file__).parent.resolve()

# AWS Glue imports directly from zip file,
# and glob won't read the contents, thus we need to scan the zip
# to exec the scripts
# We're in zip file
if current_path.is_file() and current_path.suffix == ".zip":
    archive = ZipFile(current_path, "r")

    for f in archive.namelist():
        basename = Path(f).name

        if basename.endswith(".py") and not basename.startswith("_"):
            exec(archive.read(f))

# We're in dir
elif current_path.is_dir():
    modules = [
        f
        for f in Path(__file__).parent.resolve().rglob("*.py")
        if not f.name.startswith("_")
    ]

    for f in [str(m) for m in modules]:
        exec(open(f).read())
