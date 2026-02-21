import os
from pathlib import Path
import re
import unicodedata

_WINDOWS_RESERVED = {"CON", "PRN", "AUX", "NUL"}
_WINDOWS_RESERVED.update({f"COM{i}" for i in range(1, 10)})
_WINDOWS_RESERVED.update({f"LPT{i}" for i in range(1, 10)})

_INVALID_CHARS_RE = re.compile(r'[\x00-\x1f<>:"/\\|?*]')


def sanitize_path(
    path: Path | str,
    replacement: str = "_",
    max_component_length: int = 255,
) -> Path:
    p = Path(path)

    parts = p.parts
    anchor_parts_count = 0
    if p.anchor and parts and parts[0] == p.anchor:
        anchor_parts_count = 1
        anchor_part = parts[0]
    else:
        anchor_part = None

    def _sanitize_component(comp: str) -> str:
        if comp in (".", ".."):
            return comp

        comp = unicodedata.normalize("NFC", comp)
        comp = _INVALID_CHARS_RE.sub(replacement, comp)
        comp = comp.replace("\x00", replacement)
        comp = re.sub(r"[ \.]+$", lambda m: replacement * len(m.group(0)), comp)

        if not comp:
            return replacement

        stem, ext = os.path.splitext(comp)
        if stem.upper() in _WINDOWS_RESERVED:
            stem = stem + replacement
            comp = stem + ext

        if len(comp) > max_component_length:
            stem, ext = os.path.splitext(comp)
            available = max_component_length - len(ext)
            if available <= 0:
                comp = comp[:max_component_length]
            else:
                comp = stem[:available] + ext

        if not comp:
            return replacement

        return comp

    sanitized_components: list[str] = []
    for i, comp in enumerate(parts):
        if i < anchor_parts_count:
            continue

        sanitized_components.append(_sanitize_component(comp))

    if anchor_part is not None:
        rebuilt = (
            Path(anchor_part, *sanitized_components)
            if sanitized_components
            else Path(anchor_part)
        )
    else:
        rebuilt = Path(*sanitized_components) if sanitized_components else Path(".")

    return rebuilt


def sanitize_filename(name: str | Path, replacement: str = "_", max_length: int = 255) -> str:
    if isinstance(name, Path):
        name = name.name

    name = unicodedata.normalize("NFC", name)

    leading_dot = False
    if name.startswith(".") and name not in (".", ".."):
        leading_dot = True
        name_body = name[1:]
    else:
        name_body = name

    name_body = _INVALID_CHARS_RE.sub(replacement, name_body)
    name_body = name_body.replace("\x00", replacement)
    name_body = re.sub(r"[ \.]+$", lambda m: replacement * len(m.group(0)), name_body)

    if not name_body:
        name_body = replacement

    if leading_dot:
        candidate = "." + name_body
    else:
        candidate = name_body

    stem, ext = os.path.splitext(candidate)
    compare_stem = stem[1:] if (leading_dot and stem.startswith(".")) else stem
    if compare_stem.upper() in _WINDOWS_RESERVED:
        if leading_dot and stem.startswith("."):
            stem = "." + (compare_stem + replacement)
        else:
            stem = compare_stem + replacement
        candidate = stem + ext

    if len(candidate) > max_length:
        stem, ext = os.path.splitext(candidate)
        avail = max_length - len(ext)
        if avail <= 0:
            candidate = candidate[:max_length]
        else:
            candidate = stem[:avail] + ext

    if not candidate or candidate in (".", ".."):
        candidate = replacement

    return candidate
