def choose_best_audio_format(formats: list[dict]) -> dict | None:
    candidates = []

    for f in formats:
        vcodec = (f.get("vcodec") or "").lower()
        if vcodec not in ("", "none"):
            continue

        abr = f.get("abr") or f.get("tbr") or 0
        filesize = f.get("filesize") or f.get("filesize_approx") or 0
        candidates.append((abr or 0, filesize or 0, f))

    if not candidates:
        return None

    _, _, best = max(candidates, key=lambda x: (x[0], x[1]))
    return best
