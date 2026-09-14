"""Central logging configuration for the RAG backend."""
import logging
import sys


def configure_logging(level: int = logging.INFO) -> None:
    """Configure a simple, consistent logging format for the whole app.

    Call this once, at process startup (see app.main lifespan).
    """
    root = logging.getLogger()
    if root.handlers:
        # Already configured (e.g. re-imported during tests/reload) — don't duplicate handlers.
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    )
    root.addHandler(handler)
    root.setLevel(level)

    # Keep noisy third-party loggers at a saner level.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)


logger = logging.getLogger("iti_studymate")
