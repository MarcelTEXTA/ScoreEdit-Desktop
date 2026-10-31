"""Compatibility launcher; the application lives in :mod:`scoreedit`."""

from scoreedit.app import MainWindow, main


if __name__ == "__main__":
    raise SystemExit(main())
