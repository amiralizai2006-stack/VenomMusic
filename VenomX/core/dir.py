# All rights reserved.
#
import logging
import os
import sys
import time

from config import TEMP_DB_FOLDER


def dirr():
    assets_folder = "assets"

    # Deplexo uses a read-only application filesystem.
    # /tmp is writable and suitable for temporary runtime files.
    runtime_folder = "/tmp/VenomX"

    downloads_folder = os.path.join(runtime_folder, "downloads")
    cache_folder = os.path.join(runtime_folder, "cache")
    temp_db_folder = os.path.join(runtime_folder, "temp_db")

    # Assets are part of the repository and should already exist.
    if not os.path.isdir(assets_folder):
        logging.warning(
            f"{assets_folder} Folder not Found. Please clone or fork repository again."
        )
        sys.exit()

    # Create writable runtime directories.
    os.makedirs(downloads_folder, exist_ok=True)
    os.makedirs(cache_folder, exist_ok=True)
    os.makedirs(temp_db_folder, exist_ok=True)

    # Clean stale downloads older than 1 hour.
    _clean_downloads(downloads_folder)

    logging.info("Directories Updated.")


def _clean_downloads(folder):
    """Remove download files older than 1 hour to prevent disk fill."""
    try:
        now = time.time()
        cutoff = now - 3600
        removed = 0

        for f in os.listdir(folder):
            fp = os.path.join(folder, f)

            if os.path.isfile(fp):
                try:
                    mtime = os.path.getmtime(fp)

                    if mtime < cutoff:
                        os.remove(fp)
                        removed += 1

                except Exception:
                    pass

        if removed:
            logging.info(
                f"Cleaned {removed} stale download(s) from {folder}"
            )

    except Exception as e:
        logging.warning(f"Download cleanup failed: {e}")


if __name__ == "__main__":
    dirr()
