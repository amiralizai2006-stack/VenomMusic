import logging
import os
import sys
import time

from config import TEMP_DB_FOLDER


BASE_DIR = "/tmp/VenomX"

ASSETS_FOLDER = os.path.join(BASE_DIR, "assets")
DOWNLOADS_FOLDER = os.path.join(BASE_DIR, "downloads")
CACHE_FOLDER = os.path.join(BASE_DIR, "cache")
TEMP_DB_PATH = os.path.join(BASE_DIR, "temp_db")


def dirr():
    # Create writable directories
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)
    os.makedirs(CACHE_FOLDER, exist_ok=True)
    os.makedirs(TEMP_DB_PATH, exist_ok=True)

    # Check assets from the application directory
    if not os.path.isdir("assets"):
        logging.warning(
            "assets Folder not Found. Please clone or fork repository again."
        )

    # Clean old files from downloads
    _clean_downloads(DOWNLOADS_FOLDER)

    logging.info("Directories Updated.")


def _clean_downloads(folder):
    """Remove download files older than 1 hour."""
    try:
        now = time.time()
        cutoff = now - 3600
        removed = 0

        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)

            if os.path.isfile(filepath):
                try:
                    if os.path.getmtime(filepath) < cutoff:
                        os.remove(filepath)
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
