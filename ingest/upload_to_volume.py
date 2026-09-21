"""Upload every file under data/raw/ to the Unity Catalog volume, preserving folder structure."""

from pathlib import Path

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

LOCAL_RAW = Path("data/raw")
VOLUME_ROOT = "/Volumes/workspace/public_health/raw"


def upload_all() -> int:
    """Upload each local raw file to the volume. Returns the number of files uploaded."""
    load_dotenv()
    w = WorkspaceClient()
    count = 0
    for local_path in sorted(LOCAL_RAW.rglob("*")):
        if not local_path.is_file():
            continue
        relative = local_path.relative_to(LOCAL_RAW)
        remote_path = f"{VOLUME_ROOT}/{relative.as_posix()}"
        with local_path.open("rb") as f:
            w.files.upload(remote_path, f, overwrite=True)
        size_mb = local_path.stat().st_size / 1_000_000
        print(f"uploaded {relative} ({size_mb:.1f} MB)")
        count += 1
    return count


if __name__ == "__main__":
    n = upload_all()
    print(f"done: {n} files")