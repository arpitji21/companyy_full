"""Upload validation: size limits, real content-based file-type checks, and
basic virus scanning.

Two layers of "is this actually what it claims to be" here matter more than
either alone:

1. Extension check — a fast, obvious blocklist/allowlist against the
   filename the client sent (which the client fully controls, so this
   alone proves nothing).
2. Content sniffing (python-magic/libmagic) — looks at the actual bytes,
   independent of filename or the client-supplied Content-Type header, so
   an executable renamed to "invoice.pdf" is still caught: it sniffs as
   application/x-dosexec, not application/pdf, and gets rejected.

Virus scanning is layered similarly:

1. EICAR signature check — always runs, no configuration required. The
   EICAR test file (https://www.eicar.org/) is a standard, harmless string
   every real antivirus product recognizes; checking for it here means
   this integration is verifiably wired up correctly even in local dev/CI
   with no ClamAV container running.
2. ClamAV daemon (clamd) — if CLAMD_HOST is configured, every upload's
   bytes are streamed to clamd over its documented INSTREAM protocol for a
   real scan. This is the one control in this module that fails *closed*:
   if clamd is configured but unreachable, the upload is rejected rather
   than silently skipping the scan (unlike S3/SMTP elsewhere in this app,
   where missing config means "feature not in use yet" — here, configured
   clamd is a security control and its being down shouldn't quietly
   disable that control for uploads).
"""
from __future__ import annotations

import socket
import struct

import magic

from app.core.config import settings
from app.core.exceptions import (
    FileTooLargeError,
    ScanUnavailableError,
    UnsupportedFileTypeError,
    VirusDetectedError,
)
from app.core.logging import logger

# Extensions never allowed, regardless of what the sniffed content type
# turns out to be — defense in depth alongside the content sniff below.
DANGEROUS_EXTENSIONS = {
    ".exe", ".dll", ".bat", ".cmd", ".com", ".scr", ".msi", ".msp",
    ".sh", ".bash", ".ps1", ".psm1", ".vbs", ".vbe", ".js", ".jse",
    ".jar", ".apk", ".app", ".bin", ".iso", ".deb", ".rpm", ".dmg",
}

# Extensions this "documents" feature accepts.
ALLOWED_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".csv", ".txt", ".json", ".zip",
    ".png", ".jpg", ".jpeg", ".gif", ".webp",
}

# MIME types libmagic may report for the extensions above. Office formats
# (docx/xlsx/pptx) are zip containers, so libmagic sometimes reports them
# as generic "application/zip" rather than the specific OOXML type — that's
# expected and allowed here since the earlier extension check already
# narrows down which zip-shaped file this claims to be.
ALLOWED_SNIFFED_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "text/csv",
    "text/plain",
    "application/json",
    "application/zip",
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
}

# The standard EICAR antivirus test string (see https://www.eicar.org/) —
# every real AV engine recognizes this exact string as "malware" by
# convention; it contains no actual malicious code. Checking for it lets
# this integration be tested end-to-end without a real virus sample.
_EICAR_SIGNATURE = b"EICAR-STANDARD-ANTIVIRUS-TEST-FILE"

_MAGIC_SNIFF_BYTES = 4096  # libmagic only needs the file's leading bytes


def _extension_of(filename: str) -> str:
    if "." not in filename:
        return ""
    return "." + filename.rsplit(".", 1)[-1].lower()


def validate_file_size(size_bytes: int) -> None:
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        raise FileTooLargeError(
            f"File is {size_bytes / (1024 * 1024):.1f} MB, which exceeds the "
            f"{settings.MAX_UPLOAD_SIZE_MB} MB limit."
        )


def validate_file_type(filename: str, data: bytes) -> str:
    """Checks the filename's extension and the file's actual sniffed
    content type against the allowlists above. Returns the sniffed MIME
    type on success (the caller should trust this over any Content-Type
    header the client sent)."""
    ext = _extension_of(filename)

    if ext in DANGEROUS_EXTENSIONS:
        raise UnsupportedFileTypeError(f"Files with extension '{ext}' are not allowed.")
    if ext not in ALLOWED_EXTENSIONS:
        raise UnsupportedFileTypeError(
            f"Files with extension '{ext or '(none)'}' are not allowed. "
            f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}."
        )

    sniffed_mime = magic.from_buffer(data[:_MAGIC_SNIFF_BYTES], mime=True)
    if sniffed_mime not in ALLOWED_SNIFFED_MIME_TYPES:
        raise UnsupportedFileTypeError(
            f"File content doesn't match an allowed type (detected: {sniffed_mime}). "
            "This can happen if the file extension doesn't match its actual contents."
        )

    return sniffed_mime


def _clamd_scan(data: bytes) -> None:
    """Streams `data` to clamd over its INSTREAM protocol. Raises
    VirusDetectedError if clamd reports a match, ScanUnavailableError if
    clamd can't be reached at all (fails closed — see module docstring)."""
    try:
        sock = socket.create_connection(
            (settings.CLAMD_HOST, settings.CLAMD_PORT), timeout=settings.CLAMD_TIMEOUT_SECONDS
        )
    except OSError:
        logger.exception("Could not connect to clamd at %s:%s.", settings.CLAMD_HOST, settings.CLAMD_PORT)
        raise ScanUnavailableError(
            "Virus scanning is temporarily unavailable. Please try again shortly."
        )

    try:
        sock.sendall(b"zINSTREAM\0")
        chunk_size = 8192
        for i in range(0, len(data), chunk_size):
            chunk = data[i : i + chunk_size]
            sock.sendall(struct.pack("!L", len(chunk)) + chunk)
        sock.sendall(struct.pack("!L", 0))  # zero-length chunk ends the stream

        response = b""
        while True:
            part = sock.recv(4096)
            if not part:
                break
            response += part
            if b"\0" in response:
                break
    except OSError:
        logger.exception("clamd scan failed while streaming data.")
        raise ScanUnavailableError(
            "Virus scanning is temporarily unavailable. Please try again shortly."
        )
    finally:
        sock.close()

    text = response.decode("utf-8", errors="replace").replace("\x00", "").strip()
    if "FOUND" in text:
        signature = text.split(":", 1)[-1].replace("FOUND", "").strip()
        logger.warning("clamd flagged an upload: %s", text)
        raise VirusDetectedError(f"This file was flagged by antivirus scanning ({signature}).")
    if "ERROR" in text:
        logger.error("clamd returned an error scanning an upload: %s", text)
        raise ScanUnavailableError("Virus scanning failed. Please try again.")


def scan_for_virus(data: bytes) -> None:
    """Raises VirusDetectedError if `data` looks malicious, ScanUnavailableError
    if a configured scanner couldn't be reached. Returns None (no exception)
    if the file is clean."""
    if _EICAR_SIGNATURE in data:
        logger.warning("Upload matched the EICAR antivirus test signature; rejecting.")
        raise VirusDetectedError("This file was flagged by antivirus scanning (EICAR test signature).")

    if settings.CLAMD_HOST:
        _clamd_scan(data)
