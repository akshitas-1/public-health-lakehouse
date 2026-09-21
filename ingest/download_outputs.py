"""Download every file under the outputs volume into docs/images/, preserving folder structure."""

from pathlib import Path

from databricks.sdk import WorkspaceClient
from dotenv import load_dotenv

VOLUME_ROOT = "/Volumes/workspace/public_health/outputs"
LOCAL_DIR = Path("docs/images")


def download_all() -> int:
    """Walk the outputs volume recursively and download each file. Returns the file count."""
    load_dotenv()
    w = WorkspaceClient()
    count = 0
    pending = [VOLUME_ROOT]
    while pending:
        directory = pending.pop()
        for entry in w.files.list_directory_contents(directory):
            if entry.is_directory:
                pending.append(entry.path)
                continue
            relative = Path(entry.path).relative_to(VOLUME_ROOT)
            local_path = LOCAL_DIR / relative
            local_path.parent.mkdir(parents=True, exist_ok=True)
            response = w.files.download(entry.path)
            local_path.write_bytes(response.contents.read())
            print(f"downloaded {relative}")
            count += 1
    return count


if __name__ == "__main__":
    n = download_all()
    print(f"done: {n} files")